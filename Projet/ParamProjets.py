# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ParamProjets.ui'
#
# Created: Sat May 05 00:39:00 2018
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
        Dialog.resize(504, 447)
        Dialog.setMinimumSize(QtCore.QSize(504, 447))
        Dialog.setMaximumSize(QtCore.QSize(504, 447))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/std/icone/wrench-screwdriver-icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.comboBoxProjets = QtGui.QComboBox(Dialog)
        self.comboBoxProjets.setObjectName(_fromUtf8("comboBoxProjets"))
        self.gridLayout.addWidget(self.comboBoxProjets, 0, 1, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(150, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 4, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.comboBoxCommunes = QtGui.QComboBox(Dialog)
        self.comboBoxCommunes.setObjectName(_fromUtf8("comboBoxCommunes"))
        self.gridLayout.addWidget(self.comboBoxCommunes, 0, 3, 1, 1)
        self.gridLayout.setColumnStretch(1, 150)
        self.gridLayout.setColumnStretch(3, 150)
        self.verticalLayout.addLayout(self.gridLayout)
        self.frame = QtGui.QFrame(Dialog)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButtonAddLayer = QtGui.QPushButton(self.frame)
        self.pushButtonAddLayer.setStyleSheet(_fromUtf8("padding: 6px"))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/sig/icone/layer_add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonAddLayer.setIcon(icon1)
        self.pushButtonAddLayer.setAutoDefault(False)
        self.pushButtonAddLayer.setObjectName(_fromUtf8("pushButtonAddLayer"))
        self.horizontalLayout.addWidget(self.pushButtonAddLayer)
        self.pushButtonDelLayer = QtGui.QPushButton(self.frame)
        self.pushButtonDelLayer.setEnabled(False)
        self.pushButtonDelLayer.setStyleSheet(_fromUtf8("padding: 6px"))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/sig/icone/layer_del.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonDelLayer.setIcon(icon2)
        self.pushButtonDelLayer.setAutoDefault(False)
        self.pushButtonDelLayer.setObjectName(_fromUtf8("pushButtonDelLayer"))
        self.horizontalLayout.addWidget(self.pushButtonDelLayer)
        self.pushButtonUp = QtGui.QPushButton(self.frame)
        self.pushButtonUp.setEnabled(False)
        self.pushButtonUp.setStyleSheet(_fromUtf8("padding: 6px"))
        self.pushButtonUp.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/arrows/icone/bullet_arrow_up.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonUp.setIcon(icon3)
        self.pushButtonUp.setAutoDefault(False)
        self.pushButtonUp.setObjectName(_fromUtf8("pushButtonUp"))
        self.horizontalLayout.addWidget(self.pushButtonUp)
        self.pushButtonDown = QtGui.QPushButton(self.frame)
        self.pushButtonDown.setEnabled(False)
        self.pushButtonDown.setStyleSheet(_fromUtf8("padding: 6px"))
        self.pushButtonDown.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/arrows/icone/bullet_arrow_down.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonDown.setIcon(icon4)
        self.pushButtonDown.setAutoDefault(False)
        self.pushButtonDown.setObjectName(_fromUtf8("pushButtonDown"))
        self.horizontalLayout.addWidget(self.pushButtonDown)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.frame)
        self.tableWidget = QtGui.QTableWidget(Dialog)
        self.tableWidget.setEnabled(True)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.tableWidget.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.pushButtonAppliquer = QtGui.QPushButton(Dialog)
        self.pushButtonAppliquer.setObjectName(_fromUtf8("pushButtonAppliquer"))
        self.horizontalLayout_2.addWidget(self.pushButtonAppliquer)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Paramètres Des Projets", None))
        self.label.setText(_translate("Dialog", "Projet", None))
        self.label_2.setText(_translate("Dialog", "Commune", None))
        self.pushButtonAddLayer.setText(_translate("Dialog", "Ajouter une Couche", None))
        self.pushButtonDelLayer.setText(_translate("Dialog", "Supprimer Couche", None))
        self.pushButtonUp.setToolTip(_translate("Dialog", "Remonter la Couche", None))
        self.pushButtonDown.setToolTip(_translate("Dialog", "Descendre la Couche", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Libellé", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Type", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Fichier", None))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Fond", None))
        self.pushButtonAppliquer.setText(_translate("Dialog", "Appliquer", None))

import icons_rc
