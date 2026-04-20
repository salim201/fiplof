# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ChoixTypeActe.ui'
#
# Created: Sat Apr 07 17:51:51 2018
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
        Dialog.resize(262, 152)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalGroupBox = QtGui.QGroupBox(Dialog)
        self.horizontalGroupBox.setObjectName(_fromUtf8("horizontalGroupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalGroupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.radioButtonNouveau = QtGui.QRadioButton(self.horizontalGroupBox)
        self.radioButtonNouveau.setObjectName(_fromUtf8("radioButtonNouveau"))
        self.horizontalLayout.addWidget(self.radioButtonNouveau)
        self.radioButtonExistant = QtGui.QRadioButton(self.horizontalGroupBox)
        self.radioButtonExistant.setObjectName(_fromUtf8("radioButtonExistant"))
        self.horizontalLayout.addWidget(self.radioButtonExistant)
        self.verticalLayout_2.addWidget(self.horizontalGroupBox)
        self.verticalGroupBox = QtGui.QGroupBox(Dialog)
        self.verticalGroupBox.setObjectName(_fromUtf8("verticalGroupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalGroupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.radioButtonActePublic = QtGui.QRadioButton(self.verticalGroupBox)
        self.radioButtonActePublic.setObjectName(_fromUtf8("radioButtonActePublic"))
        self.verticalLayout.addWidget(self.radioButtonActePublic)
        self.radioButtonActePrive = QtGui.QRadioButton(self.verticalGroupBox)
        self.radioButtonActePrive.setObjectName(_fromUtf8("radioButtonActePrive"))
        self.verticalLayout.addWidget(self.radioButtonActePrive)
        self.verticalLayout_2.addWidget(self.verticalGroupBox)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btnOk = QtGui.QPushButton(Dialog)
        self.btnOk.setObjectName(_fromUtf8("btnOk"))
        self.horizontalLayout_2.addWidget(self.btnOk)
        self.btnAnnuler = QtGui.QPushButton(Dialog)
        self.btnAnnuler.setObjectName(_fromUtf8("btnAnnuler"))
        self.horizontalLayout_2.addWidget(self.btnAnnuler)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Choix de type d\'acte", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonNouveau.setText(QtGui.QApplication.translate("Dialog", "Nouveau", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonExistant.setText(QtGui.QApplication.translate("Dialog", "Existant ", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonActePublic.setText(QtGui.QApplication.translate("Dialog", "Acte public", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonActePrive.setText(QtGui.QApplication.translate("Dialog", "Acte privé", None, QtGui.QApplication.UnicodeUTF8))
        self.btnOk.setText(QtGui.QApplication.translate("Dialog", "Ok", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAnnuler.setText(QtGui.QApplication.translate("Dialog", "Annuler", None, QtGui.QApplication.UnicodeUTF8))

