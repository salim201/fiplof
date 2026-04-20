# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'montant.ui'
#
# Created: Sat Dec 16 10:40:53 2023
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
        Dialog.resize(338, 183)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.labelTypePaiement = QtGui.QLabel(Dialog)
        self.labelTypePaiement.setObjectName(_fromUtf8("labelTypePaiement"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelTypePaiement)
        self.comboBoxTypePaiement = QtGui.QComboBox(Dialog)
        self.comboBoxTypePaiement.setObjectName(_fromUtf8("comboBoxTypePaiement"))
        self.comboBoxTypePaiement.addItem(_fromUtf8(""))
        self.comboBoxTypePaiement.addItem(_fromUtf8(""))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBoxTypePaiement)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_2)
        self.lineEditNumEquitance = QtGui.QLineEdit(Dialog)
        self.lineEditNumEquitance.setObjectName(_fromUtf8("lineEditNumEquitance"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.lineEditNumEquitance)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.buttonBox)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.pushButtonEnregistrer = QtGui.QPushButton(Dialog)
        self.pushButtonEnregistrer.setObjectName(_fromUtf8("pushButtonEnregistrer"))
        self.horizontalLayout_3.addWidget(self.pushButtonEnregistrer)
        self.pushButtonFermer = QtGui.QPushButton(Dialog)
        self.pushButtonFermer.setObjectName(_fromUtf8("pushButtonFermer"))
        self.horizontalLayout_3.addWidget(self.pushButtonFermer)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.labelTypePaiement.setText(_translate("Dialog", "Paiement:", None))
        self.comboBoxTypePaiement.setItemText(0, _translate("Dialog", "En Totalité", None))
        self.comboBoxTypePaiement.setItemText(1, _translate("Dialog", "En Partie", None))
        self.label.setText(_translate("Dialog", "Montant", None))
        self.label_2.setText(_translate("Dialog", "Numéro d\'équitance", None))
        self.pushButtonEnregistrer.setText(_translate("Dialog", "Enregistrer Paiement", None))
        self.pushButtonFermer.setText(_translate("Dialog", "Fermer", None))

