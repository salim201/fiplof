import psycopg2
import psycopg2.extras


class Pointscardinaux:

    def __init__(self):

        self.idpointscardinaux = None
        self.position = None
        self.fanondroana = None
        self.datemaj = None

    def map(self, row):

        self.idpointscardinaux = row["idpointscardinaux"]
        self.position = row["position"]
        self.fanondroana = row["fanondroana"]
        self.datemaj = row["datemaj"]


    @staticmethod
    def findByPosition(connection, position):

        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        )

        try:

            position = position.strip().upper()

            sql = """
                SELECT *
                FROM pointscardinaux
                WHERE UPPER("position") = %s
            """

            cursor.execute(sql, (position,))

            row = cursor.fetchone()

            if row is None:
                return None

            pc = Pointscardinaux()
            pc.map(row)

            return pc

        except Exception as e:
            print("Erreur findByPosition :", e)

        finally:
            cursor.close()

        return None

    @staticmethod
    def insert(connection, pc):

        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        )

        try:

            sql = """
                INSERT INTO pointscardinaux
                (
                    position,
                    fanondroana
                )
                VALUES
                (
                    %s, %s
                )
                RETURNING idpointscardinaux
            """

            cursor.execute(sql, (

                pc.position,
                pc.fanondroana

            ))

            id_pc = cursor.fetchone()[0]

            connection.commit()
            return id_pc

        except Exception as e:
            connection.rollback()
            print("Erreur insert Pointscardinaux :", e)

        finally:
            cursor.close()

        return None