from .Episode import Episode
from .Config import Config
import requests
from concurrent.futures import ThreadPoolExecutor

class Season:
    saison: str                         # Saison traité (ex : saison 1, saison 2, remake2024, etc...)
    title: str                          # Nom de la saison (ex : Frieren, Spice And Wolf, etc...)
    episodes: list[Episode]             # Array des lien d'episode a télécharger
    episodes_numbers: int               # Nombre d'épisode stocker dans l'objet Season
    path: str                           # Path de rangement pour le chapitre (format : nom/chapter n/scan_x.jpg)
    api_link: str                       # Variable de stockage de l'api a requests
    version: str                        # Version de l'animer traté par l'objet season (ex : vostfr, vf)

    def __init__(self, saison, title, episodes, episodes_numbers, path, api_link, version): # Methode de creation de de l'objet complet season
        self.saison = saison
        self.title = title
        self.episodes = episodes
        self.episodes_numbers = episodes_numbers
        self.path = path
        self.api_link = api_link
        self.version = version

    @staticmethod
    def search_by_name(title: str, saison: str, version: str, config: Config) -> 'Season':
        """
        Construction du dict d'objet Season :

        Agrs:
            title (str) : Titre de l'oeuvre (ex : Spice And Wolf)
            saison (str) : La saison que vous souhaité faire (ex : 1, remake2024)
            version (str) : La versions que vous souhaité travailler (ex : vostfr, vf)
            config (Config) : Objet config prealablement crée

        Returns:
            Season or str: Le résultat dépend du succès de la recherche :
            - Si la saison est trouvé : Un objet `Season` configuré.
            - Si la saison n'existe pas : Une chaîne (`str`) contenant le message d'erreur.
        """
        api_link = config.API_LINK
        version = version.lower()

        episodes = []
        try:
            base_data = requests.get(f"{api_link}/getSpecificAnime?q={title}&s={saison}&v={version}").json()
        except requests.exceptions.JSONDecodeError:
            return "Erreur le nom de l'animer choisit ne semble pas être bon"

        if base_data:
            titre = base_data["title"]
            episodes = Episode.search_by_name(title=titre, saison=saison, version=version, config=config)
        objet_season = Season(saison=base_data["Saison"], title=titre, episodes=episodes, episodes_numbers=len(episodes), path=config.PATH, api_link=api_link, version=version)
        return objet_season

    def get_episodes_numbers(self) -> int:
        """
        Renvoie le nombre d'épisode stocker dans l'objet Season :

        Returns:
            self.episodes_numbers
        """
        return self.episodes_numbers

    def get_title(self) -> str: # Renvoie le nom de la saison traité
        """
        Renvoie le titre de l'objet Season :

        Returns:
            self.title
        """
        return self.title

    def download_season(self, max_workers: int = 1) -> int:
        """
        Télécharge toute la saison actuelle :

        Args:
            max_workers (int) : Le nombre d'episode que vous souhaité télécharger en simultané
        
        Returns:
            int (int)
        """

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for episode in self.episodes:
                executor.submit(episode.download_episode)

        return 0

    def get_path(self) -> str:
        """
        Renvoie path configurer pour l'objet Season :

        Returns:
            self.path
        """
        return self.path

    def get_api_link(self) -> str:
        """
        Renvoie api_link configurer pour l'objet Season :

        Returns:
            self.api_link
        """
        return self.api_link

    def get_episodes(self) -> list['Episode']:
        """
        Renvoie l'array d'objet Episode :

        Returns:
            self.episodes
        """
        return self.episodes

    def get_version(self) -> str:
        """
        Renvoie la version de l'objet Season :

        Returns:
            self.version
        """
        return self.version

    def get_saison(self) -> str:
        """
        Renvoie la saison de l'objet Season :

        Returns:
            self.saison
        """
        return self.saison