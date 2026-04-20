import psycopg2
import psycopg2.extras

class District:
    def __init__(self):
        self.idregion, self.iddistrict, self.codedistrict, self.nomdistrict = "", "", "", ""

    @staticmethod
    def findById(connection, iddistrict):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT * FROM district  WHERE iddistrict=%s", (iddistrict,))
            res = cursor.fetchone()
            t = District()
            t.map(res)
            return t
        except Exception as e:
            print(e)
        cursor.close()
        return None

    def map(self, res):
        self.idregion, self.iddistrict, self.codedistrict, self.nomdistrict = \
        res["idregion"], res["iddistrict"], res["codedistrict"], res["nomdistrict"]
