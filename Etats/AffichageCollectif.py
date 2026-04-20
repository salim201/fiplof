# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AffichageCollectif.ui'
#
# Created: Mon Dec 18 23:44:40 2017
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
        Dialog.resize(435, 445)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.checkBoxNumeroDemande = QtGui.QCheckBox(Dialog)
        self.checkBoxNumeroDemande.setObjectName(_fromUtf8("checkBoxNumeroDemande"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.checkBoxNumeroDemande)
        self.lineEditNumeroDemande = QtGui.QLineEdit(Dialog)
        self.lineEditNumeroDemande.setEnabled(False)
        self.lineEditNumeroDemande.setObjectName(_fromUtf8("lineEditNumeroDemande"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEditNumeroDemande)
        self.checkBoxNomDemandeur = QtGui.QCheckBox(Dialog)
        self.checkBoxNomDemandeur.setObjectName(_fromUtf8("checkBoxNomDemandeur"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.checkBoxNomDemandeur)
        self.lineEditNomDemandeur = QtGui.QLineEdit(Dialog)
        self.lineEditNomDemandeur.setEnabled(False)
        self.lineEditNomDemandeur.setObjectName(_fromUtf8("lineEditNomDemandeur"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEditNomDemandeur)
        self.checkBoxDateDemande = QtGui.QCheckBox(Dialog)
        self.checkBoxDateDemande.setObjectName(_fromUtf8("checkBoxDateDemande"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.checkBoxDateDemande)
        self.dateEditDateDemande = QtGui.QDateEdit(Dialog)
        self.dateEditDateDemande.setEnabled(False)
        self.dateEditDateDemande.setCalendarPopup(True)
        self.dateEditDateDemande.setObjectName(_fromUtf8("dateEditDateDemande"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.dateEditDateDemande)
        self.checkBoxEtat = QtGui.QCheckBox(Dialog)
        self.checkBoxEtat.setObjectName(_fromUtf8("checkBoxEtat"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.checkBoxEtat)
        self.comboBoxEtat = QtGui.QComboBox(Dialog)
        self.comboBoxEtat.setEnabled(False)
        self.comboBoxEtat.setObjectName(_fromUtf8("comboBoxEtat"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.comboBoxEtat)
        self.territoire = TerritoireWidget(Dialog)
        self.territoire.setObjectName(_fromUtf8("territoire"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.SpanningRole, self.territoire)
        self.verticalLayout.addLayout(self.formLayout)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButtonAfficherTous = QtGui.QPushButton(self.groupBox)
        self.pushButtonAfficherTous.setObjectName(_fromUtf8("pushButtonAfficherTous"))
        self.horizontalLayout.addWidget(self.pushButtonAfficherTous)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonRechercher = QtGui.QPushButton(self.groupBox)
        self.pushButtonRechercher.setObjectName(_fromUtf8("pushButtonRechercher"))
        self.horizontalLayout.addWidget(self.pushButtonRechercher)
        self.verticalLayout.addWidget(self.groupBox)
        self.tableWidget = QtGui.QTableWidget(Dialog)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setTitle(_fromUtf8(""))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.checkBoxCocherTous = QtGui.QCheckBox(self.groupBox_2)
        self.checkBoxCocherTous.setObjectName(_fromUtf8("checkBoxCocherTous"))
        self.horizontalLayout_2.addWidget(self.checkBoxCocherTous)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButtonImprimer = QtGui.QPushButton(self.groupBox_2)
        self.pushButtonImprimer.setObjectName(_fromUtf8("pushButtonImprimer"))
        self.horizontalLayout_2.addWidget(self.pushButtonImprimer)
        self.pushButtonFermer = QtGui.QPushButton(self.groupBox_2)
        self.pushButtonFermer.setObjectName(_fromUtf8("pushButtonFermer"))
        self.horizontalLayout_2.addWidget(self.pushButtonFermer)
        self.verticalLayout.addWidget(self.groupBox_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.checkBoxNumeroDemande, self.lineEditNumeroDemande)
        Dialog.setTabOrder(self.lineEditNumeroDemande, self.checkBoxNomDemandeur)
        Dialog.setTabOrder(self.checkBoxNomDemandeur, self.lineEditNomDemandeur)
        Dialog.setTabOrder(self.lineEditNomDemandeur, self.checkBoxDateDemande)
        Dialog.setTabOrder(self.checkBoxDateDemande, self.dateEditDateDemande)
        Dialog.setTabOrder(self.dateEditDateDemande, self.checkBoxEtat)
        Dialog.setTabOrder(self.checkBoxEtat, self.comboBoxEtat)
        Dialog.setTabOrder(self.comboBoxEtat, self.pushButtonAfficherTous)
        Dialog.setTabOrder(self.pushButtonAfficherTous, self.pushButtonRechercher)
        Dialog.setTabOrder(self.pushButtonRechercher, self.checkBoxCocherTous)
        Dialog.setTabOrder(self.checkBoxCocherTous, self.pushButtonImprimer)
        Dialog.setTabOrder(self.pushButtonImprimer, self.pushButtonFermer)
        Dialog.setTabOrder(self.pushButtonFermer, self.tableWidget)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Affichage Collectif", None))
        self.checkBoxNumeroDemande.setText(_translate("Dialog", "Numero Demande", None))
        self.checkBoxNomDemandeur.setText(_translate("Dialog", "Nom Demandeur", None))
        self.checkBoxDateDemande.setText(_translate("Dialog", "Date Demande", None))
        self.checkBoxEtat.setText(_translate("Dialog", "Etat", None))
        self.territoire.setToolTip(_translate("Dialog", "Combobox des territoires Plof", None))
        self.territoire.setWhatsThis(_translate("Dialog", "Combobox des territoires Plof", None))
        self.pushButtonAfficherTous.setText(_translate("Dialog", "Afficher Tous ...", None))
        self.pushButtonRechercher.setText(_translate("Dialog", "Rechercher", None))
        self.checkBoxCocherTous.setText(_translate("Dialog", "Cocher Tous", None))
        self.pushButtonImprimer.setText(_translate("Dialog", "Imprimer", None))
        self.pushButtonFermer.setText(_translate("Dialog", "Fermer", None))

from Widgets.ui.territoirewidget import TerritoireWidget
