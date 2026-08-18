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
    def get_chapter(manga_title: str, Config: Config) -> list[Chapter]:
        api_link = Config.API_LINK
        data = requests.get(f"{api_link}/getScanLink?n={manga_title}").json()
        chapter_list = []
        if data:
            for chapitre, lien in data.items():
                objet_chapitre = Chapter()
                chapter_list.append(objet_chapitre)
            return chapter_list