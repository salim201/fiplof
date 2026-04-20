# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NumeroCF.ui'
#
# Created: Mon Jul 30 13:32:15 2018
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
        Dialog.resize(400, 97)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.numRoDeLaDemandeLabel = QtGui.QLabel(Dialog)
        self.numRoDeLaDemandeLabel.setObjectName(_fromUtf8("numRoDeLaDemandeLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.numRoDeLaDemandeLabel)
        self.lineEditNumDmede = QtGui.QLineEdit(Dialog)
        self.lineEditNumDmede.setObjectName(_fromUtf8("lineEditNumDmede"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEditNumDmede)
        self.dateDeLaDemandeLabel = QtGui.QLabel(Dialog)
        self.dateDeLaDemandeLabel.setObjectName(_fromUtf8("dateDeLaDemandeLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.dateDeLaDemandeLabel)
        self.lineEditNumCF = QtGui.QLineEdit(Dialog)
        self.lineEditNumCF.setObjectName(_fromUtf8("lineEditNumCF"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEditNumCF)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnOk = QtGui.QPushButton(Dialog)
        self.btnOk.setObjectName(_fromUtf8("btnOk"))
        self.horizontalLayout.addWidget(self.btnOk)
        self.btnAnnuler = QtGui.QPushButton(Dialog)
        self.btnAnnuler.setObjectName(_fromUtf8("btnAnnuler"))
        self.horizontalLayout.addWidget(self.btnAnnuler)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Numéro", None, QtGui.QApplication.UnicodeUTF8))
        self.numRoDeLaDemandeLabel.setText(QtGui.QApplication.translate("Dialog", "Numéro de la demande", None, QtGui.QApplication.UnicodeUTF8))
        self.dateDeLaDemandeLabel.setText(QtGui.QApplication.translate("Dialog", "Numéro Certificat", None, QtGui.QApplication.UnicodeUTF8))
        self.btnOk.setText(QtGui.QApplication.translate("Dialog", "Ok", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAnnuler.setText(QtGui.QApplication.translate("Dialog", "Annuler", None, QtGui.QApplication.UnicodeUTF8))

