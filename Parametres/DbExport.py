# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DbExport.ui'
#
# Created: Thu Feb 22 04:28:24 2018
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
        Dialog.resize(375, 374)
        self.formLayoutWidget = QtGui.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(9, 9, 361, 163))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setMargin(10)
        self.formLayout.setHorizontalSpacing(12)
        self.formLayout.setVerticalSpacing(10)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.nomDuFichierLabel = QtGui.QLabel(self.formLayoutWidget)
        self.nomDuFichierLabel.setObjectName(_fromUtf8("nomDuFichierLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.nomDuFichierLabel)
        self.formatLabel = QtGui.QLabel(self.formLayoutWidget)
        self.formatLabel.setObjectName(_fromUtf8("formatLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.formatLabel)
        self.formatComboBox = QtGui.QComboBox(self.formLayoutWidget)
        self.formatComboBox.setObjectName(_fromUtf8("formatComboBox"))
        self.formatComboBox.addItem(_fromUtf8(""))
        self.formatComboBox.addItem(_fromUtf8(""))
        self.formatComboBox.addItem(_fromUtf8(""))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.formatComboBox)
        self.codageLabel = QtGui.QLabel(self.formLayoutWidget)
        self.codageLabel.setObjectName(_fromUtf8("codageLabel"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.codageLabel)
        self.codageComboBox = QtGui.QComboBox(self.formLayoutWidget)
        self.codageComboBox.setObjectName(_fromUtf8("codageComboBox"))
        self.codageComboBox.addItem(_fromUtf8(""))
        self.codageComboBox.addItem(_fromUtf8(""))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.codageComboBox)
        self.nomDuRoleLabel = QtGui.QLabel(self.formLayoutWidget)
        self.nomDuRoleLabel.setObjectName(_fromUtf8("nomDuRoleLabel"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.nomDuRoleLabel)
        self.nomDuRoleComboBox = QtGui.QComboBox(self.formLayoutWidget)
        self.nomDuRoleComboBox.setObjectName(_fromUtf8("nomDuRoleComboBox"))
        self.nomDuRoleComboBox.addItem(_fromUtf8(""))
        self.nomDuRoleComboBox.setItemText(0, _fromUtf8(""))
        self.nomDuRoleComboBox.addItem(_fromUtf8(""))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.nomDuRoleComboBox)
        self.pushButton_2 = QtGui.QPushButton(self.formLayoutWidget)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.pushButton_2)
        self.verticalLayoutWidget = QtGui.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 150, 361, 131))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.listWidgetOutPut = QtGui.QListWidget(self.verticalLayoutWidget)
        self.listWidgetOutPut.setObjectName(_fromUtf8("listWidgetOutPut"))
        self.verticalLayout.addWidget(self.listWidgetOutPut)
        self.verticalLayoutWidget_2 = QtGui.QWidget(Dialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 290, 361, 31))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.progressBar = QtGui.QProgressBar(self.verticalLayoutWidget_2)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout_2.addWidget(self.progressBar)
        self.horizontalLayoutWidget = QtGui.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 330, 361, 31))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.Lancer = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.Lancer.setObjectName(_fromUtf8("Lancer"))
        self.horizontalLayout_2.addWidget(self.Lancer)
        self.pushButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_2.addWidget(self.pushButton)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Sauvegarder la base \"XXXX\"", None, QtGui.QApplication.UnicodeUTF8))
        self.nomDuFichierLabel.setText(QtGui.QApplication.translate("Dialog", "Nom du fichier", None, QtGui.QApplication.UnicodeUTF8))
        self.formatLabel.setText(QtGui.QApplication.translate("Dialog", "Format", None, QtGui.QApplication.UnicodeUTF8))
        self.formatComboBox.setItemText(0, QtGui.QApplication.translate("Dialog", "Personnalise", None, QtGui.QApplication.UnicodeUTF8))
        self.formatComboBox.setItemText(1, QtGui.QApplication.translate("Dialog", "Tar", None, QtGui.QApplication.UnicodeUTF8))
        self.formatComboBox.setItemText(2, QtGui.QApplication.translate("Dialog", "Fichier plat", None, QtGui.QApplication.UnicodeUTF8))
        self.codageLabel.setText(QtGui.QApplication.translate("Dialog", "Codage", None, QtGui.QApplication.UnicodeUTF8))
        self.codageComboBox.setItemText(0, QtGui.QApplication.translate("Dialog", "UTF8", None, QtGui.QApplication.UnicodeUTF8))
        self.codageComboBox.setItemText(1, QtGui.QApplication.translate("Dialog", "LATIN1", None, QtGui.QApplication.UnicodeUTF8))
        self.nomDuRoleLabel.setText(QtGui.QApplication.translate("Dialog", "Nom du role", None, QtGui.QApplication.UnicodeUTF8))
        self.nomDuRoleComboBox.setItemText(1, QtGui.QApplication.translate("Dialog", "Postgres", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("Dialog", "Parcourir ...", None, QtGui.QApplication.UnicodeUTF8))
        self.Lancer.setText(QtGui.QApplication.translate("Dialog", "Lancer", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Annuler", None, QtGui.QApplication.UnicodeUTF8))

