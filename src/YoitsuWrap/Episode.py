from .Config import Config
import requests, re

class Episode:
    title: str                      # Le nom de l'oeuvre que l'on souhaite traité (ex : Frieren)
    link: list                      # Lien direct vers l'episode
    path: str                       # Path ou l'épisode sera ranger
    api_link: str                   # Lien sur le quel l'objet est configurer
    season: str                     # Saison associer a l'épisode
    version: str                    # Version associer a la saison (ex : vostfr)

    def __init__(self, title: str, link: str, path: str, api_link: str, season: str, version: str): # Methode de contruction des variable de base de l'objet Episode
        self.title = title
        self.link = link
        self.path = path
        self.api_link = api_link
        self.season = season
        self.version = version

    @staticmethod
    def get_episode(title:str, saison: str, version: str, config: Config) -> list['Episode']: # Renvoie un dict des bjet episode pret a utilisation
        """
        Construction du dict d'objet Episode arguement attendu :
        - title (str) : Titre de l'oeuvre (ex : Spice And Wolf)
        - saison (str) : La saison que vous souhaité faire (ex : 1, remake2024)
        - version (str) : La versions que vous souhaité travailler (ex : vostfr, vf)
        - config (Config) : Objet config prealablement crée
        """

        api_link = config.API_LINK
        version = version.lower()

        base_data = requests.get(f"{api_link}/getSpecificAnime?q={title}&s={saison}&v={version}").json()
        data = requests.get(f"{api_link}/getAnimeLink?n={title}&s={saison}&v={version}").json()

        objet_episode = []

        if data:
            titre = base_data["title"]
            for donnee in data:
                objet_episode.append(Episode(title=titre, link=donnee["url"], path=config.PATH, api_link=api_link,season=saison, version=version))
            return objet_episode

    def get_title(self) -> str:
        """
        Renvoie le titre de l'oeuvre associer a l'episode
        """
        return self.title

    def get_link(self) -> str: # Renvoie le lien téléchargable de l'épisode
        """
        Renvoie le lien de l'épisode
        """
        return self.link

    def get_path(self) -> str:
        """
        Renvoie le path au quel l'objets Episode est configurer
        """
        return self.path

    def download_episode(self, max_workers: int = 1) -> int:
        """
        Télécharge le(s) épisode(s) associer a l'objet épisode
        """
        pass