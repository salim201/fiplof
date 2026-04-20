# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'listeTypePersonneMorale.ui'
#
# Created: Tue Jun 12 09:28:13 2018
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
        Dialog.resize(492, 351)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/users/icone/user_02.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.tableWidget = QtGui.QTableWidget(Dialog)
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(150)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.horizontalLayout_2.addWidget(self.tableWidget)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.pushButtonNouveau = QtGui.QPushButton(Dialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/std/icone/if_plus_circle_12296.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonNouveau.setIcon(icon1)
        self.pushButtonNouveau.setObjectName(_fromUtf8("pushButtonNouveau"))
        self.verticalLayout.addWidget(self.pushButtonNouveau)
        self.pushButtonModifier = QtGui.QPushButton(Dialog)
        self.pushButtonModifier.setEnabled(False)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/std/icone/if_pencil_14623.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonModifier.setIcon(icon2)
        self.pushButtonModifier.setObjectName(_fromUtf8("pushButtonModifier"))
        self.verticalLayout.addWidget(self.pushButtonModifier)
        self.pushButtonSupprimer = QtGui.QPushButton(Dialog)
        self.pushButtonSupprimer.setEnabled(False)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/std/icone/if_minus_10199.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonSupprimer.setIcon(icon3)
        self.pushButtonSupprimer.setObjectName(_fromUtf8("pushButtonSupprimer"))
        self.verticalLayout.addWidget(self.pushButtonSupprimer)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.BTFermer = QtGui.QPushButton(Dialog)
        self.BTFermer.setObjectName(_fromUtf8("BTFermer"))
        self.verticalLayout.addWidget(self.BTFermer)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Liste des types de personne morale", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Type", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Karazany", None))
        self.pushButtonNouveau.setText(_translate("Dialog", "Nouveau", None))
        self.pushButtonModifier.setText(_translate("Dialog", "Modifier", None))
        self.pushButtonSupprimer.setText(_translate("Dialog", "Supprimer", None))
        self.BTFermer.setText(_translate("Dialog", "Fermer", None))

import icons_rc
