# coding: utf-8

import os, os.path, sys
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *
from PyQt4 import QtGui

from .resCalculImpot import Ui_Dialog


class resCalculImpotRun(QDialog):
    def __init__(self, connection):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle(u"Resultat du calcul des impôts")
        self.connection = connection
        self.allImpot = 0
        now = QDate.currentDate()
        self.ui.dateDateEdit.setDate(now)


    def setNewValImpot(self, tabImpot):
        #self.allImpot = 0
        print "Tab impot"
        #self.ui.tableWidget.setRowCount(0)
        print tabImpot
        rowPosition = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(rowPosition)
        self.allImpot = self.allImpot + tabImpot[2]
        j = 1
        print len(tabImpot)
        while j < len(tabImpot):
            #print "j= " + str(j)
            self.ui.tableWidget.setItem(rowPosition, j - 1, QtGui.QTableWidgetItem(unicode(tabImpot[j])))
            j = j + 1

    def totalImpot(self):
        self.ui.totalImpoTLineEdit.setText(str(self.allImpot))

    def resetAllImpot(self):
        self.allImpot = 0