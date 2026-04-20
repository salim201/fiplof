import unittest
from ..OgrImporter import OgrImporter
from ..IOgrDriver import IOgrDriver, IOgrResource
from ..IDataMapper import IDataMapper


class PersonDataMapper(IDataMapper):
    SOURCE_QUERY = 'SELECT * FROM PERSON'

    def map(self, row):
        return [{'id': row['ID']}, {'personneName': row['NAME']}]

    def getDestinationTableName(self):
        return 'person'

    def getSourceQuery(self):
        return self.SOURCE_QUERY


class FktDataMapper(IDataMapper):
    SOURCE_QUERY = 'SELECT * FROM FOKOTANY'

    def map(self, row):
        return [{'id': row['ID']}, {'nomfokontany': row['NOM']}, {'code': row['CODE']}, {'codecommune': row['CC']}]

    def getDestinationTableName(self):
        return 'fokontany'

    def getSourceQuery(self):
        return self.SOURCE_QUERY

    def getUnicityCheckConditions(self, row):
        return [{'code': row[2]}, {'codecommune': row[3]}]


class GeomDataMapper(IDataMapper):
    SOURCE_QUERY = 'SELECT * FROM TABLEWITHGEOM'

    def map(self, row):
        return [{'id': row['ID']}, {'numero': row['NUM']}, {'geom': ''}]

    def getDestinationTableName(self):
        return 'tablewithgeom'

    def getSourceQuery(self):
        return self.SOURCE_QUERY

    def getGeomColumnIndex(self):
        return 2

    def getGeomSRID(self):
        return 1000


class FakeResource(IOgrResource):
    def __init__(self):
        self.data = []
        self.open = True

    def setFakeData(self, data):
        self.data = data

    def ExecuteSQL(self, sql, flag1, flag2):
        self.executedSQL = sql
        return self.data

    def Destroy(self):
        self.open = False

    def getExecutedSQL(self):
        return self.executedSQL

    def isOpen(self):
        return self.open


class FakeOgrDriver(IOgrDriver):
    def __init__(self):
        self.resource = FakeResource()

    def Open(self, filename, flag1):
        self.openedFilename = filename
        return self.resource

    def getOpenedFilename(self):
        return self.openedFilename

    def getExecutedSQL(self):
        return self.resource.getExecutedSQL()

    def setFakeData(self, data):
        self.resource.setFakeData(data)


class OgrImporterTest(unittest.TestCase):
    def test_getInsertStatement_withData_returnsInsert(self):
        driver = FakeOgrDriver()
        driver.setFakeData([{'ID': 1, 'NAME': 'RAKOTO'}, {'ID': 2, 'NAME': 'RASOA'}])
        mapper = PersonDataMapper()
        importer = OgrImporter('myfile.gdb', driver, mapper)

        statements = importer.getSqlStatementsFromOGR()

        self.assertEqual(driver.getOpenedFilename(), 'myfile.gdb')
        self.assertEqual(driver.getExecutedSQL(), mapper.SOURCE_QUERY)
        self.assertEqual(statements[0].query, "INSERT INTO person(id, personneName) VALUES(%s, %s) RETURNING person.*")
        self.assertEqual(statements[0].parameters, [1, 'RAKOTO'])
        self.assertEqual(statements[1].query, "INSERT INTO person(id, personneName) VALUES(%s, %s) RETURNING person.*")
        self.assertEqual(statements[1].parameters, [2, 'RASOA'])
        self.assertEqual(statements[0].unicityCheckQuery, '')
        self.assertEqual(driver.resource.isOpen(), False)

    def test_getInsertStatement_withoutData_returnsEmpty(self):
        driver = FakeOgrDriver()
        driver.setFakeData([])
        mapper = PersonDataMapper()
        importer = OgrImporter('myfile.gdb', driver, mapper)

        statements = importer.getSqlStatementsFromOGR()

        self.assertEqual(driver.getOpenedFilename(), 'myfile.gdb')
        self.assertEqual(driver.getExecutedSQL(), mapper.SOURCE_QUERY)
        self.assertEqual(len(statements), 0)

    def test_getInsertStatement_withGeom_returnPlaceholderWithGeom(self):
        driver = FakeOgrDriver()
        driver.setFakeData([{'ID': 1, 'NUM': 'RAKOTO'}, {'ID': 2, 'NUM': 'RASOA'}])
        mapper = GeomDataMapper()
        importer = OgrImporter('myfile.gdb', driver, mapper)

        statements = importer.getSqlStatementsFromOGR()

        self.assertEqual(statements[0].query, "INSERT INTO tablewithgeom(id, numero, geom) VALUES(%s, %s, ST_GeomFromText(%s, 1000)) RETURNING tablewithgeom.*")

    def test_unicityCheck(self):
        driver = FakeOgrDriver()
        driver.setFakeData([{'ID': 1, 'CODE': 'F1', 'NOM': 'FKT1', 'CC': 'C1', 'OTHERCOLUMN': 'OTHERVALUE'}, {'ID': 2, 'CODE': 'F2', 'NOM': 'FKT2', 'CC': 'C2', 'OTHERCOLUMN': 'OTHERVALUE'}])
        mapper = FktDataMapper()
        importer = OgrImporter('myfile.gdb', driver, mapper)

        statements = importer.getSqlStatementsFromOGR()

        self.assertEqual(driver.getOpenedFilename(), 'myfile.gdb')
        self.assertEqual(driver.getExecutedSQL(), mapper.SOURCE_QUERY)
        self.assertEqual(statements[0].query, "INSERT INTO fokontany(id, nomfokontany, code, codecommune) VALUES(%s, %s, %s, %s) RETURNING fokontany.*")
        self.assertEqual(statements[0].parameters, [1, 'FKT1', 'F1', 'C1'])
        self.assertEqual(statements[1].query, "INSERT INTO fokontany(id, nomfokontany, code, codecommune) VALUES(%s, %s, %s, %s) RETURNING fokontany.*")
        self.assertEqual(statements[1].parameters, [2, 'FKT2', 'F2', 'C2'])
        self.assertEqual(statements[0].unicityCheckQuery, "SELECT COUNT(*) FROM fokontany WHERE code = %s AND codecommune = %s")
        self.assertEqual(statements[0].unicityCheckParameters, ['F1', 'C1'])
        self.assertEqual(statements[0].associativeParameters['nomfokontany'], 'FKT1')

    def test_getAssociativeParameters(self):
        driver = FakeOgrDriver()
        driver.setFakeData([{'ID': 1, 'NAME': 'RAKOTO'}, {'ID': 2, 'NAME': 'RASOA'}])
        mapper = PersonDataMapper()
        importer = OgrImporter('myfile.gdb', driver, mapper)

        statements = importer.getSqlStatementsFromOGR()

        self.assertEqual(driver.getOpenedFilename(), 'myfile.gdb')
        self.assertEqual(driver.getExecutedSQL(), mapper.SOURCE_QUERY)
        self.assertEqual(statements[0].associativeParameters['id'], 1)
        self.assertEqual(statements[1].associativeParameters['personneName'], 'RASOA')
        self.assertEqual(driver.resource.isOpen(), False)
