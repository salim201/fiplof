# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\plofstandalone\Parametres\EditContenance.ui'
#
# Created: Thu Mar 07 14:44:35 2019
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
        Dialog.resize(332, 98)
        Dialog.setWindowTitle(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/sig/icone/marker--pencil.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupbox = QtGui.QGroupBox(Dialog)
        self.groupbox.setObjectName(_fromUtf8("groupbox"))
        self.formLayout = QtGui.QFormLayout(self.groupbox)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_2 = QtGui.QLabel(self.groupbox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.lineEditContenance = QtGui.QLineEdit(self.groupbox)
        self.lineEditContenance.setObjectName(_fromUtf8("lineEditContenance"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEditContenance)
        self.verticalLayout.addWidget(self.groupbox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.line = QtGui.QFrame(Dialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.groupbox1 = QtGui.QGroupBox(Dialog)
        self.groupbox1.setObjectName(_fromUtf8("groupbox1"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupbox1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButtonOK = QtGui.QPushButton(self.groupbox1)
        self.pushButtonOK.setObjectName(_fromUtf8("pushButtonOK"))
        self.horizontalLayout.addWidget(self.pushButtonOK)
        self.pushButtonAnnuler = QtGui.QPushButton(self.groupbox1)
        self.pushButtonAnnuler.setObjectName(_fromUtf8("pushButtonAnnuler"))
        self.horizontalLayout.addWidget(self.pushButtonAnnuler)
        self.verticalLayout.addWidget(self.groupbox1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.lineEditContenance, self.pushButtonOK)
        Dialog.setTabOrder(self.pushButtonOK, self.pushButtonAnnuler)

    def retranslateUi(self, Dialog):
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Contenance", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonOK.setText(QtGui.QApplication.translate("Dialog", "MODIFIER", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAnnuler.setText(QtGui.QApplication.translate("Dialog", "Annuler", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc
