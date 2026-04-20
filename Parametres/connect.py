# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connect.ui'
#
# Created: Fri May 04 23:39:03 2018
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
        Dialog.resize(313, 134)
        Dialog.setMinimumSize(QtCore.QSize(313, 134))
        Dialog.setMaximumSize(QtCore.QSize(313, 134))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/std/icone/unlock.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout_2 = QtGui.QFormLayout(self.groupBox)
        self.formLayout_2.setContentsMargins(14, 6, 8, 9)
        self.formLayout_2.setHorizontalSpacing(6)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.loginLabel = QtGui.QLabel(self.groupBox)
        self.loginLabel.setObjectName(_fromUtf8("loginLabel"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.loginLabel)
        self.loginLineEdit = QtGui.QLineEdit(self.groupBox)
        self.loginLineEdit.setObjectName(_fromUtf8("loginLineEdit"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.loginLineEdit)
        self.motDePasseLabel = QtGui.QLabel(self.groupBox)
        self.motDePasseLabel.setObjectName(_fromUtf8("motDePasseLabel"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.motDePasseLabel)
        self.motDePasseLineEdit = QtGui.QLineEdit(self.groupBox)
        self.motDePasseLineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.motDePasseLineEdit.setObjectName(_fromUtf8("motDePasseLineEdit"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.motDePasseLineEdit)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox1 = QtGui.QGroupBox(Dialog)
        self.groupBox1.setObjectName(_fromUtf8("groupBox1"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonConnexion = QtGui.QPushButton(self.groupBox1)
        self.pushButtonConnexion.setObjectName(_fromUtf8("pushButtonConnexion"))
        self.horizontalLayout.addWidget(self.pushButtonConnexion)
        self.pushButtonAnnuler = QtGui.QPushButton(self.groupBox1)
        self.pushButtonAnnuler.setObjectName(_fromUtf8("pushButtonAnnuler"))
        self.horizontalLayout.addWidget(self.pushButtonAnnuler)
        self.verticalLayout.addWidget(self.groupBox1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.loginLineEdit, self.motDePasseLineEdit)
        Dialog.setTabOrder(self.motDePasseLineEdit, self.pushButtonConnexion)
        Dialog.setTabOrder(self.pushButtonConnexion, self.pushButtonAnnuler)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Connexion Fi-PLOF", None))
        self.loginLabel.setText(_translate("Dialog", "Login", None))
        self.motDePasseLabel.setText(_translate("Dialog", "Mot de passe", None))
        self.pushButtonConnexion.setText(_translate("Dialog", "Connexion", None))
        self.pushButtonAnnuler.setText(_translate("Dialog", "Annuler", None))

import icons_rc
