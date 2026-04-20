# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ListeContribuables.ui'
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
        Dialog.setEnabled(True)
        Dialog.resize(717, 337)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 0, 700, 81))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.checkBox_3 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_3.setGeometry(QtCore.QRect(360, 20, 121, 17))
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.checkBox_4 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_4.setGeometry(QtCore.QRect(360, 50, 190, 17))
        self.checkBox_4.setObjectName(_fromUtf8("checkBox_4"))
        self.lineEdit_5 = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_5.setGeometry(QtCore.QRect(110, 50, 220, 20))
        self.lineEdit_5.setObjectName(_fromUtf8("lineEdit_5"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 50, 100, 13))
        self.label.setObjectName(_fromUtf8("label"))
        self.pushButton_4 = QtGui.QPushButton(self.groupBox)
        self.pushButton_4.setGeometry(QtCore.QRect(580, 50, 90, 23))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.comboBox = QtGui.QComboBox(self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(110, 20, 190, 22))
        self.comboBox.setEditable(True)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 20, 100, 13))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.tableWidget = QtGui.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(10, 90, 701, 191))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 290, 700, 41))
        self.groupBox_2.setTitle(_fromUtf8(""))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.pushButton = QtGui.QPushButton(self.groupBox_2)
        self.pushButton.setGeometry(QtCore.QRect(530, 10, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_3 = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_3.setGeometry(QtCore.QRect(620, 10, 75, 23))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Liste des contribuables", None))
        self.groupBox.setTitle(_translate("Dialog", "Recherche", None))
        self.checkBox_3.setText(_translate("Dialog", "Tous/ par fokontany", None))
        self.checkBox_4.setText(_translate("Dialog", "Parcelle groupé par fokontany", None))
        self.label.setText(_translate("Dialog", "Année :", None))
        self.pushButton_4.setText(_translate("Dialog", "Rechercher", None))
        self.label_2.setText(_translate("Dialog", "Fokontany :", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Nom", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Date de naissance", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Lieu", None))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "CIN", None))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "Hetra (tany)", None))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Dialog", "Hetra (trano)", None))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Dialog", "Total", None))
        self.pushButton.setText(_translate("Dialog", "Imprimer liste", None))
        self.pushButton_3.setText(_translate("Dialog", "Fermer", None))

