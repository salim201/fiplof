# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'territoire.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(225, 174)
        Form.setStyleSheet(_fromUtf8("QGroupBox { \n"
"     border: 1px solid rgb(150,150,150); \n"
"     border-radius: 5px; \n"
"     padding: 5px 0;\n"
"    font-weight:bold;\n"
" } "))
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout = QtGui.QFormLayout(self.groupBox)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.checkBoxRegion = QtGui.QCheckBox(self.groupBox)
        self.checkBoxRegion.setObjectName(_fromUtf8("checkBoxRegion"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.checkBoxRegion)
        self.comboBoxRegion = QtGui.QComboBox(self.groupBox)
        self.comboBoxRegion.setEnabled(False)
        self.comboBoxRegion.setObjectName(_fromUtf8("comboBoxRegion"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBoxRegion)
        self.checkBoxDistrict = QtGui.QCheckBox(self.groupBox)
        self.checkBoxDistrict.setObjectName(_fromUtf8("checkBoxDistrict"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.checkBoxDistrict)
        self.comboBoxDistrict = QtGui.QComboBox(self.groupBox)
        self.comboBoxDistrict.setEnabled(False)
        self.comboBoxDistrict.setObjectName(_fromUtf8("comboBoxDistrict"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.comboBoxDistrict)
        self.checkBoxCommune = QtGui.QCheckBox(self.groupBox)
        self.checkBoxCommune.setObjectName(_fromUtf8("checkBoxCommune"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.checkBoxCommune)
        self.comboBoxCommune = QtGui.QComboBox(self.groupBox)
        self.comboBoxCommune.setEnabled(False)
        self.comboBoxCommune.setObjectName(_fromUtf8("comboBoxCommune"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.comboBoxCommune)
        self.checkBoxFokontany = QtGui.QCheckBox(self.groupBox)
        self.checkBoxFokontany.setObjectName(_fromUtf8("checkBoxFokontany"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.checkBoxFokontany)
        self.comboBoxFokontany = QtGui.QComboBox(self.groupBox)
        self.comboBoxFokontany.setEnabled(False)
        self.comboBoxFokontany.setObjectName(_fromUtf8("comboBoxFokontany"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.comboBoxFokontany)
        self.horizontalLayout.addWidget(self.groupBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.checkBoxRegion.setText(_translate("Form", "Region", None))
        self.checkBoxDistrict.setText(_translate("Form", "District", None))
        self.checkBoxCommune.setText(_translate("Form", "Commune", None))
        self.checkBoxFokontany.setText(_translate("Form", "Fokontany", None))

