# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CurrentLayer.ui'
#
# Created: Sun Sep 02 16:57:27 2018
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
        Dialog.resize(335, 89)
        Dialog.setModal(False)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formGroupBox = QtGui.QGroupBox(Dialog)
        self.formGroupBox.setObjectName(_fromUtf8("formGroupBox"))
        self.formLayout = QtGui.QFormLayout(self.formGroupBox)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.choisirCoucheComboBox = QtGui.QComboBox(self.formGroupBox)
        self.choisirCoucheComboBox.setObjectName(_fromUtf8("choisirCoucheComboBox"))
        self.choisirCoucheComboBox.addItem(_fromUtf8(""))
        self.choisirCoucheComboBox.addItem(_fromUtf8(""))
        self.choisirCoucheComboBox.addItem(_fromUtf8(""))
        self.choisirCoucheComboBox.addItem(_fromUtf8(""))
        self.choisirCoucheComboBox.addItem(_fromUtf8(""))
        self.choisirCoucheComboBox.addItem(_fromUtf8(""))
        self.choisirCoucheComboBox.addItem(_fromUtf8(""))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.choisirCoucheComboBox)
        self.verticalLayout.addWidget(self.formGroupBox)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonOK = QtGui.QPushButton(Dialog)
        self.pushButtonOK.setDefault(True)
        self.pushButtonOK.setObjectName(_fromUtf8("pushButtonOK"))
        self.horizontalLayout.addWidget(self.pushButtonOK)
        self.pushButtonCancel = QtGui.QPushButton(Dialog)
        self.pushButtonCancel.setObjectName(_fromUtf8("pushButtonCancel"))
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Choix couche", None))
        self.choisirCoucheComboBox.setItemText(0, _translate("Dialog", "Choisir couche ici ...", None))
        self.choisirCoucheComboBox.setItemText(1, _translate("Dialog", "Parcelle demande", None))
        self.choisirCoucheComboBox.setItemText(2, _translate("Dialog", "Parcelle fiscalite", None))
        self.choisirCoucheComboBox.setItemText(3, _translate("Dialog", "Certificat", None))
        self.choisirCoucheComboBox.setItemText(4, _translate("Dialog", "Proposition de titre", None))
        self.choisirCoucheComboBox.setItemText(5, _translate("Dialog", "Proposition aire specifique", None))
        self.choisirCoucheComboBox.setItemText(6, _translate("Dialog", "Proposition domaine public", None))
        self.pushButtonOK.setText(_translate("Dialog", "OK", None))
        self.pushButtonCancel.setText(_translate("Dialog", "Annuler", None))

