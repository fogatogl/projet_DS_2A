"""H1 : comparaison par anneaux, pentes des paires contiguës et verdict ; pentes de H4.

H4 reprend l'estimateur des paires de H1, appliqué aux autres infrastructures.
"""

import itertools

import pandas as pd

from cadres_lycees import config


def _distances_groupes(
    communes_aire: pd.DataFrame, colonne_exposition: str, bas: float, haut: float
) -> tuple[pd.Series, pd.Series]:
    """Renvoie les distances au centre des communes exposées, puis non exposées, de [bas, haut)."""
    dans_la_cellule = communes_aire["dist_centre_km"].between(bas, haut, inclusive="left")
    cellule = communes_aire[dans_la_cellule]
    exposee = cellule[colonne_exposition] == 1
    return cellule.loc[exposee, "dist_centre_km"], cellule.loc[~exposee, "dist_centre_km"]


def cellules_anneaux(communes: pd.DataFrame, rayon: int) -> pd.DataFrame:
    """Renvoie, aire par aire, les cellules d'anneaux de distance au centre après fusion.

    Une cellule remplit la condition si les communes
    exposées (`expose_lyc_prive_<rayon>km` vaut 1) et les non exposées sont chacune au moins
    `config.EFFECTIF_MIN_GROUPE`. Tant qu'une cellule échoue, la plus proche du centre est
    fusionnée avec sa voisine qui compte le moins de communes, la plus proche du centre à
    égalité ; un anneau vide reste une cellule et peut donc être absorbé. Une cellule qui remplit
    la condition n'est estimable que si `ecart_dist_km`, l'écart des distances moyennes au
    centre des deux groupes, vaut au plus `config.ECART_DIST_MAX_KM`, sans nouvelle fusion. Une
    aire dont la dernière cellule échoue est non estimable : une seule ligne, `estimable` faux.
    Les anneaux vont de leur borne basse, incluse, à leur borne haute, exclue.
    """
    colonne_exposition = f"expose_lyc_prive_{rayon}km"
    assert communes[colonne_exposition].isin([0, 1]).all(), (
        f"{colonne_exposition} doit valoir 0 ou 1."
    )
    assert (communes["dist_centre_km"] >= 0).all(), "Distance au centre manquante ou négative."
    bornes = [*config.ANNEAUX_KM, float("inf")]

    lignes = []
    for aire, communes_aire in communes.groupby("aire"):
        # Une cellule est une suite d'anneaux contigus : ses bornes suffisent à la décrire
        cellules = list(itertools.pairwise(bornes))
        while True:
            groupes = [
                _distances_groupes(communes_aire, colonne_exposition, bas, haut)
                for bas, haut in cellules
            ]
            remplies = [
                min(len(dist_exposees), len(dist_non_exposees)) >= config.EFFECTIF_MIN_GROUPE
                for dist_exposees, dist_non_exposees in groupes
            ]
            if all(remplies) or len(cellules) == 1:
                break
            rang = remplies.index(False)
            voisines = [voisine for voisine in (rang - 1, rang + 1) if 0 <= voisine < len(cellules)]
            nb_communes = [
                len(dist_exposees) + len(dist_non_exposees)
                for dist_exposees, dist_non_exposees in groupes
            ]
            # La voisine qui compte le moins de communes ; à égalité, le plus petit rang, donc
            # la plus proche du centre
            voisine = min(voisines, key=lambda candidate: (nb_communes[candidate], candidate))
            interieure, exterieure = sorted((rang, voisine))
            cellules[interieure] = (cellules[interieure][0], cellules[exterieure][1])
            del cellules[exterieure]

        for (bas, haut), (dist_exposees, dist_non_exposees), remplie in zip(
            cellules, groupes, remplies, strict=True
        ):
            ecart = abs(dist_exposees.mean() - dist_non_exposees.mean())
            lignes.append(
                {
                    "aire": aire,
                    "bas_km": bas,
                    "haut_km": haut,
                    "n_exposees": len(dist_exposees),
                    "n_non_exposees": len(dist_non_exposees),
                    "dist_moy_exposees": dist_exposees.mean(),
                    "dist_moy_non_exposees": dist_non_exposees.mean(),
                    "ecart_dist_km": ecart,
                    # Une cellule en échec n'est jamais estimable, même équilibrée
                    "estimable": bool(remplie and ecart <= config.ECART_DIST_MAX_KM),
                }
            )
    return pd.DataFrame(lignes)
