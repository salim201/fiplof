# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UiTransparence.ui'
#
# Created: Sat Jun 09 10:27:40 2018
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
        Dialog.resize(363, 148)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/sig/icone/layer-transparent.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalSlider = QtGui.QSlider(Dialog)
        self.horizontalSlider.setEnabled(False)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName(_fromUtf8("horizontalSlider"))
        self.gridLayout.addWidget(self.horizontalSlider, 1, 0, 1, 1)
        self.checkBoxTransparence = QtGui.QCheckBox(Dialog)
        self.checkBoxTransparence.setObjectName(_fromUtf8("checkBoxTransparence"))
        self.gridLayout.addWidget(self.checkBoxTransparence, 0, 0, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
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
        self.pushButtonOK = QtGui.QPushButton(Dialog)
        self.pushButtonOK.setDefault(True)
        self.pushButtonOK.setObjectName(_fromUtf8("pushButtonOK"))
        self.horizontalLayout.addWidget(self.pushButtonOK)
        self.pushButtonCancel = QtGui.QPushButton(Dialog)
        self.pushButtonCancel.setAutoDefault(False)
        self.pushButtonCancel.setObjectName(_fromUtf8("pushButtonCancel"))
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Transparence", None))
        self.checkBoxTransparence.setText(_translate("Dialog", "Activer la transparence", None))
        self.label.setText(_translate("Dialog", "0%", None))
        self.pushButtonOK.setText(_translate("Dialog", "OK", None))
        self.pushButtonCancel.setText(_translate("Dialog", "Annuler", None))

import icons_rc
