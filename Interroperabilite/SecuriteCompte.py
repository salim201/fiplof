# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SecuriteCompte.ui'
#
# Created: Thu Jun 11 00:04:34 2026
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

class Ui_SecuriteCompte(object):
    def setupUi(self, SecuriteCompte):
        SecuriteCompte.setObjectName(_fromUtf8("SecuriteCompte"))
        SecuriteCompte.resize(1100, 700)
        SecuriteCompte.setStyleSheet(_fromUtf8("QWidget {\n"
"    background-color: #f5f5f5;\n"
"    font-family: \"Segoe UI\", Arial, sans-serif;\n"
"    font-size: 10pt;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #2c3e50;\n"
"    color: white;\n"
"    padding: 8px;\n"
"    border: none;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QTableWidget {\n"
"    background-color: white;\n"
"    alternate-background-color: #f8f9fa;\n"
"    gridline-color: #dfe6e9;\n"
"    border: 1px solid #bdc3c7;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QTableWidget::item {\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QTableWidget::item:selected {\n"
"    background-color: #3498db;\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: #3498db;\n"
"    color: white;\n"
"    border: none;\n"
"    padding: 8px 16px;\n"
"    border-radius: 4px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #2980b9;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #1f618d;\n"
"}\n"
"\n"
"QPushButton#btn_Desactiver {\n"
"    background-color: #e74c3c;\n"
"}\n"
"\n"
"QPushButton#btn_Desactiver:hover {\n"
"    background-color: #c0392b;\n"
"}\n"
"\n"
"QPushButton#btn_Activer {\n"
"    background-color: #27ae60;\n"
"}\n"
"\n"
"QPushButton#btn_Activer:hover {\n"
"    background-color: #1e8449;\n"
"}\n"
"\n"
"QLineEdit {\n"
"    padding: 8px;\n"
"    border: 1px solid #bdc3c7;\n"
"    border-radius: 4px;\n"
"    background-color: white;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 2px solid #3498db;\n"
"}\n"
"\n"
"QGroupBox {\n"
"    border: 1px solid #bdc3c7;\n"
"    border-radius: 8px;\n"
"    margin-top: 10px;\n"
"    font-weight: bold;\n"
"    background-color: white;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 10px;\n"
"    padding: 0 5px;\n"
"}\n"
"\n"
"QComboBox {\n"
"    padding: 8px;\n"
"    border: 1px solid #bdc3c7;\n"
"    border-radius: 4px;\n"
"    background-color: white;\n"
"}"))
        self.label_titre = QtGui.QLabel(SecuriteCompte)
        self.label_titre.setGeometry(QtCore.QRect(20, 10, 500, 40))
        self.label_titre.setStyleSheet(_fromUtf8("QLabel {\n"
"    font-size: 18pt;\n"
"    font-weight: bold;\n"
"    color: #2c3e50;\n"
"}"))
        self.label_titre.setObjectName(_fromUtf8("label_titre"))
        self.lineEdit_recherche = QtGui.QLineEdit(SecuriteCompte)
        self.lineEdit_recherche.setGeometry(QtCore.QRect(20, 60, 300, 30))
        self.lineEdit_recherche.setObjectName(_fromUtf8("lineEdit_recherche"))
        self.btn_rechercher = QtGui.QPushButton(SecuriteCompte)
        self.btn_rechercher.setGeometry(QtCore.QRect(330, 60, 100, 30))
        self.btn_rechercher.setObjectName(_fromUtf8("btn_rechercher"))
        self.btn_actualiser = QtGui.QPushButton(SecuriteCompte)
        self.btn_actualiser.setGeometry(QtCore.QRect(440, 60, 100, 30))
        self.btn_actualiser.setStyleSheet(_fromUtf8("QPushButton {\n"
"    background-color: #95a5a6;\n"
"}"))
        self.btn_actualiser.setObjectName(_fromUtf8("btn_actualiser"))
        self.tableWidget_comptes = QtGui.QTableWidget(SecuriteCompte)
        self.tableWidget_comptes.setGeometry(QtCore.QRect(20, 100, 1060, 350))
        self.tableWidget_comptes.setObjectName(_fromUtf8("tableWidget_comptes"))
        self.tableWidget_comptes.setColumnCount(8)
        self.tableWidget_comptes.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_comptes.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_comptes.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_comptes.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_comptes.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_comptes.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_comptes.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_comptes.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_comptes.setHorizontalHeaderItem(7, item)
        self.groupBox_modification = QtGui.QGroupBox(SecuriteCompte)
        self.groupBox_modification.setGeometry(QtCore.QRect(20, 470, 1060, 180))
        self.groupBox_modification.setObjectName(_fromUtf8("groupBox_modification"))
        self.label_id = QtGui.QLabel(self.groupBox_modification)
        self.label_id.setGeometry(QtCore.QRect(20, 30, 80, 25))
        self.label_id.setObjectName(_fromUtf8("label_id"))
        self.label_id_valeur = QtGui.QLabel(self.groupBox_modification)
        self.label_id_valeur.setGeometry(QtCore.QRect(110, 30, 100, 25))
        self.label_id_valeur.setStyleSheet(_fromUtf8("QLabel {\n"
"    font-weight: bold;\n"
"    color: #e74c3c;\n"
"}"))
        self.label_id_valeur.setObjectName(_fromUtf8("label_id_valeur"))
        self.label_login = QtGui.QLabel(self.groupBox_modification)
        self.label_login.setGeometry(QtCore.QRect(20, 65, 80, 25))
        self.label_login.setObjectName(_fromUtf8("label_login"))
        self.label_login_valeur = QtGui.QLabel(self.groupBox_modification)
        self.label_login_valeur.setGeometry(QtCore.QRect(110, 65, 200, 25))
        self.label_login_valeur.setStyleSheet(_fromUtf8("QLabel {\n"
"    font-weight: bold;\n"
"    color: #2c3e50;\n"
"}"))
        self.label_login_valeur.setObjectName(_fromUtf8("label_login_valeur"))
        self.label_statut = QtGui.QLabel(self.groupBox_modification)
        self.label_statut.setGeometry(QtCore.QRect(350, 30, 100, 25))
        self.label_statut.setObjectName(_fromUtf8("label_statut"))
        self.comboBox_statut = QtGui.QComboBox(self.groupBox_modification)
        self.comboBox_statut.setGeometry(QtCore.QRect(460, 30, 150, 25))
        self.comboBox_statut.setObjectName(_fromUtf8("comboBox_statut"))
        self.comboBox_statut.addItem(_fromUtf8(""))
        self.comboBox_statut.addItem(_fromUtf8(""))
        self.comboBox_statut.addItem(_fromUtf8(""))
        self.label_actif = QtGui.QLabel(self.groupBox_modification)
        self.label_actif.setGeometry(QtCore.QRect(350, 70, 100, 25))
        self.label_actif.setObjectName(_fromUtf8("label_actif"))
        self.checkBox_actif = QtGui.QCheckBox(self.groupBox_modification)
        self.checkBox_actif.setGeometry(QtCore.QRect(460, 70, 100, 25))
        self.checkBox_actif.setObjectName(_fromUtf8("checkBox_actif"))
        self.btn_enregistrer = QtGui.QPushButton(self.groupBox_modification)
        self.btn_enregistrer.setGeometry(QtCore.QRect(650, 30, 150, 35))
        self.btn_enregistrer.setStyleSheet(_fromUtf8("QPushButton {\n"
"    background-color: #27ae60;\n"
"}"))
        self.btn_enregistrer.setObjectName(_fromUtf8("btn_enregistrer"))
        self.btn_Activer = QtGui.QPushButton(self.groupBox_modification)
        self.btn_Activer.setGeometry(QtCore.QRect(650, 75, 70, 35))
        self.btn_Activer.setObjectName(_fromUtf8("btn_Activer"))
        self.btn_Desactiver = QtGui.QPushButton(self.groupBox_modification)
        self.btn_Desactiver.setGeometry(QtCore.QRect(730, 75, 70, 35))
        self.btn_Desactiver.setObjectName(_fromUtf8("btn_Desactiver"))
        self.btn_ValiderStatut = QtGui.QPushButton(self.groupBox_modification)
        self.btn_ValiderStatut.setGeometry(QtCore.QRect(820, 30, 120, 35))
        self.btn_ValiderStatut.setObjectName(_fromUtf8("btn_ValiderStatut"))
        self.btn_RejeterStatut = QtGui.QPushButton(self.groupBox_modification)
        self.btn_RejeterStatut.setGeometry(QtCore.QRect(950, 30, 100, 35))
        self.btn_RejeterStatut.setStyleSheet(_fromUtf8("QPushButton {\n"
"    background-color: #e74c3c;\n"
"}"))
        self.btn_RejeterStatut.setObjectName(_fromUtf8("btn_RejeterStatut"))
        self.btn_Reinitialiser = QtGui.QPushButton(self.groupBox_modification)
        self.btn_Reinitialiser.setGeometry(QtCore.QRect(820, 75, 100, 35))
        self.btn_Reinitialiser.setStyleSheet(_fromUtf8("QPushButton {\n"
"    background-color: #95a5a6;\n"
"}"))
        self.btn_Reinitialiser.setObjectName(_fromUtf8("btn_Reinitialiser"))
        self.label_message = QtGui.QLabel(SecuriteCompte)
        self.label_message.setGeometry(QtCore.QRect(20, 660, 1060, 30))
        self.label_message.setStyleSheet(_fromUtf8("QLabel {\n"
"    color: #7f8c8d;\n"
"    font-style: italic;\n"
"}"))
        self.label_message.setAlignment(QtCore.Qt.AlignCenter)
        self.label_message.setObjectName(_fromUtf8("label_message"))

        self.retranslateUi(SecuriteCompte)
        QtCore.QObject.connect(self.btn_rechercher, QtCore.SIGNAL(_fromUtf8("clicked()")), SecuriteCompte.on_btn_rechercher_clicked)
        QtCore.QObject.connect(self.btn_actualiser, QtCore.SIGNAL(_fromUtf8("clicked()")), SecuriteCompte.on_btn_actualiser_clicked)
        QtCore.QObject.connect(self.tableWidget_comptes, QtCore.SIGNAL(_fromUtf8("itemSelectionChanged()")), SecuriteCompte.on_tableWidget_comptes_itemSelectionChanged)
        QtCore.QObject.connect(self.btn_enregistrer, QtCore.SIGNAL(_fromUtf8("clicked()")), SecuriteCompte.on_btn_enregistrer_clicked)
        QtCore.QObject.connect(self.btn_Activer, QtCore.SIGNAL(_fromUtf8("clicked()")), SecuriteCompte.on_btn_Activer_clicked)
        QtCore.QObject.connect(self.btn_Desactiver, QtCore.SIGNAL(_fromUtf8("clicked()")), SecuriteCompte.on_btn_Desactiver_clicked)
        QtCore.QObject.connect(self.btn_ValiderStatut, QtCore.SIGNAL(_fromUtf8("clicked()")), SecuriteCompte.on_btn_ValiderStatut_clicked)
        QtCore.QObject.connect(self.btn_RejeterStatut, QtCore.SIGNAL(_fromUtf8("clicked()")), SecuriteCompte.on_btn_RejeterStatut_clicked)
        QtCore.QObject.connect(self.btn_Reinitialiser, QtCore.SIGNAL(_fromUtf8("clicked()")), SecuriteCompte.on_btn_Reinitialiser_clicked)
        QtCore.QObject.connect(self.lineEdit_recherche, QtCore.SIGNAL(_fromUtf8("returnPressed()")), SecuriteCompte.on_btn_rechercher_clicked)
        QtCore.QMetaObject.connectSlotsByName(SecuriteCompte)

    def retranslateUi(self, SecuriteCompte):
        SecuriteCompte.setWindowTitle(_translate("SecuriteCompte", "Gestion des Comptes API - Sécurité", None))
        self.label_titre.setText(_translate("SecuriteCompte", "Gestion des Comptes API", None))
        self.lineEdit_recherche.setPlaceholderText(_translate("SecuriteCompte", "Rechercher par login ou nom...", None))
        self.btn_rechercher.setText(_translate("SecuriteCompte", "Rechercher", None))
        self.btn_actualiser.setText(_translate("SecuriteCompte", "Actualiser", None))
        item = self.tableWidget_comptes.horizontalHeaderItem(0)
        item.setText(_translate("SecuriteCompte", "ID", None))
        item = self.tableWidget_comptes.horizontalHeaderItem(1)
        item.setText(_translate("SecuriteCompte", "Login", None))
        item = self.tableWidget_comptes.horizontalHeaderItem(2)
        item.setText(_translate("SecuriteCompte", "Nom", None))
        item = self.tableWidget_comptes.horizontalHeaderItem(3)
        item.setText(_translate("SecuriteCompte", "Nom Système", None))
        item = self.tableWidget_comptes.horizontalHeaderItem(4)
        item.setText(_translate("SecuriteCompte", "Actif", None))
        item = self.tableWidget_comptes.horizontalHeaderItem(5)
        item.setText(_translate("SecuriteCompte", "Statut", None))
        item = self.tableWidget_comptes.horizontalHeaderItem(6)
        item.setText(_translate("SecuriteCompte", "Dernière Connexion", None))
        item = self.tableWidget_comptes.horizontalHeaderItem(7)
        item.setText(_translate("SecuriteCompte", "Créé le", None))
        self.groupBox_modification.setTitle(_translate("SecuriteCompte", "Modification du Compte Sélectionné", None))
        self.label_id.setText(_translate("SecuriteCompte", "ID :", None))
        self.label_id_valeur.setText(_translate("SecuriteCompte", "-", None))
        self.label_login_valeur.setText(_translate("SecuriteCompte", "-", None))
        self.label_statut.setText(_translate("SecuriteCompte", "Statut :", None))
        self.comboBox_statut.setItemText(0, _translate("SecuriteCompte", "PENDING", None))
        self.comboBox_statut.setItemText(1, _translate("SecuriteCompte", "VALIDATED", None))
        self.comboBox_statut.setItemText(2, _translate("SecuriteCompte", "REJECTED", None))
        self.label_actif.setText(_translate("SecuriteCompte", "Actif :", None))
        self.checkBox_actif.setText(_translate("SecuriteCompte", "Actif", None))
        self.btn_enregistrer.setText(_translate("SecuriteCompte", "Enregistrer", None))
        self.btn_Activer.setText(_translate("SecuriteCompte", "Activer", None))
        self.btn_Desactiver.setText(_translate("SecuriteCompte", " Désactiver", None))
        self.btn_ValiderStatut.setText(_translate("SecuriteCompte", "Valider", None))
        self.btn_RejeterStatut.setText(_translate("SecuriteCompte", "Rejeter", None))
        self.btn_Reinitialiser.setText(_translate("SecuriteCompte", "Réinitialiser", None))
        self.label_message.setText(_translate("SecuriteCompte", "Sélectionnez un compte dans la table pour le modifier", None))

