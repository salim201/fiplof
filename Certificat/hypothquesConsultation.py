# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hypothquesConsultation.ui'
#
# Created: Tue Nov 28 10:48:20 2017
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
        Dialog.resize(545, 444)
        self.frame = QtGui.QFrame(Dialog)
        self.frame.setEnabled(False)
        self.frame.setGeometry(QtCore.QRect(10, 10, 521, 281))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayoutWidget = QtGui.QWidget(self.frame)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 501, 152))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lineEditValeur = QtGui.QLineEdit(self.gridLayoutWidget)
        self.lineEditValeur.setObjectName(_fromUtf8("lineEditValeur"))
        self.gridLayout.addWidget(self.lineEditValeur, 2, 1, 1, 1)
        self.lineEditDateInscri = QtGui.QLineEdit(self.gridLayoutWidget)
        self.lineEditDateInscri.setObjectName(_fromUtf8("lineEditDateInscri"))
        self.gridLayout.addWidget(self.lineEditDateInscri, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit_4 = QtGui.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.gridLayout.addWidget(self.lineEdit_4, 3, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.lineEditDuree = QtGui.QLineEdit(self.gridLayoutWidget)
        self.lineEditDuree.setObjectName(_fromUtf8("lineEditDuree"))
        self.gridLayout.addWidget(self.lineEditDuree, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 2, 2, 1, 1)
        self.verticalLayoutWidget = QtGui.QWidget(self.frame)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 170, 491, 104))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_6 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.verticalLayout.addWidget(self.label_6)
        self.textEditDesc = QtGui.QTextEdit(self.verticalLayoutWidget)
        self.textEditDesc.setObjectName(_fromUtf8("textEditDesc"))
        self.verticalLayout.addWidget(self.textEditDesc)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setEnabled(False)
        self.groupBox.setGeometry(QtCore.QRect(10, 310, 521, 91))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayoutWidget_2 = QtGui.QWidget(self.groupBox)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(20, 30, 471, 41))
        self.gridLayoutWidget_2.setObjectName(_fromUtf8("gridLayoutWidget_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_7 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)
        self.lineEditDateRediation = QtGui.QLineEdit(self.gridLayoutWidget_2)
        self.lineEditDateRediation.setObjectName(_fromUtf8("lineEditDateRediation"))
        self.gridLayout_2.addWidget(self.lineEditDateRediation, 0, 1, 1, 1)
        self.horizontalLayoutWidget = QtGui.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(210, 390, 299, 41))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnAide = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.btnAide.setObjectName(_fromUtf8("btnAide"))
        self.horizontalLayout.addWidget(self.btnAide)
        self.btnFermer = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.btnFermer.setObjectName(_fromUtf8("btnFermer"))
        self.horizontalLayout.addWidget(self.btnFermer)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Hypothèque sur le certificat", None))
        self.label_3.setText(_translate("Dialog", "Valeur", None))
        self.label.setText(_translate("Dialog", "Date d\'inscription dans le régistre", None))
        self.label_4.setText(_translate("Dialog", "Créanciers", None))
        self.label_2.setText(_translate("Dialog", "Durée", None))
        self.label_5.setText(_translate("Dialog", "Ar", None))
        self.label_6.setText(_translate("Dialog", "Description", None))
        self.groupBox.setTitle(_translate("Dialog", "Radiation", None))
        self.label_7.setText(_translate("Dialog", "Date de radiation", None))
        self.btnAide.setText(_translate("Dialog", "Aide", None))
        self.btnFermer.setText(_translate("Dialog", "Fermer", None))

