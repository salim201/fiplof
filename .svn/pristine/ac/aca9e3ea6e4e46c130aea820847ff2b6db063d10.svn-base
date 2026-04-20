# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Oppositions.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

import os
import time
import datetime

from PyQt4 import QtGui, QtCore
import sys
import os
import os.path
import qgis
import psycopg2
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from PyQt4 import QtSql
from qgis.gui import *
from PyQt4 import QtGui, uic


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

class Ui_Opposition(object):

    def __init__(self,parent):
        self.clickID = ""
        self.row = 0
        self.column = 0
        self.opposition = []
        self.parent = parent
        self.ndemande = self.parent.numDemande
        self.dlg = ""
        print "at init"

        def NouvelleOpposition(self):
            self.dateOpp = self.dateOppositionDateEdit.text()
            dtOpp = self.dateOpp.split('/')
            #        dateOpp =  '2013-06-01'
            self.dateDemande = self.dateDemandeDateEdit.text()
            dtDemande = self.dateDemande.split('/')
            #        dateDemande =  '2013-06-01'
            self.typeOpp = self.typeOppositionComboBox.currentText()
            self.desc = self.textEdit.toPlainText()
            self.dateReglement = self.dateReglementDateEdit.text()
            dtReglement = self.dateReglement.split('/')
            #        dateReglement = '2013-06-01'
            self.natureReglement = self.natureReglementComboBox.currentText()
            self.descReglement = self.plainTextEdit.toPlainText()

            # connection = psycopg2.connect(database="db_plof_fi", user="postgres", password="1234")
            # cursor = connection.cursor()
            #        exe =cursor.execute("INSERT INTO opposition VALUES (%(date) s,%(date) s,%s,%s,%(date) s,%s,%s)", (dateOpp, dateDemande,typeOpp,desc,dateReglement,natureReglement,descReglement))
            #        exe = cursor.execute(
            #            "INSERT INTO opposition (dateopp,datedemande,typeopp,description,datereg,naturereg,descreg) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING idopp ",
            #            (datetime.date(int(dtOpp[2]), int(dtOpp[1]), int(dtOpp[0])),
            #             datetime.date(int(dtDemande[2]), int(dtDemande[1]), int(dtDemande[0])), self.typeOpp, self.desc,
            #             datetime.date(int(dtReglement[2]), int(dtReglement[1]), int(dtReglement[0])), self.natureReglement,
            #             self.descReglement))

            data = (self.ndemande, self.dateOpp, self.typeOpp, self.desc, self.natureReglement, 45)

            #            slf = qgis.utils.iface.messageBar()
            #            slf.pushMessage("enregistrement Parcelle avec succes", level=QgsMessageBar.SUCCESS)

            #       connection.commit()
            self.dateOppositionLineEdit.setText("")
            self.dateDemandeLineEdit.setText("")
            self.textEditDescription.setText("")
            self.dateReglementLineEdit.setText("")
            self.addValueTable(data)

    def add_values(self, data):
        columns = len(data)
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.setColumnCount(columns)
        self.tableWidget.insertRow(rowPosition)
        # print len(data)
        print "at add_values"
        for i in range(len(data)):
            item = QtGui.QTableWidgetItem()
            print "at add_values range"
            print str(data[i])
            item.setText(_translate("", str(data[i]), None))
            print "at add_values range out"
            self.tableWidget.setItem(rowPosition, i, item)

    def addValueTable(self, data):
        self.add_values(data)


    def setupUi(self, Opposition):
        Opposition.setObjectName(_fromUtf8("Opposition"))
        Opposition.resize(734, 373)
        self.dlg = Opposition
        Opposition.setModal(True)

        self.formGroupBox = QtGui.QGroupBox(Opposition)
        self.formGroupBox.setGeometry(QtCore.QRect(10, 10, 321, 141))
        self.formGroupBox.setObjectName(_fromUtf8("formGroupBox"))
        self.formLayout = QtGui.QFormLayout(self.formGroupBox)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(8, 8, 8, -1)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))

        self.dateOppositionLabel = QtGui.QLabel(self.formGroupBox)
        self.dateOppositionLabel.setObjectName(_fromUtf8("dateOppositionLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.dateOppositionLabel)
        self.dateOppositionDateEdit = QtGui.QDateEdit(self.formGroupBox)
        self.dateOppositionDateEdit.setEnabled(True)
        self.dateOppositionDateEdit.setCalendarPopup(True)
        self.dateOppositionDateEdit.setObjectName(_fromUtf8("dateOppositionDateEdit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.dateOppositionDateEdit)
        self.dateDemandeLabel = QtGui.QLabel(self.formGroupBox)
        self.dateDemandeLabel.setObjectName(_fromUtf8("dateDemandeLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.dateDemandeLabel)
        self.dateDemandeDateEdit = QtGui.QDateEdit(self.formGroupBox)
        self.dateDemandeDateEdit.setObjectName(_fromUtf8("dateDemandeDateEdit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.dateDemandeDateEdit)
        self.dateDemandeDateEdit.setEnabled(True)
        self.dateDemandeDateEdit.setCalendarPopup(True)
        self.textEdit = QtGui.QTextEdit(self.formGroupBox)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.textEdit)
        self.typeOppositionComboBox = QtGui.QComboBox(self.formGroupBox)
        self.typeOppositionComboBox.setObjectName(_fromUtf8("typeOppositionComboBox"))
        self.typeOppositionComboBox.addItem(_fromUtf8(""))
        self.typeOppositionComboBox.addItem(_fromUtf8(""))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.typeOppositionComboBox)
        self.typeOppositionLabel = QtGui.QLabel(self.formGroupBox)
        self.typeOppositionLabel.setObjectName(_fromUtf8("typeOppositionLabel"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.typeOppositionLabel)
        self.DescriptionOpp = QtGui.QLabel(self.formGroupBox)
        self.DescriptionOpp.setObjectName(_fromUtf8("DescriptionOpp"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.DescriptionOpp)
        self.formGroupBox1 = QtGui.QGroupBox(Opposition)
        self.formGroupBox1.setGeometry(QtCore.QRect(10, 160, 321, 138))
        self.formGroupBox1.setObjectName(_fromUtf8("formGroupBox1"))
        self.formLayout_2 = QtGui.QFormLayout(self.formGroupBox1)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setContentsMargins(8, 8, 8, -1)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.dateReglementLabel = QtGui.QLabel(self.formGroupBox1)
        self.dateReglementLabel.setObjectName(_fromUtf8("dateReglementLabel"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.dateReglementLabel)
        self.dateReglementDateEdit = QtGui.QDateEdit(self.formGroupBox1)
        self.dateReglementDateEdit.setObjectName(_fromUtf8("dateReglementDateEdit"))
        self.dateReglementDateEdit.setEnabled(True)
        self.dateReglementDateEdit.setCalendarPopup(True)

        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.dateReglementDateEdit)
        self.plainTextEdit = QtGui.QPlainTextEdit(self.formGroupBox1)
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.plainTextEdit)
        self.natureReglementComboBox = QtGui.QComboBox(self.formGroupBox1)
        self.natureReglementComboBox.setObjectName(_fromUtf8("natureReglementComboBox"))
        self.natureReglementComboBox.addItem(_fromUtf8(""))
        self.natureReglementComboBox.addItem(_fromUtf8(""))
        self.natureReglementComboBox.addItem(_fromUtf8(""))
        self.natureReglementComboBox.addItem(_fromUtf8(""))
        self.natureReglementComboBox.addItem(_fromUtf8(""))
        self.natureReglementComboBox.addItem(_fromUtf8(""))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.natureReglementComboBox)
        self.natureReglementLabel = QtGui.QLabel(self.formGroupBox1)
        self.natureReglementLabel.setObjectName(_fromUtf8("natureReglementLabel"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.natureReglementLabel)
        self.DescriptionReglement = QtGui.QLabel(self.formGroupBox1)
        self.DescriptionReglement.setObjectName(_fromUtf8("DescriptionReglement"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.DescriptionReglement)
        self.horizontalGroupBox = QtGui.QGroupBox(Opposition)
        self.horizontalGroupBox.setGeometry(QtCore.QRect(10, 310, 321, 41))
        self.horizontalGroupBox.setObjectName(_fromUtf8("horizontalGroupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalGroupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))

        self.pushButtonValider = QtGui.QPushButton(self.horizontalGroupBox)
        self.pushButtonValider.setObjectName(_fromUtf8("pushButtonValider"))
        self.horizontalLayout.addWidget(self.pushButtonValider)
        self.pushButtonValider.setEnabled(True)

        self.pushButton_2 = QtGui.QPushButton(self.horizontalGroupBox)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.gridLayoutWidget = QtGui.QWidget(Opposition)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(350, 20, 361, 271))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tableWidget = QtGui.QTableWidget(self.gridLayoutWidget)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)

        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.horizontalGroupBox_2 = QtGui.QGroupBox(Opposition)
        self.horizontalGroupBox_2.setGeometry(QtCore.QRect(350, 310, 361, 41))
        self.horizontalGroupBox_2.setObjectName(_fromUtf8("horizontalGroupBox_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalGroupBox_2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton_5 = QtGui.QPushButton(self.horizontalGroupBox_2)
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.horizontalLayout_2.addWidget(self.pushButton_5)
        self.pushButton_4 = QtGui.QPushButton(self.horizontalGroupBox_2)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.horizontalLayout_2.addWidget(self.pushButton_4)
        self.pushButton_3 = QtGui.QPushButton(self.horizontalGroupBox_2)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.pushButton_2.setCheckable(True)
        self.tableWidget.setSelectionBehavior(1)

        #self.pushButtonValider.clicked.connect(self.NouvelleOpposition)
        try:
            self.pushButtonValider.clicked.connect(self.loadInGrid)
            self.pushButton_5.clicked.connect(self.saveOpposition)
        except Exception as e:
            print(e)

        self.retranslateUi(Opposition)
        QtCore.QMetaObject.connectSlotsByName(Opposition)


    def saveOpposition(self):

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
            dataOpp = []
            dtemp = []
            i = 1
            for item in selIndex:
                print
                "selectedIndexes", item.row(), item.column()
                dtemp = [self.tableWidget.item(item.row(), 0).text(), self.tableWidget.item(item.row(), 1).text(),
                         self.tableWidget.item(item.row(), 2).text()]
                dataOpp.append(dtemp)
                i = i + 1

            self.parent.opposition = dataOpp
            size = len(dataOpp)
            i = j = 0

            self.dlg.close()


    def loadInGrid(self):
        print " click on test "
        self.dateOpp = self.dateOppositionDateEdit.text()
        dtOpp = self.dateOpp.split('/')
        self.dateDemande = self.dateDemandeDateEdit.text()
        dtDemande = self.dateDemande.split('/')
        self.typeOpp = self.typeOppositionComboBox.currentText()
        self.desc = self.textEdit.toPlainText()

        self.dateReglement = self.dateReglementDateEdit.text()
        dtReglement = self.dateReglement.split('/')
        self.natureReglement = self.natureReglementComboBox.currentText()
        self.descReglement = self.plainTextEdit.toPlainText()

        data = (self.ndemande,self.typeOpp,self.dateOpp,self.desc, self.natureReglement,45)
        #data = ("450","aaaa","bbbb","cccc","dddd","eeeeee")

        print "dtOpp in"
        print data
        print "dtOpp out"

        #self.dateOppositionDateEdit.setText("")
        #self.dateDemandeDateEdit.setText("")
        #self.textEdit.setText("")
        #self.dateReglementDateEdit.setText("")
        #self.plainTextEdit.setText("")
        try:
            print "add table"
            self.addValueTable(data)
        except Exception as e:
            print(e)


    def retranslateUi(self, Opposition):
        Opposition.setWindowTitle(_translate("Opposition", "Dialog", None))
        self.formGroupBox.setTitle(_translate("Opposition", "OPPOSITION", None))
        self.dateOppositionLabel.setText(_translate("Opposition", "Date Opposition", None))
        self.dateDemandeLabel.setText(_translate("Opposition", "Date Demande", None))
        self.typeOppositionLabel.setText(_translate("Opposition", "Type opposition", None))

        self.typeOppositionComboBox.setItemText(0, _translate("Opposition", "SUR LIMITE", None))
        self.typeOppositionComboBox.setItemText(1, _translate("Opposition", "SUR LES DROITS", None))

        self.DescriptionOpp.setText(_translate("Opposition", "Description ", None))
        self.formGroupBox1.setTitle(_translate("Opposition", "REGLEMENT", None))
        self.dateReglementLabel.setText(_translate("Opposition", "DateReglement", None))
        self.natureReglementLabel.setText(_translate("Opposition", "Nature reglement", None))

        self.natureReglementComboBox.setItemText(0, _translate("Opposition", "ACQUIESCMENT SPONTANE", None))
        self.natureReglementComboBox.setItemText(1, _translate("Opposition", "MAIN LEVEE SPONTANNEE", None))
        self.natureReglementComboBox.setItemText(2, _translate("Opposition", "ACQUIESCEMENT APRES CONCILIATION", None))
        self.natureReglementComboBox.setItemText(3, _translate("Opposition", "MAIN LEVEE  APRES CONCILIATION", None))
        self.natureReglementComboBox.setItemText(4, _translate("Opposition", "SENTENCE ARBITRALE", None))
        self.natureReglementComboBox.setItemText(5, _translate("Opposition", "DECISION DU TRIBUNAL", None))

        self.DescriptionReglement.setText(_translate("Opposition", "Description", None))
        self.pushButtonValider.setText(_translate("Opposition", "VALIDER", None))
        self.pushButton_2.setText(_translate("Opposition", "ANNULER", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Opposition", "N Demande", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Opposition", "Type Demande", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Opposition", "Description", None))

        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Opposition", "Nature reglement", None))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Opposition", "Type Demande", None))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Opposition", "Description", None))

        self.pushButton_5.setText(_translate("Opposition", "ENREGISTRER", None))
        self.pushButton_4.setText(_translate("Opposition", "SUPPRIMER", None))
        self.pushButton_3.setText(_translate("Opposition", "DETAILS ...", None))

