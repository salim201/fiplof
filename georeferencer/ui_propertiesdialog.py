# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'propertiesdialog.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(426, 340)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 3, 0, 1, 1)
        self.groupBox_Style = QtGui.QGroupBox(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_Style.sizePolicy().hasHeightForWidth())
        self.groupBox_Style.setSizePolicy(sizePolicy)
        self.groupBox_Style.setObjectName(_fromUtf8("groupBox_Style"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_Style)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.groupBox_Style)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.horizontalSlider_Transparency = QtGui.QSlider(self.groupBox_Style)
        self.horizontalSlider_Transparency.setMaximum(100)
        self.horizontalSlider_Transparency.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_Transparency.setObjectName(_fromUtf8("horizontalSlider_Transparency"))
        self.horizontalLayout_3.addWidget(self.horizontalSlider_Transparency)
        self.spinBox_Transparency = QtGui.QSpinBox(self.groupBox_Style)
        self.spinBox_Transparency.setMaximum(100)
        self.spinBox_Transparency.setObjectName(_fromUtf8("spinBox_Transparency"))
        self.horizontalLayout_3.addWidget(self.spinBox_Transparency)
        self.label_4 = QtGui.QLabel(self.groupBox_Style)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_3.addWidget(self.label_4)
        self.formLayout.setLayout(1, QtGui.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.formLayout)
        self.gridLayout_2.addWidget(self.groupBox_Style, 2, 0, 1, 1)
        self.groupBox_Properties = QtGui.QGroupBox(Dialog)
        self.groupBox_Properties.setObjectName(_fromUtf8("groupBox_Properties"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_Properties)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.textEdit_Properties = QtGui.QTextEdit(self.groupBox_Properties)
        self.textEdit_Properties.setReadOnly(True)
        self.textEdit_Properties.setTabStopWidth(80)
        self.textEdit_Properties.setObjectName(_fromUtf8("textEdit_Properties"))
        self.gridLayout_3.addWidget(self.textEdit_Properties, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_Properties, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Properties", None))
        self.groupBox_Style.setTitle(_translate("Dialog", "Style", None))
        self.label.setText(_translate("Dialog", "Transparency", None))
        self.label_4.setText(_translate("Dialog", "%", None))
        self.groupBox_Properties.setTitle(_translate("Dialog", "Properties", None))

