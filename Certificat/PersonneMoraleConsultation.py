# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PersonneMoraleConsultation.ui'
#
# Created: Tue Nov 28 11:03:39 2017
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
        Dialog.resize(443, 346)
        self.frame = QtGui.QFrame(Dialog)
        self.frame.setEnabled(False)
        self.frame.setGeometry(QtCore.QRect(10, 10, 421, 161))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayoutWidget = QtGui.QWidget(self.frame)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 401, 146))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.comboBoxType = QtGui.QComboBox(self.gridLayoutWidget)
        self.comboBoxType.setObjectName(_fromUtf8("comboBoxType"))
        self.gridLayout.addWidget(self.comboBoxType, 0, 2, 1, 1)
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.comboBoxDateCreate = QtGui.QComboBox(self.gridLayoutWidget)
        self.comboBoxDateCreate.setObjectName(_fromUtf8("comboBoxDateCreate"))
        self.gridLayout.addWidget(self.comboBoxDateCreate, 2, 2, 1, 1)
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEditNom = QtGui.QLineEdit(self.gridLayoutWidget)
        self.lineEditNom.setObjectName(_fromUtf8("lineEditNom"))
        self.gridLayout.addWidget(self.lineEditNom, 1, 2, 1, 1)
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEditSiege = QtGui.QLineEdit(self.gridLayoutWidget)
        self.lineEditSiege.setObjectName(_fromUtf8("lineEditSiege"))
        self.gridLayout.addWidget(self.lineEditSiege, 3, 2, 1, 1)
        self.label_4 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.btnListe = QtGui.QPushButton(self.gridLayoutWidget)
        self.btnListe.setObjectName(_fromUtf8("btnListe"))
        self.gridLayout.addWidget(self.btnListe, 0, 3, 1, 1)
        self.toolBtnCalendrier = QtGui.QToolButton(self.gridLayoutWidget)
        self.toolBtnCalendrier.setObjectName(_fromUtf8("toolBtnCalendrier"))
        self.gridLayout.addWidget(self.toolBtnCalendrier, 2, 3, 1, 1)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setEnabled(False)
        self.groupBox.setGeometry(QtCore.QRect(10, 170, 421, 131))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.textEdit = QtGui.QTextEdit(self.groupBox)
        self.textEdit.setGeometry(QtCore.QRect(3, 30, 411, 91))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.horizontalLayoutWidget = QtGui.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(299, 300, 131, 41))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnFermer = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.btnFermer.setObjectName(_fromUtf8("btnFermer"))
        self.horizontalLayout.addWidget(self.btnFermer)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Personne morale", None))
        self.label_3.setText(_translate("Dialog", "Dtae de création", None))
        self.label.setText(_translate("Dialog", "Type", None))
        self.label_2.setText(_translate("Dialog", "Dénomination", None))
        self.label_4.setText(_translate("Dialog", "Siège", None))
        self.btnListe.setText(_translate("Dialog", "Liste", None))
        self.toolBtnCalendrier.setText(_translate("Dialog", "...", None))
        self.groupBox.setTitle(_translate("Dialog", "Observations", None))
        self.btnFermer.setText(_translate("Dialog", "Fermer", None))

