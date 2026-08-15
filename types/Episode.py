class Episode:
    title: str          # Titre de l'episode une fois télécharger (ex : ep 1, ep 2, etc...)
    link: str           # Lien direct vers l'episode
    path: str           # Path ou l'épisode sera ranger
    number: int         # Number est le nombre de l'épisode souhaité (ex : 6 si on télécharge l'ep 5) 

    def __init__(self, title, path, number):
        self.title = title
        self.link = "URL_FICTIF"        # get_link futur méthode de récuperation de lien
        self.path = path
        self.number = 3                 # Valeur fictive

    def construct(self): # Methode de contruction de l'objet Episode
        pass

    def get_title(self): # Renvoie le nom de l'épisode
        pass

    def get_link(self): # Renvoie le lien téléchargable de l'épisode
        pass

    def __get_path(self): # Méthode privée pour ranger l'épisode a un path spécifique
        pass

    def get_number(self): # Renvoie ne numero de l'épisode traité
        pass

    def download_episode(self): # Télécharge un épisode spécifique
        pass