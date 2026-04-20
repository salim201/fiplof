from usecases.ogrimporter.IDataMapper import IDataMapper
import globalvars


class ParcelleDemandeMapper(IDataMapper):
    def getDestinationTableName(self):
        return 'parcelle_d'

    def getSourceQuery(self):
        return 'SELECT * FROM parcelleDemande'

    def map(self, row):
        return [
            {'numdemande': row['numeroDemande']},
            {'geom': str(row.GetGeomFieldRef(0))},
        ]

    def getUnicityCheckConditions(self, row):
        return [
            {'numdemande': row[0]}
        ]

    def getGeomColumnIndex(self):
        return 1

    def getGeomSRID(self):
        return globalvars.EPSG_SCR
