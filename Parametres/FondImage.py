# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FondImage.ui'
#
# Created: Sat Jan 20 10:53:21 2018
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
        Dialog.resize(294, 134)
        Dialog.setMinimumSize(QtCore.QSize(294, 134))
        Dialog.setMaximumSize(QtCore.QSize(294, 134))
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lineEditFilename = QtGui.QLineEdit(Dialog)
        self.lineEditFilename.setObjectName(_fromUtf8("lineEditFilename"))
        self.horizontalLayout_2.addWidget(self.lineEditFilename)
        self.pushButtonBrowse = QtGui.QPushButton(Dialog)
        self.pushButtonBrowse.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/std/icone/if_folder_horizontal_open_11903.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonBrowse.setIcon(icon)
        self.pushButtonBrowse.setObjectName(_fromUtf8("pushButtonBrowse"))
        self.horizontalLayout_2.addWidget(self.pushButtonBrowse)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
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
        self.pushButtonOK = QtGui.QPushButton(Dialog)
        self.pushButtonOK.setObjectName(_fromUtf8("pushButtonOK"))
        self.horizontalLayout.addWidget(self.pushButtonOK)
        self.pushButtonAnnuler = QtGui.QPushButton(Dialog)
        self.pushButtonAnnuler.setObjectName(_fromUtf8("pushButtonAnnuler"))
        self.horizontalLayout.addWidget(self.pushButtonAnnuler)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Fond Image", None))
        self.label.setText(_translate("Dialog", "Chemin du Fichier Image :", None))
        self.pushButtonOK.setText(_translate("Dialog", "OK", None))
        self.pushButtonAnnuler.setText(_translate("Dialog", "Annuler", None))

import icons_rc
