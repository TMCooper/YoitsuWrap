# TODO Faire un dict ou un array de lien api a request pour voir anime et anime sama
import requests

class Config:
    BASE_URL: list[str]            # La base du lien de l'api a request (ex : http://127.0.0.1)
    PORT: list[int]                # Le port associer a l'api que l'on dois request (ex : 5000)
    PATH: str                      # Dossier racine ou ranger les données télécharger
    API_LINK: list[str]            # Variable non demander a la construction de l'objet mais crée par déduction
    SOURCE: list[str]              # Variable permettant a l'utilisateur de préciser au code quel lien corespond a quel api (ex : [http://127.0.0.1:5000/api/, http://127.0.0.1:5000/api/] alors il peut dire [ANIMESAMA, VOIRANIME])
 
    def __init__(self, BASE_URL: list[str], PORT: list[int], PATH: str, API_LINK: list[str], SOURCE: list[str]): # Méthode de construction pour initialiser les variable de l'objet config
        self.BASE_URL = BASE_URL
        self.PORT = PORT
        self.PATH = PATH
        self.API_LINK = API_LINK
        self.SOURCE = SOURCE

    @staticmethod
    def create_config(urls: list[str], ports: list[int], path: str, sources: list[str]) -> 'Config':
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

        dict_config: {str, Config} = {}
        max_len = max(len(urls), len(ports), len(sources))

        for i in range(max_len):
            url = urls[i] if i < len(urls) else urls[0]
            port = ports[i] if i < len(ports) else ports[0]
            source = sources[i] if i < len(sources) else sources[0]

            API_LINK = f"{url}:{port}/api"

            try:
                status = requests.get(f"{API_LINK}/status", timeout=2)
                if status.status_code == 200:
                    dict_config[source] = Config(BASE_URL=url, PORT=port, PATH=path, API_LINK=API_LINK, SOURCE=source)

            except requests.exceptions.ConnectionError:
                # Si une des api souhaité n'est pas lancer alors on n'execute pas le wrapper
                print(f"Erreur reseau : Impossible de se connecter a l'api {source}")
                exit()

        return dict_config