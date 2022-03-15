import _tkinter
import codecs
from tkinter import *
from tkinter.filedialog import askopenfilename


class Utils():
    TAGS = ["red", "green", "yellow", "orange", "blue", "purple", "white"]

    WORDLIST = [
        [r"\newcommand", r"\begin", r"\end", r"\renewcommand", r"\DeclareMathOperator", r"\usepackage"],
        [r"\classe", r"\annee"],
        ["$", r"\[", r"\]"],
        ["exercice", "enumerate", "array", "question", "center", "tikzpicture", "scale"],
        ["geometry", "amsart", "titlesec"]
    ]

    @staticmethod
    def check(champ, index, pre, post):
        letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
                   "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

        if champ.get(pre) == champ.get(index):
            pre = index
        else:
            if champ.get(pre) in letters:
                return 0

        if champ.get(post) in letters:
            return 0

        return 1

    @staticmethod
    def tagHighlight(champ):
        start = "1.0"
        end = "end"

        for mylist in Utils.WORDLIST:
            num = int(Utils.WORDLIST.index(mylist))

            for word in mylist:
                champ.mark_set("matchStart", start)
                champ.mark_set("matchEnd", start)
                champ.mark_set("SearchLimit", end)

                mycount = IntVar()

                while True:
                    index = champ.search(word, "matchEnd", "SearchLimit", count=mycount, regexp=False)

                    if index == "": break
                    if mycount.get() == 0: break

                    champ.mark_set("matchStart", index)
                    champ.mark_set("matchEnd", "%s+%sc" % (index, mycount.get()))

                    preIndex = "%s-%sc" % (index, 1)  # placeholder ( un peu comme en C )
                    postIndex = "%s+%sc" % (index, mycount.get())

                    if Utils.check(champ, index, preIndex, postIndex):
                        champ.tag_add(Utils.TAGS[num], "matchStart", "matchEnd")
                    else:
                        champ.tag_add(Utils.TAGS[6], "matchStart", "matchEnd")

    @staticmethod
    def scan(champ):
        start = "1.0"
        end = "end"
        mycount = IntVar()

        regex_patterns = [r'%.*', r'$(\w+)$']  # pour les commentaires

        for pattern in regex_patterns:
            champ.mark_set("start", start)
            champ.mark_set("end", end)

            num = int(regex_patterns.index(pattern))

            while True:
                index = champ.search(pattern, "start", "end", count=mycount, regexp=True)

                if index == "": break

                if (num == 0):
                    champ.tag_add(Utils.TAGS[5], index, index + " lineend")
                if (num == 1):
                    champ.tag_add(Utils.TAGS[3], index, index)

                champ.mark_set("start", "%s+%sc" % (index, mycount.get()))

    @staticmethod
    def configureColor(champ):
        champ.tag_configure("orange", foreground="#F97718", font="Helvetica 10")
        champ.tag_configure("yellow", foreground="#FD00B0", font="Helvetica 10")
        champ.tag_configure("blue", foreground="blue", font="Helvetica 10")
        champ.tag_configure("green", foreground="green", font="Helvetica 10")
        champ.tag_configure("red", foreground="red", font="Helvetica 10")
        champ.tag_configure("purple", foreground="#00AF7A", font="Helvetica 10")
        champ.tag_configure("white", foreground="black", font="Helvetica 10")

    @staticmethod
    def updateCode(champ):
        Utils.tagHighlight(champ)
        Utils.scan(champ)

    @staticmethod
    def open_file(champ):  # fonction permettant d'ouvrir un fichier de préférences
        try:
            filepath = askopenfilename(filetypes=[("Document Tex", "*.tex")])
        except _tkinter.TclError:
            exit()
            return

        if not filepath:
            return
        if champ:
            champ.delete(1.0, END)

            with codecs.open(filepath, "r", encoding="utf-8", errors='replace') as input_file:
                text = input_file.read()
                champ.insert(END,text)
                Utils.updateCode(champ)
