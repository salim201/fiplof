import os, os.path, sys
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import*
import qgis

class MovePointTool(QgsMapToolIdentify):
    def __init__(self, mapCanvas, layer):
        QgsMapToolIdentify.__init__(self, mapCanvas)
        self.setCursor(Qt.CrossCursor)
        self.layer    = layer
        self.dragging = False
        self.feature  = None
    def canvasPressEvent(self, event):
        print "canvas Press"
        found_features = self.identify(event.x(), event.y(),self.TopDownStopAtFirst,[self.layer],self.VectorLayer)
        if len(found_features) > 0:
            self.dragging = True
            self.feature  = found_features[0].mFeature
        else:
            self.dragging = False
            self.feature  = None
    def canvasMoveEvent(self, event):
        print "canvas Move"
        if self.dragging:
            point = self.toLayerCoordinates(self.layer,
                                            event.pos())
            geometry = QgsGeometry.fromPoint(point)
            self.layer.changeGeometry(self.feature.id(), geometry)
            self.canvas().refresh()
    def canvasReleaseEvent(self, event):
        print "Canvas Release"
        self.dragging = False
        self.feature  = None

