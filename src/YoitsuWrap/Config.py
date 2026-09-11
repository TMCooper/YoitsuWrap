import requests

class Config:
    BASE_URL: str            # La base du lien de l'api a request (ex : http://127.0.0.1)
    PORT: int                # Le port associer a l'api que l'on dois request (ex : 5000)
    PATH: str                # Dossier racine ou ranger les données télécharger
    API_LINK: str            # Variable non demander a la construction de l'objet mais crée par déduction
 
    def __init__(self, BASE_URL: str, PORT: int, PATH: str, API_LINK: str): # Méthode de construction pour initialiser les variable de l'objet config
        self.BASE_URL = BASE_URL
        self.PORT = PORT
        self.PATH = PATH
        self.API_LINK = API_LINK


    def create_config(url: str, port: int, path: str) -> 'Config':
        """
        Constructeur de la class Config 
                
        Args: 
            BASE_URL (str) : la base du lien api a request ex : http://127.0.0.1
            PORT (int) : Le port associer a l'api ex : 5000
            PATH (str) : Dossier racine ou seront rangé les données télécharger
                
        Returns:
            config (config)
        """

        API_LINK = f"{url}:{port}/api"

        try:
            status = requests.get(f"{API_LINK}/status")
            if status:
                return Config(BASE_URL=url, PORT=port, PATH=path)
        except requests.exceptions.ConnectionError:
            print("Erreur reseau : Impossible de se connecter a l'api")
            exit()