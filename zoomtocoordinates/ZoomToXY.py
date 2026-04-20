# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ztc.ui'
#
# Created: Fri Jul 20 20:57:02 2018
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

class Ui_ZoomToXY(object):
    def setupUi(self, ZoomToXY):
        ZoomToXY.setObjectName(_fromUtf8("ZoomToXY"))
        ZoomToXY.resize(518, 135)
        ZoomToXY.setModal(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/sig/icone/xy.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ZoomToXY.setWindowIcon(icon)
        self.gridLayout_2 = QtGui.QGridLayout(ZoomToXY)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tableWidget = QtGui.QTableWidget(ZoomToXY)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 2, 0, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setMargin(4)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.pushButton_2 = QtGui.QPushButton(ZoomToXY)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/std/icone/if_plus_circle_12296.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.verticalLayout_2.addWidget(self.pushButton_2)
        self.pushButton = QtGui.QPushButton(ZoomToXY)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/std/icone/if_minus_10199.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon2)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.verticalLayout_2.addWidget(self.pushButton)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 2, 1, 1, 2)
        self.horizontalGroupBox = QtGui.QGroupBox(ZoomToXY)
        self.horizontalGroupBox.setObjectName(_fromUtf8("horizontalGroupBox"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalGroupBox)
        self.horizontalLayout_2.setMargin(5)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.X = QtGui.QLabel(self.horizontalGroupBox)
        self.X.setObjectName(_fromUtf8("X"))
        self.horizontalLayout_2.addWidget(self.X)
        self.X_lineEdit = QtGui.QLineEdit(self.horizontalGroupBox)
        self.X_lineEdit.setObjectName(_fromUtf8("X_lineEdit"))
        self.horizontalLayout_2.addWidget(self.X_lineEdit)
        self.label_2 = QtGui.QLabel(self.horizontalGroupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.Y_lineEdit = QtGui.QLineEdit(self.horizontalGroupBox)
        self.Y_lineEdit.setObjectName(_fromUtf8("Y_lineEdit"))
        self.horizontalLayout_2.addWidget(self.Y_lineEdit)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.horizontalLayout_2.addItem(spacerItem)
        self.gridLayout_2.addWidget(self.horizontalGroupBox, 1, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setMargin(5)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.spinBox = QtGui.QSpinBox(ZoomToXY)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.horizontalLayout.addWidget(self.spinBox)
        self.span = QtGui.QPushButton(ZoomToXY)
        self.span.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/sig/icone/arrow-move.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.span.setIcon(icon3)
        self.span.setIconSize(QtCore.QSize(20, 20))
        self.span.setObjectName(_fromUtf8("span"))
        self.horizontalLayout.addWidget(self.span)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 1, 1, 1)

        self.retranslateUi(ZoomToXY)
        QtCore.QMetaObject.connectSlotsByName(ZoomToXY)

    def retranslateUi(self, ZoomToXY):
        ZoomToXY.setWindowTitle(_translate("ZoomToXY", "ZoomToXY", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("ZoomToXY", "X", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("ZoomToXY", "Y", None))
        self.pushButton_2.setText(_translate("ZoomToXY", "Ajouter", None))
        self.pushButton.setText(_translate("ZoomToXY", "Supprimer", None))
        self.X.setText(_translate("ZoomToXY", "X:", None))
        self.label_2.setText(_translate("ZoomToXY", "Y:", None))

import icons_rc
