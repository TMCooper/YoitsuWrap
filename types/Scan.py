class Scan:
    chapter: str       # Nom du dossier (ex : chaptire 1, chapitre 2, etc...)
    title: str         # Titre du fichier (ex : 1, 2, 3, etc...)
    page_number: int   # Nombre de page associer au chapitre
    link: str          # Lien direct vers le fichier a télécharger
    scan_path: str     # Path de rangement du scan (format : nom/chapter n/scan_x.jpg)

    def __init__(self, chapter, title, page_number, link, scan_path):
        self.chapter = chapter
        self.title = title
        self.page_number = page_number
        self.link = link
        self.scan_path = scan_path

    def construct(self): # Methode de construction de l'object scan
        pass

    def get_chapter(self): # Renvoie le chapitre traiter par l'object scan
        pass

    def get_page_number(self): # Renvoie la page traiter par l'object scan
        pass

    def get_link(self): # Renvoie le lien de l'image pret au téléchargement
        pass

    def get_path_scan(self): # Renvoie le path au quel le fichier va ou est enregistré
        pass