# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\plofstandalone\Demande\ReglementForm.ui'
#
# Created: Fri Mar 08 09:51:36 2019
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Reglement(object):
    def setupUi(self, Reglement):
        Reglement.setObjectName(_fromUtf8("Reglement"))
        Reglement.setWindowModality(QtCore.Qt.WindowModal)
        Reglement.resize(497, 136)
        Reglement.setSizeGripEnabled(True)
        Reglement.setModal(True)
        self.formGroupBox = QtGui.QGroupBox(Reglement)
        self.formGroupBox.setGeometry(QtCore.QRect(10, 10, 311, 121))
        self.formGroupBox.setObjectName(_fromUtf8("formGroupBox"))
        self.formLayout = QtGui.QFormLayout(self.formGroupBox)
        self.formLayout.setMargin(6)
        self.formLayout.setSpacing(10)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.dateReglementLabel = QtGui.QLabel(self.formGroupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.dateReglementLabel.setFont(font)
        self.dateReglementLabel.setObjectName(_fromUtf8("dateReglementLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.dateReglementLabel)
        self.dateReglementDateEdit = QtGui.QDateEdit(self.formGroupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.dateReglementDateEdit.setFont(font)
        self.dateReglementDateEdit.setObjectName(_fromUtf8("dateReglementDateEdit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.dateReglementDateEdit)
        self.natureLabel = QtGui.QLabel(self.formGroupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.natureLabel.setFont(font)
        self.natureLabel.setObjectName(_fromUtf8("natureLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.natureLabel)
        self.natureComboBox = QtGui.QComboBox(self.formGroupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.natureComboBox.setFont(font)
        self.natureComboBox.setObjectName(_fromUtf8("natureComboBox"))
        self.natureComboBox.addItem(_fromUtf8(""))
        self.natureComboBox.addItem(_fromUtf8(""))
        self.natureComboBox.addItem(_fromUtf8(""))
        self.natureComboBox.addItem(_fromUtf8(""))
        self.natureComboBox.addItem(_fromUtf8(""))
        self.natureComboBox.addItem(_fromUtf8(""))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.natureComboBox)
        self.descriptionLabel = QtGui.QLabel(self.formGroupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.descriptionLabel.setFont(font)
        self.descriptionLabel.setObjectName(_fromUtf8("descriptionLabel"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.descriptionLabel)
        self.textEdit = QtGui.QTextEdit(self.formGroupBox)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.textEdit)
        self.verticalGroupBox = QtGui.QGroupBox(Reglement)
        self.verticalGroupBox.setGeometry(QtCore.QRect(330, 10, 160, 62))
        self.verticalGroupBox.setObjectName(_fromUtf8("verticalGroupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalGroupBox)
        self.verticalLayout.setSpacing(8)
        self.verticalLayout.setMargin(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.save = QtGui.QPushButton(self.verticalGroupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.save.setFont(font)
        self.save.setObjectName(_fromUtf8("save"))
        self.verticalLayout.addWidget(self.save)
        self.cancel = QtGui.QPushButton(self.verticalGroupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.cancel.setFont(font)
        self.cancel.setObjectName(_fromUtf8("cancel"))
        self.verticalLayout.addWidget(self.cancel)
        self.formGroupBox_2 = QtGui.QGroupBox(Reglement)
        self.formGroupBox_2.setGeometry(QtCore.QRect(330, 80, 160, 51))
        self.formGroupBox_2.setObjectName(_fromUtf8("formGroupBox_2"))
        self.formLayout_2 = QtGui.QFormLayout(self.formGroupBox_2)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))

        self.retranslateUi(Reglement)
        QtCore.QMetaObject.connectSlotsByName(Reglement)

    def retranslateUi(self, Reglement):
        Reglement.setWindowTitle(QtGui.QApplication.translate("Reglement", "Reglement opposition", None, QtGui.QApplication.UnicodeUTF8))
        self.dateReglementLabel.setText(QtGui.QApplication.translate("Reglement", "Date reglement", None, QtGui.QApplication.UnicodeUTF8))
        self.natureLabel.setText(QtGui.QApplication.translate("Reglement", "Nature ", None, QtGui.QApplication.UnicodeUTF8))
        self.natureComboBox.setItemText(0, QtGui.QApplication.translate("Reglement", "ACQUIESCMENT SPONTANE", None, QtGui.QApplication.UnicodeUTF8))
        self.natureComboBox.setItemText(1, QtGui.QApplication.translate("Reglement", "MAIN LEVEE SPONTANNEE", None, QtGui.QApplication.UnicodeUTF8))
        self.natureComboBox.setItemText(2, QtGui.QApplication.translate("Reglement", "ACQUIESCEMENT APRES CONCILIATION", None, QtGui.QApplication.UnicodeUTF8))
        self.natureComboBox.setItemText(3, QtGui.QApplication.translate("Reglement", "MAIN LEVEE  APRES CONCILIATION", None, QtGui.QApplication.UnicodeUTF8))
        self.natureComboBox.setItemText(4, QtGui.QApplication.translate("Reglement", "SENTENCE ARBITRALE", None, QtGui.QApplication.UnicodeUTF8))
        self.natureComboBox.setItemText(5, QtGui.QApplication.translate("Reglement", "DECISION DU TRIBUNAL", None, QtGui.QApplication.UnicodeUTF8))
        self.descriptionLabel.setText(QtGui.QApplication.translate("Reglement", "Description", None, QtGui.QApplication.UnicodeUTF8))
        self.save.setText(QtGui.QApplication.translate("Reglement", "Enregistrer", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel.setText(QtGui.QApplication.translate("Reglement", "Annuler", None, QtGui.QApplication.UnicodeUTF8))

