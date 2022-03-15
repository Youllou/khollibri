from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import codecs
from tkinter.filedialog import askopenfilename

from Classes.Utils import Utils
from SGBD.exceptions.SGBDException import SGBDException


class GererPref(Frame):  # Classe de la fenêtre permettant de gérer les préférences d'utilisateur

    def __init__(self, parent, controller):
        import SGBD
        self.SGBD = SGBD.SGBD

        Frame.__init__(self, parent)

        self.controller = controller
        self.enonce = []
        self.enseignant = []

        self.PreferenceTexte = Label(self, text="Ajouter une préférence", font=controller.title_font)

        ################################################################################################################
        # correspond au cadre contenant le radio button de choix de mode
        self.cadre_choixMode = LabelFrame(self, text="Mode d'ajout")

        self.choixNbExos = IntVar()

        self.RadioButtonUnExo = Radiobutton(self.cadre_choixMode, text="Modification des préférences",
                                            variable=self.choixNbExos, value=0, command=self.SwitchView)
        self.RadioButtonNExo = Radiobutton(self.cadre_choixMode, text="Ajout d'un nouvel utilisateur",
                                           variable=self.choixNbExos, value=1, command=self.SwitchView)

        self.RadioButtonUnExo.pack(side=LEFT)
        self.RadioButtonNExo.pack(side=LEFT)

        ################################################################################################################
        # Modification de preférences

        self.ModifPref = Frame(self)
        self.CadreRelou = Frame(self.ModifPref)

        AuteurTexte = Label(self.CadreRelou, text="Selectionner les préférences par auteur:", font=("Helvetica", 10))
        AuteurTexte.pack(pady=5, padx=10, side=LEFT)

        self.cbAuteurs = Combobox(self.CadreRelou, values=self.SGBD.giveAuteur(), state='readonly')
        self.cbAuteurs.set("Choisir un utilisateur")
        self.cbAuteurs.pack(pady=5, side=LEFT)
        self.cbAuteurs.bind('<<ComboboxSelected>>', lambda event: self.ActualiseBouton())

        RaccourciTexte = Label(self.CadreRelou, text="Indiquer le raccourcis et la commande à ajouter",
                               font=("Helvetica", 10))
        RaccourciTexte.pack(pady=5, padx=10, side=LEFT)

        self.champNom = Entry(self.CadreRelou)
        self.champNom.pack(pady=5, side=LEFT)

        ValiderBoutton = Button(self.CadreRelou, text="Valider", command=lambda: self.ajouterChapitre())
        ValiderBoutton.pack(pady=5, side=LEFT)

        self.CadreRelou.pack()

        self.Pref = Button(self.ModifPref, text="Afficher l'ensemble des préférences pour cet auteur",
                           command=self.afficherPref)
        self.Pref.pack(pady=5, side=BOTTOM)
        self.Pref["state"] = "disabled"

        ################################################################################################################
        # Liste des raccourcis existants

        self.ListeRaccourci = Frame(self)

        Label(self.ListeRaccourci, text="Liste des raccourcis:", font=("Helvetica", 10)).pack(padx=10, side=TOP)

        self.ChampListePref = Listbox(self.ListeRaccourci, selectmode="multiple", width=120)
        self.ChampListePref.pack(padx=5, pady=5, expand=YES, fill="both", side=LEFT)

        ################################################################################################################
        # Ajouter un fichier

        self.CreerUtilisateur = Frame(self)

        FicherTexte = Label(self.CreerUtilisateur, text="Insérer votre nouveau fichier de préférence : ",
                            font=("Helvetica", 10))
        FicherTexte.pack(side=TOP, fill="x", pady=5)

        OuvrirBouton = Button(self.CreerUtilisateur, text="Ouvrir", command=lambda: self.open_file())
        OuvrirBouton.pack(pady=5, side=LEFT)

        self.champEnonce = Text(self.CreerUtilisateur, width=200, height=15, bg="#E5E5E5", fg="black",
                                insertbackground="black",
                                font="Helvetica 10", undo=True)
        Utils.configureColor(self.champEnonce)
        self.champEnonce.pack(pady=5)
        self.champEnonce.bind("<Key>", lambda event: Utils.updateCode(self.champEnonce))

        self.tags = ["red", "green", "yellow", "orange", "blue", "purple", "white"]

        self.wordlist = [
            [r"\newcommand", r"\begin", r"\end", r"\renewcommand", r"\DeclareMathOperator", r"\usepackage"],
            [r"\classe", r"\annee"],
            ["$", r"\[", r"\]"],
            ["exercice", "enumerate", "array", "question", "center", "tikzpicture", "scale"],
            ["geometry", "amsart", "titlesec"]]

        ################################################################################################################
        # Indiquer l'enseignant

        self.IndicEnseignant = Frame(self)

        Label(self.IndicEnseignant, text="Indiquer un nouvel enseignant : ", font=("Helvetica", 10)).pack(padx=10,
                                                                                                          side=LEFT)

        self.champEnseignant = Entry(self.IndicEnseignant)
        self.champEnseignant.pack(pady=5, side=LEFT)

        Button(self.IndicEnseignant, text=" Valider le fichier", command=lambda: self.ValiderFichierPref())\
            .pack(pady=5,side=BOTTOM)

        ################################################################################################################
        # Menu

        self.ShowFrame([self.ModifPref])

    def SwitchView(self):

        if self.choixNbExos.get() == 0:
            self.Pref["text"] = "Afficher l'ensemble des préférences pour cet auteur"
            self.ShowFrame([self.ModifPref])
        else:
            self.ShowFrame([self.CreerUtilisateur, self.IndicEnseignant])

    def ShowFrame(self, to_show):
        for widget in self.winfo_children():
            widget.pack_forget()

        self.PreferenceTexte.pack(side="top", fill="x", pady=10)

        self.cadre_choixMode.pack(side=TOP)

        for frame in to_show:
            frame.pack(side=TOP)

    def afficherPref(
            self):  # fonction permettant d'afficher les préférences (new commands seulement) d'un utilisateur depuis la base de données

        if self.ListeRaccourci.winfo_manager():
            self.ShowFrame([self.ModifPref])
            self.Pref["text"] = "Afficher l'ensemble des préférences pour cet auteur"

        else:
            self.ShowFrame([self.ModifPref, self.ListeRaccourci])

            self.Pref["text"] = "Cacher l'ensemble des préférences pour cet auteur"

            self.ChampListePref.delete(0, 'end')
            liste = self.SGBD.GivePrefFromAutor(self.cbAuteurs.get())

            for shortcuts in liste:
                self.ChampListePref.insert(1, (shortcuts[0] + "   " + shortcuts[1] + "\n"))

    def ActualiseBouton(self):
        self.Pref["state"] = "normal"

    def ajouterChapitre(self):
        self.SGBD.InsertClassAppChap(self.champNom.get(), self.cbAuteurs.get())

    # fonction permettant d'ajouter dans la base les nouvelles préférences selon un auteur

    def ValiderFichierPref(
            self):  # fonction permettant d'ajouter dans la base les nouvelles préférences selon un auteur

        self.enonce = self.champEnonce.get("1.0", "end-1c")
        self.auteur = self.NomEnseignant.get()

        if not self.auteur or self.auteur == "":
            messagebox.showinfo(title="Auteur", message="Merci de nommer votre nouvel enseignant.")
            return

        tab = self.remplissageCommand(self.enonce)
        self.SGBD.InsertAUTEUR(self.auteur)
        for command in tab:
            try:
                self.SGBD.InsertShortcuts(self.giveComShort(command)[1], self.auteur, self.giveComShort(command)[0])
            except SGBDException as e:
                messagebox.showerror(title="Il y a un petit problème", message=e.message)
                return
            except AttributeError as e:
                continue

        self.cbAuteurs['values'] = self.SGBD.giveAuteur()

        try:
            self.SGBD.SelectShortcuts()
        except SGBDException as e:
            messagebox.showerror(title="Il y a un petit problème", message=e.message)
            return
        messagebox.showinfo(title="Message très important", message="La préférence a été ajoutée.")


    def open_file(self):  # fonction permettant d'ouvrir un fichier de préférences
        filepath = askopenfilename(filetypes=[("Document Tex", "*.tex")])

        if not filepath:
            return

        self.champEnonce.delete(1.0, END)
        with codecs.open(filepath, "r", encoding="utf-8", errors='replace') as input_file:
            text = input_file.read()
            self.champEnonce.insert(END, text)
        Utils.updateCode(self.champEnonce)

    # fonction permettant de récupérer les new commands
    def remplissageCommand(self, contenu):
        tab = []

        lines = contenu.splitlines()
        for var in lines:
            if '\\newcommand' in var and '%\\newcommand' not in var:
                tab.append(var)

        return tab

    # fonction permettant de séparer la commande et la new command
    def giveComShort(self, chaine):
        import re

        pos1 = chaine.find('{') + 1
        pos2 = chaine.find('}')
        pattern = re.compile(
            r'\\newcommand{(\\[\w]*)}(\[\d*\])*{(?:([\w\\]*{\w*}({[\w# ]*})*)|([\w\\]*{A}\^2_{\\[\w]*})|(\\mathbb{\w*})|([^{}]*))}')

        rez = pattern.match(chaine)
        g1 = rez.group(1)
        g2 = rez.group(3) if rez.group(2) == None else rez.group(2)
        if (g2 == None):
            g2 = rez.group(4)

        if (g2 == "[1]"):
            g2 = rez.group(3)

        if (rez.group(7) != None):
            g2 = rez.group(7)

        if (rez.group(5) != None):
            g2 = rez.group(5)

        return g1, g2
