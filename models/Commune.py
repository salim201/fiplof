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
