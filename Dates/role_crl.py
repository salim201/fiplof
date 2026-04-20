# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'role_crl.ui'
#
# Created: Tue Jun 13 15:04:03 2023
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(625, 151)
        self.gridLayout_2 = QtGui.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(Dialog)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout.addWidget(self.pushButton_2, 3, 2, 1, 1)
        self.comboBoxRoleCrl = QtGui.QComboBox(Dialog)
        self.comboBoxRoleCrl.setObjectName(_fromUtf8("comboBoxRoleCrl"))
        self.gridLayout.addWidget(self.comboBoxRoleCrl, 0, 1, 1, 2)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 3, 1, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.lineEditSuppleant = QtGui.QLineEdit(Dialog)
        self.lineEditSuppleant.setObjectName(_fromUtf8("lineEditSuppleant"))
        self.gridLayout.addWidget(self.lineEditSuppleant, 2, 1, 1, 2)
        self.lineEditTitulaire = QtGui.QLineEdit(Dialog)
        self.lineEditTitulaire.setObjectName(_fromUtf8("lineEditTitulaire"))
        self.gridLayout.addWidget(self.lineEditTitulaire, 1, 1, 1, 2)
        self.toolButtonajoutsuppleant = QtGui.QToolButton(Dialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/std/icone/plus.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButtonajoutsuppleant.setIcon(icon)
        self.toolButtonajoutsuppleant.setObjectName(_fromUtf8("toolButtonajoutsuppleant"))
        self.gridLayout.addWidget(self.toolButtonajoutsuppleant, 2, 3, 1, 1)
        self.toolButtonajouttitualire = QtGui.QToolButton(Dialog)
        self.toolButtonajouttitualire.setIcon(icon)
        self.toolButtonajouttitualire.setObjectName(_fromUtf8("toolButtonajouttitualire"))
        self.gridLayout.addWidget(self.toolButtonajouttitualire, 1, 3, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 4, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Rôle CRL", None))
        self.label.setText(_translate("Dialog", "Rôle", None))
        self.pushButton_2.setText(_translate("Dialog", "Annuler", None))
        self.label_2.setText(_translate("Dialog", "Titulaire", None))
        self.pushButton.setText(_translate("Dialog", "Enregistrer", None))
        self.label_3.setText(_translate("Dialog", "Suppléant", None))
        self.toolButtonajoutsuppleant.setText(_translate("Dialog", "...", None))
        self.toolButtonajouttitualire.setText(_translate("Dialog", "...", None))

import icons_rc
