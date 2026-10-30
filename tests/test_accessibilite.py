"""Tests de `accessibilite.indicateurs` sur des communes et des lycées jouets (PLAN §2.4, §4 D).

Coordonnées en mètres, en Lambert 93, décalées d'une origine proche de Rennes : chaque
distance attendue se calcule de tête.
"""

import geopandas as gpd
import numpy as np
import pytest
from shapely.geometry import Point, Polygon, box

from cadres_lycees import accessibilite, config

X0, Y0 = 350_000, 6_790_000


def point(dx: float, dy: float) -> Point:
    """Point situé à (dx, dy) mètres de l'origine jouet."""
    return Point(X0 + dx, Y0 + dy)


def rectangle(xmin: float, ymin: float, xmax: float, ymax: float) -> Polygon:
    """Contour rectangulaire, en mètres depuis l'origine jouet."""
    return box(X0 + xmin, Y0 + ymin, X0 + xmax, Y0 + ymax)


def communes_jouets(lignes: list[tuple[str, Polygon, Point]]) -> gpd.GeoDataFrame:
    """Communes à partir de triplets (code_commune, contour, centroïde)."""
    codes, contours, centroides = zip(*lignes, strict=True)
    return gpd.GeoDataFrame(
        {
            "code_commune": list(codes),
            "centroide": gpd.GeoSeries(centroides, crs=config.CRS_CALCUL),
        },
        geometry=list(contours),
        crs=config.CRS_CALCUL,
    )


def commune_unique() -> gpd.GeoDataFrame:
    """Une commune A de 2 km de côté, centrée sur l'origine."""
    return communes_jouets([("A", rectangle(-1000, -1000, 1000, 1000), point(0, 0))])


def lycees(*decalages: tuple[float, float]) -> gpd.GeoDataFrame:
    """Lycées jouets aux décalages (dx, dy) donnés, en mètres."""
    return gpd.GeoDataFrame(geometry=[point(dx, dy) for dx, dy in decalages], crs=config.CRS_CALCUL)


def test_bord_du_rayon():
    """Un lycée à exactement 5 km compte à 5 km, un lycée à 5 000,5 m ne compte pas.

    Une zone tampon (polygone inscrit dans le cercle) ou une inégalité stricte perdrait le
    lycée du bord sans aucun signal.
    """
    resultat = accessibilite.indicateurs(
        commune_unique(), lycees((3000, 4000), (5000.5, 0)), "lyc_prive"
    )

    ligne = resultat.loc["A"]
    assert ligne["n_lyc_prive_3km"] == 0  # 5 km > 3 km
    assert ligne["n_lyc_prive_5km"] == 1  # triangle 3-4-5 : 5 000 m pile, compté ; 5 000,5 m non
    assert ligne["n_lyc_prive_10km"] == 2
    assert ligne["dist_lyc_prive_min"] == pytest.approx(5.0)  # en km, pas en mètres


def test_distance_depuis_le_centroide_et_non_le_contour():
    """Le point de référence est la colonne `centroide`, ni le contour ni un centre recalculé.

    Le centroïde fourni (0, 0) n'est pas le centre du rectangle, (2 000, 0) : c'est le cas du
    chef-lieu en robustesse (§2.4). Le lycée est sur le bord est du contour.
    """
    communes = communes_jouets([("A", rectangle(-3000, -1000, 7000, 1000), point(0, 0))])

    resultat = accessibilite.indicateurs(communes, lycees((7000, 0)), "lyc_prive")

    ligne = resultat.loc["A"]
    # 7 km depuis le centroïde ; on trouverait 0 km depuis le contour, 5 km depuis le centre
    assert ligne["n_lyc_prive_5km"] == 0
    assert ligne["n_lyc_prive_10km"] == 1
    assert ligne["dist_lyc_prive_min"] == pytest.approx(7.0)


def test_plusieurs_communes_dont_une_sans_lycee():
    """Un lycée compte pour chaque commune qui l'a dans son rayon ; C, sans lycée à 10 km, garde
    sa ligne, des comptes à 0 et sa vraie distance au plus proche.

    Rattacher chaque lycée à une seule commune, ou ne chercher le plus proche que dans le plus
    grand rayon, fausserait B ou C sans aucun signal.
    """
    communes = communes_jouets(
        [
            ("A", rectangle(-2000, -2000, 2000, 2000), point(0, 0)),
            ("B", rectangle(2000, -2000, 6000, 2000), point(4000, 0)),
            ("C", rectangle(-2000, 28000, 2000, 32000), point(0, 30000)),
        ]
    )

    resultat = accessibilite.indicateurs(communes, lycees((2000, 0), (0, 4000)), "lyc_prive")

    resultat = resultat.sort_index()
    assert list(resultat.index) == ["A", "B", "C"]
    # (2000, 0) est à 2 km de A et de B ; (0, 4000) à 4 km de A et à 4√2 ≈ 5,66 km de B
    assert resultat["n_lyc_prive_3km"].tolist() == [1, 1, 0]
    assert resultat["n_lyc_prive_5km"].tolist() == [2, 1, 0]
    assert resultat["n_lyc_prive_10km"].tolist() == [2, 2, 0]
    # C : le plus proche est (0, 4000), à 30 - 4 = 26 km, au-delà du plus grand rayon
    assert resultat["dist_lyc_prive_min"].tolist() == pytest.approx([2.0, 2.0, 26.0])


def test_coordonnees_en_degres_refusees():
    """Des lycées ou des centroïdes en WGS84 donneraient des distances en degrés, sans signal.

    Le second cas est celui du chef-lieu en robustesse (§2.4) : seule la colonne `centroide`
    est en degrés, les contours restent en Lambert 93.
    """
    lycees_wgs84 = lycees((0, 4000)).to_crs(config.CRS_CARTES)
    with pytest.raises(AssertionError, match="EPSG"):
        accessibilite.indicateurs(commune_unique(), lycees_wgs84, "lyc_prive")

    communes = commune_unique()
    communes["centroide"] = communes["centroide"].to_crs(config.CRS_CARTES)
    with pytest.raises(AssertionError, match="EPSG"):
        accessibilite.indicateurs(communes, lycees((0, 4000)), "lyc_prive")


def test_moyenne_ponderee_sans_les_valeurs_manquantes():
    """La moyenne de l'attribut est pondérée par `poids`, bord du rayon compris ; un lycée sans
    valeur reste compté mais sort de la moyenne, au numérateur comme au dénominateur.

    Une moyenne simple, ou le poids du lycée sans valeur laissé au dénominateur, donnerait un
    `ival_moy_5km` plausible et faux.
    """
    lycees_ival = gpd.GeoDataFrame(
        {"ival": [4.0, 1.0, np.nan], "poids_ival": [3.0, 1.0, 2.0]},
        geometry=[point(3000, 4000), point(0, 1000), point(0, 2000)],
        crs=config.CRS_CALCUL,
    )

    resultat = accessibilite.indicateurs(
        commune_unique(), lycees_ival, "lyc", attribut="ival", poids="poids_ival"
    )

    ligne = resultat.loc["A"]
    assert ligne["n_lyc_3km"] == 2  # le lycée sans valeur, à 2 km, reste compté
    assert ligne["n_lyc_5km"] == 3
    # 3 km : seul le lycée à 1 km a une valeur ; 1/3 si le poids 2 restait au dénominateur
    assert ligne["ival_moy_3km"] == pytest.approx(1.0)
    # 5 km, bord compris : (4×3 + 1×1) / (3 + 1) = 3,25 ; moyenne simple 2,5 ; bord exclu 1
    assert ligne["ival_moy_5km"] == pytest.approx(3.25)


def test_moyenne_manquante_sans_valeur_dans_le_rayon():
    """Sans lycée renseigné dans le rayon, la moyenne est manquante et jamais 0 : un 0 se lirait
    comme une valeur ajoutée nulle.
    """
    communes = communes_jouets(
        [
            ("A", rectangle(-2000, -2000, 2000, 2000), point(0, 0)),
            ("C", rectangle(-2000, 28000, 2000, 32000), point(0, 30000)),
        ]
    )
    lycees_ival = gpd.GeoDataFrame(
        {"ival": [np.nan, 2.0], "poids_ival": [1.0, 1.0]},
        geometry=[point(0, 2000), point(0, 4000)],
        crs=config.CRS_CALCUL,
    )

    resultat = accessibilite.indicateurs(
        communes, lycees_ival, "lyc", attribut="ival", poids="poids_ival"
    )

    # A : à 3 km, un seul lycée, sans valeur ; à 5 km, le lycée à 4 km (valeur 2) entre
    assert np.isnan(resultat.loc["A", "ival_moy_3km"])
    assert resultat.loc["A", "ival_moy_5km"] == pytest.approx(2.0)
    # C : le lycée le plus proche est à 30 - 4 = 26 km
    assert resultat.loc["C", ["ival_moy_3km", "ival_moy_5km", "ival_moy_10km"]].isna().all()
