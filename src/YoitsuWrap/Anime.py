# TODO Définir tous les type de retour des getters etc
# TODO Faire les getters de chaque variable

from .Scan import Scan
from .Season import Season
from .Config import Config
import requests

class Anime:
    title: str              # Titre de l'oeuvre (ex : Frieren, Spice And Wolf)
    cover: str              # Lien vers l'images de couverture de l'animer
    link: str               # Lien vers l'animer (ex https://anime-sama.to/catalogue/frieren)
    episode_num: int        # Nombre d'épisode dans l'anime # L'api ne renvoie pas d'épisode num pour l'instant
    season: dict[Season]    # Contiendra une hashmap des differente saison de l'animer et le nom de l'id possèdera le nom de la saison (ex : 1, 2, remake2024, etc...)
    scan: Scan              # Objet scan si l'anime choisit en possède un
    path: str               # Path ou l'épisode et les scan seront ranger
    api_link: str           # Variable de stockage de l'api a requests

    def __init__(self, title: str, cover: str, link: str, episode_num: int, season: dict[Season], scan: Scan, path: str, api_link: str): # Methode de construction pour initialisation des viariable propre a l'objet anime
        self.title = title
        self.cover = cover
        self.link = link
        self.episode_num = episode_num
        self.season = season
        self.scan = scan
        self.path = path
        self.api_link = api_link

    @staticmethod
    def search_by_name(title: str, config: Config) -> 'Anime':
        """
        Construction de l'obet Anime arguement attendu : 
        - title (str) : le titre de l'anime de votre choix
        - config (Config) : Objet config préalablement configurer
        """
        api_link = config.API_LINK

        # Data va renvoie un arrays qu'il faudra process pour savoir qui (scan ou season) il faut crée et quel version dans le cas de season
        data = requests.get(f"{api_link}/getInfoAnime?q={title}").json()

        for donnee in data:
            if donnee["Saison"] == "Scans":
                # Creation d'un objet scan et stockage dans la variable scan
                pass
            else:
                # Creation d'un objet Season et rangement dans la variable season
                pass
        pass

    def get_title(self): # Renvoie le nom de l'oeuvre
        pass

    def get_cover(self): # Renvera l'url de la couverture de l'animer
        pass

    def get_link(self): # Renvera le lien direct de l'animer (pas lien de téléchargement)
        pass

    def download_anime(self): # Méthode de téléchargement de l'anime
        pass