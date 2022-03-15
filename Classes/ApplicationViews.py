from tkinter.font import *
from tkinter import *
import sys

from Classes.AfficherExo import AfficherExo
from Classes.AjouterClasse import AjouterClasse
from Classes.AjouterExercice import AjouterExercice
from Classes.AjouterNExrecices import AjouterNExercices
from Classes.Bienvenue import Bienvenue
from Classes.CreerFeuille import CreerFeuille
from Classes.GererPref import GererPref
from Classes.GererPref2 import GererPref2
from Classes.GestionChapitre import GestionChapitre
from Classes.MenPrincipal import MenuBar
from Classes.PageDeux import PageDeux


# Classe permettant de charger l'ensemble des frames/fenêtres. Pour toute fenêtre créée, il est obligatoire de la charger ici
class ApplicationViews(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        w, h = Tk.winfo_screenwidth(self), Tk.winfo_screenheight(self)
        self.title("Application de génération de sujets")
        self.iconphoto(False, PhotoImage(file='assets/logouniv.png'))
        if "win" in sys.platform.lower():
            self.state("zoomed")
        else :

            self.attributes('-zoomed', True)
        self.title_font = Font(family='Helvetica', size=18, weight="bold", slant="italic")
        menubar = MenuBar(self)
        Tk.config(self,menu=menubar)


        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.pages = (AjouterExercice, PageDeux, AfficherExo,
                      CreerFeuille, AjouterClasse, GestionChapitre,
                      GererPref, GererPref2, Bienvenue, AjouterNExercices)
        for F in self.pages:
            frame = F(self.container, self)
            self.frames[F] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Bienvenue)

    def show_frame(self, page):
        if page == "MenuBar":
            page = MenuBar
        # fonction permettant d'afficher une fenêtre selon son nom
        frame = page(parent=self.container, controller=self)
        self.frames[page] = frame

        # put all of the pages in the same location;
        # the one on the top of the stacking order
        # will be the one that is visible.
        frame.grid(row=0, column=0, sticky="nsew")

        frame.tkraise()

    def fissionChapitre(self,classe):
        self.show_frame()
