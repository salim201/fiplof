# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'OppForm.ui'
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
from qgis.utils import *
from PyQt4 import QtGui, uic
from qgis.utils import iface


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
        self.parent = parent
        self.id_of_new_row = 0
        os.chdir(self.resolve(".."))
        CURRENT_DIR = os.path.dirname("Configuration/DbConfig.py")
        sys.path.append(os.path.dirname(CURRENT_DIR))
        from Configuration import DbConfig
        self.db_config = DbConfig.DbConfig()
#        print self.parent.txt

    def getTableItems(self, row):
        n = self.parent.tableWidget.columnCount()
        fileList = list()
        header_labels = ['Column 1', 'Column 2', 'Column 3', 'Column 4', 'Column 5', 'Column 6']
        parent.tableWidget.setHorizontalHeaderLabels(header_labels)
        for i in xrange(0, n):
            print i
            fileList.append(self.parent.tableWidget.item(row, i).text())
            print fileList
        print fileList

        return fileList

    def add_values(self, data):
        columns = len(data)
        rowPosition = self.parent.tableWidget.rowCount()
        self.parent.tableWidget.setColumnCount(columns)
        self.parent.tableWidget.insertRow(rowPosition)
        # print len(data)
        for i in range(len(data)):
            item = QtGui.QTableWidgetItem()
            item.setText(_translate("", str(data[i]), None))
            self.parent.tableWidget.setItem(rowPosition, i, item)

    def addValueTable(self,data):
        self.add_values(data)


    def NouvelleOpposition(self,iface):
        self.dateOpp = self.dateDeLOppositionLineEdit.text()
        dtOpp = self.dateOpp.split('/')
        print "date opp"
        print dtOpp

        #        dateOpp =  '2013-06-01'
        self.dateDemande = self.dateDemandeLineEdit.text()
        dtDemande = self.dateDemande.split('/')
        #        dateDemande =  '2013-06-01'
        self.typeOpp = self.typeDOppositionComboBox.currentText()
        self.desc = self.textEdit.toPlainText()
        self.dateReglement = self.dateReglementLineEdit.text()
        dtReglement = self.dateReglement.split('/')
        #        dateReglement = '2013-06-01'
        self.natureReglement = self.natureReglementComboBox.currentText()
        self.descReglement = self.textEdit_2.toPlainText()



        connection = psycopg2.connect(database="db_plof_fi", user="postgres", password="")
        cursor = connection.cursor()
        #        exe =cursor.execute("INSERT INTO opposition VALUES (%(date) s,%(date) s,%s,%s,%(date) s,%s,%s)", (dateOpp, dateDemande,typeOpp,desc,dateReglement,natureReglement,descReglement))
        exe = cursor.execute(
            "INSERT INTO opposition (dateopp,datedemande,typeopp,description,datereg,naturereg,descreg) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING idopp ",
            (datetime.date(int(dtOpp[2]), int(dtOpp[1]), int(dtOpp[0])),
             datetime.date(int(dtDemande[2]), int(dtDemande[1]), int(dtDemande[0])), self.typeOpp, self.desc,
             datetime.date(int(dtReglement[2]), int(dtReglement[1]), int(dtReglement[0])), self.natureReglement,
             self.descReglement))

        self.id_of_new_row = cursor.fetchone()[0]
        self.ndemande = ""
        data = (self.ndemande,self.dateOpp, self.typeOpp,self.desc, self.natureReglement, self.id_of_new_row)

        slf = qgis.utils.iface.messageBar()
        slf.pushMessage("enregistrement Parcelle avec succes", level=QgsMessageBar.SUCCESS)

        connection.commit()

        self.addValueTable(data)


#        self.dateDeLOppositionLineEdit.setText("")
#        self.dateDemandeLineEdit.setText("")
#        self.textEdit.setText("")
#        self.textEdit_2.setText("")



#        self.close()


    def updateDate(self, *args):
        date = self.calendar.selectedDate()
        self.dateDeLOppositionLineEdit.setText("{}/{}/{}".format(date.day(), date.month(), date.year()))  # output: 20/9/2013
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
    def updateDate1(self, *args):
        date = self.calendar.selectedDate()
        self.dateDemandeLineEdit.setText("{}/{}/{}".format(date.day(), date.month(), date.year()))  # output: 20/9/2013
            #        getDate = self.calendar.selectedDate().
            #        self.lineEdit.setText(getDate)
    def updateDate2(self, *args):
        date = self.calendar.selectedDate()
        self.dateReglementLineEdit.setText("{}/{}/{}".format(date.day(), date.month(), date.year()))  # output: 20/9/2013
            #        getDate = self.calendar.selectedDate().
            #        self.lineEdit.setText(getDate)
    def __init__(self, parent):
        self.parent = parent
    #       self.id_of_new_row = 0
    #       print self.parent.txt

    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(313, 446)
        self.formGroupBox = QtGui.QGroupBox(Dialog)
        self.formGroupBox.setGeometry(QtCore.QRect(10, 10, 291, 191))
        self.formGroupBox.setObjectName(_fromUtf8("formGroupBox"))
        self.dateDeLOppositionLabel = QtGui.QLabel(self.formGroupBox)
        self.dateDeLOppositionLabel.setGeometry(QtCore.QRect(7, 30, 103, 16))
        self.dateDeLOppositionLabel.setObjectName(_fromUtf8("dateDeLOppositionLabel"))
        self.dateDeLOppositionLineEdit = QtGui.QLineEdit(self.formGroupBox)
        self.dateDeLOppositionLineEdit.setGeometry(QtCore.QRect(116, 30, 161, 20))
        self.dateDeLOppositionLineEdit.setObjectName(_fromUtf8("dateDeLOppositionLineEdit"))
        self.dateDemandeLabel = QtGui.QLabel(self.formGroupBox)
        self.dateDemandeLabel.setGeometry(QtCore.QRect(7, 56, 70, 16))
        self.dateDemandeLabel.setObjectName(_fromUtf8("dateDemandeLabel"))
        self.dateDemandeLineEdit = QtGui.QLineEdit(self.formGroupBox)
        self.dateDemandeLineEdit.setGeometry(QtCore.QRect(116, 56, 161, 20))
        self.dateDemandeLineEdit.setObjectName(_fromUtf8("dateDemandeLineEdit"))
        self.typeDOppositionLabel = QtGui.QLabel(self.formGroupBox)
        self.typeDOppositionLabel.setGeometry(QtCore.QRect(7, 82, 83, 16))
        self.typeDOppositionLabel.setObjectName(_fromUtf8("typeDOppositionLabel"))
        self.typeDOppositionComboBox = QtGui.QComboBox(self.formGroupBox)
        self.typeDOppositionComboBox.setGeometry(QtCore.QRect(116, 82, 161, 20))
        self.typeDOppositionComboBox.setObjectName(_fromUtf8("typeDOppositionComboBox"))
        self.typeDOppositionComboBox.addItem(_fromUtf8(""))
        self.typeDOppositionComboBox.addItem(_fromUtf8(""))
        self.label = QtGui.QLabel(self.formGroupBox)
        self.label.setGeometry(QtCore.QRect(7, 108, 53, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.textEdit = QtGui.QTextEdit(self.formGroupBox)
        self.textEdit.setGeometry(QtCore.QRect(116, 108, 165, 76))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.pushButtonDateOpp = QtGui.QPushButton(self.formGroupBox)
        self.pushButtonDateOpp.setGeometry(QtCore.QRect(260, 30, 21, 21))
        self.pushButtonDateOpp.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("D:/EN COURS/PYTHON/DatePickerDialog.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonDateOpp.setIcon(icon)
        self.pushButtonDateOpp.setObjectName(_fromUtf8("pushButtonDateOpp"))
        self.pushButtonDatedemande = QtGui.QPushButton(self.formGroupBox)
        self.pushButtonDatedemande.setGeometry(QtCore.QRect(260, 56, 21, 20))
        self.pushButtonDatedemande.setText(_fromUtf8(""))
        self.pushButtonDatedemande.setIcon(icon)
        self.pushButtonDatedemande.setObjectName(_fromUtf8("pushButtonDatedemande"))
        self.formGroupBox1 = QtGui.QGroupBox(Dialog)
        self.formGroupBox1.setGeometry(QtCore.QRect(10, 210, 291, 171))
        self.formGroupBox1.setObjectName(_fromUtf8("formGroupBox1"))
        self.dateReglementLabel = QtGui.QLabel(self.formGroupBox1)
        self.dateReglementLabel.setGeometry(QtCore.QRect(11, 32, 74, 16))
        self.dateReglementLabel.setObjectName(_fromUtf8("dateReglementLabel"))
        self.dateReglementLineEdit = QtGui.QLineEdit(self.formGroupBox1)
        self.dateReglementLineEdit.setGeometry(QtCore.QRect(101, 32, 181, 20))
        self.dateReglementLineEdit.setObjectName(_fromUtf8("dateReglementLineEdit"))
        self.natureReglementLabel = QtGui.QLabel(self.formGroupBox1)
        self.natureReglementLabel.setGeometry(QtCore.QRect(11, 58, 84, 16))
        self.natureReglementLabel.setObjectName(_fromUtf8("natureReglementLabel"))
        self.natureReglementComboBox = QtGui.QComboBox(self.formGroupBox1)
        self.natureReglementComboBox.setGeometry(QtCore.QRect(101, 58, 181, 20))
        self.natureReglementComboBox.setObjectName(_fromUtf8("natureReglementComboBox"))

        self.natureReglementComboBox.addItem(_fromUtf8(""))
        self.natureReglementComboBox.addItem(_fromUtf8(""))
        self.natureReglementComboBox.addItem(_fromUtf8(""))
        self.natureReglementComboBox.addItem(_fromUtf8(""))
        self.natureReglementComboBox.addItem(_fromUtf8(""))
        self.natureReglementComboBox.addItem(_fromUtf8(""))

        self.label_2 = QtGui.QLabel(self.formGroupBox1)
        self.label_2.setGeometry(QtCore.QRect(11, 84, 53, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.textEdit_2 = QtGui.QTextEdit(self.formGroupBox1)
        self.textEdit_2.setGeometry(QtCore.QRect(101, 84, 179, 76))
        self.textEdit_2.setObjectName(_fromUtf8("textEdit_2"))
        self.pushButtonDateReglement = QtGui.QPushButton(self.formGroupBox1)
        self.pushButtonDateReglement.setGeometry(QtCore.QRect(260, 30, 21, 20))
        self.pushButtonDateReglement.setText(_fromUtf8(""))
        self.pushButtonDateReglement.setIcon(icon)
        self.pushButtonDateReglement.setObjectName(_fromUtf8("pushButtonDateReglement"))
        self.horizontalGroupBox = QtGui.QGroupBox(Dialog)
        self.horizontalGroupBox.setGeometry(QtCore.QRect(10, 390, 291, 41))
        self.horizontalGroupBox.setObjectName(_fromUtf8("horizontalGroupBox"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalGroupBox)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButtonEnregistrer = QtGui.QPushButton(self.horizontalGroupBox)
        self.pushButtonEnregistrer.setObjectName(_fromUtf8("pushButtonEnregistrer"))
        self.horizontalLayout_2.addWidget(self.pushButtonEnregistrer)
        self.pushButtonAnnuler = QtGui.QPushButton(self.horizontalGroupBox)
        self.pushButtonAnnuler.setObjectName(_fromUtf8("pushButtonAnnuler"))
        self.horizontalLayout_2.addWidget(self.pushButtonAnnuler)

        self.pushButtonDateOpp.clicked.connect(self.showCalWid)
        self.pushButtonDatedemande.clicked.connect(self.showCalWid1)
        self.pushButtonDateReglement.clicked.connect(self.showCalWid2)

        self.pushButtonEnregistrer.clicked.connect(self.NouvelleOpposition)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):

        Dialog.setWindowTitle(_translate("Dialog", "Ajout nouvelle opposition", None))
        self.formGroupBox.setTitle(_translate("Dialog", "Opposition", None))
        self.dateDeLOppositionLabel.setText(_translate("Dialog", "Date de l\'opposition *", None))
        self.dateDemandeLabel.setText(_translate("Dialog", "Date demande", None))
        self.typeDOppositionLabel.setText(_translate("Dialog", "Type d\'opposition", None))
        self.typeDOppositionComboBox.setItemText(0, _translate("Dialog", "SUR LIMITE", None))
        self.typeDOppositionComboBox.setItemText(1, _translate("Dialog", "SUR LES DROITS", None))
        self.label.setText(_translate("Dialog", "Description", None))
        self.formGroupBox1.setTitle(_translate("Dialog", "Reglement", None))
        self.dateReglementLabel.setText(_translate("Dialog", "Date reglement", None))
        self.natureReglementLabel.setText(_translate("Dialog", "Nature reglement", None))
        self.natureReglementComboBox.setItemText(0, _translate("Dialog", "ACQUIESCMENT SPONTANE", None))
        self.natureReglementComboBox.setItemText(1, _translate("Dialog", "MAIN LEVEE SPONTANNEE", None))
        self.natureReglementComboBox.setItemText(2, _translate("Dialog", "ACQUIESCEMENT APRES CONCILIATION", None))
        self.natureReglementComboBox.setItemText(3, _translate("Dialog", "MAIN LEVEE  APRES CONCILIATION", None))
        self.natureReglementComboBox.setItemText(4, _translate("Dialog", "SENTENCE ARBITRALE", None))
        self.natureReglementComboBox.setItemText(5, _translate("Dialog", "DECISION DU TRIBUNAL", None))
        self.label_2.setText(_translate("Dialog", "Description", None))
        self.pushButtonEnregistrer.setText(_translate("Dialog", "Enregistrer", None))
        self.pushButtonAnnuler.setText(_translate("Dialog", "Annuler", None))

