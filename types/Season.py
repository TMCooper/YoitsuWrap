from Episode import Episode

class Season:
    number: str                 # Saison actuelle (ex : saison 1, saison 2, etc...)
    title: str                  # Nom de la saison (ex : Frieren, Spice And Wolf, etc...)
    episode: list[Episode]      # Array des lien d'episode a télécharger

    def __init__(self, number, title, episode):
        self.number = number
        self.title = title
        self.episode = episode

    def construct(self): # Methode de creation de de l'objet complet season
        pass
    
    def get_number(self): # Renvoie l'actuelle saison traité
        pass

    def get_title(self): # Renvoie le nom de la saison traité
        pass

    def download_season(self): # Télécharge toute la saison actuelle 
        pass