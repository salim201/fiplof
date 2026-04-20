from GeometryLoader.GeometryDataSource import GeometryDataSource


class LayerProperties:
    index = 0
    label = "" # type: str
    name = ''
    styles = {}
    dataSource = None  # type: GeometryDataSource
    isCurrent = False

    def __init__(self, layerIndex, layerLabel, namePrefix=""):
        self.index = layerIndex
        self.label = layerLabel
        self.name = "%s%s" % (namePrefix, layerLabel)

    def setCurrent(self):
        self.isCurrent = True