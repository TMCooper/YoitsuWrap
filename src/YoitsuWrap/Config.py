# TODO Faire un dict ou un array de lien api a request pour voir anime et anime sama
import requests

class Config:
    BASE_URL: str                  # La base du lien de l'api a request (ex : http://127.0.0.1)
    PORT: int                      # Le port associer a l'api que l'on dois request (ex : 5000)
    PATH: str                      # Dossier racine ou ranger les données télécharger
    API_LINK: str                  # Variable non demander a la construction de l'objet mais crée par déduction
    SOURCE: str                    # Variable permettant a l'utilisateur de préciser au code quel lien corespond a quel api (ex : ANIMESAMA, VOIRANIME)
 
    def __init__(self, BASE_URL: str, PORT: int, PATH: str, API_LINK: str, SOURCE: str): # Méthode de construction pour initialiser les variable de l'objet config
        self.BASE_URL = BASE_URL
        self.PORT = PORT
        self.PATH = PATH
        self.API_LINK = API_LINK
        self.SOURCE = SOURCE

    @staticmethod
    def create_config(urls: list[str] = None, ports: list[int] = None, path: str = "", sources: list[str] = None, **kwargs) -> dict[str, 'Config']:
        """
        Constructeur de la class Config 
                
        Args: 
            urls (list[str]) : la base du lien api a request ex : http://127.0.0.1
            ports (list[int]) : Le port associer a l'api ex : 5000
            path (str) : Dossier racine ou seront rangé les données télécharger
            sources: (list[str]) : Variable permettant a l'utilisateur de préciser au code quel lien corespond a quel api (ex : [{urls}:5000/api/, {urls}:8000/api/] alors ceci est bon : [ANIMESAMA, VOIRANIME])
                
        Returns:
            dict[str, Config] : Un dictionnaire associant chaque nom de source à sa Config
        """

        if urls is None:
            urls = kwargs.get("url", kwargs.get("URL", ["http://127.0.0.1"]))
        if ports is None:
            ports = kwargs.get("port", kwargs.get("PORT", [5000]))
        if not path:
            path = kwargs.get("PATH", kwargs.get("path", "."))
        if sources is None:
            sources = kwargs.get("source", kwargs.get("SOURCE", None))

        if isinstance(urls, str):
            urls = [urls]
        if isinstance(ports, int):
            ports = [ports]
        if isinstance(sources, str):
            sources = [sources]

        if not urls:
            urls = ["http://127.0.0.1"]
        if not ports:
            ports = [5000]

        max_len = max(len(urls), len(ports), len(sources) if sources else 0, 1)

        if not sources:
            default_names = ["ANIMESAMA", "VOIRANIME"]
            sources = [default_names[i] if i < len(default_names) else f"SOURCE_{i+1}" for i in range(max_len)]

        dict_config: dict[str, Config] = {}

        for i in range(max_len):
            url = urls[i] if i < len(urls) else urls[0]
            port = ports[i] if i < len(ports) else ports[0]
            source = sources[i] if i < len(sources) else sources[0]

            API_LINK = f"{url}:{port}/api"

            try:
                status = requests.get(f"{API_LINK}/status", timeout=2)
                if status.status_code == 200:
                    dict_config[source] = Config(BASE_URL=url, PORT=port, PATH=path, API_LINK=API_LINK, SOURCE=source)

            except (requests.exceptions.RequestException, requests.exceptions.ConnectionError):
                print(f"Erreur reseau : Impossible de se connecter a l'api {source} ({API_LINK})")

        return dict_config