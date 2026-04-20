class MapToolMixin():
    def setLayer(self, layer):
        self.layer = layer
    def transformCoordinates(self, screenPt):
        return (self.toMapCoordinates(screenPt),self.toLayerCoordinates(self.layer, screenPt))
    def calcTolerance(self, pos):
        pt1 = QPoint(pos.x(), pos.y())
        pt2 = QPoint(pos.x() + 10, pos.y())
        mapPt1,layerPt1 = self.transformCoordinates(pt1)
        mapPt2,layerPt2 = self.transformCoordinates(pt2)
        tolerance = layerPt2.x() - layerPt1.x()
        return tolerance