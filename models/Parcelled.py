import psycopg2
import psycopg2.extras


class Parcelled:
    def __init__(self):
        self.gid, self.numdemande, self.surface = "", "", 0

    def map(self, res):
        self.gid, self.numdemande, self.surface = \
            res['gid'], res['numdemande'], res['sf']

    @staticmethod
    def find_by_numdemande(connection, num):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT gid, numdemande, st_area(geom) as sf FROM parcelle_d  "
                           "WHERE trim(numdemande)=%s", (num.strip(),))
            res = cursor.fetchone()
            t = Parcelled()
            t.map(res)
            return t
        except Exception as e:
            print(e)
        cursor.close()
        return None

    #arivola 05-03-2023
    @staticmethod
    def find_idby_numdemande(connection, num):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT iddemande, pd.gid  FROM demande as d INNER JOIN parcelle_d as pd ON d.gid=pd.gid"
                                " WHERE d.numdemande =%s", (str(num),))
            res = cursor.fetchone()
            return res
        except Exception as e:
            print(e)
        cursor.close()
        return None

    #arivola 13-05-2026
    @staticmethod
    def insert_parcelle_d_by_interrop(connection, data):
        """
        data = dict venant de ton JSON API
        """
        print("DEBUG  insert_parcelle_d_by_interrop ", data)
        cursor = connection.cursor()

        try:
            query = """
                INSERT INTO parcelle_d (
                    codeparcelle,
                    commune,
                    district,
                    region,
                    fkt,
                    idhameau,
                    consistance,
                    categorie,
                    id_commune,
                    geom,
                    surface
                )
                VALUES (
                    %(parcelle)s,
                    %(commune)s,
                    %(district)s,
                    %(region)s,
                    %(fkt)s,
                    %(id_hameau)s,
                    %(consistance)s,
                    %(categorie)s,
                    %(id_commune)s,

                    ST_SetSRID(
                        ST_GeomFromWKB(
                            decode(%(geom)s, 'hex')
                        ),
                        29702
                    ),

                    ST_Area(
                        ST_SetSRID(
                            ST_GeomFromWKB(
                                decode(%(geom)s, 'hex')
                            ),
                            29702
                        )
                    )
                )
                RETURNING gid
                """

            cursor.execute(query, data)

            gid = cursor.fetchone()[0]
            connection.commit()
            print("DEBUG  gid ", gid)

            return gid

        except Exception as e:
            connection.rollback()
            print("INSERT ERROR parcelle_d:", str(e))
            return None

        finally:
            cursor.close()


    @staticmethod
    def updateNumDemande(connection, gid, numdemande):

        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        )
        try:
            sql = """
                UPDATE parcelle_d
                SET numdemande = %s
                WHERE gid = %s
            """
            cursor.execute(sql, (
                numdemande,
                gid
            ))
            connection.commit()
            print("INFO : updateNumDemande EFFECTUE")
            return True
        except Exception as e:
            connection.rollback()
            print("Erreur updateNumDemande :", e)
        finally:
            cursor.close()
        return False
