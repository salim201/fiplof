# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'EtatAttestation.ui'
#
# Created: Sat Apr 14 17:13:15 2018
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
        Dialog.resize(317, 514)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.lineEditCommune = QtGui.QLineEdit(Dialog)
        self.lineEditCommune.setEnabled(False)
        self.lineEditCommune.setObjectName(_fromUtf8("lineEditCommune"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEditCommune)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.lineEditNumCertificat = QtGui.QLineEdit(Dialog)
        self.lineEditNumCertificat.setObjectName(_fromUtf8("lineEditNumCertificat"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEditNumCertificat)
        self.pushButtonRechercher = QtGui.QPushButton(Dialog)
        self.pushButtonRechercher.setObjectName(_fromUtf8("pushButtonRechercher"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.pushButtonRechercher)
        self.verticalLayout.addLayout(self.formLayout)
        self.tableWidget = QtGui.QTableWidget(Dialog)
        self.tableWidget.setMinimumSize(QtCore.QSize(0, 381))
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonImprimer = QtGui.QPushButton(Dialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/std/icone/printer.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonImprimer.setIcon(icon)
        self.pushButtonImprimer.setObjectName(_fromUtf8("pushButtonImprimer"))
        self.horizontalLayout.addWidget(self.pushButtonImprimer)
        self.pushButtonAnnuler = QtGui.QPushButton(Dialog)
        self.pushButtonAnnuler.setObjectName(_fromUtf8("pushButtonAnnuler"))
        self.horizontalLayout.addWidget(self.pushButtonAnnuler)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Impression Attestation", None))
        self.label.setText(_translate("Dialog", "Commune", None))
        self.label_2.setText(_translate("Dialog", "Num. Certificat", None))
        self.pushButtonRechercher.setText(_translate("Dialog", "Rechercher", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Numero", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Date Création", None))
        self.pushButtonImprimer.setText(_translate("Dialog", "Imprimer", None))
        self.pushButtonAnnuler.setText(_translate("Dialog", "Annuler", None))

import icons_rc
