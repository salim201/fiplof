import psycopg2
import psycopg2.extras


class AvoirDemande:

    def __init__(self):

        self.idpersonne = None
        self.iddemande = None
        self.idparcelle = None
        self.representant = False
        self.csv_id = None
        self.datemaj = None

    def map(self, row):

        self.idpersonne = row["idpersonne"]
        self.iddemande = row["iddemande"]
        self.idparcelle = row["idparcelle"]
        self.representant = row["representant"]
        self.csv_id = row["csv_id"]
        self.datemaj = row["datemaj"]

    @staticmethod
    def insert(connection, avoir_demande):


        print("DEBUG : AVOIR DEMANDE ",avoir_demande)

        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        )

        try:

            sql = """
                INSERT INTO avoir_demande
                (
                    idpersonne,
                    iddemande,
                    idparcelle,
                    representant
                )
                VALUES
                (
                    %s, %s, %s, %s
                )
            """

            cursor.execute(sql, (

                avoir_demande.idpersonne,
                avoir_demande.iddemande,
                avoir_demande.idparcelle,
                avoir_demande.representant

            ))

            connection.commit()

            return True

        except Exception as e:

            connection.rollback()
            print(e)

        finally:

            cursor.close()

        return False

    @staticmethod
    def findById(connection, idpersonne, idparcelle):

        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        )

        try:

            sql = """
                SELECT *
                FROM avoir_demande
                WHERE idpersonne = %s
                AND idparcelle = %s
            """

            cursor.execute(sql, (
                idpersonne,
                idparcelle
            ))

            row = cursor.fetchone()

            if row is None:
                return None

            a = AvoirDemande()
            a.map(row)

            return a

        except Exception as e:

            print(e)

        finally:

            cursor.close()

        return None