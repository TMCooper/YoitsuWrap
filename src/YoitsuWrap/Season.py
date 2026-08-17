from .Episode import Episode

class Season:
    saison: list[str]           # Saison actuelle (ex : saison 1, saison 2, etc...)
    title: str                  # Nom de la saison (ex : Frieren, Spice And Wolf, etc...)
    episode: list[Episode]      # Array des lien d'episode a télécharger

    def __init__(self, saison, title, episode): # Methode de creation de de l'objet complet season
        self.saison = saison
        self.title = title
        self.episode = episode

    def get_number(self): # Renvoie l'actuelle saison traité
        pass

    def get_title(self): # Renvoie le nom de la saison traité
        pass

    def download_season(self): # Télécharge toute la saison actuelle 
        pass