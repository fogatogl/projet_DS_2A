"""Mise en forme des tableaux affichés dans le rapport : libellés en clair, unités, virgule.

Les calculs sont dans `analyse.py`, `h1.py`, `h3.py` et `robustesse.py` ; ces fonctions ne font
que présenter leurs résultats. `document_markdown` met en forme le dictionnaire des variables,
affiché tel quel en annexe.
"""

from pathlib import Path

import pandas as pd

from cadres_lycees import charte, config


def _nombre(valeur: float, facteur: float = 1, signe: bool = True, decimales: int = 2) -> str:
    """Écrit un nombre à la française (virgule, vrai signe moins), à `decimales` décimales."""
    texte = f"{valeur * facteur:{'+' if signe else ''}.{decimales}f}"
    return texte.replace(".", ",").replace("-", "−")


def _estimation(ligne: pd.Series, valeur: str, facteur: float) -> str:
    """Écrit « estimation [bas ; haut] », et les tirages écartés du bootstrap s'il y en a."""
    ecartes = int(ligne["tirages_ecartes"])
    estimation = _nombre(ligne[valeur], facteur)
    if pd.isna(ligne["ic_bas"]):
        return f"{estimation} (intervalle non rapporté, {ecartes} tirages écartés)"
    texte = (
        f"{estimation} [{_nombre(ligne['ic_bas'], facteur)} ; {_nombre(ligne['ic_haut'], facteur)}]"
    )
    if ecartes:
        texte += f" ({ecartes} tirages écartés)"
    return texte


def tableau_acces(resume: pd.DataFrame) -> pd.DataFrame:
    """Met en forme `analyse.resume_acces` : libellés en clair et unités, une aire par colonne."""
    rayon = config.RAYON_PRINCIPAL_KM
    libelles = {
        "communes": "Communes",
        "part_exposees": f"Part des communes avec un lycée privé sous contrat à {rayon} km (%)",
        "dist_lyc_prive_min": "Distance au lycée privé sous contrat le plus proche (km, médiane)",
        "dist_lyc_public_min": "Distance au lycée public le plus proche (km, médiane)",
        "dist_gare_min": "Distance à la gare la plus proche (km, médiane)",
        "apl_mg": "APL aux médecins généralistes (consultations par an et par habitant, médiane)",
        f"n_sport_{rayon}km": f"Installations sportives à {rayon} km (médiane)",
        f"n_culture_{rayon}km": f"Équipements culturels à {rayon} km (médiane)",
    }
    tableau = resume.copy()
    tableau["part_exposees"] = tableau["part_exposees"] * 100
    tableau = tableau[list(libelles)].rename(columns=libelles).T
    # Comptes sans décimale ; parts, distances et APL à une décimale, leur précision réelle
    texte = tableau.apply(
        lambda ligne: ligne.map(
            lambda valeur: _nombre(
                valeur, signe=False, decimales=0 if (ligne % 1 == 0).all() else 1
            )
        ),
        axis=1,
    )
    return texte[charte.aires_ordonnees(texte.columns)].rename_axis(index=None, columns=None)


def tableau_effectifs(effectifs: pd.DataFrame) -> pd.DataFrame:
    """Met en forme `analyse.effectifs_base` : une ligne par étape, une aire par colonne."""
    libelles = {
        "communes": "Communes (arrondissements à Lyon)",
        "petites_communes": f"dont moins de {config.ACTIFS_MIN_ROBUSTESSE} actifs de 25 à 54 ans",
        "communes_avec_prix": f"dont un prix au m² (au moins {config.MIN_VENTES_DVF} ventes)",
        "lycees_publics": "Lycées retenus dans l'aire : publics",
        "lycees_prives": "Lycées retenus dans l'aire : privés sous contrat",
        "lycees_avec_ival": "Lycées retenus dans l'aire avec une IVAL (au moins 5 sessions)",
        "paires": "Paires de communes contiguës",
    }
    tableau = effectifs[list(libelles)].rename(columns=libelles).T
    return tableau[charte.aires_ordonnees(tableau.columns)].rename_axis(index=None, columns=None)


def tableau_gradient(parts: pd.DataFrame) -> pd.DataFrame:
    """Met en forme `analyse.parts_par_anneau` : une ligne par anneau, une aire par colonne.

    Chaque case donne la part de cadres de l'anneau, en %, et le nombre de communes.
    """
    cases = parts.apply(
        lambda ligne: (
            f"{_nombre(ligne['part_cadres_2022'], 100, signe=False, decimales=1)} % "
            f"({int(ligne['communes'])} communes)"
        ),
        axis=1,
    ).unstack("aire")
    return (
        cases[charte.aires_ordonnees(cases.columns)]
        .fillna("—")
        .rename_axis(index=None, columns=None)
    )


def tableau_support(criteres: pd.DataFrame, support: pd.DataFrame) -> str:
    """Met en forme les critères et le support de `analyse.lire_tableau_support` en Markdown.

    Libellés en clair et virgule décimale ; les valeurs sont celles du fichier commité.
    """
    frontiere = f"communes_a_moins_de_{config.DIST_FRONTIERE_KM}km_frontiere"
    aires = criteres.set_index("aire")
    criteres_lisibles = pd.DataFrame(
        {
            "Ouest (a)": aires["ouest"].map({"True": "oui", "False": "non"}),
            "Privé, part des lycées (b)": aires["part_prive_lycees"].map(_pourcentage),
            "Privé, part des candidats au bac (b)": aires["part_prive_candidats"].map(_pourcentage),
            "Écart d'IPS privé − public (b)": aires["ecart_ips"].map(
                lambda valeur: _nombre(valeur, decimales=1)
            ),
            "Lycées avec IPS, public / privé": aires["n_ips_public"].astype(str)
            + " / "
            + aires["n_ips_prive"].astype(str),
            "Population 2022 (c)": aires["population_2022"].map(lambda valeur: f"{valeur:,}"),
            "Lycées privés sous contrat / retenus (d)": aires["lycees_prives"].astype(str)
            + " / "
            + aires["lycees"].astype(str),
            f"Communes à moins de {config.DIST_FRONTIERE_KM} km d'une frontière (f)": aires[
                frontiere
            ],
        }
    )
    criteres_lisibles["Population 2022 (c)"] = criteres_lisibles["Population 2022 (c)"].str.replace(
        ",", "\u202f"
    )
    support_lisible = pd.DataFrame(
        {
            "Aire": support["aire"],
            "Rayon": support["rayon_km"].astype(str) + " km",
            "Communes exposées": support["exposees"].astype(str)
            + " sur "
            + support["communes"].astype(str),
            "Cellules estimables": support["cellules_estimables"],
            "Paires de statut différent": support["paires_statut_different"],
            "Corrélation des écarts de distance": support["correlation_non_centree"].map(
                lambda valeur: _nombre(valeur, signe=False, decimales=3)
            ),
        }
    )
    return "\n\n".join(
        [
            "**Critères (a) à (d) et (f).** Le critère (e) est détaillé dans le second tableau ;"
            " (f), faisabilité : la source donne les arrondissements de Lyon.",
            criteres_lisibles.rename_axis("Aire").to_markdown(),
            "**Support de l'exposition (e).** Une commune est exposée si un lycée privé sous"
            " contrat est dans le rayon ; la corrélation, non centrée, porte sur les écarts de"
            " distance au lycée privé et au centre dans les paires contiguës.",
            support_lisible.to_markdown(index=False),
            f"Source et détail des cellules : `{config.CHEMIN_TABLEAU_SUPPORT.name}` dans `docs/`,"
            " commité avant le choix des aires, sans aucune donnée sur les cadres.",
        ]
    )


def _pourcentage(part: float) -> str:
    """Écrit une part (fraction) en pourcentage entier, « 47 % »."""
    return f"{part * 100:.0f}\u202f%"


def encadre_replie(titre: str, contenu: str) -> str:
    """Renvoie `contenu` (Markdown) dans un encadré Quarto replié, titré `titre`.

    À imprimer dans une cellule `output: asis` : le lecteur l'ouvre d'un clic.
    """
    return f'::: {{.callout-note collapse="true" title="{titre}"}}\n{contenu}\n:::'


def document_markdown(chemin: Path) -> str:
    """Renvoie un document Markdown du dépôt sans son titre, pour l'afficher dans le rapport.

    Les titres sont descendus de deux niveaux (`##` devient `####`) pour rester sous la section
    du rapport qui affiche le document ; une ligne qui commence par `#` dans un bloc de code est
    un commentaire et reste telle quelle.
    """
    corps = chemin.read_text(encoding="utf-8").split("\n", maxsplit=1)[1]
    lignes = []
    dans_un_bloc_de_code = False
    for ligne in corps.splitlines():
        if ligne.startswith("```"):
            dans_un_bloc_de_code = not dans_un_bloc_de_code
        if ligne.startswith("#") and not dans_un_bloc_de_code:
            ligne = "##" + ligne
        lignes.append(ligne)
    return "\n".join(lignes)
