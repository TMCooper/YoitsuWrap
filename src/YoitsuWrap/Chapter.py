import requests, re, os
from .Config import Config
from concurrent.futures import ThreadPoolExecutor

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
    def get_chapter(manga_title: str, config: Config) -> dict['Chapter']: # Trier les chapitre dans l'ordre
        """
        Renvoie un objet de la class chapter les arguement attendu sont :
        - manga_title (str) : le titre du manga
        - config (Config) : Un objets config configurer au préalable
        """

        api_link = config.API_LINK

        base_data = requests.get(f"{api_link}/getScanHashmap?n={manga_title}").json()
        data = requests.get(f"{api_link}/getScanLink?n={manga_title}").json()

        title = base_data["title"]
        chapter_dict = dict()

        if data:
            for chapitre, page_link in data.items():
                objet_chapitre = Chapter(title=title, page_link=page_link, chapter=chapitre, number_of_pages=len(page_link), path=config.PATH, api_link=api_link)

                # Expression regex pour extraire le chiffre de notre chapitre actuellement traité et le tranformé en int
                match = re.search(r'\d+', chapitre)
                chap_num = int(match.group())

                chapter_dict[chap_num] = objet_chapitre

        return chapter_dict

    def get_number_of_page(self) -> int:
        """
        Renvoie le nombre de page d'un chapitre spécifique arguement attendu : 
        """
        return self.number_of_pages

    def download_chapter(self, max_workers: int = 1) -> int:
        """
        Télécharge le chapitre souhaité par l'utilisateur argument attendu :
        - max_workers (int) : Le nombre d'image que vous souhaité télécharger en simultané
        """
        i = 1

        pre_path = os.path.join(self.path, self.title, self.chapter)
        os.makedirs(pre_path, exist_ok=True)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for lien in self.page_link:
                executor.submit(self.__thread_download, lien, pre_path, i)
                i += 1
        return 0

    def __thread_download(self, lien: str, pre_path: str, i: int) -> int:
        """
        Télécharge les images argument attendu : 
        - lien (str) : le lien de l'image a télécharger
        - pre_path (str) : chemain pefait ou l'image va être enregistrer
        - i (int) : un nombre de votre choix qui nomera votre page au format page_i.jpg
        """
        resolved_path = os.path.join(pre_path, f"page_{i}.jpg")
        image = requests.get(lien)
        with open(resolved_path, "wb") as data:
            data.write(image.content)
        return 0


    def get_page_link(self) -> list:
        """
        Renvoie la liste des lien téléchargable du chapitre souhaité argument attendu : 
        """
        return self.page_link

    def get_chapter_name(self) -> str:
        """
        Renvoie le nom au format str du chapitre souhaité (ex : "Chapitre 1") argument attendu :
        """
        return self.chapter

    def get_path(self) -> str: # Renvoie la valeur de la variable PATH 
        """
        Renvoie le path configurer pour l'objet chapter
        """
        return self.path

    def get_api_link(self) -> str: # Renvoie la valeur de la variable PATH
        """
        Renvoie le lien vers le quel l'objects chapter fait ses requets api
        """
        return self.api_link

    def get_title(self) -> str: # Revoie la valeur de title
        """"
        Renvoie la valeur de la variable titre associer au chapitre
        """
        return self.title