# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Params.ui'
#
# Created: Mon Nov 11 08:29:59 2024
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

class Ui_Params(object):
    def setupUi(self, Params):
        Params.setObjectName(_fromUtf8("Params"))
        Params.resize(528, 119)
        self.verticalLayout = QtGui.QVBoxLayout(Params)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lineEditPathAutoSave = QtGui.QLineEdit(Params)
        self.lineEditPathAutoSave.setMinimumSize(QtCore.QSize(300, 0))
        self.lineEditPathAutoSave.setObjectName(_fromUtf8("lineEditPathAutoSave"))
        self.gridLayout.addWidget(self.lineEditPathAutoSave, 0, 1, 1, 1)
        self.toolButtonParcourir = QtGui.QToolButton(Params)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/std/icone/if_folder_horizontal_open_11903.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButtonParcourir.setIcon(icon)
        self.toolButtonParcourir.setObjectName(_fromUtf8("toolButtonParcourir"))
        self.gridLayout.addWidget(self.toolButtonParcourir, 0, 2, 1, 1)
        self.checkBoxOnLineInterco = QtGui.QCheckBox(Params)
        self.checkBoxOnLineInterco.setObjectName(_fromUtf8("checkBoxOnLineInterco"))
        self.gridLayout.addWidget(self.checkBoxOnLineInterco, 2, 0, 1, 1)
        self.label = QtGui.QLabel(Params)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.checkBoxZCertifiable = QtGui.QCheckBox(Params)
        self.checkBoxZCertifiable.setObjectName(_fromUtf8("checkBoxZCertifiable"))
        self.gridLayout.addWidget(self.checkBoxZCertifiable, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonEnregistrer = QtGui.QPushButton(Params)
        self.pushButtonEnregistrer.setObjectName(_fromUtf8("pushButtonEnregistrer"))
        self.horizontalLayout.addWidget(self.pushButtonEnregistrer)
        self.pushButtonFermer = QtGui.QPushButton(Params)
        self.pushButtonFermer.setObjectName(_fromUtf8("pushButtonFermer"))
        self.horizontalLayout.addWidget(self.pushButtonFermer)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Params)
        QtCore.QMetaObject.connectSlotsByName(Params)

    def retranslateUi(self, Params):
        Params.setWindowTitle(_translate("Params", "Options supplémentaires", None))
        self.toolButtonParcourir.setText(_translate("Params", "...", None))
        self.checkBoxOnLineInterco.setText(_translate("Params", "Interconnexion en ligne", None))
        self.label.setText(_translate("Params", "Chemin de sauvegarde automatique", None))
        self.checkBoxZCertifiable.setText(_translate("Params", "Avec zone certifiable", None))
        self.pushButtonEnregistrer.setText(_translate("Params", "Enregistrer", None))
        self.pushButtonFermer.setText(_translate("Params", "Fermer", None))

import icons_rc
