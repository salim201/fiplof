class GeometryDataSource:
    schema = ""
    tableName = ''
    geometryFieldName = ''
    labelFieldName = ''
    keyFieldName = ''
    selectionCondition = ''

    def __init__(self, tableName, labelFieldName, selectionCondition="", schema="public", geometryFieldName="geom", keyFieldName="gid"):
        self.schema = schema
        self.tableName = tableName
        self.geometryFieldName = geometryFieldName
        self.labelFieldName = labelFieldName
        self.keyFieldName = keyFieldName
        self.selectionCondition = selectionCondition