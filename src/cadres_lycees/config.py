"""Constantes du projet : les choix fixés par le plan et les paramètres des sources."""

from pathlib import Path

RAYON_PRINCIPAL_KM = 5
CHEMIN_TABLEAU_SUPPORT = Path(__file__).parents[2] / "docs" / "tableau_support.md"
DIST_FRONTIERE_KM = 10

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
