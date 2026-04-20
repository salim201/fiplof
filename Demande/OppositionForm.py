# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'OppositionForm.ui'
#
# Created: Sat Jun 09 11:09:30 2018
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Opposition(object):
    def setupUi(self, Opposition):
        Opposition.setObjectName(_fromUtf8("Opposition"))
        Opposition.resize(435, 189)
        self.formLayoutWidget = QtGui.QWidget(Opposition)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 311, 169))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setMargin(6)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.typeOppositionLabel = QtGui.QLabel(self.formLayoutWidget)
        self.typeOppositionLabel.setObjectName(_fromUtf8("typeOppositionLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.typeOppositionLabel)
        self.typeOppositionComboBox = QtGui.QComboBox(self.formLayoutWidget)
        self.typeOppositionComboBox.setObjectName(_fromUtf8("typeOppositionComboBox"))
        self.typeOppositionComboBox.addItem(_fromUtf8(""))
        self.typeOppositionComboBox.addItem(_fromUtf8(""))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.typeOppositionComboBox)
        self.dateOppositionLabel = QtGui.QLabel(self.formLayoutWidget)
        self.dateOppositionLabel.setObjectName(_fromUtf8("dateOppositionLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.dateOppositionLabel)
        self.dateOppositionDateEdit = QtGui.QDateEdit(self.formLayoutWidget)
        self.dateOppositionDateEdit.setObjectName(_fromUtf8("dateOppositionDateEdit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.dateOppositionDateEdit)
        self.dateDemandeLabel = QtGui.QLabel(self.formLayoutWidget)
        self.dateDemandeLabel.setObjectName(_fromUtf8("dateDemandeLabel"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.dateDemandeLabel)
        self.dateDemandeDateEdit = QtGui.QDateEdit(self.formLayoutWidget)
        self.dateDemandeDateEdit.setObjectName(_fromUtf8("dateDemandeDateEdit"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.dateDemandeDateEdit)
        self.descriptionLabel = QtGui.QLabel(self.formLayoutWidget)
        self.descriptionLabel.setObjectName(_fromUtf8("descriptionLabel"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.descriptionLabel)
        self.textEdit = QtGui.QTextEdit(self.formLayoutWidget)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.textEdit)
        self.verticalLayoutWidget = QtGui.QWidget(Opposition)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(330, 9, 101, 81))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.BtnAddOpp = QtGui.QPushButton(self.verticalLayoutWidget)
        self.BtnAddOpp.setObjectName(_fromUtf8("BtnAddOpp"))
        self.verticalLayout.addWidget(self.BtnAddOpp)
        self.BtnCncl = QtGui.QPushButton(self.verticalLayoutWidget)
        self.BtnCncl.setObjectName(_fromUtf8("BtnCncl"))
        self.verticalLayout.addWidget(self.BtnCncl)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.formLayoutWidget_2 = QtGui.QWidget(Opposition)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(330, 100, 101, 80))
        self.formLayoutWidget_2.setObjectName(_fromUtf8("formLayoutWidget_2"))
        self.formLayout_2 = QtGui.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setMargin(0)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))

        self.retranslateUi(Opposition)
        QtCore.QMetaObject.connectSlotsByName(Opposition)

    def retranslateUi(self, Opposition):
        Opposition.setWindowTitle(QtGui.QApplication.translate("Opposition", "Saisie opposition", None, QtGui.QApplication.UnicodeUTF8))
        self.typeOppositionLabel.setText(QtGui.QApplication.translate("Opposition", "Type opposition", None, QtGui.QApplication.UnicodeUTF8))
        self.typeOppositionComboBox.setItemText(0, QtGui.QApplication.translate("Opposition", "SUR LES LIMITES", None, QtGui.QApplication.UnicodeUTF8))
        self.typeOppositionComboBox.setItemText(1, QtGui.QApplication.translate("Opposition", "SUR LES DROITS", None, QtGui.QApplication.UnicodeUTF8))
        self.dateOppositionLabel.setText(QtGui.QApplication.translate("Opposition", "Date opposition", None, QtGui.QApplication.UnicodeUTF8))
        self.dateDemandeLabel.setText(QtGui.QApplication.translate("Opposition", "Date demande", None, QtGui.QApplication.UnicodeUTF8))
        self.descriptionLabel.setText(QtGui.QApplication.translate("Opposition", "Description", None, QtGui.QApplication.UnicodeUTF8))
        self.BtnAddOpp.setText(QtGui.QApplication.translate("Opposition", "Ajouter", None, QtGui.QApplication.UnicodeUTF8))
        self.BtnCncl.setText(QtGui.QApplication.translate("Opposition", "Annuler", None, QtGui.QApplication.UnicodeUTF8))

