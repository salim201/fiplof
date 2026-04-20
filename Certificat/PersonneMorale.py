# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PersonneMorale.ui'
#
# Created: Mon Feb  9 18:53:47 2026
#      by: PyQt4 UI code generator 4.10
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
        Dialog.resize(491, 393)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/users/icone/user_02.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame = QtGui.QFrame(Dialog)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.comboBoxType = QtGui.QComboBox(self.frame)
        self.comboBoxType.setObjectName(_fromUtf8("comboBoxType"))
        self.gridLayout.addWidget(self.comboBoxType, 0, 2, 1, 1)
        self.label = QtGui.QLabel(self.frame)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.btnListe = QtGui.QPushButton(self.frame)
        self.btnListe.setObjectName(_fromUtf8("btnListe"))
        self.gridLayout.addWidget(self.btnListe, 0, 3, 1, 1)
        self.label_4 = QtGui.QLabel(self.frame)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.dateEditCreation = QtGui.QDateEdit(self.frame)
        self.dateEditCreation.setCalendarPopup(True)
        self.dateEditCreation.setObjectName(_fromUtf8("dateEditCreation"))
        self.gridLayout.addWidget(self.dateEditCreation, 2, 2, 1, 1)
        self.lineEditNom = QtGui.QLineEdit(self.frame)
        self.lineEditNom.setObjectName(_fromUtf8("lineEditNom"))
        self.gridLayout.addWidget(self.lineEditNom, 1, 2, 1, 1)
        self.lineEditSiege = QtGui.QLineEdit(self.frame)
        self.lineEditSiege.setObjectName(_fromUtf8("lineEditSiege"))
        self.gridLayout.addWidget(self.lineEditSiege, 3, 2, 1, 1)
        self.label_5 = QtGui.QLabel(self.frame)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.lineEditNomRepresentant = QtGui.QLineEdit(self.frame)
        self.lineEditNomRepresentant.setReadOnly(True)
        self.lineEditNomRepresentant.setObjectName(_fromUtf8("lineEditNomRepresentant"))
        self.gridLayout.addWidget(self.lineEditNomRepresentant, 4, 2, 1, 1)
        self.pushButtonListePP = QtGui.QPushButton(self.frame)
        self.pushButtonListePP.setObjectName(_fromUtf8("pushButtonListePP"))
        self.gridLayout.addWidget(self.pushButtonListePP, 4, 3, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout.addWidget(self.frame)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.textEdit = QtGui.QTextEdit(self.groupBox)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.verticalLayout_3.addWidget(self.textEdit)
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(9, -1, 9, 9)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnOk = QtGui.QPushButton(Dialog)
        self.btnOk.setDefault(True)
        self.btnOk.setObjectName(_fromUtf8("btnOk"))
        self.horizontalLayout.addWidget(self.btnOk)
        self.btnAnnuler = QtGui.QPushButton(Dialog)
        self.btnAnnuler.setAutoDefault(False)
        self.btnAnnuler.setObjectName(_fromUtf8("btnAnnuler"))
        self.horizontalLayout.addWidget(self.btnAnnuler)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.comboBoxType, self.lineEditNom)
        Dialog.setTabOrder(self.lineEditNom, self.dateEditCreation)
        Dialog.setTabOrder(self.dateEditCreation, self.lineEditSiege)
        Dialog.setTabOrder(self.lineEditSiege, self.textEdit)
        Dialog.setTabOrder(self.textEdit, self.btnOk)
        Dialog.setTabOrder(self.btnOk, self.btnListe)
        Dialog.setTabOrder(self.btnListe, self.btnAnnuler)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Personne morale", None))
        self.label.setText(_translate("Dialog", "Type", None))
        self.label_3.setText(_translate("Dialog", "Dtae de création", None))
        self.label_2.setText(_translate("Dialog", "Dénomination", None))
        self.btnListe.setText(_translate("Dialog", "Liste", None))
        self.label_4.setText(_translate("Dialog", "Siège", None))
        self.label_5.setText(_translate("Dialog", "Represenatant", None))
        self.pushButtonListePP.setText(_translate("Dialog", "Liste", None))
        self.groupBox.setTitle(_translate("Dialog", "Observations", None))
        self.btnOk.setText(_translate("Dialog", "Enregistrer", None))
        self.btnAnnuler.setText(_translate("Dialog", "Annuler", None))

import icons_rc
