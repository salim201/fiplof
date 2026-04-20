#coding: utf-8
from PyQt4.QtGui import *
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import *
import time, psycopg2, datetime, os, sys
from psycopg2.extensions import *
from .PersonnePhysique import Ui_Dialog
import globalvars

#sys.setrecursionlimit(1500)

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class PersonnePhysiqueRun(QDialog):
    def __init__(self, connection, idConjoint = None):
        QDialog.__init__(self)
        self.setModal(True)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setModal(True)
        self.ui.neVersCheckBox.setChecked(False)
        self.ui.lineEditDateCIN.setCalendarPopup(True)
        self.connection = connection
        self.initActions()
        self.initDB()
        self.consulter = 0
        self.ui.stackedWidget.setCurrentIndex(0)
        self.initMasks()
        self.isValid = True
        self.missedFields = []
        self.idConjoint = idConjoint
        if self.idConjoint != None:
            self.getPersonneById(self.idConjoint)
            self.showDetails(self.dataToShow)



    def initActions(self):
        self.ui.radioBtnCIN.clicked.connect(self.showCin)
        self.ui.radioBtnActeDeNaiss.clicked.connect(self.showActeNaiss)
        #self.btnOk.clicked.connect(self.readInput)
        self.ui.radioBtnCelib.clicked.connect(self.changeMatrimoniale)
        self.ui.radioBtnMarie.clicked.connect(self.changeMatrimoniale)
        self.ui.radioBtnVeuf.clicked.connect(self.changeMatrimoniale)
        self.ui.btnAnnuler.clicked.connect(self.close)
        self.ui.lineEditCIN_1.textEdited.connect(self.nextFields)
        self.ui.lineEditCIN_2.textEdited.connect(self.nextFields)
        self.ui.lineEditCIN_3.textEdited.connect(self.nextFields)
        self.ui.neVersCheckBox.stateChanged.connect(self.updateDateField)

        self.ui.btnListePersSimil.setVisible(False)
        self.ui.btnOk.setVisible(False)
        self.ui.btnAnnuler.setVisible(False)
        self.ui.btnSelectionner.setVisible(False)

    def ouvrirListePersonnePque(self):
        from .ListePersonnePqueRun import ListePersonnePqueRun
        self.listepersonne = ListePersonnePqueRun(self.connection)
        self.listepersonne.ui.btnSelectionner.clicked.connect(self.ajoutConjoint)
        self.listepersonne.show()
        result = self.listepersonne.exec_()


    def voirConjoint(self):
        try:
            self.conjoint = PersonnePhysiqueRun(self.connection, self.idConjoint)
            self.conjoint.consultation(1)
            #self.conjoint.getPersonneById(self.idConjoint)
            result = self.conjoint.exec_()
        except StandardError as e:
            print e

    def showCin(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def showActeNaiss(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def readInput(self):
        if self.consulter != 1:
            self.missedFields[:] = []
            data = {}
            data['nom'] = unicode(self.ui.lineEditNom.text()).encode('utf-8')
            if self.ui.lineEditNom.text() == '':
                self.missedFields.append("Nom")
                self.isValid = False

            data['prenom'] = unicode(self.ui.lineEditPrenom.text()).encode('utf-8')
            if self.ui.neVersCheckBox.isChecked():
                data['datenaissance'] = self.ui.lineEditDateNaiss.date().year()
            else:
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
                    self.missedFields.append("Numero CIN")
                    self.isValid = False
                data['datecin'] = datetime.date(self.ui.lineEditDateCIN.date().year(), self.ui.lineEditDateCIN.date().month(), self.ui.lineEditDateCIN.date().day())
                data['lieucin'] = unicode(self.ui.lineEditLeuCIN.text()).encode('utf-8')
                if self.ui.lineEditLeuCIN.text() == "":
                    self.missedFields.append("Lieu CIN")
                    self.isValid = False
                if self.isValid:
                    return self.writeData(data, 1)
                else:
                    print "erreur"
                    message = "Les champs suivants sont obligatoires "
                    for value in self.missedFields:
                        message = message + value + ",  "
                    qmessage = QString(message)
                    self.messageErreur(qmessage)
                    return False
            elif self.ui.radioBtnActeDeNaiss.isChecked():
                data['actenaissance'] = unicode(self.ui.lineEditNumActeNaiss.text()).encode('utf-8')
                if self.ui.lineEditNumActeNaiss.text() == "":
                    self.missedFields.append("Numero acte de naissance")
                    self.isValid = False
                data['dateacte'] = datetime.date(self.ui.lineEditDateActeNaiss.date().year(), self.ui.lineEditDateActeNaiss.date().month(), self.ui.lineEditDateActeNaiss.date().day())
                data['lieuacte'] = unicode(self.ui.lineEditLieuActeNaiss.text()).encode('utf-8')
                if self.ui.lineEditLieuActeNaiss.text() == "":
                    self.missedFields.append("Lieu acte de naissance")
                    self.isValid = False
                if self.isValid:
                    return self.writeData(data, 2)
                else:
                    print "erreur"
                    message = "Les champs suivants sont obligatoires "
                    for value in self.missedFields:
                        message = message + value + ",  "
                    qmessage = QString(message)
                    self.messageErreur(qmessage)
                    return False
            elif self.ui.radioBtnRien.isChecked():
                data['rien'] = ''
                if self.isValid:
                    return self.writeData(data, 3)
                else:
                    print "erreur"
                    message = "Les champs suivants sont obligatoires "
                    for value in self.missedFields:
                        message = message + value + ",  "
                    qmessage = QString(message)
                    self.messageErreur(qmessage)
                    return False
        else:
            self.close()




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

    def initDB(self):
        self.cur = self.connection.cursor()
        # revenir au fichier de depart

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


    def getPersonneById(self, idpersonne):
        self.idConjoint = None
        self.cur.execute("SELECT * FROM personnephysique WHERE idpersonne = %s", (idpersonne, ))
        self.idPersonne = idpersonne
        self.dataToShow = self.cur.fetchone()
        if self.dataToShow[14] != None:
            self.idConjoint = self.dataToShow[14]
            self.ui.btnEtatConjoint.clicked.connect(self.voirConjoint)
        else:
            self.ui.btnEtatConjoint.clicked.connect(self.ouvrirListePersonnePque)

        print self.dataToShow[1]
        #self.dataToShow
        #if self.consulter == 1:
            #self.showDetails(data)
            # if self.consulter == 1:
            # self.showDetails(data)

    def showDetails(self, data):
        if data[1]:
            self.ui.lineEditNom.setText(data[1])
        if data[2]:
            self.ui.lineEditPrenom.setText(data[2])
        if data[3]:
            self.ui.lineEditDateNaiss.setDate(data[3])
        if data[5] == 'masculin':
            self.ui.radioBtnMale.setChecked(True)

        if data[5] == 'feminin':
            self.ui.radioBtnFemale.setChecked(True)
        if data[6]:
            self.ui.lineEditAdresse.setText(data[6])
        if data[8]:
            self.ui.stackedWidget.setCurrentIndex(0)
            self.ui.radioBtnCIN.setChecked(True)
            self.ui.lineEditCIN_1.setText(data[8][0:3])
            self.ui.lineEditCIN_2.setText(data[8][3:6])
            self.ui.lineEditCIN_3.setText(data[8][6:9])
            self.ui.lineEditCIN_4.setText(data[8][9:len(data[8])])
            if data[9]:
                self.ui.lineEditDateCIN.setDate(data[9])
            if data[10]:
                self.ui.lineEditLeuCIN.setText(data[10])

            #self.radioBtnActeDeNaiss.setChecked(True)
            #Effacer champs Acte de naissance
            self.ui.lineEditNumActeNaiss.setText('')
            self.ui.lineEditDateActeNaiss.hide()
            self.ui.lineEditLieuActeNaiss.setText('')

        if data[11]:
            self.ui.stackedWidget.setCurrentIndex(1)
            self.ui.radioBtnActeDeNaiss.setChecked(True)
            self.ui.lineEditNumActeNaiss.setText(data[11])
            if data[12]:
                self.ui.lineEditDateActeNaiss.setDate(data[12])
            if data[13]:
                self.ui.lineEditLieuActeNaiss.setText(data[13])
            #Effacer champs CIN
            self.ui.lineEditCIN_1.setText('')
            self.ui.lineEditCIN_2.setText('')
            self.ui.lineEditCIN_3.setText('')
            self.ui.lineEditCIN_4.setText('')
            self.ui.lineEditDateCIN.hide()
            self.ui.lineEditLeuCIN.setText('')

        if data[15] == 1:
            self.ui.btnEtatConjoint.setEnabled(False)
            self.ui.radioBtnCelib.setChecked(True)
        if data[15] == 2:
            self.ui.btnEtatConjoint.setEnabled(True)
            self.ui.radioBtnMarie.setChecked(True)
        if data[15] == 3:
            self.ui.btnEtatConjoint.setEnabled(True)
            self.ui.radioBtnVeuf.setChecked(True)
        if data[16]:
            self.ui.nomDuPReLineEdit.setText(data[16])
        if data[17]:
            self.ui.nomDeLaMReLineEdit.setText(data[17])


    def consultation(self, value):
        # self.consulter = 0 => ajout d'une personne, 1 => consultation d'une personne (lecture seule), 2 => modification d'une personne
        if value == 1: # consultation
            self.ui.lineEditNom.setEnabled(False)
            self.ui.lineEditLieuActeNaiss.setEnabled(False)
            self.ui.lineEditDateActeNaiss.setEnabled(False)
            self.ui.lineEditNumActeNaiss.setEnabled(False)
            self.ui.lineEditLeuCIN.setEnabled(False)
            self.ui.lineEditCIN_4.setEnabled(False)
            self.ui.lineEditCIN_3.setEnabled(False)
            self.ui.lineEditCIN_2.setEnabled(False)
            self.ui.lineEditCIN_1.setEnabled(False)
            self.ui.radioBtnVeuf.setEnabled(False)
            self.ui.radioBtnMarie.setEnabled(False)
            self.ui.radioBtnCelib.setEnabled(False)
            self.ui.radioBtnActeDeNaiss.setEnabled(False)
            self.ui.radioBtnCIN.setEnabled(False)
            self.ui.radioBtnRien.setEnabled(False)
            self.ui.radioBtnFemale.setEnabled(False)
            self.ui.radioBtnMale.setEnabled(False)
            self.ui.btnEtatConjoint.setEnabled(False)
            self.ui.lineEditAdresse.setEnabled(False)
            self.ui.lineEditPrenom.setEnabled(False)
            self.ui.lineEditDateCIN.setEnabled(False)
            self.ui.lineEditDateNaiss.setEnabled(False)
            self.ui.nomDeLaMReLineEdit.setEnabled(False)
            self.ui.nomDuPReLineEdit.setEnabled(False)

            self.consulter = value
            self.showDetails(self.dataToShow)
        elif value == 0 or value == 2:
            self.ui.lineEditNom.setEnabled(True)
            self.ui.lineEditLieuActeNaiss.setEnabled(True)
            self.ui.lineEditDateActeNaiss.setEnabled(True)
            self.ui.lineEditNumActeNaiss.setEnabled(True)
            self.ui.lineEditLeuCIN.setEnabled(True)
            self.ui.lineEditCIN_4.setEnabled(True)
            self.ui.lineEditCIN_3.setEnabled(True)
            self.ui.lineEditCIN_2.setEnabled(True)
            self.ui.lineEditCIN_1.setEnabled(True)
            self.ui.radioBtnVeuf.setEnabled(True)
            self.ui.radioBtnMarie.setEnabled(True)
            self.ui.radioBtnCelib.setEnabled(True)
            self.ui.radioBtnActeDeNaiss.setEnabled(True)
            self.ui.radioBtnCIN.setEnabled(True)
            self.ui.radioBtnRien.setEnabled(True)
            self.ui.radioBtnFemale.setEnabled(True)
            self.ui.radioBtnMale.setEnabled(True)
            self.ui.btnEtatConjoint.setEnabled(True)
            self.ui.lineEditAdresse.setEnabled(True)
            self.ui.lineEditPrenom.setEnabled(True)
            self.ui.lineEditDateCIN.setEnabled(True)
            self.ui.lineEditDateNaiss.setEnabled(True)
            self.ui.nomDeLaMReLineEdit.setEnabled(True)
            self.ui.nomDuPReLineEdit.setEnabled(True)
            if value == 0:
                self.consulter = value
                self.viderChamps()
            else:
                self.consulter = value
                self.showDetails(self.dataToShow)

    def viderChamps(self):
        self.ui.lineEditNom.clear()
        self.ui.lineEditLieuActeNaiss.clear()
        self.ui.lineEditDateActeNaiss.setEnabled(True)
        self.ui.lineEditNumActeNaiss.clear()
        self.ui.lineEditLeuCIN.clear()
        self.ui.lineEditCIN_4.clear()
        self.ui.lineEditCIN_3.clear()
        self.ui.lineEditCIN_2.clear()
        self.ui.lineEditCIN_1.clear()
        self.ui.radioBtnCelib.setChecked(True)
        self.ui.radioBtnCIN.setChecked(True)
        self.ui.radioBtnMale.setChecked(True)
        self.ui.btnEtatConjoint.setDisabled(True)
        self.ui.lineEditAdresse.clear()
        self.ui.lineEditPrenom.clear()
        self.ui.lineEditDateCIN.setDate(QDate.currentDate())
        self.ui.lineEditDateNaiss.setDate(QDate.currentDate())
        self.ui.nomDeLaMReLineEdit.clear()
        self.ui.nomDuPReLineEdit.clear()

        ###### Masque de saisie#######

    def initMasks(self):
        validatorAlpha = QRegExpValidator(globalvars.regexpAlpha)
        validatorAlphaNum = QRegExpValidator(globalvars.regexpAlphaNum)
        validatorNum = QRegExpValidator(globalvars.regexpNum)

        self.ui.lineEditNom.setValidator(validatorAlpha)
        self.ui.lineEditPrenom.setValidator(validatorAlpha)
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
        #self.ui.lineEditCIN.setMaxLength(3)
        self.ui.lineEditCIN_1.setMaxLength(3)
        self.ui.lineEditCIN_2.setMaxLength(3)
        self.ui.lineEditCIN_3.setMaxLength(3)
        self.ui.lineEditCIN_4.setMaxLength(3)

    def messageErreur(self, message):
        self.isValid = True
        msgBox = QtGui.QMessageBox()
        msgBox.setText(message)
        msgBox.setModal(True)
        msgBox.show()
        msgBox.exec_()

    def getIdPersonne(self):
        return self.idPersonne

    def ajoutConjoint(self):
        self.idConjoint = self.listepersonne.getIdPersonne()
        self.listepersonne.close()

    def nextFields(self):
        senderName = self.sender().objectName()
        if senderName == "lineEditCIN_1" and self.sender().text().length() == 3:
            self.ui.lineEditCIN_2.setFocus()
        if senderName == "lineEditCIN_2" and self.sender().text().length() == 3:
            self.ui.lineEditCIN_3.setFocus()
        if senderName == "lineEditCIN_3" and self.sender().text().length() == 3:
            self.ui.lineEditCIN_4.setFocus()

    def updateDateField(self):
        if self.ui.neVersCheckBox.isChecked():
            self.ui.lineEditDateNaiss.setDisplayFormat("yyyy")
            self.ui.lineEditDateNaiss.setCalendarPopup(False)
        else:
            self.ui.lineEditDateNaiss.setDisplayFormat("dd/MM/yyyy")
            self.ui.lineEditDateNaiss.setCalendarPopup(True)

    def __del__(self):
        self.cur.close()


