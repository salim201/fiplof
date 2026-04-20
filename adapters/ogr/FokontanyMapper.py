from usecases.ogrimporter.IDataMapper import IDataMapper
import globalvars


class FokontanyMapper(IDataMapper):
    def getDestinationTableName(self):
        return 'fokontany'

    def map(self, row):
        return [
            {'codefokontany': row['F_CODE']},
            {'nomfokontany': row['FOKONTANY']},
            {'idcommune': globalvars.id_commune},
        ]

    def getSourceQuery(self):
        return 'SELECT * FROM limiteFokotany'

    def getUnicityCheckConditions(self, row):
        return [
            {'codefokontany': row[0]}
        ]
