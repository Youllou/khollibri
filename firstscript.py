import os
import pathlib
from tkinter import filedialog
import shutil

#ce script (PAS ENCORE FONCTIONNEL) devra etre lancé apres le téléchargement de l'application pour installer les bibliothèque et generer le .exe à l'endroit souhaité

# Installe les bibliothèques non natives nécéssaires
cmd = 'pip3 install glob2'
# os.system(cmd) #installe glob
cmd2 = 'pip install pyinstaller'
#os.system(cmd2) #installe pyinstaller pour generer un .exe de l'application (ne marche pas pour l'instant)
cmd3 = 'pyinstaller --onefile main.py'
#os.system(cmd3)
#ouvre la fenetre de choix du dossier d'installation
#dirname = filedialog.askdirectory(initialdir="/",
#                                      title="Choisir un dossier",
#                                      mustexist = True)

originalpath = os.path.abspath("appliComplete") #pathlib.Path().resolve()
#print(dirname)
print(originalpath)
#shutil.move(originalpath,dirname)
print(pathlib.Path().resolve())