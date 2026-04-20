# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'StatsCertificat.ui'
#
# Created: Thu May 24 04:09:50 2018
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
        Dialog.resize(809, 426)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/std/icone/chart_bar.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.comboBoxSource = QtGui.QComboBox(Dialog)
        self.comboBoxSource.setObjectName(_fromUtf8("comboBoxSource"))
        self.comboBoxSource.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBoxSource, 0, 1, 1, 1)
        self.comboBoxTypeGraphe = QtGui.QComboBox(Dialog)
        self.comboBoxTypeGraphe.setEnabled(False)
        self.comboBoxTypeGraphe.setObjectName(_fromUtf8("comboBoxTypeGraphe"))
        self.comboBoxTypeGraphe.addItem(_fromUtf8(""))
        self.comboBoxTypeGraphe.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBoxTypeGraphe, 0, 3, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.spinBoxAmplitude = QtGui.QSpinBox(Dialog)
        self.spinBoxAmplitude.setEnabled(False)
        self.spinBoxAmplitude.setMinimum(1)
        self.spinBoxAmplitude.setObjectName(_fromUtf8("spinBoxAmplitude"))
        self.gridLayout.addWidget(self.spinBoxAmplitude, 0, 5, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 4, 1, 1)
        self.pushButtonGenerer = QtGui.QPushButton(Dialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/std/icone/cog_go.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonGenerer.setIcon(icon1)
        self.pushButtonGenerer.setAutoDefault(False)
        self.pushButtonGenerer.setObjectName(_fromUtf8("pushButtonGenerer"))
        self.gridLayout.addWidget(self.pushButtonGenerer, 0, 6, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tableWidget = QtGui.QTableWidget(Dialog)
        self.tableWidget.setMaximumSize(QtCore.QSize(216, 16777215))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.horizontalLayout.addWidget(self.tableWidget)
        self.graphicsView = PlotWidget(Dialog)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.horizontalLayout.addWidget(self.graphicsView)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButtonImprimer = QtGui.QPushButton(Dialog)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/std/icone/printer.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonImprimer.setIcon(icon2)
        self.pushButtonImprimer.setObjectName(_fromUtf8("pushButtonImprimer"))
        self.horizontalLayout_2.addWidget(self.pushButtonImprimer)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Statistique Des Certificats", None))
        self.comboBoxSource.setItemText(0, _translate("Dialog", "Age Propriétaire", None))
        self.comboBoxTypeGraphe.setItemText(0, _translate("Dialog", "Diagramme", None))
        self.comboBoxTypeGraphe.setItemText(1, _translate("Dialog", "Camembert", None))
        self.label.setText(_translate("Dialog", "Source De Données", None))
        self.label_2.setText(_translate("Dialog", "Type de Graphe", None))
        self.label_3.setText(_translate("Dialog", "Amplitude de Classe", None))
        self.pushButtonGenerer.setText(_translate("Dialog", "Générer", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Abscisse", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Ordonnées", None))
        self.pushButtonImprimer.setText(_translate("Dialog", "Imprimer", None))

from pyqtgraph import PlotWidget
import icons_rc
