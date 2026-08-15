class Episode:
    title: str          # Titre de l'episode une fois télécharger (ex : ep 1, ep 2, etc...)
    link: str           # Lien direct vers l'episode
    path: str           # Path ou l'épisode sera ranger
    number: int         # Number est le nombre de l'épisode souhaité (ex : 6 si on télécharge l'ep 5) 

    def __init__(self, title, path, number):
        self.title = title
        self.link = "URL_FICTIF"        # get_link futur méthode de récuperation de lien
        self.path = "PATH_FICTIF"
        self.number = 3                 # Valeur fictive