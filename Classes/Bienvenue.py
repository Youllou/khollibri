from tkinter import *


class Bienvenue(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.labelBienvenu = Label(self,text="Bienvenue sur",font=self.controller.title_font)
        self.labelBienvenu.pack(pady=15)
        label = Label(self, text="Soft de génération de feuilles d'exercices", font=self.controller.title_font)
        label.pack(pady=15)

        self.cadre_bas = Frame(self)
        self.credits = Button(self.cadre_bas, text="Credits")
        self.credits.pack(side=RIGHT)
        self.cadre_bas.pack(side=BOTTOM, fill='x', pady=5, padx=5)
