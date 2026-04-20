# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'popupInfos.ui'
#
# Created: Mon Sep 11 12:07:58 2023
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

class Ui_INFORMATIONS(object):
    def setupUi(self, INFORMATIONS):
        INFORMATIONS.setObjectName(_fromUtf8("INFORMATIONS"))
        INFORMATIONS.resize(343, 237)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/sig/icone/information.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        INFORMATIONS.setWindowIcon(icon)
        self.verticalLayout_2 = QtGui.QVBoxLayout(INFORMATIONS)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.codeParcelle = QtGui.QLineEdit(INFORMATIONS)
        self.codeParcelle.setObjectName(_fromUtf8("codeParcelle"))
        self.verticalLayout.addWidget(self.codeParcelle)
        self.numDemandeCF = QtGui.QLineEdit(INFORMATIONS)
        self.numDemandeCF.setObjectName(_fromUtf8("numDemandeCF"))
        self.verticalLayout.addWidget(self.numDemandeCF)
        self.infos1 = QtGui.QLineEdit(INFORMATIONS)
        self.infos1.setObjectName(_fromUtf8("infos1"))
        self.verticalLayout.addWidget(self.infos1)
        self.infos2 = QtGui.QLineEdit(INFORMATIONS)
        self.infos2.setObjectName(_fromUtf8("infos2"))
        self.verticalLayout.addWidget(self.infos2)
        self.infos3 = QtGui.QLineEdit(INFORMATIONS)
        self.infos3.setObjectName(_fromUtf8("infos3"))
        self.verticalLayout.addWidget(self.infos3)
        self.infos5 = QtGui.QLineEdit(INFORMATIONS)
        self.infos5.setObjectName(_fromUtf8("infos5"))
        self.verticalLayout.addWidget(self.infos5)
        self.infos6 = QtGui.QLineEdit(INFORMATIONS)
        self.infos6.setObjectName(_fromUtf8("infos6"))
        self.verticalLayout.addWidget(self.infos6)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.line = QtGui.QFrame(INFORMATIONS)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout_2.addWidget(self.line)
        self.buttonsLayout = QtGui.QHBoxLayout()
        self.buttonsLayout.setObjectName(_fromUtf8("buttonsLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.buttonsLayout.addItem(spacerItem)
        self.pushButtonEditFisc = QtGui.QPushButton(INFORMATIONS)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/std/icone/if_pencil_14623.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonEditFisc.setIcon(icon1)
        self.pushButtonEditFisc.setObjectName(_fromUtf8("pushButtonEditFisc"))
        self.buttonsLayout.addWidget(self.pushButtonEditFisc)
        self.pushButtonCreateDemande = QtGui.QPushButton(INFORMATIONS)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/sig/icone/layer--plus.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonCreateDemande.setIcon(icon2)
        self.pushButtonCreateDemande.setObjectName(_fromUtf8("pushButtonCreateDemande"))
        self.buttonsLayout.addWidget(self.pushButtonCreateDemande)
        self.pushButtonCreateCert = QtGui.QPushButton(INFORMATIONS)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/std/icone/add_02.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonCreateCert.setIcon(icon3)
        self.pushButtonCreateCert.setObjectName(_fromUtf8("pushButtonCreateCert"))
        self.buttonsLayout.addWidget(self.pushButtonCreateCert)
        self.verticalLayout_2.addLayout(self.buttonsLayout)

        self.retranslateUi(INFORMATIONS)
        QtCore.QMetaObject.connectSlotsByName(INFORMATIONS)

    def retranslateUi(self, INFORMATIONS):
        INFORMATIONS.setWindowTitle(_translate("INFORMATIONS", "Infos", None))
        self.pushButtonEditFisc.setText(_translate("INFORMATIONS", "Editer (Fisc)", None))
        self.pushButtonCreateDemande.setText(_translate("INFORMATIONS", "Créer Demande", None))
        self.pushButtonCreateCert.setText(_translate("INFORMATIONS", "Créer un Certificat", None))

import icons_rc
