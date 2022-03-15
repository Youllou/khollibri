import json
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from SGBD.SGBD import *
from tkinter import *

def exportBase():

    sortie = {
        "Classes": {},
        "Exercices": {}
    }

    for i in giveClasse():
        sortie["Classes"][i] = giveChap(i)

    for i in ExoIdStock():
        sortie["Exercices"][i] = {
            "Enonce": giveEnonce(i)[0],
            "Corrige": giveCorrige(i)[0],
            "Contenu": {}
        }

    for i in sortie["Exercices"].keys():
        print(GiveExoFromChap(i))
        for j, k in GiveExoFromChap(i).items():

            sortie["Exercices"][i]["Contenu"][j] = {}

            sortie["Exercices"][i]["Contenu"][j]["Chapitres"] = k[0]
            sortie["Exercices"][i]["Contenu"][j]["Niveau"] = k[1]

    with open("json.json", "w") as f:
        json.dump(sortie, f)
        messagebox.showinfo(
            title="Export de base", message="Vous trouverez votre fichier json dans les fichiers de l'application.")
