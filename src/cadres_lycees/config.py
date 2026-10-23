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
# Sous ce nombre de ventes, la médiane du prix d'une commune est manquante
MIN_VENTES_DVF = 10
# Délai de `requests` par lecture (pas la durée totale) et essais par URL
DELAI_TELECHARGEMENT_S = 120
NB_ESSAIS_TELECHARGEMENT = 3
# Seuil des petites communes (actifs de 25 à 54 ans) et permutations de l'indice de Moran
ACTIFS_MIN_ROBUSTESSE = 200
COULEUR_TEXTE = "#52514e"
COULEUR_GRILLE = "#ececea"
# Taille des notes sous les figures, lisible une fois la figure réduite à la colonne
TAILLE_NOTE_FIGURES = 10.5
# Une couleur par aire (palette d'Okabe et Ito), distincte des couleurs des secteurs
COULEURS_AIRES = {"Nantes": "#009e73", "Lyon": "#a2559c", "Strasbourg": "#9c6b1f"}
