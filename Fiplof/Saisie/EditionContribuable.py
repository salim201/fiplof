# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'EditionContribuable.ui'
#
# Created: Sat Dec 15 01:01:43 2018
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
        Dialog.resize(632, 327)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/users/icone/group.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButtonAjouter = QtGui.QPushButton(Dialog)
        self.pushButtonAjouter.setObjectName(_fromUtf8("pushButtonAjouter"))
        self.horizontalLayout_2.addWidget(self.pushButtonAjouter)
        self.pushButtonEnleverProprioPpque = QtGui.QPushButton(Dialog)
        self.pushButtonEnleverProprioPpque.setObjectName(_fromUtf8("pushButtonEnleverProprioPpque"))
        self.horizontalLayout_2.addWidget(self.pushButtonEnleverProprioPpque)
        self.pushButtonDetailsPhysique = QtGui.QPushButton(Dialog)
        self.pushButtonDetailsPhysique.setObjectName(_fromUtf8("pushButtonDetailsPhysique"))
        self.horizontalLayout_2.addWidget(self.pushButtonDetailsPhysique)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.tableWidgetPhysique = QtGui.QTableWidget(self.groupBox)
        self.tableWidgetPhysique.setObjectName(_fromUtf8("tableWidgetPhysique"))
        self.tableWidgetPhysique.setColumnCount(4)
        self.tableWidgetPhysique.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetPhysique.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetPhysique.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetPhysique.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetPhysique.setHorizontalHeaderItem(3, item)
        self.verticalLayout_3.addWidget(self.tableWidgetPhysique)
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton_4 = QtGui.QPushButton(Dialog)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.pushButtonAnnuler = QtGui.QPushButton(Dialog)
        self.pushButtonAnnuler.setObjectName(_fromUtf8("pushButtonAnnuler"))
        self.horizontalLayout.addWidget(self.pushButtonAnnuler)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Propriétaires", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAjouter.setText(QtGui.QApplication.translate("Dialog", "Ajouter", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonEnleverProprioPpque.setText(QtGui.QApplication.translate("Dialog", "Enlever", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDetailsPhysique.setText(QtGui.QApplication.translate("Dialog", "Details", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Personne Physique", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidgetPhysique.horizontalHeaderItem(0)
        item.setText(QtGui.QApplication.translate("Dialog", "Nom", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidgetPhysique.horizontalHeaderItem(1)
        item.setText(QtGui.QApplication.translate("Dialog", "Prenoms", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidgetPhysique.horizontalHeaderItem(2)
        item.setText(QtGui.QApplication.translate("Dialog", "CIN", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidgetPhysique.horizontalHeaderItem(3)
        item.setText(QtGui.QApplication.translate("Dialog", "Adresse", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_4.setText(QtGui.QApplication.translate("Dialog", "Valider", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAnnuler.setText(QtGui.QApplication.translate("Dialog", "Annuler", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc
