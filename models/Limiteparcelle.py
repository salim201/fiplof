import psycopg2
import psycopg2.extras


class Limiteparcelle:
    def __init__(self):
        self.idpointscardinaux, self.idparcelle, self.description, self.position = 0, 0, "", ""

    def map(self, res):
        self.idpointscardinaux, self.idparcelle, self.description, self.position = \
            res['idpointscardinaux'], res['idparcelle'], res['description'], res['position']

    @staticmethod
    def find_by_parcelleid(connection, idparcelle):
        results = []
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT L.*, P.position FROM limitesparcelle L "
                           "JOIN pointscardinaux P on P.idpointscardinaux = L.idpointscardinaux "
                           "WHERE L.idparcelle = %s", (idparcelle,))
            rows = cursor.fetchall()
            for r in rows:
                d = Limiteparcelle()
                d.map(r)
                results.append(d)
        except Exception as e:
            print(e)
        cursor.close()
        return results

    @staticmethod
    def insert(connection, lp):

        cursor = connection.cursor(
                cursor_factory=psycopg2.extras.DictCursor
            )

        try:

                sql = """
                    INSERT INTO limitesparcelle
                    (
                        idpointscardinaux,
                        idparcelle,
                        description
                    )
                    VALUES
                    (
                        %s, %s, %s
                    )
                """

                cursor.execute(sql, (

                    lp.idpointscardinaux,
                    lp.idparcelle,
                    lp.description

                ))

                connection.commit()
                return True

        except Exception as e:
            connection.rollback()
            print("Erreur insert LimitesParcelle :", e)

        finally:
            cursor.close()

        return False

