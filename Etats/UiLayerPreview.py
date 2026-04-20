# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\plofstandalone\trunk\Etats\UiLayerPreview.ui'
#
# Created: Wed May 18 11:19:45 2022
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from qgis.gui import *
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_FormLayerPreview(object):
    def setupUi(self, FormLayerPreview):
        FormLayerPreview.setObjectName(_fromUtf8("FormLayerPreview"))
        FormLayerPreview.resize(272, 491)
        self.verticalLayout_2 = QtGui.QVBoxLayout(FormLayerPreview)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.frame = QtGui.QFrame(FormLayerPreview)
        self.frame.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.spinBoxGridX = QtGui.QSpinBox(self.frame)
        self.spinBoxGridX.setMinimum(1)
        self.spinBoxGridX.setMaximum(999999)
        self.spinBoxGridX.setProperty("value", 200)
        self.spinBoxGridX.setObjectName(_fromUtf8("spinBoxGridX"))
        self.horizontalLayout.addWidget(self.spinBoxGridX)
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.spinBoxGridY = QtGui.QSpinBox(self.frame)
        self.spinBoxGridY.setMinimum(1)
        self.spinBoxGridY.setMaximum(999999)
        self.spinBoxGridY.setProperty("value", 200)
        self.spinBoxGridY.setObjectName(_fromUtf8("spinBoxGridY"))
        self.horizontalLayout.addWidget(self.spinBoxGridY)
        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 3)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 3)

        self.verticalLayout_2.addWidget(self.frame)
        self.verticalLayoutPreview = QtGui.QVBoxLayout()
        self.verticalLayoutPreview.setObjectName(_fromUtf8("verticalLayoutPreview"))
        self.verticalLayout_2.addLayout(self.verticalLayoutPreview)

        self.retranslateUi(FormLayerPreview)
        QtCore.QMetaObject.connectSlotsByName(FormLayerPreview)


    def retranslateUi(self, FormLayerPreview):
        FormLayerPreview.setWindowTitle(QtGui.QApplication.translate("FormLayerPreview", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("FormLayerPreview", "Grille", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("FormLayerPreview", "x", None, QtGui.QApplication.UnicodeUTF8))

