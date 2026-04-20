# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'compteur.ui'
#
# Created: Thu Feb 23 15:31:31 2023
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
        Dialog.resize(285, 108)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.pushButtonModifier = QtGui.QPushButton(Dialog)
        self.pushButtonModifier.setObjectName(_fromUtf8("pushButtonModifier"))
        self.gridLayout.addWidget(self.pushButtonModifier, 4, 0, 1, 1)
        self.pushButtonQuitter = QtGui.QPushButton(Dialog)
        self.pushButtonQuitter.setObjectName(_fromUtf8("pushButtonQuitter"))
        self.gridLayout.addWidget(self.pushButtonQuitter, 4, 1, 1, 1)
        self.lineEditCptDemande = QtGui.QLineEdit(Dialog)
        self.lineEditCptDemande.setObjectName(_fromUtf8("lineEditCptDemande"))
        self.gridLayout.addWidget(self.lineEditCptDemande, 0, 1, 1, 1)
        self.lineEditCptCF = QtGui.QLineEdit(Dialog)
        self.lineEditCptCF.setObjectName(_fromUtf8("lineEditCptCF"))
        self.gridLayout.addWidget(self.lineEditCptCF, 2, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "Compteur Demande:", None))
        self.label_2.setText(_translate("Dialog", "Compteur Certificat:", None))
        self.pushButtonModifier.setText(_translate("Dialog", "Modifier", None))
        self.pushButtonQuitter.setText(_translate("Dialog", "Quitter", None))

