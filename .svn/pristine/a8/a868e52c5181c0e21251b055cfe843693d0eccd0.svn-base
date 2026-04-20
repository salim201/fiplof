#coding: utf-8
import os
import sys
import os
import os.path
import psycopg2
import qgis
# from qgis.utils import iface
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
from qgis.gui import *
import time
import datetime
import globalvars
from PyQt4 import QtGui, Qt
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, Qt
from PyQt4 import QtCore, QtGui
from PyQt4 import QtGui, Qt
from PyQt4 import Qt, QtGui
import psycopg2
from psycopg2 import extras
from Utils import Utils
from PyQt4.QtCore import *
import globalvars

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

from Demandeurs import Ui_Demandeur

class DemandeursUpdateFormRun(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.

        self.parent = parent
        self.demandeurs = self.parent.demandeurs
        self.ui = Ui_Demandeur()
        self.ui.setupUi(self)
        self.CreationDemande = ""
        self.coddistrict = 0
        self.codecommune = 0
        self.idfokontany = 0
        self.iddemande = 0
        self.idopposition = 0
        self.connection = ""
        self.ddDate = 0
        self.idDemandeurs = self.parent.idDemandeurS
        self.connection = self.parent.connection
        self.tabWigdets = self.parent.tabWigdets
        self.tbDemande = self.parent.tbDemande

        self.cursor = self.connection.cursor()
        self.setModal(True)
        #self.id_projet = self.parent.id_projet
        #self.ui.btnadd.clicked.connect(self.addDemandeurs())
        self.ui.btnadd.clicked.connect(self.addDemandeurs)

        self.ui.lineEditDateNaiss.setEnabled(True)
        self.ui.lineEditDateNaiss.setCalendarPopup(True)
        self.ui.lineEditDateNaiss.setDisplayFormat("dd/MM/yyyy")
        self.ui.lineEditDateNaiss.setDate(QDate.currentDate())

        self.ui.lineEditDateCIN.setEnabled(True)
        self.ui.lineEditDateCIN.setCalendarPopup(True)
        self.ui.lineEditDateCIN.setDisplayFormat("dd/MM/yyyy")
        self.ui.lineEditDateCIN.setDate(QDate.currentDate())

        self.isValid = True
        self.isValid = True
        self.missedFields = []
        self.initActions()
        self.initMasks()
        self.ui.radioBtnCIN.setChecked(True)
        self.ui.radioBtnCelib.setChecked(True)
        self.ui.btnadd.setText("Modifier")
        self.fetchDemandeur()
        #self.ui.uploadPhotos.clicked.connect(self.updloaFiles)

    def fetchDemandeur(self):

        import time
        import datetime, globalvars
        import datetime
        from datetime import date
        cursor = self.connection.cursor()
        cursor = self.connection.cursor()
        cursor.execute("SELECT *   FROM demandeur_d  WHERE iddemandeur=%s", [int(self.idDemandeurs)])
        res = cursor.fetchone()

        if len(res) >= 1 :
            print "fdfsdfs"
            self.ui.nomLineEdit.setText(str(res[1]))
            self.ui.prenomLineEdit.setText(str(res[2]))
            if res[3] != None :
                dateNaissance = res[3].isoformat()
                year, month, day = res[9].isoformat().split("-")
                dateNaissance = date(int(year), int(month), int(day))
                #self.ui.dateDemandeDateEdit.setDate(dateDemande)
                self.ui.lineEditDateNaiss.setDate(dateNaissance)

            if (str(res[5]) == 'masculin') :
                self.ui.radioBtnMale.setChecked(True)
            else :
                self.ui.radioBtnFemale.setChecked(True)
            self.ui.nomDuPReLineEdit.setText(str(res[14]))
            self.ui.nomDeLaMReLineEdit.setText(str(res[15]))

            if res[8] != None :
                self.ui.lineEditCIN_1.setText(res[8][0:3])
                self.ui.lineEditCIN_2.setText(res[8][3:6])
                self.ui.lineEditCIN_3.setText(res[8][6:9])
                self.ui.lineEditCIN_4.setText(res[8][9:len(res[8])])

            if res[9] != None :
                dateNCIN = res[9].isoformat()
                year, month, day = res[9].isoformat().split("-")
                dateNCIN = date(int(year), int(month), int(day))
                self.ui.lineEditDateCIN.setDate(dateNCIN)
            #self.ui.lineEditDateCIN.setDate(dateNCIN)
            self.ui.lineEditLeuCIN.setText(str(res[10]))





    def initMasks(self):
        validatorAlpha = QRegExpValidator(globalvars.regexpAlpha)
        validatorAlphaNum = QRegExpValidator(globalvars.regexpAlphaNum)
        validatorNum = QRegExpValidator(globalvars.regexpNum)

        self.ui.nomLineEdit.setValidator(validatorAlpha)
        self.ui.prenomLineEdit.setValidator(validatorAlpha)
        self.ui.lineEditAdresse.setValidator(validatorAlphaNum)
        self.ui.nomDuPReLineEdit.setValidator(validatorAlpha)
        self.ui.nomDeLaMReLineEdit.setValidator(validatorAlpha)
        self.ui.lineEditCIN_1.setValidator(validatorNum)
        self.ui.lineEditCIN_2.setValidator(validatorNum)
        self.ui.lineEditCIN_3.setValidator(validatorNum)
        self.ui.lineEditCIN_4.setValidator(validatorNum)
        self.ui.lineEditLeuCIN.setValidator(validatorAlphaNum)
        self.ui.lineEditNumActeNaiss.setValidator(validatorNum)
        self.ui.lineEditLieuActeNaiss.setValidator(validatorAlphaNum)
        # self.ui.lineEditCIN.setMaxLength(3)
        self.ui.lineEditCIN_1.setMaxLength(3)
        self.ui.lineEditCIN_2.setMaxLength(3)
        self.ui.lineEditCIN_3.setMaxLength(3)
        self.ui.lineEditCIN_4.setMaxLength(3)

    def initActions(self):
        self.ui.radioBtnCIN.clicked.connect(self.showCin)
        self.ui.radioBtnActeDeNaiss.clicked.connect(self.showActeNaiss)
        #self.btnOk.clicked.connect(self.readInput)
        self.ui.radioBtnCelib.clicked.connect(self.changeMatrimoniale)
        self.ui.radioBtnMarie.clicked.connect(self.changeMatrimoniale)
        self.ui.radioBtnVeuf.clicked.connect(self.changeMatrimoniale)
        self.ui.btncancel.clicked.connect(self.close)
        self.ui.lineEditCIN_1.textEdited.connect(self.nextFields)
        self.ui.lineEditCIN_2.textEdited.connect(self.nextFields)
        self.ui.lineEditCIN_3.textEdited.connect(self.nextFields)
        #self.ui.neVersCheckBox.stateChanged.connect(self.updateDateField)

    def showCin(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    def showActeNaiss(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def changeMatrimoniale(self):
        if self.ui.radioBtnCelib.isChecked():
            if self.ui.btnEtatConjoint.isEnabled():
                self.ui.btnEtatConjoint.setEnabled(False)
        elif self.ui.radioBtnMarie.isChecked():
            if not self.ui.btnEtatConjoint.isEnabled():
                self.ui.btnEtatConjoint.setEnabled(True)
        elif self.ui.radioBtnVeuf.isChecked():
            if not self.ui.btnEtatConjoint.isEnabled():
                self.ui.btnEtatConjoint.setEnabled(True)
    def nextFields(self):
        senderName = self.sender().objectName()
        if senderName == "lineEditCIN_1" and self.sender().text().length() == 3:
            self.ui.lineEditCIN_2.setFocus()
        if senderName == "lineEditCIN_2" and self.sender().text().length() == 3:
            self.ui.lineEditCIN_3.setFocus()
        if senderName == "lineEditCIN_3" and self.sender().text().length() == 3:
            self.ui.lineEditCIN_4.setFocus()

    def messageErreur(self, message):
        self.isValid = True
        msgBox = QtGui.QMessageBox()
        msgBox.setText(message)
        msgBox.setModal(True)
        msgBox.show()
        msgBox.exec_()
    def readInput(self):
        print "test"

        self.missedFields[:] = []
        data = {}

        if self.ui.nomLineEdit.text() == '':
            QMessageBox.critical(self.ui.nomLineEdit, "Erreur", "Veuillez remplir le champ Nom")
            self.isValid = False
            return
        else:
            self.isValid = True

        if self.ui.prenomLineEdit.text() == '':
            QMessageBox.critical(self.ui.prenomLineEdit, "Erreur", "Veuillez remplir le champ Prenom")
            self.isValid = False
            return
        else :
            self.isValid = True

        if self.ui.lineEditAdresse.text() == '':
            self.isValid = False
            QMessageBox.critical(self.ui.lineEditAdresse, "Erreur", "Veuillez remplir le champ Adresse")
            return
        else :
            self.isValid = True

        if self.ui.nomDuPReLineEdit.text() == '':
            self.isValid = False
            QMessageBox.critical(self.ui.nomDuPReLineEdit, "Erreur", "Veuillez remplir le champ Pere")
            return
        else :
            self.isValid = True

        if self.ui.nomDeLaMReLineEdit.text() == '':
            self.isValid = False
            QMessageBox.critical(self.ui.nomDeLaMReLineEdit, "Erreur", "Veuillez remplir le champ Mere")
            return
        else :
            self.isValid = True

        if self.ui.lineEditCIN_1.text() == '':
            self.isValid = False
            QMessageBox.critical(self.ui.lineEditCIN_1, "Erreur", "Veuillez remplir le 1er champ CIN")
            return
        else :
            self.isValid = True

        if self.ui.lineEditCIN_2.text() == '':
            self.isValid = False
            QMessageBox.critical(self.ui.lineEditCIN_2, "Erreur", "Veuillez remplir le 2nd champ CIN")
            return
        else :
            self.isValid = True

        if self.ui.lineEditCIN_3.text() == '':
            self.isValid = False
            QMessageBox.critical(self.ui.lineEditCIN_3, "Erreur", "Veuillez remplir la 3eim champ CIN")
            return
        else :
            self.isValid = True


        if self.ui.lineEditCIN_4.text() == '':
            self.isValid = False
            QMessageBox.critical(self.ui.lineEditCIN_4, "Erreur", "Veuillez remplir la 4iem champ CIN")
            return
        else :
            self.isValid = True

        data['nom'] = unicode(self.ui.nomLineEdit.text()).encode('utf-8')
        data['prenom'] = unicode(self.ui.prenomLineEdit.text()).encode('utf-8')
        data['datenaissance'] = datetime.date(self.ui.lineEditDateNaiss.date().year(), self.ui.lineEditDateNaiss.date().month(), self.ui.lineEditDateNaiss.date().day())
        if self.ui.radioBtnMale.isChecked():
            data['sexe'] = "masculin"
        elif self.ui.radioBtnFemale.isChecked():
            data['sexe'] = "feminin"

        data['adresse'] = unicode(self.ui.lineEditAdresse.text()).encode('utf-8')
        data['pere'] = unicode(self.ui.nomDuPReLineEdit.text()).encode('utf-8')
        data['mere'] = unicode(self.ui.nomDeLaMReLineEdit.text()).encode('utf-8')

        if self.ui.radioBtnCelib.isChecked():
            data['matrimoniale'] = 1
        elif self.ui.radioBtnMarie.isChecked():
            data['matrimoniale'] = 2
        elif self.ui.radioBtnVeuf.isChecked():
            data['matrimoniale'] = 3


        if self.ui.radioBtnCIN.isChecked():
            data['cin'] = unicode(self.ui.lineEditCIN_1.text()).encode('utf-8') + unicode(self.ui.lineEditCIN_2.text()).encode('utf-8') + unicode(self.ui.lineEditCIN_3.text()).encode('utf-8') + unicode(self.ui.lineEditCIN_4.text()).encode('utf-8')
            if len(data['cin']) < 12:
                self.isValid = False
                QMessageBox.critical(self.ui.lineEditCIN_4, "Erreur", "Veuillez respecter la longueur du champ CIN")
                return
            else :
                self.isValid = True

            data['datecin'] = datetime.date(self.ui.lineEditDateCIN.date().year(), self.ui.lineEditDateCIN.date().month(), self.ui.lineEditDateCIN.date().day())
            data['lieucin'] = unicode(self.ui.lineEditLeuCIN.text()).encode('utf-8')
            if self.ui.lineEditLeuCIN.text() == "":
                self.isValid = False
                QMessageBox.critical(self.ui.lineEditLeuCIN, "Erreur", "Veuillez remplir le champ Lieu CIN")
                return
            else:
                self.isValid = True
            data['actenaissance']  = 0
            data['dateacte'] = datetime.date(2001,1,1)
            data['lieuacte'] = '...'

        elif self.ui.radioBtnActeDeNaiss.isChecked():
            data['actenaissance'] = unicode(self.ui.lineEditNumActeNaiss.text()).encode('utf-8')
            if self.ui.lineEditNumActeNaiss.text() == "":
                self.isValid = False
                QMessageBox.critical(self.ui.lineEditNumActeNaiss, "Erreur", "Veuillez remplir le champ acte de naissance")
                return
            else :
                self.isValid = True
            data['dateacte'] = datetime.date(self.ui.lineEditDateActeNaiss.date().year(), self.ui.lineEditDateActeNaiss.date().month(), self.ui.lineEditDateActeNaiss.date().day())
            data['lieuacte'] = unicode(self.ui.lineEditLieuActeNaiss.text()).encode('utf-8')
            if self.ui.lineEditLieuActeNaiss.text() == "":
                self.isValid = False
                QMessageBox.critical(self.ui.lineEditLieuActeNaiss, "Erreur", "Veuillez remplir le champ lieu acte de naissance")
                return
            else:
                self.isValid = True
            data['cin'] = '...'
            data['lieucin'] = '...'
            data['datecin'] = datetime.date(2001,1,1)
        self.parent.data.append(data)
        return self.isValid
        #self.demandeurs



    def writeData(self, data, cin):
        if cin == 1:
            try:
                if self.consulter == 0:
                    if self.idConjoint:
                        if self.ui.neVersCheckBox.isChecked():
                            personne = self.cur.execute(
                                "INSERT INTO personnephysique (nompersonne, prenompersonne, nevers, sexepersonne, adressepersonne, numcipersonne, datecipersonne, lieucipersonne, situationmatrimoniale, nompere, nommere, idconjoint) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning idpersonne",
                                (data['nom'], data['prenom'], data['datenaissance'], data['sexe'], data['adresse'],
                                 data['cin'], data['datecin'], data['lieucin'], data['matrimoniale'], data['pere'],
                                 data['mere'], self.idConjoint))
                        else:
                            personne = self.cur.execute(
                            "INSERT INTO personnephysique (nompersonne, prenompersonne, datenaissancepersonne, sexepersonne, adressepersonne, numcipersonne, datecipersonne, lieucipersonne, situationmatrimoniale, nompere, nommere, idconjoint) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning idpersonne",
                            (data['nom'],data['prenom'], data['datenaissance'], data['sexe'], data['adresse'], data['cin'], data['datecin'], data['lieucin'], data['matrimoniale'], data['pere'], data['mere'], self.idConjoint))
                    else:
                        if self.ui.neVersCheckBox.isChecked():
                            personne = self.cur.execute(
                                "INSERT INTO personnephysique (nompersonne, prenompersonne, nevers, sexepersonne, adressepersonne, numcipersonne, datecipersonne, lieucipersonne, situationmatrimoniale, nompere, nommere) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning idpersonne",
                                (data['nom'], data['prenom'], data['datenaissance'], data['sexe'], data['adresse'],
                                 data['cin'],
                                 data['datecin'], data['lieucin'], data['matrimoniale'], data['pere'], data['mere']))
                        else:
                            personne = self.cur.execute(
                            "INSERT INTO personnephysique (nompersonne, prenompersonne, datenaissancepersonne, sexepersonne, adressepersonne, numcipersonne, datecipersonne, lieucipersonne, situationmatrimoniale, nompere, nommere) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning idpersonne",
                            (data['nom'], data['prenom'], data['datenaissance'], data['sexe'], data['adresse'], data['cin'],
                             data['datecin'], data['lieucin'], data['matrimoniale'], data['pere'], data['mere']))
                else: # egale 2
                    if self.idConjoint:
                        if self.ui.neVersCheckBox.isChecked():
                            personne = self.cur.execute(
                                "UPDATE personnephysique SET nompersonne = %s, prenompersonne = %s, nevers = %s, sexepersonne = %s, adressepersonne = %s, numcipersonne = %s, datecipersonne = %s, lieucipersonne = %s, situationmatrimoniale = %s, nompere = %s, nommere = %s, idconjoint = %s WHERE idpersonne = %s returning idpersonne",
                                (data['nom'], data['prenom'], data['datenaissance'], data['sexe'], data['adresse'],
                                 data['cin'], data['datecin'], data['lieucin'], data['matrimoniale'], data['pere'],
                                 data['mere'], self.idConjoint, self.idPersonne))
                        else:
                            personne = self.cur.execute(
                            "UPDATE personnephysique SET nompersonne = %s, prenompersonne = %s, datenaissancepersonne = %s, sexepersonne = %s, adressepersonne = %s, numcipersonne = %s, datecipersonne = %s, lieucipersonne = %s, situationmatrimoniale = %s, nompere = %s, nommere = %s, idconjoint = %s WHERE idpersonne = %s returning idpersonne",
                            (data['nom'],data['prenom'], data['datenaissance'], data['sexe'], data['adresse'], data['cin'], data['datecin'], data['lieucin'], data['matrimoniale'], data['pere'], data['mere'], self.idConjoint, self.idPersonne))
                    else:
                        if self.ui.neVersCheckBox.isChecked():
                            personne = self.cur.execute(
                                "UPDATE personnephysique SET nompersonne = %s, prenompersonne = %s, nevers = %s, sexepersonne = %s, adressepersonne = %s, numcipersonne = %s, datecipersonne = %s, lieucipersonne = %s, situationmatrimoniale = %s, nompere = %s, nommere = %s WHERE idpersonne = %s returning idpersonne",
                                (data['nom'], data['prenom'], data['datenaissance'], data['sexe'], data['adresse'],
                                 data['cin'],
                                 data['datecin'], data['lieucin'], data['matrimoniale'], data['pere'], data['mere'],
                                 self.idPersonne))
                        else:
                            personne = self.cur.execute(
                            "UPDATE personnephysique SET nompersonne = %s, prenompersonne = %s, datenaissancepersonne = %s, sexepersonne = %s, adressepersonne = %s, numcipersonne = %s, datecipersonne = %s, lieucipersonne = %s, situationmatrimoniale = %s, nompere = %s, nommere = %s WHERE idpersonne = %s returning idpersonne",
                            (data['nom'], data['prenom'], data['datenaissance'], data['sexe'], data['adresse'], data['cin'],
                             data['datecin'], data['lieucin'], data['matrimoniale'], data['pere'], data['mere'], self.idPersonne))
                #personne = self.cur.execute("INSERT INTO personnephysique (nompersonne) VALUES (%s) returning idpersonne",(data[0],))

                self.connection.commit()
                self.idPersonne = self.cur.fetchone()
                if self.idConjoint:
                    try:
                        conjoint = self.cur.execute(
                            "UPDATE personnephysique SET situationmatrimoniale = %s, idconjoint = %s WHERE idpersonne = %s returning idpersonne",
                            (2, self.idPersonne[0], self.idConjoint))
                        self.connection.commit()
                    except StandardError as e:
                        print e
                        self.connection.rollback()
                return True
                #print personne
            except psycopg2.Error as e:
                #print e.pgcode
                if e.pgcode == "23505":
                    QMessageBox.critical(self, "Erreur", u"Ce numero de carte d'identité éxiste déjà")
                self.connection.rollback()
                return False

        if cin == 2:
            try:
                if self.consulter == 0:
                    if self.idConjoint:
                        if self.ui.neVersCheckBox.isChecked():
                            personne = self.cur.execute(
                                "INSERT INTO personnephysique (nompersonne, prenompersonne, nevers, sexepersonne, adressepersonne, numactenaissancepersonne, dateactenaissancepersonne, lieuactenaissancepersonne, situationmatrimoniale, nompere, nommere, idconjoint) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning idpersonne",
                                (data['nom'], data['prenom'], data['datenaissance'], data['sexe'], data['adresse'],
                                 data['actenaissance'], data['dateacte'], data['lieuacte'], data['matrimoniale'],
                                 data['pere'], data['mere'], self.idConjoint))
                        else:
                            personne = self.cur.execute("INSERT INTO personnephysique (nompersonne, prenompersonne, datenaissancepersonne, sexepersonne, adressepersonne, numactenaissancepersonne, dateactenaissancepersonne, lieuactenaissancepersonne, situationmatrimoniale, nompere, nommere, idconjoint) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning idpersonne", (data['nom'],data['prenom'], data['datenaissance'], data['sexe'], data['adresse'], data['actenaissance'], data['dateacte'], data['lieuacte'], data['matrimoniale'], data['pere'], data['mere'], self.idConjoint))
                    else:
                        if self.ui.neVersCheckBox.isChecked():
                            personne = self.cur.execute(
                                "INSERT INTO personnephysique (nompersonne, prenompersonne, nevers, sexepersonne, adressepersonne, numactenaissancepersonne, dateactenaissancepersonne, lieuactenaissancepersonne, situationmatrimoniale, nompere, nommere) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning idpersonne",
                                (data['nom'], data['prenom'], data['datenaissance'], data['sexe'], data['adresse'],
                                 data['actenaissance'], data['dateacte'], data['lieuacte'], data['matrimoniale'],
                                 data['pere'],
                                 data['mere']))
                        else:
                            personne = self.cur.execute(
                            "INSERT INTO personnephysique (nompersonne, prenompersonne, datenaissancepersonne, sexepersonne, adressepersonne, numactenaissancepersonne, dateactenaissancepersonne, lieuactenaissancepersonne, situationmatrimoniale, nompere, nommere) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning idpersonne",
                            (data['nom'], data['prenom'], data['datenaissance'], data['sexe'], data['adresse'],
                             data['actenaissance'], data['dateacte'], data['lieuacte'], data['matrimoniale'], data['pere'],
                             data['mere']))
                else:
                    if self.idConjoint:
                        if self.ui.neVersCheckBox.isChecked():
                            personne = self.cur.execute(
                                "UPDATE personnephysique SET nompersonne = %s, prenompersonne = %s, nevers = %s, sexepersonne = %s, adressepersonne = %s, numactenaissancepersonne = %s, dateactenaissancepersonne = %s, lieuactenaissancepersonne = %s, situationmatrimoniale = %s, nompere = %s, nommere = %s, idconjoint = %s WHERE idpersonne = %s returning idpersonne",
                                (data['nom'], data['prenom'], data['datenaissance'], data['sexe'], data['adresse'],
                                 data['actenaissance'], data['dateacte'], data['lieuacte'], data['matrimoniale'],
                                 data['pere'], data['mere'], self.idConjoint, self.idPersonne))
                        else:
                            personne = self.cur.execute("UPDATE personnephysique SET nompersonne = %s, prenompersonne = %s, datenaissancepersonne = %s, sexepersonne = %s, adressepersonne = %s, numactenaissancepersonne = %s, dateactenaissancepersonne = %s, lieuactenaissancepersonne = %s, situationmatrimoniale = %s, nompere = %s, nommere = %s, idconjoint = %s WHERE idpersonne = %s returning idpersonne", (data['nom'],data['prenom'], data['datenaissance'], data['sexe'], data['adresse'], data['actenaissance'], data['dateacte'], data['lieuacte'], data['matrimoniale'], data['pere'], data['mere'], self.idConjoint, self.idPersonne))
                    else:
                        if self.ui.neVersCheckBox.isChecked():
                            personne = self.cur.execute(
                                "UPDATE personnephysique SET nompersonne = %s, prenompersonne = %s, nevers = %s, sexepersonne = %s, adressepersonne = %s, numactenaissancepersonne = %s, dateactenaissancepersonne = %s, lieuactenaissancepersonne = %s, situationmatrimoniale = %s, nompere = %s, nommere = %s WHERE idpersonne = %s returning idpersonne",
                                (data['nom'], data['prenom'], data['datenaissance'], data['sexe'], data['adresse'],
                                 data['actenaissance'], data['dateacte'], data['lieuacte'], data['matrimoniale'],
                                 data['pere'],
                                 data['mere'], self.idPersonne))
                        else:
                            personne = self.cur.execute(
                            "UPDATE personnephysique SET nompersonne = %s, prenompersonne = %s, datenaissancepersonne = %s, sexepersonne = %s, adressepersonne = %s, numactenaissancepersonne = %s, dateactenaissancepersonne = %s, lieuactenaissancepersonne = %s, situationmatrimoniale = %s, nompere = %s, nommere = %s WHERE idpersonne = %s returning idpersonne",
                            (data['nom'], data['prenom'], data['datenaissance'], data['sexe'], data['adresse'],
                             data['actenaissance'], data['dateacte'], data['lieuacte'], data['matrimoniale'], data['pere'],
                             data['mere'], self.idPersonne))
                #personne = self.cur.execute("INSERT INTO personnephysique (nompersonne) VALUES (%s) returning idpersonne",(data[0],))
                self.connection.commit()
                self.idPersonne = self.cur.fetchone()
                return True
                #print personne
            except StandardError as e:
                print e
                self.connection.rollback()
                return False

        if cin == 3:
            try:
                if self.consulter == 0:
                    if self.idConjoint:
                        if self.ui.neVersCheckBox.isChecked():
                            personne = self.cur.execute(
                                "INSERT INTO personnephysique (nompersonne, prenompersonne, nevers, sexepersonne, adressepersonne, situationmatrimoniale, nompere, nommere, idconjoint) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) returning idpersonne",
                                (data['nom'], data['prenom'], data['datenaissance'], data['sexe'], data['adresse'],
                                 data['matrimoniale'], data['pere'], data['mere'], self.idConjoint))
                        else:
                            personne = self.cur.execute("INSERT INTO personnephysique (nompersonne, prenompersonne, datenaissancepersonne, sexepersonne, adressepersonne, situationmatrimoniale, nompere, nommere, idconjoint) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) returning idpersonne", (data['nom'],data['prenom'], data['datenaissance'], data['sexe'], data['adresse'], data['matrimoniale'], data['pere'], data['mere'], self.idConjoint))
                    else:
                        if self.ui.neVersCheckBox.isChecked():
                            personne = self.cur.execute(
                                "INSERT INTO personnephysique (nompersonne, prenompersonne, nevers, sexepersonne, adressepersonne, situationmatrimoniale, nompere, nommere) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) returning idpersonne",
                                (data['nom'], data['prenom'], data['datenaissance'], data['sexe'], data['adresse'],
                                 data['matrimoniale'], data['pere'], data['mere']))
                        else:
                            personne = self.cur.execute(
                            "INSERT INTO personnephysique (nompersonne, prenompersonne, datenaissancepersonne, sexepersonne, adressepersonne, situationmatrimoniale, nompere, nommere) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) returning idpersonne",
                            (data['nom'], data['prenom'], data['datenaissance'], data['sexe'], data['adresse'],
                             data['matrimoniale'], data['pere'], data['mere']))
                else:
                    if self.idConjoint:
                        if self.ui.neVersCheckBox.isChecked():
                            personne = self.cur.execute(
                                "UPDATE personnephysique SET nompersonne = %s, prenompersonne = %s, nevers = %s, sexepersonne = %s, adressepersonne = %s, situationmatrimoniale = %s, nompere = %s, nommere = %s, idconjoint = % WHERE idpersonne = %s returning idpersonne",
                                (data['nom'], data['prenom'], data['datenaissance'], data['sexe'], data['adresse'],
                                 data['matrimoniale'], data['pere'], data['mere'], self.idConjoint, self.idPersonne))
                        else:
                            personne = self.cur.execute("UPDATE personnephysique SET nompersonne = %s, prenompersonne = %s, datenaissancepersonne = %s, sexepersonne = %s, adressepersonne = %s, situationmatrimoniale = %s, nompere = %s, nommere = %s, idconjoint = % WHERE idpersonne = %s returning idpersonne", (data['nom'],data['prenom'], data['datenaissance'], data['sexe'], data['adresse'], data['matrimoniale'], data['pere'], data['mere'], self.idConjoint, self.idPersonne))
                    else:
                        if self.ui.neVersCheckBox.isChecked():
                            personne = self.cur.execute(
                                "UPDATE personnephysique SET nompersonne = %s, prenompersonne = %s, nevers = %s, sexepersonne = %s, adressepersonne = %s, situationmatrimoniale = %s, nompere = %s, nommere = %s WHERE idpersonne = %s returning idpersonne",
                                (data['nom'], data['prenom'], data['datenaissance'], data['sexe'], data['adresse'],
                                 data['matrimoniale'], data['pere'], data['mere'], self.idPersonne))
                        else:
                            personne = self.cur.execute(
                            "UPDATE personnephysique SET nompersonne = %s, prenompersonne = %s, datenaissancepersonne = %s, sexepersonne = %s, adressepersonne = %s, situationmatrimoniale = %s, nompere = %s, nommere = %s WHERE idpersonne = %s returning idpersonne",
                            (data['nom'], data['prenom'], data['datenaissance'], data['sexe'], data['adresse'],
                             data['matrimoniale'], data['pere'], data['mere'], self.idPersonne))
                #personne = self.cur.execute("INSERT INTO personnephysique (nompersonne) VALUES (%s) returning idpersonne",(data[0],))
                self.connection.commit()
                self.idPersonne = self.cur.fetchone()
                return True
                #print personne
            except StandardError as e:
                print e
                self.connection.rollback()
                return False


    def updloaFiles(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.')
        print  'Path file :', filename
        self.ui.label.setPixmap(QtGui.QPixmap(filename))

    def addValueTable(self,data):
        columns = len(data)
        rowPosition = self.tbDemande.rowCount()
        self.tbDemande.setColumnCount(columns)
        self.tbDemande.insertRow(rowPosition)
        # print len(data)
        for i in range(len(data)):
            item = QtGui.QTableWidgetItem()
            item.setText(_translate("", str(data[i]), None))
            self.tbDemande.setItem(rowPosition, i, item)

    def resolve(self, name, basepath=None):
        if not basepath:
            basepath = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(basepath, name)

    def deleteDemandeurs(self):

        cursor = self.connection.cursor()

        if self.iddemande != 0 :
            print "delete"
            cursor.execute("delete from  avoir_dmd WHERE iddemandeur =%s", [int(self.clickID)])
            cursor.execute("delete from  demandeur_d WHERE iddemandeur=%s", [int(self.clickID)])
            self.connection.commit()

        self.tableWidget.removeRow(self.row)
        print "delete row"

    def cellSelected(self, row, column):

        self.clickID = self.tableWidget.item(row, 2).text()
        print "self.clickID in"
        print self.clickID
        print "self.clickID out"

        print "self.tableWidget.item(row, 3).text()"
        print self.tableWidget.item(row, 0).text()

        print "self.tableWidget.item(row, 4).text()"
        print self.tableWidget.item(row, 1).text()

        self.nomLineEdit.setText(self.tableWidget.item(row, 0).text())
        self.prenomLineEdit.setText(self.tableWidget.item(row, 1).text())

        self.row = row



    def addDemandeurs(self):

        isvalid = self.readInput()
        if isvalid :
            self.sexe = ""
            self.nom = self.ui.nomLineEdit.text()
            self.prenom = self.ui.prenomLineEdit.text()
            #self.dateNaissance = datetime.date(self.ui.lineEditDateActeNaiss.date().year(), self.ui.lineEditDateActeNaiss.date().month(), self.ui.lineEditDateActeNaiss.date().day())
            self.dateNaissance = self.ui.lineEditDateNaiss.text()

            if self.ui.radioBtnMale.isChecked():
                self.sexe = "masculin"
            elif self.ui.radioBtnFemale.isChecked():
                self.sexe = "feminin"

            cursor = self.connection.cursor()
            self.adresse = self.ui.lineEditAdresse.text()
            self.nompere = self.ui.nomDuPReLineEdit.text()
            self.nommere =  self.ui.nomDeLaMReLineEdit.text()

            dateNaissance = datetime.date(self.ui.lineEditDateNaiss.date().year(), self.ui.lineEditDateNaiss.date().month(), self.ui.lineEditDateNaiss.date().day())

            if self.ui.radioBtnCelib.isChecked():
                self.matrim = "Celibataire"
            if self.ui.radioBtnMarie.isChecked():
                self.matrim = "Marié"
            if self.ui.radioBtnVeuf.isChecked():
                self.matrim = "Veuf"

            #print " self.parent.demandeurs IN"
            #print self.demandeurs

            if self.ui.radioBtnCIN.isChecked():
                #self.CIN = "Veuf"
                self.CIN = unicode(self.ui.lineEditCIN_1.text()).encode('utf-8') + unicode(self.ui.lineEditCIN_2.text()).encode('utf-8') + unicode(self.ui.lineEditCIN_3.text()).encode( 'utf-8') + unicode(self.ui.lineEditCIN_4.text()).encode('utf-8')
            self.adresseCIN = self.ui.lineEditLeuCIN.text()
            self.dtemp = []
            dateCin = datetime.date(self.ui.lineEditDateCIN.date().year(),
                                          self.ui.lineEditDateCIN.date().month(),
                                          self.ui.lineEditDateCIN.date().day())


            if ( (str(self.nom) != "") or (str(self.prenom) != "")) :
                print "dqdqs"
                self.dtemp.append(str(self.nom))
                self.dtemp.append(str(self.prenom))
                #self.demandeurs.append(self.dtemp)
                #exe = cursor.execute("INSERT INTO demandeur (nom,prenom) VALUES (%s,%s) RETURNING id ",(str(self.nom), str(self.prenom)))
                #connection.commit()
                #self.id_of_new_row = cursor.fetchone()[0]
                #data = (self.nom, self.prenom, self.id_of_new_row)
                cursor.execute(
                    "UPDATE demandeur_d SET nom=(%s), prenom= (%s), datenaissancepersonne=(%s)  , sexepersonne=(%s) , adressepersonne=(%s) "
                    ", nompere=(%s) , nommere=(%s) , matrimoniale=(%s) , numcipersonne=(%s) , lieucipersonne=(%s) , datecipersonne=(%s)  WHERE iddemandeur = (%s)",
                    (str(self.nom), str(self.prenom), dateNaissance, str(self.sexe),str(self.adresse),str(self.nompere), str(self.nommere), str(self.matrim), self.CIN,str(self.adresseCIN), dateCin, int(self.idDemandeurs)))

                data = (self.nom, self.prenom,self.dateNaissance,self.CIN,self.sexe,self.adresse,self.nompere,self.nommere,dateCin,self.adresseCIN,self.idDemandeurs)
                self.parent.ui.tableDemande.removeRow(self.parent.currentRow)
                self.addValueTable(data)


            self.ui.nomLineEdit.setText("")
            self.ui.prenomLineEdit.setText("")
            self.close()
        else :
            return
        #return  self.demandeurs
        #



