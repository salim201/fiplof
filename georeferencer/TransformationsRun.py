# -*- coding: utf-8 -*-
import os.path
from PyQt4 import QtGui, Qt, QtCore
from PyQt4 import QtGui
from PyQt4.QtCore import QFileInfo, pyqtSignal
from qgis.gui import *
from .TableTransformations import Ui_Dialog
import janek_transformations
import numpy
import sys
import tempfile
reload(sys)
sys.setdefaultencoding('utf8')


class Transformations(Qt.QDialog):
    referenceTerminatedSignal = pyqtSignal(str)
    pointDeleted = pyqtSignal(int)

    def __init__(self, parent, points, raster_path):
        Qt.QDialog.__init__(self)
        self.parent = parent
        self.iface = self.parent.iface
        self.canvas = self.parent.canvas
        self.layers = []
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.init_actions()
        self.points, self.raster_path = points, raster_path
        self.points_xy = []
        for index, p in enumerate(points):
            self.points_xy.append([p['src'][0], p['src'][1], p['dst'][0], p['dst'][1]])
        self.gcp_table = numpy.array(self.points_xy)
        self.init_table()

    def init_actions(self):
        self.ui.transformationsComboBox.currentIndexChanged.connect(self.refresh_table)
        self.ui.pushButtonDelete.clicked.connect(self.delete_point)
        self.ui.pushButtonOK.clicked.connect(self.run)

    def init_table(self):
        self.ui.tableWidget.setRowCount(len(self.points))
        for index, p in enumerate(self.points):
            item0 = QtGui.QTableWidgetItem()
            item0.setCheckState(QtCore.Qt.Checked)
            self.ui.tableWidget.setItem(index, 0, item0)
            self.ui.tableWidget.setItem(index, 1, QtGui.QTableWidgetItem(str(p['src'][0])))
            self.ui.tableWidget.setItem(index, 2, QtGui.QTableWidgetItem(str(p['src'][1])))
            self.ui.tableWidget.setItem(index, 3, QtGui.QTableWidgetItem(str(p['dst'][0])))
            self.ui.tableWidget.setItem(index, 4, QtGui.QTableWidgetItem(str(p['dst'][1])))
            self.ui.tableWidget.setItem(index, 5, QtGui.QTableWidgetItem("-"))
        self.refresh_table()

    def refresh_table(self):
        for i in range(self.ui.tableWidget.rowCount()):
            for j in range(0, 6):
                item = self.ui.tableWidget.item(i, j)
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
            self.ui.tableWidget.item(i, 5).setText("-")
        if len(self.gcp_table) == 0:
            return
        transformation = str(self.ui.transformationsComboBox.currentText())
        result = []
        if transformation == 'Helmert':
            result = janek_transformations.JanekTransform().helm_trans(self.gcp_table)

        if 'Polynomial' in transformation:
            order = int(transformation[-1])
            result = janek_transformations.JanekTransform().polynomial(order, self.gcp_table, 0, 1, 2, 3)

        if len(result) > 0:
            for i in range(self.ui.tableWidget.rowCount()):
                self.ui.tableWidget.item(i, 5).setText(str(result[2][i]))
            self.ui.mXYLineEdit.setText(str(result[3]))
            self.ui.mXLineEdit.setText(str(result[4]))
            self.ui.mYLineEdit.setText(str(result[5]))

    def delete_point(self):
        row = self.ui.tableWidget.currentRow()
        if row < 0:
            return
        del self.points[row]
        self.init_table()
        self.pointDeleted.emit(row)

    def run(self):
        qgis_srs_epsg = self.canvas.mapRenderer().destinationCrs().authid()[5:]
        qgis_srs_epsg = str(globalvars.EPSG_SCR)
        outfile_path = QtGui.QFileDialog.getSaveFileName(
            None,
            'Georeferenced image path',
            self.raster_path[:-len(self.raster_path.split('/')[-1].split('.')[-1]) - 1] + '_EPSG' + qgis_srs_epsg,
            '*.tif'
        )
        methods = ['near', 'bilinear', 'cubic', 'cubicspline', 'lanczos']
        transformations = ['order 1', 'order 2', 'order 3', 'tps', 'line']
        rs_method = methods[self.ui.echantillonnageComboBox.currentIndex()]
        tr_method = transformations[self.ui.transformationsComboBox.currentIndex()]
        cp_method = "NONE"

        gcp_txt = ""
        for i in range(len(self.points_xy)):
            gcp_txt += '-gcp ' + str(self.points_xy[i][0]) + ' ' + str(-self.points_xy[i][1]) + \
                       ' ' + str(self.points_xy[i][2]) + ' ' + str(self.points_xy[i][3]) + ' '
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
            self.accept()
