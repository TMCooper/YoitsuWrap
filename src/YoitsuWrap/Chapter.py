class Chapter:
    title: str                          # Le nom de l'oeuvre que l'on souhaite traité (ex : Frieren)
    chapter: str                        # Nom du dossier (ex : chaptire 1, chapitre 2, etc...)
    number_of_pages: int                # Nombre entier de page disponible pour se chapitre
    path: str                           # Path de rangement pour le chapitre (format : nom/chapter n/scan_x.jpg)
    api_link: str                       # Variable de stockage de l'api a requests

    def __init__(self, title: str, chapter: str, number_of_pages: int, path: str, api_link: str):
        self.title = title
        self.chapter = chapter
        self.number_of_pages = number_of_pages
        self.path = path
        self.api_link = api_link