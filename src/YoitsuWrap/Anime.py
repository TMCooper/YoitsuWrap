from Scan import Scan
from Season import Season

class Anime:
    title: str        # Titre de l'oeuvre (ex : Frieren, Spice And Wolf)
    cover: str        # Lien vers l'images de couverture de l'animer
    link: str         # Lien vers l'animer
    # episode_num: int  # Nombre d'épisode dans l'anime # L'api ne renvoie pas d'épisode num pour l'instant

    def __init__(self, title, cover, link): # Construit l'objet anime
        self.title = title
        self.cover = cover
        self.link = link

    def get_title(self): # Renvoie le nom de l'oeuvre
        pass

    def get_cover(self): # Renvera l'url de la couverture de l'animer
        pass

    def get_link(self): # Renvera le lien direct de l'animer (pas lien de téléchargement)
        pass

    def download_anime(self): # Méthode de téléchargement de l'anime
        pass