# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogs/ui_xy_fields.ui'
#
# Created: Wed Mar 19 14:02:28 2014
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_XyFields(object):
    def setupUi(self, XyFields):
        XyFields.setObjectName(_fromUtf8("XyFields"))
        XyFields.resize(338, 274)
        XyFields.setModal(True)
        self.groupxy = QtGui.QGroupBox(XyFields)
        self.groupxy.setEnabled(True)
        self.groupxy.setGeometry(QtCore.QRect(20, 20, 289, 234))
        self.groupxy.setObjectName(_fromUtf8("groupxy"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupxy)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.cmbXcoord = QtGui.QComboBox(self.groupxy)
        self.cmbXcoord.setObjectName(_fromUtf8("cmbXcoord"))
        self.gridLayout_2.addWidget(self.cmbXcoord, 1, 1, 1, 1)
        self.cmbYcoord = QtGui.QComboBox(self.groupxy)
        self.cmbYcoord.setObjectName(_fromUtf8("cmbYcoord"))
        self.gridLayout_2.addWidget(self.cmbYcoord, 2, 1, 1, 1)
        self.buttonBox_2 = QtGui.QDialogButtonBox(self.groupxy)
        self.buttonBox_2.setEnabled(False)
        self.buttonBox_2.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_2.setStandardButtons(QtGui.QDialogButtonBox.NoButton)
        self.buttonBox_2.setObjectName(_fromUtf8("buttonBox_2"))
        self.gridLayout_2.addWidget(self.buttonBox_2, 5, 1, 1, 1)
        self.label = QtGui.QLabel(self.groupxy)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupxy)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(self.groupxy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 6, 1, 1, 1)
        self.textEdit = QtGui.QTextEdit(self.groupxy)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout_2.addWidget(self.textEdit, 0, 0, 1, 2)

        self.retranslateUi(XyFields)
        self.cmbXcoord.setCurrentIndex(-1)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), XyFields.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), XyFields.reject)
        QtCore.QMetaObject.connectSlotsByName(XyFields)

    def retranslateUi(self, XyFields):
        XyFields.setWindowTitle(_translate("XyFields", "XYTools - Coordinate fields", None))
        self.groupxy.setTitle(_translate("XyFields", "layer", None))
        self.label.setText(_translate("XyFields", "X: ", None))
        self.label_2.setText(_translate("XyFields", "Y:", None))
        self.textEdit.setHtml(_translate("XyFields", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:10pt;\">Veuillez selectionner deux attributs ...</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\'; font-size:10pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:10pt;\"></span></p></body></html>", None))

