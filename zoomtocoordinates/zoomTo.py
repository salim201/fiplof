# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'zoomTo.ui'
#
# Created: Sun Aug 19 17:51:54 2018
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
        #Dialog.setWindowModality(QtCore.Qt.NonModal)
        #self.dlg.setWindowModality(QtCore.Qt.NonModal)
        Dialog.resize(605, 57)
        Dialog.setSizeGripEnabled(True)
        Dialog.setModal(False)
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        self.horizontalGroupBox = QtGui.QGroupBox(Dialog)
        self.horizontalGroupBox.setGeometry(QtCore.QRect(10, 10, 501, 41))
        self.horizontalGroupBox.setObjectName(_fromUtf8("horizontalGroupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalGroupBox)
        self.horizontalLayout.setContentsMargins(6, 6, 14, 6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.horizontalGroupBox)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Agency FB"))
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit_2 = QtGui.QLineEdit(self.horizontalGroupBox)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.horizontalLayout.addWidget(self.lineEdit_2)
        self.label_2 = QtGui.QLabel(self.horizontalGroupBox)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Agency FB"))
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit = QtGui.QLineEdit(self.horizontalGroupBox)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(520, 20, 75, 23))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Agency FB"))
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("icons/zoom.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("icons/zoom.png")), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(18, 18))
        self.pushButton.setCheckable(True)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "ZoomTo XY", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "X:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Y:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "GoTo", None, QtGui.QApplication.UnicodeUTF8))

