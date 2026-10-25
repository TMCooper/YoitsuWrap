from .Config import Config
import requests, os, yt_dlp

class Episode:
    title: str                      # Le nom de l'oeuvre que l'on souhaite traité (ex : Frieren)
    link: list                      # Lien direct vers l'episode
    path: str                       # Path ou l'épisode sera ranger
    api_link: str                   # Lien sur le quel l'objet est configurer
    season: str                     # Saison associer a l'épisode
    version: str                    # Version associer a la saison (ex : vostfr)
    episode_number: int             # Numero de l'épisode contenue dans l'objet
    source: Config                  # Permet de savoir d'ou provient le lien de l'épisode 

    def __init__(self, title: str, link: str, path: str, api_link: str, season: str, version: str, episode_number: int, source: Config): # Methode de contruction des variable de base de l'objet Episode
        self.title = title
        self.link = link
        self.path = path
        self.api_link = api_link
        self.season = season
        self.version = version
        self.episode_number = episode_number
        self.source = source

    @staticmethod
    def search_by_name(title:str, saison: str, version: str, config: Config) -> list['Episode']: # Renvoie un dict des bjet episode pret a utilisation
        """
        Construction du dict d'objet Episode :

        Args:
            title (str) : Titre de l'oeuvre (ex : Spice And Wolf)
            saison (str) : La saison que vous souhaité faire (ex : 1, remake2024)
            version (str) : La versions que vous souhaité travailler (ex : vostfr, vf)
            config (Config) : Objet config prealablement crée

        Returns:
            Episode or str: Le résultat dépend du succès de la recherche :
            - Si l'episode est trouvé : Un objet `Episode` configuré.
            - Si l'episode n'existe pas : Une chaîne (`str`) contenant le message d'erreur.
        """

        # api_link = config.API_LINK
        version = version.lower()

        objet_episode = []
        mauvais_episode = []

        for conf in config.values():
            try:
                base_data = requests.get(f"{conf.API_LINK}/getSpecificAnime?q={title}&s={saison}&v={version}").json()
            except requests.exceptions.JSONDecodeError:
                return "Erreur le nom de l'animer choisit ne semble pas être bon"

            data = requests.get(f"{conf.API_LINK}/getAnimeLink?n={title}&s={saison}&v={version}").json()
            i = 1

            if data:
                titre = base_data["title"]
                if not mauvais_episode: # Alors on itère sur la première source
                    for donnee in data:
                        if Episode.check_vid_health(link=donnee["url"]) == True:
                            objet_episode.append(Episode(title=titre, link=donnee["url"], path=conf.PATH, api_link=conf.API_LINK, season=base_data["Saison"], version=version, episode_number=i, source=conf.SOURCE))
                        else:
                            mauvais_episode.append(i)
                        i += 1

                    if len(objet_episode) == len(data): # Fonctionelle
                        break

                else: # On itère sur la seconde source si des mauvais épisode on été trouvée
                    for donnee in data:
                        if donnee["episode"] in mauvais_episode:
                            if Episode.check_vid_health(link=donnee["url"]) == True:
                                objet_episode.append(Episode(title=titre, link=donnee["url"], path=conf.PATH, api_link=conf.API_LINK, season=base_data["Saison"], version=version, episode_number=donnee["episode"], source=conf.SOURCE))
                        else:
                            pass

        return objet_episode

    def get_title(self) -> str:
        """
        Renvoie le titre de l'oeuvre associer a l'episode :

        Returns:
            self.title
        """
        return self.title

    def get_link(self) -> str: # Renvoie le lien téléchargable de l'épisode
        """
        Renvoie le lien de l'épisode :

        Returns:
            self.link
        """
        return self.link

    def get_path(self) -> str:
        """
        Renvoie le path au quel l'objets Episode est configurer :

        Returns:
            self.path
        """
        return self.path

    @staticmethod
    def check_vid_health(link) -> bool:
        """
        Vérifie si une vidéo est accessible et téléchargeable via yt-dlp.
        
        Returns:
            True si c'est bon
            False sinon
        """
        class Silent_Log(object):
            def debug(self, msg):
                pass

            def warning(self, msg):
                pass

            def error(self, msg):
                pass

        ydl_opts = {
            "noplaylist": True,
            "quiet": True,
            "logger": Silent_Log(), 
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(link, download=False)
            return True
        except Exception as e:
            # print(f"[DEBUG] Erreur : {type(e).__name__} - {e}")
            return False

    def download_episode(self) -> int:
        """
        Télécharge l'épisodes associer a l'objet épisode :

        Returns:
            int (int)
        """
        pre_path = os.path.join(self.path, "Anime", self.title, self.season, self.version)

        ydl_opts = {
            "format": "best",                                                                                     # Qualité vidéo maximale
            "outtmpl": os.path.join(pre_path, f"{self.episode_number}.mp4"),                                      # Nom du fichier de sortie
            "quiet": False,                                                                                       # N'affiche pas les logs
            "no_warning": True,                                                                                   # Supprime les warnings
            # "logger": cleanLogger,                                                                                # Logger personalisé
            # "progress_hooks": [cleanLogger.hook],                                                                 # Pour un affichage personnalisé de la progression
            "http_headers": self.__get_headers(),                                                                 # Header pour effectuer la requets
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.link])

    def __get_headers(self) -> dict:
        headers = {
                'authority': 'p16-ad-sg.tiktokcdn.com',
                'method': 'GET',
                'path': '/obj/ad-site-i18n-sg/202508125d0d6bceedbe1123419c9459',
                'scheme': 'https',
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br, zstd',
                'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,de;q=0.5,zh-CN;q=0.4,zh;q=0.3,ru;q=0.2,es;q=0.1,ko;q=0.1,vi;q=0.1,pl;q=0.1',
                'cache-control': 'no-cache',
                'origin': 'https://smoothpre.com',
                'pragma': 'no-cache',
                'priority': 'u=1, i',
                'referer': 'https://smoothpre.com/',
                'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Opera GX";v="122"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'cross-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0',
                }

        return headers

    def get_api_link(self) -> str:
        """
        Renvoie l'api configurer pour l'objet episode :

        Returns:
            self.api_link
        """
        return self.api_link

    def get_season(self) -> str:
        """
        Renvoie la saison au quel l'objet episode appartient ex : Saison 1, remake2024, Saison 2, etc :

        Returns:
            self.season
        """
        return self.season

    def get_version(self) -> str:
        """
        Renvoie la version au quel l'épisode appartient ex : vostfr, vf :

        Returns:
            self.version
        """
        return self.version

    def get_episode_number(self) -> int:
        """
        Renvoie le numero de l'épisode ex : 1, 2, 3 etc :

        Returns:
            self.episode_number
        """
        return self.episode_number