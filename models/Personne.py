import psycopg2
import psycopg2.extras


class Personne:

    def __init__(self):

        self.idpersonne = None
        self.nompersonne = None
        self.prenompersonne = None
        self.sexepersonne = None
        self.datenaissancepersonne = None
        self.nevers = None
        self.lieunaissancepersonne = None
        self.numcipersonne = None
        self.datecipersonne = None
        self.lieucipersonne = None
        self.numactenaissancepersonne = None
        self.dateactenaissancepersonne = None
        self.lieuactenaissancepersonne = None
        self.adressepersonne = None
        self.situationmatrimoniale = 0
        self.nompere = None
        self.nommere = None
        self.csv_id = None
        self.rcin_personne = None
        self.ogr_id = None
        self.handicap = False
        self.niveau_education = None
        self.possede_emploi = True
        self.migrant = False
        self.date_arrivee = None
        self.conjoint = None
        self.datemaj = None
        self.cin_nom_prenom_key = None

    def map(self, row):

        self.idpersonne = row["idpersonne"]
        self.nompersonne = row["nompersonne"]
        self.prenompersonne = row["prenompersonne"]
        self.sexepersonne = row["sexepersonne"]
        self.datenaissancepersonne = row["datenaissancepersonne"]
        self.nevers = row["nevers"]
        self.lieunaissancepersonne = row["lieunaissancepersonne"]
        self.numcipersonne = row["numcipersonne"]
        self.datecipersonne = row["datecipersonne"]
        self.lieucipersonne = row["lieucipersonne"]
        self.numactenaissancepersonne = row["numactenaissancepersonne"]
        self.dateactenaissancepersonne = row["dateactenaissancepersonne"]
        self.lieuactenaissancepersonne = row["lieuactenaissancepersonne"]
        self.adressepersonne = row["adressepersonne"]
        self.situationmatrimoniale = row["situationmatrimoniale"]
        self.nompere = row["nompere"]
        self.nommere = row["nommere"]
        self.csv_id = row["csv_id"]
        self.rcin_personne = row["rcin_personne"]
        self.ogr_id = row["ogr_id"]
        self.handicap = row["handicap"]
        self.niveau_education = row["niveau_education"]
        self.possede_emploi = row["possede_emploi"]
        self.migrant = row["migrant"]
        self.date_arrivee = row["date_arrivee"]
        self.conjoint = row["conjoint"]
        self.datemaj = row["datemaj"]
        self.cin_nom_prenom_key = row["cin_nom_prenom_key"]

    @staticmethod
    def insert(connection, personne):

        print("DEBUG : ATO AMIN'NY INSERTION PERSONNE")
        print(personne)
        print("DEBUG : FIN ATO AMIN'NY INSERTION PERSONNE")

        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        )

        try:

                # =========================================
                # 1. VERIFIER EXISTENCE
                # =========================================
                sql_check = """
                    SELECT idpersonne
                    FROM personne
                    WHERE numcipersonne = %s
                    AND nompersonne = %s
                    AND prenompersonne = %s
                    LIMIT 1
                """

                cursor.execute(sql_check, (
                    personne.numcipersonne,
                    personne.nompersonne,
                    personne.prenompersonne
                ))

                row = cursor.fetchone()

                if row:
                    print("DEBUG : PERSONNE EXISTE DEJA")
                    return row[0]

                sql = """
                    INSERT INTO personne
                    (
                        nompersonne,
                        prenompersonne,
                        sexepersonne,
                        datenaissancepersonne,
                        lieunaissancepersonne,
                        nevers,
                        numactenaissancepersonne,
                        dateactenaissancepersonne,
                        numcipersonne,
                        datecipersonne,
                        lieucipersonne,
                        nompere,
                        nommere,
                        situationmatrimoniale,
                        adressepersonne
                    )
                    VALUES
                    (
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s
                    )
                    RETURNING idpersonne
                """

                cursor.execute(sql, (

                    personne.nompersonne,
                    personne.prenompersonne,
                    personne.sexepersonne,
                    personne.datenaissancepersonne,
                    personne.lieunaissancepersonne,
                    personne.nevers,
                    personne.numactenaissancepersonne,
                    personne.dateactenaissancepersonne,
                    personne.numcipersonne,
                    personne.datecipersonne,
                    personne.lieucipersonne,
                    personne.nompere,
                    personne.nommere,
                    personne.situationmatrimoniale,
                    personne.adressepersonne

                ))

                idpersonne = cursor.fetchone()[0]

                connection.commit()

                return idpersonne

        except Exception as e:

                connection.rollback()
                print(e)

        finally:

                cursor.close()

        return None



        
    @staticmethod
    def findById(connection, idpersonne):

        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        )

        try:

            sql = """
                SELECT *
                FROM personne
                WHERE idpersonne = %s
            """

            cursor.execute(sql, (idpersonne,))

            row = cursor.fetchone()

            if row is None:
                return None

            p = Personne()
            p.map(row)

            return p

        except Exception as e:

            print(e)

        finally:

            cursor.close()

        return None