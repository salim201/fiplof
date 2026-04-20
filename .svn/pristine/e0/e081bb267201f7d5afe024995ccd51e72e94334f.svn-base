import os, os.path, sys
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *

class EditTool(QgsMapTool):

    def __init__(self, mapCanvas, layer, onGeometryChanged):
        print "edit tool"
        QgsMapTool.__init__(self, mapCanvas)
        self.setCursor(Qt.CrossCursor)
        self.layer             = layer
        self.onGeometryChanged = onGeometryChanged
        self.dragging          = False
        self.feature           = None
        self.vertex            = None
        self.canvas            = mapCanvas

    def canvasPressEvent(self, event):
        print "at canvasPressEvent in"
        feature = self.findFeatureAt(event.pos())
        print "event.pos() in"
        print event.pos()
        print "event.pos() out"
        if feature == None:
            print "None Feature"
            return

        mapPt, layerPt = self.transformCoordinates(event.pos())
        geometry = feature.geometry()
        vertexCoord, vertex, prevVertex, nextVertex, distSquared = geometry.closestVertex(layerPt)
        print "distSquared in"
        print distSquared
        print "distSquared out"
        #distance = math.sqrt(distSquared)
        distance = 18.8803540154
        print "distance in"
        print distance
        print "distance out "
        tolerance = self.calcTolerance(event.pos())

        print "tolerance in "
        print tolerance
        print "tolerance out "
        if distance > tolerance:

            return
        print "event.button() in "
        print event.button()
        print "event.button() out"
        if event.button() == Qt.LeftButton:
            print "Qt.LeftButton:"
            self.dragging = True
            self.feature = feature
            self.vertex = vertex
            self.moveVertexTo(event.pos())
            self.canvas().refresh()
        elif event.button() == Qt.RightButton:
            # Right click -> delete vertex.
            print "Qt.RightButton::"
            self.deleteVertex(feature, vertex)
            self.canvas().refresh()
        print "at canvasPressEvent out"


    def transformCoordinates(self, canvasPt):
        print "at transformCoordinates in"
        return (self.toMapCoordinates(canvasPt), self.toLayerCoordinates(self.layer, canvasPt))


    def canvasDoubleClickEvent(self, event):
        print "at canvasDoubleClickEvent in"
        feature = self.findFeatureAt(event.pos())
        if feature == None:
            return
        mapPt, layerPt = self.transformCoordinates(event.pos())
        geometry = feature.geometry()
        distSquared, closestPt, beforeVertex = geometry.closestSegmentWithContext(layerPt)
        #distance = math.sqrt(distSquared)
        distance = 18.8803540154
        tolerance = self.calcTolerance(event.pos())
        if distance > tolerance:
            return
        geometry.insertVertex(closestPt.x(), closestPt.y(),beforeVertex)
        self.layer.changeGeometry(feature.id(),geometry)
        self.canvas().refresh()
        print "at canvasDoubleClickEvent out"

    def canvasReleaseEvent(self, event):
        print "at canvasReleaseEvent in"
        if self.dragging:
            self.moveVertexTo(event.pos())
            self.layer.updateExtents()
            self.canvas().refresh()
            self.dragging = False
            self.feature = None
            self.vertex = None
        print "at canvasReleaseEvent out"

    def moveVertexTo(self, pos):
        print "at moveVertexTo in"
        geometry = self.feature.geometry()
        layerPt = self.toLayerCoordinates(self.layer, pos)
        geometry.moveVertex(layerPt.x(), layerPt.y(), self.vertex)
        self.layer.changeGeometry(self.feature.id(), geometry)
        #self.onGeometryChanged()
        print "at moveVertexTo out"

    def findFeatureAt(self, pos):

        mapPt,layerPt = self.transformCoordinates(pos)
        tolerance = self.calcTolerance(pos)
        searchRect = QgsRectangle(layerPt.x() - tolerance,
                                  layerPt.y() - tolerance,
                                  layerPt.x() + tolerance,
                                  layerPt.y() + tolerance)
        request = QgsFeatureRequest()
        request.setFilterRect(searchRect)
        request.setFlags(QgsFeatureRequest.ExactIntersect)

        for feature in self.layer.getFeatures(request):
            return feature
        #print "at findFeatureAt out"
        return None

    def canvasMoveEvent(self, event):
        print "at canvasMoveEvent in"
        if self.dragging:
            self.moveVertexTo(event.pos())
            self.canvas().refresh()

    def calcTolerance(self,pos):

        pt1 = QPoint(pos.x(), pos.y())
        pt2 = QPoint(pos.x() + 10, pos.y())
        mapPt1,layerPt1 = self.transformCoordinates(pt1)
        mapPt2,layerPt2 = self.transformCoordinates(pt2)
        tolerance = layerPt2.x() - layerPt1.x()
        return tolerance

    def deleteVertex(self, feature, vertex):
        print "at deleteVertex in"
        geometry = feature.geometry()
        if geometry.wkbType() == QGis.WKBLineString:
            lineString = geometry.asPolyline()
            if len(lineString) <= 2:
                return
            elif geometry.wkbType() == QGis.WKBPolygon:
                polygon = geometry.asPolygon()
                exterior = polygon[0]
                if len(exterior) <= 4:
                    return
        if geometry.deleteVertex(vertex):
            self.layer.changeGeometry(feature.id(), geometry)
            #self.onGeometryChanged()

