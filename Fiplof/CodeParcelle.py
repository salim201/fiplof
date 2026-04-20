# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CodeParcelle.ui'
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
        Dialog.resize(339, 170)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 321, 110))
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.lineEdit_3 = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_3.setGeometry(QtCore.QRect(100, 80, 210, 20))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.comboBox = QtGui.QComboBox(self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(100, 20, 210, 22))
        self.comboBox.setEditable(True)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox_2 = QtGui.QComboBox(self.groupBox)
        self.comboBox_2.setGeometry(QtCore.QRect(100, 50, 210, 22))
        self.comboBox_2.setEditable(True)
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 20, 70, 13))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 46, 13))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 80, 46, 13))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.groupBox_3 = QtGui.QGroupBox(Dialog)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 120, 320, 41))
        self.groupBox_3.setTitle(_fromUtf8(""))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.pushButton = QtGui.QPushButton(self.groupBox_3)
        self.pushButton.setGeometry(QtCore.QRect(140, 10, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 10, 75, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Code parcelle", None))
        self.label.setText(_translate("Dialog", "Fokontany : ", None))
        self.label_2.setText(_translate("Dialog", "Hameau :", None))
        self.label_3.setText(_translate("Dialog", "Code : ", None))
        self.pushButton.setText(_translate("Dialog", "OK", None))
        self.pushButton_2.setText(_translate("Dialog", "Annuler", None))

