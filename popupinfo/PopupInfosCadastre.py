# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PopupInfosCadastre.ui'
#
# Created: Sat Mar 16 11:05:52 2024
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
        INFORMATIONS.resize(303, 159)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/sig/icone/information.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        INFORMATIONS.setWindowIcon(icon)
        self.verticalLayout_2 = QtGui.QVBoxLayout(INFORMATIONS)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.nom_section = QtGui.QLineEdit(INFORMATIONS)
        self.nom_section.setObjectName(_fromUtf8("nom_section"))
        self.gridLayout.addWidget(self.nom_section, 0, 1, 1, 1)
        self.section = QtGui.QLineEdit(INFORMATIONS)
        self.section.setObjectName(_fromUtf8("section"))
        self.gridLayout.addWidget(self.section, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(INFORMATIONS)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(INFORMATIONS)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label = QtGui.QLabel(INFORMATIONS)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.parcelle = QtGui.QLineEdit(INFORMATIONS)
        self.parcelle.setObjectName(_fromUtf8("parcelle"))
        self.gridLayout.addWidget(self.parcelle, 2, 1, 1, 1)
        self.label_4 = QtGui.QLabel(INFORMATIONS)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.nom_plan = QtGui.QLineEdit(INFORMATIONS)
        self.nom_plan.setObjectName(_fromUtf8("nom_plan"))
        self.gridLayout.addWidget(self.nom_plan, 3, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.line = QtGui.QFrame(INFORMATIONS)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout_2.addWidget(self.line)
        self.buttonsLayout = QtGui.QHBoxLayout()
        self.buttonsLayout.setObjectName(_fromUtf8("buttonsLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.buttonsLayout.addItem(spacerItem)
        self.pushButtonValider = QtGui.QPushButton(INFORMATIONS)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/std/icone/accept.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonValider.setIcon(icon1)
        self.pushButtonValider.setObjectName(_fromUtf8("pushButtonValider"))
        self.buttonsLayout.addWidget(self.pushButtonValider)
        self.pushButtonAnnuler = QtGui.QPushButton(INFORMATIONS)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/sig/icone/cross.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonAnnuler.setIcon(icon2)
        self.pushButtonAnnuler.setObjectName(_fromUtf8("pushButtonAnnuler"))
        self.buttonsLayout.addWidget(self.pushButtonAnnuler)
        self.pushButtonEditFisc = QtGui.QPushButton(INFORMATIONS)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/std/icone/if_pencil_14623.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonEditFisc.setIcon(icon3)
        self.pushButtonEditFisc.setObjectName(_fromUtf8("pushButtonEditFisc"))
        self.buttonsLayout.addWidget(self.pushButtonEditFisc)
        self.verticalLayout_2.addLayout(self.buttonsLayout)

        self.retranslateUi(INFORMATIONS)
        QtCore.QMetaObject.connectSlotsByName(INFORMATIONS)

    def retranslateUi(self, INFORMATIONS):
        INFORMATIONS.setWindowTitle(_translate("INFORMATIONS", "Infos", None))
        self.label_2.setText(_translate("INFORMATIONS", "SECTION", None))
        self.label_3.setText(_translate("INFORMATIONS", "PARCELLE", None))
        self.label.setText(_translate("INFORMATIONS", "NOM_SECTION", None))
        self.label_4.setText(_translate("INFORMATIONS", "NOM_PLAN", None))
        self.pushButtonValider.setText(_translate("INFORMATIONS", "Valider", None))
        self.pushButtonAnnuler.setText(_translate("INFORMATIONS", "Annuler", None))
        self.pushButtonEditFisc.setText(_translate("INFORMATIONS", "Editer", None))

import icons_rc
