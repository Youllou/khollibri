from tkinter import *
from tkinter.ttk import *

from Classes.AfficherExo import AfficherExo
from Classes.AjouterClasse import AjouterClasse
from Classes.AjouterExercice import AjouterExercice
from Classes.AjouterNExrecices import AjouterNExercices
from Classes.CreerFeuille import CreerFeuille
from Classes.GererPref import GererPref
import Classes.ExporterBase
from Classes.ImporterBase import importBase
from Classes.GererPref2 import GererPref2
from Classes.GestionChapitre import GestionChapitre
from Classes.PageDeux import PageDeux


class MenuBar(Menu):
    def __init__(self, parent):
        Menu.__init__(self, parent)

        menu_user = Menu(self, tearoff=0)
        self.add_cascade(label="Utilisateur", menu=menu_user)
        menu_user.add_command(label="Créer un nouvel utilisateur (gererPref)",
                              command=lambda: parent.show_frame(GererPref))
        menu_user.add_separator()
        menu_user.add_command(label="Modifier un profil (gererPref2)",
                              command=lambda: parent.show_frame(GererPref2))

        self.add_separator()

        menu_exo = Menu(self, tearoff=0)
        self.add_cascade(label="Exercices", menu=menu_exo)
        menu_exo.add_command(label="Ajouter un exercice",
                             command=lambda: parent.show_frame(AjouterExercice))
        menu_exo.add_separator()
        menu_exo.add_command(label="Ajouter plusieurs exercices",
                             command=lambda: parent.show_frame(AjouterNExercices))
        menu_exo.add_separator()
        menu_exo.add_command(label="Afficher un exercice",
                             command=lambda: parent.show_frame(AfficherExo))

        self.add_separator()

        menu_feuille = Menu(self, tearoff=0)
        self.add_cascade(label="Feuille d'exercices", menu=menu_feuille)
        menu_feuille.add_command(label="Creer une feuille d'exercices",
                                 command=lambda: parent.show_frame(CreerFeuille))

        self.add_separator()

        menu_chapitre = Menu(self, tearoff=0)
        self.add_cascade(label="Gérer les chapitres", menu=menu_chapitre)
        menu_chapitre.add_command(
            label="Ajouter un chapitre", command=lambda: parent.show_frame(GestionChapitre))
        menu_chapitre.add_separator()
        menu_chapitre.add_command(
            label="Fusionner des chapitres", command=lambda: parent.show_frame(GestionChapitre))
        menu_chapitre.add_separator()
        menu_chapitre.add_command(
            label="Diviser un chapitre", command=lambda: parent.show_frame(GestionChapitre))

        self.add_separator()

        menu_classe = Menu(self, tearoff=0)
        self.add_cascade(label="Gérer les classes", menu=menu_classe)
        menu_classe.add_command(
            label="Ajouter une classe", command=lambda: parent.show_frame(AjouterClasse))
        self.add_separator()

        menu_traitementbase = Menu(self, tearoff=0)
        self.add_cascade(label="Traiter base", menu=menu_traitementbase)
        menu_traitementbase.add_command(
            label="Exporter base", command=lambda: Classes.ExporterBase.exportBase())
        menu_traitementbase.add_separator()
        menu_traitementbase.add_command(
            label="Importer base", command=lambda: parent.show_frame(importBase))