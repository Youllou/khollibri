from tkinter import *
from tkinter import messagebox
import tkinter
from tkinter.ttk import *


class GestionChapitre(
        Frame):  # Classe de la fenêtre permettant d'ajouter un chapitre dans la base de données selon une classe

    def __init__(self, parent, controller):
        super().__init__(parent)
        import SGBD
        self.SGBD = SGBD.SGBD

        self.controller = controller

        self.cadre_Haut = Frame(self)

        self.labelTitre = Label(self.cadre_Haut, text="Gestion des chapitres", font=controller.title_font)
        self.labelTitre.pack(fill="both", pady=10)

        ########################################

        self.cadre_ChoixClasse = Frame(self.cadre_Haut)

        self.labelChoixClasse = Label(self.cadre_ChoixClasse, text="choisissez la classe : ")
        self.labelChoixClasse.pack(side=LEFT)

        self.ComboClass = Combobox(self.cadre_ChoixClasse, values=self.SGBD.giveClasse(), state='readonly')
        self.ComboClass.set("Choisir une classe")
        self.ComboClass.pack(padx=(5, 0), side=LEFT)
        self.ComboClass.bind('<<ComboboxSelected>>', lambda event: self.ChangeClasse())

        self.cadre_ChoixClasse.pack(side=TOP)

        self.cadre_Haut.pack(side=TOP,fill="x")

        ########################################

        self.cadre_Corp = Frame(self)

        self.cadre_ChoixChapitre = Frame(self.cadre_Corp)

        self.labelChapitre = Label(self.cadre_ChoixChapitre, text="Liste des chapitres de cette classe")
        self.labelChapitre.pack(side=TOP)

        self.champListeChap = Listbox(self.cadre_ChoixChapitre, selectmode="multiple", exportselection=False)
        self.champListeChap.pack(side=LEFT,fill=BOTH)

        self.cadre_ChoixChapitre.pack(side=LEFT,fill=Y)

        ########################################

        self.cadre_Boutons = Frame(self.cadre_Corp)

        self.Boutton_ajouter = Button(self.cadre_Boutons, text="Ajouter un chapitre", command=self.ajouterChapitre)

        self.labelNewChapitre = Label(self.cadre_Boutons, text="Nouveau chapitre :")
        self.labelNewChapitre.grid(row=0, column=0)

        self.newChapitre = Text(self.cadre_Boutons, height=self.Boutton_ajouter.winfo_height(), width=20)
        self.newChapitre.grid(row=1, column=0, padx=(0, 5))

        self.Boutton_ajouter.grid(row=0, column=1)

        self.Boutton_fusion = Button(self.cadre_Boutons, text="Fusionner deux chapitres", command=self.fusionChapitre)
        self.Boutton_fusion.grid(row=1, column=1, pady=5)

        self.Boutton_fission = tkinter.Button(self.cadre_Boutons, text="Casser un chapitre",
                                              command=self.startFissionChapitre)
        self.Boutton_fission.grid(row=2, column=1)

        self.cadre_Boutons.pack(side=TOP)

        ########################################

        self.cadre_Fission = Frame(self.cadre_Corp)
        self.cadre_Fission.rowconfigure(1,weight=5)
        self.labelNewFissure = Label(self.cadre_Fission, text="Nom des nouveaux chapitres")
        self.labelNewFissure.grid(row=0, column=0)

        self.newChapitreFission = Text(self.cadre_Fission, height=self.labelNewFissure.winfo_height(), width=20)
        self.newChapitreFission.grid(row=0, column=1, padx=5)

        self.newFissureButton = Button(self.cadre_Fission, text="Ajouter le nouveau chapitre",command=self.addToFission)
        self.newFissureButton.grid(row=0, column=2)

        self.champChapFission = Listbox(self.cadre_Fission, selectmode=SINGLE, exportselection=False)
        self.champChapFission.grid(row=2, column=0, columnspan=3, sticky=N+W+S+E)

        self.pic = PhotoImage("Fission", file="assets/arrow.png")
        self.arrow = Label(self.cadre_Boutons, image=self.pic)

        self.cadre_Corp.pack(side=TOP,fill="both",padx=20)

        self.cadre_Bas = Frame(self)

        self.Boutton_ValiderFission = Button(self.cadre_Bas, text="Conttinuer la fission du chapitre", command=self.repartitionExo)
        self.cadre_Bas.pack(side=BOTTOM,fill=X)

    def startFissionChapitre(self):
        if self.Boutton_fission['relief'] == SUNKEN:
            self.champListeChap.configure(selectmode=MULTIPLE)
            self.Boutton_ajouter.configure(state=NORMAL)
            self.Boutton_fusion.configure(state=NORMAL)
            self.newChapitre.configure(state=NORMAL)
            self.Boutton_fission.configure(relief=RAISED)
            self.arrow.grid_forget()
            self.cadre_Fission.pack_forget()
            self.SGBD.ClearTableTempChap()
            self.Boutton_ValiderFission.pack_forget()

        else:
            self.champListeChap.select_clear(0, END)
            self.champListeChap.configure(selectmode=SINGLE)
            self.newChapitre.configure(state=DISABLED)
            self.Boutton_ajouter.configure(state=DISABLED)
            self.Boutton_fusion.configure(state=DISABLED)
            self.Boutton_fission.configure(relief=SUNKEN)
            self.arrow.grid(row=3, column=0, columnspan=2)
            self.cadre_Fission.pack(side=RIGHT)
            self.ActualiseAffichage()
            self.Boutton_ValiderFission.pack(side=RIGHT)

    def addToFission(self):
        newChapName = self.newChapitreFission.get(1.0, 'end-1c')
        self.newChapitreFission.delete('1.0',END)
        self.newChapitreFission.focus()
        if newChapName == "":
            messagebox.showinfo(title="Chapitre",
                                message="Merci d'écrire un nom de chapitre")
            return

        if self.ComboClass.get() == "Choisir une classe":
            messagebox.showinfo(title="Chapitre",
                                message="Merci de choisir une classe")
            return

        listChap = self.SGBD.giveChap(self.ComboClass.get())
        listChap+=self.SGBD.giveTempChap()
        print(listChap)

        for chap in listChap:
            if chap == newChapName:
                messagebox.showinfo(title="Chapitre",
                                    message="Merci de choisir un nom de chapitre non existant")
                return

        self.SGBD.InsertTableTempChap(newChapName)
        self.ActualiseAffichage()

    def repartitionExo(self):
        if self.champChapFission.size() <= 1:
            messagebox.showinfo(title="Chapitre",
                                message="Merci d'ajouter au moins deux chapitres")
            return

        if len(self.champListeChap.curselection()) == 0:
            messagebox.showinfo(title="Chapitre",
                                message="Merci de choisir un chapitre à casser")

            return

    def fusionChapitre(self):
        classeToWork = self.ComboClass.get()
        if classeToWork == "Choisir une classe":
            messagebox.showinfo(title="Classe",
                                message="Merci de choisir une classe existante")
            return

        newChapitrename = self.newChapitre.get(1.0, "end-1c")
        if newChapitrename == "":
            messagebox.showinfo(title="Chapitre",
                                message="Merci d'écrire un nom de chapitre")
            return

        listechap = self.SGBD.giveChap(self.ComboClass.get())

        for chap in listechap:
            if chap == newChapitrename:
                messagebox.showinfo(title="Chapitre",
                                    message="Merci de choisir un nom de chapitre non existant")
                return

        aFusioner = [self.champListeChap.get(i).replace("\n", "") for i in self.champListeChap.curselection()]
        if len(aFusioner) <= 1:
            messagebox.showinfo(title="Chapitre",
                                message="Merci de choisir au moins deux chapitres à fusionner")
            return

        self.SGBD.ClearTableTempChap()
        self.SGBD.CreateTableTempChap()
        self.SGBD.InsertClassAppChap(newChapitrename, classeToWork)
        for chapitre in aFusioner:
            self.SGBD.InsertTableTempChap(chapitre)
        self.SGBD.fusion(newChapitrename, classeToWork)

        messagebox.showinfo(title="Chapitre",
                            message="La fusion a bien été effectué")
        self.SGBD.ClearTableTempChap()
        self.ActualiseAffichage()

    def ajouterChapitre(self):  # fonction qui permet d'ajouter des chapitres dans la base

        if self.ComboClass.get() == "Choisir une classe":
            messagebox.showinfo(title="Classe",
                                message="Merci de choisir une classe existante")
            return

        if self.newChapitre.get(1.0, "end-1c") == "":
            messagebox.showinfo(title="Chapitre",
                                message="Merci d'écrire un nom de chapitre")
            return

        listechap = self.SGBD.giveChap(self.ComboClass.get())

        for chap in listechap:
            if chap == self.newChapitre.get(1.0, "end-1c"):
                messagebox.showinfo(title="Chapitre",
                                    message="Merci de choisir un nom de chapitre non existant")
                return

        self.SGBD.InsertClassAppChap(self.newChapitre.get(1.0, "end-1c"), self.ComboClass.get())

        messagebox.showinfo(title="Chapitre", message="Le chapitre a bien été crée.")

    def ActualiseAffichage(self):

        self.champListeChap.delete(0, 'end')
        print(self.ComboClass.get())
        liste = self.SGBD.giveChap(self.ComboClass.get())

        for chap in liste:
            self.champListeChap.insert(0, chap)

        self.champChapFission.delete(0,END)

        listeFission = self.SGBD.giveTempChap()

        if listeFission:
            for chap in listeFission:
                self.champChapFission.insert(0,chap)

    def ChangeClasse(self):
        self.SGBD.ClearTableTempChap()
        self.ActualiseAffichage()
