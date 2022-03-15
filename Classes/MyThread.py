import codecs, glob, shutil, threading, subprocess, os
from tkinter import messagebox
from SGBD.SGBD import *

from Classes import CreerFeuille
from Classes.ApplicationViews import *

exitFlag = 0

class myThread(threading.Thread):
    """
    Cette classe permet la création des différents Threads
    Il y a 5 threads différents :
            - ThreadAppli                   : Le lancement de l'application
            - ThreadPreVisualisation        : La génération et visualisation d'un exercice
            - ThreadPrevisualisationFeuille : La génération et visualisation d'une feuille de colle
            - ThreadLogCompilation          : Le lancement de la fenetre d'affichage de la compilation d'un exercice
            - WriteInLog                    : L'affichage de la compilation d'un exercice
    Afin de permettre cette dernière fonctionnalité,
    des méthodes ont été rajoutés afin de mimer le fonctionnement d'un objet File de python
    """

    def __init__(self, name, logWindow=None, pipeReader=None, enonceTemp=None, corrigeTemp=None, questionCours=None):
        """
        Constructeur de Threads
        :param name: Chaque threads ont un nom, celui-ci
                     permet l'identification du thread et ainsi, parmatrer le fonctionnement du thread
        :param logWindow: Paramètre nécessaire uniquement pour le Thread WriteInLog,
                          il permet d'identifié la fenetre crée par le thread LogCompilation et de, ainsi, la modifier
        :param pipeReader: Paramètre nécessaire uniquement pour le Thread WriteInLog,
                           il permet d'identifié la sortie de la commande de compilation et d'en récupéré le contenu
        """
        # dans tous les cas, on initialise le thread et le nom du thread
        threading.Thread.__init__(self)
        self.name = name
        # si le thread est celui de création de la fenetre de log,
        # on a besoin d'attribut pour mimer le fonctionnement d'un fichier
        if self.name == "ThreadLogCompilation":
            self.fdRead, self.fdWrite = os.pipe()
            self.pipeReader = os.fdopen(self.fdRead)
            self.daemon = False
        # si le thread est celui d'écriture de log, on récupère la fenetre et le reader
        if self.name == "WriteInLog":
            self.logWindow = logWindow
            self.pipeReader = pipeReader
        self.enonceTemp = enonceTemp
        self.corrigeTemp = corrigeTemp
        self.questionCours = questionCours

    def run(self):
        """
        méthode qui est appelée pour lancer un thread
        elle s'occupe de renvoyer vers la bonne méthode selon le nom du thread
        """
        if self.name == "ThreadAppli":
            self.application = ApplicationViews()
            self.creation_temp()
            self.application.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.application.mainloop()
        if self.name == "ThreadPreVisualisation":
            self.PrevisualisationExo()
        if self.name == "ThreadPrevisualisationFeuille":
            self.PrevisualtisaionFeuille()
        if self.name == "ThreadLogCompilation":
            self.LogCompilation()
        if self.name == "WriteInLog":
            self.WriteInLog()

    def PrevisualisationExo(self):
        """
        Fonction appelé lorsque le thread est ThreadPreVisualisation
        Il permet la compilation et l'affichage d'un exercice
        Ce Thread crée et appel le thread ThreadLogCompilation pour donner des informations à l'utilisateur
        # IMPORTANT : toute écriture dans un fichier tex pour qu'il soit compilé devra être en encodé UTF-8
        """
        temp = open('temp/exoTemp.tex', 'wb')
        with codecs.open("assets/tex/header.tex", encoding="utf-8", errors='replace') as fichier:
            contenu = fichier.readlines()
            for k in contenu:
                temp.write(k.encode('utf-8'))

            temp.write(("\n" + r"\begin{exo}" + "\n").encode('utf-8'))
            temp.write(self.enonceTemp.encode('utf-8'))

            temp.write(("\n" + r"\end{exo}" + "\n").encode('utf-8'))

            temp.write(("\n" + "\n" + r"\begin{sol}" + "\n").encode('utf-8'))
            temp.write(self.corrigeTemp.encode('utf-8'))
            temp.write(("\n" + r"\end{sol}" + "\n").encode('utf-8'))
            temp.write(("\end{document}").encode('utf-8'))

            temp.close()

            # on crée le thread de log et on le démarre
            log = myThread("ThreadLogCompilation")
            log.start()
            # ce thread peut être interprété comme fichier de sortie de commande
            # on peut donc spécifier a subprocess.Popen,
            # qui s'occupe de compiler le fichier latex via la commande de shell pdflatex,
            # que le fichier de sortie est le thread ThreadLogCompilation
            process = subprocess.Popen(
                ['pdflatex', "-halt-on-error ", 'temp/exoTemp.tex'], stdout=log,
                stderr=log)
            # on attend la fin de la compilation
            # (par défaut subprocess.Popen renvoi dès le lancement de la commande)
            process.wait()

            # on ferme le "fichier"
            os.close(log.fdWrite)
            # et on attend la fin du thread
            log.join()

            shutil.move('exoTemp.pdf', 'temp/exoTemp.pdf')
            list_of_files = glob.glob(r'temp/*.pdf')
            latest_file = max(list_of_files, key=os.path.getctime)

            os.remove("exoTemp.aux")
            os.remove("exoTemp.log")
            os.remove("exoTemp.out")

            self.open_file(latest_file)

    def PrevisualtisaionFeuille(self):
        temp = open('temp/exoTemp.tex', 'wb')
        with codecs.open("assets/tex/header.tex", encoding="utf-8", errors='replace') as fichier:
            contenu = fichier.readlines()
            write = True
            for k in contenu:
                if write:
                    if k.startswith(r'\begin{cours}'):
                        if self.questionCours != "":
                            temp.write(k.encode('utf-8'))
                            temp.write(self.questionCours.encode('utf-8'))
                        write = False
                    else:
                        temp.write(k.encode('utf-8'))
                else:
                    if k.startswith(r'\end{cours}'):
                        if self.questionCours != "":
                            temp.write(k.encode('utf-8'))
                        write = True

            temp.write(('\n').encode('utf-8'))
            temp.write((r"\reversemarginpar").encode('utf-8'))

            for exoId in CreerFeuille.listeFinale.keys():
                exo = [exoId,
                       CreerFeuille.listeFinale.get(exoId).get("exo"),
                       CreerFeuille.listeFinale.get(exoId).get("sol")]
                print(exo)
                temp.write(("\n" + r"\begin{exo}" + "\n").encode('utf-8'))
                temp.write((
                                       "\n" + r"\marginpar{\small{\vspace{\baselineskip} \hspace{0.05cm} \textcolor{rouge}{ID exo :}} " + str(
                                   exo[0]) + "}").encode('utf-8'))
                temp.write(exo[1].encode('utf-8'))

                temp.write(("\n" + r"\end{exo}" + "\n").encode('utf-8'))

                temp.write(("\n" + "\n" + r"\begin{sol}" + "\n").encode('utf-8'))
                temp.write(exo[2].encode('utf-8'))
                temp.write(("\n" + r"\end{sol}" + "\n").encode('utf-8'))

            temp.write(("\end{document}").encode('utf-8'))
            temp.close()

            subprocess.check_output(["pdflatex", "temp/exoTemp.tex"])
            try:
                shutil.move('exoTemp.pdf', 'temp/exoTemp.pdf')
            except FileNotFoundError as e:
                messagebox.showerror(title="Erreur lors de la compilation",
                                     message="pdflatex est nécessaire à la compilation des fichers\nVeuillez l'installer avant de continuer")
            else:
                # création d'un pop-up
                messagebox.showinfo(title="Veuillez patienter, compilation en cours",
                                    message="La prévisualisation s'ouvrira d'elle même")

                list_of_files = glob.glob(r'temp/*.pdf')
                latest_file = max(list_of_files, key=os.path.getctime)

                os.remove("exoTemp.aux")
                os.remove("exoTemp.log")
                os.remove("exoTemp.out")
                self.open_file(latest_file)

    def LogCompilation(self):
        logWindow = Tk()
        logWindow.title = "Compilation en Cours"
        logText = Text(logWindow, bg="#E5E5E5")
        logText.pack()
        finishButton = Button(logWindow, text="Afficher l'exercice", state='disabled')
        finishButton.pack()
        writer = myThread("WriteInLog", logWindow, self.pipeReader)
        writer.start()
        logWindow.mainloop()
        writer.join()
        self.pipeReader.close()

    def WriteInLog(self):
        logText = self.logWindow.winfo_children()[0]
        finishButton = self.logWindow.winfo_children()[1]
        for line in iter(self.pipeReader.readline, ''):
            logText.configure(state='normal')
            logText.insert('end', line)
            logText.see('end')
            logText.configure(state='disabled')
        self.pipeReader.close()
        finishButton.configure(command=self.logWindow.destroy, state='normal')

    def open_file(self, filename):
        if "win" in sys.platform.lower():
            os.startfile(filename)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, filename])

    def fileno(self):
        """Return the write file descriptor of the pipe
      """
        return self.fdWrite

    def creation_temp(self):
        try:
            if not os.path.exists("temp"):
                os.makedirs('temp')
        except:
            messagebox.showerror("Impossible de créer le dossier temp. Essayez de créer un dossier temp.")
            return

    def on_closing(self):
        try:
            shutil.rmtree('./temp', ignore_errors=True)
        except:
            print("Impossible de supprimer le dossier temp.")
        self.application.destroy()
        exit()
