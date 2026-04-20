# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UiTypePersonneMorale.ui'
#
# Created: Tue Jun 12 04:21:52 2018
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
        Dialog.resize(333, 143)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/users/icone/user_02.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.lineEditType = QtGui.QLineEdit(Dialog)
        self.lineEditType.setMaxLength(50)
        self.lineEditType.setObjectName(_fromUtf8("lineEditType"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEditType)
        self.lineEditKarazany = QtGui.QLineEdit(Dialog)
        self.lineEditKarazany.setMaxLength(50)
        self.lineEditKarazany.setObjectName(_fromUtf8("lineEditKarazany"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEditKarazany)
        self.verticalLayout.addLayout(self.formLayout)
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
        self.pushButtonEnregistrer = QtGui.QPushButton(Dialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/std/icone/disk.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonEnregistrer.setIcon(icon1)
        self.pushButtonEnregistrer.setObjectName(_fromUtf8("pushButtonEnregistrer"))
        self.horizontalLayout.addWidget(self.pushButtonEnregistrer)
        self.pushButtonAnnuler = QtGui.QPushButton(Dialog)
        self.pushButtonAnnuler.setObjectName(_fromUtf8("pushButtonAnnuler"))
        self.horizontalLayout.addWidget(self.pushButtonAnnuler)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Edition Type de Personne Morale", None))
        self.label.setText(_translate("Dialog", "Type", None))
        self.label_2.setText(_translate("Dialog", "Karazany", None))
        self.pushButtonEnregistrer.setText(_translate("Dialog", "Enregistrer", None))
        self.pushButtonAnnuler.setText(_translate("Dialog", "Annuler", None))

import icons_rc
