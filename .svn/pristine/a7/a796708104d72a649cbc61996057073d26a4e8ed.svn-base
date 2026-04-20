#coding: utf-8
from PyQt4.QtGui import *
from PyQt4 import QtGui, QtCore
from qgis.core import *
from qgis.gui import *
import datetime, time
import globalvars, os, sys, psycopg2

from .Historique import Ui_Dialog


class HistoriqueRun(QDialog):
    def __init__(self, connection, parent):
        QDialog.__init__(self)
        self.connection = connection
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        #self.ui.treeWidget.addTopLevelItem(QTreeWidgetItem('Certificat'))
        self.setModal(True)
        self.idCF = parent.idCF
        self.initDB()
        self.initActions()
        self.readHistorique()

    def initActions(self):
        self.ui.pushButtonFermer.clicked.connect(self.close)

    def writeInHistorique(self, idCF, typeOp, dateOp):
        try:
            self.cur.execute("INSERT INTO historique(idcertificat, typeoperation, dateoperation) "
                             "VALUES(%s, %s, %s)",(idCF,typeOp,dateOp))
            self.connection.commit()
        except:
            self.connection.rollback()

    def readHistorique(self):
        try:
            self.cur.execute("SELECT typeoperation FROM historique WHERE idcertificat = %s",(self.idCF,))
            typeOperations = self.cur.fetchall()
            print typeOperations
            self.showInTableOperations(typeOperations)
        except StandardError as e:
            print e

        try:
            self.cur.execute("SELECT numerocertificat, numerodemande, "
                             "typecertificat, datecreation, dateedition,"
                             "datedelivrance, memo, idfokontany FROM certificat WHERE idcertificat = %s", (self.idCF,))
            data = self.cur.fetchall()
            #print data
            self.showInTableCertificat(data)
        except StandardError as e:
            print e

    def showInTableCertificat(self, data):
        print data
        self.ui.tableWidget_2.setRowCount(0)
        self.ui.treeWidget.setHeaderLabel(data[0][0])
        i = 0
        while i < len(data):
            rowPosition = self.ui.tableWidget_2.rowCount()
            self.ui.tableWidget_2.insertRow(rowPosition)
            #self.idsTitre.append(data[i][0])
            j = 0
            while j < len(data[i]) - 1:
                if j == 3 or j == 4 or j == 5:
                    if data[i][j] is not None:
                        self.ui.tableWidget_2.setItem(rowPosition, j, QtGui.QTableWidgetItem(unicode(data[i][j].strftime('%d/%m/%Y'))))
                else:
                    self.ui.tableWidget_2.setItem(rowPosition, j , QtGui.QTableWidgetItem(unicode(data[i][j])))
                j = j + 1
            i = i + 1

    def showInTableOperations(self, data):
        print data
        self.ui.tableWidget.setRowCount(0)
        i = 0
        while i < len(data):
            rowPosition = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(rowPosition)
            #self.idsTitre.append(data[i][0])
            j = 0
            while j < len(data[i]):
                self.ui.tableWidget.setItem(rowPosition, j , QtGui.QTableWidgetItem(unicode(data[i][j])))
                j = j + 1
            i = i + 1

    def initDB(self):
        self.cur = self.connection.cursor()

    def __del__(self):
        self.cur.close()
