import codecs
import json
from tkinter import messagebox, ttk
from tkinter.filedialog import askopenfilename
from SGBD.SGBD import *
from tkinter import *


class importBase(Frame):

    def __init__(self, parent, controller):

        file = askopenfilename(filetypes=[('Database JSON file', '*.json')])
        if file:

            Frame.__init__(self, parent)
            self.controller = controller

            arbre = ttk.Treeview(self)
            arbre.pack()

            with codecs.open(file, "r", encoding="utf-8", errors='replace') as input_file:
                entree = json.loads(input_file.read())

                try:

                    for i in entree["Classes"]:

                        root1 = arbre.insert("", 0, text=i)

                        for j in giveChap(i):

                            arbre.insert(root1, 0, text=j)

                except:
                    pass


def Destroy(frame):
    for widget in frame.winfo_children():
        widget.pack_forget()
