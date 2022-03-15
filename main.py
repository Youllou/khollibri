## Projet DUT2 Soft de génération de feuilles d'exercices

import SGBD.SGBD
from Classes.MyThread import *

"""
Programme principal
"""
if __name__ == '__main__':
	# création des tables
	SGBD.SGBD.Createtables()

	# lancement du thread principal
	threadPrincipal = myThread("ThreadAppli")
	threadPrincipal.start()
