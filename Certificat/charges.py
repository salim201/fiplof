# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'charges.ui'
#
# Created: Thu Dec 14 21:00:04 2017
#      by: PyQt4 UI code generator 4.11.3
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
        Dialog.resize(414, 305)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btnEnlever = QtGui.QPushButton(self.groupBox)
        self.btnEnlever.setObjectName(_fromUtf8("btnEnlever"))
        self.horizontalLayout_2.addWidget(self.btnEnlever)
        self.btnAjouter = QtGui.QPushButton(self.groupBox)
        self.btnAjouter.setObjectName(_fromUtf8("btnAjouter"))
        self.horizontalLayout_2.addWidget(self.btnAjouter)
        self.btnDetails = QtGui.QPushButton(self.groupBox)
        self.btnDetails.setObjectName(_fromUtf8("btnDetails"))
        self.horizontalLayout_2.addWidget(self.btnDetails)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tableWidget = QtGui.QTableWidget(self.groupBox)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(150)
        self.verticalLayout.addWidget(self.tableWidget)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btnValider = QtGui.QPushButton(Dialog)
        self.btnValider.setObjectName(_fromUtf8("btnValider"))
        self.horizontalLayout.addWidget(self.btnValider)
        self.btnAnnuler = QtGui.QPushButton(Dialog)
        self.btnAnnuler.setObjectName(_fromUtf8("btnAnnuler"))
        self.horizontalLayout.addWidget(self.btnAnnuler)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Charges sur un certificat foncier", None))
        self.groupBox.setTitle(_translate("Dialog", "Liste des charges", None))
        self.btnEnlever.setText(_translate("Dialog", "Enlever", None))
        self.btnAjouter.setText(_translate("Dialog", "Ajouter", None))
        self.btnDetails.setText(_translate("Dialog", "Détails", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Type de charge", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Certificat", None))
        self.btnValider.setText(_translate("Dialog", "Valider", None))
        self.btnAnnuler.setText(_translate("Dialog", "Annuler", None))

