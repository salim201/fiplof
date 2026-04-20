# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ImportFromParcelleCrisp.ui'
#
# Created: Wed Oct 11 21:19:50 2023
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
        Dialog.resize(643, 413)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/std/icone/database-import-icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.labelFilename = QtGui.QLabel(Dialog)
        self.labelFilename.setObjectName(_fromUtf8("labelFilename"))
        self.horizontalLayout_2.addWidget(self.labelFilename)
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.pushButtonParcourir = QtGui.QPushButton(Dialog)
        self.pushButtonParcourir.setMaximumSize(QtCore.QSize(28, 16777215))
        self.pushButtonParcourir.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/std/icone/if_folder_horizontal_open_11903.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonParcourir.setIcon(icon1)
        self.pushButtonParcourir.setObjectName(_fromUtf8("pushButtonParcourir"))
        self.horizontalLayout_2.addWidget(self.pushButtonParcourir)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.checkBoxModeCorrection = QtGui.QCheckBox(Dialog)
        self.checkBoxModeCorrection.setObjectName(_fromUtf8("checkBoxModeCorrection"))
        self.verticalLayout.addWidget(self.checkBoxModeCorrection)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.listWidgetSteps = QtGui.QListWidget(Dialog)
        self.listWidgetSteps.setMaximumSize(QtCore.QSize(240, 16777215))
        self.listWidgetSteps.setAlternatingRowColors(True)
        self.listWidgetSteps.setObjectName(_fromUtf8("listWidgetSteps"))
        self.horizontalLayout_3.addWidget(self.listWidgetSteps)
        self.listWidget = QtGui.QListWidget(Dialog)
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.horizontalLayout_3.addWidget(self.listWidget)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)
        self.line = QtGui.QFrame(Dialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonLancer = QtGui.QPushButton(Dialog)
        self.pushButtonLancer.setObjectName(_fromUtf8("pushButtonLancer"))
        self.horizontalLayout.addWidget(self.pushButtonLancer)
        self.pushButtonAnnuler = QtGui.QPushButton(Dialog)
        self.pushButtonAnnuler.setObjectName(_fromUtf8("pushButtonAnnuler"))
        self.horizontalLayout.addWidget(self.pushButtonAnnuler)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Importer Données", None))
        self.labelFilename.setText(_translate("Dialog", "Choisir fichier source:", None))
        self.checkBoxModeCorrection.setText(_translate("Dialog", "Mode correction", None))
        self.pushButtonLancer.setText(_translate("Dialog", "Lancer", None))
        self.pushButtonAnnuler.setText(_translate("Dialog", "Fermer", None))

import icons_rc
