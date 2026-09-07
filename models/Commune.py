import psycopg2
import psycopg2.extras

class Commune:
    def __init__(self):
        self.idcommune, self.iddistrict, self.codecommune, self.nomcommune,self.maire = "", "", "", "", ""

    @staticmethod
    def findById(connection, idcommune):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT * FROM commune  WHERE idcommune=%s", (idcommune,))
            res = cursor.fetchone()
            t = Commune()
            t.map(res)
            return t
        except Exception as e:
            print(e)
        cursor.close()
        return None

    def map(self, res):
        self.idcommune, self.iddistrict, self.codecommune, self.nomcommune, self.maire = \
        res["idcommune"], res["iddistrict"], res["codecommune"], res["nomcommune"], res["maire"]


    @staticmethod
    def findByName(connection, nom_commune):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        print('DEBUG: Commune', nom_commune)
        try:
            cursor.execute(
                """
                SELECT *
                FROM commune
                WHERE UPPER(TRIM(nomcommune)) = UPPER(TRIM(%s))
                """,
                (nom_commune,)
            )

            res = cursor.fetchone()

            if res is None:
                return None

            commune = Commune()
            commune.map(res)
            return commune

        except Exception as e:
            print("[Commune.findByName] erreur:", e)
            return None

        finally:
            cursor.close()
