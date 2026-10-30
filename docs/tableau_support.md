# Tableau de support du choix des aires

Écrit par `pipeline.ecrire_tableau_support()` (PLAN §2.2, §5.2), avant le choix des aires et sans aucune donnée sur les cadres. Les règles de fusion des anneaux et la borne d'équilibre sont celles de l'amendement A6.

## Critères (a) à (d) et frontière (f)

| aire       | ouest   |   part_prive_lycees |   part_prive_candidats |   ecart_ips |   n_ips_public |   n_ips_prive |   population_2022 |   lycees |   lycees_prives | communes_a_moins_de_10km_frontiere   |
|:-----------|:--------|--------------------:|-----------------------:|------------:|---------------:|--------------:|------------------:|---------:|----------------:|:-------------------------------------|
| Bordeaux   | False   |               0.35  |                  0.211 |        15.1 |             26 |            14 |           1412388 |       40 |              14 | —                                    |
| Grenoble   | False   |               0.207 |                  0.135 |        13.8 |             21 |             6 |            724742 |       29 |               6 | —                                    |
| Lille      | False   |               0.442 |                  0.429 |        24   |             29 |            22 |           1528848 |       52 |              23 | 110                                  |
| Lyon       | False   |               0.451 |                  0.28  |        23.7 |             44 |            37 |           2327861 |       82 |              37 | —                                    |
| Nantes     | True    |               0.474 |                  0.367 |        11.8 |             19 |            17 |           1041894 |       38 |              18 | —                                    |
| Rennes     | True    |               0.417 |                  0.311 |        10.1 |             14 |            10 |            780549 |       24 |              10 | —                                    |
| Strasbourg | False   |               0.273 |                  0.155 |        22.8 |             22 |             8 |            868665 |       33 |               9 | 55                                   |
| Toulouse   | False   |               0.268 |                  0.151 |        15.5 |             30 |            11 |           1513396 |       41 |              11 | —                                    |

Critère (f), faisabilité : la part de cadres des arrondissements de Lyon vient du même fichier et avec la même définition que celle des autres communes ; le coût de Lyon est nul pour la variable à expliquer (amendement A11).

## Support de l'exposition (critère e), à 5 et 10 km

| aire       |   rayon_km |   communes |   exposees |   part_exposees |   cellules_estimables |   paires_statut_different |   correlation_non_centree |
|:-----------|-----------:|-----------:|-----------:|----------------:|----------------------:|--------------------------:|--------------------------:|
| Bordeaux   |          5 |        275 |         27 |           0.098 |                     0 |                        70 |                     0.521 |
| Grenoble   |          5 |        204 |         24 |           0.118 |                     0 |                        52 |                     0.666 |
| Lille      |          5 |        201 |         76 |           0.378 |                     0 |                       111 |                     0.261 |
| Lyon       |          5 |        405 |         93 |           0.23  |                     2 |                       169 |                     0.168 |
| Nantes     |          5 |        116 |         19 |           0.164 |                     0 |                        62 |                     0.282 |
| Rennes     |          5 |        183 |         15 |           0.082 |                     0 |                        45 |                     0.507 |
| Strasbourg |          5 |        268 |         11 |           0.041 |                     0 |                        26 |                     0.448 |
| Toulouse   |          5 |        527 |         20 |           0.038 |                     0 |                        43 |                     0.439 |
| Bordeaux   |         10 |        275 |         93 |           0.338 |                     0 |                        96 |                     0.521 |
| Grenoble   |         10 |        204 |         65 |           0.319 |                     0 |                        66 |                     0.666 |
| Lille      |         10 |        201 |        173 |           0.861 |                     0 |                        61 |                     0.261 |
| Lyon       |         10 |        405 |        242 |           0.598 |                     2 |                       203 |                     0.168 |
| Nantes     |         10 |        116 |         64 |           0.552 |                     1 |                        76 |                     0.282 |
| Rennes     |         10 |        183 |         52 |           0.284 |                     1 |                        71 |                     0.507 |
| Strasbourg |         10 |        268 |         53 |           0.198 |                     1 |                        64 |                     0.448 |
| Toulouse   |         10 |        527 |         81 |           0.154 |                     0 |                        83 |                     0.439 |

## Cellules après fusion des anneaux

| aire       |   bas_km |   haut_km |   n_exposees |   n_non_exposees |   dist_moy_exposees |   dist_moy_non_exposees |   ecart_dist_km | estimable   |   rayon_km |
|:-----------|---------:|----------:|-------------:|-----------------:|--------------------:|------------------------:|----------------:|:------------|-----------:|
| Bordeaux   |        0 |       inf |           27 |              248 |               13.53 |                   28.08 |           14.56 | False       |          5 |
| Grenoble   |        0 |       inf |           24 |              180 |               10.72 |                   23.32 |           12.59 | False       |          5 |
| Lille      |        0 |        20 |           60 |               77 |                9.42 |                   14.33 |            4.91 | False       |          5 |
| Lille      |       20 |       inf |           16 |               48 |               29.66 |                   26.74 |            2.92 | False       |          5 |
| Lyon       |        0 |        20 |           52 |               78 |                8.24 |                   15.23 |            7    | False       |          5 |
| Lyon       |       20 |        30 |           20 |              112 |               26.2  |                   24.97 |            1.23 | True        |          5 |
| Lyon       |       30 |       inf |           21 |              122 |               35.08 |                   36.14 |            1.06 | True        |          5 |
| Nantes     |        0 |       inf |           19 |               97 |               14.6  |                   23.46 |            8.85 | False       |          5 |
| Rennes     |        0 |       inf |           15 |              168 |               12.8  |                   23.63 |           10.83 | False       |          5 |
| Strasbourg |        0 |       inf |           11 |              257 |                8.83 |                   24.78 |           15.95 | False       |          5 |
| Toulouse   |        0 |       inf |           20 |              507 |               10.21 |                   32.04 |           21.83 | False       |          5 |
| Bordeaux   |        0 |        20 |           57 |               24 |               12.24 |                   15.8  |            3.56 | False       |         10 |
| Bordeaux   |       20 |       inf |           36 |              158 |               25.24 |                   33.82 |            8.59 | False       |         10 |
| Grenoble   |        0 |        20 |           45 |               35 |                8.37 |                   15.54 |            7.17 | False       |         10 |
| Grenoble   |       20 |       inf |           20 |              104 |               25.62 |                   29.05 |            3.43 | False       |         10 |
| Lille      |        0 |       inf |          173 |               28 |               16.52 |                   20.33 |            3.81 | False       |         10 |
| Lyon       |        0 |        20 |           98 |               32 |               10.82 |                   17.37 |            6.55 | False       |         10 |
| Lyon       |       20 |        30 |           66 |               66 |               25.34 |                   24.98 |            0.37 | True        |         10 |
| Lyon       |       30 |       inf |           78 |               65 |               35.79 |                   36.22 |            0.43 | True        |         10 |
| Nantes     |        0 |        20 |           35 |               15 |               11.48 |                   17.37 |            5.88 | False       |         10 |
| Nantes     |       20 |       inf |           29 |               37 |               28.31 |                   28.9  |            0.59 | True        |         10 |
| Rennes     |        0 |        20 |           35 |               29 |               10.41 |                   16.27 |            5.86 | False       |         10 |
| Rennes     |       20 |       inf |           17 |              102 |               29.52 |                   27.69 |            1.83 | True        |         10 |
| Strasbourg |        0 |        20 |           30 |               55 |                8.63 |                   16.07 |            7.44 | False       |         10 |
| Strasbourg |       20 |       inf |           23 |              160 |               29.62 |                   29.01 |            0.61 | True        |         10 |
| Toulouse   |        0 |       inf |           81 |              446 |               13.98 |                   34.34 |           20.35 | False       |         10 |
