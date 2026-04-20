# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CreationPropositionDomainePublic.ui'
#
# Created: Fri Jul 06 20:19:09 2018
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
        Dialog.resize(837, 283)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 451, 211))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lineEditNom = QtGui.QLineEdit(self.groupBox)
        self.lineEditNom.setObjectName(_fromUtf8("lineEditNom"))
        self.gridLayout.addWidget(self.lineEditNom, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.textEditObservation = QtGui.QTextEdit(self.groupBox)
        self.textEditObservation.setObjectName(_fromUtf8("textEditObservation"))
        self.gridLayout.addWidget(self.textEditObservation, 2, 0, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.horizontalLayoutWidget_2 = QtGui.QWidget(Dialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 230, 451, 41))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.btnAide = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.btnAide.setObjectName(_fromUtf8("btnAide"))
        self.horizontalLayout_2.addWidget(self.btnAide)
        self.btnCreer = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.btnCreer.setObjectName(_fromUtf8("btnCreer"))
        self.horizontalLayout_2.addWidget(self.btnCreer)
        self.btnAnnuler = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.btnAnnuler.setObjectName(_fromUtf8("btnAnnuler"))
        self.horizontalLayout_2.addWidget(self.btnAnnuler)
        self.checkBox = QtGui.QCheckBox(self.horizontalLayoutWidget_2)
        self.checkBox.setText(_fromUtf8(""))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.horizontalLayout_2.addWidget(self.checkBox)
        self.horizontalLayoutWidget = QtGui.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(479, 19, 351, 251))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayoutGeom = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayoutGeom.setMargin(0)
        self.horizontalLayoutGeom.setObjectName(_fromUtf8("horizontalLayoutGeom"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Créatio d\'une proposition de domaine public", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Domaine public", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Nom", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Observations", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAide.setText(QtGui.QApplication.translate("Dialog", "Aide", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCreer.setText(QtGui.QApplication.translate("Dialog", "Créer", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAnnuler.setText(QtGui.QApplication.translate("Dialog", "Annuler", None, QtGui.QApplication.UnicodeUTF8))

