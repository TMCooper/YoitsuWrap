from .Episode import Episode
from .Config import Config
import requests

class Season:
    saison: str                         # Saison traité (ex : saison 1, saison 2, remake2024, etc...)
    title: str                          # Nom de la saison (ex : Frieren, Spice And Wolf, etc...)
    episodes: list[Episode]             # Array des lien d'episode a télécharger
    episode_number: int                 # Nombre d'épisode stocker dans l'objet Season
    path: str                           # Path de rangement pour le chapitre (format : nom/chapter n/scan_x.jpg)
    api_link: str                       # Variable de stockage de l'api a requests

    def __init__(self, saison, title, episodes, episode_number, path, api_link): # Methode de creation de de l'objet complet season
        self.saison = saison
        self.title = title
        self.episodes = episodes
        self.episode_number = episode_number
        self.path = path
        self.api_link = api_link

    @staticmethod
    def get_season(title: str, saison: str, version: str, config: Config) -> list['Season']:
        """
        Construction du dict d'objet Season arguement attendu :
        - title (str) : Titre de l'oeuvre (ex : Spice And Wolf)
        - saison (str) : La saison que vous souhaité faire (ex : 1, remake2024)
        - version (str) : La versions que vous souhaité travailler (ex : vostfr, vf)
        - config (Config) : Objet config prealablement crée
        """
        api_link = config.API_LINK
        pass

    def get_episode_number(self):
        """
        Renvoie le nombre d'épisode stocker dans l'objet Season
        """
        return len(self.episodes)

    def get_title(self): # Renvoie le nom de la saison traité
        """
        Renvoie le titre de l'objet Season
        """
        return self.title

    def download_season(self): # Télécharge toute la saison actuelle 
        pass

    def get_path(self):
        """
        Renvoie path configurer pour l'objet Season
        """
        pass

    def get_api_link(self):
        """
        Renvoie api_link configurer pour l'objet Season
        """
        pass