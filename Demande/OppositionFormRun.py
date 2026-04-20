# -*- coding: utf-8 -*-
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

from OppositionForm import Ui_Opposition

class OppositionFormRun(QtGui.QDialog):

    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        print "OPPOSITIONS"
        self.parent = parent
        self.tbOpposition = self.parent.tbOpposition
        self.numDemande = self.parent.numDemande
        self.ui = Ui_Opposition()
        self.ui.setupUi(self)
        self.CreationDemande = ""
        self.coddistrict = 0
        self.codecommune = 0
        self.idfokontany = 0
        self.idparcelle = self.parent.idparcelle
        print 'numdemande'
        print self.numDemande
        self.idopposition = 0
        self.connection = ""
        self.ddDate = 0
        self.connection = self.parent.connection
        self.cursor = self.connection.cursor()
        self.setModal(True)
        self.ui.dateOppositionDateEdit.setCalendarPopup(True)
        self.ui.dateOppositionDateEdit.setDisplayFormat("dd/MM/yyyy")
        self.ui.dateOppositionDateEdit.setDate(QDate.currentDate())
        self.ui.dateDemandeDateEdit.setEnabled(True)
        self.ui.dateDemandeDateEdit.setCalendarPopup(True)
        self.ui.dateDemandeDateEdit.setDisplayFormat("dd/MM/yyyy")
        self.ui.dateDemandeDateEdit.setDate(QDate.currentDate())
        self.ui.BtnAddOpp.clicked.connect(self.add)

    def add(self):
        print "dqdqsdqs"
        self.dateOpp = self.ui.dateOppositionDateEdit.text()
        dtOpp = self.dateOpp.split('/')
        #        dateOpp =  '2013-06-01'
        self.dateDemande = self.ui.dateDemandeDateEdit.text()
        dtDemande = self.dateDemande.split('/')
        #        dateDemande =  '2013-06-01'
        self.typeOpp = self.ui.typeOppositionComboBox.currentText()
        self.desc = self.ui.textEdit.toPlainText()

        try :
            self.cursor.execute("select * from demande where numdemande =%s",[str(self.numDemande)])
            results = self.cursor.fetchone()
            if len(results) >= 1 :
                idDemande = results[0]
        except Exception as e:
            print(e)
            self.connection.rollack()

        try:
            #dateOpposition = o[2]
            #dateOpposition = dateOpposition.split('/')
            dateOpposition = datetime.date(int(dtOpp[2]), int(dtOpp[1]),int(dtOpp[0]))

            #dateDemande = o[3]
            #dateDemande = dateDemande.split('/')
            dateDemande = datetime.date(int(dtDemande[2]), int(dtDemande[1]), int(dtDemande[0]))
            exe = self.cursor.execute(
                "INSERT INTO oppositions (typeopposition,description,dateopposition,datedemande,iddemande,gid)"
                " VALUES (%s,%s,%s,%s,%s,%s) returning idopposition",
                (str(self.typeOpp), str(self.desc), dateOpposition, dateDemande, int(idDemande),
                 self.idparcelle))
            self.connection.commit()
            res = self.cursor.fetchone()
            if res is not None:
                self.idopposition = int(res[0])
            msgBox = QtGui.QMessageBox()
            msgBox.setText("Enregistrement du opposition reussi")
        except Exception as e:
            print(e)
            self.connection.rollback()
        data = (self.desc, self.typeOpp,self.dateDemande, self.dateOpp, self.idopposition)
        if self.idopposition != 0:
            self.add_values(data)
        self.close()

    def delRow(self):
        self.tbOpposition.removeRow(self.selectedRow)

    def cellSelected(self, row, column):
        print " row "
        print row
        self.selectedRow = row


    def add_values(self, data):
        columns = len(data)
        rowPosition = self.tbOpposition.rowCount()
        self.tbOpposition.setColumnCount(columns)
        self.tbOpposition.insertRow(rowPosition)
        for i in range(len(data)):
            item = QtGui.QTableWidgetItem()
            print
            "at add_values range"
            print
            str(data[i])
            item.setText(_translate("", str(data[i]), None))
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            print
            "at add_values range out"
            self.tbOpposition.setItem(rowPosition, i, item)

    def addValueTable(self, data):
        self.add_values(data)


