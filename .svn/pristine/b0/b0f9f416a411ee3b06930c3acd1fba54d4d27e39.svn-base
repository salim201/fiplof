# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FormImportDxf.ui'
#
# Created: Mon Mar 11 16:12:08 2024
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
        Dialog.resize(450, 126)
        Dialog.setMinimumSize(QtCore.QSize(450, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../icone/dxf.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.labelCouche = QtGui.QLabel(Dialog)
        self.labelCouche.setObjectName(_fromUtf8("labelCouche"))
        self.gridLayout.addWidget(self.labelCouche, 0, 0, 1, 1)
        self.comboBoxCouche = QtGui.QComboBox(Dialog)
        self.comboBoxCouche.setObjectName(_fromUtf8("comboBoxCouche"))
        self.comboBoxCouche.addItem(_fromUtf8(""))
        self.comboBoxCouche.addItem(_fromUtf8(""))
        self.comboBoxCouche.addItem(_fromUtf8(""))
        self.comboBoxCouche.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBoxCouche, 0, 1, 1, 1)
        self.lineEditPath = QtGui.QLineEdit(Dialog)
        self.lineEditPath.setObjectName(_fromUtf8("lineEditPath"))
        self.gridLayout.addWidget(self.lineEditPath, 1, 1, 1, 1)
        self.labelFichier = QtGui.QLabel(Dialog)
        self.labelFichier.setObjectName(_fromUtf8("labelFichier"))
        self.gridLayout.addWidget(self.labelFichier, 1, 0, 1, 1)
        self.toolButtonParcourir = QtGui.QToolButton(Dialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/std/icone/if_folder_horizontal_open_11903.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButtonParcourir.setIcon(icon1)
        self.toolButtonParcourir.setObjectName(_fromUtf8("toolButtonParcourir"))
        self.gridLayout.addWidget(self.toolButtonParcourir, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonImporter = QtGui.QPushButton(Dialog)
        self.pushButtonImporter.setObjectName(_fromUtf8("pushButtonImporter"))
        self.horizontalLayout.addWidget(self.pushButtonImporter)
        self.pushButtonFermer = QtGui.QPushButton(Dialog)
        self.pushButtonFermer.setObjectName(_fromUtf8("pushButtonFermer"))
        self.horizontalLayout.addWidget(self.pushButtonFermer)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.labelCouche.setText(_translate("Dialog", "Couche:", None))
        self.comboBoxCouche.setItemText(0, _translate("Dialog", "Titre", None))
        self.comboBoxCouche.setItemText(1, _translate("Dialog", "Cadastre", None))
        self.comboBoxCouche.setItemText(2, _translate("Dialog", "Demande FN", None))
        self.comboBoxCouche.setItemText(3, _translate("Dialog", "Terrain à statut spécifique", None))
        self.labelFichier.setText(_translate("Dialog", "Fichier", None))
        self.toolButtonParcourir.setText(_translate("Dialog", "...", None))
        self.pushButtonImporter.setText(_translate("Dialog", "Importer", None))
        self.pushButtonFermer.setText(_translate("Dialog", "Fermer", None))

import icons_rc
