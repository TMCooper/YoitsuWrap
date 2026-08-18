class Config:
    BASE_URL: str            # La base du lien de l'api a request (ex : http://127.0.0.1)
    PORT: int                # Le port associer a l'api que l'on dois request (ex : 5000)
    PATH: str                # Dossier racine ou ranger les données télécharger
    API_LINK: str            # Variable non demander a la construction de l'objet mais crée par déduction
 
    def __init__(self, BASE_URL: str, PORT: int, PATH: str): # Méthode de construction pour initialiser les variable de l'objet config
        """
        Constructeur de la class Config les arguments attendu sont : 
        - BASE_URL (str) : la base du lien api a request ex : http://127.0.0.1
        - PORT (int) : Le port associer a l'api ex : 5000
        - PATH (str) : Dossier racine ou seront rangé les données télécharger
        """

        self.BASE_URL = BASE_URL
        self.PORT = PORT
        self.PATH = PATH
        self.API_LINK = f"{BASE_URL}:{PORT}/api"