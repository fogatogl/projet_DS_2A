"""Collecte des sources de données : copies brutes dans raw/, contrôlées par leur sha256."""

import hashlib
import io
import zipfile
from collections.abc import Callable

import geopandas as gpd
import pandas as pd
import requests
from cartiflette import carti_download

from cadres_lycees import config, stockage


def _copies_publiques(chemin: str) -> list[str]:
    """Renvoie les URL publiques d'une copie gelée : la release du dépôt, puis celle du groupe.

    Les deux releases portent les mêmes fichiers ; le `sha256` est contrôlé quelle que soit
    l'origine.
    """
    nom = chemin.removeprefix("raw/")
    return [config.URL_COPIES_RELEASE + nom, config.URL_COPIES_RELEASE_SECOURS + nom]


def geler_annuaire(chemin: str) -> str:
    """Écrit à `chemin` l'export complet de l'annuaire par l'API et renvoie son sha256.

    Le rapport ne l'appelle pas, il lit la copie gelée (`annuaire_education`). Mode d'emploi dans
    le README.
    """
    return _geler(config.URL_ANNUAIRE, chemin, _parquet_complet)


def _geler(url: str, chemin: str, est_complet: Callable[[bytes], bool]) -> str:
    """Écrit à `chemin` le fichier téléchargé à `url` et renvoie son sha256.

    Une réponse 200 peut être tronquée : `est_complet` contrôle le contenu avant l'écriture.
    """
    # Un chemin daté déjà pris est une copie gelée, peut-être publique : on ne l'écrase jamais
    assert not stockage.existe(chemin), f"{chemin} existe déjà : choisir un autre chemin daté."
    reponse = requests.get(url, timeout=config.DELAI_TELECHARGEMENT_S)
    reponse.raise_for_status()
    assert est_complet(reponse.content), (
        f"Le fichier de {url} est incomplet : rien n'a été enregistré."
    )
    stockage.ecrire_octets(reponse.content, chemin)
    return hashlib.sha256(reponse.content).hexdigest()


def _parquet_complet(contenu: bytes) -> bool:
    """Dit si `contenu` est un fichier Parquet entier : "PAR1" l'ouvre et le ferme toujours."""
    return contenu.startswith(b"PAR1") and contenu.endswith(b"PAR1")


def _csv_complet(contenu: bytes) -> bool:
    """Dit si `contenu` est un CSV entier : un fichier tronqué ne finit pas par un saut de ligne."""
    return contenu.endswith(b"\n")


def _xlsx_complet(contenu: bytes) -> bool:
    """Dit si `contenu` est un xlsx entier : une archive zip dont chaque fichier se relit.

    Une archive tronquée fait échouer `zipfile` (BadZipFile) ; un fichier abîmé est renvoyé par
    `testzip`.
    """
    return zipfile.ZipFile(io.BytesIO(contenu)).testzip() is None


def annuaire_education(
    natures: tuple[int, ...] = config.NATURES_LYCEES,
    contrats: tuple[str, ...] = config.CONTRATS_PRIVE_RETENUS,
) -> gpd.GeoDataFrame:
    """Renvoie les lycées de France métropolitaine de l'annuaire de l'éducation.

    Par défaut, lycées généraux, technologiques et polyvalents, publics ou privés sous contrat,
    repérés par `code_nature` car les `voie_*` de l'annuaire sont trop souvent vides ; la robustesse
    élargit `natures` et `contrats`. Toute la métropole est gardée, pas seulement les aires et une
    marge autour : le lycée le plus proche d'une commune du bord peut être bien au-delà de l'aire.
    Une ligne par site : un UAI multi-sites apparaît plusieurs fois (dédoublonné au nettoyage). Lu
    dans la copie gelée, jamais dans l'API, qui change chaque jour.
    """
    contenu = stockage.copie_controlee(
        _copies_publiques(config.CHEMIN_RAW_ANNUAIRE),
        config.CHEMIN_RAW_ANNUAIRE,
        config.SHA256_ANNUAIRE,
    )
    annuaire = gpd.read_parquet(io.BytesIO(contenu))

    # L'annuaire écrit les départements sur trois caractères : de "001" à "095", "02A" et "02B"
    # en métropole, à partir de "971" outre-mer
    metropole = annuaire["code_departement"].str.startswith("0")
    # Le type "Lycée" isole la partie lycée d'une cité scolaire, dont la partie collège
    # (type "Collège") porte le même UAI
    est_lycee = annuaire["type_etablissement"] == "Lycée"
    nature_retenue = annuaire["code_nature"].isin(natures)
    # `lycee_agricole` est parfois vide : on exclut aussi sur la tutelle
    pas_agricole = (annuaire["ministere_tutelle"] != "AGRICULTURE") & (
        annuaire["lycee_agricole"] != "1"
    )
    candidats = metropole & est_lycee & nature_retenue & pas_agricole

    # Un statut vide fait échouer les deux comparaisons plus bas : sans ce contrôle, le
    # lycée serait écarté sans bruit. Seuls les cas connus de `config` sont écartés
    statut_vide = candidats & annuaire["statut_public_prive"].isna()
    uai_sans_statut = sorted(annuaire.loc[statut_vide, "identifiant_de_l_etablissement"])
    assert uai_sans_statut == sorted(config.UAI_SANS_STATUT), (
        f"Lycées sans statut public ou privé : {uai_sans_statut}, attendus : "
        f"{sorted(config.UAI_SANS_STATUT)} (config.UAI_SANS_STATUT)."
    )

    est_public = annuaire["statut_public_prive"] == "Public"
    est_prive = annuaire["statut_public_prive"] == "Privé"
    contrat_retenu = annuaire["code_type_contrat_prive"].isin(contrats)
    lycees = annuaire[candidats & (est_public | (est_prive & contrat_retenu))]
    return lycees.reset_index(drop=True)


def aav_2020() -> pd.DataFrame:
    """Renvoie la composition communale du zonage en aires d'attraction des villes 2020.

    Une ligne par commune du COG 2025, avec `AAV2020` (code de l'aire, "000" hors aire) et
    `CATEAAV2020` (commune-centre, pôle ou couronne). Tout est lu en chaîne : "013" perdrait son
    zéro en entier. Lyon, Marseille et Paris n'y figurent que par leur commune parente, pas par
    leurs arrondissements. Le zip de l'Insee est permanent : il est lu à son URL d'origine.
    """
    contenu = stockage.copie_controlee([config.URL_AAV], config.CHEMIN_RAW_AAV, config.SHA256_AAV)
    with zipfile.ZipFile(io.BytesIO(contenu)) as archive:
        classeur = io.BytesIO(archive.read(config.XLSX_AAV))
    aav = pd.read_excel(
        classeur,
        sheet_name=config.FEUILLE_AAV,
        header=config.ENTETE_AAV,
        dtype=str,
        engine="calamine",
    )

    assert len(aav) == config.NB_COMMUNES_AAV, (
        f"{len(aav)} communes dans l'AAV, {config.NB_COMMUNES_AAV} attendues (COG 2025)."
    )
    assert aav["CODGEO"].is_unique, "Des codes communes sont en double dans l'AAV."
    categories_inconnues = set(aav["CATEAAV2020"]) - set(config.CATEGORIES_AAV)
    assert not categories_inconnues, f"Catégories AAV inconnues : {sorted(categories_inconnues)}"
    return aav


def serie_historique_rp2022() -> pd.DataFrame:
    """Renvoie la population et la superficie du recensement 2022, par commune ou arrondissement.

    Colonnes `CODGEO`, `P22_POP` et `SUPERF` (km²), en COG 2025. Les arrondissements de Lyon,
    Marseille et Paris y figurent avec leur commune parente : sommer tout le fichier compterait
    ces villes deux fois. Le zip de l'Insee est permanent : il est lu à son URL d'origine.
    """
    contenu = stockage.copie_controlee(
        [config.URL_SERIE_RP2022], config.CHEMIN_RAW_SERIE_RP2022, config.SHA256_SERIE_RP2022
    )
    with zipfile.ZipFile(io.BytesIO(contenu)) as archive:
        csv = io.BytesIO(archive.read(config.CSV_SERIE_RP2022))
    # Lu en nombre, "01001" deviendrait 1001 ; une colonne disparue fait échouer la lecture
    serie = pd.read_csv(
        csv, sep=";", usecols=["CODGEO", "P22_POP", "SUPERF"], dtype={"CODGEO": str}
    )

    assert len(serie) == config.NB_LIGNES_SERIE_RP2022, (
        f"{len(serie)} lignes dans la série historique, {config.NB_LIGNES_SERIE_RP2022} attendues."
    )
    assert serie["CODGEO"].is_unique, "Des codes communes sont en double dans la série historique."
    return serie


def evol_struct_rp2022() -> pd.DataFrame:
    """Renvoie les actifs de 25 à 54 ans par groupe socioprofessionnel, en 2011 et en 2022.

    Une ligne par commune ou arrondissement (`CODGEO`), en COG 2025, avec les colonnes de
    `config.ACTIFS_2554_2011` et `config.ACTIFS_2554_2022`, et, pour la robustesse, les cadres
    et la population de 15 ans ou plus en 2022. Les effectifs sont décimaux
    (exploitation complémentaire du recensement). Les arrondissements de Lyon, Marseille et Paris
    y figurent avec leur commune parente : sommer tout le fichier compterait ces villes deux
    fois. Le zip de l'Insee est permanent : il est lu à son URL d'origine.
    """
    contenu = stockage.copie_controlee(
        [config.URL_EVOL_STRUCT_RP2022],
        config.CHEMIN_RAW_EVOL_STRUCT_RP2022,
        config.SHA256_EVOL_STRUCT_RP2022,
    )
    with zipfile.ZipFile(io.BytesIO(contenu)) as archive:
        csv = io.BytesIO(archive.read(config.CSV_EVOL_STRUCT_RP2022))
    colonnes = [
        "CODGEO",
        *config.ACTIFS_2554_2011,
        *config.ACTIFS_2554_2022,
        config.CADRES_15P_2022,
        config.POP_15P_2022,
    ]
    # Lu en nombre, "01001" deviendrait 1001 ; une colonne disparue fait échouer la lecture
    effectifs = pd.read_csv(csv, sep=";", usecols=colonnes, dtype={"CODGEO": str})

    assert len(effectifs) == config.NB_LIGNES_EVOL_STRUCT_RP2022, (
        f"{len(effectifs)} lignes dans « Évolution et structure », "
        f"{config.NB_LIGNES_EVOL_STRUCT_RP2022} attendues."
    )
    assert effectifs["CODGEO"].is_unique, "Des codes communes sont en double."
    return effectifs


def ival_lycees() -> pd.DataFrame:
    """Renvoie les indicateurs de valeur ajoutée des lycées GT : une ligne par lycée et session.

    Lu dans la copie gelée de l'export de l'API (`config.URL_IVAL`). Tout est lu en
    chaîne, pour garder les codes communes tels quels (« 2A004 », zéros
    en tête) : la conversion des valeurs se fait au nettoyage.
    """
    contenu = stockage.copie_controlee(
        _copies_publiques(config.CHEMIN_RAW_IVAL), config.CHEMIN_RAW_IVAL, config.SHA256_IVAL
    )
    ival = pd.read_csv(io.BytesIO(contenu), sep=";", encoding="utf-8-sig", dtype=str)

    assert len(ival) == config.NB_LIGNES_IVAL, (
        f"{len(ival)} lignes dans l'IVAL, {config.NB_LIGNES_IVAL} attendues."
    )
    assert not ival.duplicated(["uai", "annee"]).any(), "Lycée en double dans l'IVAL."
    return ival


def geler_contours(chemin: str, valeur: str, maille: str, filtre: str) -> str:
    """Écrit à `chemin` des contours téléchargés par cartiflette et renvoie leur sha256.

    `valeur`, `maille` et `filtre` sont les arguments `values`, `borders` et `filter_by` de
    `carti_download` : un code d'aire, "COMMUNE_ARRONDISSEMENT" et "AIRE_ATTRACTION_VILLES" pour les
    contours d'une aire ; "France", "DEPARTEMENT" et "FRANCE_ENTIERE" pour les départements ; un
    code d'aire, "IRIS" et "AIRE_ATTRACTION_VILLES" pour les IRIS d'une aire. Le rapport ne
    l'appelle pas, il lit les copies gelées. Le sha256 fige une sérialisation (versions de geopandas
    et de pyarrow comprises), pas seulement des données. Mode d'emploi dans le README.
    """
    assert not stockage.existe(chemin), f"{chemin} existe déjà : choisir un autre chemin daté."
    contours = carti_download(
        values=valeur,
        borders=maille,
        filter_by=filtre,
        year=config.ANNEE_COG,
        simplification=config.SIMPLIFICATION_CONTOURS,
    )
    stockage.ecrire_parquet(contours, chemin)
    return hashlib.sha256(stockage.lire_octets(chemin)).hexdigest()


def contours_aire(code_aav: str) -> gpd.GeoDataFrame:
    """Renvoie les contours des communes d'une aire d'attraction, en WGS84 (COG 2025).

    Les arrondissements municipaux remplacent leur commune parente (Lyon 69123 devient 69381 à
    69389) ; `INSEE_COM` garde le code de la commune parente et `INSEE_COG` celui de l'unité. Lu
    dans la copie gelée.
    """
    chemin = config.CHEMIN_RAW_CONTOURS.format(aav=code_aav)
    contenu = stockage.copie_controlee(
        _copies_publiques(chemin), chemin, config.SHA256_CONTOURS[code_aav]
    )
    return gpd.read_parquet(io.BytesIO(contenu))


def contours_departements() -> gpd.GeoDataFrame:
    """Renvoie les contours des départements, DOM compris, en WGS84 (COG 2025).

    Leur union donne le contour de la France métropolitaine (`geo.distance_contour_national_km`).
    Lu dans la copie gelée.
    """
    contenu = stockage.copie_controlee(
        _copies_publiques(config.CHEMIN_RAW_DEPARTEMENTS),
        config.CHEMIN_RAW_DEPARTEMENTS,
        config.SHA256_DEPARTEMENTS,
    )
    return gpd.read_parquet(io.BytesIO(contenu))


def ips_lycees() -> pd.DataFrame:
    """Renvoie l'IPS des lycées : une ligne par lycée et par rentrée, de 2023-2024 à 2025-2026.

    Lu dans la copie gelée de l'export de l'API (`config.URL_IPS`). Tout est lu en
    chaîne, la conversion en nombres se fait au nettoyage.
    """
    contenu = stockage.copie_controlee(
        _copies_publiques(config.CHEMIN_RAW_IPS), config.CHEMIN_RAW_IPS, config.SHA256_IPS
    )
    ips = pd.read_csv(io.BytesIO(contenu), sep=";", encoding="utf-8-sig", dtype=str)

    assert len(ips) == config.NB_LIGNES_IPS, (
        f"{len(ips)} lignes dans l'IPS, {config.NB_LIGNES_IPS} attendues."
    )
    assert not ips.duplicated(["uai", "rentree_scolaire"]).any(), "Lycée en double dans l'IPS."
    return ips
