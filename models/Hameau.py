import psycopg2
import psycopg2.extras


class Hameau:

    def table_name(self):
        return "hameau"

    def key_name(self):
        return "idhameau"

    def key_value(self):
        return self.idhameau

    def fields(self):
        return (
            "idfokontany",
            "codehameau",
            "nomhameau"
        )

    def values(self):
        return (
            self.idfokontany,
            self.codehameau,
            self.nomhameau
        )

    def __init__(self, connection):

        self.idhameau = None
        self.idfokontany = None
        self.codehameau = ""
        self.nomhameau = ""

    def map(self, res):
        if not res:
            return

        self.idhameau = res["idhameau"]
        self.idfokontany = res["idfokontany"]
        self.codehameau = res["codehameau"]
        self.nomhameau = res["nomhameau"]

    @staticmethod
    def findByName(connection, nomhameau):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        print('DEBUG: Hameau', nomhameau)
        try:
            cursor.execute(
                """
                SELECT *
                FROM hameau
                WHERE UPPER(TRIM(nomhameau)) = UPPER(TRIM(%s))
                """,
                (nomhameau,)
            )

            res = cursor.fetchone()

            if not res:
                return None

            h = Hameau(connection)
            h.map(res)
            return h

        except Exception as e:
            print("[Hameau.findByName] erreur:", e)
            return None

        finally:
            cursor.close()