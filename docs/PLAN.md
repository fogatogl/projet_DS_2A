# Lycées et géographie des cadres dans trois aires urbaines de province

> **Projet** : Python pour la data science (ENSAE), groupe de 3 personnes **Rendu** : mardi 24 novembre 2026 · **Soutenance** : janvier 2027 **Grille d'évaluation** : https://pythonds.linogaliana.fr/content/annexes/evaluation.html **Statut du document** : plan de référence du projet. Toute décision qui s'en écarte est notée dans le journal des décisions (section 13).

------------------------------------------------------------------------

## Sommaire

0.  Résumé du projet
1.  Problématique, contexte et hypothèses
2.  Périmètre et choix structurants (fixés avant de voir les résultats)
3.  Sources de données
4.  Construction de la base communale (pipeline)
5.  Méthodologie d'analyse
6.  Plan du rapport final
7.  Organisation du dépôt
8.  Conventions de travail
9.  Calendrier, rôles et jalons
10. Risques et ordre de sacrifice
11. Checklist de rendu
12. Instructions pour Claude Code : par où commencer
13. Journal des décisions

------------------------------------------------------------------------

## 0. Résumé du projet

**Question.** Dans des aires urbaines de province aux traditions scolaires contrastées, les communes offrant un meilleur accès à des lycées privés ou à forte valeur ajoutée concentrent-elles davantage de cadres que leurs voisines, et ce lien résiste-t-il face aux autres infrastructures ?

**Approche.**

- On construit une base à une ligne par commune pour trois aires d'attraction des villes (hors Paris), en croisant le recensement, les données de l'Éducation nationale et des données d'infrastructures.
- On mesure l'accès de chaque commune aux lycées, et non leur simple présence dans la commune.
- On compare les communes à position égale dans l'aire : par anneaux de distance au centre, puis par paires de communes contiguës.

**Statut des résultats.** Le projet décrit des associations, pas des effets causaux. Un résultat nul bien établi est un résultat valable et sera présenté comme tel.

------------------------------------------------------------------------

## 1. Problématique, contexte et hypothèses

### 1.1 Contexte et littérature

- **Fack G. et Grenet J. (2010)**, « When do better schools raise housing prices? Evidence from Paris public and private schools », *Journal of Public Economics*, 94(1-2), p. 59-77. À Paris, une hausse d'un écart-type de la performance des collèges publics augmente les prix immobiliers de 1,4 à 2,4 %. Cet effet diminue quand l'offre privée à proximité augmente. C'est notre mécanisme de départ : l'offre scolaire entre dans les choix résidentiels, et le privé joue le rôle d'option de repli.
- **Black S. (1999)**, « Do Better Schools Matter? Parental Valuation of Elementary Education », *Quarterly Journal of Economics*. C'est la référence méthodologique sur la comparaison de logements situés de part et d'autre des limites de secteurs scolaires. Notre comparaison entre communes contiguës en est une version simplifiée.
- **Le contraste régional (DEPP, Repères et références statistiques).** En métropole, environ 78 % des élèves du second degré sont scolarisés dans le public, contre seulement six sur dix environ dans les académies de Rennes et de Nantes. Dans l'Ouest, le privé est un choix courant. On s'attend donc à ce qu'il y soit moins socialement sélectif.

### 1.2 Hypothèses

Elles sont fixées avant toute analyse. L'indicateur principal est défini en section 2.4.

| ID | Énoncé | Mesure | Test principal | Figure |
|-------------|-------------|-------------|---------------------|-------------|
| H1 | À distance égale du centre de l'aire, la part de cadres est plus élevée dans les communes ayant un meilleur accès aux lycées privés sous contrat. | `dist_lyc_prive_min` (principale) et `n_lyc_prive_5km` (secondaire) contre `part_cadres_2022` | Différences entre communes contiguës (5.3), complétées par les anneaux de distance (5.2) | Fig. 5, 4 |
| H2 | Ce lien est plus faible dans l'aire de l'Ouest, où le privé est plus répandu. | H1 estimée aire par aire | Comparaison des écarts entre aires (5.4) | Fig. 4 (une facette par aire) |
| H3 | C'est la qualité des lycées accessibles (valeur ajoutée IVAL), plus que leur nombre, qui accompagne la hausse de la part de cadres entre 2011 et 2022. | `ival_moy_5km` contre `evol_cadres_pts`, à nombre de lycées égal | Section 5.5 | Fig. 6 |
| H4 | L'association avec les lycées est plus forte que celle avec les autres infrastructures (gares, médecins, équipements). | Même fonction d'accessibilité appliquée à chaque infrastructure | Section 5.7 ; descriptive, sans verdict (journal du 03/11/2026 : aucune règle fixée avant l'estimation) | Fig. 7 |

### 1.3 Ce que le projet ne peut pas montrer

- **Causalité inverse.** Les lycées privés peuvent s'implanter ou se maintenir là où vivent déjà les familles aisées.
- **Sélection résidentielle non observée.** Les préférences des ménages ne sont pas mesurées.
- **Croissance démographique non contrôlée.** Elle peut attirer des lycées et accompagne l'arrivée des cadres ; elle reste hors des contrôles (§2.5), et une partie de l'association peut lui revenir.
- **Mesure d'accès imparfaite.** Les distances sont calculées à vol d'oiseau depuis un point de référence unique par commune.

Ces limites sont annoncées dès l'introduction du rapport et reprises dans la conclusion.

------------------------------------------------------------------------

## 2. Périmètre et choix structurants (fixés avant de voir les résultats)

Fixer ces choix à l'avance évite de chercher la spécification qui « marche ». Toute modification est justifiée dans le journal des décisions (section 13).

### 2.1 Unité et géographie

- **Unité d'observation** : la commune. Pour Lyon, Marseille et Paris, ce sont les arrondissements municipaux.
- **Géographie de référence** : le Code officiel géographique (COG) au 1er janvier 2025, celui du recensement 2022. Toutes les sources sont ramenées à cette géographie grâce à la table de passage de l'Insee.
- **Projection** : Lambert 93 (EPSG:2154) pour tous les calculs de distance, en mètres. WGS84 (EPSG:4326) uniquement pour les cartes interactives.

### 2.2 Périmètre géographique

- **Trois aires d'attraction des villes** (zonage Insee 2020), pôle et couronne compris. Paris est exclu, à cause du poids des transports en commun.
- **Choix des aires (semaine 1, à partir des données).**
  - Candidates : Rennes, Nantes, Toulouse, Bordeaux, Lyon, Grenoble, Lille, Strasbourg.
  - Critères :
    - (a) au moins une aire de l'Ouest (Rennes ou Nantes) ;
    - (b) un contraste dans le poids du privé, mesuré par la part de lycées privés sous contrat et l'écart d'IPS moyen entre public et privé ;
    - (c) des tailles d'aire comparables (population de l'aire : somme de `P22_POP` du recensement 2022) ;
    - (d) au moins une dizaine de lycées privés par aire (seuil indicatif) ;
    - (e) un support suffisant de l'exposition : le nombre de cellules estimables à 10 km (règle du §5.2, après fusion des anneaux et contrôle de l'équilibre de distance) et le nombre de paires de communes contiguës dont le statut exposé/non exposé diffère (au moins un lycée privé sous contrat à 10 km). Les valeurs à 5 km sont journalisées à côté. L'aire de l'Ouest retenue est celle qui maximise le nombre de cellules estimables ; à égalité, celle qui compte le plus de paires de statut différent ;
    - (f) la faisabilité : le coût réel de Lyon est mesuré avant toute décision ; mesuré le 20/10, il est nul pour la variable à expliquer, la source du §2.3 donnant les arrondissements avec la même définition (A11). Une exclusion de Lyon est justifiée par écrit, en rappelant que d'après les premiers comptes d'exposition Lyon est l'aire la mieux dotée en support.
  - Les valeurs de tous les critères (a) à (f) pour les 8 candidates sont journalisées au moment du choix (§13), dans le tableau de support décrit au §5.2.
  - Le choix et ses justifications forment la section 3.1 du rapport.

### 2.3 Variable à expliquer

- **Principale** : la part des cadres et professions intellectuelles supérieures (groupe socioprofessionnel 3) parmi les actifs de 25 à 54 ans, en 2011 et en 2022.
  - **Source** : recensement 2022, « Évolution et structure de la population » (source 2), qui donne 2011 et 2022 en COG 2025, avec les arrondissements de Lyon. Numérateur `C22_POP2554_STAT_GSEC13_23` (2022) et `C11_POP2554_CS3` (2011) ; dénominateur, la somme des 6 groupes socioprofessionnels des 25-54 ans, c'est-à-dire les actifs occupés et les chômeurs ayant déjà travaillé. C'est la définition des séries historiques de l'Insee, la même pour les deux années, et leurs valeurs sont identiques (A11).
  - **Pourquoi 25-54 ans** : c'est l'âge des parents de lycéens, et cela neutralise les écarts de structure par âge (les retraités en particulier).
- **Dérivée** : `evol_cadres_pts` = part en 2022 moins part en 2011, en points de pourcentage.
- Une commune sans actif de 25 à 54 ans à une date (somme des 6 groupes nulle) n'a pas de part à cette date : la valeur est manquante à cette date seulement, et la commune reste dans les analyses de l'autre date. Ces communes sont nommées dans `config.py`, d'après les seuls effectifs d'actifs ; toute autre commune sans actif fait échouer.
- **Robustesse** : la part de cadres dans la population de 15 ans ou plus (recensement 2022, base « Évolution et structure de la population »).
- Le passage à la nomenclature PCS 2020 dans le recensement 2022 ne change pas les deux premiers niveaux : selon l'Insee, « les premier et deuxième niveaux de la PCS 2020 sont restés inchangés par rapport aux versions précédentes (1982 et 2003) » (documentation de la source 2, rubrique « CSP / PCS / PCS-ESE », lue le 20/10/2026). Le groupe des cadres reste donc comparable dans le temps. Non vérifiés : les reclassements de professions détaillées et les changements de codage entre les deux recensements. S'ils sont uniformes dans une aire, les effets fixes de H3 (§5.5) les absorbent ; s'ils sont liés à la composition des communes, ils sont une limite de H3. H1, H2 et H4 n'utilisent que 2022.

### 2.4 Indicateur principal d'accès aux lycées (fixé maintenant)

- **Lycées retenus** : lycées d'enseignement général et technologique, et lycées polyvalents, publics et privés sous contrat. Les lycées professionnels seuls et le privé hors contrat sont exclus de l'indicateur principal et réintégrés en robustesse ; les lycées agricoles sont exclus partout, robustesse comprise (journal du 03/11/2026 : leur privé relève d'un contrat avec le ministère de l'Agriculture, que le plan ne définit pas).
- **Point de référence de la commune** : son centroïde géométrique. Le chef-lieu (point mairie de la couche ADMIN EXPRESS de l'IGN) est une alternative testée en robustesse.
- **Rayon principal : 5 km.** Les rayons de 3 et 10 km servent en robustesse.
- **Indicateurs calculés pour chaque commune** :
  - `n_lyc_prive_5km`, `n_lyc_public_5km` : nombre de lycées dans le rayon ;
  - `dist_lyc_prive_min`, `dist_lyc_public_min` : distance au plus proche, en km ;
  - `ival_moy_5km` : pour chaque lycée, moyenne simple des `va_acces_2nde` des sessions 2012 à 2022, à condition d'avoir au moins 5 sessions valides (`va_acces_2nde` renseignée) ; puis moyenne des lycées du rayon, pondérée par la moyenne de `presents_total` sur ces sessions. Les lycées de moins de 5 sessions valides restent comptés dans les `n_lyc_*` mais sortent de l'IVAL. Le stock de lycées est l'instantané de l'annuaire du 13/10/2026 (les lycées fermés en sont absents).
- **Effet de bord** : les indicateurs sont calculés sur tous les lycées retenus de France métropolitaine (2 413 UAI dans l'annuaire du 13/10/2026), y compris hors des aires. Une marge de 10 km au-delà de l'aire suffit pour les comptes, mais pas pour la distance au plus proche lycée. Les lycées étrangers sont absents de l'annuaire.

### 2.5 Variables de contrôle et « mauvais contrôles »

- **Contrôles** :
  - `dist_centre_km` : distance au centroïde de la commune-centre de l'aire (`CATEAAV2020` = 11 dans le zonage de l'Insee ; Lyon entière, réunion de ses arrondissements) ;
  - `densite` : habitants par km² (`P22_POP` / `SUPERF`, série historique du recensement 2022), en logarithme népérien partout où elle sert de contrôle (`log_densite` dans les cellules du §5.2, `d_log_densite` dans les paires du §5.3) ;
  - `aire` : effet fixe, c'est-à-dire qu'on compare toujours à l'intérieur d'une même aire.
- **Mauvais contrôles**, jamais utilisés comme contrôles dans la spécification principale :
  - le niveau de vie médian (Filosofi), qui est en grande partie une conséquence de la part de cadres ;
  - l'IPS des lycées, construit à partir de la profession des parents et donc quasi mécaniquement lié à la part de cadres.
  - Ces deux variables restent purement descriptives.
  - La croissance de la population (série historique du recensement) joue deux rôles : elle peut attirer des ouvertures de lycées (les communes « sans IVAL » du §5.5 sont surtout des ouvertures récentes en périurbain), donc confondre l'association ; elle se fait aussi en partie par l'arrivée des mêmes ménages que les cadres, en même temps que `evol_cadres_pts` sur 2011-2022 (H3), et la contrôler en retirerait une partie. Elle reste hors des contrôles, sans robustesse dédiée, et la confusion possible est une limite (§1.3).
- **Prix immobiliers (DVF)** : ils sont à la fois cause et conséquence. On les présente avec et sans ce contrôle, à Lyon et à Nantes (l'Alsace-Moselle n'est pas dans DVF), et on discute l'écart.

------------------------------------------------------------------------

## 3. Sources de données

Priorité : **P1** = indispensable aux hypothèses H1 à H3, **P2** = partie 5 et contrôles, **P3** = bonus si le temps le permet. Les URL marquées « à confirmer » doivent être vérifiées en semaine 1, et le lien direct de téléchargement copié dans `config.py`.

### 3.1 Tableau des sources

| # | Source | Producteur | Maille | Accès | Rôle | Priorité |
|-----------|-----------|-----------|-----------|-----------|-----------|-----------|
| 1 | Séries historiques : population active de 25-54 ans par CSP (1968-2022) — https://www.insee.fr/fr/statistiques/1893185 | Insee | Commune | Fichier | Fig. 2 (§5.1) : part de cadres de 25-54 ans en 1999, 2006, 2011, 2016 et 2022, chaque date ramenée au COG 2025 par la table de passage (source 9), Lyon entière ; contrôle de cohérence de la source 2 (mêmes valeurs en 2011 et 2022) | Carte descriptive |
| 2 | Recensement 2022, « Évolution et structure de la population » — https://www.insee.fr/fr/statistiques/8581696 | Insee | Commune et arrondissement | Fichier | Variable à expliquer (2011, 2022) ; robustesse (cadres 15 ans ou plus) | P1 |
| 2 bis | Recensement 2022, séries historiques — https://www.insee.fr/fr/statistiques/8582555 | Insee | Commune | Fichier | Population (`P22_POP`), superficie (`SUPERF`), densité ; population de l'aire (critère c) | P1 |
| 3 | Annuaire de l'éducation — https://data.education.gouv.fr/explore/dataset/fr-en-annuaire-education/api/ | Ministère de l'Éducation nationale | Établissement (point) | **API** Opendatasoft | Liste des lycées, statut public/privé, coordonnées | P1 |
| 4 | Adresse et géolocalisation des établissements — https://www.data.gouv.fr/datasets/adresse-et-geolocalisation-des-etablissements-denseignement-des-premier-et-second-degres | Ministère de l'Éducation nationale | Point | Fichier ou API | Coordonnées de secours si l'annuaire en manque | P1 |
| 5 | IPS des lycées (à partir de 2023) — https://www.data.gouv.fr/datasets/ips-lycees-a-partir-de-2023 | DEPP | Établissement | Fichier ou API | Descriptif : écart public/privé par aire (choix des aires, H2) | P1 |
| 6 | IVAL, lycées d'enseignement général et technologique — https://www.data.gouv.fr/datasets/6707515c84dfa4012c3ecd45 | DEPP | Établissement | Fichier ou API | Qualité des lycées (H3) | P1 |
| 7 | Contours communaux (IGN ADMIN EXPRESS via `cartiflette`) — https://github.com/inseefrlab/cartiflette | IGN / InseeFrLab | Commune (polygone) | Package Python | Géométries, centroïdes, contiguïté | P1 |
| 8 | Zonage en aires d'attraction des villes 2020 (table d'appartenance des communes) — insee.fr, *à confirmer* | Insee | Commune | Fichier | Périmètre, pôle et couronne, commune-centre | P1 |
| 9 | Table de passage annuelle des codes communes (COG) — insee.fr, *à confirmer* | Insee | Commune | Fichier | Harmonisation des géographies | P1 |
| 10 | « Statistiques DVF » d'Etalab, jeu data.gouv `statistiques-dvf` (URL du fichier dans `config.py`) ; les DVF géolocalisées ne remontent plus à 2020 | DGFiP / Etalab | Commune (agrégat) | Fichier, copie gelée du 03/11/2026 | Prix médian au m², juillet 2021 à juin 2026 (contrôle discuté, robustesse à Lyon et Nantes ; Alsace-Moselle hors DVF) | P2 |
| 11 | Filosofi 2021, communes — https://www.insee.fr/fr/statistiques/7756855?sommaire=7756859 | Insee | Commune | Fichier | Descriptif uniquement ; abandonné le 03/11 (aucune hypothèse ne l'utilise) | Abandonnée |
| 12 | Gares de voyageurs, export Opendatasoft `gares-de-voyageurs` de SNCF Gares & Connexions (URL dans `config.py` ; data.gouv ne fait que pointer vers cet export) | SNCF Gares & Connexions | Point | API (export), copie gelée du 03/11/2026 | H4 : distance à la gare la plus proche | P2 |
| 13 | APL aux médecins généralistes, pièce jointe du jeu DREES `530_l-accessibilite-potentielle-localisee-apl` (URL dans `config.py` ; la page de l'Observatoire des territoires n'offre pas de fichier) | DREES | Commune et arrondissement | Fichier, copie gelée du 03/11/2026 | H4 : santé, APL 2024 tous âges, utilisée directement | P2 |
| 14 | Base permanente des équipements 2025, fichier détail géolocalisé — https://www.insee.fr/fr/statistiques/8217525 (le lien data.gouv d'origine était une republication de la BPE 2023 par l'Île-de-France) | Insee | Point | Fichier, copie gelée du 03/11/2026 | H4 : équipements culturels (sous-domaine F3) | P2 |
| 15 | Data ES, équipements sportifs, API nationale du ministère des Sports, jeu `data-es` (URL dans `config.py` ; le lien data.gouv d'origine ne couvrait que l'Île-de-France) | Ministère des Sports | Point | API (export), copie gelée du 03/11/2026 | H4 : installations sportives | P2 |
| 16 | Migrations résidentielles, fichier détail MIGCOM 2022 — https://www.insee.fr/fr/statistiques/8589767 | Insee | Individu (Parquet, environ 17 millions de lignes) | Fichier | Piste de conclusion (§6), sans code | Piste |
| 16 bis | Bases infracommunales « Activité des résidents », 2011 et 2022 — insee.fr, pages 8647006 (2022) et 2028668 (2011), URL et sha256 dans `docs/exploration_sources.md` §12 ; contours IRIS par `cartiflette`, en copie gelée (§7) | Insee | IRIS | Fichier | Carte des limites (§6), exploration au sens du §5.8 : part de cadres de 15 à 64 ans par IRIS en 2011 et 2022 | P3 |
| 17 | Fiscalité locale des particuliers — https://data.economie.gouv.fr/explore/dataset/fiscalite-locale-des-particuliers-geo | DGFiP | Commune | API | Bonus : taux de taxe foncière | P3 |
| 18 | Aménagements cyclables — https://www.data.gouv.fr/datasets/60a37b7f303fdf4f2654b73d | Geovelo / OpenStreetMap | Ligne | Parquet | Bonus : cadre de vie | P3 |

### 3.2 Points d'attention à documenter dans le rapport (encadré « choix et biais »)

- **IPS** : les données du privé ne sont pas comparables avant 2023, car la remontée des professions des parents s'y est fortement améliorée. On n'utilise que la série à partir de 2023. L'IPS reste descriptif (voir 2.5).
- **IVAL** : c'est une mesure relative, qui ne couvre que le public et le privé sous contrat, et qui comprend plusieurs indicateurs (taux de réussite, taux d'accès de la seconde au bac, taux de mentions). Indicateur principal : **valeur ajoutée du taux d'accès de la seconde au bac**, car il reflète le parcours complet de l'élève. Le taux de réussite sert en robustesse. Décalage temporel : les IVAL sont récents, alors que l'évolution des cadres porte sur 2011-2022. Vérification faite le 13/10/2026 : l'ancienne version de data.gouv est identique à la v2 (pas de millésime indépendant), et la valeur ajoutée d'un lycée est peu stable d'une session à l'autre (corrélation de 0,56 à un an, 0,32 à cinq ans, 0,12 entre 2012 et 2025). On retient donc la moyenne des sessions 2012 à 2022 (§2.4), qui couvre la période entre les deux recensements ; c'est un choix de conception, pas un constat de stabilité. Contrôle sans cadres : pas de rupture de la corrélation de `va_acces_2nde` autour de 2016-2017 (0,60 entre 2016 et 2017), un creux vers 2017-2020 de cause non vérifiée, guides méthodologiques 2016 et 2020 non lus. **Fiabilité**, calculée et journalisée après le choix des aires et avant le premier commit de T5 : pour les lycées de la règle du §2.4 qui ont au moins 3 sessions valides dans chaque moitié, on calcule deux `ival_moy_5km` par commune, l'un sur 2012-2017, l'autre sur 2018-2022, avec les poids de l'indicateur principal ; on prend la corrélation de Pearson entre les deux sur les communes de la population de H3 (§5.5) des 3 aires retenues, après centrage par aire, corrigée par Spearman-Brown (2r / (1 + r)). Seule cette valeur, toutes aires ensemble, tranche H3 ; les valeurs par aire sont descriptives. Le nombre de lycées distincts est donné à côté de chaque valeur : des communes voisines partagent les mêmes lycées (leurs disques de 5 km se recouvrent), ce qui réduit l'effectif réel et peut gonfler la corrélation. En dessous de 0,5, H3 est « non testable avec cette mesure » (ni confirmée ni infirmée). Elle est calculée par `h3.fiabilite_ival`, que le rapport appelle à la section 4.4, où H3 est présentée ; l'encadré « choix et biais » y renvoie. Robustesse : moyenne sur 2012-2025.
- **Filosofi** : le millésime 2021 est le dernier de l'ancien dispositif. Le millésime 2023 (Filosofi 2) n'est pas comparable et ne fournit que deux indicateurs à la commune.
- **Secret statistique et petites communes** : on signale les communes de moins de 200 actifs de 25-54 ans (seuil indicatif), comptés en 2022 pour H1, H2 et H4, et au plus petit de 2011 et 2022 pour H3, dont la variable mêle les deux recensements. Les moyennes sont pondérées par `actifs_2022`, sauf les pentes des paires (§5.3) et H3 (§5.5). On teste aussi l'exclusion de ces communes.
- **DVF** : fenêtre de cinq ans glissants. On utilise la médiane du prix au m² des ventes d'appartements et de maisons réunies, calculée par Etalab sur toute la période publiée (juillet 2021 à juin 2026 dans la copie du 03/11/2026 ; aucune source DVF ne remonte à 2020, la fenêtre 2020-2024 n'existe plus), à condition d'avoir au moins 10 ventes (sinon valeur manquante, signalée). L'Alsace-Moselle n'est pas dans DVF (livre foncier) : pas de prix dans l'aire de Strasbourg.

------------------------------------------------------------------------

## 4. Construction de la base communale (pipeline)

``` mermaid
flowchart LR
    A[Référentiel communes<br/>AAV + COG + contours] --> D[Accessibilité<br/>fonction générique]
    B[Recensement<br/>cadres 2011 et 2022] --> G[Base communale<br/>final/base_communale.parquet]
    C[Lycées<br/>API annuaire + IPS + IVAL] --> D
    E[Autres points<br/>gares, BPE, Data ES] --> D
    D --> G
    F[Contrôles<br/>distance centre, densité, DVF] --> G
    A --> P[Paires contiguës<br/>final/paires.parquet]
    G --> P
```

Chaque étape correspond à une fonction de `src/cadres_lycees/`. Elle lit les données brutes depuis S3 (et les télécharge si elles n'y sont pas encore), puis écrit son résultat sur S3. Chaque étape se termine par des **vérifications** (`assert`) qui font échouer le code bruyamment si une jointure perd des lignes. Tous les téléchargements passent par une seule fonction, `stockage.copie_controlee(urls, chemin, sha256)`, qui essaie les URL dans l'ordre (pour les copies gelées, la release `donnees-20261020` du dépôt de référence, puis la même release du dépôt du groupe ; le dossier public du bucket n'est plus essayé depuis le 04/11) et échoue si le `sha256` diffère. Les sources mutables sont collectées une fois par leur API (export Opendatasoft de l'annuaire, cartiflette pour les contours) en une copie gelée datée ; le rapport lit ces copies, dont la date, l'URL d'origine et le `sha256` sont donnés dans le README et dans la section 2.1 du rapport.

| Étape | Fonction(s) | Sortie | Vérifications |
|----------------|-------------------|----------------|----------------------|
| A. Référentiel | `geo.referentiel_communes(aires)` | GeoDataFrame des communes des 3 aires : `code_commune`, `aire`, `pole_couronne`, `geometry`, `centroide`, `dist_centre_km` | Nombre de communes égal à celui de la table AAV ; codes uniques ; aucune géométrie vide |
| B. Cadres | `collecte.evol_struct_rp2022()`, `nettoyage.part_cadres()` | `part_cadres_2011`, `part_cadres_2022`, `evol_cadres_pts`, `actifs_2011`, `actifs_2022` | Parts comprises entre 0 et 1 ; aucune commune manquante (fichier en COG 2025) ; communes sans actif nommées (§2.3) |
| C. Lycées | `collecte.annuaire_education()` (France métropolitaine, copie gelée du 13/10/2026), `collecte.ips_lycees()`, `collecte.ival_lycees()`, `nettoyage.lycees_geo()` découpée en quatre fonctions (lycées retenus, aire, IPS, IVAL) | GeoDataFrame des lycées : `uai`, `secteur`, `aire`, `ips`, `ival`, `poids_ival`, `geometry` | Identifiants UAI uniques ; part des lycées géolocalisés > 98 % ; part des lycées avec IVAL indiquée dans le rapport ; un lycée sans statut public/privé fait échouer la collecte, sauf `0271911F`, écarté nommément ; listes d'UAI nommées propres aux 3 aires retenues |
| D. Accessibilité | `accessibilite.indicateurs(communes, points, prefixe, rayons, attribut, poids)`, filtre public/privé fait avant l'appel | Colonnes `n_<x>_<r>km`, `dist_<x>_min`, `<attr>_moy_<r>km` | Tests unitaires sur données jouets (`tests/test_accessibilite.py`) ; `assert` dans le pipeline : les comptes du tableau de support (§2.2, §5.2) sont reproduits pour les aires retenues |
| E. Contrôles | `collecte.statistiques_dvf()`, `nettoyage.prix_m2()`, `collecte.serie_historique_rp2022()`, `nettoyage.population()` | `prix_m2_med`, `log_prix_m2`, `densite` | Nombre de ventes par commune ; règle du seuil de 10 ventes appliquée |
| F. Paires | `geo.paires_contigues(communes, variables)` | Une ligne par paire (i < j, ordre des codes) de communes contiguës au sens Queen (bord ou point commun) dans une même aire, avec les écarts `d_part_cadres_2022`, `d_n_lyc_prive_5km`, etc. (`d_<v>` pour chaque variable `v`) | Pas de doublon (i,j)/(j,i) ; les deux communes appartiennent à la même aire ; une commune sans voisine fait échouer |
| G. Table finale | `pipeline.construire_base(aires)`, appelée par `rapport.ipynb` : le rapport reconstruit la base depuis les copies gelées, `final/` n'est qu'une sortie | `final/base_communale.parquet`, `final/paires.parquet`, `docs/dictionnaire_variables.md` | Une ligne par commune ; dictionnaire à jour ; moins de 30 minutes depuis le brut gelé, bootstrap compris, mesuré dès le test complet de S4 |

------------------------------------------------------------------------

## 5. Méthodologie d'analyse

Rappel : l'ENSAE n'attend plus de partie modélisation. L'analyse repose sur des comparaisons transparentes. Une régression linéaire peut apparaître, uniquement comme outil descriptif (« à distance au centre égale, l'écart vaut… »), jamais comme exercice de prédiction.

### 5.1 Descriptif (sections 3.1 à 3.3 du rapport)

- **Fig. 1** : pour les 8 candidates, les 3 aires retenues mises en avant : part du privé sous contrat en nombre de lycées et pondérée par les candidats au bac (moyenne de `presents_total` de l'IVAL, couverture indiquée), et IPS de chaque lycée par secteur (un point par lycée, moyenne et écart privé moins public). Justifie le choix des aires ; pour H2, elle montre les deux dimensions du critère (b), la prévalence du privé et sa sélectivité sociale (§1.1).
- **Fig. 2** : carte folium à curseur, une par aire en onglets, de la part de cadres de 25-54 ans par commune aux recensements 1999, 2006, 2011, 2016 et 2022 (source 1, chaque date ramenée au COG 2025 par la table de passage ; Lyon entière, la série n'ayant pas ses arrondissements ; communes de moins de 200 actifs pâles), sans lycées. Montre le gradient centre-périphérie, donc pourquoi il faut comparer à distance égale, et son évolution. Descriptive, exploratoire au sens du §5.8. Avant 1999, la table de passage ne suffit pas (`docs/exploration_sources.md` §9). Remplace le 03/11 la courbe par tranches de distance, peu lisible.
- **Fig. 3** : carte folium par aire retenue, en 3 onglets Quarto avec un seul commentaire (vérifié au premier `quarto render`, le 20/10 : la carte d'un onglet caché montrait le monde entier ; un script de `_quarto.yml` la recrée la première fois que son onglet s'affiche ; repli, si un rendu le casse : les trois cartes à la suite) : distance au lycée privé sous contrat le plus proche par commune, lycées en points selon le secteur ; en dernier et si le temps le permet, une couche des limites entre communes contiguës de statut différent.

### 5.2 H1 : comparaison par anneaux de distance (complément des paires)

Les anneaux complètent l'estimation par paires (5.3) là où les cellules sont estimables.

- **Anneaux** : 0-5, 5-10, 10-20, 20-30 et plus de 30 km du centre, borne basse incluse et borne haute exclue. Un anneau vide reste une cellule de 0 commune, soumise aux mêmes règles.
- **Cellule estimable.** Une cellule (aire × anneau) n'est estimée que si les deux conditions suivantes sont remplies, au rayon considéré :
  - chacun des deux groupes, communes **avec** au moins un lycée privé dans le rayon et communes **sans**, compte au moins 15 communes. Sinon, on fusionne, aire par aire et séparément à chaque rayon : tant qu'une cellule ne remplit pas la condition, la plus proche du centre de ces cellules est fusionnée avec sa voisine (anneau immédiatement intérieur ou extérieur, déjà fusionné ou non) qui compte le moins de communes, la plus proche du centre à égalité. Si la dernière cellule restante ne remplit pas la condition, l'aire est « non estimable » par anneaux. Le seuil de 15 communes est celui du plan d'origine ;
  - l'écart entre les distances moyennes au centre des deux groupes, vérifié après fusion, ne dépasse pas 2 km (moyennes simples ; borne proposée le 13/10 et validée le 20/10 ; elle correspond à 20 % de la largeur d'un anneau de 10 km), et la comparaison est contrôlée par `dist_centre_km` et la densité (§2.5) dans la cellule. Une cellule qui dépasse la borne est non estimable, sans nouvelle fusion.
- Dans chaque cellule estimable, l'estimation est l'écart avec/sans dans une régression de `part_cadres_2022` sur l'exposition et les contrôles de la cellule, pondérée par les actifs ; l'écart brut des parts moyennes pondérées est donné à côté.
- Intervalles de confiance par **bootstrap** sur les communes (1 000 tirages avec remise dans chaque groupe de la cellule, percentiles 2,5 et 97,5).
- **Rayons.** Le rayon de 5 km reste principal. Le rayon de 10 km, qui reste une spécification de robustesse (§2.4), est calculé pour les mêmes aires et rapporté à côté du 5 km sans le remplacer ; sa concordance avec le 5 km entre dans le verdict de H1 (§5.3). Comme les fusions diffèrent selon le rayon, la concordance se lit par anneau d'origine : on compare les estimations des deux cellules estimables qui le contiennent, une à chaque rayon.
- **Tableau de support**, livrable commité dans `docs/` avant que le choix des aires soit journalisé, et publié avant tout résultat sur les cadres. Pour chacune des 8 candidates, à 5 et à 10 km : population de l'aire, nombre et part de communes exposées, effectifs avec/sans par cellule après fusion, distance moyenne au centre de chaque groupe, nombre de cellules estimables, nombre de paires de statut différent (l'indicateur 0/1 « au moins un lycée privé sous contrat dans le rayon » diffère entre les deux communes), corrélation non centrée (indépendante du sens i − j) entre `d_dist_lyc_prive_min` et `d_dist_centre_km` dans les paires, et, pour Lille et Strasbourg (seules candidates proches d'une frontière terrestre), nombre de communes à moins de 10 km du contour national (critère f). Il est calculé une seule fois, avec les règles ci-dessus.
- **Fig. 4** : estimations de H1 par aire, en points avec intervalles à 95 %, trois panneaux à axes propres : pente principale des paires, pente secondaire, écarts des cellules estimables à 5 et à 10 km. Les aires sont sur la même ligne d'un panneau à l'autre, ce qui sert aussi H2 (§5.4) ; les cellules non estimables sont nommées en note.

### 5.3 H1 : différences entre communes contiguës (résultat principal)

- Pour chaque paire de communes qui se touchent : `d_part_cadres_2022` comparé à `d_dist_lyc_prive_min`, l'écart de distance au plus proche lycée privé sous contrat. C'est l'estimation principale de H1 et elle porte le verdict. Les écarts de distance au centre (`d_dist_centre_km`) et de densité (`d_log_densite`) sont en contrôle (§2.5), car la distance au plus proche lycée varie avec la distance à la ville et avec la densité.
- `d_n_lyc_prive_5km` est l'estimation secondaire.
- **Logique** : tout ce que deux voisines partagent (marché de l'emploi, climat, prix régionaux) s'annule dans la différence.
- **Fig. 5** : nuage de points regroupé par classes (binned scatter) sur les paires symétrisées (chaque paire dans les deux sens), avec la pente d'une régression des écarts de part de cadres sur les écarts d'accès et les écarts des contrôles. Le sens i − j suit l'ordre des codes : toutes les pentes des paires (principale, secondaire, H4) sont estimées sans constante, sans pondération. Un panneau par aire retenue.
- **Limite** : les paires ne sont pas indépendantes, car une même commune apparaît dans plusieurs paires. Les intervalles sont calculés par bootstrap **par commune**, et non par paire : 1 000 tirages avec remise des communes de l'aire, chaque paire comptée autant de fois que le produit des tirages de ses deux communes, percentiles 2,5 et 97,5. Un tirage dont les régresseurs sont colinéaires est écarté et compté ; au-delà de 50 écartés (5 %), l'intervalle n'est pas rapporté (règle du §5.5).
- **Verdict de H1**, aire par aire, lu sur la pente principale (`d_part_cadres_2022` sur `d_dist_lyc_prive_min`, intervalle de confiance à 95 %). Sens attendu : plus proche d'un lycée privé, plus de cadres (pente négative). Deux estimations « concordent » si elles ont le même signe et des intervalles qui se recoupent ; les estimations de 5 et de 10 km se comparent dans chaque « anneau comparé », c'est-à-dire chaque anneau d'origine couvert par une cellule estimable à chacun des deux rayons (§5.2) ; pour les deux écarts d'accès des paires, on compare seulement le sens. Toute cellule estimable peut contredire ; celles d'un anneau comparé servent en plus à la concordance : si l'intervalle d'une cellule estimable exclut zéro dans le sens contraire à H1 (moins de cadres dans les communes exposées), une pente « confirmée » devient « nuancée » ; s'il exclut zéro dans le sens de H1, un résultat nul n'est pas « établi ».
  - « confirmée » : pente principale dans le sens attendu avec un intervalle qui exclut zéro, pente secondaire dans le sens attendu, estimations concordantes dans chaque anneau comparé, aucune cellule estimable qui la contredise. Sans anneau comparé, le verdict porte la mention « paires seules » dans le tableau des hypothèses (§6) ;
  - « nuancée » : intervalle qui exclut zéro dans le sens attendu, mais pente secondaire de sens contraire, estimations non concordantes dans un anneau comparé, ou cellule estimable qui la contredit ;
  - « infirmée » : pente de sens contraire dont l'intervalle exclut zéro, ou **résultat nul établi**, c'est-à-dire un intervalle qui contient zéro, avec au moins un anneau comparé, des estimations concordantes dans chaque anneau comparé et aucune cellule estimable qui le contredise. Un résultat nul n'est jamais dit « établi » sans anneau comparé ;
  - « non concluante » : tous les autres cas, en particulier un intervalle qui contient zéro sans anneau comparé.

### 5.4 H2 : hétérogénéité entre aires

- On répète 5.2 et 5.3 aire par aire, puis on compare les écarts. Ce sont les facettes de la Fig. 4.
- **H2 est descriptive** : une seule aire de l'Ouest parmi trois. On compare les estimations aire par aire avec leurs intervalles, au même rayon, sans test de différence entre aires.

### 5.5 H3 : qualité ou simple présence

- **Population** : les communes ayant au moins un lycée retenu (§2.4, public ou privé) à 5 km. Celles dont aucun de ces lycées n'a d'IVAL (59 sur 658 dans les 8 candidates, dont 30 sur 97 à Toulouse et 11 sur 62 à Bordeaux, surtout des ouvertures récentes) forment une catégorie « sans IVAL », montrée à part dans la Fig. 6 et exclue de l'estimation et des terciles.
- **Estimation**, sur les communes qui ont un `ival_moy_5km`, les 3 aires ensemble : régression de `evol_cadres_pts` sur `ival_moy_5km` et `log_n_lyc_ival_5km` (logarithme du nombre de lycées à 5 km qui ont une IVAL, c'est-à-dire ceux dont la qualité est mesurée), tous deux centrés réduits dans chaque aire, une seule fois, sur cet échantillon (moyenne et écart-type simples), avec `dist_centre_km` et `log_densite` en contrôle (§2.5) et un effet fixe par aire × anneau (anneaux du §5.2, sans fusion). Elle est sans pondération et sans contrôle par `part_cadres_2011`, dont le bruit de sondage entre aussi, de signe opposé, dans `evol_cadres_pts` ; une convergence entre communes (hausse plus forte là où la part de 2011 était basse) reste donc une confusion possible, dite dans les limites. On note β_q la pente de l'IVAL et β_n celle du nombre de lycées. Le stock de lycées reste l'annuaire de 2026 : un lycée ouvert jusque vers 2018 peut compter, et les lycées fermés depuis 2011 manquent ; ce reste de causalité inverse (§2.5, croissance) gonfle β_n et tire β_q − β_n vers le bas, ce que le rapport dit.
- **Intervalles** : bootstrap par grappes, 1 000 tirages avec remise des grappes dans chaque aire, graine fixée dans `config.py`, percentiles 2,5 et 97,5 de β_q, β_n et β_q − β_n sur les mêmes tirages, sans refaire la standardisation. Une grappe réunit les communes qui ont le même lycée avec IVAL le plus proche de leur centroïde. Des communes de grappes différentes partagent encore des lycées (leurs disques de 5 km se recouvrent) : les intervalles sont optimistes, ce que le rapport dit. Un tirage dont la matrice des régresseurs (effets fixes des cellules présentes compris) n'est pas de plein rang est écarté et compté ; les percentiles portent sur les autres, et le nombre d'écartés est donné à côté de l'intervalle ; au-delà de 50 écartés (5 %), l'intervalle n'est pas rapporté et le verdict est « non concluante ».
- **Verdict de H3**, toutes aires ensemble, si la fiabilité de l'IVAL (§3.2) est d'au moins 0,5, sinon « non testable avec cette mesure » ; première règle vérifiée, dans cet ordre :
  - « infirmée » : l'intervalle de β_q, ou celui de β_q − β_n, est entièrement sous zéro ;
  - « confirmée » : les intervalles de β_q et de β_q − β_n sont entièrement au-dessus de zéro ;
  - « nuancée » : l'intervalle de β_q est au-dessus de zéro, celui de β_q − β_n contient zéro ;
  - « non concluante » : tous les autres cas.
  L'erreur de mesure de l'IVAL atténue β_q et non β_n : la comparaison penche contre H3, ce que le rapport dit. Les pentes par aire, estimées de même, sont descriptives.
- **Fig. 6** : moyenne simple de `evol_cadres_pts` par tercile d'IVAL calculé dans chaque aire, en points avec les intervalles du même bootstrap, une couleur par aire, la catégorie « sans IVAL » à part. Ses intervalles viennent de tirages des grappes sur toute la population (280 communes, « sans IVAL » comprise) ; un tirage sans commune d'une catégorie est écarté pour elle et compté. Elle décrit ; le verdict se lit sur β_q et β_n.

### 5.6 Robustesse (une figure récapitulative, tableau détaillé replié)

- Rayons de 3 et 10 km pour la pente secondaire (la pente principale porte sur une distance, sans rayon ; les cellules à 10 km sont dans la Fig. 4).
- Résultats avec et sans le contrôle du logarithme du prix au m² (`d_log_prix_m2`), à Lyon et à Nantes (Strasbourg hors DVF, §3.2).
- Part de cadres parmi les 15 ans ou plus (recensement 2022) à la place des 25-54 ans.
- Lycées professionnels et privé hors contrat inclus (natures 300, 301, 302, 306 et 320 ; contrats 30, 31 et 10 ; lycées agricoles toujours exclus, §2.4) : seule la distance au lycée privé le plus proche change.
- Commune-centre exclue (la plus proche du centre de l'aire ; Lyon entière, tous ses arrondissements), avec toutes ses paires.
- Communes de moins de 200 actifs exclues.
- Si Lille ou Strasbourg est retenue : communes à moins de 10 km du contour national exclues, car les lycées étrangers manquent à l'annuaire.
- Sans contrôle de densité.
- Distances depuis le chef-lieu (point mairie d'ADMIN EXPRESS COG 2025 de l'IGN, lu par son service WFS, copie gelée du 03/11) au lieu du centroïde (§2.4).
- H3 : IVAL moyenne sur 2012-2025, puis valeur ajoutée du taux de réussite, à la place de l'indicateur principal (§3.2).
- La robustesse de H1 est présentée par une figure (pente principale par aire, avec intervalles, pour les 6 variantes de `config.VARIANTES_FIGURE_ROBUSTESSE`), le tableau détaillé replié dessous gardant toutes les variantes ; celle de H3 par un tableau de β_q, β_n et β_q − β_n.
- **Autocorrélation spatiale** : indice I de Moran (packages `esda` et `libpysal`, contiguïté de type Queen) sur `part_cadres_2022`, puis sur les écarts restants après comparaison par anneaux (part moins la moyenne simple de son anneau du §5.2, sans fusion). On interprète ce que cela implique pour les intervalles de confiance.

### 5.7 H4 : lycées et autres infrastructures

- La même fonction `accessibilite.indicateurs` est appliquée aux gares (distance à la plus proche), aux installations sportives (Data ES, installations en service de métropole, une par `inst_numero`) et aux équipements culturels (BPE 2025, sous-domaine F3, doublons type × position retirés). Pour le sport et la culture, la mesure est log(1 + nombre à 5 km) : la distance au plus proche ne distingue pas les communes. L'APL (2024, tous âges) est utilisée directement, puisqu'elle est déjà calculée par la DREES. Le lycée privé sous contrat entre par la mesure principale de H1, `dist_lyc_prive_min`.
- Toutes les mesures d'accès sont standardisées (centrées réduites) à l'intérieur de chaque aire, les distances retournées pour qu'une pente positive se lise « plus d'accès, plus de cadres ». On compare leurs associations avec la part de cadres dans les paires contiguës (pente, contrôles et bootstrap du §5.3, mêmes tirages pour toutes les mesures). Pas de comparaison anneau par anneau, abandonnée le 03/11 : les cellules du §5.2 ne sont définies que pour l'exposition 0/1 au lycée privé (6 estimables sur 12), et des anneaux pour des mesures continues seraient une spécification non fixée à l'avance (§5.8).
- **Fig. 7** : un point par infrastructure et par aire avec son intervalle de confiance, triés de la plus forte à la plus faible association moyenne des 3 aires.
- **H4 est descriptive**, comme H2 : aucune règle de verdict n'a été fixée avant l'estimation du 03/11. La Fig. 7 compare les pentes et leurs intervalles, sans test de différence ; le rapport n'affirme pas que l'association est « plus forte avec les lycées qu'avec les autres équipements ».

### 5.8 Règle contre la multiplication des tests

- Seules les spécifications de la section 2.4 constituent les résultats principaux. Tout le reste est présenté comme robustesse ou exploration.
- Si une hypothèse est infirmée, on le dit clairement : on ne cherche pas une autre spécification jusqu'à ce que « ça marche ».
