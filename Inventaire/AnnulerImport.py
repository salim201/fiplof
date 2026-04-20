# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AnnulerImport.ui'
#
# Created: Fri Mar  3 13:51:29 2023
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(706, 533)
        self.gridLayout_3 = QtGui.QGridLayout(Dialog)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.pushButtonRechercher = QtGui.QPushButton(Dialog)
        self.pushButtonRechercher.setObjectName(_fromUtf8("pushButtonRechercher"))
        self.gridLayout_3.addWidget(self.pushButtonRechercher, 1, 0, 1, 1)
        self.pushButtonAfficherTous = QtGui.QPushButton(Dialog)
        self.pushButtonAfficherTous.setObjectName(_fromUtf8("pushButtonAfficherTous"))
        self.gridLayout_3.addWidget(self.pushButtonAfficherTous, 1, 1, 1, 1)
        self.pushButtonSupprimer = QtGui.QPushButton(Dialog)
        self.pushButtonSupprimer.setObjectName(_fromUtf8("pushButtonSupprimer"))
        self.gridLayout_3.addWidget(self.pushButtonSupprimer, 1, 2, 1, 1)
        self.tableWidgetImports = QtGui.QTableWidget(Dialog)
        self.tableWidgetImports.setObjectName(_fromUtf8("tableWidgetImports"))
        self.tableWidgetImports.setColumnCount(2)
        self.tableWidgetImports.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetImports.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetImports.setHorizontalHeaderItem(1, item)
        self.gridLayout_3.addWidget(self.tableWidgetImports, 2, 0, 1, 3)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.dateEditDateImport = QtGui.QDateEdit(self.groupBox)
        self.dateEditDateImport.setEnabled(False)
        self.dateEditDateImport.setCalendarPopup(True)
        self.dateEditDateImport.setObjectName(_fromUtf8("dateEditDateImport"))
        self.gridLayout.addWidget(self.dateEditDateImport, 1, 2, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.lineEditRefImport = QtGui.QLineEdit(self.groupBox)
        self.lineEditRefImport.setEnabled(False)
        self.lineEditRefImport.setObjectName(_fromUtf8("lineEditRefImport"))
        self.gridLayout.addWidget(self.lineEditRefImport, 0, 2, 1, 1)
        self.checkBox = QtGui.QCheckBox(self.groupBox)
        self.checkBox.setText(_fromUtf8(""))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout.addWidget(self.checkBox, 0, 0, 1, 1)
        self.checkBox_2 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_2.setText(_fromUtf8(""))
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.gridLayout.addWidget(self.checkBox_2, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Annuler import", None))
        self.pushButtonRechercher.setText(_translate("Dialog", "Rechercher", None))
        self.pushButtonAfficherTous.setText(_translate("Dialog", "Afficher Tous", None))
        self.pushButtonSupprimer.setText(_translate("Dialog", "Supprimer", None))
        item = self.tableWidgetImports.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Ref Import", None))
        item = self.tableWidgetImports.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Date Import", None))
        self.groupBox.setTitle(_translate("Dialog", "Recherche", None))
        self.label_2.setText(_translate("Dialog", "Date:", None))
        self.label.setText(_translate("Dialog", "Référence:", None))

