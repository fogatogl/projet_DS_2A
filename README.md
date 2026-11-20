# Lycées et géographie des cadres dans trois aires urbaines de province

Projet du cours « Python pour la data science » (ENSAE), rendu le 24 novembre 2026.

- **Le rapport** : https://fogatogl.github.io/projet_DS_2A/
- **La présentation interactive** de la soutenance : https://fogatogl.github.io/projet_DS_2A/presentation.html

## La question

Les familles paient pour l'école de leurs enfants : à Paris, les logements sont plus chers dans les secteurs des collèges publics les plus performants. Nous avons cherché si ce lien se retrouve en province, avec les lycées. Dans les aires urbaines de Nantes, Lyon et Strasbourg, les communes proches d'un lycée privé ou d'un lycée à forte valeur ajoutée comptent-elles plus de cadres que leurs voisines ? Et ce lien est-il plus fort qu'avec d'autres équipements, comme les gares ou les médecins ?

## Ce que nous avons fait

**Les données.** Nous avons construit une base de 789 communes (les arrondissements à Lyon) qui réunit :

- la part de cadres parmi les actifs de 25 à 54 ans, en 2011 et en 2022, tirée du recensement de l'Insee ;
- l'accès aux lycées généraux et technologiques, publics et privés sous contrat, mesuré depuis le centre de chaque commune : distance au lycée privé le plus proche, nombre de lycées à moins de 5 km et valeur ajoutée moyenne de ces lycées, publiée par le ministère de l'Éducation nationale ;
- l'accès aux gares, aux médecins généralistes et aux équipements sportifs et culturels ;
- la distance au centre de l'aire, la densité de population et le prix au m².

**Le choix des aires.** Nous avons comparé huit aires candidates sans regarder les données sur les cadres (voir le [tableau de support](src/cadres_lycees/tableau_support.md)). Nantes représente l'Ouest, où le privé est très répandu et peu sélectif socialement ; à Lyon et à Strasbourg, il est plus sélectif.

**La méthode.** La part de cadres baisse nettement du centre vers la périphérie, et les lycées privés sont surtout au centre. Pour ne pas confondre les deux, nous comparons des communes voisines, qui ont la même position dans l'aire : quand une commune est plus proche d'un lycée privé que sa voisine, compte-t-elle plus de cadres ? Les intervalles de confiance viennent d'un bootstrap, qui tire les communes au hasard. Une seconde comparaison, entre communes situées à la même distance du centre, sert à confirmer le résultat. Le niveau de vie et la composition sociale des lycées ne sont jamais utilisés comme contrôles, car ils dépendent eux-mêmes de la part de cadres.

| | Hypothèse | Comment nous la testons |
|---|---|---|
| H1 | À distance égale du centre, il y a plus de cadres là où un lycée privé est plus proche | Comparaison de communes voisines, confirmée par anneaux de distance au centre |
| H2 | Ce lien est plus faible à Nantes, où le privé est plus répandu | H1 aire par aire, comparée sans test |
| H3 | La hausse des cadres de 2011 à 2022 suit la qualité des lycées proches plus que leur nombre | Régression de cette hausse sur la valeur ajoutée et sur le nombre de lycées |
| H4 | Le lien est plus fort avec les lycées qu'avec les gares, les médecins ou les équipements | Même comparaison entre voisines pour chaque équipement, sans verdict |

**Comment nous concluons.** H1 est confirmée si l'intervalle de confiance exclut zéro et si les autres estimations vont dans le même sens. Quand l'intervalle contient zéro, nous ne parlons de résultat nul que si la comparaison par anneaux le confirme ; sinon, le test n'est « pas concluant ». Pour H3, nous avons d'abord vérifié que la valeur ajoutée des lycées est une mesure assez stable d'une année à l'autre pour être utilisée.

## Résultats

- **La part de cadres dépend d'abord de la distance au centre.** Elle est 1,9 à 2,5 fois plus élevée à moins de 5 km du centre qu'au-delà de 30 km.
- **Le privé n'a pas le même profil partout.** Il représente 47 % des lycées à Nantes, 45 % à Lyon et 27 % à Strasbourg, mais l'écart de position sociale entre lycées privés et publics est deux fois plus faible à Nantes (12 points) qu'à Lyon (24) et à Strasbourg (23).
- **Entre communes voisines, être plus près d'un lycée privé ne va pas de pair avec un écart net de cadres (H1).** À Lyon, le lien est proche de zéro : pour 5 km de moins jusqu'au lycée privé, l'écart de part de cadres est compris entre −1,0 et +2,7 points. À Nantes et à Strasbourg, les données ne permettent pas de conclure, et Nantes ne se distingue pas des deux autres aires (H2).
- **La hausse des cadres suit le nombre de lycées proches plus que leur valeur ajoutée (H3 infirmée).** Un écart-type de lycées en plus va de pair avec 1,73 point de hausse, contre 0,22 point pour un écart-type de valeur ajoutée.
- **Aucun équipement ne se détache (H4).** Les liens avec les lycées, les gares, les médecins et les équipements sportifs et culturels sont tous faibles.

Ces résultats décrivent des associations : un lycée privé peut aussi s'implanter là où vivent déjà des cadres. Comme des communes voisines se ressemblent, nos intervalles de confiance sont aussi probablement un peu trop étroits.

## Mettre le site à jour

Le rapport et la présentation sont recalculés depuis les données et publiés sur la branche `gh-pages`. Aucun fichier HTML n'est commité sur les autres branches. Depuis un clone à jour de `main` :

```bash
uv run quarto render                       # exécute le rapport et écrit le site dans _site/
uv run python presentation/construire.py   # ajoute _site/presentation.html
uv run quarto publish gh-pages --no-render # publie _site/ tel quel sur la branche gh-pages
```

Pour regarder le site sans le publier : `uv run quarto preview`.

## Reproduire le projet

Il faut Python 3.13 et [uv](https://docs.astral.sh/uv/).

```bash
uv sync --locked                 # installe exactement les dépendances figées dans uv.lock
uv run pre-commit install        # active nb-clean et ruff avant chaque commit
uv run pytest                    # lance les tests
```

Le rapport est `rapport.ipynb`. Ses figures et ses tableaux sont recalculés à chaque exécution à partir des données brutes. Le site se construit avec [Quarto](https://quarto.org/), installé par `uv sync` (paquet `quarto-cli`, version figée dans `uv.lock`) : rien d'autre à installer.

```bash
uv run quarto render             # exécute rapport.ipynb et écrit le site dans _site/
```

`uv run` est nécessaire : il lance le Quarto de l'environnement du projet et lui donne le Python où le paquet `cadres_lycees` est installé.

Sur un clone neuf, les 28 fichiers de données sont téléchargés puis gardés dans `data/`, et l'exécution complète prend environ 17 minutes. Pour exécuter le notebook sans construire le site :

```bash
uv run jupyter nbconvert --to notebook --execute rapport.ipynb --output rapport_execute.ipynb
```

### Stockage des données

Les données ne sont pas dans Git. Le module `stockage.py` les range :

- sur le S3 du SSPCloud si les variables `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` et `BUCKET_S3` sont définies. Les deux premières le sont déjà sur un service SSPCloud ; le nom du bucket se donne avec `export BUCKET_S3=<nom du bucket>`, avant de lancer Jupyter. Les fichiers sont alors dans `s3://<bucket>/projet-cadres-lycees/` ;
- sinon dans le dossier local `data/`, avec un simple avertissement.

### Copies gelées des données

Certaines sources changent sans prévenir, comme l'annuaire de l'éducation, mis à jour chaque jour. Nous les avons téléchargées une fois et publiées dans la release GitHub [`donnees-20261020`](https://github.com/fogatogl/projet_DS_2A/releases/tag/donnees-20261020) de ce dépôt. Le rapport lit ces copies et vérifie à chaque lecture que leur empreinte `sha256` n'a pas changé.

| Copie | Date | Origine | `sha256` |
|---|---|---|---|
| `annuaire_education_20261013.parquet` | 13/10/2026 | https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-annuaire-education/exports/parquet | `2c493f152bc8fc682aa8b1f063392015941bcff36bae2ae59a4d1a1e6334e94a` |
| `gares_voyageurs_20261103.parquet` | 03/11/2026 | https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/gares-de-voyageurs/exports/parquet | `61ccf3392b01cb6785268be7152337f1a95dda93fa9eadf9134901b5f366bc44` |
| `apl_medecins_generalistes_20261103.xlsx` | 03/11/2026 | https://data.drees.solidarites-sante.gouv.fr/api/explore/v2.1/catalog/datasets/530_l-accessibilite-potentielle-localisee-apl/attachments/indicateur_d_apl_aux_medecins_generalistes_xlsx | `21c73deff57dc7a83a3cd6fcfd5b5ceb8c7a40e98590a50b5b1194f2dd4d75a2` |
| `equipements_sportifs_20261103.parquet` | 03/11/2026 | https://equipements.sports.gouv.fr/api/explore/v2.1/catalog/datasets/data-es/exports/parquet | `c78cb234bb591f54660277c5720e5a8275ec26ffacf7120b141024cfba936eef` |
| `bpe_2025_20261103.parquet` | 03/11/2026 | https://www.insee.fr/fr/statistiques/fichier/8217525/BPE25.parquet | `3bad0dc8b02eff0bee86832acf97fdeccef02116bbeb8a6dca2ad0e99d054f6a` |
| `statistiques_dvf_20261103.csv` | 03/11/2026 | https://data-pipeline-open.s3.sbg.io.cloud.ovh.net/dvf/stats_whole_period.csv | `eca12b1b1b45274e315859135d5f4ac15137f3e084712ea9b614b11c4a100722` |
| `chefs_lieux_cog2025_20261103.parquet` | 03/11/2026 | WFS de l'IGN, couches `ADMINEXPRESS-COG.2025:chef_lieu_de_commune` et `:chef_lieu_d_arrondissement_municipal` (`collecte.geler_chefs_lieux`) | `a43f55f677f463f10bb9487007426874fddf14a127a3e48021e787753e9849f6` |
| `ips_lycees_20261013.csv` | 13/10/2026 | https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-ips-lycees-ap2023/exports/csv | `31b2aafd8fb4597608c55f8f78f7144444a350df795111a651fb5222ee9c8aa7` |
| `ival_lycees_gt_20261020.csv` | 20/10/2026 | https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-indicateurs-de-resultat-des-lycees-gt_v2/exports/csv | `6ab77b391e3405f5157bb942d4548d5f1cfbacd94e76dd52b93db9b370de8658` |
| `contours_departements_20261020.parquet` | 20/10/2026 | `cartiflette==0.4.0`, départements de France entière, COG 2025, sans simplification | `a6e4d3b3a7657f61b8fe9b710efa5f50c0cab76cde0d522f4cfd4adfdbe405ca` |
| `contours_aav_<code>_20261013.parquet` | 13/10/2026 | `cartiflette==0.4.0`, contours des communes et arrondissements par aire, COG 2025, sans simplification | `002` : `5fc255ef5f92c540c5037f793c15c24007642c7cdce256a1e4f47d516176f231`<br>`004` : `6ff1e4bc0675ab567b7af3eb506774c0740ab855c5f333c66ee6b8fe1eb89982`<br>`005` : `c42afd4910a9a6907c54e2f8d476b8a4b6db3630bf9ffdff7b41cedf8a3b2c6e`<br>`006` : `6e0cb9a94a69887fd123a2d57c49068aa25b207da9541813652c00f1b2930c28`<br>`008` : `54665ed725b9ae364166d6dc76cd09b71b8e42397916e6fe564d8f0308786e59`<br>`010` : `454d27768198bb48be5882987f3aa36f88902add34bf443dff0cd37cc8be7790`<br>`013` : `c846f8d895d3121435037f5c04054a9e2275bb95e2de1791cae61498550b4cec`<br>`014` : `a1d13c20cc9565de3e2b3bb78b8d020076bae7c2a94ac2648d7aa96aa0699357` |
| `contours_iris_<code>_20261021.parquet` | 21/10/2026 | `cartiflette==0.4.0`, contours des IRIS par aire retenue, COG 2025, sans simplification | `008` : `61e52233fcdd7fe09d0f0350b6a5060719ca83f0a56c7710848a5ae35d34ff23`<br>`002` : `5c77cb03f2cfb55e3e2634218f4f94b6b43f13ed1496e85572919dc271b43018`<br>`010` : `15b57329479d4261de4a443b9b4458332f92692b286caecbb270a3b678aad82c` |

Les fichiers de l'Insee (aires d'attraction des villes, recensement, table de passage des codes communes) ne changent pas. Ils sont lus à leur adresse d'origine et, si le site de l'Insee ne répond pas, dans la même release, avec le même contrôle du `sha256` (adresses dans `src/cadres_lycees/config.py`).

**Refaire un gel** (seulement pour changer de copie) :

```python
from cadres_lycees import collecte

collecte.geler_annuaire("raw/annuaire_education_AAAAMMJJ.parquet")  # renvoie le sha256
collecte.geler_gares("raw/gares_voyageurs_AAAAMMJJ.parquet")
collecte.geler_apl("raw/apl_medecins_generalistes_AAAAMMJJ.xlsx")
collecte.geler_equipements_sportifs("raw/equipements_sportifs_AAAAMMJJ.parquet")
collecte.geler_bpe("raw/bpe_2025_AAAAMMJJ.parquet")
collecte.geler_dvf("raw/statistiques_dvf_AAAAMMJJ.csv")
collecte.geler_chefs_lieux("raw/chefs_lieux_cog2025_AAAAMMJJ.parquet")
collecte.geler_contours(
    "raw/contours_aav_013_AAAAMMJJ.parquet",
    valeur="013",
    maille="COMMUNE_ARRONDISSEMENT",
    filtre="AIRE_ATTRACTION_VILLES",
)
collecte.geler_contours(
    "raw/contours_departements_AAAAMMJJ.parquet",
    valeur="France",
    maille="DEPARTEMENT",
    filtre="FRANCE_ENTIERE",
)
collecte.geler_contours(
    "raw/contours_iris_008_AAAAMMJJ.parquet",
    valeur="008",
    maille="IRIS",
    filtre="AIRE_ATTRACTION_VILLES",
)
```

Ces fonctions refusent d'écraser un fichier existant. Il faut ensuite reporter le chemin et le `sha256` dans `config.py`, publier le fichier sur la release ci-dessus et mettre à jour ce tableau.

## Usage de l'IA générative

Nous avons utilisé un assistant de code (Claude Code, d'Anthropic) pour accélérer le projet, dans un cadre fixé dès le départ : l'assistant exécutait des étapes dont nous avions défini la méthode, et rien n'était intégré sans notre relecture.

**Ce qui vient du groupe.** La question de recherche, les hypothèses, le choix des trois aires, l'organisation de la base de données, la méthode (paires de communes contiguës, anneaux de distance, bootstrap par commune, régression de H3, choix des contrôles et des mauvais contrôles) et l'interprétation des résultats. Ces choix ont été affinés au fil des premières analyses, en revenant aux données et à leurs limites.

**Comment l'assistant était encadré.** Nous lui avons donné des règles écrites :

- il ne codait qu'une étape à la fois, après que nous lui avions donné la méthode à suivre et la structure attendue, et il résumait ce qu'il allait faire avant de le faire ;
- il ne pouvait pas avancer sans que nous soyons à jour de ce qu'il avait fait : chaque étape était relue et ses sorties vérifiées avant de passer à la suivante ;
- il ne devait rien ajouter qui n'ait été demandé (fonctions, tests ou documents superflus), ni modifier du code hors de l'étape en cours ;
- toutes les constantes vont dans `config.py`, et une assertion vérifie le résultat de chaque jointure ou filtre qui peut perdre des lignes.

Ces règles et des contrôles automatiques (ruff, tests) faisaient partie de notre environnement de travail.

**Pipeline et analyses** (`src/cadres_lycees/`). L'architecture du pipeline et la méthode de chaque étape viennent du groupe. L'assistant a écrit le code des parties mécaniques une fois ces choix faits : par exemple les jointures une fois l'organisation de la base décidée, ou le calcul des distances une fois la méthode des paires choisie. Chaque fonction a été relue et ses résultats contrôlés par le groupe.

**Tests, figures, cartes interactives, site Quarto et présentation.** Nous avons décidé ce que chaque figure devait montrer et quels calculs méritaient un test. L'assistant a écrit le code, en particulier pour Quarto et les cartes interactives, que nous ne connaissions pas ; nous avons relu ce code et ajusté le rendu.

**Recherche des sources.** Nous avons cherché les données nous-mêmes, puis demandé à l'assistant d'autres sources possibles ; nous avons vérifié et retenu chaque source.

**Texte du rapport.** Rédigé ensemble, puis relu avec l'assistant pour le clarifier et alléger le style. Chaque passe a été relue par nous, et les interprétations sont les nôtres.

**Répartition du travail.** Solal : construction et nettoyage de la base de données. Gabriel : méthodologie d'analyse. Giulio : rédaction du rapport et visualisations, avec une aide sur les autres parties. Chacun a ensuite relu l'ensemble du projet, et chacun peut expliquer le code.

**Historique Git.** Nous avons d'abord travaillé dans d'autres dépôts, où les versions des branches se sont mélangées. Nous avons repris le projet dans ce dépôt, créé le 08/11/2026, en demandant à l'assistant d'y transférer le travail déjà fait. C'est lui qui a recréé l'historique, et une partie des commits a été faite directement par l'assistant. Les dates et les auteurs des commits ne correspondent donc ni au moment où chaque étape a été faite, ni à la personne qui l'a faite : la répartition réelle du travail est celle décrite plus haut.

## Organisation

- `src/cadres_lycees/` : le code du pipeline, un module par étape, et le tableau de support du choix des aires (`tableau_support.md`).
- `presentation/` : la présentation interactive de soutenance, un gabarit HTML et JavaScript (`page.html`) et le script qui y insère les données et les résultats (`construire.py`).
- `tests/` : les tests des calculs critiques (accessibilité, paires de communes contiguës, fusion des anneaux, bootstrap par commune, sens des paires, verdicts de H1 et de H3).
- `docs/` : le [dictionnaire des variables](docs/dictionnaire_variables.md) de la base communale (`pipeline.construire_base`).
