# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gestionUtilisateur.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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
        Dialog.resize(377, 441)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 341, 61))
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.choixUtilisateur = QtGui.QLabel(self.groupBox)
        self.choixUtilisateur.setGeometry(QtCore.QRect(30, 30, 101, 16))
        self.choixUtilisateur.setObjectName(_fromUtf8("choixUtilisateur"))
        self.comboChoixUtilisateur = QtGui.QComboBox(self.groupBox)
        self.comboChoixUtilisateur.setGeometry(QtCore.QRect(150, 30, 171, 22))
        self.comboChoixUtilisateur.setObjectName(_fromUtf8("comboChoixUtilisateur"))
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 70, 341, 311))
        self.groupBox_2.setTitle(_fromUtf8(""))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.nomUtilisateur = QtGui.QLabel(self.groupBox_2)
        self.nomUtilisateur.setGeometry(QtCore.QRect(50, 20, 46, 13))
        self.nomUtilisateur.setObjectName(_fromUtf8("nomUtilisateur"))
        self.lineEdit = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit.setGeometry(QtCore.QRect(130, 10, 191, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.prenm = QtGui.QLabel(self.groupBox_2)
        self.prenm.setGeometry(QtCore.QRect(50, 40, 46, 13))
        self.prenm.setObjectName(_fromUtf8("prenm"))
        self.lineEditPrenom = QtGui.QLineEdit(self.groupBox_2)
        self.lineEditPrenom.setGeometry(QtCore.QRect(130, 40, 191, 20))
        self.lineEditPrenom.setObjectName(_fromUtf8("lineEditPrenom"))
        self.login = QtGui.QLabel(self.groupBox_2)
        self.login.setGeometry(QtCore.QRect(50, 70, 61, 16))
        self.login.setObjectName(_fromUtf8("login"))
        self.lineEditLogin = QtGui.QLineEdit(self.groupBox_2)
        self.lineEditLogin.setGeometry(QtCore.QRect(130, 70, 191, 20))
        self.lineEditLogin.setObjectName(_fromUtf8("lineEditLogin"))
        self.motdepasse = QtGui.QLabel(self.groupBox_2)
        self.motdepasse.setGeometry(QtCore.QRect(50, 100, 81, 16))
        self.motdepasse.setObjectName(_fromUtf8("motdepasse"))
        self.lineEditMotPasse = QtGui.QLineEdit(self.groupBox_2)
        self.lineEditMotPasse.setGeometry(QtCore.QRect(130, 100, 191, 20))
        self.lineEditMotPasse.setObjectName(_fromUtf8("lineEditMotPasse"))
        self.confirmerMotPasse = QtGui.QLabel(self.groupBox_2)
        self.confirmerMotPasse.setGeometry(QtCore.QRect(10, 130, 121, 20))
        self.confirmerMotPasse.setObjectName(_fromUtf8("confirmerMotPasse"))
        self.lineEditConfirmMotPasse = QtGui.QLineEdit(self.groupBox_2)
        self.lineEditConfirmMotPasse.setGeometry(QtCore.QRect(130, 130, 191, 20))
        self.lineEditConfirmMotPasse.setObjectName(_fromUtf8("lineEditConfirmMotPasse"))
        self.telephone = QtGui.QLabel(self.groupBox_2)
        self.telephone.setGeometry(QtCore.QRect(45, 160, 61, 20))
        self.telephone.setObjectName(_fromUtf8("telephone"))
        self.lineEditTelephone = QtGui.QLineEdit(self.groupBox_2)
        self.lineEditTelephone.setGeometry(QtCore.QRect(130, 160, 191, 20))
        self.lineEditTelephone.setObjectName(_fromUtf8("lineEditTelephone"))
        self.Adresse = QtGui.QLabel(self.groupBox_2)
        self.Adresse.setGeometry(QtCore.QRect(50, 190, 46, 13))
        self.Adresse.setObjectName(_fromUtf8("Adresse"))
        self.textEditAdresse = QtGui.QTextEdit(self.groupBox_2)
        self.textEditAdresse.setGeometry(QtCore.QRect(130, 190, 191, 71))
        self.textEditAdresse.setObjectName(_fromUtf8("textEditAdresse"))
        self.fonction = QtGui.QLabel(self.groupBox_2)
        self.fonction.setGeometry(QtCore.QRect(50, 270, 46, 13))
        self.fonction.setObjectName(_fromUtf8("fonction"))
        self.lineEditFonction = QtGui.QLineEdit(self.groupBox_2)
        self.lineEditFonction.setGeometry(QtCore.QRect(130, 270, 191, 20))
        self.lineEditFonction.setObjectName(_fromUtf8("lineEditFonction"))
        self.groupBox_3 = QtGui.QGroupBox(self.groupBox_2)
        self.groupBox_3.setGeometry(QtCore.QRect(0, 310, 211, 51))
        self.groupBox_3.setTitle(_fromUtf8(""))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.Nouveau = QtGui.QPushButton(Dialog)
        self.Nouveau.setGeometry(QtCore.QRect(10, 400, 61, 23))
        self.Nouveau.setObjectName(_fromUtf8("Nouveau"))
        self.Modifier = QtGui.QPushButton(Dialog)
        self.Modifier.setGeometry(QtCore.QRect(80, 400, 61, 23))
        self.Modifier.setObjectName(_fromUtf8("Modifier"))
        self.Supprimer = QtGui.QPushButton(Dialog)
        self.Supprimer.setGeometry(QtCore.QRect(150, 400, 61, 23))
        self.Supprimer.setObjectName(_fromUtf8("Supprimer"))
        self.groupBox_4 = QtGui.QGroupBox(Dialog)
        self.groupBox_4.setGeometry(QtCore.QRect(220, 380, 131, 51))
        self.groupBox_4.setTitle(_fromUtf8(""))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.Annuler = QtGui.QPushButton(self.groupBox_4)
        self.Annuler.setGeometry(QtCore.QRect(10, 20, 51, 23))
        self.Annuler.setObjectName(_fromUtf8("Annuler"))
        self.Fermer = QtGui.QPushButton(self.groupBox_4)
        self.Fermer.setGeometry(QtCore.QRect(70, 20, 51, 23))
        self.Fermer.setObjectName(_fromUtf8("Fermer"))
        
        self.Nouveau.clicked.connect(self.NouveaUser) 
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    
    def NouveaUser(self):
        from NouveauUserRunn import NouveauUserRunn
        np = NouveauUserRunn()
        result = np.exec_()

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.choixUtilisateur.setText(_translate("Dialog", "Choisir Utilisateur :", None))
        self.nomUtilisateur.setText(_translate("Dialog", "Nom : ", None))
        self.prenm.setText(_translate("Dialog", "Prenom :", None))
        self.login.setText(_translate("Dialog", "Identifiant :", None))
        self.motdepasse.setText(_translate("Dialog", "Mot de passe :", None))
        self.confirmerMotPasse.setText(_translate("Dialog", "Confirmer mot de passe :", None))
        self.telephone.setText(_translate("Dialog", "Telephone :", None))
        self.Adresse.setText(_translate("Dialog", "Adresse :", None))
        self.fonction.setText(_translate("Dialog", "Fonction :", None))
        self.Nouveau.setText(_translate("Dialog", "Nouveau", None))
        self.Modifier.setText(_translate("Dialog", "Modifier", None))
        self.Supprimer.setText(_translate("Dialog", "Supprimer", None))
        self.Annuler.setText(_translate("Dialog", "Annuler", None))
        self.Fermer.setText(_translate("Dialog", "Fermer", None))

