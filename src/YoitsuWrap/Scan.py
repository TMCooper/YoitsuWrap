import requests
from .Chapter import Chapter
from .Config import Config

class Scan:
    title: str                      # Le nom de l'oeuvre que l'on souhaite traité (ex : Frieren)
    chapters: list[Chapter]         # Liste de tous les chapitre, objets de la class chapter
    link: list[str]                 # Lien direct vers le fichier a télécharger
    path: str                       # Path de rangement du scan (format : nom/chapter n/scan_x.jpg)
    api_link: str                   # Variable de stockage de l'api a requests
    
    def __init__(self, title: str, chapters: list[Chapter], link: list[str], path: str, api_link: str): # Methode de construction pour initialisation des viariable propre a l'objets scan
        """
        Constructeur de la class Scan les argument attendu sont : 
        - title (str) : Nom de l'oeuvre a traté
        - chapters (str) : Chapitre du scan a traté
        - link (str) : Lien resolue vers le fichier actuellement traité 
        - path (str) : Dossier racine ou les scan seront télécharger
        - api_link (str) : Lien de l'api actuellement utiliser pour recuperer les données
        """

        self.chapters = chapters            # Le chapitre poura être égale ou a un chapitre1 ou a all pour tous recuperer
        self.title = title                  # Ne sera pas egale au title mais égale au resultat que l'api retournera après resolution du titre
        self.link = link                    # Fourni dans le fonction de creation et recuperer via l'api"
        self.path = path                    # Configurer grace a la class Config
        self.api_link = api_link            # Configurer via class Config

    @staticmethod
    def search_by_name(manga_name: str, Config: Config):
        """
        Renvoie un objet de la class scan les arguments attendu sont :
        - manga_name (str) : Le nom du manga souhaité ex: Frieren
        - config (Config) : Un objets config configurer au préalable
        """
        api_link = Config.API_LINK
        data = requests.get(f"{api_link}/getSerchAnime?n={manga_name}").json()
        title = data["title"]
        # Crée un objets chapitre pour crée une liste de chapitre ?
        # Crée une boucle de creation pour crée des title file n fois le nombre de page number du chapitre
        objet_scan = Scan(title=title, chapters="valeurnondefiniencore", title_file="pas_encoredef", page_number="pasencoredefini", link="pasencorerecupérer", path=Config.PATH, api_link=api_link)
        pass

    def download_scan(self): # Est du processus de téléchargement de la totalité des scan de l'object scan
        """
        Télécharge le(s) scan(s) disponibles dans l'objets scan lui même
        """
        pass

    def get_chapter(self): # Renvoie le chapitre traiter par l'object scan
        """
        Return le/les chapitre(s) traité par l'objet scan sous forme d'array
        """
        pass

    def get_page_number(self): # Renvoie la page traiter par l'object scan
        """
        Return le(s) nombre de page(s) que l'objet scan traite sous forme d'array
        """
        pass

    def get_link(self): # Renvoie le lien de l'image pret au téléchargement
        """
        Return un array des lien traité par l'api
        """
        pass

    def get_scan_path(self): # Renvoie le path au quel le fichier va ou est enregistré
        """
        Return le path ou les fichier télécharger seront stocker
        """
        pass

    def get_api_link(self): # Renvoie l'api configurer pour la recuperation des scan
        """
        Return le lien vers le quel l'objects scan fait ses requets api
        """
        return self.api_link 