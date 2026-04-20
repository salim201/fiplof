# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RecalculImpot.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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
        Dialog.resize(400, 300)
        self.lineEdit_13 = QtGui.QLineEdit(Dialog)
        self.lineEdit_13.setGeometry(QtCore.QRect(170, 20, 120, 20))
        self.lineEdit_13.setText(_fromUtf8(""))
        self.lineEdit_13.setObjectName(_fromUtf8("lineEdit_13"))
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(20, 20, 140, 13))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.lineEdit_8 = QtGui.QLineEdit(Dialog)
        self.lineEdit_8.setGeometry(QtCore.QRect(170, 50, 120, 20))
        self.lineEdit_8.setText(_fromUtf8(""))
        self.lineEdit_8.setObjectName(_fromUtf8("lineEdit_8"))
        self.label_12 = QtGui.QLabel(Dialog)
        self.label_12.setGeometry(QtCore.QRect(20, 50, 140, 13))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(310, 20, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.textEdit = QtGui.QTextEdit(Dialog)
        self.textEdit.setEnabled(False)
        self.textEdit.setGeometry(QtCore.QRect(20, 80, 361, 171))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.pushButton_2 = QtGui.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(310, 260, 75, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(20, 260, 291, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Re-calcule des impôts pour chaque contribuable", None))
        self.label_6.setText(_translate("Dialog", "Nombres des contribuables :", None))
        self.label_12.setText(_translate("Dialog", "Nombres des parcelles :", None))
        self.pushButton.setText(_translate("Dialog", "Charger", None))
        self.pushButton_2.setText(_translate("Dialog", "Calculer", None))

