# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'EchangeCF.ui'
#
# Created: Tue Aug 21 06:11:32 2018
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
        Dialog.resize(400, 257)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 9, 381, 241))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalGroupBox = QtGui.QGroupBox(self.groupBox)
        self.horizontalGroupBox.setGeometry(QtCore.QRect(10, 50, 361, 35))
        self.horizontalGroupBox.setObjectName(_fromUtf8("horizontalGroupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalGroupBox)
        self.horizontalLayout.setContentsMargins(6, 6, 10, 6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonDetails = QtGui.QPushButton(self.horizontalGroupBox)
        self.pushButtonDetails.setObjectName(_fromUtf8("pushButtonDetails"))
        self.horizontalLayout.addWidget(self.pushButtonDetails)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 30, 141, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayoutWidget = QtGui.QWidget(self.groupBox)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 90, 361, 80))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tableWidget = QtGui.QTableWidget(self.gridLayoutWidget)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.horizontalGroupBox1 = QtGui.QGroupBox(self.groupBox)
        self.horizontalGroupBox1.setGeometry(QtCore.QRect(10, 180, 361, 41))
        self.horizontalGroupBox1.setObjectName(_fromUtf8("horizontalGroupBox1"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.horizontalGroupBox1)
        self.horizontalLayout_4.setContentsMargins(6, 6, 10, 6)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.enregistrer = QtGui.QPushButton(self.horizontalGroupBox1)
        self.enregistrer.setObjectName(_fromUtf8("enregistrer"))
        self.horizontalLayout_4.addWidget(self.enregistrer)
        self.annuler = QtGui.QPushButton(self.horizontalGroupBox1)
        self.annuler.setObjectName(_fromUtf8("annuler"))
        self.horizontalLayout_4.addWidget(self.annuler)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Echange de CF", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Permutation  des propriétaires", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDetails.setText(QtGui.QApplication.translate("Dialog", "Details ...", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Liste de propriétaires :", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(QtGui.QApplication.translate("Dialog", "N° Certificat", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(QtGui.QApplication.translate("Dialog", "Type propriétaires", None, QtGui.QApplication.UnicodeUTF8))
        self.enregistrer.setText(QtGui.QApplication.translate("Dialog", "Enregistrer ", None, QtGui.QApplication.UnicodeUTF8))
        self.annuler.setText(QtGui.QApplication.translate("Dialog", "Annuler", None, QtGui.QApplication.UnicodeUTF8))

