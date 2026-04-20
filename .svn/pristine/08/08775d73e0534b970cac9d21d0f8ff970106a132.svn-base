# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RechercheDemandeCertificat.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
import time
import datetime
from PyQt4 import QtCore, QtGui
import psycopg2
from Ui_certificatCreation import Ui_certificatCreation
from Configuration import DbConfig
#from PyQt4 import QtCore, QtGui
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
    def __init__(self):
        self.db_config = DbConfig.DbConfig()

    def callCreateCF(self):
        certificatCreation = Ui_certificatCreation()
        result = certificatCreation.exec_()
    
    def updateDateDemande (self,*args):
        date = self.calendar.selectedDate()
        self.lineEdit_3.setText("{}/{}/{}".format(date.day(),date.month(), date.year())) # output: 20/9/2013
        self.calendar.deleteLater()
    
    def updateDateAu (self,*args):
        date = self.calendar.selectedDate()
        self.lineEdit_4.setText("{}/{}/{}".format(date.day(),date.month(), date.year())) # output: 20/9/2013
        self.calendar.deleteLater()
        
    def showCalWidDatDemande(self):
        self.calendar = QtGui.QCalendarWidget()
        self.calendar.setMinimumDate(QtCore.QDate(1900, 1, 1))
        self.calendar.setMaximumDate(QtCore.QDate(3000, 1, 1))
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.updateDateDemande)
        self.calendar.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.calendar.setStyleSheet('background: white; color: black')
        self.calendar.setGridVisible(True)
        pos = QtGui.QCursor.pos()
        self.calendar.setGeometry(pos.x(), pos.y(),300,200)
        self.calendar.show()
    
    def showCalWidAu(self):
        self.calendar = QtGui.QCalendarWidget()
        self.calendar.setMinimumDate(QtCore.QDate(1900, 1, 1))
        self.calendar.setMaximumDate(QtCore.QDate(3000, 1, 1))
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.updateDateAu)
        self.calendar.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.calendar.setStyleSheet('background: white; color: black')
        self.calendar.setGridVisible(True)
        pos = QtGui.QCursor.pos()
        self.calendar.setGeometry(pos.x(), pos.y(),300, 200)
        self.calendar.show()
    
    def conex (self):
        connection = psycopg2.connect(host=self.db_config.db_host, port=self.db_config.db_port, database=self.db_config.db_name, user=self.db_config.db_user, password=self.db_config.db_pass)
        cursor = connection.cursor()
        cursor.execute( "select  gid,numdemande,nomdemandeur,surface,titre,feuille,partie,parcelle,etat from parcelle_d")
#        cursor.execute("select  numdemande,nomdemandeur,surface,titre,feuille,partie,parcelle,titre_r,etat_cf from demande")
        self.data=cursor.fetchall()

    def getTableItems(self,row):
        n = self.tableWidget.columnCount()
        fileList = list()
        for i in range(0, n):
            print(i)
            fileList.append(self.tableWidget.item(row, i).text())
            print(fileList)
        return fileList
        
    def getAttrib(self):
        numDemande=self.lineEdit.text()
        nomDemandeur=self.lineEdit_2.text()
        dateDemande=self.lineEdit_3.text()
        dtDemande=dateDemande.split('/')
        dateAu=self.lineEdit_4.text()
        dtDateAu=dateAu.split('/')
        
        connection = psycopg2.connect(host=self.db_config.db_host, port=self.db_config.db_port, database=self.db_config.db_name, user=self.db_config.db_user, password=self.db_config.db_pass)
        cursor = connection.cursor()
#        exe =cursor.execute("INSERT INTO opposition VALUES (%(date) s,%(date) s,%s,%s,%(date) s,%s,%s)", (dateOpp, dateDemande,typeOpp,desc,dateReglement,natureReglement,descReglement))
        cursor.execute("select numdemande,nomdemandeur,surface,titre,feuille,partie,parcelle,titre_r,etat_cf from demande where nomdemandeur= %(nomDemandeur)s OR numdemande=%(numDemande)s", {"nomDemandeur": nomDemandeur, "numDemande":numDemande})
#        data=(numDemande,nomDemandeur, dateDemande,dateAu)
        self.data=cursor.fetchall()
        connection.commit()
    
    def add_values(self,data):
        i=0
        j=0
        nb_row = len(data)
        lignes=len(data)
        columns =  9
        self.tableWidget.setRowCount(nb_row)
        self.tableWidget.setColumnCount(columns)
        
        for i in range(lignes):
            for j in range(columns):
                item = QtGui.QTableWidgetItem(data[i][j])
                item.setText(_translate("", str(data[i][j]), None))
                self.tableWidget.setItem(i, j, item)
                print(data[i][j])
        self.tableWidget.cellClicked.connect(self.cellSelected)
    def cellSelected(self, row, column):
        if column!=0:
            return
        ID =self.tableWidget.item(row, column).text()
        print ("celll selected")
        print (ID)
        canvas = qgis.utils.iface.mapCanvas()
        cLayer = canvas.currentLayer()
        mc = qgis.utils.iface.mapCanvas()
        for layer in mc.layers():
            if layer.type() == layer.VectorLayer:
                layer.removeSelection()

        mc.refresh()
        cLayer.select(int(ID))
#        cLayer.select(496)

        canvas.zoomToSelected(cLayer)
 #       print self.getTableItems (row)
    def rechercheBT(self):
        self.conex()
        self.add_values(self.data)
        
    def btrecherche(self):
        self.getAttrib()
        self.add_values(self.data)
    
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(409, 488)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 371, 151))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.checkBox = QtGui.QCheckBox(self.groupBox)
        self.checkBox.setGeometry(QtCore.QRect(20, 20, 141, 17))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.lineEdit = QtGui.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(160, 20, 191, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.checkBox_2 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_2.setGeometry(QtCore.QRect(20, 50, 121, 17))
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.lineEdit_2 = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_2.setGeometry(QtCore.QRect(160, 50, 191, 20))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.checkBox_3 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_3.setGeometry(QtCore.QRect(20, 80, 111, 17))
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.lineEdit_3 = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_3.setGeometry(QtCore.QRect(160, 80, 191, 20))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.checkBox_4 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_4.setGeometry(QtCore.QRect(20, 110, 70, 17))
        self.checkBox_4.setObjectName(_fromUtf8("checkBox_4"))
        self.lineEdit_4 = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_4.setGeometry(QtCore.QRect(160, 110, 191, 20))
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.pushButton_8 = QtGui.QPushButton(self.groupBox)
        self.pushButton_8.setGeometry(QtCore.QRect(330, 80, 21, 23))
        self.pushButton_8.setText(_fromUtf8(""))
        self.pushButton_8.setObjectName(_fromUtf8("pushButton_8"))
        self.pushButton_9 = QtGui.QPushButton(self.groupBox)
        self.pushButton_9.setGeometry(QtCore.QRect(330, 110, 21, 23))
        self.pushButton_9.setText(_fromUtf8(""))
        self.pushButton_9.setObjectName(_fromUtf8("pushButton_9"))
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 160, 371, 61))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.pushButton = QtGui.QPushButton(self.groupBox_2)
        self.pushButton.setGeometry(QtCore.QRect(20, 20, 121, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_2.setGeometry(QtCore.QRect(264, 20, 91, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.groupBox_3 = QtGui.QGroupBox(Dialog)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 220, 371, 80))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.pushButton_3 = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_3.setGeometry(QtCore.QRect(220, 30, 41, 31))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_4 = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_4.setGeometry(QtCore.QRect(270, 30, 41, 31))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.groupBox_4 = QtGui.QGroupBox(Dialog)
        self.groupBox_4.setGeometry(QtCore.QRect(20, 310, 371, 141))
        self.groupBox_4.setTitle(_fromUtf8(""))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.tableWidget = QtGui.QTableWidget(self.groupBox_4)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 351, 121))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(9)
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
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        self.pushButton_5 = QtGui.QPushButton(Dialog)
        self.pushButton_5.setGeometry(QtCore.QRect(150, 450, 75, 23))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.pushButton_6 = QtGui.QPushButton(Dialog)
        self.pushButton_6.setGeometry(QtCore.QRect(230, 450, 75, 23))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.pushButton_7 = QtGui.QPushButton(Dialog)
        self.pushButton_7.setGeometry(QtCore.QRect(310, 450, 75, 23))
        self.pushButton_7.setObjectName(_fromUtf8("pushButton_7"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton_7, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.pushButton_8.clicked.connect(self.showCalWidDatDemande)
        self.pushButton_9.clicked.connect(self.showCalWidAu)
        self.pushButton.clicked.connect(self.rechercheBT)
        self.pushButton_2.clicked.connect(self.btrecherche)
        self.pushButton_6.clicked.connect(self.callCreateCF)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.groupBox.setTitle(_translate("Dialog", "Critère de recherche", None))
        self.checkBox.setText(_translate("Dialog", "Numero Demande", None))
        self.checkBox_2.setText(_translate("Dialog", "Nom demandeur", None))
        self.checkBox_3.setText(_translate("Dialog", "Du Date demande", None))
        self.checkBox_4.setText(_translate("Dialog", "Au :", None))
        self.groupBox_2.setTitle(_translate("Dialog", "GroupBox", None))
        self.pushButton.setText(_translate("Dialog", "Afficher tous ...", None))
        self.pushButton_2.setText(_translate("Dialog", "Rechercher", None))
        self.groupBox_3.setTitle(_translate("Dialog", "Selection sur carte", None))
        self.pushButton_3.setText(_translate("Dialog", "...", None))
        self.pushButton_4.setText(_translate("Dialog", "c..", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Numero du Demandeur", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Nom du demandeur", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Surface", None))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Titre", None))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "Feuille", None))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Dialog", "Partie", None))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Dialog", "Parcelle", None))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("Dialog", "Titre_r", None))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("Dialog", "Etat", None))
        self.pushButton_5.setText(_translate("Dialog", "Details ...", None))
        self.pushButton_6.setText(_translate("Dialog", "Selectionner", None))
        self.pushButton_7.setText(_translate("Dialog", "Quitter", None))

