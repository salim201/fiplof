# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RecalculImpot.ui'
#
# Created: Wed Sep 19 11:21:01 2018
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
        Dialog.resize(414, 345)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.comboBoxForfait = QtGui.QComboBox(Dialog)
        self.comboBoxForfait.setObjectName(_fromUtf8("comboBoxForfait"))
        self.comboBoxForfait.addItem(_fromUtf8(""))
        self.comboBoxForfait.addItem(_fromUtf8(""))
        self.comboBoxForfait.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBoxForfait, 1, 1, 1, 1)
        self.lineEdit_8 = QtGui.QLineEdit(Dialog)
        self.lineEdit_8.setText(_fromUtf8(""))
        self.lineEdit_8.setObjectName(_fromUtf8("lineEdit_8"))
        self.gridLayout.addWidget(self.lineEdit_8, 4, 1, 1, 1)
        self.label_12 = QtGui.QLabel(Dialog)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout.addWidget(self.label_12, 4, 0, 1, 1)
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)
        self.lineEdit_13 = QtGui.QLineEdit(Dialog)
        self.lineEdit_13.setText(_fromUtf8(""))
        self.lineEdit_13.setObjectName(_fromUtf8("lineEdit_13"))
        self.gridLayout.addWidget(self.lineEdit_13, 2, 1, 1, 1)
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.textEdit = QtGui.QTextEdit(Dialog)
        self.textEdit.setEnabled(False)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.verticalLayout.addWidget(self.textEdit)
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)
        self.pushButton_2 = QtGui.QPushButton(Dialog)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.verticalLayout.addWidget(self.pushButton_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Re-calcule des impôts pour chaque contribuable", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Forfaitaire", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxForfait.setItemText(0, QtGui.QApplication.translate("Dialog", "Par surface", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxForfait.setItemText(1, QtGui.QApplication.translate("Dialog", "Par consistance", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxForfait.setItemText(2, QtGui.QApplication.translate("Dialog", "Par classe", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("Dialog", "Nombres des parcelles :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Dialog", "Nombres des contribuables :", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Charger", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("Dialog", "Calculer", None, QtGui.QApplication.UnicodeUTF8))

