'''
Created on 12/10/2014

@author: ferrari
'''
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


class CoordinatesPoints(QgsMapTool):

    def __init__(self, iface, canvas,parent):
        self.canvas = canvas
        self.iface = iface
        self.layer= canvas.currentLayer()
        self.active = True
        self.parent = parent
        QgsMapTool.__init__(self,canvas)


    def canvasReleaseEvent(self, e):
        print "canvasReleaseEvent out"
        point = self.toLayerCoordinates(self.layer, e.pos())
        d = self.canvas.mapUnitsPerPixel() * 4
        self.parent.labelCoordonnees.setText(str(point.x()) + "," + str(point.y()))
        #self.mouseDown = True
        #self.layer.triggerRepaint()

    def canvasMoveEvent(self, e):
        #if not self.mouseDown: return
        point = self.toLayerCoordinates(self.layer, e.pos())
        d = self.canvas.mapUnitsPerPixel() * 4
        self.parent.labelCoordonnees.setText(str(point.x())+","+str(point.y()))