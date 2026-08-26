# TODO Définir tous les type de retour des getters etc


from .Scan import Scan
from .Season import Season
from .Config import Config
import requests, re

class Anime:
    title: str              # Titre de l'oeuvre (ex : Frieren, Spice And Wolf)
    cover: str              # Lien vers l'images de couverture de l'animer
    link: str               # Lien vers l'animer (ex https://anime-sama.to/catalogue/frieren)
    episodes_num: int       # Nombre d'épisode dans l'anime # L'api ne renvoie pas d'épisode num pour l'instant
    season: dict[Season]    # Contiendra une hashmap des differente saison de l'animer et le nom de l'id possèdera le nom de la saison (ex : 1, 2, remake2024, etc...)
    scan: Scan              # Objet scan si l'anime choisit en possède un
    path: str               # Path ou l'épisode et les scan seront ranger
    api_link: str           # Variable de stockage de l'api a requests

    def __init__(self, title: str, cover: str, link: str, episodes_num: int, season: dict[Season], scan: Scan, path: str, api_link: str): # Methode de construction pour initialisation des viariable propre a l'objet anime
        self.title = title
        self.cover = cover
        self.link = link
        self.episodes_num = episodes_num
        self.season = season
        self.scan = scan
        self.path = path
        self.api_link = api_link

    @staticmethod
    def search_by_name(title: str, config: Config, version: str = "vostfr") -> dict['Anime']:
        """
        Construction de l'obet Anime arguement attendu : 
        - title (str) : le titre de l'anime de votre choix
        - config (Config) : Objet config préalablement configurer
        - version (str) : La version souhaité ex : vf, vostfr (par défaut = vostfr)
        """
        api_link = config.API_LINK
        version = version.lower()

        # Data va renvoie un arrays qu'il faudra process pour savoir qui (scan ou season) il faut crée et quel version dans le cas de season
        data = requests.get(f"{api_link}/getInfoAnime?q={title}").json()

        dict_season: dict[int, Season] = {} # Définition spécifique pour disposer de l'autocompletion
        scans = []

        for donnee in data:
            if donnee["Saison"] == "Scans":
                scans = Scan.search_by_name(manga_name=donnee["title"], config=config)
            else:
                match = re.search(r'\d+', donnee["Saison"])
                season_num = int(match.group())

                dict_season[season_num] = Season.search_by_name(title=donnee["title"], saison=donnee["Saison"], config=config, version=version)

        for season in dict_season.values():
            episodes_num = season.get_episodes_numbers()

        objet_anime = Anime(title=donnee["title"], cover=data[0]["cover"], link=data[0]["base_url"], episodes_num=episodes_num, season=dict_season, scan=scans, path=config.PATH, api_link=config.API_LINK)

        return objet_anime

    def get_title(self): # Renvoie le nom de l'oeuvre
        pass

    def get_cover(self): # Renvera l'url de la couverture de l'animer
        pass

    def get_link(self): # Renvera le lien direct de l'animer (pas lien de téléchargement)
        pass

    def download_anime(self): # Méthode de téléchargement de l'anime
        pass

    def get_episodes_num(self):
        """
        Renvoie le nombre total d'épisode de l'anime
        """
        pass

    def get_seasons(self):
        """
        Renvoie les objets season
        """
        pass

    def get_season(self):
        """
        Renvoie l'objet d'une saison spécifique
        """
        pass

    def get_scan(self):
        """
        Renvoie l'objet scan
        """
        pass

    def get_path(self):
        """
        Renvoie le path sur le quel l'objet anime est configurer
        """
        pass

    def get_api_link(self):
        """
        Renvoie api_link sur le quel l'objet anime est configurer
        """
        pass