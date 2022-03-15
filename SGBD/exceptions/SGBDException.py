## Projet DUT2 Soft de génération de feuilles d'exercices

class SGBDException(Exception):
    """
    Exception levée dans la classe SGBD
    """

    def __init__(self, message="La requête n'a pas pu aboutir."):
        self.message = message
        super().__init__(self.message)
