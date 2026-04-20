# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'listeCommunes.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 433)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(30, 20, 311, 91))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.labelDistrict = QtGui.QLabel(self.groupBox)
        self.labelDistrict.setGeometry(QtCore.QRect(40, 40, 46, 13))
        self.labelDistrict.setObjectName(_fromUtf8("labelDistrict"))
        self.comboDistrict = QtGui.QComboBox(self.groupBox)
        self.comboDistrict.setGeometry(QtCore.QRect(90, 30, 201, 22))
        self.comboDistrict.setObjectName(_fromUtf8("comboDistrict"))
        self.checkParDistrict = QtGui.QCheckBox(self.groupBox)
        self.checkParDistrict.setGeometry(QtCore.QRect(169, 60, 121, 20))
        self.checkParDistrict.setObjectName(_fromUtf8("checkParDistrict"))
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(30, 120, 311, 80))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.labelCommune = QtGui.QLabel(self.groupBox_2)
        self.labelCommune.setGeometry(QtCore.QRect(40, 20, 46, 13))
        self.labelCommune.setObjectName(_fromUtf8("labelCommune"))
        self.lineEditCommune = QtGui.QLineEdit(self.groupBox_2)
        self.lineEditCommune.setGeometry(QtCore.QRect(90, 20, 201, 20))
        self.lineEditCommune.setObjectName(_fromUtf8("lineEditCommune"))
        self.label = QtGui.QLabel(self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(40, 50, 46, 13))
        self.label.setObjectName(_fromUtf8("label"))
        self.lineEditCode = QtGui.QLineEdit(self.groupBox_2)
        self.lineEditCode.setGeometry(QtCore.QRect(90, 50, 201, 20))
        self.lineEditCode.setObjectName(_fromUtf8("lineEditCode"))
        self.tableWidgetCommunes = QtGui.QTableWidget(Dialog)
        self.tableWidgetCommunes.setGeometry(QtCore.QRect(30, 210, 311, 161))
        self.tableWidgetCommunes.setObjectName(_fromUtf8("tableWidgetCommunes"))
        self.tableWidgetCommunes.setColumnCount(3)
        self.tableWidgetCommunes.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetCommunes.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetCommunes.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetCommunes.setHorizontalHeaderItem(2, item)
        self.groupBox_3 = QtGui.QGroupBox(Dialog)
        self.groupBox_3.setGeometry(QtCore.QRect(30, 370, 311, 61))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.pushAjouter = QtGui.QPushButton(self.groupBox_3)
        self.pushAjouter.setGeometry(QtCore.QRect(10, 20, 71, 23))
        self.pushAjouter.setObjectName(_fromUtf8("pushAjouter"))
        self.pushModifier = QtGui.QPushButton(self.groupBox_3)
        self.pushModifier.setGeometry(QtCore.QRect(80, 20, 71, 23))
        self.pushModifier.setObjectName(_fromUtf8("pushModifier"))
        self.pushSupprimer = QtGui.QPushButton(self.groupBox_3)
        self.pushSupprimer.setGeometry(QtCore.QRect(150, 20, 75, 23))
        self.pushSupprimer.setObjectName(_fromUtf8("pushSupprimer"))
        self.pushFermer = QtGui.QPushButton(self.groupBox_3)
        self.pushFermer.setGeometry(QtCore.QRect(230, 20, 71, 23))
        self.pushFermer.setObjectName(_fromUtf8("pushFermer"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.groupBox.setTitle(_translate("Dialog", "District", None))
        self.labelDistrict.setText(_translate("Dialog", "Nom :", None))
        self.checkParDistrict.setText(_translate("Dialog", "Afficher par district", None))
        self.groupBox_2.setTitle(_translate("Dialog", "Commune", None))
        self.labelCommune.setText(_translate("Dialog", "Nom :", None))
        self.label.setText(_translate("Dialog", "Code :", None))
        item = self.tableWidgetCommunes.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Code district", None))
        item = self.tableWidgetCommunes.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Code commune", None))
        item = self.tableWidgetCommunes.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Nom", None))
        self.groupBox_3.setTitle(_translate("Dialog", "GroupBox", None))
        self.pushAjouter.setText(_translate("Dialog", "Ajouter", None))
        self.pushModifier.setText(_translate("Dialog", "Modifier", None))
        self.pushSupprimer.setText(_translate("Dialog", "Supprimer", None))
        self.pushFermer.setText(_translate("Dialog", "Fermer", None))

