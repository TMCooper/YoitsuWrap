class Config:
    BASE_URL=str            # La base du lien de l'api a request
    PORT=int                # Le port associer a l'api que l'on dois request

    def __init__(self, BASE_URL, PORT): # Méthode de construction de l'objet config
        self.BASE_URL = BASE_URL
        self.PORT = PORT
