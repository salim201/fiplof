from PyQt4 import QtGui
from qgis.gui import *
from qgis.core import QgsRasterLayer, QgsPoint, QgsMapLayerRegistry
from PyQt4.QtCore import QFileInfo, pyqtSignal
from .FormGeoreferencer import Ui_FormGeoreferencer
import os
import tempfile


class GeoReferencerRun(QtGui.QWidget):
    pointAddedSignal = pyqtSignal(QgsPoint)
    pointRemovedSignal = pyqtSignal(QgsVertexMarker)
    referenceTerminatedSignal = pyqtSignal(str)

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_FormGeoreferencer()
        self.ui.setupUi(self)
        self.init_canvas()

        self.toolBar = QtGui.QToolBar()
        self.toolBar.addAction(self.ui.actionLoadLayer)
        self.toolBar.addAction(self.ui.actionPan)
        self.toolBar.addAction(self.ui.actionAddPoint)
        self.toolBar.addAction(self.ui.actionDelPoint)
        self.toolBar.addAction(self.ui.actionRun)
        self.ui.horizontalLayout.addWidget(self.toolBar)

        self.toolPan = QgsMapToolPan(self.canvas)
        self.toolPan.setAction(self.ui.actionPan)
        self.toolPoint = QgsMapToolEmitPoint(self.canvas)
        self.toolPoint.setAction(self.ui.actionAddPoint)

        self.current_row = None
        self.nodes = []
        self.vertices = []

        self.init_actions()

    def init_actions(self):
        self.ui.actionLoadLayer.triggered.connect(self.load_layer)
        self.ui.actionPan.triggered.connect(self.pan)
        self.ui.actionAddPoint.triggered.connect(self.add_point)
        self.ui.actionDelPoint.triggered.connect(self.del_point)
        self.toolPoint.canvasClicked.connect(self.point_clicked)
        self.ui.tableWidget.itemSelectionChanged.connect(self.row_clicked)
        self.ui.actionRun.triggered.connect(self.run)

    def init_canvas(self):
        self.canvas = QgsMapCanvas()
        self.ui.verticalLayout_2.addWidget(self.canvas)
        self.canvas.show()

    def pan(self):
        if(self.ui.actionPan.isChecked()):
            self.canvas.setMapTool(self.toolPan)
        else:
            self.canvas.unsetMapTool(self.toolPan)

    def add_point(self):
        if(self.ui.actionAddPoint.isChecked()):
            self.canvas.setMapTool(self.toolPoint)
        else:
            self.canvas.unsetMapTool(self.toolPoint)

    def del_point(self):
        if self.current_row is None:
            return
        del self.nodes[self.current_row]
        self.canvas.scene().removeItem(self.vertices[self.current_row][0])
        if self.vertices[self.current_row][1] is not None:
            self.pointRemovedSignal.emit(self.vertices[self.current_row][1])
        del self.vertices[self.current_row]
        self.update_table()
        if len(self.vertices):
            self.current_row = 0

    def point_clicked(self, point, button):
        m = QgsVertexMarker(self.canvas)
        m.setCenter(point)
        m.setIconType(QgsVertexMarker.ICON_BOX)
        self.vertices.append([m, None])
        self.nodes.append([point[0], point[1], 0, 0])
        self.update_table()
        self.current_row = len(self.nodes) - 1
        self.pointAddedSignal.emit(point)

    def update_table(self):
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setRowCount(len(self.nodes))
        for i, point in enumerate(self.nodes):
            itemx1 = QtGui.QTableWidgetItem(str(point[0]))
            itemy1 = QtGui.QTableWidgetItem(str(point[1]))
            itemx2 = QtGui.QTableWidgetItem(str(point[2]))
            itemy2 = QtGui.QTableWidgetItem(str(point[3]))
            self.ui.tableWidget.setItem(i, 0, itemx1)
            self.ui.tableWidget.setItem(i, 1, itemy1)
            self.ui.tableWidget.setItem(i, 2, itemx2)
            self.ui.tableWidget.setItem(i, 3, itemy2)

    def row_clicked(self):
        indexes = self.ui.tableWidget.selectedIndexes()
        if len(indexes) == 0:
            return
        self.current_row = indexes[0].row()

    def setDestination(self, point, canvas):
        if self.current_row is None:
            return
        self.nodes[self.current_row][2] = point[0]
        self.nodes[self.current_row][3] = point[1]
        self.update_table()
        if not self.vertices[self.current_row][1]:
            m = QgsVertexMarker(canvas)
            m.setCenter(point)
            m.setIconType(QgsVertexMarker.ICON_BOX)
            self.vertices[self.current_row][1] = m
        else:
            self.vertices[self.current_row][1].setCenter(point)

    def load_layer(self):

        filename = QtGui.QFileDialog.getOpenFileName(self, "Choisissez un fichier")
        if not filename:
            return
        self.raster_path = filename
        fileInfo = QFileInfo(filename)
        baseName = fileInfo.baseName()
        layer = QgsRasterLayer(filename, baseName)
        if not layer.isValid():
            print("Layer " + filename + " is not valid raster")
            return None
        reg = QgsMapLayerRegistry.instance()
        reg.addMapLayer(layer)
        self.canvas.setExtent(layer.extent())
        self.canvas.setLayerSet([QgsMapCanvasLayer(layer)])

    def run(self):
        qgis_srs_epsg = self.canvas.mapRenderer().destinationCrs().authid()[5:]
        outfile_path = QtGui.QFileDialog.getSaveFileName(
            None,
            'Georeferenced image path',
            self.raster_path[:-len(self.raster_path.split('/')[-1].split('.')[-1]) - 1] + '_EPSG' + qgis_srs_epsg,
            '*.tif'
        )
        methods = ['near', 'bilinear', 'cubic', 'cubicspline', 'lanczos']
        transformations = ['order 1', 'order 2', 'order 3', 'tps', 'line']
        rs_method = methods[self.ui.comboBoxResampling.currentIndex()]
        tr_method = transformations[self.ui.comboBoxTransformation.currentIndex()]
        cp_method = "NONE"

        gcp_txt = ""
        for i in range(len(self.nodes)):
            gcp_txt += '-gcp ' + str(self.nodes[i][0]) + ' ' + str(-self.nodes[i][1]) + \
                ' ' + str(self.nodes[i][2]) + ' ' + str(self.nodes[i][3]) + ' '
        basename = self.raster_path.split('/')[-1]
        temp_rast_path = os.path.join(tempfile.gettempdir(), str(basename))
        os.system('gdal_translate -of GTiff ' + gcp_txt + '"' + str(self.raster_path) + '" "' + temp_rast_path + '"')
        os.system(
            'gdalwarp -r ' + rs_method +
            ' -' + tr_method + ' -co COMPRESS=' + cp_method +
            ' -t_srs EPSG:' + str(qgis_srs_epsg) +
            ' -dstalpha "' + str(temp_rast_path) +
            '" "' + str(outfile_path) + '"'
        )
        if os.path.isfile(str(outfile_path)):
            self.referenceTerminatedSignal.emit(str(outfile_path))
