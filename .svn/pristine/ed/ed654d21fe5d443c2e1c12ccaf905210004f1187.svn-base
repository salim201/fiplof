# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Oppositions.ui'
#
# Created: Tue May 08 11:50:43 2018
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!


from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
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
from PyQt4.QtCore import *
import datetime
from datetime import *
from PyQt4 import QtCore, QtGui

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
    def __init__(self, parent):
        self.clickID = ""
        self.dlg = ""
        self.row = 0
        self.column = 0
        self.opposition = []
        self.parent = parent
        self.connection = self.parent.connection
        self.idopposition = self.parent.idopposition
        self.iddemande = self.parent.iddemande
        self.ndemande = self.parent.numDemande
        self.dlg = ""
        self.ddDate = 0


        #        self.dateDemandeLineEdit.setInputMask(_fromUtf8(""))


    def setupUi(self, Opposition):
        self.dlg = Opposition
        Opposition.setObjectName(_fromUtf8("Opposition"))
        Opposition.setWindowModality(QtCore.Qt.WindowModal)
        Opposition.resize(930, 373)
        Opposition.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        Opposition.setSizeGripEnabled(True)
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
        self.dateOppositionDateEdit.setObjectName(_fromUtf8("dateOppositionDateEdit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.dateOppositionDateEdit)
        self.dateDemandeLabel = QtGui.QLabel(self.formGroupBox)
        self.dateDemandeLabel.setObjectName(_fromUtf8("dateDemandeLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.dateDemandeLabel)
        self.dateDemandeDateEdit = QtGui.QDateEdit(self.formGroupBox)
        self.dateDemandeDateEdit.setObjectName(_fromUtf8("dateDemandeDateEdit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.dateDemandeDateEdit)
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
        self.pushButton = QtGui.QPushButton(self.horizontalGroupBox)
        self.pushButton.setCheckable(False)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtGui.QPushButton(self.horizontalGroupBox)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.gridLayoutWidget = QtGui.QWidget(Opposition)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(350, 20, 571, 271))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tableWidget = QtGui.QTableWidget(self.gridLayoutWidget)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(8)
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
        self.tableWidget.horizontalHeader().setDefaultSectionSize(100)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(33)
        self.tableWidget.verticalHeader().setMinimumSectionSize(43)
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

        self.retranslateUi(Opposition)
        QtCore.QMetaObject.connectSlotsByName(Opposition)


        self.dateOppositionDateEdit.setEnabled(True)
        self.dateOppositionDateEdit.setCalendarPopup(True)
        self.dateOppositionDateEdit.setObjectName(_fromUtf8("dateOppositionDateEdit"))
        self.dateOppositionDateEdit.setDisplayFormat("dd/MM/yyyy")
        self.dateOppositionDateEdit.setDate(QDate.currentDate())

        self.dateDemandeDateEdit.setEnabled(True)
        self.dateDemandeDateEdit.setCalendarPopup(True)
        self.dateDemandeDateEdit.setObjectName(_fromUtf8("dateOppositionDateEdit"))
        self.dateDemandeDateEdit.setDisplayFormat("dd/MM/yyyy")
        self.dateDemandeDateEdit.setDate(QDate.currentDate())

        self.dateReglementDateEdit.setEnabled(True)
        self.dateReglementDateEdit.setCalendarPopup(True)
        self.dateReglementDateEdit.setObjectName(_fromUtf8("dateOppositionDateEdit"))
        self.dateReglementDateEdit.setDisplayFormat("dd/MM/yyyy")
        self.dateReglementDateEdit.setDate(QDate.currentDate())


        self.pushButton.clicked.connect(self.loadInGrid)
        self.pushButton_5.clicked.connect(self.saveOpposition)
        self.tableWidget.cellClicked.connect(self.cellSelected)
        self.dateOppositionDateEdit.dateChanged.connect(self.evaluateDateReconnaissance)

        cursor = self.connection.cursor()

        if self.iddemande != 0:

            print
            " self.iddemande != 0: "
            cursor.execute("Select op.dateopposition, op.datedemande, op.typeopposition , op.description, "
                           " op.datereglement, op.naturereglement, op.descriptionreglement, d.numdemande "
                           " from oppositions op"
                           " INNER JOIN demande d ON op.iddemande = d.iddemande"
                           "  WHERE op.iddemande=%s", [int(self.iddemande)])
            oppositions = cursor.fetchall()
            self.dtemp = []

            for d in oppositions:

                # 2018 - 05 - 09
                year, month, day = d[0].isoformat().split("-")
                # dateOpposition = d[0].strftime('%d/%m/%y')
                dateOpposition = day + "/" + month + "/" + year

                year, month, day = d[1].isoformat().split("-")
                # dateDemande = d[1].strftime('%d/%m/%y')
                dateDemande = day + "/" + month + "/" + year

                year, month, day = d[4].isoformat().split("-")
                # dateReglement = d[4].strftime('%d/%m/%y')
                dateReglement = day + "/" + month + "/" + year

                data = (str(d[7]), str(d[2]), str(d[3]), dateOpposition, dateDemande, str(d[5]),
                        str(d[6]), dateReglement)
                # data = ("450","aaaa","bbbb","cccc","dddd","eeeeee")
                try:
                    self.addValueTable(data)
                except Exception as e:
                    print(e)

    def evaluateDateReconnaissance(self):
        print
        "first test of all"
        from datetime import datetime
        from datetime import date
        date_format = "%d/%m/%Y"
        # a = datetime.strptime(self.dateDemandeLineEdit.text(), date_format)
        # b = datetime.strptime(self.dateDeReconnaissanceLineEdit.text(), date_format)

        a = self.dateDemandeDateEdit.text()
        a = a.split("/")
        a = date(int(a[2]), int(a[1]), int(a[0]))

        b = self.dateOppositionDateEdit.text()
        b = b.split("/")
        b = date(int(b[2]), int(b[1]), int(b[0]))

        diffdate = b - a

        self.ddDate = diffdate.days
        if self.ddDate < 1:
            QMessageBox.critical(self.dateOppositionDateEdit, "Erreur",
                                 "La date opposition doit etre superieur a la date demande")
            self.dateOppositionDateEdit.setFocus(Qt.Qt.OtherFocusReason)

            # self.dateDeReconnaissanceLineEdit.setText("")
            # self.dateDeReconnaissanceLineEdit.setReadOnly(True)

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
        for i in range(len(data)):
            item = QtGui.QTableWidgetItem()
            print
            "at add_values range"
            print
            str(data[i])
            item.setText(_translate("", str(data[i]), None))
            print
            "at add_values range out"
            self.tableWidget.setItem(rowPosition, i, item)

    def addValueTable(self, data):
        self.add_values(data)

    def saveOpposition(self):

        currentRW = self.tableWidget.currentRow()
        rowCount = self.tableWidget.rowCount()
        columnCount = self.tableWidget.columnCount()

        self.evaluateDateReconnaissance()

        if self.ddDate < 1:
            self.dateOppositionDateEdit.setFocus(Qt.Qt.OtherFocusReason)
            return

        if currentRW == -1:
            QMessageBox.critical(self.tableWidget, "Erreur", "Veuillez entrer au moins choisir une ligne opposition")
            return
        else:
            #            print self.row
            #            print self.column
            xRow = 0
            yColumn = 0
            selItems = self.tableWidget.selectedItems()
            #            for item in selItems:
            #                print item.text()

            selIndex = self.tableWidget.selectedIndexes()

            print
            len(selIndex)
            print
            "selIndex out"

            dataOpp = []
            dtemp = []
            i = 1

            for item in selIndex:
                print
                "selectedIndexes", item.row(), item.column()
                dtemp = [self.tableWidget.item(item.row(), 0).text(), self.tableWidget.item(item.row(), 1).text(),
                         self.tableWidget.item(item.row(), 2).text(), self.tableWidget.item(item.row(), 3).text(),
                         self.tableWidget.item(item.row(), 4).text(), self.tableWidget.item(item.row(), 5).text(),
                         self.tableWidget.item(item.row(), 6).text(), self.tableWidget.item(item.row(), 7).text()]
                dataOpp.append(dtemp)
                i = i + 1

            self.parent.opposition = dataOpp
            size = len(dataOpp)
            i = j = 0

            self.dlg.close()

    def cellSelected(self, row, column):

        self.clickID = self.tableWidget.item(row, 2).text()
        print
        self.clickID
        print
        "self.clickID out"
        print
        self.tableWidget.item(row, 0).text()
        print
        self.tableWidget.item(row, 1).text()
        print
        self.tableWidget.item(row, 1).text()

        dateopposition = self.tableWidget.item(row, 3).text()
        day, month, year = dateopposition.split("/")
        print
        month
        print
        day
        print
        year
        # 09/05/18

        dateopposition = date(int(year), int(month), int(day))
        self.dateOppositionDateEdit.setDate(dateopposition)

        dateDemande = self.tableWidget.item(row, 4).text()
        day, month, year = dateDemande.split("/")
        dateDemande = date(int(year), int(month), int(day))
        self.dateDemandeDateEdit.setDate(dateDemande)

        # self.ui.typeOppositionComboBox.setText(self.ui.tableWidget.item(row, 1).text())
        self.textEdit.setText(self.tableWidget.item(row, 2).text())

        dateReglement = self.tableWidget.item(row, 7).text()
        day, month, year = dateReglement.split("/")
        dateReglement = date(int(year), int(month), int(day))
        self.dateReglementDateEdit.setDate(dateReglement)

        # self.ui.plainTextEdit.setText(self.ui.tableWidget.item(row, 6).text())





        self.row = row

    def loadInGrid(self):
        print
        " click on test "
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

        data = (self.ndemande, self.typeOpp, self.desc, self.dateOpp, self.dateDemande, self.natureReglement,
                self.descReglement, self.dateReglement)
        # data = ("450","aaaa","bbbb","cccc","dddd","eeeeee")

        print
        "dtOpp in"
        print
        data
        print
        "dtOpp out"

        # self.dateOppositionDateEdit.setText("")
        # self.dateDemandeDateEdit.setText("")
        # self.textEdit.setText("")
        # self.dateReglementDateEdit.setText("")
        # self.plainTextEdit.setText("")
        try:
            print
            "add table"
            self.addValueTable(data)
        except Exception as e:
            print(e)

    def retranslateUi(self, Opposition):
        Opposition.setWindowTitle(QtGui.QApplication.translate("Opposition", "Opposition ", None, QtGui.QApplication.UnicodeUTF8))
        self.formGroupBox.setTitle(QtGui.QApplication.translate("Opposition", "OPPOSITION", None, QtGui.QApplication.UnicodeUTF8))
        self.dateOppositionLabel.setText(QtGui.QApplication.translate("Opposition", "Date Opposition", None, QtGui.QApplication.UnicodeUTF8))
        self.dateDemandeLabel.setText(QtGui.QApplication.translate("Opposition", "Date Demande", None, QtGui.QApplication.UnicodeUTF8))
        self.typeOppositionComboBox.setItemText(0, QtGui.QApplication.translate("Opposition", "SUR LIMITE", None, QtGui.QApplication.UnicodeUTF8))
        self.typeOppositionComboBox.setItemText(1, QtGui.QApplication.translate("Opposition", "SUR LES DROITS", None, QtGui.QApplication.UnicodeUTF8))
        self.typeOppositionLabel.setText(QtGui.QApplication.translate("Opposition", "Type opposition", None, QtGui.QApplication.UnicodeUTF8))
        self.DescriptionOpp.setText(QtGui.QApplication.translate("Opposition", "Description ", None, QtGui.QApplication.UnicodeUTF8))
        self.formGroupBox1.setTitle(QtGui.QApplication.translate("Opposition", "REGLEMENT", None, QtGui.QApplication.UnicodeUTF8))
        self.dateReglementLabel.setText(QtGui.QApplication.translate("Opposition", "DateReglement", None, QtGui.QApplication.UnicodeUTF8))
        self.natureReglementComboBox.setItemText(0, QtGui.QApplication.translate("Opposition", "ACQUIESCMENT SPONTANE", None, QtGui.QApplication.UnicodeUTF8))
        self.natureReglementComboBox.setItemText(1, QtGui.QApplication.translate("Opposition", "MAIN LEVEE SPONTANNEE", None, QtGui.QApplication.UnicodeUTF8))
        self.natureReglementComboBox.setItemText(2, QtGui.QApplication.translate("Opposition", "ACQUIESCEMENT APRES CONCILIATION", None, QtGui.QApplication.UnicodeUTF8))
        self.natureReglementComboBox.setItemText(3, QtGui.QApplication.translate("Opposition", "MAIN LEVEE  APRES CONCILIATION", None, QtGui.QApplication.UnicodeUTF8))
        self.natureReglementComboBox.setItemText(4, QtGui.QApplication.translate("Opposition", "SENTENCE ARBITRALE", None, QtGui.QApplication.UnicodeUTF8))
        self.natureReglementComboBox.setItemText(5, QtGui.QApplication.translate("Opposition", "DECISION DU TRIBUNAL", None, QtGui.QApplication.UnicodeUTF8))
        self.natureReglementLabel.setText(QtGui.QApplication.translate("Opposition", "Nature reglement", None, QtGui.QApplication.UnicodeUTF8))
        self.DescriptionReglement.setText(QtGui.QApplication.translate("Opposition", "Description", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Opposition", "VALIDER", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("Opposition", "ANNULER", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(QtGui.QApplication.translate("Opposition", "N Demande", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(QtGui.QApplication.translate("Opposition", "Type Opposition", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(QtGui.QApplication.translate("Opposition", "Description Opposition", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(QtGui.QApplication.translate("Opposition", "Date Opposition", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(QtGui.QApplication.translate("Opposition", "Date Demande", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(QtGui.QApplication.translate("Opposition", "Nature Reglement", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(QtGui.QApplication.translate("Opposition", "Description Reglement", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(QtGui.QApplication.translate("Opposition", "Date Reglement", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_5.setText(QtGui.QApplication.translate("Opposition", "ENREGISTRER", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_4.setText(QtGui.QApplication.translate("Opposition", "SUPPRIMER", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("Opposition", "DETAILS ...", None, QtGui.QApplication.UnicodeUTF8))

