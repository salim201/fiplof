# -*- coding: utf-8 -*-
import os.path
from PyQt4 import QtGui, Qt
from PyQt4 import QtGui
from qgis.gui import *
from qgis.core import QgsRasterLayer, QgsPoint, QgsMapLayerRegistry
from PyQt4.QtCore import QFileInfo, pyqtSignal
from PyQt4.QtCore import QFileInfo,QSettings
from qgis.core import QgsRasterLayer, QgsCoordinateReferenceSystem


from qgis.core import QgsProject
from .exportgeorefrasterdialog import Ui_ExportGeorefRasterDialog
from qgis.core import QgsMapLayerRegistry, QgsPluginLayerRegistry, QgsMapLayer

from .freehandrastergeoreferencer_commands import ExportGeorefRasterCommand
from .freehandrastergeoreferencer_layer import FreehandRasterGeoreferencerLayerType, FreehandRasterGeoreferencerLayer
from .freehandrastergeoreferencer_maptools import MoveRasterMapTool,RotateRasterMapTool, ScaleRasterMapTool, AdjustRasterMapTool,GeorefRasterBy2PointsMapTool
#from freehandrastergeoreferencerdialog
import utils
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class addFiles(Qt.QDialog):
    def __init__(self, parent):
        Qt.QDialog.__init__(self)
        self.parent = parent

        self.iface = self.parent.iface
        self.canvas = self.parent.canvas
        self.layers = []
        #self.connection = connection
        self.ui = Ui_ExportGeorefRasterDialog()
        self.ui.setupUi(self)
        #self.refresh()
        self.initActions()


    def initActions(self):
        print "init"
        self.ui.pushButtonBrowse.clicked.connect(self.chargerImages)
        #self.ui.actionMerge.triggered.connect(self.MergeLayer)

    def showBrowserDialog(self):
        #bDir, found = QgsProject.instance().readEntry(
        #    utils.SETTINGS_KEY,
        #    utils.SETTING_BROWSER_RASTER_DIR,
        #    None)

        #if not found or not os.path.isdir(bDir):
        #    bDir = os.path.expanduser("~")

        #qDebug(repr(bDir))
        filepath = '%s' % (QtGui.QFileDialog.getOpenFileName(
            self, "Select image", "Images (*.png *.bmp *.jpg *.tif)"))
        self.lineEditImagePath.setText(filepath)


    def initTransparenct(self):
        print "init"
    def chargerImages(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, "Choisissez un fichier", ".")
        if not filename:
            return
        self.raster_path = filename
        fileInfo = QFileInfo(filename)
        baseName = fileInfo.baseName()
        # title = os.path.basename(str(name))
        self.ui.lineEditImagePath.setText(filename)
        self.raster_path = filename
        fileInfo = QFileInfo(filename)
        baseName = fileInfo.baseName()
        crs = QgsCoordinateReferenceSystem(globalvars.EPSG_SCR, QgsCoordinateReferenceSystem.EpsgCrsId)
        screenExtent = self.canvas.extent()
        layer = FreehandRasterGeoreferencerLayer(self, self.raster_path, baseName, screenExtent)
        layer.setCrs(crs)
        self.canvas.setCurrentLayer(layer)
        self.parent.GeorefLayer = layer

        print " FreehandRasterGeoreferencerLayer layer "
        print layer
        print " self.cLayer"
        print self.parent.cLayer


        if layer.isValid():
            print "layer is valid"
            QgsMapLayerRegistry.instance().addMapLayer(layer)
            self.canvas.setExtent(layer.extent())
            self.parent.vectors.append(layer)
            self.parent.layers.append(QgsMapCanvasLayer(layer))
            self.canvas.setLayerSet([QgsMapCanvasLayer(layer)])
            #self.layers[125] = layer
            self.parent.addLayerToPanel(baseName)
            self.canvas.setExtent(layer.extent())
            # clamp to 100
            tr = min(layer.transparency + 10, 100)
            layer.setTransparency(tr)
            #layer.setOpacity(10.5)

            #layer.transparencyChanged(tr)
            #self.iface.legendInterface().setCurrentLayer(layer)

        #self.parent.addLayerToPanel(baseName)





    def upload(self):

            #from PyQt4.QtGui import QImageReader, QPainter, QColor
            #reader = QImageReader("C:/Program Files (x86)/QGIS Wien/apps/qgis-ltr/python/plugins/qgsplof/Demande/preview.png")
            #self.image = reader.read()
            #print "WWIDTH"
            #print self.image.width()

            filename = QtGui.QFileDialog.getOpenFileName(self, "Choisissez un fichier",".")
            if not filename:
                return
            self.raster_path = filename
            fileInfo = QFileInfo(filename)
            baseName = fileInfo.baseName()
            #title = os.path.basename(str(name))
            self.ui.lineEditImagePath.setText(filename)

            self.raster_path = filename
            fileInfo = QFileInfo(filename)
            baseName = fileInfo.baseName()
            layer = QgsRasterLayer(filename, baseName)
            crs = QgsCoordinateReferenceSystem(globalvars.EPSG_SCR, QgsCoordinateReferenceSystem.EpsgCrsId)

            if not layer.isValid():
                print("Layer " + filename + " is not valid raster")
                return None

            self.canvas.setCurrentLayer(layer)
            layer.setCrs(crs)
            reg = QgsMapLayerRegistry.instance()
            reg.addMapLayer(layer)
            #self.parent.addLayerToPanel(baseName)
            #return QgsMapCanvasLayer(layer)
            #self.canvas.setExtent(layer.extent())
            self.parent.vectors.append(layer)
            self.parent.layers.append(QgsMapCanvasLayer(layer))
            self.canvas.setLayerSet([QgsMapCanvasLayer(layer)])
            self.parent.addLayerToPanel(baseName)

            print "BASE NAME"
            #print baseName

            print " SELF.RASTER_PATH"
            #print self.raster_path
            #self.parent.addLayerToPanel(baseName)
            screenExtent = self.canvas.extent()
            #layer = FreehandRasterGeoreferencerLayer(
            #    self, self.raster_path, baseName, screenExtent)
            #layer.setCrs(crs)

            #if layer.isValid():
            #    QgsMapLayerRegistry.instance().addMapLayer(layer)
            #    self.canvas.setExtent(layer.extent())
            #    self.parent.vectors.append(layer)
            #    self.canvas.setLayerSet([QgsMapCanvasLayer(layer)])
            #    #self.layers[125] = layer
            #    self.canvas.setCurrentLayer(layer)
            #    self.parent.addLayerToPanel(baseName)
            #     self.iface.legendInterface().setCurrentLayer(layer)


