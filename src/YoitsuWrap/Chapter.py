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
    def search_by_name(manga_title: str, config: Config) -> dict['Chapter']: # Trier les chapitre dans l'ordre
        """
        Renvoie un objet de la class Chapter :
        
        Args:
            manga_title (str) : le titre du manga
            config (Config) : Un objets config configurer au préalable

        Returns:
            dict['Chapter'] : Dict de l'object Chapter
        """

        base_data = None
        data = None
        api_link = ""
        path = ""

        for conf in config.values():
            try:
                base_data_res = requests.get(f"{conf.API_LINK}/getScanHashmap?n={manga_title}")
                data_res = requests.get(f"{conf.API_LINK}/getScanLink?n={manga_title}")
                base_data = base_data_res.json()
                data = data_res.json()
            except (requests.exceptions.RequestException, ValueError, KeyError):
                continue
            
            if base_data and data and isinstance(base_data, dict) and isinstance(data, dict):
                api_link = conf.API_LINK
                path = conf.PATH
                break

        chapter_dict = dict()

        if data and isinstance(data, dict) and base_data and isinstance(base_data, dict):
            title = base_data.get("title", manga_title)
            for chapitre, page_link in data.items():
                objet_chapitre = Chapter(title=title, page_link=page_link, chapter=chapitre, number_of_pages=len(page_link), path=path, api_link=api_link)

                # Expression regex pour extraire le chiffre de notre chapitre actuellement traité
                match = re.search(r'\d+(?:\.\d+)?', str(chapitre))
                if match:
                    val = match.group()
                    chap_num = float(val) if '.' in val else int(val)
                else:
                    chap_num = chapitre

                chapter_dict[chap_num] = objet_chapitre

        return chapter_dict

    def get_number_of_pages(self) -> int:
        """
        Renvoie le nombre de page d'un chapitre spécifique arguement attendu : 

        Returns:
            self.number_of_pages
        """
        return self.number_of_pages

    def download_chapter(self, max_workers: int = 1) -> int:
        """
        Télécharge le chapitre dans l'objet Chapter :

        Args:
            max_workers (int) : Le nombre d'image que vous souhaité télécharger en simultané

        Returns:
            int (int)
        """
        pre_path = os.path.join(self.path, "Anime", self.title, "Scans", self.chapter)
        os.makedirs(pre_path, exist_ok=True)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for i, lien in enumerate(self.page_link, start=1):
                executor.submit(self.__thread_download, lien=lien, pre_path=pre_path, i=i)
        return 0

    def __thread_download(self, lien: str, pre_path: str, i: int) -> int:
        """
        Télécharge les images argument attendu :

        Args:
            lien (str) : le lien de l'image a télécharger
            pre_path (str) : chemain pefait ou l'image va être enregistrer
            i (int) : un nombre de votre choix qui nomera votre page au format page_i.jpg
        
        Returns:
            int (int)
        """
        resolved_path = os.path.join(pre_path, f"page_{i}.jpg")
        try:
            image = requests.get(lien, timeout=20)
            if image.status_code == 200:
                with open(resolved_path, "wb") as f:
                    f.write(image.content)
        except requests.exceptions.RequestException:
            pass
        return 0

    def get_page_link(self) -> list:
        """
        Renvoie la liste des lien téléchargable du chapitre stocker dans l'objet self :
        
        Returns:
            self.page_link
        """
        return self.page_link

    def get_chapter_name(self) -> str:
        """
        Renvoie le nom au format str du chapitre souhaité (ex : "Chapitre 1") :

        Returns:
            self.chapter
        """
        return self.chapter

    def get_path(self) -> str: # Renvoie la valeur de la variable PATH 
        """
        Renvoie le path configurer pour l'objet chapter :

        Returns:
            self.path
        """
        return self.path

    def get_api_link(self) -> str: # Renvoie la valeur de la variable PATH
        """
        Renvoie le lien vers le quel l'objects chapter fait ses requets api :
        
        Returns:
            self.api_link
        """
        return self.api_link

    def get_title(self) -> str: # Revoie la valeur de title
        """"
        Renvoie la valeur de la variable titre associer au chapitre :

        Returns:
            self.title
        """
        return self.title