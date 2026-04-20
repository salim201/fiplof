# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'J:\Demande\Voisins.ui'
#
# Created: Sat May 14 08:06:38 2022
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
        Dialog.resize(395, 120)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setContentsMargins(4, 6, 4, 6)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.nomEtPrNomsLabel = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.nomEtPrNomsLabel.setFont(font)
        self.nomEtPrNomsLabel.setObjectName(_fromUtf8("nomEtPrNomsLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.nomEtPrNomsLabel)
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBox)
        self.nomsEtPrNomsLabel = QtGui.QLabel(Dialog)
        self.nomsEtPrNomsLabel.setObjectName(_fromUtf8("nomsEtPrNomsLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.nomsEtPrNomsLabel)
        self.nomEtPrNomsLineEdit = QtGui.QLineEdit(Dialog)
        self.nomEtPrNomsLineEdit.setObjectName(_fromUtf8("nomEtPrNomsLineEdit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.nomEtPrNomsLineEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Enregistrement des voisins", None, QtGui.QApplication.UnicodeUTF8))
        self.nomEtPrNomsLabel.setText(QtGui.QApplication.translate("Dialog", "Repère : ", None, QtGui.QApplication.UnicodeUTF8))
        self.nomsEtPrNomsLabel.setText(QtGui.QApplication.translate("Dialog", "Description", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Enregistrer", None, QtGui.QApplication.UnicodeUTF8))

