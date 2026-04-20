# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'VoirListeContribuable.ui'
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
        Dialog.resize(598, 416)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 0, 581, 141))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.checkBox = QtGui.QCheckBox(self.groupBox)
        self.checkBox.setGeometry(QtCore.QRect(30, 20, 101, 17))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.checkBox_2 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_2.setGeometry(QtCore.QRect(30, 50, 80, 17))
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.lineEdit = QtGui.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(140, 20, 290, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.pushButton_2 = QtGui.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(430, 110, 110, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.lineEdit_4 = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_4.setGeometry(QtCore.QRect(140, 50, 200, 20))
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.lineEdit_5 = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_5.setGeometry(QtCore.QRect(140, 110, 200, 20))
        self.lineEdit_5.setObjectName(_fromUtf8("lineEdit_5"))
        self.checkBox_3 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_3.setGeometry(QtCore.QRect(30, 80, 100, 17))
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.checkBox_4 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_4.setGeometry(QtCore.QRect(30, 110, 80, 17))
        self.checkBox_4.setObjectName(_fromUtf8("checkBox_4"))
        self.lineEdit_12 = QtGui.QLineEdit(Dialog)
        self.lineEdit_12.setGeometry(QtCore.QRect(300, 80, 41, 20))
        self.lineEdit_12.setObjectName(_fromUtf8("lineEdit_12"))
        self.lineEdit_6 = QtGui.QLineEdit(Dialog)
        self.lineEdit_6.setGeometry(QtCore.QRect(150, 80, 41, 20))
        self.lineEdit_6.setObjectName(_fromUtf8("lineEdit_6"))
        self.lineEdit_11 = QtGui.QLineEdit(Dialog)
        self.lineEdit_11.setGeometry(QtCore.QRect(250, 80, 41, 20))
        self.lineEdit_11.setObjectName(_fromUtf8("lineEdit_11"))
        self.lineEdit_10 = QtGui.QLineEdit(Dialog)
        self.lineEdit_10.setGeometry(QtCore.QRect(200, 80, 41, 20))
        self.lineEdit_10.setObjectName(_fromUtf8("lineEdit_10"))
        self.groupBox_3 = QtGui.QGroupBox(Dialog)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 150, 581, 221))
        self.groupBox_3.setTitle(_fromUtf8(""))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.pushButton_4 = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 10, 60, 23))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.tableWidget = QtGui.QTableWidget(self.groupBox_3)
        self.tableWidget.setGeometry(QtCore.QRect(0, 40, 580, 151))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.pushButton_5 = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_5.setGeometry(QtCore.QRect(0, 190, 75, 30))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.pushButton_6 = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_6.setGeometry(QtCore.QRect(70, 190, 75, 30))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.pushButton_7 = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_7.setGeometry(QtCore.QRect(500, 190, 81, 30))
        self.pushButton_7.setObjectName(_fromUtf8("pushButton_7"))
        self.pushButton_8 = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_8.setGeometry(QtCore.QRect(430, 190, 75, 30))
        self.pushButton_8.setObjectName(_fromUtf8("pushButton_8"))
        self.pushButton_9 = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_9.setGeometry(QtCore.QRect(360, 190, 75, 30))
        self.pushButton_9.setObjectName(_fromUtf8("pushButton_9"))
        self.comboBox_3 = QtGui.QComboBox(self.groupBox_3)
        self.comboBox_3.setGeometry(QtCore.QRect(230, 190, 130, 30))
        self.comboBox_3.setEditable(True)
        self.comboBox_3.setObjectName(_fromUtf8("comboBox_3"))
        self.lineEdit_3 = QtGui.QLineEdit(self.groupBox_3)
        self.lineEdit_3.setEnabled(False)
        self.lineEdit_3.setGeometry(QtCore.QRect(140, 190, 90, 30))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.pushButton_3 = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_3.setGeometry(QtCore.QRect(70, 10, 90, 23))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.groupBox_4 = QtGui.QGroupBox(Dialog)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 370, 580, 41))
        self.groupBox_4.setTitle(_fromUtf8(""))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.pushButton = QtGui.QPushButton(self.groupBox_4)
        self.pushButton.setGeometry(QtCore.QRect(380, 10, 100, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_10 = QtGui.QPushButton(self.groupBox_4)
        self.pushButton_10.setGeometry(QtCore.QRect(500, 10, 75, 23))
        self.pushButton_10.setObjectName(_fromUtf8("pushButton_10"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Liste des contribuable", None))
        self.groupBox.setTitle(_translate("Dialog", "Critère de recherche", None))
        self.checkBox.setText(_translate("Dialog", "Nom :", None))
        self.checkBox_2.setText(_translate("Dialog", "Prénom :", None))
        self.pushButton_2.setText(_translate("Dialog", "Rechercher", None))
        self.checkBox_3.setText(_translate("Dialog", "N° CIN :", None))
        self.checkBox_4.setText(_translate("Dialog", "N° Acte :", None))
        self.pushButton_4.setText(_translate("Dialog", "Voir", None))
        self.pushButton_5.setText(_translate("Dialog", "<<=", None))
        self.pushButton_6.setText(_translate("Dialog", "<=", None))
        self.pushButton_7.setText(_translate("Dialog", "=>>", None))
        self.pushButton_8.setText(_translate("Dialog", "=>", None))
        self.pushButton_9.setText(_translate("Dialog", "ll", None))
        self.pushButton_3.setText(_translate("Dialog", "Modifier", None))
        self.pushButton.setText(_translate("Dialog", "Sélectionner", None))
        self.pushButton_10.setText(_translate("Dialog", "Fermer", None))

