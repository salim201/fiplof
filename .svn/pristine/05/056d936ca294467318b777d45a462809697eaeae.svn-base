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

