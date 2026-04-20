# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ListePointsCardinaux.ui'
#
# Created: Tue Nov 28 10:56:05 2017
#      by: PyQt4 UI code generator 4.11.2
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
        Dialog.resize(467, 305)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(30, 240, 421, 51))
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.groupBox)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(140, 10, 277, 41))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.BTEnregistrer = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.BTEnregistrer.setObjectName(_fromUtf8("BTEnregistrer"))
        self.horizontalLayout.addWidget(self.BTEnregistrer)
        self.BTSupprimer = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.BTSupprimer.setObjectName(_fromUtf8("BTSupprimer"))
        self.horizontalLayout.addWidget(self.BTSupprimer)
        self.BTFermer = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.BTFermer.setObjectName(_fromUtf8("BTFermer"))
        self.horizontalLayout.addWidget(self.BTFermer)
        self.tableWidget = QtGui.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(30, 11, 421, 221))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(150)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Liste des points cardinaux", None))
        self.BTEnregistrer.setText(_translate("Dialog", "Enregistrer", None))
        self.BTSupprimer.setText(_translate("Dialog", "Supprimer", None))
        self.BTFermer.setText(_translate("Dialog", "Fermer", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Position", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Fanondroana", None))

