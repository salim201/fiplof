# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PageHtml.ui'
#
# Created: Tue Dec 12 03:54:31 2017
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
        Dialog.resize(529, 390)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 306))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout.addWidget(self.groupBox)
        self.frame = QtGui.QFrame(Dialog)
        self.frame.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnImprimer = QtGui.QPushButton(self.frame)
        self.btnImprimer.setObjectName(_fromUtf8("btnImprimer"))
        self.horizontalLayout.addWidget(self.btnImprimer)
        self.btnEnreg = QtGui.QPushButton(self.frame)
        self.btnEnreg.setObjectName(_fromUtf8("btnEnreg"))
        self.horizontalLayout.addWidget(self.btnEnreg)
        self.btnFermer = QtGui.QPushButton(self.frame)
        self.btnFermer.setObjectName(_fromUtf8("btnFermer"))
        self.horizontalLayout.addWidget(self.btnFermer)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Export HTML", None))
        self.btnImprimer.setText(_translate("Dialog", "Imprimer", None))
        self.btnEnreg.setText(_translate("Dialog", "Enregistrer", None))
        self.btnFermer.setText(_translate("Dialog", "Fermer", None))

