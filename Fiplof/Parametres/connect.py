# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connect.ui'
#
# Created: Sun Nov 26 13:01:07 2017
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
        Dialog.resize(350, 166)
        self.formLayoutWidget = QtGui.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(9, 9, 331, 101))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout_2 = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout_2.setMargin(0)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.loginLabel = QtGui.QLabel(self.formLayoutWidget)
        self.loginLabel.setObjectName(_fromUtf8("loginLabel"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.loginLabel)
        self.loginLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.loginLineEdit.setObjectName(_fromUtf8("loginLineEdit"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.loginLineEdit)
        self.motDePasseLabel = QtGui.QLabel(self.formLayoutWidget)
        self.motDePasseLabel.setObjectName(_fromUtf8("motDePasseLabel"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.motDePasseLabel)
        self.motDePasseLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.motDePasseLineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.motDePasseLineEdit.setObjectName(_fromUtf8("motDePasseLineEdit"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.motDePasseLineEdit)
        self.pushButton_2 = QtGui.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(140, 120, 95, 31))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(241, 120, 95, 31))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Connexion", None))
        self.loginLabel.setText(_translate("Dialog", "Login", None))
        self.motDePasseLabel.setText(_translate("Dialog", "Mot de passe", None))
        self.pushButton_2.setText(_translate("Dialog", "Connexion", None))
        self.pushButton.setText(_translate("Dialog", "Annuler", None))

