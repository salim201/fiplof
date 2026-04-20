# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ListeTypesAire.ui'
#
# Created: Sat Mar 17 04:17:43 2018
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
        Dialog.resize(467, 305)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableWidget = QtGui.QTableWidget(Dialog)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(150)
        self.verticalLayout.addWidget(self.tableWidget)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.BTEnregistrer = QtGui.QPushButton(self.groupBox)
        self.BTEnregistrer.setObjectName(_fromUtf8("BTEnregistrer"))
        self.horizontalLayout.addWidget(self.BTEnregistrer)
        self.BTSupprimer = QtGui.QPushButton(self.groupBox)
        self.BTSupprimer.setObjectName(_fromUtf8("BTSupprimer"))
        self.horizontalLayout.addWidget(self.BTSupprimer)
        self.BTFermer = QtGui.QPushButton(self.groupBox)
        self.BTFermer.setObjectName(_fromUtf8("BTFermer"))
        self.horizontalLayout.addWidget(self.BTFermer)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Liste de types d\'aire à statut spécifique", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(QtGui.QApplication.translate("Dialog", "Type", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(QtGui.QApplication.translate("Dialog", "Karazany", None, QtGui.QApplication.UnicodeUTF8))
        self.BTEnregistrer.setText(QtGui.QApplication.translate("Dialog", "Enregistrer", None, QtGui.QApplication.UnicodeUTF8))
        self.BTSupprimer.setText(QtGui.QApplication.translate("Dialog", "Supprimer", None, QtGui.QApplication.UnicodeUTF8))
        self.BTFermer.setText(QtGui.QApplication.translate("Dialog", "Fermer", None, QtGui.QApplication.UnicodeUTF8))

