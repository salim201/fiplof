# -*- coding: utf-8 -*-
import psycopg2
import psycopg2.extras


class Projet:

    def __init__(self):
        self.idprojet = None
        self.date_lancement = None
        self.date_premier_import = None
        self.date_dernier_import = None
        self.langue = None
        self.nom = None
        self.datemaj = None
    
    # -------------------------
    # MAP RESULT DB → OBJ
    # -------------------------
    def map(self, res):
        if not res:
            return

        self.idprojet = res["idprojet"]
        self.date_lancement = res["date_lancement"]
        self.date_premier_import = res["date_premier_import"]
        self.date_dernier_import = res["date_dernier_import"]
        self.langue = res["langue"]
        self.nom = res["nom"]
        self.datemaj = res["datemaj"]


    @staticmethod
    def getFirstProjetId(connection):
        """
        Retourne l'id du premier projet (le plus petit idprojet)
        """
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT idprojet
                FROM public.projet
                ORDER BY idprojet ASC
                LIMIT 1
            """)

            result = cursor.fetchone()

            if result:
                return result[0]
            return None

        except Exception as e:
            print("Erreur getFirstProjetId:", str(e))
            return None

        finally:
            cursor.close()


    
    # -------------------------
    # FIND BY ID
    # -------------------------
    @staticmethod
    def find_by_id(connection, idprojet):

        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        try:
            cursor.execute("""
                SELECT *
                FROM projet
                WHERE idprojet = %s
            """, (idprojet,))

            row = cursor.fetchone()

            obj = Projet()
            obj.map(row)

            return obj

        except Exception as e:
            print("ERROR find_by_id Projet:", e)
            return None

        finally:
            cursor.close()

    # -------------------------
    # FIND BY NAME
    # -------------------------
    @staticmethod
    def find_by_name(connection, nom):

        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        try:
            cursor.execute("""
                SELECT *
                FROM projet
                WHERE trim(lower(nom)) = trim(lower(%s))
            """, (nom,))

            row = cursor.fetchone()

            if not row:
                return None

            obj = Projet()
            obj.map(row)

            return obj

        except Exception as e:
            print("ERROR find_by_name Projet:", e)
            return None

        finally:
            cursor.close()

    # -------------------------
    # INSERT
    # -------------------------
    @staticmethod
    def insert(connection, data):

        cursor = connection.cursor()

        try:
            cursor.execute("""
                INSERT INTO projet (
                    date_lancement,
                    date_premier_import,
                    date_dernier_import,
                    langue,
                    nom
                )
                VALUES (
                    %(date_lancement)s,
                    %(date_premier_import)s,
                    %(date_dernier_import)s,
                    %(langue)s,
                    %(nom)s
                )
                RETURNING idprojet
            """, data)

            idp = cursor.fetchone()[0]
            connection.commit()

            return idp

        except Exception as e:
            connection.rollback()
            print("ERROR INSERT Projet:", e)
            return None

        finally:
            cursor.close()