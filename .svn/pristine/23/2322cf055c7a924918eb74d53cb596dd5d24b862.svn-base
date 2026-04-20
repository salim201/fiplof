from usecases.ogrimporter.IDataMapper import IDataMapper


class CommuneMapper(IDataMapper):
    def getDestinationTableName(self):
        return 'commune'

    def getSourceQuery(self):
        return 'SELECT * FROM limiteFokotany'

    def map(self, row):
        return [
            {'codecommune': row['C_CODE']},
            {'nomcommune': row['COMMUNE']},
        ]

    def getUnicityCheckConditions(self, row):
        return [
            {'codecommune': row[0]},
        ]
