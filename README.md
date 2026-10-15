# Lycées et géographie des cadres dans trois aires urbaines de province

Projet du cours « Python pour la data science » (ENSAE), rendu le 24 novembre 2026.

## Question

Dans des aires urbaines de province aux traditions scolaires contrastées, les communes offrant un meilleur accès à des lycées privés ou à forte valeur ajoutée concentrent-elles davantage de cadres que leurs voisines, et ce lien résiste-t-il face aux autres infrastructures ?

## Reproduire le projet

Python 3.13 et [uv](https://docs.astral.sh/uv/) sont nécessaires.

```bash
uv sync --locked                 # installe exactement les dépendances figées dans uv.lock
uv run pre-commit install        # active nb-clean et ruff avant chaque commit
uv run pytest                    # lance les tests
```

Le rapport est `rapport.ipynb` : texte, figures et tableaux, recalculés à chaque exécution depuis les données brutes. Le site se construit avec [Quarto](https://quarto.org/), déjà installé sur le SSPCloud :

```bash
uv run quarto render             # exécute rapport.ipynb et écrit le site dans _site/
```

`uv run` est nécessaire : il donne à Quarto le Python de l'environnement du projet, où `cadres_lycees` est installé.

Sur un compte neuf, les données sont téléchargées depuis les copies gelées publiques décrites ci-dessous, puis gardées dans `data/`. Depuis un clone neuf, sans identifiants S3, le notebook s'exécute de bout en bout en environ 16 minutes, téléchargements compris (mesuré le 04/11/2026 sur un clone neuf de la branche `main` de la fork, dans un dossier vide, sans `data/` ni `BUCKET_S3` : les 28 fichiers bruts ont été lus sur la release et leur `sha256` contrôlé). Pour l'exécuter sans construire le site :

```bash
uv run jupyter nbconvert --to notebook --execute rapport.ipynb --output rapport_execute.ipynb
```
