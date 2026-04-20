# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'separation_bd.ui'
#
# Created: Tue Oct 10 11:54:39 2023
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
        Dialog.resize(506, 307)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableWidget = QtGui.QTableWidget(Dialog)
        self.tableWidget.setMinimumSize(QtCore.QSize(450, 0))
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(200)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.tableWidget)
        self.listWidget = QtGui.QListWidget(Dialog)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.launch = QtGui.QPushButton(Dialog)
        self.launch.setObjectName(_fromUtf8("launch"))
        self.horizontalLayout.addWidget(self.launch)
        self.cancel = QtGui.QPushButton(Dialog)
        self.cancel.setObjectName(_fromUtf8("cancel"))
        self.horizontalLayout.addWidget(self.cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Séparation de base de données", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Commune", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Nom de la base données", None))
        self.launch.setText(_translate("Dialog", "Lancer la séparation", None))
        self.cancel.setText(_translate("Dialog", "Fermer", None))

