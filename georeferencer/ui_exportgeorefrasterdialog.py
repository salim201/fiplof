# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'exportgeorefrasterdialog.ui'
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

class Ui_ExportGeorefRasterDialog(object):
    def setupUi(self, ExportGeorefRasterDialog):
        ExportGeorefRasterDialog.setObjectName(_fromUtf8("ExportGeorefRasterDialog"))
        ExportGeorefRasterDialog.resize(458, 94)
        self.buttonBox = QtGui.QDialogButtonBox(ExportGeorefRasterDialog)
        self.buttonBox.setGeometry(QtCore.QRect(110, 60, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.lineEditImagePath = QtGui.QLineEdit(ExportGeorefRasterDialog)
        self.lineEditImagePath.setGeometry(QtCore.QRect(90, 10, 271, 20))
        self.lineEditImagePath.setObjectName(_fromUtf8("lineEditImagePath"))
        self.pushButtonBrowse = QtGui.QPushButton(ExportGeorefRasterDialog)
        self.pushButtonBrowse.setGeometry(QtCore.QRect(370, 10, 81, 23))
        self.pushButtonBrowse.setObjectName(_fromUtf8("pushButtonBrowse"))
        self.label = QtGui.QLabel(ExportGeorefRasterDialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 71, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.checkBoxRotationMode = QtGui.QCheckBox(ExportGeorefRasterDialog)
        self.checkBoxRotationMode.setGeometry(QtCore.QRect(10, 40, 161, 17))
        self.checkBoxRotationMode.setObjectName(_fromUtf8("checkBoxRotationMode"))

        self.retranslateUi(ExportGeorefRasterDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ExportGeorefRasterDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ExportGeorefRasterDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ExportGeorefRasterDialog)

    def retranslateUi(self, ExportGeorefRasterDialog):
        ExportGeorefRasterDialog.setWindowTitle(_translate("ExportGeorefRasterDialog", "Export georeferenced raster", None))
        self.pushButtonBrowse.setText(_translate("ExportGeorefRasterDialog", "Browse...", None))
        self.label.setText(_translate("ExportGeorefRasterDialog", "Image path", None))
        self.checkBoxRotationMode.setToolTip(_translate("ExportGeorefRasterDialog", "<html><head/><body><p>If checked, the raster will be exported as is and the world file will contain the rotation, scaling and translation. Some GIS software may not be able to georeference the raster correctly in this mode. If unchecked, the raster will be modified with the rotation and the scaling between axis and the world file will contain the rest of the transformation.</p></body></html>", None))
        self.checkBoxRotationMode.setText(_translate("ExportGeorefRasterDialog", "Put rotation in world file ", None))

