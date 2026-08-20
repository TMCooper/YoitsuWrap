import requests
from .Config import Config

class Chapter:
    title: str                          # Le nom de l'oeuvre que l'on souhaite traité (ex : Frieren)
    page_link: list[str]                # List lien resolu des pages associer au chapitres
    chapter: str                        # Nom du dossier (ex : chaptire 1, chapitre 2, etc...)
    number_of_pages: int                # Nombre entier de page disponible pour se chapitre
    path: str                           # Path de rangement pour le chapitre (format : nom/chapter n/scan_x.jpg)
    api_link: str                       # Variable de stockage de l'api a requests

    def __init__(self, title: str, page_link: list[str], chapter: str, number_of_pages: int, path: str, api_link: str):
        self.title = title
        self.page_link = page_link
        self.chapter = chapter
        self.number_of_pages = number_of_pages
        self.path = path
        self.api_link = api_link

    @staticmethod
    def get_chapter(manga_title: str, config: Config) -> list['Chapter']:
        """
        Renvoie un objet de la class chapter les arguement attendu sont :
        - manga_title (str) : le titre du manga
        - config (Config) : Un objets config configurer au préalable
        """

        api_link = config.API_LINK

        base_data = requests.get(f"{api_link}/getScanHashmap?n={manga_title}").json()
        data = requests.get(f"{api_link}/getScanLink?n={manga_title}").json()

        title = base_data["title"]
        chapter_list = []

        if data:
            for chapitre, page_link in data.items():
                objet_chapitre = Chapter(title=title, page_link=page_link, chapter=chapitre, number_of_pages=len(page_link), path=config.PATH, api_link=api_link)
                chapter_list.append(objet_chapitre)

        return chapter_list

    def get_number_of_page(self) -> int:
        """
        Renvoie le nombre de page d'un chapitre spécifique arguement attendu : 
        """
        return self.number_of_pages

    def download_chapter(self, chapitre: int):
        """
        Télécharge le chapitre souhaité par l'utilisateur argument attendu : 
        - chapitre (int) : Le chapitre souhaité (ex : 1)
        """
        pass

    def get_page_link(self, chapitre: int) -> list:
        """
        Renvoie la liste des lien téléchargable du chapitre souhaité argument attendu : 
        - chapitre (str) : Le chapitre souhaité (ex : 1)
        """
        pass

    def get_chapter_name(self, chapitre: int) -> str:
        """
        Renvoie le nom au format str du chapitre souhaité (ex : "Chapitre 1") argument attendu :
        - chapitre (str) : Le chapitre souhaité (ex : 1)
        """
        pass

    def get_path(self): # Renvoie la valeur de la variable PATH 
        """
        Return le path configurer pour l'objet chapter
        """
        return self.path

    def get_api_link(self): # Renvoie la valeur de la variable PATH
        """
        Return le lien vers le quel l'objects chapter fait ses requets api
        """
        return self.api_link