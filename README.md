# **Application**

L'application de génération de sujets est un programme réalisé dans le cadre de projets tutoré afin de permettre à des enseignants de faciliter la création de fiches d'exercices rédigé en LaTeX. Ce programme permet de générer des PDFs en suivant les raccourcis de plusieurs utilisateurs et de choisir les exercices utilisés pour la génération selon leur niveau de difficulté, la classe et le chapitre auxquels ils appartiennent.

# **Installation**
## Linux

### **Tkinter**

Tkinter est la bibliothèque graphique libre d'origine pour le langage Python, permettant la création d'interfaces graphiques. Elle vient d'une adaptation de la bibliothèque graphique Tk écrite pour Tcl. *(source : https://fr.wikipedia.org/wiki/Tkinter)*

**Installation**

    sudo apt-get install python-tk

### **TeX Live**

TeX Live est une distribution TeX libre visant à fournir un environnement TeX/LaTeX complet et prêt à utiliser, sous les principaux systèmes d’exploitation. Depuis la version 2008, elle inclut un gestionnaire de paquets permettant la mise à jour de ses composants depuis internet. *(source : https://fr.wikipedia.org/wiki/TeX_Live)*

**Installation**

    sudo apt install texlive

**Dépendance necessaire**

    sudo apt install texlive-lang-french texlive-latex-extra texlive-science

### **Lire un PDF**

Cette application de génération de feuilles d'exercices mathématiques nécessite un logiciel de lecture de fichiers PDF reconnu par xdg-open comme par exemple :

    chromium
    firefox
    iceweasel
    chrome
    edge
    ...

Il est possible d'utilisé l'application sans une telle application mais le programme n'ouvrira aucun fichier PDF par lui-même ( - n'affecte pas la génération).