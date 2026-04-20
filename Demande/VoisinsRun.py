import os
import sys
import os
import os.path
import psycopg2
import qgis
# from qgis.utils import iface
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
from qgis.gui import *
import time
import datetime
import globalvars
from PyQt4 import QtGui, Qt
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, Qt
from PyQt4 import QtCore, QtGui
from PyQt4 import QtGui, Qt
from PyQt4 import Qt, QtGui
import psycopg2
from psycopg2 import extras
from Utils import Utils
from PyQt4.QtCore import *
import globalvars

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

from Voisins import Ui_Dialog

class VoisinsRun(QtGui.QDialog):

    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.tbVoisin = self.parent.tbVoisin
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.CreationDemande = ""
        self.coddistrict = 0
        self.codecommune = 0
        self.repereID = 0
        self.idfokontany = 0
        self.isVoisin = 0
        self.numDemande =  self.parent.numDemande
        # = self.parent.idparcelle
        print 'numdemande'
        print self.numDemande
        self.idopposition = 0
        self.connection = ""
        self.ddDate = 0
        self.idPointsCardinaux = []
        self.connection = self.parent.connection
        self.cursor = self.connection.cursor()
        self.setModal(True)
        self.ui.pushButton.clicked.connect(self.add)
        self.readPointsCardinaux()

    def add(self):
        print "dqdqsdqs"
        self.isVoisin = 0
        try:
            self.nom = self.ui.nomEtPrNomsLineEdit.text()
            self.repereID = self.ui.comboBox.currentIndex()



            print("REPERE ---")
            print(self.repereID)
            self.currenTextCombo = unicode(self.ui.comboBox.currentText()).encode('utf-8')
            repereID = self.idPointsCardinaux[self.ui.comboBox.currentIndex()]
            data = {}
            data = (self.currenTextCombo, self.nom,repereID)
            self.addValueTable(data)
        except Exception as e:
            print(e)

        self.close()

    def readPointsCardinaux(self):
        print('avant')
        try:
            self.ui.comboBox.clear()
            print("apres !!!")
            self.cursor.execute("SELECT idpointscardinaux, position FROM pointscardinaux ORDER BY idpointscardinaux")
            pointsCardinaux = self.cursor.fetchall()

            print("apres 222!!!")
            i = 0
            while i < len(pointsCardinaux):
                self.idPointsCardinaux.append(pointsCardinaux[i][0])
                print("READ FROM POINTS CARDINAUX")
                print(pointsCardinaux[i][0])
                self.ui.comboBox.addItem(_fromUtf8(pointsCardinaux[i][1]))
                print("READ FROM i1 POINTS CARDINAUX")
                print(pointsCardinaux[i][1])
                i = i + 1
        except Exception as e:
            print(e)
    def delRow(self):
        self.tbOpposition.removeRow(self.selectedRow)
    def cellSelected(self, row, column):
        print " row "
        print row
        self.selectedRow = row


    def add_values(self, data):
        self.isVoisin = 0
        rowPosition = self.tbVoisin.rowCount()
        print('VOISIN DATA')
        print(data[2])
        try:
            columns = len(data)
            i = 0
            if rowPosition >= 1:
                while (i < rowPosition):
                    idD = self.tbVoisin.item(i, 2).text()
                    if int(idD) == int(data[2]):
                        self.isVoisin = 1
                        break
                    i = i + 1

            if self.isVoisin == 1:
                QMessageBox.critical(self.tbVoisin, "Erreur", "Repere deja existant")
                return
            else :
                self.isVoisin = 0
                self.tbVoisin.setColumnCount(columns)
                self.tbVoisin.insertRow(rowPosition)
                for i in range(len(data)):
                    item = QtGui.QTableWidgetItem()
                    item.setText(_translate("", str(data[i]), None))
                    item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                    self.tbVoisin.setItem(rowPosition, i, item)
        except Exception as e:
            print(e)

    def addValueTable(self, data):
        self.add_values(data)


