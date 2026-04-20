# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ListeContribuables.ui'
#
# Created: Tue Jan 30 15:01:47 2018
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.setEnabled(True)
        Dialog.resize(717, 337)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 0, 700, 81))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.checkBoxTousParFokontany = QtGui.QCheckBox(self.groupBox)
        self.checkBoxTousParFokontany.setGeometry(QtCore.QRect(360, 20, 121, 17))
        self.checkBoxTousParFokontany.setObjectName(_fromUtf8("checkBoxTousParFokontany"))
        self.checkBoxGroupeeParFokontany = QtGui.QCheckBox(self.groupBox)
        self.checkBoxGroupeeParFokontany.setGeometry(QtCore.QRect(360, 50, 190, 17))
        self.checkBoxGroupeeParFokontany.setObjectName(_fromUtf8("checkBoxGroupeeParFokontany"))
        self.lineEditAnnee = QtGui.QLineEdit(self.groupBox)
        self.lineEditAnnee.setGeometry(QtCore.QRect(110, 50, 220, 20))
        self.lineEditAnnee.setObjectName(_fromUtf8("lineEditAnnee"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 50, 100, 13))
        self.label.setObjectName(_fromUtf8("label"))
        self.btnRechercher = QtGui.QPushButton(self.groupBox)
        self.btnRechercher.setGeometry(QtCore.QRect(580, 50, 90, 23))
        self.btnRechercher.setObjectName(_fromUtf8("btnRechercher"))
        self.comboFokontany = QtGui.QComboBox(self.groupBox)
        self.comboFokontany.setGeometry(QtCore.QRect(110, 20, 190, 22))
        self.comboFokontany.setEditable(True)
        self.comboFokontany.setObjectName(_fromUtf8("comboFokontany"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 20, 100, 13))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.tableWidget = QtGui.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(10, 90, 701, 191))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(7)
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
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 290, 700, 41))
        self.groupBox_2.setTitle(_fromUtf8(""))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.btnImprimerListe = QtGui.QPushButton(self.groupBox_2)
        self.btnImprimerListe.setGeometry(QtCore.QRect(530, 10, 75, 23))
        self.btnImprimerListe.setObjectName(_fromUtf8("btnImprimerListe"))
        self.btnFermer = QtGui.QPushButton(self.groupBox_2)
        self.btnFermer.setGeometry(QtCore.QRect(620, 10, 75, 23))
        self.btnFermer.setObjectName(_fromUtf8("btnFermer"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Liste des contribuables", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Recherche", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxTousParFokontany.setText(QtGui.QApplication.translate("Dialog", "Tous/ par fokontany", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxGroupeeParFokontany.setText(QtGui.QApplication.translate("Dialog", "Parcelle groupé par fokontany", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Année :", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRechercher.setText(QtGui.QApplication.translate("Dialog", "Rechercher", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Fokontany :", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(QtGui.QApplication.translate("Dialog", "Nom", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(QtGui.QApplication.translate("Dialog", "Date de naissance", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(QtGui.QApplication.translate("Dialog", "Lieu", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(QtGui.QApplication.translate("Dialog", "CIN", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(QtGui.QApplication.translate("Dialog", "Hetra (tany)", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(QtGui.QApplication.translate("Dialog", "Hetra (trano)", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(QtGui.QApplication.translate("Dialog", "Total", None, QtGui.QApplication.UnicodeUTF8))
        self.btnImprimerListe.setText(QtGui.QApplication.translate("Dialog", "Imprimer liste", None, QtGui.QApplication.UnicodeUTF8))
        self.btnFermer.setText(QtGui.QApplication.translate("Dialog", "Fermer", None, QtGui.QApplication.UnicodeUTF8))

