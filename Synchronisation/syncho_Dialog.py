# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'syncho_Dialog.ui'
#
# Created: Tue Mar 19 11:24:27 2024
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

class Ui_Synchronisation(object):
    def setupUi(self, Synchronisation):
        Synchronisation.setObjectName(_fromUtf8("Synchronisation"))
        Synchronisation.resize(743, 133)
        self.verticalLayoutWidget = QtGui.QWidget(Synchronisation)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 39, 731, 71))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.verticalLayoutWidget)
        self.label.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.progressBar = QtGui.QProgressBar(self.verticalLayoutWidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)

        self.retranslateUi(Synchronisation)
        QtCore.QMetaObject.connectSlotsByName(Synchronisation)

    def retranslateUi(self, Synchronisation):
        Synchronisation.setWindowTitle(_translate("Synchronisation", "Dialog", None))
        self.label.setText(_translate("Synchronisation", "Tentative de synchronisation", None))

