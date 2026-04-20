import psycopg2
import psycopg2.extras

class Region:
    def __init__(self):
        self.idregion, self.coderegion, self.nomregion = "", "", ""

    @staticmethod
    def findById(connection, idregion):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT * FROM region  WHERE idregion=%s", (idregion,))
            res = cursor.fetchone()
            t = Region()
            t.map(res)
            return t
        except Exception as e:
            print(e)
        cursor.close()
        return None

    def map(self, res):
        self.idregion, self.coderegion, self.nomregion = \
        res["idregion"], res["coderegion"], res["nomregion"]
