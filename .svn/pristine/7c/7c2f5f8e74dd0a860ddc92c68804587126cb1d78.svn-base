import os, os.path, sys
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *

from .ListePointsCardinaux import Ui_Dialog
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class ListePointsCardinauxRun(QDialog):
    def __init__(self, connection):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setModal(True)
        self.connection = connection
        self.initDB()
        self.prevNbrColonne = 0
        self.initActions()
        self.prevNbrColonne = self.readPointsCardinaux()

    def initActions(self):
        self.ui.tableWidget.cellChanged.connect(self.newRow)

    def initDB(self):
        self.cur = self.connection.cursor()

    def newRow(self, row, column):
        if row == self.ui.tableWidget.rowCount() - 1 and column == 1 :
            if self.ui.tableWidget.item(row, column).text() != '':
                rowPosition = self.ui.tableWidget.rowCount()
                self.ui.tableWidget.insertRow(rowPosition)

    def readPointsCardinaux(self):
        self.ui.tableWidget.setRowCount(0)
        self.cur.execute("SELECT idpointscardinaux, position, fanondroana FROM pointscardinaux ORDER BY idpointscardinaux")
        pointsCardinaux = self.cur.fetchall()

        i = 0
        while i < len(pointsCardinaux):
            self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
            j = 0
            while j < len(pointsCardinaux[i]) - 1:
                print pointsCardinaux[i][j+1]
                print "listeDesPoints"
                self.ui.tableWidget.setItem(i, j, QtGui.QTableWidgetItem(unicode(pointsCardinaux[i][j+1])))
                j = j + 1

            i = i + 1

        return self.ui.tableWidget.rowCount()

    def savePtsCard(self):
        i = self.prevNbrColonne - 1
        while i < self.ui.tableWidget.rowCount():
            try:
                self.cur.execute("INSERT INTO pointscardinaux (position, fanondroana) VALUES (%s, %s)", (unicode(self.ui.tableWidget.item(i, 0).text()).encode('utf-8'), unicode(self.ui.tableWidget.item(i, 1).text()).encode('utf-8')))
                self.connection.commit()
                i = i + 1
            except:
                i = i + 1


    def __del__(self):
        self.cur.close()
