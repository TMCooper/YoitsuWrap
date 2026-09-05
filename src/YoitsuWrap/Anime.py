# TODO Définir tous les type de retour des getters etc

from .Scan import Scan
from .Season import Season
from .Config import Config
import requests, re
from concurrent.futures import ThreadPoolExecutor

class Anime:
    title: str              # Titre de l'oeuvre (ex : Frieren, Spice And Wolf)
    cover: str              # Lien vers l'images de couverture de l'animer
    link: str               # Lien vers l'animer (ex https://anime-sama.to/catalogue/frieren)
    episodes_num: int       # Nombre d'épisode dans l'anime # L'api ne renvoie pas d'épisode num pour l'instant
    seasons: dict[Season]   # Contiendra une hashmap des differente saison de l'animer et le nom de l'id possèdera le nom de la saison (ex : 1, 2, remake2024, etc...)
    scan: Scan              # Objet scan si l'anime choisit en possède un
    path: str               # Path ou l'épisode et les scan seront ranger
    api_link: str           # Variable de stockage de l'api a requests

    def __init__(self, title: str, cover: str, link: str, episodes_num: int, seasons: dict[Season], scan: Scan, path: str, api_link: str): # Methode de construction pour initialisation des viariable propre a l'objet anime
        self.title = title
        self.cover = cover
        self.link = link
        self.episodes_num = episodes_num
        self.seasons = seasons
        self.scan = scan
        self.path = path
        self.api_link = api_link

    @staticmethod
    def search_by_name(title: str, config: Config, version: str = "vostfr") -> 'Anime':
        """
        Recherche un anime par son titre et construit l'objet correspondant :
        
        Args:
            title (str) : le titre de l'anime de votre choix
            config (Config) : Objet config préalablement configurer
            version (str) : La version souhaité ex : vf, vostfr (par défaut = vostfr)

        Returns:
            Anime or str: Le résultat dépend du succès de la recherche :
            - Si l'anime est trouvé : Un objet `Anime` configuré.
            - Si l'anime n'existe pas : Une chaîne (`str`) contenant le message d'erreur.
        """
        api_link = config.API_LINK
        version = version.lower()

        # Data va renvoie un arrays qu'il faudra process pour savoir qui (scan ou season) il faut crée et quel version dans le cas de season
        try:
            data = requests.get(f"{api_link}/getInfoAnime?q={title}").json()
        except requests.exceptions.JSONDecodeError:
            return "Erreur le nom de l'animer choisit ne semble pas être bon"

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

        objet_anime = Anime(title=donnee["title"], cover=data[0]["cover"], link=data[0]["base_url"], episodes_num=episodes_num, seasons=dict_season, scan=scans, path=config.PATH, api_link=config.API_LINK)

        return objet_anime

    def get_title(self) -> str: # Renvoie le nom de l'oeuvre
        """
        Renvoie le titre de l'oeuvre que l'objet Anime contient :

        Returns:
            self.title (str)
        """
        return self.title

    def get_cover(self) -> str: # Renvera l'url de la couverture de l'animer
        """
        Renvoie la cover de l'objet Anime :

        Returns:
            self.cover (str)
        """
        return self.cover

    def get_link(self) -> str: # Renvera le lien direct de l'animer (pas lien de téléchargement)
        """
        Renvoie le lien direct vers le site source (ex ; https://anime-sama.to/catalogue/frieren)
        
        Returns:
            self.link (str)
        """
        return self.link

    def download_anime(self, max_seasons_workers: int = 1, max_workers:int = 2) -> int: # Méthode de téléchargement de l'anime
        """
        Télécharge l'anime associer a l'objet Anime
        
        Args:
            max_seasons_workers (int) : Nombre de saison a télécharger en même temps (ex : 1, 2) defaut = 1
            max_workers (int) : Nombre d'épisode a télécharger en même temps (ex : 1, 2) defaut = 4

        Returns:
            int (int)
        """
        with ThreadPoolExecutor(max_workers=max_seasons_workers) as executor:
            for episode in self.seasons.values():
                executor.submit(episode.download_season, max_workers=max_workers)

        return 0

    def get_episodes_num(self) -> int:
        """
        Renvoie le nombre total d'épisode de l'anime :

        Returns:
            self.episodes_num (int)
        """
        return self.episodes_num

    def get_seasons(self) -> dict['Season']:
        """
        Renvoie les objets seasons :

        Returns:
            self.seasons (dict[Season])
        """
        return self.seasons

    def get_season(self, season:int = 1) -> 'Season':
        """
        Renvoie l'objet d'une saison spécifique :

        Args:
            season (str) : saison souhaité ex 1, 2 / défaut = 1

        Returns:
            Season (Season) : Objet Season souhaité
        """
        return self.seasons[season]

    def get_scan(self) -> 'Scan':
        """
        Renvoie l'objet scan :

        Returns:
            self.scan (Scan)
        """
        return self.scan

    def get_path(self) -> str:
        """
        Renvoie le path sur le quel l'objet anime est configurer :

        Returns:
            self.path (str)
        """
        return self.path

    def get_api_link(self) -> str:
        """
        Renvoie api_link sur le quel l'objet anime est configurer :

        Returns:
            self.api_link (str)
        """
        return self.api_link