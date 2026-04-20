# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Projets.ui'
#
# Created: Sun Jan 28 12:25:56 2018
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
        Dialog.resize(889, 304)
        self.horizontalLayout = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tableWidget = QtGui.QTableWidget(Dialog)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(150)
        self.horizontalLayout.addWidget(self.tableWidget)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.pushButtonNouveau = QtGui.QPushButton(Dialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/std/icone/if_plus_circle_12296.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonNouveau.setIcon(icon)
        self.pushButtonNouveau.setObjectName(_fromUtf8("pushButtonNouveau"))
        self.verticalLayout.addWidget(self.pushButtonNouveau)
        self.pushButtonModifier = QtGui.QPushButton(Dialog)
        self.pushButtonModifier.setEnabled(False)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/std/icone/if_pencil_14623.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonModifier.setIcon(icon1)
        self.pushButtonModifier.setObjectName(_fromUtf8("pushButtonModifier"))
        self.verticalLayout.addWidget(self.pushButtonModifier)
        self.pushButtonParametres = QtGui.QPushButton(Dialog)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/std/icone/wrench-screwdriver-icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonParametres.setIcon(icon2)
        self.pushButtonParametres.setObjectName(_fromUtf8("pushButtonParametres"))
        self.verticalLayout.addWidget(self.pushButtonParametres)
        self.line = QtGui.QFrame(Dialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.pushButtonSupprimer = QtGui.QPushButton(Dialog)
        self.pushButtonSupprimer.setEnabled(False)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/std/icone/if_minus_10199.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonSupprimer.setIcon(icon3)
        self.pushButtonSupprimer.setObjectName(_fromUtf8("pushButtonSupprimer"))
        self.verticalLayout.addWidget(self.pushButtonSupprimer)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.pushButtonFermer = QtGui.QPushButton(Dialog)
        self.pushButtonFermer.setObjectName(_fromUtf8("pushButtonFermer"))
        self.verticalLayout.addWidget(self.pushButtonFermer)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Liste des Projets", None))
        self.pushButtonNouveau.setText(_translate("Dialog", "Nouveau", None))
        self.pushButtonModifier.setText(_translate("Dialog", "Modifier", None))
        self.pushButtonParametres.setText(_translate("Dialog", "Paramètres", None))
        self.pushButtonSupprimer.setText(_translate("Dialog", "Supprimer", None))
        self.pushButtonFermer.setText(_translate("Dialog", "Fermer", None))

import icons_rc
