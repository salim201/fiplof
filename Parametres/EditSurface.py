# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\plofstandalone\Parametres\EditSurface.ui'
#
# Created: Thu Mar 07 18:06:39 2019
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
        Dialog.setWindowModality(QtCore.Qt.NonModal)
        Dialog.setEnabled(True)
        Dialog.resize(484, 59)
        Dialog.setMouseTracking(False)
        Dialog.setAcceptDrops(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../icone/ic_edition.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setWindowOpacity(1.0)
        Dialog.setAutoFillBackground(True)
        Dialog.setStyleSheet(_fromUtf8(""))
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.horizontalGroupBox = QtGui.QGroupBox(Dialog)
        self.horizontalGroupBox.setGeometry(QtCore.QRect(20, 10, 160, 41))
        self.horizontalGroupBox.setObjectName(_fromUtf8("horizontalGroupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalGroupBox)
        self.horizontalLayout.setContentsMargins(6, 4, 6, 4)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEditSurface = QtGui.QLineEdit(self.horizontalGroupBox)
        self.lineEditSurface.setObjectName(_fromUtf8("lineEditSurface"))
        self.horizontalLayout.addWidget(self.lineEditSurface)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(190, 20, 47, 13))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalGroupBox_2 = QtGui.QGroupBox(Dialog)
        self.horizontalGroupBox_2.setGeometry(QtCore.QRect(220, 10, 251, 41))
        self.horizontalGroupBox_2.setObjectName(_fromUtf8("horizontalGroupBox_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalGroupBox_2)
        self.horizontalLayout_2.setContentsMargins(6, 4, 6, 4)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.update = QtGui.QPushButton(self.horizontalGroupBox_2)
        self.update.setObjectName(_fromUtf8("update"))
        self.horizontalLayout_2.addWidget(self.update)
        self.cancel = QtGui.QPushButton(self.horizontalGroupBox_2)
        self.cancel.setObjectName(_fromUtf8("cancel"))
        self.horizontalLayout_2.addWidget(self.cancel)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Parametrage Surface", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Ha", None, QtGui.QApplication.UnicodeUTF8))
        self.update.setText(QtGui.QApplication.translate("Dialog", "Modifier", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel.setText(QtGui.QApplication.translate("Dialog", "Annuler", None, QtGui.QApplication.UnicodeUTF8))

