"""Tests de `geo.paires_contigues` sur des communes jouets (PLAN §4 F, §5.3).

Communes carrées de 1 km de côté sur une grille en Lambert 93, décalée d'une origine proche
de Rennes : chaque contact se voit sur un dessin.
"""

import math

import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import Polygon, box

from cadres_lycees import config, geo

X0, Y0 = 350_000, 6_790_000
COTE = 1000


def carre(colonne: int, ligne: int) -> Polygon:
    """Carré de 1 km de côté à la case (colonne, ligne) de la grille jouet."""
    x, y = X0 + colonne * COTE, Y0 + ligne * COTE
    return box(x, y, x + COTE, y + COTE)


def communes_jouets(
    lignes: list[tuple[str, str, Polygon]], **colonnes: list[float]
) -> gpd.GeoDataFrame:
    """Communes à partir de triplets (code_commune, aire, contour) et de colonnes numériques."""
    codes, aires, contours = zip(*lignes, strict=True)
    return gpd.GeoDataFrame(
        {"code_commune": list(codes), "aire": list(aires), **colonnes},
        geometry=list(contours),
        crs=config.CRS_CALCUL,
    )


def triees(paires: pd.DataFrame) -> pd.DataFrame:
    """Paires dans l'ordre des codes, puisque l'ordre des lignes n'est pas spécifié."""
    return paires.sort_values(["code_commune_i", "code_commune_j"]).reset_index(drop=True)


def test_grille_2x2_contiguite_queen():
    """Sur une grille 2 × 2, les 6 paires sortent, chacune une fois, diagonales comprises.

    Une contiguïté par les bords seuls (« Rook ») perdrait les 2 diagonales ; une matrice de
    voisinage lue sans le filtre i < j donnerait chaque paire deux fois, et sa diagonale des
    paires (i, i). Aucun de ces écarts ne lèverait d'erreur.
    """
    communes = communes_jouets(
        [
            ("35004", "Rennes", carre(0, 1)),  # nord-ouest
            ("35003", "Rennes", carre(1, 1)),  # nord-est
            ("35002", "Rennes", carre(0, 0)),  # sud-ouest
            ("35001", "Rennes", carre(1, 0)),  # sud-est
        ],
        part_cadres_2022=[0.40, 0.30, 0.20, 0.10],
    )

    paires = triees(geo.paires_contigues(communes, ["part_cadres_2022"]))

    assert paires[["code_commune_i", "code_commune_j"]].to_numpy().tolist() == [
        ["35001", "35002"],  # bord sud
        ["35001", "35003"],  # bord est
        ["35001", "35004"],  # diagonale : un seul point commun, le centre de la grille
        ["35002", "35003"],  # diagonale
        ["35002", "35004"],  # bord ouest
        ["35003", "35004"],  # bord nord
    ]
    assert paires["aire"].tolist() == ["Rennes"] * 6


def test_ecarts_i_moins_j_sur_les_bonnes_lignes():
    """`d_<v>` vaut la valeur de i moins celle de j, i étant le plus petit code.

    Les codes ne suivent ni l'ordre des lignes ni l'ordre ouest-est, la commune du milieu est
    tantôt i, tantôt j, et l'index est celui d'un tableau trié. Un écart j - i, une valeur lue
    à la mauvaise ligne (une position prise pour une étiquette) ou deux variables interverties
    fausseraient la pente de H1 sans aucun signal. Une part de cadres manquante donne un écart
    manquant : un `fillna(0)` tirerait la pente vers zéro.
    """
    communes = communes_jouets(
        [
            ("35200", "Rennes", carre(1, 0)),  # milieu
            ("35300", "Rennes", carre(0, 0)),  # ouest
            ("35100", "Rennes", carre(2, 0)),  # est, à 1 km de l'ouest
        ],
        dist_lyc_prive_min=[1.5, 4.0, 7.0],
        part_cadres_2022=[0.30, 0.10, math.nan],  # est sans part de cadres
    )
    # index d'un tableau trié sans reset_index : aucune étiquette n'égale sa position
    communes.index = [2, 0, 1]

    paires = geo.paires_contigues(communes, ["part_cadres_2022", "dist_lyc_prive_min"])

    # l'ordre des d_ suit `variables`, pas celui des colonnes en entrée
    assert list(paires.columns) == [
        "code_commune_i",
        "code_commune_j",
        "aire",
        "d_part_cadres_2022",
        "d_dist_lyc_prive_min",
    ]
    paires = triees(paires)
    assert paires[["code_commune_i", "code_commune_j"]].to_numpy().tolist() == [
        ["35100", "35200"],  # est, milieu
        ["35200", "35300"],  # milieu, ouest
    ]
    # est - milieu : manquant, est n'ayant pas de valeur ; milieu - ouest = 0,30 - 0,10
    assert paires["d_part_cadres_2022"].tolist() == pytest.approx([math.nan, 0.20], nan_ok=True)
    # l'autre variable reste calculée : est - milieu = 7,0 - 1,5 ; milieu - ouest = 1,5 - 4,0
    assert paires["d_dist_lyc_prive_min"].tolist() == pytest.approx([5.5, -2.5])


def test_aucune_paire_entre_deux_aires():
    """Deux communes contiguës forment une paire seulement si elles sont dans la même aire.

    35002 (Rennes) et 44002 (Nantes) se touchent par un bord. Une contiguïté calculée sur
    toutes les aires sans filtre ajouterait une paire sans aucun signal.
    """
    communes = communes_jouets(
        [
            ("35001", "Rennes", carre(0, 0)),
            ("35002", "Rennes", carre(1, 0)),
            ("44002", "Nantes", carre(2, 0)),
            ("44001", "Nantes", carre(3, 0)),
        ],
        part_cadres_2022=[0.10, 0.20, 0.30, 0.40],
    )

    paires = triees(geo.paires_contigues(communes, ["part_cadres_2022"]))

    # 35002 et 44002 se touchent mais ne sont pas dans la même aire
    assert paires[["code_commune_i", "code_commune_j", "aire"]].to_numpy().tolist() == [
        ["35001", "35002", "Rennes"],
        ["44001", "44002", "Nantes"],
    ]
