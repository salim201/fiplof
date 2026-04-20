# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loaderrordialog.ui'
#
# Created: Mon Mar 12 15:57:00 2018
#      by: PyQt4 UI code generator 4.10.2
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

class Ui_LoadError(object):
    def setupUi(self, LoadError):
        LoadError.setObjectName(_fromUtf8("LoadError"))
        LoadError.resize(460, 126)
        LoadError.setModal(True)
        self.buttonBox = QtGui.QDialogButtonBox(LoadError)
        self.buttonBox.setGeometry(QtCore.QRect(80, 90, 371, 23))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.lineEditImagePath = QtGui.QLineEdit(LoadError)
        self.lineEditImagePath.setGeometry(QtCore.QRect(90, 50, 271, 20))
        self.lineEditImagePath.setObjectName(_fromUtf8("lineEditImagePath"))
        self.pushButtonBrowse = QtGui.QPushButton(LoadError)
        self.pushButtonBrowse.setGeometry(QtCore.QRect(370, 50, 81, 23))
        self.pushButtonBrowse.setObjectName(_fromUtf8("pushButtonBrowse"))
        self.label = QtGui.QLabel(LoadError)
        self.label.setGeometry(QtCore.QRect(10, 50, 71, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.lblError = QtGui.QLabel(LoadError)
        self.lblError.setGeometry(QtCore.QRect(10, 10, 431, 31))
        self.lblError.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lblError.setWordWrap(True)
        self.lblError.setObjectName(_fromUtf8("lblError"))

        self.retranslateUi(LoadError)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), LoadError.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), LoadError.reject)
        QtCore.QMetaObject.connectSlotsByName(LoadError)
        LoadError.setTabOrder(self.lineEditImagePath, self.pushButtonBrowse)
        LoadError.setTabOrder(self.pushButtonBrowse, self.buttonBox)

    def retranslateUi(self, LoadError):
        LoadError.setWindowTitle(_translate("LoadError", "Freehand Raster Georeferencer - Image not found", None))
        self.pushButtonBrowse.setText(_translate("LoadError", "Browse...", None))
        self.label.setText(_translate("LoadError", "Image path", None))
        self.lblError.setText(_translate("LoadError", "LabelError", None))

