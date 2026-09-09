# YoitsuWrap

> **Wrapper Python pour AnimeSamaApi** — téléchargez des épisodes d'anime et des chapitres de scan en quelques lignes de code.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Version](https://img.shields.io/badge/version-0.1.3-green)]()

---

## Sommaire

- [Présentation](#-présentation)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
  - [Recherche & téléchargement d'un anime](#recherche--téléchargement-dun-anime)
  - [Travailler avec les saisons](#travailler-avec-les-saisons)
  - [Travailler avec les épisodes](#travailler-avec-les-épisodes)
  - [Travailler avec les scans](#travailler-avec-les-scans)
- [Structure du projet](#-structure-du-projet)
- [Référence des classes](#-référence-des-classes)
- [Roadmap](#-roadmap)
- [Licence](#-licence)

---

## Présentation

**YoitsuWrap** est un wrapper Python orienté objet qui simplifie l'interaction avec **AnimeSamaApi**. Il expose une API propre et intuitive pour :

- **Rechercher** un anime par son titre
- **Télécharger** des épisodes (VOSTFR, VF) via `yt-dlp`
- **Télécharger** des chapitres de scan (images)
- **Paralléliser** les téléchargements avec du multithreading

---

## Prérequis

- Python **3.8+**
- Une instance **AnimeSamaApi** lancée et accessible (par défaut sur `http://127.0.0.1:5000`)
- `yt-dlp` installé (géré automatiquement via les dépendances)

---

## Installation

### Via pip (recommandé)

```bash
pip install YoitsuWrap
```

### En mode développement

```bash
git clone https://github.com/TMCooper/YoitsuWrap.git
cd YoitsuWrap
pip install -e .
```

---

## Configuration

Avant toute utilisation, créez un objet `Config` pointant vers votre instance AnimeSamaApi :

```python
from YoitsuWrap.Config import Config

config = Config(
    BASE_URL="http://127.0.0.1",            # URL de l'API
    PORT=5000,                              # Port de l'API
    PATH=r"C:\Users\vous\Téléchargements"   # Dossier de destination
)
```

> **Note :** Si l'API est inaccessible, le programme affichera une erreur et s'arrêtera.

Les fichiers téléchargés seront organisés automatiquement dans le dossier `PATH` selon la structure suivante :

```
PATH/
└── Anime/
    └── <Titre>/
        ├── <Saison>/
        │   └── <Version>/
        │       ├── 1.mp4
        │       ├── 2.mp4
        │       └── ...
        └── Scans/
            └── Chapitre 1/
                ├── page_1.jpg
                ├── page_2.jpg
                └── ...
```

---

## Utilisation

### Recherche & téléchargement d'un anime

```python
from YoitsuWrap.Config import Config
from YoitsuWrap.Anime import Anime

config = Config(BASE_URL="http://127.0.0.1", PORT=5000, PATH=r"C:\Téléchargements")

# Rechercher un anime (version VOSTFR par défaut)
frieren = Anime.search_by_name(title="Frieren", config=config)

# Télécharger tous les épisodes ET les scans disponibles
frieren.download_all()

# Télécharger uniquement les épisodes
frieren.download_anime()

# Télécharger uniquement les épisodes d'une saison précise
frieren.download_anime(season="1")

# Télécharger uniquement les scans
frieren.download_scan()

# Télécharger un chapitre de scan spécifique
frieren.download_scan(chapter=5)
```

### Travailler avec les saisons

```python
from YoitsuWrap.Season import Season

# Récupérer un objet Season directement
saison = Season.search_by_name(
    title="Spice And Wolf",
    saison="remake2024",
    version="vostfr",
    config=config
)

# Télécharger toute la saison (2 épisodes en parallèle)
saison.download_season(max_workers=2)

# Informations
print(saison.get_title())            # "Spice And Wolf"
print(saison.get_saison())           # "remake2024"
print(saison.get_episodes_numbers()) # Nombre d'épisodes
print(saison.get_version())          # "vostfr"
```

### Travailler avec les épisodes

```python
from YoitsuWrap.Episode import Episode

# Récupérer la liste des épisodes d'une saison
episodes = Episode.search_by_name(
    title="Spice And Wolf",
    saison="remake2024",
    version="vostfr",
    config=config
)

# Télécharger le premier épisode
episodes[0].download_episode()

# Informations sur un épisode
print(episodes[0].get_title())          # "Spice And Wolf"
print(episodes[0].get_episode_number()) # 1
print(episodes[0].get_season())         # "remake2024"
print(episodes[0].get_link())           # URL de l'épisode
```

### Travailler avec les scans

```python
from YoitsuWrap.Scan import Scan

# Récupérer un objet Scan
scan = Scan.search_by_name(manga_name="Frieren", config=config)

# Télécharger tous les chapitres (4 images en parallèle, 2 chapitres simultanés)
scan.download_scan(images_workers=4, max_workers=2)

# Télécharger un chapitre spécifique
scan.download_scan(chapter=33, images_workers=4)

# Informations
print(scan.get_number_of_chapters()) # Nombre total de chapitres
print(scan.get_number_of_pages())    # Nombre total de pages
```

---

## Structure du projet

```
YoitsuWrap/
├── src/
│   └── YoitsuWrap/
│       ├── Config.py    # Configuration de la connexion à l'API
│       ├── Anime.py     # Classe principale — point d'entrée recommandé
│       ├── Season.py    # Gestion des saisons d'un anime
│       ├── Episode.py   # Gestion et téléchargement des épisodes
│       ├── Scan.py      # Gestion des scans (manga)
│       └── Chapter.py   # Gestion et téléchargement des chapitres
├── pyproject.toml
└── README.md
```

---

## Référence des classes

### `Config`

| Paramètre  | Type  | Description                             |
|------------|-------|-----------------------------------------|
| `BASE_URL` | `str` | URL de base de l'API (ex: `http://127.0.0.1`) |
| `PORT`     | `int` | Port de l'API (ex: `5000`)              |
| `PATH`     | `str` | Dossier racine pour les téléchargements |

---

### `Anime`

| Méthode | Description |
|---------|-------------|
| `Anime.search_by_name(title, config, version="vostfr")` | Recherche et construit l'objet anime |
| `download_anime(season=None, max_seasons_workers=1, max_workers=2)` | Télécharge les épisodes |
| `download_scan(chapter=None, images_workers=1, max_workers=2)` | Télécharge les scans |
| `download_all(max_seasons_workers=1, max_workers=2, chapter_workers=1)` | Télécharge tout (épisodes + scans) |
| `get_title()` | Retourne le titre |
| `get_cover()` | Retourne l'URL de la couverture |
| `get_link()` | Retourne le lien vers la page source |
| `get_season(season="1")` | Retourne un objet `Season` |
| `get_seasons()` | Retourne toutes les saisons |
| `get_scan()` | Retourne l'objet `Scan` |

---

### `Season`

| Méthode | Description |
|---------|-------------|
| `Season.search_by_name(title, saison, version, config)` | Construit l'objet saison |
| `download_season(max_workers=1)` | Télécharge toute la saison |
| `get_episodes()` | Retourne la liste des objets `Episode` |
| `get_episodes_numbers()` | Retourne le nombre d'épisodes |
| `get_saison()` | Retourne le nom de la saison |
| `get_version()` | Retourne la version (ex: `vostfr`) |

---

### `Episode`

| Méthode | Description |
|---------|-------------|
| `Episode.search_by_name(title, saison, version, config)` | Retourne la liste des épisodes |
| `download_episode()` | Télécharge l'épisode |
| `get_episode_number()` | Retourne le numéro de l'épisode |
| `get_link()` | Retourne l'URL de l'épisode |
| `get_season()` | Retourne la saison associée |
| `get_version()` | Retourne la version |

---

### `Scan`

| Méthode | Description |
|---------|-------------|
| `Scan.search_by_name(manga_name, config)` | Construit l'objet scan |
| `download_scan(chapter=None, images_workers=1, max_workers=1)` | Télécharge le(s) chapitre(s) |
| `get_chapters(chapter=None)` | Retourne un ou tous les chapitres |
| `get_number_of_chapters()` | Retourne le nombre de chapitres |
| `get_number_of_pages()` | Retourne le nombre total de pages |

---

### `Chapter`

| Méthode | Description |
|---------|-------------|
| `Chapter.search_by_name(manga_title, config)` | Retourne un dict de tous les chapitres |
| `download_chapter(max_workers=1)` | Télécharge toutes les pages du chapitre |
| `get_chapter_name()` | Retourne le nom du chapitre (ex: `"Chapitre 1"`) |
| `get_number_of_pages()` | Retourne le nombre de pages |
| `get_page_link()` | Retourne la liste des URLs des pages |


---

## Licence

Ce projet est distribué sous licence **GPL-3.0-or-later**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

<p align="center">Se repo est fait et maintenue par <a href="https://github.com/TMCooper">TMCooper</a></p>
