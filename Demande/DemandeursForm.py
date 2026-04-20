# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DemandeursForm.ui'
#
# Created: Sun Jun 10 13:49:56 2018
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Demandeur(object):
    def setupUi(self, Demandeur):
        Demandeur.setObjectName(_fromUtf8("Demandeur"))
        Demandeur.resize(476, 216)
        Demandeur.setSizeGripEnabled(False)
        Demandeur.setModal(True)
        self.formGroupBox = QtGui.QGroupBox(Demandeur)
        self.formGroupBox.setGeometry(QtCore.QRect(10, 10, 291, 71))
        self.formGroupBox.setObjectName(_fromUtf8("formGroupBox"))
        self.formLayout = QtGui.QFormLayout(self.formGroupBox)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(14, 10, 5, 6)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.nomLabel = QtGui.QLabel(self.formGroupBox)
        self.nomLabel.setObjectName(_fromUtf8("nomLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.nomLabel)
        self.nomLineEdit = QtGui.QLineEdit(self.formGroupBox)
        self.nomLineEdit.setObjectName(_fromUtf8("nomLineEdit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.nomLineEdit)
        self.prenomLabel = QtGui.QLabel(self.formGroupBox)
        self.prenomLabel.setObjectName(_fromUtf8("prenomLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.prenomLabel)
        self.prenomLineEdit = QtGui.QLineEdit(self.formGroupBox)
        self.prenomLineEdit.setObjectName(_fromUtf8("prenomLineEdit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.prenomLineEdit)
        self.verticalGroupBox = QtGui.QGroupBox(Demandeur)
        self.verticalGroupBox.setGeometry(QtCore.QRect(10, 89, 291, 51))
        self.verticalGroupBox.setObjectName(_fromUtf8("verticalGroupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalGroupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.uploadPhotos = QtGui.QPushButton(self.verticalGroupBox)
        self.uploadPhotos.setObjectName(_fromUtf8("uploadPhotos"))
        self.verticalLayout.addWidget(self.uploadPhotos)
        self.gridLayoutWidget = QtGui.QWidget(Demandeur)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(310, 10, 160, 131))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        self.label.setText(_fromUtf8(""))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.horizontalGroupBox = QtGui.QGroupBox(Demandeur)
        self.horizontalGroupBox.setGeometry(QtCore.QRect(10, 170, 291, 41))
        self.horizontalGroupBox.setObjectName(_fromUtf8("horizontalGroupBox"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalGroupBox)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.btnadd = QtGui.QPushButton(self.horizontalGroupBox)
        self.btnadd.setObjectName(_fromUtf8("btnadd"))
        self.horizontalLayout_2.addWidget(self.btnadd)
        self.btncancel = QtGui.QPushButton(self.horizontalGroupBox)
        self.btncancel.setObjectName(_fromUtf8("btncancel"))
        self.horizontalLayout_2.addWidget(self.btncancel)

        self.retranslateUi(Demandeur)
        QtCore.QMetaObject.connectSlotsByName(Demandeur)

    def retranslateUi(self, Demandeur):
        Demandeur.setWindowTitle(QtGui.QApplication.translate("Demandeur", "Saisie demandeur", None, QtGui.QApplication.UnicodeUTF8))
        self.nomLabel.setText(QtGui.QApplication.translate("Demandeur", "Nom *", None, QtGui.QApplication.UnicodeUTF8))
        self.prenomLabel.setText(QtGui.QApplication.translate("Demandeur", "Prenom *", None, QtGui.QApplication.UnicodeUTF8))
        self.uploadPhotos.setText(QtGui.QApplication.translate("Demandeur", "... Photos", None, QtGui.QApplication.UnicodeUTF8))
        self.btnadd.setText(QtGui.QApplication.translate("Demandeur", "Ajouter", None, QtGui.QApplication.UnicodeUTF8))
        self.btncancel.setText(QtGui.QApplication.translate("Demandeur", "Annuler", None, QtGui.QApplication.UnicodeUTF8))

