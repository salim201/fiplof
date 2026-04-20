# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\plofstandalone\trunk\Parametres\EditConsistance.ui'
#
# Created: Thu May 26 09:39:56 2022
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
        Dialog.resize(335, 216)
        Dialog.setMaximumSize(QtCore.QSize(335, 216))
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.lineEditLibelle = QtGui.QLineEdit(Dialog)
        self.lineEditLibelle.setMaxLength(50)
        self.lineEditLibelle.setObjectName(_fromUtf8("lineEditLibelle"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEditLibelle)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.lineEditParcelleOuBatiment = QtGui.QLineEdit(Dialog)
        self.lineEditParcelleOuBatiment.setMaxLength(50)
        self.lineEditParcelleOuBatiment.setObjectName(_fromUtf8("lineEditParcelleOuBatiment"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEditParcelleOuBatiment)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.line = QtGui.QFrame(Dialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButtonEnregistrer = QtGui.QPushButton(Dialog)
        self.pushButtonEnregistrer.setObjectName(_fromUtf8("pushButtonEnregistrer"))
        self.horizontalLayout.addWidget(self.pushButtonEnregistrer)
        self.pushButtonAnnuler = QtGui.QPushButton(Dialog)
        self.pushButtonAnnuler.setObjectName(_fromUtf8("pushButtonAnnuler"))
        self.horizontalLayout.addWidget(self.pushButtonAnnuler)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Edition Categorie", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Categorie", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Momba ny Tany", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonEnregistrer.setText(QtGui.QApplication.translate("Dialog", "Enregistrer", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAnnuler.setText(QtGui.QApplication.translate("Dialog", "Annuler", None, QtGui.QApplication.UnicodeUTF8))

