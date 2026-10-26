import requests
from .Chapter import Chapter
from .Config import Config
from concurrent.futures import ThreadPoolExecutor

class Scan:
    title: str                      # Le nom de l'oeuvre que l'on souhaite traité (ex : Frieren)
    chapters: dict[int, Chapter]    # Liste de tous les chapitre, objets de la class chapter
    number_of_chapters: int         # Entier indiquant la quantité de chapitre disponible pour se scan
    path: str                       # Path de rangement du scan (format : nom/chapter n/scan_x.jpg)
    api_link: str                   # Variable de stockage de l'api a requests
    
    def __init__(self, title: str, chapters: dict[int, Chapter], number_of_chapters: int, path: str, api_link: str): # Methode de construction pour initialisation des viariable propre a l'objets scan
        self.chapters = chapters                        # Le chapitre poura être égale ou a un chapitre1 ou a all pour tous recuperer
        self.title = title                              # Ne sera pas egale au title mais égale au resultat que l'api retournera après resolution du titre
        self.number_of_chapters = number_of_chapters    # Contien un entier du nombre total de chapitre disponible dans un seul scan
        self.path = path                                # Configurer grace a la class Config
        self.api_link = api_link                        # Configurer via class Config

    @staticmethod
    def search_by_name(manga_name: str, config: Config) -> 'Scan':
        """
        Renvoie un objet de la class Scan :
        
        Args:
            manga_name (str) : Le nom du manga souhaité ex: Frieren
            config (Config) : Un objets config configurer au préalable
        
        Returns:
            Scan (Scan) : Object exploitable scan
        """

        for conf in config.values():
            try:
                data = requests.get(f"{conf.API_LINK}/getScanHashmap?n={manga_name}").json()
            except (requests.exceptions.RequestException, ValueError, KeyError):
                continue

            if data and isinstance(data, dict) and "title" in data and "max_chapter" in data:
                title = data["title"]
                number_of_chapters = data["max_chapter"]

                chapters = Chapter.search_by_name(manga_title=manga_name, config=config)
                objet_scan = Scan(title=title, chapters=chapters, number_of_chapters=number_of_chapters, path=conf.PATH, api_link=conf.API_LINK)
                return objet_scan

        return None # Dans le cas ou notre boucle for n'a pas eux de data on renvoie None 

    def download_scan(self, chapter: int = None, images_workers: int = 1, max_workers: int = 1) -> int: # Est du processus de téléchargement de la totalité des scan de l'object scan
        """
        Télécharge le(s) chapitre(s) disponibles dans l'objets Scan lui même :

        Args:
            chapter (int) : Le chapitre spécifique si il y en a un ex 1 (default = None donc il télécharge tous)        
            images_workers (int) : Le nombre de d'image qu'un chapitre peut télécharger en simutané (default = 1)
            max_workers (int) : Le nombre de chaptire télécharger en simultané (defaul = 1)
        
        Returns:
            int (int)
        """
        if not self.chapters:
            return 0

        if chapter is None:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                for chap in self.chapters.values():
                    if hasattr(chap, "download_chapter"):
                        executor.submit(chap.download_chapter, max_workers=images_workers)
        else:
            chap_obj = self.get_chapters(chapter)
            if chap_obj and hasattr(chap_obj, "download_chapter"):
                chap_obj.download_chapter(max_workers=images_workers)
        return 0

    def get_chapters(self, chapter: int = None):
        """
        Renvoie le(s) chapitre(s) traité par l'objet Scan sous forme de hashmap :

        Args:
            chapter (int) : le nombre du chapitre souhaité ex : 15 (defaut = None donc il vaut tous)
        
        Returns:
            self.chapters[chapter]
        """
        if not self.chapters:
            return {} if chapter is None else None
        if chapter is None:
            return self.chapters
        if chapter in self.chapters:
            return self.chapters[chapter]
        try:
            int_chap = int(chapter)
            if int_chap in self.chapters:
                return self.chapters[int_chap]
        except (ValueError, TypeError):
            pass
        return self.chapters.get(str(chapter))

    def get_number_of_pages(self) -> int:
        """
        Renvoie le nombre de page de tous l'objet Scan :

        Returns:
            number_of_pages (int)
        """
        if not self.chapters:
            return 0
        number_of_pages = 0
        for obj_chap in self.chapters.values():
            if hasattr(obj_chap, "number_of_pages"):
                number_of_pages += obj_chap.number_of_pages
        return number_of_pages

    def get_path(self) -> str: # Renvoie le path sur le quel l'objet scan est configurer
        """
        Renvoie le path sur le quel l'objet scan est configurer

        Returns:
            self.path (str)
        """
        return self.path

    def get_api_link(self) -> str: # Renvoie l'api configurer pour la recuperation des scan
        """
        Renvoie le lien vers le quel l'objects scan fait ses requets api

        Returns:
            self.api_link (str)
        """
        return self.api_link

    def get_number_of_chapters(self) -> int:
        """
        Renvoie le nombre de chapitre total disponible dans l'objet scan

        Returns:
            self.number_of_chapters (int)
        """
        return self.number_of_chapters

    def get_title(self) -> str:
        """
        Renvoie le nom du scan au quel est associer l'objet scan
        
        Returns:
            self.title (str)
        """
        return self.title