# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ListeFokontany.ui'
#
# Created: Tue Nov 28 10:52:44 2017
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
        Dialog.resize(462, 482)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 451, 101))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayoutWidget_2 = QtGui.QWidget(self.groupBox)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 30, 421, 61))
        self.gridLayoutWidget_2.setObjectName(_fromUtf8("gridLayoutWidget_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.ComboBoxCommune = gui.QgsFieldComboBox(self.gridLayoutWidget_2)
        self.ComboBoxCommune.setEditable(True)
        self.ComboBoxCommune.setObjectName(_fromUtf8("ComboBoxCommune"))
        self.gridLayout_3.addWidget(self.ComboBoxCommune, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.checkBoxTriCommune = QtGui.QCheckBox(self.gridLayoutWidget_2)
        self.checkBoxTriCommune.setObjectName(_fromUtf8("checkBoxTriCommune"))
        self.gridLayout_3.addWidget(self.checkBoxTriCommune, 1, 1, 1, 1)
        self.groupBox_3 = QtGui.QGroupBox(Dialog)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 420, 551, 41))
        self.groupBox_3.setTitle(_fromUtf8(""))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.groupBox_3)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(60, 0, 361, 41))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.BTAjout = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.BTAjout.setObjectName(_fromUtf8("BTAjout"))
        self.horizontalLayout.addWidget(self.BTAjout)
        self.BTSupprimer = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.BTSupprimer.setObjectName(_fromUtf8("BTSupprimer"))
        self.horizontalLayout.addWidget(self.BTSupprimer)
        self.BTModifier = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.BTModifier.setObjectName(_fromUtf8("BTModifier"))
        self.horizontalLayout.addWidget(self.BTModifier)
        self.BTFermer = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.BTFermer.setObjectName(_fromUtf8("BTFermer"))
        self.horizontalLayout.addWidget(self.BTFermer)
        self.groupBox_4 = QtGui.QGroupBox(Dialog)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 110, 451, 111))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.gridLayoutWidget = QtGui.QWidget(self.groupBox_4)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 30, 421, 74))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_4 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)
        self.nomFkt = QtGui.QLineEdit(self.gridLayoutWidget)
        self.nomFkt.setObjectName(_fromUtf8("nomFkt"))
        self.gridLayout_2.addWidget(self.nomFkt, 0, 1, 1, 1)
        self.codeFkt = QtGui.QLineEdit(self.gridLayoutWidget)
        self.codeFkt.setObjectName(_fromUtf8("codeFkt"))
        self.gridLayout_2.addWidget(self.codeFkt, 1, 1, 1, 1)
        self.verticalLayoutWidget = QtGui.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 250, 421, 161))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.listHameau = QtGui.QListWidget(self.verticalLayoutWidget)
        self.listHameau.setObjectName(_fromUtf8("listHameau"))
        self.verticalLayout.addWidget(self.listHameau)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Liste des fokontany", None))
        self.groupBox.setTitle(_translate("Dialog", "Commune", None))
        self.label.setText(_translate("Dialog", "Commune : ", None))
        self.checkBoxTriCommune.setText(_translate("Dialog", "Afficher par commune", None))
        self.BTAjout.setText(_translate("Dialog", "Ajouter", None))
        self.BTSupprimer.setText(_translate("Dialog", "Supprimer", None))
        self.BTModifier.setText(_translate("Dialog", "Modifier", None))
        self.BTFermer.setText(_translate("Dialog", "Fermer", None))
        self.groupBox_4.setTitle(_translate("Dialog", "Fokontany", None))
        self.label_4.setText(_translate("Dialog", "Nom", None))
        self.label_5.setText(_translate("Dialog", "Code", None))

from qgis import gui
