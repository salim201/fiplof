# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'exportgeorefrasterdialog.ui'
#
# Created: Thu Aug 02 19:10:11 2018
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

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
        self.label.setGeometry(QtCore.QRect(10, 10, 71, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.checkBoxRotationMode = QtGui.QCheckBox(ExportGeorefRasterDialog)
        self.checkBoxRotationMode.setGeometry(QtCore.QRect(10, 40, 161, 17))
        self.checkBoxRotationMode.setObjectName(_fromUtf8("checkBoxRotationMode"))

        self.retranslateUi(ExportGeorefRasterDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ExportGeorefRasterDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ExportGeorefRasterDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ExportGeorefRasterDialog)

    def retranslateUi(self, ExportGeorefRasterDialog):
        ExportGeorefRasterDialog.setWindowTitle(QtGui.QApplication.translate("ExportGeorefRasterDialog", "Export georeferenced raster", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonBrowse.setText(QtGui.QApplication.translate("ExportGeorefRasterDialog", "Parcourir...", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ExportGeorefRasterDialog", "Chemin fichier :", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxRotationMode.setToolTip(QtGui.QApplication.translate("ExportGeorefRasterDialog", "<html><head/><body><p>If checked, the raster will be exported as is and the world file will contain the rotation, scaling and translation. Some GIS software may not be able to georeference the raster correctly in this mode. If unchecked, the raster will be modified with the rotation and the scaling between axis and the world file will contain the rest of the transformation.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxRotationMode.setText(QtGui.QApplication.translate("ExportGeorefRasterDialog", "Rotation", None, QtGui.QApplication.UnicodeUTF8))

