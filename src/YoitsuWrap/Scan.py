import requests
from Config import Config

class Scan:
    title: str               # Le nom de l'oeuvre que l'on souhaite traité (ex : Frieren)
    chapter: list[str]       # Nom du dossier (ex : chaptire 1, chapitre 2, etc...)
    title_file: list[str]    # Titre du fichier (ex : 1, 2, 3, etc...)
    page_number: list[int]         # Nombre de page associer au chapitre
    link: list[str]          # Lien direct vers le fichier a télécharger
    scan_path: str           # Path de rangement du scan (format : nom/chapter n/scan_x.jpg)
    api_link: str            # Variable de stockage de l'api a requests
    
    def __init__(self, chapter, title, scan_path): # Methode de construction de l'object scan
        """
        Constructeur de la class Scan les argument attendu sont : 
        - chapter (str) : Chapitre du scan a traté
        - title (str) : Nom de l'oeuvre a traté
        - scan_path (str) : Dossier racine ou les scan seront télécharger
        """

        self.chapter = chapter # Le chapitre poura être égale ou a un chapotre1 ou a all pour tous recuperer
        self.title = title # Ne sera pas egale au title mais égale au resultat que l'api retournera après resolution du titre
        self.title_file = "Construction manielle via le scan_path"
        self.page_number = 2 # A recuperer via la hashmap de l'api
        self.link = "A recuperer via l'api"
        self.scan_path = scan_path
        self.api_link = f"{Config.BASE_URL}{Config.PORT}/api/"

        return self

    def download_scan(self): # Est du processus de téléchargement de la totalité des scan de l'object scan
        """
        Télécharge le(s) scan(s) disponibles dans l'objets scan lui même
        """


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