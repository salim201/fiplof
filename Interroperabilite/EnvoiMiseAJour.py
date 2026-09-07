# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'EnvoiMiseAJour.ui'
#
# Created: Wed Jun 10 23:35:32 2026
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

class Ui_EnvoiMiseAJour(object):
    def setupUi(self, EnvoiMiseAJour):
        EnvoiMiseAJour.setObjectName(_fromUtf8("EnvoiMiseAJour"))
        EnvoiMiseAJour.resize(900, 500)
        self.verticalLayout = QtGui.QVBoxLayout(EnvoiMiseAJour)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_filtre = QtGui.QHBoxLayout()
        self.horizontalLayout_filtre.setObjectName(_fromUtf8("horizontalLayout_filtre"))
        self.labelFiltre = QtGui.QLabel(EnvoiMiseAJour)
        self.labelFiltre.setObjectName(_fromUtf8("labelFiltre"))
        self.horizontalLayout_filtre.addWidget(self.labelFiltre)
        self.comboBoxFiltreStatut = QtGui.QComboBox(EnvoiMiseAJour)
        self.comboBoxFiltreStatut.setMinimumContentsLength(15)
        self.comboBoxFiltreStatut.setObjectName(_fromUtf8("comboBoxFiltreStatut"))
        self.comboBoxFiltreStatut.addItem(_fromUtf8(""))
        self.comboBoxFiltreStatut.addItem(_fromUtf8(""))
        self.comboBoxFiltreStatut.addItem(_fromUtf8(""))
        self.horizontalLayout_filtre.addWidget(self.comboBoxFiltreStatut)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_filtre.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_filtre)
        self.groupBox = QtGui.QGroupBox(EnvoiMiseAJour)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tableWidget_retour = QtGui.QTableWidget(self.groupBox)
        self.tableWidget_retour.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget_retour.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableWidget_retour.setObjectName(_fromUtf8("tableWidget_retour"))
        self.tableWidget_retour.setColumnCount(6)
        self.tableWidget_retour.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_retour.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_retour.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_retour.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_retour.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_retour.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_retour.setHorizontalHeaderItem(5, item)
        self.verticalLayout_2.addWidget(self.tableWidget_retour)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.checkBoxCocherTous = QtGui.QCheckBox(self.groupBox)
        self.checkBoxCocherTous.setObjectName(_fromUtf8("checkBoxCocherTous"))
        self.horizontalLayout.addWidget(self.checkBoxCocherTous)
        self.labelStatutEnvoi = QtGui.QLabel(self.groupBox)
        self.labelStatutEnvoi.setText(_fromUtf8(""))
        self.labelStatutEnvoi.setObjectName(_fromUtf8("labelStatutEnvoi"))
        self.horizontalLayout.addWidget(self.labelStatutEnvoi)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButtonEnvoyer = QtGui.QPushButton(self.groupBox)
        self.pushButtonEnvoyer.setObjectName(_fromUtf8("pushButtonEnvoyer"))
        self.horizontalLayout.addWidget(self.pushButtonEnvoyer)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(EnvoiMiseAJour)
        QtCore.QMetaObject.connectSlotsByName(EnvoiMiseAJour)

    def retranslateUi(self, EnvoiMiseAJour):
        EnvoiMiseAJour.setWindowTitle(_translate("EnvoiMiseAJour", "Envoi Mise à Jour", None))
        self.labelFiltre.setText(_translate("EnvoiMiseAJour", "Filtrer par statut :", None))
        self.comboBoxFiltreStatut.setItemText(0, _translate("EnvoiMiseAJour", "Tous", None))
        self.comboBoxFiltreStatut.setItemText(1, _translate("EnvoiMiseAJour", "Non envoyé", None))
        self.comboBoxFiltreStatut.setItemText(2, _translate("EnvoiMiseAJour", "Envoyé", None))
        self.groupBox.setTitle(_translate("EnvoiMiseAJour", "Retours externes", None))
        item = self.tableWidget_retour.horizontalHeaderItem(1)
        item.setText(_translate("EnvoiMiseAJour", "Code Parcelle", None))
        item = self.tableWidget_retour.horizontalHeaderItem(2)
        item.setText(_translate("EnvoiMiseAJour", "Numero", None))
        item = self.tableWidget_retour.horizontalHeaderItem(3)
        item.setText(_translate("EnvoiMiseAJour", "Type", None))
        item = self.tableWidget_retour.horizontalHeaderItem(4)
        item.setText(_translate("EnvoiMiseAJour", "Statut", None))
        item = self.tableWidget_retour.horizontalHeaderItem(5)
        item.setText(_translate("EnvoiMiseAJour", "Date Statut", None))
        self.checkBoxCocherTous.setText(_translate("EnvoiMiseAJour", "Cocher tous", None))
        self.labelStatutEnvoi.setStyleSheet(_translate("EnvoiMiseAJour", "font-weight: bold; font-size: 12px;", None))
        self.pushButtonEnvoyer.setText(_translate("EnvoiMiseAJour", "ENVOYER", None))
        self.pushButtonEnvoyer.setStyleSheet(_translate("EnvoiMiseAJour", "font-weight: bold; font-size: 14px; padding: 8px 20px;", None))

