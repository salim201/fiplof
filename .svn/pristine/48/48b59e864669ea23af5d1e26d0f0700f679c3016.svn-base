from usecases.ogrimporter.IDataMapper import IDataMapper


class TempProprietaireMapper(IDataMapper):
    def __init__(self, connection):
        self.initTempTable(connection)

    def getDestinationTableName(self):
        return "ogr_proprietaire"

    def getSourceQuery(self):
        return "SELECT P.numeroProprietaire AS numeroProprietaire, C.numeroDemande AS numeroDemande FROM proprietaire P JOIN certificat C on C.numeroCertificat = P.numeroCertificat WHERE typeProprio = '2'"

    def map(self, row):
        return [
            {'numeroproprietaire': row['numeroProprietaire']},
            {'numerodemande': row['numeroDemande']},
        ]

    def getUnicityCheckConditions(self, row):
        return [
            {'numeroproprietaire': row[0]},
            {'numerodemande': row[1]},
        ]

    def initTempTable(self, connection):
        cursor = connection.cursor()
        try:
            cursor.execute('CREATE TABLE IF NOT EXISTS ogr_proprietaire(numeroproprietaire character varying(32), numerodemande character varying(32))')
            cursor.execute('DELETE FROM ogr_proprietaire')
            connection.commit()
        except Exception as e:
            print(e)
            connection.rollback()
        cursor.close()
