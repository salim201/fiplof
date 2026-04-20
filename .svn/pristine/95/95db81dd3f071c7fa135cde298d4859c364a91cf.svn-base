from unittest import result
from .IDataMapper import IDataMapper
from .IOgrDriver import IOgrDriver


class IQueryDefinition:
    def __init__(self):
        self.query = ''
        self.parameters = []
        self.associativeParameters = {}
        self.unicityCheckQuery = ''
        self.unicityCheckParameters = []


class OgrImporter():
    def __init__(self, filename, driver, mapper):  # type:(str, IOgrDriver, IDataMapper) -> None
        self.filename = filename
        self.driver = driver
        self.mapper = mapper

    def getSqlStatementsFromOGR(self):  # type:() -> list[IQueryDefinition]
        definitions = []
        rawResults = self.__queryFromOGR()
        if len(rawResults) == 0:
            return definitions
        mappedResults = map(self.mapper.map, rawResults)
        firstRow = mappedResults[0]
        values = self.__getValues(mappedResults)
        for row in values:
            queryDefinition = self.__buildQueryDefinition(firstRow, row)
            definitions.append(queryDefinition)
        return definitions

    def __queryFromOGR(self):
        resource = self.driver.Open(self.filename, False)
        sql = self.mapper.getSourceQuery()
        buffer = resource.ExecuteSQL(sql, None, None)
        results = []
        for row in buffer:
            results.append(row)
        resource.Destroy()
        return results

    def __getValues(self, rows):
        values = []
        for row in rows:
            values.append(map(lambda r: r.values()[0], row))
        return values

    def __buildQueryDefinition(self, firstRow, row):
        fields = self.__getFieldsFromRow(firstRow)
        placeholders = self.__getPlaceholdersFromRow(row)
        unicityConditions = self.__getUnicityConditions(row)
        unicityParameters = self.__getUnicityParameters(row)
        queryDefinition = IQueryDefinition()
        tableName = self.mapper.getDestinationTableName()
        queryDefinition.query = "INSERT INTO %s(%s) VALUES(%s) RETURNING %s.*" % (tableName, ', '.join(fields), ', '.join(placeholders), tableName)
        queryDefinition.parameters = row
        for fieldIndex, field in enumerate(fields):
            queryDefinition.associativeParameters[field] = row[fieldIndex]
        if len(unicityConditions) > 0:
            queryDefinition.unicityCheckQuery = "SELECT COUNT(*) FROM %s WHERE %s" % (tableName, unicityConditions)
            queryDefinition.unicityCheckParameters = unicityParameters
        return queryDefinition

    def __getFieldsFromRow(self, row):
        fields = []
        for field in row:
            fields.append(field.keys()[0])
        return fields

    def __getPlaceholdersFromRow(self, row):  # type:(list[dict]) -> list[str]
        placeholders = []
        for index, _ in enumerate(row):
            placeholders.append(self.__formatPlaceholder(index))
        return placeholders

    def __formatPlaceholder(self, index):
        geomIndex = self.mapper.getGeomColumnIndex()
        srid = self.mapper.getGeomSRID()
        if index == geomIndex:
            return 'ST_GeomFromText(%%s, %s)' % (srid)
        else:
            return '%s'

    def __getUnicityConditions(self, row):
        conditions = self.mapper.getUnicityCheckConditions(row)
        res = []
        for condition in conditions:
            column = condition.keys()[0]
            res.append('%s = %%s' % column)
        return ' AND '.join(res)

    def __getUnicityParameters(self, row):
        conditionParameters = self.mapper.getUnicityCheckConditions(row)
        return map(lambda c: c.values()[0], conditionParameters)
