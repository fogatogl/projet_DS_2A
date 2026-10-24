"""Constantes du projet : les choix fixés par le plan et les paramètres des sources."""

from pathlib import Path

RAYON_PRINCIPAL_KM = 5

# Anneaux : bornes basses en km (le dernier est ouvert), effectif minimal de chaque groupe d'une
# cellule et écart maximal des distances moyennes au centre des deux groupes
ANNEAUX_KM = (0, 5, 10, 20, 30)
CHEMIN_TABLEAU_SUPPORT = Path(__file__).parents[2] / "docs" / "tableau_support.md"
# Rayons du tableau de support : le principal et le 10 km rapporté à côté
RAYONS_SUPPORT_KM = (5, 10)
DIST_FRONTIERE_KM = 10
# Écarts calculés dans les paires ; ceux du tableau de support n'utilisent pas la part de cadres
VARIABLES_PAIRES_SANS_CADRES = (
    "dist_lyc_prive_min",
    "n_lyc_prive_5km",
    "dist_centre_km",
    "log_densite",
    "expose_lyc_prive_5km",
    "expose_lyc_prive_10km",
)

# Stockage : S3 si les identifiants AWS et le nom du bucket sont définis, sinon le dossier data/
VARIABLES_AWS = ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY")
VARIABLE_BUCKET_S3 = "BUCKET_S3"
PREFIXE_S3 = "projet-cadres-lycees"
DOSSIER_LOCAL = Path(__file__).parents[2] / "data"
# Dépôt de référence du projet ; ses releases publient les copies gelées
URL_DEPOT = "https://github.com/fogatogl/DataScience"
URL_COPIES_RELEASE = f"{URL_DEPOT}/releases/download/donnees-20261020/"
# La même release, sur le dépôt du groupe dont le dépôt de référence est une fork, en secours
URL_COPIES_RELEASE_SECOURS = (
    "https://github.com/gabrielwenger1-coder/DataScience/releases/download/donnees-20261020/"
)

# Annuaire de l'éducation : export complet de l'API, gelé car il change chaque jour
URL_ANNUAIRE = (
    "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/"
    "fr-en-annuaire-education/exports/parquet"
)
CHEMIN_RAW_ANNUAIRE = "raw/annuaire_education_20261013.parquet"
SHA256_ANNUAIRE = "2c493f152bc8fc682aa8b1f063392015941bcff36bae2ae59a4d1a1e6334e94a"
# Sous ce nombre de ventes, la médiane du prix d'une commune est manquante
MIN_VENTES_DVF = 10
# Délai de `requests` par lecture (pas la durée totale) et essais par URL
DELAI_TELECHARGEMENT_S = 120
NB_ESSAIS_TELECHARGEMENT = 3
# Zonage en aires d'attraction des villes 2020, géographie au 01/01/2025
URL_AAV = "https://www.insee.fr/fr/statistiques/fichier/4803954/AAV2020_au_01-01-2025.zip"
SHA256_AAV = "738f81b12832fe294bd24ddbfe3a31830c20d850143fc8b4393f18d4b8ee8181"
CHEMIN_RAW_AAV = "raw/AAV2020_au_01-01-2025.zip"
XLSX_AAV = "AAV2020_au_01-01-2025.xlsx"
FEUILLE_AAV = "Composition_communale"
ENTETE_AAV = 5
NB_COMMUNES_AAV = 34875
# `CATEAAV2020` : 11 commune-centre, 12 pôle principal, 13 pôle secondaire, 20 couronne, 30 hors
CATEGORIES_AAV = ("11", "12", "13", "20", "30")

# Série historique du recensement 2022 : population et superficie (km²), COG 2025
URL_SERIE_RP2022 = (
    "https://www.insee.fr/fr/statistiques/fichier/8582555/base-cc-serie-historique-2022_csv.zip"
)
SHA256_SERIE_RP2022 = "ff0187ec6bb77fd2e5da639c08159368ff152cad0682ee0908358a829830c273"
CHEMIN_RAW_SERIE_RP2022 = "raw/base-cc-serie-historique-2022_csv.zip"
CSV_SERIE_RP2022 = "base-cc-serie-historique-2022.CSV"
NB_LIGNES_SERIE_RP2022 = 34903

# « Évolution et structure de la population » 2022 : actifs de 25 à 54 ans par groupe
# socioprofessionnel en 2011 et 2022, COG 2025, arrondissements de Lyon compris
URL_EVOL_STRUCT_RP2022 = (
    "https://www.insee.fr/fr/statistiques/fichier/8581696/base-cc-evol-struct-pop-2022_csv.zip"
)
SHA256_EVOL_STRUCT_RP2022 = "cb4b918862289527232ad79fb3b712d5f4635c6de5bae762e8d22a132717ed83"
CHEMIN_RAW_EVOL_STRUCT_RP2022 = "raw/base-cc-evol-struct-pop-2022_csv.zip"
CSV_EVOL_STRUCT_RP2022 = "base-cc-evol-struct-pop-2022.CSV"
NB_LIGNES_EVOL_STRUCT_RP2022 = 34903
# Groupes 1 à 6 (occupés et chômeurs) : leur somme est le dénominateur, le groupe 3 le
# numérateur. Noms recopiés du fichier, qui dit `GSEC15_25` là où la page dit `GSEC16_25`
ACTIFS_2554_2022 = (
    "C22_POP2554_STAT_GSEC11_21",
    "C22_POP2554_STAT_GSEC12_22",
    "C22_POP2554_STAT_GSEC13_23",
    "C22_POP2554_STAT_GSEC14_24",
    "C22_POP2554_STAT_GSEC15_25",
    "C22_POP2554_STAT_GSEC16_26",
)
ACTIFS_2554_2011 = (
    "C11_POP2554_CS1",
    "C11_POP2554_CS2",
    "C11_POP2554_CS3",
    "C11_POP2554_CS4",
    "C11_POP2554_CS5",
    "C11_POP2554_CS6",
)
# Robustesse : cadres parmi la population de 15 ans ou plus en 2022
CADRES_15P_2022 = "C22_POP15P_STAT_GSEC13_23"
POP_15P_2022 = "C22_POP15P"

# Lycées retenus : `code_nature` 300, 301, 302 et 306 (général, technologique, polyvalent)
NATURES_LYCEES = (300, 301, 302, 306)
# `code_type_contrat_prive` du privé sous contrat d'association
CONTRATS_PRIVE_RETENUS = ("30", "31")
# Lycée retenu sans statut public ou privé dans l'annuaire (Eure, loin des aires) : écarté
UAI_SANS_STATUT = ("0271911F",)

# Contours communaux de cartiflette : sans `year`, il prendrait l'année courante ; sans
# simplification nulle, les centroïdes bougeraient
ANNEE_COG = 2025
SIMPLIFICATION_CONTOURS = 0
# Une copie gelée par aire : le serveur et le client de cartiflette changent
CHEMIN_RAW_CONTOURS = "raw/contours_aav_{aav}_20261013.parquet"
SHA256_CONTOURS = {
    "002": "5fc255ef5f92c540c5037f793c15c24007642c7cdce256a1e4f47d516176f231",
    "004": "6ff1e4bc0675ab567b7af3eb506774c0740ab855c5f333c66ee6b8fe1eb89982",
    "005": "c42afd4910a9a6907c54e2f8d476b8a4b6db3630bf9ffdff7b41cedf8a3b2c6e",
    "006": "6e0cb9a94a69887fd123a2d57c49068aa25b207da9541813652c00f1b2930c28",
    "008": "54665ed725b9ae364166d6dc76cd09b71b8e42397916e6fe564d8f0308786e59",
    "010": "454d27768198bb48be5882987f3aa36f88902add34bf443dff0cd37cc8be7790",
    "013": "c846f8d895d3121435037f5c04054a9e2275bb95e2de1791cae61498550b4cec",
    "014": "a1d13c20cc9565de3e2b3bb78b8d020076bae7c2a94ac2648d7aa96aa0699357",
}
# Contours des départements : leur union donne le contour de la métropole (frontière)
CHEMIN_RAW_DEPARTEMENTS = "raw/contours_departements_20261020.parquet"
SHA256_DEPARTEMENTS = "a6e4d3b3a7657f61b8fe9b710efa5f50c0cab76cde0d522f4cfd4adfdbe405ca"

# IPS des lycées : export de l'API, copie gelée
URL_IPS = (
    "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/"
    "fr-en-ips-lycees-ap2023/exports/csv"
)
SHA256_IPS = "31b2aafd8fb4597608c55f8f78f7144444a350df795111a651fb5222ee9c8aa7"
CHEMIN_RAW_IPS = "raw/ips_lycees_20261013.csv"
NB_LIGNES_IPS = 10905
# Rentrée la plus récente, voie générale et technologique ; lycées professionnels exclus
RENTREE_IPS = "2025-2026"

# IVAL des lycées généraux et technologiques : export de l'API, copie gelée
URL_IVAL = (
    "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/"
    "fr-en-indicateurs-de-resultat-des-lycees-gt_v2/exports/csv"
)
SHA256_IVAL = "6ab77b391e3405f5157bb942d4548d5f1cfbacd94e76dd52b93db9b370de8658"
CHEMIN_RAW_IVAL = "raw/ival_lycees_gt_20261020.csv"
NB_LIGNES_IVAL = 32485
# Seuil des petites communes (actifs de 25 à 54 ans) et permutations de l'indice de Moran
ACTIFS_MIN_ROBUSTESSE = 200
# Charte des figures : bleu et orange pour les secteurs, lisibles en cas de daltonisme
COULEURS_SECTEURS = {"public": "#2a78d6", "prive": "#eb6834"}
COULEUR_TEXTE = "#52514e"
COULEUR_LIAISON = "#c3c2b7"
COULEUR_GRILLE = "#ececea"
COULEUR_FOND_RETENUES = "#f0efec"
DATE_ANNUAIRE = "13/10/2026"
LIBELLES_SECTEURS = {"public": "public", "prive": "privé sous contrat"}
# Taille des notes sous les figures, lisible une fois la figure réduite à la colonne
TAILLE_NOTE_FIGURES = 10.5
# Une couleur par aire (palette d'Okabe et Ito), distincte des couleurs des secteurs
COULEURS_AIRES = {"Nantes": "#009e73", "Lyon": "#a2559c", "Strasbourg": "#9c6b1f"}
