# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'intervalle.ui'
#
# Created: Sat Nov 25 13:42:13 2017
#      by: PyQt4 UI code generator 4.11.2
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
        Dialog.resize(400, 185)
        self.verticalLayoutWidget = QtGui.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 381, 171))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.debutLabel = QtGui.QLabel(self.verticalLayoutWidget)
        self.debutLabel.setObjectName(_fromUtf8("debutLabel"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.debutLabel)
        self.dButLineEdit = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.dButLineEdit.setObjectName(_fromUtf8("dButLineEdit"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.dButLineEdit)
        self.finLabel = QtGui.QLabel(self.verticalLayoutWidget)
        self.finLabel.setObjectName(_fromUtf8("finLabel"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.finLabel)
        self.finLineEdit = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.finLineEdit.setObjectName(_fromUtf8("finLineEdit"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.finLineEdit)
        self.horizontalLayout_2.addLayout(self.formLayout_2)
        self.formLayout_6 = QtGui.QFormLayout()
        self.formLayout_6.setObjectName(_fromUtf8("formLayout_6"))
        self.Label = QtGui.QLabel(self.verticalLayoutWidget)
        self.Label.setObjectName(_fromUtf8("Label"))
        self.formLayout_6.setWidget(0, QtGui.QFormLayout.LabelRole, self.Label)
        self.ComboBox = QtGui.QComboBox(self.verticalLayoutWidget)
        self.ComboBox.setObjectName(_fromUtf8("ComboBox"))
        self.ComboBox.addItem(_fromUtf8(""))
        self.ComboBox.addItem(_fromUtf8(""))
        self.ComboBox.addItem(_fromUtf8(""))
        self.ComboBox.addItem(_fromUtf8(""))
        self.formLayout_6.setWidget(0, QtGui.QFormLayout.FieldRole, self.ComboBox)
        self.Label_2 = QtGui.QLabel(self.verticalLayoutWidget)
        self.Label_2.setObjectName(_fromUtf8("Label_2"))
        self.formLayout_6.setWidget(1, QtGui.QFormLayout.LabelRole, self.Label_2)
        self.ComboBox_2 = QtGui.QComboBox(self.verticalLayoutWidget)
        self.ComboBox_2.setObjectName(_fromUtf8("ComboBox_2"))
        self.ComboBox_2.addItem(_fromUtf8(""))
        self.ComboBox_2.addItem(_fromUtf8(""))
        self.ComboBox_2.addItem(_fromUtf8(""))
        self.ComboBox_2.addItem(_fromUtf8(""))
        self.formLayout_6.setWidget(1, QtGui.QFormLayout.FieldRole, self.ComboBox_2)
        self.horizontalLayout_2.addLayout(self.formLayout_6)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_2 = QtGui.QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Intervalle", None))
        self.debutLabel.setText(_translate("Dialog", "Début", None))
        self.finLabel.setText(_translate("Dialog", "Fin", None))
        self.Label.setText(_translate("Dialog", " ", None))
        self.ComboBox.setItemText(0, _translate("Dialog", "m2", None))
        self.ComboBox.setItemText(1, _translate("Dialog", "a", None))
        self.ComboBox.setItemText(2, _translate("Dialog", "Ha", None))
        self.ComboBox.setItemText(3, _translate("Dialog", "Pièces", None))
        self.Label_2.setText(_translate("Dialog", " ", None))
        self.ComboBox_2.setItemText(0, _translate("Dialog", "m2", None))
        self.ComboBox_2.setItemText(1, _translate("Dialog", "a", None))
        self.ComboBox_2.setItemText(2, _translate("Dialog", "Ha", None))
        self.ComboBox_2.setItemText(3, _translate("Dialog", "Pièces", None))
        self.pushButton_2.setText(_translate("Dialog", "Ok", None))
        self.pushButton.setText(_translate("Dialog", "Annuler", None))

