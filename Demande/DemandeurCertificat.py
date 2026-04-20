# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DemandeurCertificat.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

import os
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import *

import psycopg2
import os
import sys
import qgis
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

class Ui_Dialog(object):

    def __init__(self,parent):
        self.clickID = ""
        self.row = 0
        self.column = 0
        self.parent = parent
        self.connection = self.parent.connection
        self.iddemande = self.parent.iddemande
        self.demandeurs = []
        os.chdir(self.resolve(".."))
        dr = os.getcwd()
        sys.path.append(os.path.dirname(dr))
        from Configuration import DbConfig
        #        from Configuration import DbConfig
        self.db_config = DbConfig.DbConfig()


    def addValueTable(self,data):
        columns = len(data)
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.setColumnCount(columns)
        self.tableWidget.insertRow(rowPosition)

        # print len(data)
        for i in range(len(data)):
            item = QtGui.QTableWidgetItem()
            item.setText(_translate("", str(data[i]), None))
            self.tableWidget.setItem(rowPosition, i, item)

    def resolve(self, name, basepath=None):
        if not basepath:
            basepath = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(basepath, name)

    def deleteDemandeurs(self):

        cursor = self.connection.cursor()

        if self.iddemande != 0 :
            print "delete"
            cursor.execute("delete from  avoir_dmd WHERE iddemandeur =%s", [int(self.clickID)])
            cursor.execute("delete from  demandeur_d WHERE iddemandeur=%s", [int(self.clickID)])
            self.connection.commit()

        self.tableWidget.removeRow(self.row)
        print "delete row"

    def cellSelected(self, row, column):

        self.clickID = self.tableWidget.item(row, 2).text()
        print "self.clickID in"
        print self.clickID
        print "self.clickID out"

        print "self.tableWidget.item(row, 3).text()"
        print self.tableWidget.item(row, 0).text()

        print "self.tableWidget.item(row, 4).text()"
        print self.tableWidget.item(row, 1).text()

        self.nomLineEdit.setText(self.tableWidget.item(row, 0).text())
        self.prenomLineEdit.setText(self.tableWidget.item(row, 1).text())

        self.row = row



    def addDemandeurs(self):
        self.nom = self.nomLineEdit.text()
        self.prenom = self.prenomLineEdit.text()

        cursor = self.connection.cursor()
        print "connection in "
        print self.nom
        print self.prenom
        print self.prenom
        print "connection out"
        self.dtemp = []

        if ( (str(self.nom) != "") & (str(self.prenom) != "")) :
            print "dqdqs"
            self.dtemp.append(str(self.nom))
            self.dtemp.append(str(self.prenom))
            self.demandeurs.append(self.dtemp)
            #exe = cursor.execute("INSERT INTO demandeur (nom,prenom) VALUES (%s,%s) RETURNING id ",(str(self.nom), str(self.prenom)))
            #connection.commit()
            #self.id_of_new_row = cursor.fetchone()[0]
            #data = (self.nom, self.prenom, self.id_of_new_row)
            data = (self.nom, self.prenom, 1)
            self.addValueTable(data)

        self.nomLineEdit.setText("")
        self.prenomLineEdit.setText("")
        return  self.demandeurs
        #


    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(325, 337)
        Dialog.setModal(True)
        self.dlg = Dialog

        self.horizontalGroupBox = QtGui.QGroupBox(Dialog)
        self.horizontalGroupBox.setGeometry(QtCore.QRect(10, 100, 311, 41))
        self.horizontalGroupBox.setObjectName(_fromUtf8("horizontalGroupBox"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalGroupBox)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButtonAjouter = QtGui.QPushButton(self.horizontalGroupBox)
        self.pushButtonAjouter.setObjectName(_fromUtf8("pushButtonAjouter"))
        self.horizontalLayout_2.addWidget(self.pushButtonAjouter)
        self.pushButtonEnlever = QtGui.QPushButton(self.horizontalGroupBox)
        self.pushButtonEnlever.setObjectName(_fromUtf8("pushButtonEnlever"))
        self.horizontalLayout_2.addWidget(self.pushButtonEnlever)
        self.verticalLayoutWidget = QtGui.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 150, 311, 131))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableWidget = QtGui.QTableWidget(self.verticalLayoutWidget)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalGroupBox_2 = QtGui.QGroupBox(Dialog)
        self.horizontalGroupBox_2.setGeometry(QtCore.QRect(10, 290, 311, 41))
        self.horizontalGroupBox_2.setObjectName(_fromUtf8("horizontalGroupBox_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalGroupBox_2)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.pushButtonOk = QtGui.QPushButton(self.horizontalGroupBox_2)
        self.pushButtonOk.setObjectName(_fromUtf8("pushButtonOk"))
        self.horizontalLayout_3.addWidget(self.pushButtonOk)
        self.pushButtonAnnuler = QtGui.QPushButton(self.horizontalGroupBox_2)
        self.pushButtonAnnuler.setObjectName(_fromUtf8("pushButtonAnnuler"))
        self.horizontalLayout_3.addWidget(self.pushButtonAnnuler)
        self.formGroupBox = QtGui.QGroupBox(Dialog)
        self.formGroupBox.setGeometry(QtCore.QRect(10, 10, 311, 80))
        self.formGroupBox.setObjectName(_fromUtf8("formGroupBox"))
        self.formLayout = QtGui.QFormLayout(self.formGroupBox)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(6, 16, 10, -1)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.nomLabel = QtGui.QLabel(self.formGroupBox)
        self.nomLabel.setObjectName(_fromUtf8("nomLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.nomLabel)
        self.nomLineEdit = QtGui.QLineEdit(self.formGroupBox)
        self.nomLineEdit.setObjectName(_fromUtf8("nomLineEdit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.nomLineEdit)
        self.prenomLabel = QtGui.QLabel(self.formGroupBox)
        self.prenomLabel.setObjectName(_fromUtf8("prenomLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.prenomLabel)
        self.prenomLineEdit = QtGui.QLineEdit(self.formGroupBox)
        self.prenomLineEdit.setObjectName(_fromUtf8("prenomLineEdit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.prenomLineEdit)
        self.horizontalGroupBox.raise_()
        self.verticalLayoutWidget.raise_()
        self.horizontalGroupBox_2.raise_()
        self.formGroupBox.raise_()
        cursor = self.connection.cursor()

        if self.iddemande != 0 :
            cursor.execute("SELECT d.iddemandeur,d.nom,d.prenom   FROM demandeur_d d "
                       " INNER JOIN avoir_dmd avd ON d.iddemandeur = avd.iddemandeur"
                       " INNER JOIN demande dmd   ON avd.iddemande = dmd.iddemande"
                       " WHERE avd.iddemande=%s", [int(self.iddemande)])
            demandeurs = cursor.fetchall()
            self.dtemp = []

            for d in demandeurs :
                print "indentation"
                self.dtemp.append(str(d[1]))
                self.dtemp.append(str(d[2]))
                self.demandeurs.append(self.dtemp)
                data = (str(d[1]), str(d[2]),int(d[0]))
                self.addValueTable(data)
        else :
            print " self.iddemande autres"
        self.pushButtonAjouter.clicked.connect(self.addDemandeurs)
        self.pushButtonOk.clicked.connect(self.saveAll)
        self.tableWidget.cellClicked.connect(self.cellSelected)
        self.pushButtonEnlever.clicked.connect(self.deleteDemandeurs)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def saveAll(self):

        currentRW = self.tableWidget.currentRow()
        rowCount = self.tableWidget.rowCount()
        columnCount = self.tableWidget.columnCount()

        if currentRW == -1:
            QMessageBox.critical(self.tableWidget, "Erreur", "Veuillez entrer au moins choisir une ligne opposition")
        else:
            #            print self.row
            #            print self.column
            xRow = 0
            yColumn = 0
            selItems = self.tableWidget.selectedItems()
            #            for item in selItems:
            #                print item.text()
            selIndex = self.tableWidget.selectedIndexes()
            dataDmd = []
            dtemp = []
            i = 1
            for item in selIndex:
                print "selectedIndexes", item.row(), item.column()
                dtemp = [self.tableWidget.item(item.row(), 0).text(), self.tableWidget.item(item.row(), 1).text(),
                         self.tableWidget.item(item.row(), 2).text()]
                dataDmd.append(dtemp)
                i = i + 1


            self.parent.demandeurs = dataDmd
            size = len(dataDmd)
            i = j = 0
            print "demandeurs form in"
            print dataDmd
            print "demandeurs form out"
            for demandeur in dataDmd:
                print "demandeur in"
                #print str(demandeur[1])
                print "demandeur out"

            self.dlg.close()

            #                print self.tableWidget.item(int(item.row()),int(2)).text()


            #            for xRow in rowCount:
            #                for yColumn in columnCount :
            #                    if self.tableWidget.selectedItems()
            #            print currentRW

            #        print rowCount
            #        print columnCount

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Demandeurs de certificat", None))
        self.pushButtonAjouter.setText(_translate("Dialog", " + Ajouter", None))
        self.pushButtonEnlever.setText(_translate("Dialog", "- Enlever", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Nom", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Prenom", None))
        self.pushButtonOk.setText(_translate("Dialog", "OK", None))
        self.pushButtonAnnuler.setText(_translate("Dialog", "Annuler", None))
        self.nomLabel.setText(_translate("Dialog", "Nom", None))
        self.prenomLabel.setText(_translate("Dialog", "Prenom", None))

