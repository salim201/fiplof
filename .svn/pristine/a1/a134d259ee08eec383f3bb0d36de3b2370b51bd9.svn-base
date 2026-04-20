from qgis.gui import *
from qgis.core import *
from PyQt4.Qt import *
from PyQt4.QtCore import Qt
from qgis.gui import QgsMapTool
#from qgis.utils import iface
from PyQt4 import QtGui
from qgis.core import *
from qgis.gui  import QgsMessageBar
from PyQt4.QtCore import Qt, QSettings, QTranslator, qVersion, QCoreApplication, QFileInfo
from PyQt4.QtGui import QMessageBox, QAction, QIcon, QProgressBar
from PyQt4.QtSql import *
import math
#import MapToolMixin

class EditTrackTool(QgsMapTool):

    CAPTURE_LINE = 1
    CAPTURE_POLYGON = 2

    def __init__(self, canvas, layer, onTrackEdited):
        QgsMapTool.__init__(self,canvas)
        self.onTrackEdited = onTrackEdited
        self.dragging      = False
        self.feature       = None
        self.vertex        = None
        self.layer         = layer
        self.canvas        = canvas
        self.captureMode   = 1
        #self.rubberBand = None
        #self.tempRubberBand = None


        color = QColor("red")
        color.setAlphaF(0.08)
        self.rubberBand = QgsRubberBand(self.canvas, self.bandType())
        self.rubberBand.setWidth(2)
        self.rubberBand.setColor(color)
        self.rubberBand.show()

        self.tempRubberBand = QgsRubberBand(self.canvas, self.bandType())
        self.tempRubberBand.setWidth(1)
        color = QColor("white")
        color.setAlphaF(0.1)
        self.tempRubberBand.setColor(color)
        self.tempRubberBand.setLineStyle(Qt.DotLine)
        self.tempRubberBand.show()
        self.capturing = True
        self.setCursor(Qt.CrossCursor)

    def bandType(self):

        if self.captureMode == EditTrackTool.CAPTURE_POLYGON:
            print
            "at bandType"
            return QGis.Polygon
        else:
            return QGis.Line
    def onTrackEdited(self):
        self.modified = True
        self.mapCanvas.refresh()

    def findFeatureAt(self, pos):
        print "at findFeatureAt"
        mapPt, layerPt = self.transformCoordinates(pos)
        #tolerance = self.calcTolerance(pos)
        tolerance = self.canvas.mapUnitsPerPixel() * 4
        searchRect = QgsRectangle(layerPt.x() - tolerance, layerPt.y() - tolerance, layerPt.x() + tolerance,
                                  layerPt.y() + tolerance)
        request = QgsFeatureRequest()
        request.setFilterRect(searchRect)
        request.setFlags(QgsFeatureRequest.ExactIntersect)

        for feature in self.layer.getFeatures(request):
            return feature
        return None
    def canvasPressEvent(self, event):
        feature = self.findFeatureAt(event.pos())
        if feature == None:
            return
        vertex = self.findVertexAt(feature, event.pos())
        if vertex == None: return
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.feature  = feature
            self.vertex   = vertex

            self.moveVertexTo(event.pos())
            self.canvas.refresh()
        elif event.button() == Qt.RightButton:
            self.deleteVertex(feature, vertex)
            self.canvas.refresh()

    def canvasMoveEvent(self, event):
        if self.dragging:
            self.moveVertexTo(event.pos())
            self.canvas.refresh()

    def canvasReleaseEvent(self, event):
        if self.dragging:
            self.moveVertexTo(event.pos())
            self.layer.updateExtents()
            self.canvas.refresh()
            self.dragging = False
            self.feature = None
            self.vertex = None

    def transformCoordinates(self, screenPt):
        return (self.toMapCoordinates(screenPt), self.toLayerCoordinates(self.layer, screenPt))

    def canvasDoubleClickEvent(self, event):
        feature = self.findFeatureAt(event.pos())
        if feature == None:
            return
        mapPt, layerPt = self.transformCoordinates(event.pos())
        geometry = feature.geometry()
        distSquared, closestPt, beforeVertex = geometry.closestSegmentWithContext(layerPt)
        distance = math.sqrt(distSquared)
        tolerance = self.calcTolerance(event.pos())
        if distance > tolerance:
            return

        geometry.insertVertex(closestPt.x(), closestPt.y(), beforeVertex)
        self.layer.changeGeometry(feature.id(), geometry)
        self.onTrackEdited()
        self.canvas.refresh()

    def moveVertexTo(self, pos):

        snappedPt = self.snapToNearestVertex(pos, self.layer, self.feature)
        geometry = self.feature.geometry()
        layerPt = self.toLayerCoordinates(self.layer, pos)
        geometry.moveVertex(snappedPt.x(), snappedPt.y(), self.vertex)
        self.layer.changeGeometry(self.feature.id(), geometry)
        self.onTrackEdited()

    def deleteVertex(self, feature, vertex):
        geometry = feature.geometry()
        lineString = geometry.asPolyline()
        if len(lineString) <= 2:
            return
        if geometry.deleteVertex(vertex):
            self.layer.changeGeometry(feature.id(), geometry)
            self.onTrackEdited()

    def snapToNearestVertex(self, pos, trackLayer,excludeFeature=None):
        mapPt,layerPt = self.transformCoordinates(pos)
        feature = self.findFeatureAt(pos)
        if feature == None:
            return layerPt
        vertex = self.findVertexAt(feature, pos)
        if vertex == None: return layerPt
        return feature.geometry().vertexAt(vertex)

    def addVertex(self, canvasPoint):
        snapPt = self.snapToNearestVertex(canvasPoint, self.layer)
        mapPt = self.toMapCoordinates(self.layer, snapPt)
        self.rubberBand.addPoint(mapPt)
        self.capturedPoints.append(snapPt)
        self.tempRubberBand.reset(QGis.Line)
        self.tempRubberBand.addPoint(mapPt)

    def findVertexAt(self, feature, pos):
        mapPt, layerPt = self.transformCoordinates(pos)
        tolerance = self.calcTolerance(pos)
        vertexCoord, vertex, prevVertex, nextVertex, distSquared = feature.geometry().closestVertex(layerPt)
        distance = math.sqrt(distSquared)
        if distance > tolerance:
            return None
        else:
            return vertex

    def calcTolerance(self, pos):
        pt1 = QPoint(pos.x(), pos.y())
        pt2 = QPoint(pos.x() + 10, pos.y())
        mapPt1, layerPt1 = self.transformCoordinates(pt1)
        mapPt2, layerPt2 = self.transformCoordinates(pt2)
        tolerance = layerPt2.x() - layerPt1.x()
        return tolerance

