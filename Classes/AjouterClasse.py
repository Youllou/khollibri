from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *

import SGBD


class AjouterClasse(Frame): #Classe de la fenêtre pour ajouter une classe dans la base de données.

    def __init__(self, parent, controller):
        
        self.SGBD = SGBD.SGBD
        Frame.__init__(self, parent)
        self.controller = controller

        self.listeChoixChap = []

        label = Label(self, text="Ajouter une classe", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.cadre1 = Frame(self)

        self.buttonAfficher = Button(self.cadre1, text="Afficher l'ensemble des classes", command=self.afficherClasse)
        self.buttonAfficher.pack(pady=5, side=BOTTOM)

        Label(self.cadre1,
              text="Indiquer le nom de la classe à ajouter:",
              font=("Helvetica", 10)).pack(pady=5, padx=10, side=LEFT)
        self.champNom = Entry(self.cadre1)
        self.champNom.pack(pady=5, side=LEFT)
        self.continuer = Button(self.cadre1, text="Continuer",
               command=lambda: self.ajouterClasse())
        self.continuer.pack(pady=5, side=LEFT)

        self.cadre2 = Frame(self)
        Label(self.cadre2,
              text="Liste des classes déjà présentes dans la base de données:",
              font=("Helvetica", 10)).pack(pady=5, padx=10, side=TOP)
        self.champListeClasses = Listbox(self.cadre2, selectmode = "multiple")
        self.champListeClasses.pack(padx = 10, pady = 10, expand = YES, fill = "both")
        self.supprimerButton = Button(self.cadre2, text="Supprimer (pas encore implémenté)", state='disabled',
                                      command=lambda: self.supprimerC()).pack(pady=5,
                                                                                 side=LEFT)
        self.cadre1.pack(pady=10)

        self.cadre3 = Frame(self)
        self.champChoixChap = Listbox(self.cadre3, selectmode = "multiple")
        self.champChoixChap.pack(padx = 10, pady = 10, expand = YES, fill = "both",side=BOTTOM)
        Label(self.cadre3,
              text="Indiquer au moins un chapitre à ajouter dans la classe:",
              font=("Helvetica", 10)).pack(pady=5, padx=10, side=LEFT)
        self.champChap = Entry(self.cadre3)
        self.champChap.pack(pady=5, side=LEFT)
        Button(self.cadre3, text="Ajouter un chapitre",
               command=lambda: self.ajouterChap()).pack(pady=5, side=LEFT)

        self.supprimerButton = Button(self.cadre3, text="Supprimer", command=lambda: self.supprimerChap()).pack(pady=5,
                                                                                                            side=LEFT)

    def ajouterClasse(self): #fonction permettant de passe au choix des chapitres après avoir choisi le nom de la nouvelle classe

        if self.champNom.get() == "" :
            messagebox.showinfo(title="Classe", message="Merci de préciser un nom de classe.")
            return

        liste = self.SGBD.giveClasse()
        for classe in liste:
            if self.champNom.get() == classe :
                messagebox.showinfo(title="Classe", message="Merci de préciser un nom non existant.")
                return

        self.continuer['state'] = 'disabled'

        if self.cadre2.winfo_manager() :
            self.cadre2.pack_forget()
            self.buttonAfficher["text"] ="Afficher l'ensemble des chapitres"
        
        self.buttonAfficher['state'] = 'disabled'

        self.cadre3.pack(pady=5)
        self.cadre4 = Frame(self)
        Button(self.cadre4, text="Valider",
               command=lambda: self.valider()).pack(pady=5, side=LEFT)
        self.cadre4.pack(pady=5)

        self.champNom['state'] = 'disabled'

    def afficherClasse(self): #fonction permettant d'afficher dans un champd de texte l'ensemble des classes présentes dans la base

        if self.cadre2.winfo_manager() :
            self.cadre2.pack_forget()
            self.buttonAfficher["text"] ="Afficher l'ensemble des chapitres"

        else :
            self.cadre2.pack(pady=10)       
            self.buttonAfficher["text"] ="Cacher l'ensemble des chapitres"

            self.ActualiseAffichageClasse()

    def ActualiseAffichageClasse(self) :
        self.champListeClasses.delete(0,'end')
            
        liste = self.SGBD.giveClasse()
        for classe in liste:
            classe+="\n"
            self.champListeClasses.insert(0,classe)

    def ajouterChap(self): #fonction permettant de faire le choix des chapitres à ajouter

        if self.champChap.get() == "" :
            messagebox.showinfo(title="Classe", message="Merci de préciser un nom de chapitre.")
            return

        if self.champChap.get() in self.listeChoixChap :
            messagebox.showinfo(title="Classe", message="Merci de préciser un nom de chapitre non existant.")
            return

        self.listeChoixChap.append(self.champChap.get())
        
        self.champChoixChap.insert(END,self.champChap.get())

        self.champChap.delete(0, 'end')

    def valider(self): #fonction permettant d'ajouter les choix effectués dans la base de données

        if not self.listeChoixChap :
            messagebox.showinfo(title="Classe", message="Merci de créer au moins un chapitre.")
            return
        self.SGBD.InsertCLASSE(self.champNom.get())
        for chap in self.listeChoixChap:
            self.SGBD.InsertClassAppChap(chap,self.champNom.get())

        self.SGBD.SelectClassAppChap()

        messagebox.showinfo(title="Classe", message="La classe a bien été crée.")

    def supprimerChap(self) :

        chapSuppr = 0
        for i in self.champChoixChap.curselection():
            self.listeChoixChap.pop(i-chapSuppr)
            chapSuppr += 1

        self.champChoixChap.delete(0, "end")

        for value in self.listeChoixChap:
            self.champChoixChap.insert(END, value)