import requests
from .Chapter import Chapter
from .Config import Config

class Scan:
    title: str                      # Le nom de l'oeuvre que l'on souhaite traité (ex : Frieren)
    chapters: list[Chapter]         # Liste de tous les chapitre, objets de la class chapter
    number_of_chapter: int          # Entier indiquant la quantité de chapitre disponible pour se scan
    path: str                       # Path de rangement du scan (format : nom/chapter n/scan_x.jpg)
    api_link: str                   # Variable de stockage de l'api a requests
    
    def __init__(self, title: str, chapters: list[Chapter], number_of_chapter: int, path: str, api_link: str): # Methode de construction pour initialisation des viariable propre a l'objets scan
        """
        Constructeur de la class Scan les argument attendu sont : 
        - title (str) : Nom de l'oeuvre a traté
        - chapters (str) : Chapitre du scan a traté
        - path (str) : Dossier racine ou les scan seront télécharger
        - api_link (str) : Lien de l'api actuellement utiliser pour recuperer les données
        """

        self.chapters = chapters                    # Le chapitre poura être égale ou a un chapitre1 ou a all pour tous recuperer
        self.title = title                          # Ne sera pas egale au title mais égale au resultat que l'api retournera après resolution du titre
        self.number_of_chapter = number_of_chapter  # Contien un entier du nombre total de chapitre disponible dans un seul scan
        self.path = path                            # Configurer grace a la class Config
        self.api_link = api_link                    # Configurer via class Config

    @staticmethod
    def search_by_name(manga_name: str, config: Config) -> 'Scan':
        """
        Renvoie un objet de la class scan les arguments attendu sont :
        - manga_name (str) : Le nom du manga souhaité ex: Frieren
        - config (Config) : Un objets config configurer au préalable
        """

        api_link = config.API_LINK

        data = requests.get(f"{api_link}/getScanHashmap?n={manga_name}").json()
        title = data["title"]
        number_of_chapter = data["max_chapter"]

        chapters = Chapter.get_chapter(manga_title=manga_name, config=config)
        objet_scan = Scan(title=title, chapters=chapters, number_of_chapter=number_of_chapter, path=config.PATH, api_link=api_link)
        return objet_scan

    def download_scan(self): # Est du processus de téléchargement de la totalité des scan de l'object scan
        """
        Télécharge le(s) scan(s) disponibles dans l'objets scan lui même
        """
        pass

    def get_chapter(self) -> list[Chapter]: # Renvoie les chapitres traiter par l'object scan
        """
        Return les chapitres traité par l'objet scan sous forme d'array
        """
        pass

    def get_number_of_page(self, chapitre: int) -> int:
        """
        Renvoie le nombre de page d'un chapitre spécifique arguement attendu : 
        - chapitre (int) : Le chapitre souhaité (ex : 1)        
        """
        for obj_chap in self.chapters:
            if f"Chapitre {chapitre}" == obj_chap.chapter:
                return obj_chap.number_of_pages
        return None

    def get_path(self): # Renvoie le path au quel le fichier va ou est enregistré
        """
        Return le path ou les fichier télécharger seront stocker
        """
        pass

    def get_api_link(self): # Renvoie l'api configurer pour la recuperation des scan
        """
        Return le lien vers le quel l'objects scan fait ses requets api
        """
        return self.api_link