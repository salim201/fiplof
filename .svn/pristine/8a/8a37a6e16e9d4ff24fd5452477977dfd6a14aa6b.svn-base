# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FormExport_u.ui'
#
# Created: Thu Apr 20 04:43:15 2023
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

class Ui_Export(object):
    def setupUi(self, Export):
        Export.setObjectName(_fromUtf8("Export"))
        Export.resize(569, 394)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/std/icone/database-export-icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Export.setWindowIcon(icon)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Export)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalGroupBox_2 = QtGui.QGroupBox(Export)
        self.horizontalGroupBox_2.setObjectName(_fromUtf8("horizontalGroupBox_2"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalGroupBox_2)
        self.horizontalLayout.setContentsMargins(15, 6, 6, 6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.horizontalGroupBox_2)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.filename = QtGui.QLineEdit(self.horizontalGroupBox_2)
        self.filename.setObjectName(_fromUtf8("filename"))
        self.horizontalLayout.addWidget(self.filename)
        self.find = QtGui.QPushButton(self.horizontalGroupBox_2)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/std/icone/if_folder_horizontal_open_11903.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.find.setIcon(icon1)
        self.find.setObjectName(_fromUtf8("find"))
        self.horizontalLayout.addWidget(self.find)
        self.verticalLayout_2.addWidget(self.horizontalGroupBox_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.labelNomBase = QtGui.QLabel(Export)
        self.labelNomBase.setObjectName(_fromUtf8("labelNomBase"))
        self.horizontalLayout_3.addWidget(self.labelNomBase)
        self.lineEditNomBase = QtGui.QLineEdit(Export)
        self.lineEditNomBase.setObjectName(_fromUtf8("lineEditNomBase"))
        self.horizontalLayout_3.addWidget(self.lineEditNomBase)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.checkBoxConnectDB = QtGui.QCheckBox(Export)
        self.checkBoxConnectDB.setChecked(True)
        self.checkBoxConnectDB.setObjectName(_fromUtf8("checkBoxConnectDB"))
        self.horizontalLayout_4.addWidget(self.checkBoxConnectDB)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.listWidget = QtGui.QListWidget(Export)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.verticalLayout.addWidget(self.listWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.progressBar = QtGui.QProgressBar(Export)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout_2.addWidget(self.progressBar)
        self.horizontalGroupBox = QtGui.QGroupBox(Export)
        self.horizontalGroupBox.setObjectName(_fromUtf8("horizontalGroupBox"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalGroupBox)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.launch = QtGui.QPushButton(self.horizontalGroupBox)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/std/icone/cog_go.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.launch.setIcon(icon2)
        self.launch.setObjectName(_fromUtf8("launch"))
        self.horizontalLayout_2.addWidget(self.launch)
        self.cancel = QtGui.QPushButton(self.horizontalGroupBox)
        self.cancel.setEnabled(False)
        self.cancel.setObjectName(_fromUtf8("cancel"))
        self.horizontalLayout_2.addWidget(self.cancel)
        self.verticalLayout_2.addWidget(self.horizontalGroupBox)

        self.retranslateUi(Export)
        QtCore.QMetaObject.connectSlotsByName(Export)

    def retranslateUi(self, Export):
        Export.setWindowTitle(_translate("Export", "Export des donnees PLOF", None))
        self.label.setText(_translate("Export", "Nom du fichier :", None))
        self.find.setText(_translate("Export", "Parcourir", None))
        self.labelNomBase.setText(_translate("Export", "Nom de la base à restaurer:", None))
        self.checkBoxConnectDB.setText(_translate("Export", "Se connecter à la base restaurée au prochain demarrage de FIPLOF", None))
        self.launch.setText(_translate("Export", "Lancer l\'export", None))
        self.cancel.setText(_translate("Export", "Fermer", None))

import icons_rc
