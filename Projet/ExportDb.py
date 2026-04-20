# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ExportDb.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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
        Dialog.resize(339, 190)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 60, 46, 13))
        self.label.setObjectName(_fromUtf8("label"))
        self.comboExport = QtGui.QComboBox(Dialog)
        self.comboExport.setGeometry(QtCore.QRect(110, 50, 201, 22))
        self.comboExport.setObjectName(_fromUtf8("comboExport"))
        self.comboExport.addItem(_fromUtf8(""))
        self.comboExport.addItem(_fromUtf8(""))
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(150, 130, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.checkBox = QtGui.QCheckBox(Dialog)
        self.checkBox.setGeometry(QtCore.QRect(180, 80, 131, 20))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.pushButton_2 = QtGui.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(230, 130, 75, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "Format :", None))
        self.comboExport.setItemText(0, _translate("Dialog", "SQL", None))
        self.comboExport.setItemText(1, _translate("Dialog", "SHAPEFILE", None))
        self.pushButton.setText(_translate("Dialog", "Lancer", None))
        self.checkBox.setText(_translate("Dialog", "Base de données PLOF", None))
        self.pushButton_2.setText(_translate("Dialog", "Annuler", None))

