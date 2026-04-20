# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PopupInfosTitre.ui'
#
# Created: Sat Mar 16 11:27:34 2024
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
        INFORMATIONS.resize(303, 237)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/sig/icone/information.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        INFORMATIONS.setWindowIcon(icon)
        self.verticalLayout_2 = QtGui.QVBoxLayout(INFORMATIONS)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(INFORMATIONS)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 6, 0, 1, 1)
        self.label_7 = QtGui.QLabel(INFORMATIONS)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 0, 0, 1, 1)
        self.label_3 = QtGui.QLabel(INFORMATIONS)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.label_2 = QtGui.QLabel(INFORMATIONS)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 5, 0, 1, 1)
        self.label_6 = QtGui.QLabel(INFORMATIONS)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 1)
        self.label_5 = QtGui.QLabel(INFORMATIONS)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.label_4 = QtGui.QLabel(INFORMATIONS)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.titres = QtGui.QLineEdit(INFORMATIONS)
        self.titres.setObjectName(_fromUtf8("titres"))
        self.gridLayout.addWidget(self.titres, 0, 1, 1, 1)
        self.propriete = QtGui.QLineEdit(INFORMATIONS)
        self.propriete.setObjectName(_fromUtf8("propriete"))
        self.gridLayout.addWidget(self.propriete, 1, 1, 1, 1)
        self.sur_plan = QtGui.QLineEdit(INFORMATIONS)
        self.sur_plan.setObjectName(_fromUtf8("sur_plan"))
        self.gridLayout.addWidget(self.sur_plan, 2, 1, 1, 1)
        self.titre_r = QtGui.QLineEdit(INFORMATIONS)
        self.titre_r.setObjectName(_fromUtf8("titre_r"))
        self.gridLayout.addWidget(self.titre_r, 3, 1, 1, 1)
        self.parcelle = QtGui.QLineEdit(INFORMATIONS)
        self.parcelle.setObjectName(_fromUtf8("parcelle"))
        self.gridLayout.addWidget(self.parcelle, 4, 1, 1, 1)
        self.partie = QtGui.QLineEdit(INFORMATIONS)
        self.partie.setObjectName(_fromUtf8("partie"))
        self.gridLayout.addWidget(self.partie, 5, 1, 1, 1)
        self.feuille = QtGui.QLineEdit(INFORMATIONS)
        self.feuille.setObjectName(_fromUtf8("feuille"))
        self.gridLayout.addWidget(self.feuille, 6, 1, 1, 1)
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
        self.label.setText(_translate("INFORMATIONS", "FEUILLE", None))
        self.label_7.setText(_translate("INFORMATIONS", "TITRES", None))
        self.label_3.setText(_translate("INFORMATIONS", "PARCELLE", None))
        self.label_2.setText(_translate("INFORMATIONS", "PARTIE", None))
        self.label_6.setText(_translate("INFORMATIONS", "PROPRIETE", None))
        self.label_5.setText(_translate("INFORMATIONS", "SUR_PLAN", None))
        self.label_4.setText(_translate("INFORMATIONS", "TITRE_REQ", None))
        self.pushButtonValider.setText(_translate("INFORMATIONS", "Valider", None))
        self.pushButtonAnnuler.setText(_translate("INFORMATIONS", "Annuler", None))
        self.pushButtonEditFisc.setText(_translate("INFORMATIONS", "Editer", None))

import icons_rc
