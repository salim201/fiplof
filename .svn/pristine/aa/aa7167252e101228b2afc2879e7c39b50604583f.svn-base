class IDataMapper():
    def map(self, row):  # type:(dict)->list[dict]
        raise NotImplementedError

    def getDestinationTableName(self):  # type:() ->str
        raise NotImplementedError

    def getSourceQuery(self):  # type:() -> str
        raise NotImplementedError

    def getGeomColumnIndex(self):  # type:() -> int
        return None

    def getGeomSRID(self):  # type:()->int
        return None

    def getUnicityCheckConditions(self, row):  # type:(dict)->list[dict]
        return []
