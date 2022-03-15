import _tkinter
import codecs
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.ttk import *

import SGBD
from Classes.AjouterExercice import AjouterExercice
from Classes.Utils import Utils


class AjouterNExercices(Frame):

    def __init__(self, parent, controller):

        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        label = Label(self, text="Ajouter Plusieurs Exercice", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.emplaceAjout = {}

        self.enonce = []
        self.corrige = []
        self.SGBD = SGBD.SGBD
        self.isFirstLoop = True

        # correspond à la page lorsque l'on veut ajouter plusieurs exercice
        # ce n'est pas la page affichée par défaut
        self.Page_AjoutNExo = Frame(self)

        self.listeExo = []
        self.listeSol = []

        self.BouttonImport = Button(self.Page_AjoutNExo, text="Choisir le fichier", command=lambda: self.open_file())
        self.BouttonImport.pack(pady=(100, 0))

        self.labelNbExo = Label(self.Page_AjoutNExo, text=f"Nombre d'exercices détéctés : {len(self.listeExo)}")
        self.labelNbExo.pack()

        self.labelRapel = Label(self.Page_AjoutNExo, text="Rappel :\n"
                                                          "Les fichiers d'exercice doivent être du format suivant : ")
        self.labelRapel.pack(pady=20)

        self.rappelFormat = Text(self.Page_AjoutNExo, width=50, height=10, bg="#E5E5E5", fg="black",
                                 insertbackground="black",
                                 font="Helvetica 10", undo=True)

        self.rappelFormat.insert(END,
                                 "\\begin{exo}\n% Exercice\n\\end{exo}\n\n\\begin{sol}\n% Solution (peut etre laissée vide)\n\\end{sol}")
        Utils.configureColor(self.rappelFormat)
        Utils.updateCode(self.rappelFormat)
        self.rappelFormat.configure(state='disabled')
        self.rappelFormat.pack()

        self.BouttonValiderImport = Button(self.Page_AjoutNExo, text='Valider', state='disabled',
                                           command=self.processList)
        self.BouttonValiderImport.pack()

        self.Page_AjoutNExo.pack()

    def open_file(self):
        try:
            filepath = askopenfilename(filetypes=[("Document Tex", "*.tex")])
        except _tkinter.TclError:
            exit()

        with codecs.open(filepath, "r", encoding="utf-8", errors='replace') as input_file:
            text = input_file.read()

        self.listeExo, self.listeSol = self.ExoAndSolFromText(text)
        if len(self.listeExo) == 0:
            messagebox.showerror("Fichier Incorrect",
                                 "Aucun exercice n'a été détecté, vérifiez que le fichier suis le format d'exercice indiqué")
        else:
            self.labelNbExo.configure(text=f"Nombre d'exercices détectés : {len(self.listeExo)}")
            self.BouttonValiderImport.configure(state='normal')

    def ExoAndSolFromText(self, data):

        splitted_exo = [oneSplit for oneSplit in data.split("\\begin{exo}")[1:]]
        exos = [OneExo.split("\end{exo}")[0] for OneExo in splitted_exo]

        splitted_sol = [oneSplit for oneSplit in data.split("\\begin{sol}")[1:]]
        sol = [OneSol.split("\end{sol}")[0] for OneSol in splitted_sol]

        return exos, sol

    def processList(self):
        self.destroy()
        for exo,sol,ind in zip(self.listeExo,self.listeSol,range(len(self.listeExo))):
            AjouterExercice.launchWithData(self.parent, self.controller, exo, sol,ind)


