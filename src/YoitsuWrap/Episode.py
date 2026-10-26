from .Config import Config
import requests, os, yt_dlp

class Episode:
    title: str                      # Le nom de l'oeuvre que l'on souhaite traité (ex : Frieren)
    link: str                       # Lien direct vers l'episode
    path: str                       # Path ou l'épisode sera ranger
    api_link: str                   # Lien sur le quel l'objet est configurer
    season: str                     # Saison associer a l'épisode
    version: str                    # Version associer a la saison (ex : vostfr)
    episode_number: int             # Numero de l'épisode contenue dans l'objet
    source: str                     # Permet de savoir d'ou provient le lien de l'épisode 

    def __init__(self, title: str, link: str, path: str, api_link: str, season: str, version: str, episode_number: int, source: str): # Methode de contruction des variable de base de l'objet Episode
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
            list[Episode] : Liste des objets Episode configurés.
        """

        version = version.lower()
        objet_episode = []
        mauvais_episode = set()

        for conf in config.values():
            try:
                base_data_res = requests.get(f"{conf.API_LINK}/getSpecificAnime?q={title}&s={saison}&v={version}")
                base_data = base_data_res.json()
            except (requests.exceptions.RequestException, ValueError, KeyError):
                continue

            try:
                data_res = requests.get(f"{conf.API_LINK}/getAnimeLink?n={title}&s={saison}&v={version}")
                data = data_res.json()
            except (requests.exceptions.RequestException, ValueError, KeyError):
                continue

            if not data or not isinstance(data, list):
                continue

            titre = base_data.get("title", title) if isinstance(base_data, dict) else title
            saison_val = base_data.get("Saison", saison) if isinstance(base_data, dict) else saison

            if not mauvais_episode and not objet_episode: # Première source valide
                for i, donnee in enumerate(data, start=1):
                    ep_num = donnee.get("episode", i)
                    url = donnee.get("url")
                    if url and Episode.check_vid_health(link=url):
                        objet_episode.append(Episode(title=titre, link=url, path=conf.PATH, api_link=conf.API_LINK, season=saison_val, version=version, episode_number=ep_num, source=conf.SOURCE))
                    else:
                        mauvais_episode.add(ep_num)

                if not mauvais_episode: # Tout est bon dès la première source
                    break

            else: # Sources suivantes pour remplacer les mauvais épisodes
                for i, donnee in enumerate(data, start=1):
                    ep_num = donnee.get("episode", i)
                    if ep_num in mauvais_episode:
                        url = donnee.get("url")
                        if url and Episode.check_vid_health(link=url):
                            objet_episode.append(Episode(title=titre, link=url, path=conf.PATH, api_link=conf.API_LINK, season=saison_val, version=version, episode_number=ep_num, source=conf.SOURCE))
                            mauvais_episode.discard(ep_num)

                if not mauvais_episode:
                    break

        objet_episode.sort(key=lambda ep: ep.episode_number)
        return objet_episode

    def get_title(self) -> str:
        """
        Renvoie le titre de l'oeuvre associer a l'episode :

        Returns:
            self.title (str)
        """
        return self.title

    def get_link(self) -> str: # Renvoie le lien téléchargable de l'épisode
        """
        Renvoie le lien de l'épisode :

        Returns:
            self.link (str)
        """
        return self.link

    def get_path(self) -> str:
        """
        Renvoie le path au quel l'objets Episode est configurer :

        Returns:
            self.path (str)
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
            "http_headers": Episode.__get_headers("any"),           # "Any" est simplement la pour donner un argument a la fonction de sorte a se quel puisse fonctionner
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
        os.makedirs(pre_path, exist_ok=True)

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

        return 0

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
            self.api_link (str)
        """
        return self.api_link

    def get_season(self) -> str:
        """
        Renvoie la saison au quel l'objet episode appartient ex : Saison 1, remake2024, Saison 2, etc :

        Returns:
            self.season (str)
        """
        return self.season

    def get_version(self) -> str:
        """
        Renvoie la version au quel l'épisode appartient ex : vostfr, vf :

        Returns:
            self.version (str)
        """
        return self.version

    def get_episode_number(self) -> int:
        """
        Renvoie le numero de l'épisode ex : 1, 2, 3 etc :

        Returns:
            self.episode_number (int)
        """
        return self.episode_number

    def get_source(self) -> str:
        """
        Renvoie de quel api l'épisode a été pris (ex : ANIMESAMA)
        
        Returns:
            self.source (str)
        """
        return self.source