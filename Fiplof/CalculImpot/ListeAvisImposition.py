# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ListeAvisImposition.ui'
#
# Created: Fri Jan 26 07:32:47 2018
#      by: PyQt4 UI code generator 4.11.3
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
        Dialog.resize(489, 551)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.checkBoxNom = QtGui.QCheckBox(self.groupBox)
        self.checkBoxNom.setObjectName(_fromUtf8("checkBoxNom"))
        self.gridLayout.addWidget(self.checkBoxNom, 0, 0, 1, 1)
        self.checkBoxAnnee = QtGui.QCheckBox(self.groupBox)
        self.checkBoxAnnee.setObjectName(_fromUtf8("checkBoxAnnee"))
        self.gridLayout.addWidget(self.checkBoxAnnee, 1, 2, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 10, 2, 1, 1)
        self.lineEditAnnee = QtGui.QLineEdit(self.groupBox)
        self.lineEditAnnee.setEnabled(False)
        self.lineEditAnnee.setMaxLength(4)
        self.lineEditAnnee.setObjectName(_fromUtf8("lineEditAnnee"))
        self.gridLayout.addWidget(self.lineEditAnnee, 1, 3, 1, 1)
        self.lineEdit_4 = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.gridLayout.addWidget(self.lineEdit_4, 10, 3, 1, 1)
        self.checkBoxCIN = QtGui.QCheckBox(self.groupBox)
        self.checkBoxCIN.setObjectName(_fromUtf8("checkBoxCIN"))
        self.gridLayout.addWidget(self.checkBoxCIN, 1, 0, 1, 1)
        self.lineEditCIN = QtGui.QLineEdit(self.groupBox)
        self.lineEditCIN.setEnabled(False)
        self.lineEditCIN.setObjectName(_fromUtf8("lineEditCIN"))
        self.gridLayout.addWidget(self.lineEditCIN, 1, 1, 1, 1)
        self.lineEdit_5 = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_5.setEnabled(False)
        self.lineEdit_5.setObjectName(_fromUtf8("lineEdit_5"))
        self.gridLayout.addWidget(self.lineEdit_5, 10, 1, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 10, 0, 1, 1)
        self.lineEditNom = QtGui.QLineEdit(self.groupBox)
        self.lineEditNom.setEnabled(False)
        self.lineEditNom.setObjectName(_fromUtf8("lineEditNom"))
        self.gridLayout.addWidget(self.lineEditNom, 0, 1, 1, 3)
        self.pushButtonRechercher = QtGui.QPushButton(self.groupBox)
        self.pushButtonRechercher.setObjectName(_fromUtf8("pushButtonRechercher"))
        self.gridLayout.addWidget(self.pushButtonRechercher, 8, 0, 1, 1)
        self.territoire = TerritoireWidget(self.groupBox)
        self.territoire.setObjectName(_fromUtf8("territoire"))
        self.gridLayout.addWidget(self.territoire, 3, 0, 1, 4)
        self.line_3 = QtGui.QFrame(self.groupBox)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.gridLayout.addWidget(self.line_3, 9, 0, 1, 4)
        self.verticalLayout.addWidget(self.groupBox)
        self.line = QtGui.QFrame(Dialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.tableWidget = QtGui.QTableWidget(Dialog)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.line_2 = QtGui.QFrame(Dialog)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonAvisImposition = QtGui.QPushButton(Dialog)
        self.pushButtonAvisImposition.setEnabled(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/std/icone/printer.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonAvisImposition.setIcon(icon)
        self.pushButtonAvisImposition.setObjectName(_fromUtf8("pushButtonAvisImposition"))
        self.horizontalLayout.addWidget(self.pushButtonAvisImposition)
        self.pushButtonVoir = QtGui.QPushButton(Dialog)
        self.pushButtonVoir.setObjectName(_fromUtf8("pushButtonVoir"))
        self.horizontalLayout.addWidget(self.pushButtonVoir)
        self.pushButtonFermer = QtGui.QPushButton(Dialog)
        self.pushButtonFermer.setObjectName(_fromUtf8("pushButtonFermer"))
        self.horizontalLayout.addWidget(self.pushButtonFermer)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Liste des Avis d\'Imposition", None))
        self.groupBox.setTitle(_translate("Dialog", "Recherche", None))
        self.checkBoxNom.setText(_translate("Dialog", "Nom", None))
        self.checkBoxAnnee.setText(_translate("Dialog", "Année", None))
        self.label_2.setText(_translate("Dialog", "Pages à Imprimer", None))
        self.checkBoxCIN.setText(_translate("Dialog", "CIN", None))
        self.lineEditCIN.setInputMask(_translate("Dialog", "000-000-000-000; ", None))
        self.label.setText(_translate("Dialog", "Nombre de Pages", None))
        self.pushButtonRechercher.setText(_translate("Dialog", "Rechercher", None))
        self.territoire.setToolTip(_translate("Dialog", "Combobox des territoires Plof", None))
        self.territoire.setWhatsThis(_translate("Dialog", "Combobox des territoires Plof", None))
        self.pushButtonAvisImposition.setText(_translate("Dialog", "Avis d\'Imposition", None))
        self.pushButtonVoir.setText(_translate("Dialog", "Voir", None))
        self.pushButtonFermer.setText(_translate("Dialog", "Fermer", None))

from Widgets.ui.territoirewidget import TerritoireWidget
import icons_rc
