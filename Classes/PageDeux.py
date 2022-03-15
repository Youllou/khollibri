# Projet DUT2 Soft de génération de feuilles d'exercices

from tkinter import *
from tkinter.ttk import *

"""
Classe contenant l'architecture de base d'une fenêtre, le nom de la classe correspond au nom de la fenêtre
"""


class PageDeux(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
