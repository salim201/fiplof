# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Opposition.ui'
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
#from qgis.utils import *
from PyQt4 import QtGui, uic
#from qgis.utils import iface

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
        self.opposition = []
        self.parent = parent
        print "at init"


    def resolve(self, name, basepath=None):
        if not basepath:
            basepath = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(basepath, name)


    def deleteRow(self):
        connection = psycopg2.connect(host=self.db_config.db_host, port=self.db_config.db_port,
                                      database=self.db_config.db_name, user=self.db_config.db_user,
                                      password=self.db_config.db_pass)
        cursor = connection.cursor()

        cursor.execute("delete from  opposition WHERE idopp=%s", [int(self.clickID)])
        connection.commit()
        self.tableWidget.removeRow(self.row)


    def getTableItems(self, row):
        n = self.tableWidget.columnCount()
        fileList = list()
        header_labels = ['Column 1', 'Column 2', 'Column 3', 'Column 4', 'Column 5', 'Column 6']
        self.tableWidget.setHorizontalHeaderLabels(header_labels)
        for i in xrange(0, n):
            print i
            fileList.append(self.tableWidget.item(row, i).text())
            print fileList
        print fileList

        return fileList

    def add_values(self, data):
        columns = len(data)
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.setColumnCount(columns)
        self.tableWidget.insertRow(rowPosition)
        # print len(data)
        for i in range(len(data)):
            item = QtGui.QTableWidgetItem()
            item.setText(_translate("", str(data[i]), None))
            self.tableWidget.setItem(rowPosition, i, item)

    def addValueTable(self,data):
        self.add_values(data)

    def NouvelleOpposition(self,iface):
        self.dateOpp = self.dateOppositionLineEdit.text()
        dtOpp = self.dateOpp.split('/')
        print "date opp"
        print dtOpp

        #        dateOpp =  '2013-06-01'
        self.dateDemande = self.dateDemandeLineEdit.text()
        dtDemande = self.dateDemande.split('/')
        #        dateDemande =  '2013-06-01'
        self.typeOpp = self.typeOppositionComboBox.currentText()
        self.desc = self.textEditDescription.toPlainText()
        self.dateReglement = self.dateReglementLineEdit.text()
        dtReglement = self.dateReglement.split('/')
        #        dateReglement = '2013-06-01'
        self.natureReglement = self.natureReglementComboBox.currentText()
        self.descReglement = self.textEdit.toPlainText()



        connection = psycopg2.connect(database="db_plof_fi", user="postgres", password="")
        cursor = connection.cursor()
        #        exe =cursor.execute("INSERT INTO opposition VALUES (%(date) s,%(date) s,%s,%s,%(date) s,%s,%s)", (dateOpp, dateDemande,typeOpp,desc,dateReglement,natureReglement,descReglement))
#        exe = cursor.execute(
#            "INSERT INTO opposition (dateopp,datedemande,typeopp,description,datereg,naturereg,descreg) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING idopp ",
#            (datetime.date(int(dtOpp[2]), int(dtOpp[1]), int(dtOpp[0])),
#             datetime.date(int(dtDemande[2]), int(dtDemande[1]), int(dtDemande[0])), self.typeOpp, self.desc,
#             datetime.date(int(dtReglement[2]), int(dtReglement[1]), int(dtReglement[0])), self.natureReglement,
#             self.descReglement))


        self.ndemande = self.numDemande
        data = (self.ndemande,self.dateOpp, self.typeOpp,self.desc, self.natureReglement,45)

        slf = qgis.utils.iface.messageBar()
        slf.pushMessage("enregistrement Parcelle avec succes", level=QgsMessageBar.SUCCESS)



 #       connection.commit()
        self.dateOppositionLineEdit.setText("")
        self.dateDemandeLineEdit.setText("")
        self.textEditDescription.setText("")
        self.dateReglementLineEdit.setText("")
        self.addValueTable(data)

    def cellSelected(self, row, column):
        print row
        print column
        self.clickID = self.tableWidget.item(row, 5).text()
        self.row = row
        self.column = column

    def ValidateOppAdd(self):
        currentRW = self.tableWidget.currentRow()
        rowCount = self.tableWidget.rowCount()
        columnCount = self.tableWidget.columnCount()
        if currentRW == -1:
            QMessageBox.critical(self.tableWidget, "Erreur",
                                     "Veuillez entrer au moins choisir une ligne opposition")

        else:
            xRow = 0
            yColumn = 0
            selItems = self.tableWidget.selectedItems()
            selIndex = self.tableWidget.selectedIndexes()
            dataopp = []
            dtemp = []
            i = 1
            for item in selIndex:
                print "selectedIndexes", item.row(), item.column()
                dtemp = [self.tableWidget.item(item.row(), 0).text(), self.tableWidget.item(item.row(), 1).text(),self.tableWidget.item(item.row(), 2).text(),
                             self.tableWidget.item(item.row(), 3).text(), self.tableWidget.item(item.row(), 4).text()]
                dataopp.append(dtemp)
                i = i + 1
            self.opposition = dataopp
            self.parent.opposition = dataopp

    def updateDate(self, *args):
        date = self.calendar.selectedDate()
        self.dateOppositionLineEdit.setText("{}/{}/{}".format(date.day(), date.month(), date.year()))  # output: 20/9/2013
        #        getDate = self.calendar.selectedDate().
        #        self.lineEdit.setText(getDate)
        self.calendar.deleteLater()

    def showCalWid(self):
        self.calendar = QtGui.QCalendarWidget()
        self.calendar.setMinimumDate(QtCore.QDate(1900, 1, 1))
        self.calendar.setMaximumDate(QtCore.QDate(3000, 1, 1))
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.updateDate)
        self.calendar.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.calendar.setStyleSheet('background: white; color: black')
        self.calendar.setGridVisible(True)
        pos = QtGui.QCursor.pos()
        self.calendar.setGeometry(pos.x(), pos.y(), 300, 200)
        self.calendar.show()

    def updateDate1(self, *args):
        date = self.calendar.selectedDate()
        self.dateDemandeLineEdit.setText("{}/{}/{}".format(date.day(), date.month(), date.year()))  # output: 20/9/2013
            #        getDate = self.calendar.selectedDate().
            #        self.lineEdit.setText(getDate)
    def showCalWid1(self):
        self.calendar = QtGui.QCalendarWidget()
        self.calendar.setMinimumDate(QtCore.QDate(1900, 1, 1))
        self.calendar.setMaximumDate(QtCore.QDate(3000, 1, 1))
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.updateDate1)
        self.calendar.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.calendar.setStyleSheet('background: white; color: black')
        self.calendar.setGridVisible(True)
        pos = QtGui.QCursor.pos()
        self.calendar.setGeometry(pos.x(), pos.y(), 300, 200)
        self.calendar.show()

    def updateDate2(self, *args):
        date = self.calendar.selectedDate()
        self.dateReglementLineEdit.setText("{}/{}/{}".format(date.day(), date.month(), date.year()))  # output: 20/9/2013
            #        getDate = self.calendar.selectedDate().
            #        self.lineEdit.setText(getDate)

    def showCalWid2(self):
        self.calendar = QtGui.QCalendarWidget()
        self.calendar.setMinimumDate(QtCore.QDate(1900, 1, 1))
        self.calendar.setMaximumDate(QtCore.QDate(3000, 1, 1))
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.updateDate2)
        self.calendar.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.calendar.setStyleSheet('background: white; color: black')
        self.calendar.setGridVisible(True)
        pos = QtGui.QCursor.pos()
        self.calendar.setGeometry(pos.x(), pos.y(), 300, 200)
        self.calendar.show()




    def setupUi(self, Dialog):

        print "at UI"
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(497, 432)
        Dialog.setFixedSize(497, 432)
        # L h
        Dialog.setMouseTracking(False)
        Dialog.setAcceptDrops(False)
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.formGroupBox = QtGui.QGroupBox(Dialog)
        self.formGroupBox.setGeometry(QtCore.QRect(10, 10, 231, 171))
        self.formGroupBox.setObjectName(_fromUtf8("formGroupBox"))
        self.dateOppositionLabel = QtGui.QLabel(self.formGroupBox)
        self.dateOppositionLabel.setGeometry(QtCore.QRect(7, 24, 75, 16))
        self.dateOppositionLabel.setObjectName(_fromUtf8("dateOppositionLabel"))
        self.dateOppositionLineEdit = QtGui.QLineEdit(self.formGroupBox)
        self.dateOppositionLineEdit.setGeometry(QtCore.QRect(88, 24, 133, 20))
        self.dateOppositionLineEdit.setObjectName(_fromUtf8("dateOppositionLineEdit"))
        self.dateDemandeLabel = QtGui.QLabel(self.formGroupBox)
        self.dateDemandeLabel.setGeometry(QtCore.QRect(7, 50, 70, 16))
        self.dateDemandeLabel.setObjectName(_fromUtf8("dateDemandeLabel"))
        self.dateDemandeLineEdit = QtGui.QLineEdit(self.formGroupBox)
        self.dateDemandeLineEdit.setGeometry(QtCore.QRect(88, 50, 133, 20))
        self.dateDemandeLineEdit.setObjectName(_fromUtf8("dateDemandeLineEdit"))
        self.typeOppositionLabel = QtGui.QLabel(self.formGroupBox)
        self.typeOppositionLabel.setGeometry(QtCore.QRect(7, 76, 75, 16))
        self.typeOppositionLabel.setObjectName(_fromUtf8("typeOppositionLabel"))
        self.typeOppositionComboBox = QtGui.QComboBox(self.formGroupBox)
        self.typeOppositionComboBox.setGeometry(QtCore.QRect(88, 76, 131, 20))
        self.typeOppositionComboBox.setObjectName(_fromUtf8("typeOppositionComboBox"))
        self.typeOppositionComboBox.addItem(_fromUtf8(""))
        self.typeOppositionComboBox.addItem(_fromUtf8(""))

        self.descriptionLabel = QtGui.QLabel(self.formGroupBox)
        self.descriptionLabel.setGeometry(QtCore.QRect(7, 102, 53, 16))
        self.descriptionLabel.setObjectName(_fromUtf8("descriptionLabel"))
        self.textEditDescription = QtGui.QTextEdit(self.formGroupBox)
        self.textEditDescription.setGeometry(QtCore.QRect(88, 102, 136, 62))
        self.textEditDescription.setObjectName(_fromUtf8("textEditDescription"))
        self.pushButtonCalOpp = QtGui.QPushButton(self.formGroupBox)
        self.pushButtonCalOpp.setGeometry(QtCore.QRect(200, 20, 21, 23))
        self.pushButtonCalOpp.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("D:/EN COURS/PYTHON/DatePickerDialog.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonCalOpp.setIcon(icon)
        self.pushButtonCalOpp.setObjectName(_fromUtf8("pushButtonCalOpp"))
        self.pushButtonCalDemande = QtGui.QPushButton(self.formGroupBox)
        self.pushButtonCalDemande.setGeometry(QtCore.QRect(200, 50, 21, 23))
        self.pushButtonCalDemande.setText(_fromUtf8(""))
        self.pushButtonCalDemande.setIcon(icon)
        self.pushButtonCalDemande.setObjectName(_fromUtf8("pushButtonCalDemande"))
        self.formGroupBox_2 = QtGui.QGroupBox(Dialog)
        self.formGroupBox_2.setGeometry(QtCore.QRect(250, 10, 231, 171))
        self.formGroupBox_2.setObjectName(_fromUtf8("formGroupBox_2"))
        self.dateReglementLabel = QtGui.QLabel(self.formGroupBox_2)
        self.dateReglementLabel.setGeometry(QtCore.QRect(7, 24, 74, 16))
        self.dateReglementLabel.setObjectName(_fromUtf8("dateReglementLabel"))
        self.dateReglementLineEdit = QtGui.QLineEdit(self.formGroupBox_2)
        self.dateReglementLineEdit.setGeometry(QtCore.QRect(97, 24, 127, 20))
        self.dateReglementLineEdit.setObjectName(_fromUtf8("dateReglementLineEdit"))
        self.natureReglementLabel = QtGui.QLabel(self.formGroupBox_2)
        self.natureReglementLabel.setGeometry(QtCore.QRect(7, 50, 84, 16))
        self.natureReglementLabel.setObjectName(_fromUtf8("natureReglementLabel"))

        self.natureReglementComboBox = QtGui.QComboBox(self.formGroupBox_2)
        self.natureReglementComboBox.setGeometry(QtCore.QRect(97, 50, 131, 20))
        self.natureReglementComboBox.setObjectName(_fromUtf8("natureReglementComboBox"))
        self.natureReglementComboBox.addItem(_fromUtf8(""))
        self.natureReglementComboBox.addItem(_fromUtf8(""))
        self.natureReglementComboBox.addItem(_fromUtf8(""))
        self.natureReglementComboBox.addItem(_fromUtf8(""))
        self.natureReglementComboBox.addItem(_fromUtf8(""))
        self.natureReglementComboBox.addItem(_fromUtf8(""))


        self.descriptionLabel_2 = QtGui.QLabel(self.formGroupBox_2)
        self.descriptionLabel_2.setGeometry(QtCore.QRect(7, 76, 53, 16))
        self.descriptionLabel_2.setObjectName(_fromUtf8("descriptionLabel_2"))
        self.textEdit = QtGui.QTextEdit(self.formGroupBox_2)
        self.textEdit.setGeometry(QtCore.QRect(97, 76, 127, 88))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.pushButtonCalReglement = QtGui.QPushButton(self.formGroupBox_2)
        self.pushButtonCalReglement.setGeometry(QtCore.QRect(204, 20, 21, 23))
        self.pushButtonCalReglement.setText(_fromUtf8(""))
        self.pushButtonCalReglement.setIcon(icon)
        self.pushButtonCalReglement.setObjectName(_fromUtf8("pushButtonCalReglement"))
        self.horizontalGroupBox = QtGui.QGroupBox(Dialog)
        self.horizontalGroupBox.setGeometry(QtCore.QRect(10, 190, 471, 41))
        self.horizontalGroupBox.setObjectName(_fromUtf8("horizontalGroupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalGroupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButtonAjouterOpp = QtGui.QPushButton(self.horizontalGroupBox)
        self.pushButtonAjouterOpp.setObjectName(_fromUtf8("pushButtonAjouterOpp"))
        self.horizontalLayout.addWidget(self.pushButtonAjouterOpp)
        self.pushButtonDeleteOpp = QtGui.QPushButton(self.horizontalGroupBox)
        self.pushButtonDeleteOpp.setObjectName(_fromUtf8("pushButtonDeleteOpp"))
        self.horizontalLayout.addWidget(self.pushButtonDeleteOpp)
        self.pushButtonDetail = QtGui.QPushButton(self.horizontalGroupBox)
        self.pushButtonDetail.setObjectName(_fromUtf8("pushButtonDetail"))
        self.horizontalLayout.addWidget(self.pushButtonDetail)
        self.gridLayoutWidget = QtGui.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 240, 471, 121))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.tableWidget = QtGui.QTableWidget(self.gridLayoutWidget)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.gridLayout_2.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.horizontalGroupBox1 = QtGui.QGroupBox(Dialog)
        self.horizontalGroupBox1.setGeometry(QtCore.QRect(10, 370, 471, 51))
        self.horizontalGroupBox1.setObjectName(_fromUtf8("horizontalGroupBox1"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalGroupBox1)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButtonValider = QtGui.QPushButton(self.horizontalGroupBox1)
        self.pushButtonValider.setObjectName(_fromUtf8("pushButtonValider"))
        self.horizontalLayout_2.addWidget(self.pushButtonValider)
        self.pushButtonCancel = QtGui.QPushButton(self.horizontalGroupBox1)
        self.pushButtonCancel.setObjectName(_fromUtf8("pushButtonCancel"))
        self.horizontalLayout_2.addWidget(self.pushButtonCancel)


        self.pushButtonCalOpp.clicked.connect(self.showCalWid)
        self.pushButtonCalDemande.clicked.connect(self.showCalWid1)
        self.pushButtonCalReglement.clicked.connect(self.showCalWid2)

        self.pushButtonAjouterOpp.clicked.connect(self.NouvelleOpposition)
        self.tableWidget.cellClicked.connect(self.cellSelected)
        self.pushButtonDeleteOpp.clicked.connect(self.deleteRow)
        self.pushButtonValider.clicked.connect(self.ValidateOppAdd)


        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.formGroupBox.setTitle(_translate("Dialog", "Opposition", None))
        self.dateOppositionLabel.setText(_translate("Dialog", "Date opposition", None))
        self.dateDemandeLabel.setText(_translate("Dialog", "Date demande", None))
        self.typeOppositionLabel.setText(_translate("Dialog", "Type d\'opposition", None))
        self.typeOppositionComboBox.setItemText(0, _translate("Dialog", "SUR LIMITE", None))
        self.typeOppositionComboBox.setItemText(1, _translate("Dialog", "SUR LES DROITS", None))
#        self.typeOppositionLabel.setText(_translate("Dialog", "Type opposition", None))
        self.descriptionLabel.setText(_translate("Dialog", "Description", None))
        self.formGroupBox_2.setTitle(_translate("Dialog", "Reglement", None))
        self.dateReglementLabel.setText(_translate("Dialog", "Date reglement", None))
        self.natureReglementLabel.setText(_translate("Dialog", "Nature reglement", None))
        self.natureReglementComboBox.setItemText(0, _translate("Dialog", "ACQUIESCMENT SPONTANE", None))
        self.natureReglementComboBox.setItemText(1, _translate("Dialog", "MAIN LEVEE SPONTANNEE", None))
        self.natureReglementComboBox.setItemText(2, _translate("Dialog", "ACQUIESCEMENT APRES CONCILIATION", None))
        self.natureReglementComboBox.setItemText(3, _translate("Dialog", "MAIN LEVEE  APRES CONCILIATION", None))
        self.natureReglementComboBox.setItemText(4, _translate("Dialog", "SENTENCE ARBITRALE", None))
        self.natureReglementComboBox.setItemText(5, _translate("Dialog", "DECISION DU TRIBUNAL", None))



        self.descriptionLabel_2.setText(_translate("Dialog", "Description", None))
        self.pushButtonAjouterOpp.setText(_translate("Dialog", "Enregistrer Opposition", None))
        self.pushButtonDeleteOpp.setText(_translate("Dialog", "Supprimer", None))
        self.pushButtonDetail.setText(_translate("Dialog", "Details ...", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "N Demande", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Nouvelle colonne", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Type Opposition", None))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Description", None))
        self.pushButtonValider.setText(_translate("Dialog", "Valider", None))
        self.pushButtonCancel.setText(_translate("Dialog", "Annuler", None))

