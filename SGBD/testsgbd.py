import sqlite3

def Createtables(): # permet de recréer les tables, seule la table ClassAppChap n'est jamais supprimer et donc recréer
    try:
        conn = sqlite3.connect('TEST.db')

        conn.execute('''CREATE TABLE IF NOT EXISTS AUTEUR(
                        IdAuteur TEXT NOT NULL PRIMARY KEY );''')

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
        conn.close()
    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)

def insert():
    try:
        conn = sqlite3.connect('TEST.db')

        conn.execute("PRAGMA foreign_keys = ON")
     #   print("                     Insertion d'auteurs : ")
        conn.execute('''Insert into AUTEUR(IdAuteur) VALUES ('Damien Gobin')''')
        conn.execute('''Insert into AUTEUR(IdAuteur) VALUES ('Leray')''')

      #  print("                     Insertion de raccourcis : ")
        conn.execute('''Insert into Shortcuts(command,IdAuteur,shortcut)VALUES ('commande1','Damien Gobin','raccourcis1') ''')
        conn.execute('''Insert into Shortcuts(command,IdAuteur,shortcut)VALUES ('commande2','Leray','raccourcis2') ''')

      #  print("                     Insertion d'exercice : ")
        conn.execute('''Insert into Exercice(Enonce,Corrige,DateAjout,IdAuteur) VALUES('enonce1','corrige1','2022','Damien Gobin')''')
        conn.execute('''Insert into Exercice(Enonce,Corrige,DateAjout,IdAuteur) VALUES('enonce2','corrige2','2022','Leray')''')
        conn.execute('''Insert into Exercice(Enonce,Corrige,DateAjout,IdAuteur) VALUES('enonce3','corrige3','2022','Damien Gobin')''')


      #  print("                     Insertion de Classe : ")
        conn.execute('''Insert into CLASSE(IdClasse,Annee) VALUES('MPSI','2022')''')
        conn.execute('''Insert into CLASSE(IdClasse,Annee) VALUES('BCPST','2022')''')

       # print("                     Insertion de Chap : ")
        conn.execute('''Insert into ClassAppChap(NomChap,IdClasse) VALUES('Chap1','MPSI')''')
        conn.execute('''Insert into ClassAppChap(NomChap,IdClasse) VALUES('Chap2','BCPST')''')

      #  print("                     Insertion dans ExoUtilChap : ")
        conn.execute('''Insert into ExoUtilChap(IdExo,IdClasse,NomChap) VALUES('1','MPSI','Chap1')''')
        conn.execute('''Insert into ExoUtilChap(IdExo,IdClasse,NomChap) VALUES('2','BCPST','Chap2')''')
        conn.execute('''Insert into ExoUtilChap(IdExo,IdClasse,NomChap) VALUES('3','BCPST','Chap2')''')



       # print("                     Insertion dans ExoPossNiveau : ")
        conn.execute('''Insert into ExoPossNiveau(IdExo,IdClasse,Niveau) VALUES('1','MPSI','1')''')
        conn.execute('''Insert into ExoPossNiveau(IdExo,IdClasse,Niveau) VALUES('2','BCPST','2')''')
        conn.execute('''Insert into ExoPossNiveau(IdExo,IdClasse,Niveau) VALUES('3','BCPST','4')''')



        res = conn.execute('''Select * from AUTEUR''')
        print("Données présentes dans la table AUTEUR : ")
        for row in res:
            print("                     "+str(row))

        res = conn.execute('''Select * from Shortcuts''')
        print("Données présentes dans la table Shortcuts : ")
        for row in res:
            print("                     "+str(row))

        res = conn.execute('''Select * from Exercice''')
        print("Données présentes dans la table Exercice : ")
        for row in res:
            print("                     " + str(row))

        res = conn.execute('''Select * from CLASSE''')
        print("Données présentes dans la table CLASSE : ")
        for row in res:
            print("                     " + str(row))

        res = conn.execute('''Select * from ClassAppChap''')
        print("Données présentes dans la table ClassAppChap : ")
        for row in res:
            print("                     " + str(row))

        res = conn.execute('''Select * from ExoUtilChap''')
        print("Données présentes dans la table ExoUtilChap : ")
        for row in res:
            print("                     " + str(row))

        res = conn.execute('''Select * from ExoPossNiveau''')
        print("Données présentes dans la table ExoPossNiveau : ")
        for row in res:
            print("                     " + str(row))



        conn.commit()
        conn.close()
    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)


def delete():
    try:
        conn = sqlite3.connect('TEST.db')
        conn.execute("PRAGMA foreign_keys = ON")

        conn.execute('''Delete from AUTEUR where IdAuteur='Leray' ''')
        print("Auteur Leray supprimé ! ")
        res = conn.execute('''Select * from AUTEUR''')
        print("Données présentes dans la table AUTEUR : ")
        for row in res:
            print("                     "+str(row))

        res = conn.execute('''Select * from Shortcuts''')
        print("Données présentes dans la table Shortcuts : ")
        for row in res:
            print("                     "+str(row))

        res = conn.execute('''Select * from Exercice''')
        print("Données présentes dans la table Exercice : ")
        for row in res:
            print("                     " + str(row))

        conn.execute('''DELETE FROM CLASSE WHERE IdClasse='MPSI' ''')
        print("Classe MSPI supprimée !")
        res = conn.execute('''Select * from CLASSE''')
        print("Données présentes dans la table CLASSE : ")
        for row in res:
            print("                     " + str(row))

        res = conn.execute('''Select * from ClassAppChap''')
        print("Données présentes dans la table ClassAppChap : ")
        for row in res:
            print("                     " + str(row))

        res = conn.execute('''Select * from ExoUtilChap''')
        print("Données présentes dans la table ExoUtilChap : ")
        for row in res:
            print("                     " + str(row))

        res = conn.execute('''Select * from ExoPossNiveau''')
        print("Données présentes dans la table ExoPossNiveau : ")
        for row in res:
            print("                     " + str(row))
        conn.commit()
        conn.close()
    except sqlite3.Error as error:
        print("Erreur lors de la self.connexion à SQLite", error)



Createtables()
insert()
delete()