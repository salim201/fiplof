# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Authentification.ui'
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
        Dialog.resize(597, 260)
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(400, 10, 190, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.lineEdit_2 = QtGui.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(400, 40, 190, 20))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(400, 70, 190, 22))
        self.comboBox.setEditable(True)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.listView = QtGui.QListView(Dialog)
        self.listView.setGeometry(QtCore.QRect(220, 100, 371, 121))
        self.listView.setObjectName(_fromUtf8("listView"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(220, 10, 150, 13))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(220, 40, 150, 13))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(220, 70, 150, 13))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(410, 230, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(510, 230, 75, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Authentification", None))
        self.label.setText(_translate("Dialog", "Identifiant d\'utilisateur :", None))
        self.label_2.setText(_translate("Dialog", "Mot de passe :", None))
        self.label_3.setText(_translate("Dialog", "Projet :", None))
        self.pushButton.setText(_translate("Dialog", "Ok", None))
        self.pushButton_2.setText(_translate("Dialog", "Annuler", None))

