# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UiLayer.ui'
#
# Created: Sat Jul 21 04:30:46 2018
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
        Dialog.resize(510, 388)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/std/icone/wrench-screwdriver-icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayout = QtGui.QGridLayout(self.tab)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.frame = QtGui.QFrame(self.tab)
        self.frame.setMinimumSize(QtCore.QSize(200, 0))
        self.frame.setStyleSheet(_fromUtf8("background: white"))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout.addWidget(self.frame, 1, 1, 2, 1)
        self.groupBox = QtGui.QGroupBox(self.tab)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout = QtGui.QFormLayout(self.groupBox)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.checkBoxLabel = QtGui.QCheckBox(self.groupBox)
        self.checkBoxLabel.setObjectName(_fromUtf8("checkBoxLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.checkBoxLabel)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.fontComboBox = QtGui.QFontComboBox(self.groupBox)
        self.fontComboBox.setEnabled(False)
        self.fontComboBox.setObjectName(_fromUtf8("fontComboBox"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.fontComboBox)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.spinBoxLabelSize = QtGui.QSpinBox(self.groupBox)
        self.spinBoxLabelSize.setEnabled(False)
        self.spinBoxLabelSize.setMaximum(1000)
        self.spinBoxLabelSize.setProperty("value", 12)
        self.spinBoxLabelSize.setObjectName(_fromUtf8("spinBoxLabelSize"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.spinBoxLabelSize)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_3)
        self.pushButtonLabelColor = QtGui.QPushButton(self.groupBox)
        self.pushButtonLabelColor.setEnabled(False)
        self.pushButtonLabelColor.setObjectName(_fromUtf8("pushButtonLabelColor"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.pushButtonLabelColor)
        self.checkBoxMapUnit = QtGui.QCheckBox(self.groupBox)
        self.checkBoxMapUnit.setEnabled(False)
        self.checkBoxMapUnit.setObjectName(_fromUtf8("checkBoxMapUnit"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.checkBoxMapUnit)
        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(self.tab)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.formLayout_2 = QtGui.QFormLayout(self.groupBox_2)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.checkBoxBuffer = QtGui.QCheckBox(self.groupBox_2)
        self.checkBoxBuffer.setObjectName(_fromUtf8("checkBoxBuffer"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.checkBoxBuffer)
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_4)
        self.spinBoxBufferSize = QtGui.QSpinBox(self.groupBox_2)
        self.spinBoxBufferSize.setEnabled(False)
        self.spinBoxBufferSize.setObjectName(_fromUtf8("spinBoxBufferSize"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.spinBoxBufferSize)
        self.label_5 = QtGui.QLabel(self.groupBox_2)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_5)
        self.pushButtonBufferColor = QtGui.QPushButton(self.groupBox_2)
        self.pushButtonBufferColor.setEnabled(False)
        self.pushButtonBufferColor.setObjectName(_fromUtf8("pushButtonBufferColor"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.pushButtonBufferColor)
        self.gridLayout.addWidget(self.groupBox_2, 2, 0, 1, 1)
        self.checkBoxDarkBg = QtGui.QCheckBox(self.tab)
        self.checkBoxDarkBg.setObjectName(_fromUtf8("checkBoxDarkBg"))
        self.gridLayout.addWidget(self.checkBoxDarkBg, 3, 1, 1, 1)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonOK = QtGui.QPushButton(Dialog)
        self.pushButtonOK.setDefault(True)
        self.pushButtonOK.setObjectName(_fromUtf8("pushButtonOK"))
        self.horizontalLayout.addWidget(self.pushButtonOK)
        self.pushButtonCancel = QtGui.QPushButton(Dialog)
        self.pushButtonCancel.setAutoDefault(False)
        self.pushButtonCancel.setObjectName(_fromUtf8("pushButtonCancel"))
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Configuration de la couche", None))
        self.groupBox.setTitle(_translate("Dialog", "Texte du libellé", None))
        self.checkBoxLabel.setText(_translate("Dialog", "Afficher le libellé", None))
        self.label.setText(_translate("Dialog", "Police", None))
        self.label_2.setText(_translate("Dialog", "Taille", None))
        self.label_3.setText(_translate("Dialog", "Couleur", None))
        self.pushButtonLabelColor.setText(_translate("Dialog", "...", None))
        self.checkBoxMapUnit.setText(_translate("Dialog", "Taille en unité de carte", None))
        self.groupBox_2.setTitle(_translate("Dialog", "Contour du libellé", None))
        self.checkBoxBuffer.setText(_translate("Dialog", "Afficher le contour", None))
        self.label_4.setText(_translate("Dialog", "Taille", None))
        self.label_5.setText(_translate("Dialog", "Couleur", None))
        self.pushButtonBufferColor.setText(_translate("Dialog", "...", None))
        self.checkBoxDarkBg.setText(_translate("Dialog", "Aperçu en fond sombre", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Libellé", None))
        self.pushButtonOK.setText(_translate("Dialog", "OK", None))
        self.pushButtonCancel.setText(_translate("Dialog", "Annuler", None))

import icons_rc
