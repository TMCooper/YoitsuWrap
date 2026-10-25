# YoitsuWrap

> **Wrapper Python moderne et multi-sources pour AnimeSamaApi & VoirAnime_API** — recherchez et téléchargez des épisodes d'anime et des chapitres de scans manga en quelques lignes de code avec gestion du multithreading et vérification de la santé des flux vidéo.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Version](https://img.shields.io/badge/version-0.1.6-green)](https://github.com/TMCooper/YoitsuWrap)

---

## Sommaire

- [Présentation](#-présentation)
- [Fonctionnalités clés](#-fonctionnalités-clés)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Configuration Multi-Sources](#-configuration-multi-sources)
  - [Structure des dossiers téléchargés](#structure-des-dossiers-téléchargés)
- [Guide d'utilisation](#-guide-dutilisation)
  - [1. Recherche & téléchargement d'un anime complet](#1-recherche--téléchargement-dun-anime-complet)
  - [2. Travailler avec les saisons](#2-travailler-avec-les-saisons)
  - [3. Travailler avec les épisodes](#3-travailler-avec-les-épisodes)
  - [4. Travailler avec les scans](#4-travailler-avec-les-scans)
  - [5. Travailler avec les chapitres](#5-travailler-avec-les-chapitres)
- [Architecture du projet](#-architecture-du-projet)
- [Référence de l'API](#-référence-de-lapi)
  - [`Config`](#config)
  - [`Anime`](#anime)
  - [`Season`](#season)
  - [`Episode`](#episode)
  - [`Scan`](#scan)
  - [`Chapter`](#chapter)
- [Licence](#-licence)

---

## Présentation

**YoitsuWrap** est une bibliothèque Python orientée objet conçue pour interagir simplement avec les APIs d'agrégation d'animes et de mangas (comme **AnimeSamaApi** et **VoirAnime_API**).

Elle prend en charge :
- La recherche unifiée d'œuvres (animes & scans).
- Le support multi-sources avec bascule automatique.
- Le téléchargement haute performance grâce au multithreading (épisodes vidéo, chapitres et pages de scans).

---

## Fonctionnalités clés

- **Multi-APIs & Redondance** : Configurez simultanément plusieurs sources (ex : `ANIMESAMA`, `VOIRANIME`). Si un contenu ou un lien est indisponible sur une API, YoitsuWrap bascule automatiquement sur les sources suivantes.
- **Téléchargement parallèle configurable** : Contrôlez précisément le nombre de threads simultanés pour les saisons, les épisodes, les chapitres de scans et les images individuelles.
- **Organisation automatique** : Classement arborescent standardisé de vos médias par titre, saison, version linguistique (VOSTFR, VF) et chapitres.

---

## Prérequis

- **Python 3.8+**
- Au moins une instance d'API compatible en cours d'exécution (par exemple `AnimeSamaApi` sur le port `5000` et/ou `VoirAnime_API` sur le port `8000`).
- Les dépendances Python listées dans `pyproject.toml` (`requests`, `yt-dlp`).

---

## Installation

### Via pip

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

## Configuration Multi-Sources

Avant de requêter les animes, initialisez votre configuration via la méthode statique `Config.create_config()`. Cette méthode teste la disponibilité des APIs via leur endpoint `/status` et retourne un dictionnaire de configurations valides :

```python
from YoitsuWrap.Config import Config

# Configuration mono ou multi-sources
config = Config.create_config(
    urls=["http://127.0.0.1"],                             # URL(s) de base des APIs
    ports=[5000, 8000],                                    # Ports respectifs des APIs
    path=r"C:\Users\vous\Téléchargements",                 # Dossier racine de destination
    sources=["ANIMESAMA", "VOIRANIME"]                     # Identifiants des sources
)
```

> **Remarque :** Si une source est injoignable lors de l'initialisation, une erreur réseau est signalée et le processus s'arrête par sécurité.

### Structure des dossiers téléchargés

Les fichiers sont automatiquement rangés selon l'arborescence suivante :

```
<PATH>/
└── Anime/
    └── <Titre de l'oeuvre>/
        ├── <Saison>/                  # Ex: 1, 2, remake2024, film, oav...
        │   └── <Version>/             # Ex: vostfr, vf
        │       ├── 1.mp4
        │       ├── 2.mp4
        │       └── ...
        └── Scans/
            ├── Chapitre 1/
            │   ├── page_1.jpg
            │   ├── page_2.jpg
            │   └── ...
            └── Chapitre 2/
                └── ...
```

---

## Guide d'utilisation

### 1. Recherche & téléchargement d'un anime complet

La classe `Anime` est le point d'entrée principal pour manipuler une œuvre (épisodes et scans éventuels) :

```python
from YoitsuWrap.Config import Config
from YoitsuWrap.Anime import Anime

config = Config.create_config(
    urls=["http://127.0.0.1"],
    ports=[5000, 8000],
    path=r"C:\Téléchargements",
    sources=["ANIMESAMA", "VOIRANIME"]
)

# 1. Recherche par titre (version 'vostfr' par défaut, ou 'vf')
frieren = Anime.search_by_name(title="Frieren", config=config, version="vostfr")

# Informations générales
print("Titre :", frieren.get_title())
print("Cover :", frieren.get_cover())
print("Lien source :", frieren.get_link())
print("Nombre total d'épisodes :", frieren.get_episodes_num())

# 2. Téléchargement global (épisodes de toutes les saisons + scans si existants)
frieren.download_all(max_seasons_workers=1, max_workers=2, chapter_workers=2)

# 3. Télécharger uniquement les épisodes vidéo
frieren.download_anime(max_seasons_workers=1, max_workers=4)

# 4. Télécharger une saison précise (ex: saison "1", "oav", "film")
frieren.download_anime(season="1", max_workers=2)

# 5. Télécharger les scans associés
frieren.download_scan(images_workers=4, max_workers=2)

# 6. Télécharger un chapitre spécifique de scan
frieren.download_scan(chapter=33, images_workers=4)
```

---

### 2. Travailler avec les saisons

Vous pouvez inspecter et télécharger directement un objet `Season` :

```python
from YoitsuWrap.Season import Season

# Instanciation ciblée d'une saison
saison = Season.search_by_name(
    title="Spice And Wolf",
    saison="remake2024",
    version="vostfr",
    config=config
)

print(f"{saison.get_title()} - {saison.get_saison()} ({saison.get_version()})")
print("Nombre d'épisodes :", saison.get_episodes_numbers())

# Téléchargement multithreadé de la saison (2 épisodes en parallèle)
saison.download_season(max_workers=2)
```

---

### 3. Travailler avec les épisodes

La classe `Episode` permet de manipuler les épisodes individuellement, d'extraire leurs URLs de streaming ou de tester leur disponibilité :

```python
from YoitsuWrap.Episode import Episode

# Récupérer la liste des épisodes d'une saison
episodes = Episode.search_by_name(
    title="Spice And Wolf",
    saison="remake2024",
    version="vostfr",
    config=config
)

premier_ep = episodes[0]

print("Épisode numéro :", premier_ep.get_episode_number())
print("Lien direct :", premier_ep.get_link())
print("Saison :", premier_ep.get_season())
print("Version :", premier_ep.get_version())
print("Source :", premier_ep.get_source())

# Télécharger l'épisode individuel
premier_ep.download_episode()
```

---

### 4. Travailler avec les scans

La classe `Scan` gère l'ensemble des chapitres d'un manga associé à un titre :

```python
from YoitsuWrap.Scan import Scan

# Recherche des scans d'une œuvre
scan = Scan.search_by_name(manga_name="Frieren", config=config)

if scan:
    print("Manga :", scan.get_title())
    print("Nombre de chapitres :", scan.get_number_of_chapters())
    print("Nombre total de pages :", scan.get_number_of_pages())

    # Télécharger tous les chapitres
    # (max_workers = chapitres en simultané, images_workers = pages par chapitre)
    scan.download_scan(images_workers=4, max_workers=2)

    # Télécharger un chapitre précis
    scan.download_scan(chapter=1, images_workers=4)
```

---

### 5. Travailler avec les chapitres

La classe `Chapter` permet d'accéder au découpage page par page :

```python
from YoitsuWrap.Chapter import Chapter

# Récupérer tous les chapitres sous forme de dictionnaire {numéro_int: Chapter}
chapitres = Chapter.search_by_name(manga_title="Frieren", config=config)

chapitre_1 = chapitres[1]
print("Nom du chapitre :", chapitre_1.get_chapter_name()) # "Chapitre 1"
print("Nombre de pages :", chapitre_1.get_number_of_pages())
print("URLs des pages :", chapitre_1.get_page_link()[:3])  # Les premières URLs

# Télécharger les pages du chapitre (ex: 4 images en simultané)
chapitre_1.download_chapter(max_workers=4)
```

---

## Architecture du projet

```
YoitsuWrap/
├── src/
│   └── YoitsuWrap/
│       ├── __init__.py
│       ├── Config.py      # Gestion des sources API, validation & configuration
│       ├── Anime.py       # Classe centrale regroupant saisons, épisodes et scans
│       ├── Season.py      # Modèle et gestion des saisons d'anime
│       ├── Episode.py     # Gestion d'un épisode, yt-dlp & health check vidéo
│       ├── Scan.py        # Gestion globale des scans d'un manga
│       └── Chapter.py     # Gestion et téléchargement multithreadé des pages
├── pyproject.toml         # Métadonnées, dépendances et configuration du build
├── LICENSE                # Licence GPL-3.0-or-later
└── README.md
```

---

## Référence de l'API

### `Config`

| Méthode / Attribut | Type / Retour | Description |
|-------------------|---------------|-------------|
| `Config.create_config(urls, ports, path, sources)` | `dict[str, Config]` | Teste l'accessibilité de chaque API via `/status` et renvoie la table des configurations |
| `BASE_URL` | `str` | URL de base de l'API (ex: `"http://127.0.0.1"`) |
| `PORT` | `int` | Port associé à l'API (ex: `5000`) |
| `PATH` | `str` | Chemin du dossier racine pour les téléchargements |
| `API_LINK` | `str` | URL complète de l'API déduite (ex: `"http://127.0.0.1:5000/api"`) |
| `SOURCE` | `str` | Nom de la source associée (ex: `"ANIMESAMA"`) |

---

### `Anime`

| Méthode | Paramètres | Retour | Description |
|---------|------------|--------|-------------|
| `search_by_name` | `title: str, config: dict, version: str = "vostfr"` | `Anime \| str` | Recherche l'anime sur les APIs et construit l'objet complet |
| `download_all` | `max_seasons_workers=1, max_workers=2, chapter_workers=1` | `int` | Télécharge l'ensemble des saisons et des scans |
| `download_anime` | `max_seasons_workers=1, max_workers=2, season=None` | `int` | Télécharge tous les épisodes ou ceux d'une saison ciblée |
| `download_scan` | `chapter=None, images_workers=1, max_workers=2` | `int` | Télécharge les scans disponibles |
| `get_title()` | - | `str` | Titre de l'œuvre |
| `get_cover()` | - | `str` | URL de la jaquette |
| `get_link()` | - | `str` | Lien direct vers la page catalogue source |
| `get_episodes_num()` | - | `int` | Nombre total d'épisodes recensés |
| `get_seasons()` | - | `dict[str, Season]` | Dictionnaire de toutes les saisons disponibles |
| `get_season(season="1")` | `season: str` | `Season` | Retourne l'objet `Season` spécifié |
| `get_scan()` | - | `Scan` | Retourne l'objet `Scan` associé (ou `[]` si aucun) |
| `get_path()` | - | `str` | Dossier de destination configuré |
| `get_api_links()` | - | `list[str]` | Liste des liens d'APIs ayant répondu pour cet anime |

---

### `Season`

| Méthode | Paramètres | Retour | Description |
|---------|------------|--------|-------------|
| `search_by_name` | `title: str, saison: str, version: str, config: dict` | `Season \| str` | Construit l'objet d'une saison spécifique |
| `download_season` | `max_workers=1` | `int` | Télécharge tous les épisodes de la saison en parallèle |
| `get_title()` | - | `str` | Titre de l'œuvre |
| `get_saison()` | - | `str` | Nom de la saison (ex: `"1"`, `"remake2024"`) |
| `get_version()` | - | `str` | Version linguistique (ex: `"vostfr"`, `"vf"`) |
| `get_episodes()` | - | `list[Episode]` | Liste des objets `Episode` |
| `get_episodes_numbers()` | - | `int` | Nombre d'épisodes de la saison |
| `get_path()` | - | `str` | Dossier de destination |
| `get_api_link()` | - | `str` | URL de l'API source ayant servi pour la saison |

---

### `Episode`

| Méthode | Paramètres | Retour | Description |
|---------|------------|--------|-------------|
| `search_by_name` | `title: str, saison: str, version: str, config: dict` | `list[Episode] \| str` | Récupère la liste des épisodes avec bascule de source automatique si nécessaire |
| `download_episode` | - | `int` | Télécharge l'épisode via `yt-dlp` au format MP4 |
| `check_vid_health(link)` | `link: str` *(statique)* | `bool` | Vérifie sans télécharger si le lien vidéo est valide et accessible |
| `get_title()` | - | `str` | Titre de l'œuvre |
| `get_episode_number()` | - | `int` | Numéro de l'épisode |
| `get_season()` | - | `str` | Saison de l'épisode |
| `get_version()` | - | `str` | Version linguistique |
| `get_link()` | - | `str` | URL du flux vidéo |
| `get_path()` | - | `str` | Dossier de destination |
| `get_api_link()` | - | `str` | Lien de l'API d'origine |
| `get_source()` | - | `str` | API source qui a été utilisée pour la récupération des données |

---

### `Scan`

| Méthode | Paramètres | Retour | Description |
|---------|------------|--------|-------------|
| `search_by_name` | `manga_name: str, config: dict` | `Scan \| None` | Construit l'objet Scan pour un manga |
| `download_scan` | `chapter=None, images_workers=1, max_workers=1` | `int` | Télécharge tous les chapitres ou un chapitre précis |
| `get_title()` | - | `str` | Titre du manga |
| `get_chapters(chapter=None)` | `chapter: int = None` | `dict[int, Chapter] \| Chapter` | Retourne tous les chapitres ou le chapitre demandé |
| `get_number_of_chapters()` | - | `int` | Nombre total de chapitres |
| `get_number_of_pages()` | - | `int` | Nombre total de pages cumulées |
| `get_path()` | - | `str` | Dossier de destination |
| `get_api_link()` | - | `str` | Lien de l'API utilisée |

---

### `Chapter`

| Méthode | Paramètres | Retour | Description |
|---------|------------|--------|-------------|
| `search_by_name` | `manga_title: str, config: dict` | `dict[int, Chapter]` | Récupère tous les chapitres indexés par numéro entier |
| `download_chapter` | `max_workers=1` | `int` | Télécharge toutes les pages du chapitre dans des fichiers `page_X.jpg` |
| `get_title()` | - | `str` | Titre du manga |
| `get_chapter_name()` | - | `str` | Nom du dossier/chapitre (ex: `"Chapitre 1"`) |
| `get_number_of_pages()` | - | `int` | Nombre de pages dans ce chapitre |
| `get_page_link()` | - | `list[str]` | Liste des URLs des images du chapitre |
| `get_path()` | - | `str` | Dossier de destination |
| `get_api_link()` | - | `str` | Lien de l'API d'origine |

---

## Licence

Ce projet est distribué sous licence **GPL-3.0-or-later**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

<p align="center">Ce dépôt est créé et maintenu par <a href="https://github.com/TMCooper">TMCooper</a></p>
