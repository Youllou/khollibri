# -*- coding: utf-8 -*-
import sqlite3
import datetime

from SGBD.exceptions.SGBDException import SGBDException

"""
 Ce document constitue l'ensemble des fonctions permettant de manipuler la base de données.
 Certaines fonctions sont identiques et agissent juste sur une table différente 
 (exemple : SelectExo et SelectClassAppChap ou InsertExo et InsertClassAppChap ou ClearExo et ClearClassAppChap )
 Le cas échéant, seule une première version sera détaillée, en prenant compte, bien sûr, les différences pour certaines fonctions
"""


def SelectExo():# Récupère toutes les données de la table Exercice et les affiche dans le terminal

    try: # nécessité de mettre la connexion à la base dans une clause try et de renvoyer l'erreur
        conn = sqlite3.connect('SGBD/BDProjetTut.db') # la connexion à la base BDProjetTut.db créée un objet de type SQLite connexion
        sql = '''SELECT * FROM Exercice ;''' # la requête est stockée dans une variable
        cur = conn.cursor() # cursor() permet à l'objet SQLite d'effectuer des requêtes vers la base
        cur.execute(sql) # la méthode execute() permet de lancer la requête
        res = cur.fetchall() # le résultat est stocké sous forme de tableau associatif
        if (len(res) == 0):
            print("La table Exercice est vide")

        for row in res: # chaque ligne du tableau res est un tableau, chaque case du tableau correspond à une colonne de la table (cf modèle relationnel des tables )
            print("Idexo : ", row[0])
            print("Enonce : ", row[1])
            print("Corrige : ", row[2])
            print("Dateajout : ", row[3])
            print("Auteur : ", row[4])
            print("\n")
        cur.close() # fermeture du curseur
        conn.close() # fermeture de la connexion, elle ne dure que le temps d'une méthode

    except sqlite3.Error as error: # permet de catcher l'erreur et de l'afficher dans le terminal
        print("Erreur lors de la self.connexion à SQLite", error)


def InsertExo(Enonce, Corrige, Auteur): # permet d'ajouter dans la table Exercice des données par le biais de requêtes préparées
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        conn.execute("PRAGMA foreign_keys = ON")
        # nécessité de définir chaque colonne dans lesquelles nous allons ajouter
        # ( si la table nous le permet --> contraintes de la table) des données
        # Pour associer une données à une column nous insérons des '?' à l'emplacement de la donnée
        # et nous mettons en relation ces '?' avec la donnée passée en paramètre grâce à une variable
        sql = '''Insert into Exercice(enonce,corrige,dateajout,IdAuteur) values (?,?,?,?);'''
        cur = conn.cursor()
        time = datetime.date.today()
        data = [Enonce, Corrige, str(time), Auteur] # récupération des données pour les insérer dans l'ordre précis indiqué
        # ici, Enonce sera le premier '?' et donc ira dans la colonne enonce de la table
        # la colonne IdExo est gérée en autoincrement donc nous n'avons pas à gérer l'insertion dans cette colonne.
        cur.execute(sql, data) # execution de la requête avec le tableau de données à insérer
        conn.commit() # commit permet de valider l'insertion
        print("Nouvel enregistrement dans la table Exercice ajouté !")
        cur.close()
        conn.close()


    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)


def ClearExo(): # permet de nettoyer une table sans supprimer l'ordre des autoIncrements, explications:
    # si nous avons 3 enregistrement alors le dernier ID est le 3
    # clear la table va supprimer les données mais le prochain ID sera le 4 et non le 1
    # aucune action n'est réversible après le commit()
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        conn.execute("PRAGMA foreign_keys = ON")
        sql = '''Delete from Exercice ;'''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print("La table Exercice est désormais vide !")
        cur.close()
        conn.close()


    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)


def SelectClassAppChap(): # meme principe que SelectExo
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        sql = '''SELECT * FROM ClassAppChap;'''
        cur = conn.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        if (len(res) == 0):
            print("La table ClassAppChap est vide")

        for row in res:
            print("IdChap : ", row[0])
            print("IdClasse : ", row[1])
            print("NomChap : ", row[2])
            print("\n")
        cur.close()
        conn.close()



    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)


def InsertClassAppChap(Chap, Classe): # meme principe que InsertExo
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        conn.execute("PRAGMA foreign_keys = ON")
        sql = '''Insert into ClassAppChap(Nomchap,IdClasse) values (?,?);'''
        cur = conn.cursor()
        data = [Chap, Classe]
        cur.execute(sql, data)
        conn.commit()
        print("Nouvel enregistrement dans la table ClassAppChap ajouté !")
        cur.close()
        conn.close()

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)


def ClearClassAppChap(): # meme principe que ClearExo
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        conn.execute("PRAGMA foreign_keys = ON")
        sql = '''Delete from ClassAppChap ;'''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print("La table ClassAppChap est désormais vide !")
        cur.close()
        conn.close()
    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)


def SelectExoUtilChap(): # meme principe que SelectExo
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        sql = '''SELECT * FROM ExoUtilChap;'''
        cur = conn.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        if (len(res) == 0):
            print("La table ExoUtilChap est vide")

        for row in res:
            print("IdExo : ", row[0])
            print("IdChap : ", row[1])
            print("IdClasse : ", row[2])
            print("\n")
        return res
        cur.close()
        conn.close()

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)


def InsertExoUtilChap(Chap, Classe, IdExo): # meme principe que InsertExo
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        conn.execute("PRAGMA foreign_keys = ON")
        # la premiere value ajoutée sera dans la colonne IdExo, pour lier les tables nous recherchons la dernière
        # valeur ajoutée dans la table exercice avec Select IdExo from Exercice ORDER BY IdExo DESC limit 1
        # pour associer les chapitre et classes ajoutées
        cur = conn.cursor()

        if(IdExo==0):
            sql = '''Insert into ExoUtilChap(IdExo,NomChap,IdClasse) values ((Select IdExo from Exercice ORDER BY IdExo DESC limit 1),?,?);'''
            data = [Chap, Classe]
        else :
            sql = '''Insert into ExoUtilChap(IdExo,NomChap,IdClasse) values (?,?,?);'''
            data = [IdExo, Chap, Classe]
        cur.execute(sql, data)
        conn.commit()
        print("Nouvel enregistrement dans la classe ExoUtilChap ajouté !")
        cur.close()
        conn.close()


    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)


def ClearExoUtilChap(): # meme principe que ClearExo
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        conn.execute("PRAGMA foreign_keys = ON")
        sql = '''Delete from ExoUtilChap;'''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print("La table ExoUtilChap est désormais vide !")
        cur.close()
        conn.close()

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)


def SelectExoPossNiveau(): # meme principe que SelectExo
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        sql = '''SELECT * FROM ExoPossNiveau;'''
        cur = conn.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        if (len(res) == 0):
            print("La table ExoPossNiveau est vide")

        for row in res:
            print("IdExo : ", row[0])
            print("IdClasse : ", row[1])
            print("Niveau : ", row[2])
            print("\n")
        return res
        cur.close()
        conn.close()

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)


def InsertExoPossNiveau(Classe, Niv): # Meme principe que InsertExoUtilChap
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        conn.execute("PRAGMA foreign_keys = ON")
        sql = '''Insert into ExoPossNiveau(IdExo,IdClasse,Niveau) values ((Select IdExo from Exercice ORDER BY IdExo DESC limit 1),?,?);'''
        cur = conn.cursor()
        data = [Classe, Niv]
        cur.execute(sql, data)
        conn.commit()
        print("Nouvel enregistrement dans la table ExoPossNiveau ajouté !")
        cur.close()
        conn.close()


    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)


def ClearExoPossNiveau(): # meme principe que ClearExo
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        conn.execute("PRAGMA foreign_keys = ON")
        sql = '''Delete from ExoPossNiveau;'''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print("La table ExoPossNiveau est désormais vide !")
        cur.close()
        conn.close()

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)


def SelectShortcuts(): # meme principe que SelectExo
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        sql = '''SELECT * FROM Shortcuts;'''
        cur = conn.cursor()
        res = cur.execute(sql).fetchall()

        if (len(res) == 0):
            print("La table Shortcuts est vide")

        for row in res:
            print("Command : ", row[0])
            print("Auteur : ", row[1])
            print("Shortcut : ", row[2])
            print("\n")

        cur.close()
        conn.close()

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)
    #    raise SGBDException("Erreur lors de la connexion à la base de données.")


def InsertShortcuts(command, autor, shortcut): # meme principe que SelectExo
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        conn.execute("PRAGMA foreign_keys = ON")
        sql = '''Insert into Shortcuts(command,IdAuteur,shortcut) values (?,?,?);'''
        cur = conn.cursor()
        data = [command, autor, shortcut]
        cur.execute(sql, data)
        conn.commit()
        print("Nouvel enregistrement dans la table Shortcuts ajouté !")
        cur.close()
        conn.close()


    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)
        print(error.__class__)
        if error.__class__ == sqlite3.IntegrityError:
            raise SGBDException("L'auteur et/ou la préférence existe(nt) déjà.")
        else:
            raise SGBDException("La préférence n'a pas pu être ajoutée.")


def ClearShortcuts(): # meme principe que ClearExo
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        conn.execute("PRAGMA foreign_keys = ON")
        sql = '''Delete from Shortcuts;'''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print("La table Shortcuts est désormais vide !")
        cur.close()
        conn.close()

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)


def Createtables(): # permet de recréer les tables, seule la table ClassAppChap n'est jamais supprimer et donc recréer
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')

        conn.execute('''CREATE TABLE IF NOT EXISTS AUTEUR(
                                IdAuteur TEXT NOT NULL PRIMARY KEY,
                                 Etablissement TEXT,
                                 BlackList TEXT );''')

        conn.execute('''CREATE TABLE IF NOT EXISTS CLASSE(
                            IdClasse TEXT NOT NULL PRIMARY KEY,
                            Annee TEXT NOT NULL);''')

        conn.execute('''    CREATE TABLE IF NOT EXISTS ClassAppChap(
                                                IdChap    INTEGER NOT NULL,
                                                NomChap   TEXT NOT NULL UNIQUE,
                                                IdClasse  TEXT NOT NULL REFERENCES CLASSE("IdClasse") ON DELETE CASCADE,
                                                PRIMARY KEY("IdChap" AUTOINCREMENT));''')

        conn.execute('''CREATE TABLE IF NOT EXISTS Shortcuts(
                                            Command   TEXT NOT NULL,
                                            IdAuteur    TEXT NOT NULL REFERENCES AUTEUR(IdAuteur) ON DELETE CASCADE,
                                            Shortcut  TEXT NOT NULL,
                                            PRIMARY KEY("IdAuteur","Shortcut"));''')

        conn.execute('''    CREATE TABLE IF NOT EXISTS Exercice(
                                    IdExo INTEGER NOT NULL,
                                    Enonce    TEXT NOT NULL UNIQUE,
                                    Corrige  TEXT NOT NULL UNIQUE,
                                    DateAjout TEXT NOT NULL,
                                    IdAuteur TEXT NOT NULL REFERENCES AUTEUR(IdAuteur) ON DELETE CASCADE,
                                    PRIMARY KEY("IdExo" AUTOINCREMENT));''')

        conn.execute('''    CREATE TABLE IF NOT EXISTS "ExoPossNiveau" (
                                    IdExo INTEGER NOT NULL REFERENCES "Exercice"("IdExo") ON DELETE CASCADE,
                                    IdClasse TEXT NOT NULL REFERENCES CLASSE("IdClasse") ON DELETE CASCADE,
                                    Niveau INTEGER NOT NULL,
                                    PRIMARY KEY("IdExo", "IdClasse"));''')

        conn.execute('''CREATE TABLE IF NOT EXISTS "ExoUtilChap" (
                                    IdExo INTEGER NOT NULL REFERENCES "Exercice"("IdExo") ON DELETE CASCADE,
                                    IdClasse TEXT NOT NULL REFERENCES CLASSE("IdClasse") ON DELETE CASCADE,
                                    NomChap   TEXT NOT NULL REFERENCES "ClassAppChap"("NomChap") ON DELETE CASCADE,
                                    PRIMARY KEY("IdExo","NomChap") );''')


        conn.commit()
        print("Nouvelles tables créées !")
        conn.close()

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)
def Droptables():# Permet de supprimer définitivement les tables, toutes les données, y compris les autoincrements
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        conn.execute("PRAGMA foreign_keys = ON")

        sql0 = '''Drop table ClassAppChap;'''

        sql = ''' Drop table Exercice;'''


        """
        sql2 = ''' Drop table ExoPossNiveau;'''
        """
        # exemple de suppresion de table
        sql3 = ''' Drop table ExoUtilChap;'''
        """
        """
        sql4='''Drop table Shortcuts;'''


        cur = conn.cursor()

        cur.execute(sql0)
        cur.execute(sql4)

        conn.commit()
        print("Table supprimée !")
        cur.close()
        conn.close()

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)


def giveEnonce(idExo): # renvoi l'enonce pour un idExo donné
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        sql = '''Select enonce from Exercice  where IdExo=?; ''' # option de requete avec where
        conn.row_factory = lambda cursor, row: row[0] # transforme un tableau de liste en tableau à une valeur
        data = [idExo]
        cur = conn.cursor()
        cur.execute(sql, data)
        res = cur.fetchall()
        cur.close()
        conn.close()
        return res

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)


def giveCorrige(idExo): # meme principe que giveEnonce pour le corrige cette fois
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        sql = '''Select corrige from Exercice  where IdExo=?; '''
        conn.row_factory = lambda cursor, row: row[0]
        data = [idExo]
        cur = conn.cursor()
        cur.execute(sql, data)
        res = cur.fetchall()
        cur.close()
        conn.close()
        return res

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)


def giveChap(Classe): # récupère l'ensemble des chapitres présent dans une classe donnée
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        sql = '''Select NomChap from ClassAppChap where IdClasse= ?; '''
        conn.row_factory = lambda cursor, row: row[0] # transforme la liste de liste en tableau
        data = [Classe]
        cur = conn.cursor()
        res = cur.execute(sql, data, ).fetchall()
        cur.close()
        conn.close()
        print(res)
        return res

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)


def giveClasse(): # donne les différentes classes présentes dans la base

    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        sql = '''Select DISTINCT IdClasse from ClassAppChap  ; ''' # DISTINCT evite les doublons
        conn.row_factory = lambda cursor, row: row[0]
        cur = conn.cursor()
        res = cur.execute(sql).fetchall()
        cur.close()
        conn.close()

        return res

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)

def giveAuteur(): # meme principe que giveClasse pour les auteurs
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        sql = '''Select DISTINCT IdAuteur from Shortcuts  ; '''
        conn.row_factory = lambda cursor, row: row[0]
        cur = conn.cursor()
        res = cur.execute(sql).fetchall()
        cur.close()
        conn.close()

        return res

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)

def GivePrefFromAutor(autor): # récupère tous les raccourcis et leur commandes pour un auteur donné
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        sql = '''Select command,shortcut from Shortcuts where IdAuteur=?  ; '''
        cur = conn.cursor()
        data = [autor]
        res = cur.execute(sql,data).fetchall()
        cur.close()
        conn.close()

        return res

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)

def ModifyShortcutToCommand(enonce, autor, corrige): # modifie les enonces et les corriges pour enlever les raccourcis d'un auteur.
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        conn.execute("PRAGMA foreign_keys = ON")
        sql = '''Select Command,Shortcut from Shortcuts where IdAuteur=?  ''' # recupère tous les énoncés d'un auteurs
        cur = conn.cursor()
        data = [autor]
        res = cur.execute(sql, data).fetchall()
        for var in res: # pour chaque couple (raccourcis,commande) nous remplaçons le raccourcis ( s'il est présent ) par la commande
            enonce = enonce.replace(var[1], var[0])
            corrige = corrige.replace(var[1], var[0])


        return enonce, corrige
        cur.close()
        conn.close()
        print("Exercice modifié")

        return enonce, corrige
    except sqlite3.Error as error:
        print("Erreur lors de la modification : ", error)

def ModifyCommandToShortcut(enonce, autor, corrige): # meme principe que ModifyShortcutToCommand mais dans le sens invers
                                                    # pour pouvoir afficher un exercice avec les raccourcis d'un auteur
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        conn.execute("PRAGMA foreign_keys = ON")
        sql = '''Select Shortcut,Command from Shortcuts where IdAuteur=?  '''
        cur = conn.cursor()
        data = [autor]
        res = cur.execute(sql, data).fetchall()
        for var in res:
            enonce = enonce.replace(var[1], var[0])
            corrige = corrige.replace(var[1], var[0])


        return enonce, corrige
        cur.close()
        conn.close()
        print("Exercice modifié")

        return enonce, corrige
    except sqlite3.Error as error:
        print("Erreur lors de la modification : ", error)

def ModifyExo(IdExo,enonce,corrige): # permet de modifier l'enoncé et le corrigé depuis la page AfficherExo
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        conn.execute("PRAGMA foreign_keys = ON")
        sql = '''Update Exercice set enonce=?, corrige=? where IdExo=?;''' # requete Update...set pour modifier
        cur = conn.cursor()
        data=[enonce,corrige,IdExo]
        cur.execute(sql,data)
        conn.commit()
        cur.close()
        conn.close()

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)


def CreateTableTempChap(): # table temporaire pour les chapitres sélectionés lors des étapes de la génération de feuille
    # pour plus d'informations, voir les commentaires sur la fonction GiveExoFromSelect
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        sql = '''CREATE TABLE IF NOT EXISTS "TempQueryChap" ("Chaps"  TEXT NOT NULL );'''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print("TableChap temporaire créée !")
        cur.close()
        conn.close()

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)

def InsertTableTempChap(chap): # meme principe que InsertExo
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        sql = '''Insert into TempQueryChap(Chaps) values (?)'''
        data = [chap]
        cur = conn.cursor()
        cur.execute(sql,data)
        conn.commit()
        print("Insertion TableChap temporaire réussi !")
        cur.close()
        conn.close()

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)

def giveTempChap():
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        sql = '''SELECT Chaps from TempQueryChap;'''
        conn.row_factory = lambda cursor, row: row[0]
        cur = conn.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        cur.close()
        conn.close()
        return res
    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)

def DropTableTempChap(): # la table temporaire est obligatoirement supprimée après la recherche d'exercice
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        sql = ''' Drop table TempQueryChap;'''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print("TableChap temporaire supprimée !")
        cur.close()
        conn.close()

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)

def ClearTableTempChap():
    DropTableTempChap()
    CreateTableTempChap()

def CreateTableTempLevels(): # meme principe avec la table temporaire CreateTableTempChap
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        sql = '''CREATE TABLE "TempQueryLevels" ("Levels" INTEGER NOT NULL );'''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print("TableLevel temporaire créée !")
        cur.close()
        conn.close()

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)

def ClearTableTempLevels(): # la table levels est clear pour insérer de nouveaux niveau par rapport a la quantité d'exercices sélectionés:
    # explications : un utilisateur peut selectionner 3 exercice de niveau 1-2 puis 2 exercices de niveau 3-4
    # ainsi, pour la première boucle avec la quantité 3, la table TempQueryLevels comporte les niveaux 1-2
    # puis la table est vidée pour accueillir les deux lignes 3-4 pour la quantité 2
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        sql = '''Delete from TempQueryLevels '''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)


def InsertTableTempLevels(Niv): # meme principe que InsertExo
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        conn.execute("PRAGMA foreign_keys = ON")
        sql = '''Insert into TempQueryLevels(Levels) values (?)'''
        data = [Niv]
        cur = conn.cursor()
        cur.execute(sql,data)
        conn.commit()
        print("Insertion TableLevel temporaire réussi !")
        cur.close()
        conn.close()

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)

def DropTableTempLevels(): # meme principe que DropTableTempChap
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        sql = ''' Drop table TempQueryLevels;'''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print("TableLevel temporaire supprimée !")
        cur.close()
        conn.close()

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)


def GiveExoFromSelect(): # fonction qui permet la recherche aléatoire des exercices dans la table
    # selon les critères de selection des exercices, voir fin de page pour les explications de la recherche.

    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        sql = '''Select DISTINCT IdExo,enonce,corrige from Exercice 
                   where idexo IN (SELECT DISTINCT ExoUtilChap.IdExo from ExoUtilChap 
                                   WHERE ExoUtilChap.nomchap in (SELECT DISTINCT Chaps from TempQueryChap) )                
                   AND idexo IN (Select DISTINCT ExoPossNiveau.IdExo from ExoPossNiveau 
                                 where ExoPossNiveau.Niveau in (SELECT DISTINCT Levels from TempQueryLevels) 
                                 ANd ExoPossNiveau.IdClasse in (Select ClassAppChap.IdClasse from ClassAppChap 
                                                               where ClassAppChap.nomchap in (SELECT DISTINCT Chaps from TempQueryChap)  ))
                   ORDER BY random()'''

        cur = conn.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        if (len(res) == 0):
            print("La table Exercice est vide")
        cur.close()
        conn.close()
        return res

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)

    # la requete commence par selectionner des données lorsque l'idExo est présent dans les chapitres sélectionnés.
    # Mais il nous faut aussi s'assurer que les niveaux selectionnés soient présents dans les niveaux sélectionnés .
    # Un niveau dépend d'une classe donc nous avons besoin de selectionner les classes correspondant aux chapitres sélectionnés
    # Pour selectionner des données parmis une liste de données, on ne peut pas faire " Selection data1 where data2 in (datax,datax1,datax2,etc.)"
    # avec des requetes préparés comme pour les autres requetes présentes dans le fichiers.
    # Nous faisons donc une requete SQL à la place d'une liste : "... where data2 in (Select data ....) "

    def InsertAUTEUR(auteur):
        try:
            conn = sqlite3.connect('SGBD/BDProjetTut.db')
            conn.execute("PRAGMA foreign_keys = ON")
            sql = ''' Insert into AUTEUR(IdAuteur) VALUES(?);'''
            cur = conn.cursor()
            data = [auteur]
            cur.execute(sql,data)
            conn.commit()
            cur.close()
            conn.close()

        except sqlite3.Error as error:
            print("Erreur lors de la self.connexion à SQLite", error)


def InsertCLASSE(classe):
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        conn.execute("PRAGMA foreign_keys = ON")
        sql = ''' Insert into CLASSE(IdClasse,Annee) VALUES(?,'2022-2023');'''
        cur = conn.cursor()
        data = [classe]
        cur.execute(sql, data)
        conn.commit()
        cur.close()
        conn.close()

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)


def SupprimerClasse(classe):
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        conn.execute("PRAGMA foreign_keys = ON")
        sql = ''' DELETE FROM CLASSE WHERE IdClasse=?;'''
        cur = conn.cursor()
        data = [classe]
        cur.execute(sql, data)
        conn.commit()
        cur.close()
        conn.close()

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)

def SupprimerAuteur(auteur):
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        conn.execute("PRAGMA foreign_keys = ON")
        sql = '''DELETE FROM AUTEUR WHERE IdAuteur=?;'''
        cur = conn.cursor()
        data = [auteur]
        cur.execute(sql, data)
        conn.commit()
        cur.close()
        conn.close()

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)

def SupprimerChap(chap):
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        conn.execute("PRAGMA foreign_keys = ON")
        sql = ''' DELETE FROM ClassAppChap WHERE NomChap=?;'''
        cur = conn.cursor()
        data = [chap]
        cur.execute(sql, data)
        conn.commit()
        cur.close()
        conn.close()

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)


def RetirerExoChap(idExo,chap):
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        conn.execute("PRAGMA foreign_keys = ON")
        sql = ''' DELETE FROM ExoUtilChap where IdExo=? and NomChap=?;'''
        cur = conn.cursor()
        data = [idExo,chap]
        cur.execute(sql, data)
        conn.commit()
        cur.close()
        conn.close()

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)

def RetirerExoClasse(idExo,classe):
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        conn.execute("PRAGMA foreign_keys = ON")
        sql = ''' DELETE FROM ExoUtilChap where IdExo=? and IdClasse=?;'''
        cur = conn.cursor()
        data = [idExo,classe]
        cur.execute(sql, data)
        conn.commit()
        cur.close()
        conn.close()

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)


def fusion(newchap, classe):
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        # on récupère tous les idexos concernés
        listexo = conn.execute(''' select DISTINCT ExoUtilChap.IdExo from ExoUtilChap where ExoUtilChap.NomChap in (SELECT * FROM TempQueryChap)''').fetchall()
        datainsert = [classe,newchap] # le couple de données qui change pas pour l'insertion
        conn.execute("PRAGMA foreign_keys = ON")

        for exo, in listexo:
            datainsert.insert(0,exo)
            print(datainsert)
            conn.execute("PRAGMA foreign_keys = ON")
            sqlinsert = '''Insert into ExoUtilChap(IdExo,IdClasse,NomChap) values (?,?,?) '''
            cur.execute(sqlinsert, datainsert)
            datainsert.pop(0)

        sqldelete = '''Delete from ClassAppChap where NomChap in (SELECT * FROM TempQueryChap )'''
        cur.execute(sqldelete)
        conn.commit()
        cur.close()
        conn.close()

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)

def GiveExoFromChap(IdExo):
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        cur = conn.cursor()

        sql = '''SELECT  DISTINCT ExoUtilChap.NomChap, ExoPossNiveau.IdClasse, ExoPossNiveau.Niveau from ExoUtilChap,ExoPossNiveau where ExoPossNiveau.IdExo=? 
        AND ExoPossNiveau.IdClasse=ExoUtilChap.IdClasse 
        and ExoUtilChap.NomChap In (select ExoUtilChap.NomChap from ExoUtilChap where idexo=?)'''

        data = [IdExo, IdExo]
        res = cur.execute(sql, data)

        sortie = {}

        for row in res :
            if not sortie.get(row[1]) :
                sortie[row[1]] = [[row[0]], row[2]]
            else :
                sortie[row[1]][0].append(row[0])

        conn.commit()
        cur.close()
        conn.close()

        return sortie

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)

def ModifyNiveau(IdExo, Classe, newDiff):
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        cur = conn.cursor()
        sql = '''UPDATE ExoPossNiveau set Niveau=? where IdClasse=? and IdExo=?'''
        data = [newDiff, Classe, IdExo]
        res = cur.execute(sql, data)
        conn.commit()
        cur.close()
        conn.close()

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)

def SelectNotInChaps(IdExo):
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        cur = conn.cursor()
        sql = '''Select Cl.nomchap, Cl.idclasse from ClassAppChap AS Cl where Cl.NomChap not in (select Exo.nomchap from ExoUtilChap AS Exo where Exo.IdExo=?)'''
        data = [ IdExo]
        res = cur.execute(sql, data)

        sortie = {}

        for row in res :
            if not sortie.get(row[1]) :
                sortie[row[1]] = [row[0]]
            else :
                sortie[row[1]].append(row[0])

        conn.commit()
        cur.close()
        conn.close()

        return sortie

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)

def ExoIdStock() :
    try :
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        sql = '''Select DISTINCT IdExo from Exercice  ; ''' # DISTINCT evite les doublons
        conn.row_factory = lambda cursor, row: row[0]
        cur = conn.cursor()
        res = cur.execute(sql).fetchall()
        cur.close()
        conn.close()

        return res

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)

def Exportdb():
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        cur = conn.cursor()
        sql = '''SELECT  DISTINCT  Exercice.Enonce, Exercice.Corrige, ExoUtilChap.NomChap, ExoPossNiveau.IdClasse, ExoPossNiveau.Niveau from Exercice,ExoUtilChap,ExoPossNiveau 
                    where ExoPossNiveau.IdExo in (select DISTINCT Exercice.IdExo from Exercice)
		            AND ExoPossNiveau.idexo=Exercice.IdExo
                    AND ExoPossNiveau.IdClasse=ExoUtilChap.IdClasse 
                    and ExoUtilChap.NomChap In (select ExoUtilChap.NomChap from ExoUtilChap where idexo in (select DISTINCT Exercice.IdExo from Exercice)) '''
        res = cur.execute(sql)

        sortie = {}

        for row in res :
            if not sortie.get(row[1]) :
                sortie[row[1]] = [row[0]]
            else :
                sortie[row[1]].append(row[0])

        conn.commit()
        cur.close()
        conn.close()

        return sortie

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)

def AddBlackList(IdAuteur, IdExo):
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        conn.row_factory = lambda cursor, row: row[0]
        cur = conn.cursor()
        data =[IdAuteur]
        sqlsearch = '''Select BlackList from AUTEUR where IdAuteur=?'''
        sqlintsert = '''Update Auteur set Blacklist=? where IdAuteur=?'''
        cur.execute(sqlsearch, data)
        res2 = cur.fetchall()
        if (res2[0]==None):
            data = [IdExo, IdAuteur]
            cur.execute(sqlintsert, data)
        else:
            newres = res2[0] + " "+ IdExo
            data = [newres,IdAuteur]
            cur.execute(sqlintsert, data)
        conn.commit()

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)


def giveBlacklist(IdAuteur):
    try:
        conn = sqlite3.connect('SGBD/BDProjetTut.db')
        conn.row_factory = lambda cursor, row: row[0]
        cur = conn.cursor()
        sql = '''Select BlackList from AUTEUR where IdAuteur=?'''
        data = [IdAuteur]
        res = cur.execute(sql, data).fetchall()
        print(res)
        cur.close()
        conn.close()

    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)

    """
    commentaire pour faire 1000 lignes
    """
