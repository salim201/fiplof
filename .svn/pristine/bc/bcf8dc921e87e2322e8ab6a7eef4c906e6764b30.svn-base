# coding: utf-8
import os, os.path, sys, time, datetime
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *
import globalvars, psycopg2

from .Contribuable import Ui_Dialog



class ContribuableRun(QDialog):
    def __init__(self, connection):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.radioHomme.setChecked(True)
        self.connection = connection
        self.ui.CIN.setCurrentIndex(0)
        self.consulter = None
        self.missedFields = []
        self.isValid = True
        self.initDB()
        self.ui.neVersCheckBox.setChecked(False)
        print "construction contribuable"
        from Certificat.ListePersonnePqueRun import ListePersonnePqueRun
        self.listepersonne = ListePersonnePqueRun(self.connection)
        print "fin construction contribuable"
        self.initAction()
        self.initMasks()



    def initAction(self):
        self.ui.btnConsorts.clicked.connect(self.listeConsorts)
        self.ui.btnAnnuler.clicked.connect(self.close)
        self.ui.btnPersonnePhysique.clicked.connect(self.ouvrirListePersonnePhysique)
        self.listepersonne.ui.btnSelectionner.clicked.connect(self.getPersonnePhysique)
        self.ui.lineEditCIN1.textEdited.connect(self.nextFields)
        self.ui.lineEditCIN2.textEdited.connect(self.nextFields)
        self.ui.lineEditCIN3.textEdited.connect(self.nextFields)
        self.ui.neVersCheckBox.stateChanged.connect(self.updateDateField)
        #self.ui.btnOk.clicked.connect(self.readInput)

    def listeConsorts(self):
        from .ListeConsortsRun import ListeConsortsRun
        self.consorts = ListeConsortsRun(self.connection)
        try:
            self.consorts.getAllConsortsOfContribuable(self.idcontribuable)
        except StandardError as e:
            print e
        self.consorts.ui.btnOk.clicked.connect(self.getIdsConsorts)
        result = self.consorts.exec_()

    def getContribuableById(self, id):
        self.cur.execute("SELECT * FROM contribuable WHERE idcontribuable = %s", (id,))
        self.idcontribuable = id
        print self.idcontribuable
        data = self.cur.fetchone()
        print data
        self.fillFields(data)

    def fillFields(self, data):
        if data[1]:
            self.ui.lineEditNom.setText(data[1])
        if data[9]:
            self.ui.lineEditPrenom.setText(data[9])
        if data[10]:
            self.ui.lineEditAdresse.setText(data[10])
        if data[2]:
            self.ui.dateEditNaissance.setDate(data[2])
        if data[3]:
            self.ui.lineEditLieuNaissance.setText(data[3])
        if data[4]:
            self.ui.CIN.setCurrentIndex(0)
            self.ui.lineEditCIN1.setText(data[4][0:3])
            self.ui.lineEditCIN2.setText(data[4][3:6])
            self.ui.lineEditCIN3.setText(data[4][6:9])
            self.ui.lineEditCIN4.setText(data[4][9:len(data[4])])
            if data[11]:
                self.ui.dateEditCIN.setDate(data[11])
            if data[17]:
                self.ui.lineEditLieuCIN.setText(data[17])
        if data[12]:
            self.ui.CIN.setCurrentIndex(1)
            self.ui.lineEditNumActeNaissance.setText(data[12])
            if data[13]:
                self.ui.dateEditActeNaissance.setDate(data[13])
            if data[14]:
                self.ui.lineEditLieuActeNaissance.setText(data[14])
        if data[15]:
            if data[15] == "masculin":
                self.ui.radioHomme.setChecked(True)
            if data[15] == "feminin":
                self.ui.radioFemme.setChecked(True)

    def getIdsConsorts(self):
        self.idConsorts = self.consorts.getIdsConsorts()
        self.consorts.close()
        print self.idConsorts

    def writeConsorts(self):
        if self.idConsorts and self.idcontribuable:
            for idconsort in self.idConsorts:
                #print idconsort
                #print self.idcontribuable
                try:
                    print "debut try"
                    self.cur.execute("INSERT INTO contribuableconsorts(idcontribuable, idconsort) VALUES(%s, %s)", (self.idcontribuable, idconsort))
                    self.connection.commit()
                    print "fin commit"
                except StandardError as e:
                    print e
                    self.connection.rollback()

    def writeContribuable(self):
        return self.readInput()

    def initDB(self):
        self.cur = self.connection.cursor()

    def __del__(self):
        self.cur.close()

    def estConsultation(self, value):
        self.consulter = value
        if value == 0 or value == 2: #Modification ou ajout
            self.ui.lineEditLieuActeNaissance.setEnabled(True)
            self.ui.lineEditNumActeNaissance.setEnabled(True)
            self.ui.dateEditActeNaissance.setEnabled(True)
            self.ui.lineEditLieuCIN.setEnabled(True)
            self.ui.dateEditNaissance.setEnabled(True)
            self.ui.CIN.setEnabled(True)
            self.ui.lineEditAdresse.setEnabled(True)
            self.ui.lineEditPrenom.setEnabled(True)
            self.ui.lineEditNom.setEnabled(True)
            self.ui.lineEditCIN1.setEnabled(True)
            self.ui.lineEditCIN2.setEnabled(True)
            self.ui.lineEditCIN3.setEnabled(True)
            self.ui.lineEditCIN4.setEnabled(True)
            self.ui.radioFemme.setEnabled(True)
            self.ui.radioHomme.setEnabled(True)
            self.ui.checkBox.setEnabled(True)
            if value == 2:
                self.clearAll()
        else:
            self.ui.lineEditLieuActeNaissance.setDisabled(True)
            self.ui.lineEditNumActeNaissance.setDisabled(True)
            self.ui.dateEditActeNaissance.setDisabled(True)
            self.ui.lineEditLieuCIN.setDisabled(True)
            self.ui.dateEditNaissance.setDisabled(True)
            self.ui.CIN.setDisabled(True)
            self.ui.lineEditAdresse.setDisabled(True)
            self.ui.lineEditPrenom.setDisabled(True)
            self.ui.lineEditNom.setDisabled(True)
            self.ui.lineEditCIN1.setDisabled(True)
            self.ui.lineEditCIN2.setDisabled(True)
            self.ui.lineEditCIN3.setDisabled(True)
            self.ui.lineEditCIN4.setDisabled(True)
            self.ui.radioFemme.setDisabled(True)
            self.ui.radioHomme.setDisabled(True)
            self.ui.checkBox.setDisabled(True)

    def clearAll(self):
        self.ui.lineEditLieuActeNaissance.clear()
        self.ui.lineEditNumActeNaissance.clear()
        self.ui.dateEditActeNaissance.clear()
        self.ui.lineEditLieuCIN.clear()
        self.ui.dateEditNaissance.clear()
        #self.ui.CIN.clear()
        self.ui.lineEditAdresse.clear()
        self.ui.lineEditPrenom.clear()
        self.ui.lineEditNom.clear()
        self.ui.lineEditCIN1.clear()
        self.ui.lineEditCIN2.clear()
        self.ui.lineEditCIN3.clear()
        self.ui.lineEditCIN4.clear()
        #self.ui.radioFemme.setDisabled(True)
        #self.ui.radioHomme.setDisabled(True)

    def ouvrirListePersonnePhysique(self):
        self.listepersonne.exec_()

    def getPersonnePhysique(self):
        if self.listepersonne is not None:
            idPersonne = self.listepersonne.getIdPersonne()
            print idPersonne
            self.listepersonne.close()
            try:
                self.cur.execute("SELECT * FROM personnephysique WHERE idpersonne = %s", (idPersonne,))
                self.dataToShow = self.cur.fetchone()
                self.showDetails(self.dataToShow)
            except StandardError as e:
                print e

    def showDetails(self, data):
        if data[1]:
            self.ui.lineEditNom.setText(data[1])
        if data[2]:
            self.ui.lineEditPrenom.setText(data[2])
        if data[3]:
            self.ui.dateEditNaissance.setDate(data[3])
        if data[4]:
            self.ui.lineEditLieuNaissance.setText(data[4])
        if data[5] == 'masculin':
            self.ui.radioHomme.setChecked(True)

        if data[5] == 'feminin':
            self.ui.radioFemme.setChecked(True)
        if data[6]:
            self.ui.lineEditAdresse.setText(data[6])
        if data[8] is not None: #CIN
            self.ui.CIN.setCurrentIndex(0)
            #self.ui.radioBtnCIN.setChecked(True)
            self.ui.lineEditCIN1.setText(data[8][0:3])
            self.ui.lineEditCIN2.setText(data[8][3:6])
            self.ui.lineEditCIN3.setText(data[8][6:9])
            self.ui.lineEditCIN4.setText(data[8][9:len(data[8])])
            if data[9]:
                self.ui.dateEditCIN.setDate(data[9])
            if data[10]:
                self.ui.lineEditLieuCIN.setText(data[10])

            #self.radioBtnActeDeNaiss.setChecked(True)
            #Effacer champs Acte de naissance
            self.ui.lineEditNumActeNaissance.setText('')
            self.ui.dateEditActeNaissance.hide()
            self.ui.lineEditLieuActeNaissance.setText('')

        elif data[11] is not None and data[11] != 0: #acte de naissance
            self.ui.CIN.setCurrentIndex(1)
            #self.ui.radioBtnActeDeNaiss.setChecked(True)
            self.ui.lineEditNumActeNaissance.setText(data[11])
            if data[12]:
                self.ui.dateEditActeNaissance.setDate(data[12])
            if data[13]:
                self.ui.lineEditLieuActeNaissance.setText(data[13])
            #Effacer champs CIN
            self.ui.lineEditCIN1.setText('')
            self.ui.lineEditCIN2.setText('')
            self.ui.lineEditCIN3.setText('')
            self.ui.lineEditCIN4.setText('')
            self.ui.dateEditCIN.hide()
            self.ui.lineEditLieuCIN.setText('')

    def readInput(self):
        self.isValid = True
        print "Read input ato"
        if self.consulter != 1:
            print "AJOUT OU MODIFICATION"
            self.missedFields[:] = []
            data = {}
            data['nom'] = unicode(self.ui.lineEditNom.text()).encode('utf-8')
            if self.ui.lineEditNom.text() == '':
                self.missedFields.append("Nom")
                self.isValid = False

            data['prenom'] = unicode(self.ui.lineEditPrenom.text()).encode('utf-8')
            if self.ui.neVersCheckBox.isChecked():
                data['datenaissance'] = self.ui.dateEditNaissance.date().year()
            else:
                data['datenaissance'] = datetime.date(self.ui.dateEditNaissance.date().year(), self.ui.dateEditNaissance.date().month(), self.ui.dateEditNaissance.date().day())

            data['lieunaissance'] = unicode(self.ui.lineEditLieuNaissance.text()).encode('utf-8')

            if self.ui.radioHomme.isChecked():
                data['sexe'] = "masculin"
            elif self.ui.radioFemme.isChecked():
                data['sexe'] = "feminin"

            data['adresse'] = unicode(self.ui.lineEditAdresse.text()).encode('utf-8')
            #data['pere'] = unicode(self.ui.nomDuPReLineEdit.text()).encode('utf-8')
            #data['mere'] = unicode(self.ui.nomDeLaMReLineEdit.text()).encode('utf-8')

            #if self.ui.radioBtnCelib.isChecked():
                #data['matrimoniale'] = 1
            #elif self.ui.radioBtnMarie.isChecked():
                #data['matrimoniale'] = 2
            #elif self.ui.radioBtnVeuf.isChecked():
                #data['matrimoniale'] = 3


            if self.ui.CIN.currentIndex() == 0: # CIN
                data['cin'] = unicode(self.ui.lineEditCIN1.text()).encode('utf-8') + unicode(self.ui.lineEditCIN2.text()).encode('utf-8') + unicode(self.ui.lineEditCIN3.text()).encode('utf-8') + unicode(self.ui.lineEditCIN4.text()).encode('utf-8')
                if len(data['cin']) < 12:
                    self.missedFields.append("Numero CIN")
                    self.isValid = False
                data['datecin'] = datetime.date(self.ui.dateEditCIN.date().year(), self.ui.dateEditCIN.date().month(), self.ui.dateEditCIN.date().day())
                data['lieucin'] = unicode(self.ui.lineEditLieuCIN.text()).encode('utf-8')
                if self.ui.lineEditLieuCIN.text() == "":
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
            elif self.ui.CIN.currentIndex() == 1: #Acte de naissance
                data['actenaissance'] = unicode(self.ui.lineEditNumActeNaissance.text()).encode('utf-8')
                if self.ui.lineEditNumActeNaissance.text() == "":
                    self.missedFields.append("Numero acte de naissance")
                    self.isValid = False
                data['dateacte'] = datetime.date(self.ui.dateEditActeNaissance.date().year(), self.ui.dateEditActeNaissance.date().month(), self.ui.dateEditActeNaissance.date().day())
                data['lieuacte'] = unicode(self.ui.lineEditLieuNaissance.text()).encode('utf-8')
                if self.ui.lineEditLieuActeNaissance.text() == "":
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
            elif self.ui.CIN.currentIndex() == 2:
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

    def writeData(self, data, cin):
        if cin == 1:
            print "Ato am writedata"
            try:
                if self.consulter == 2:
                    print "Ajout de contribuable"
                    try:
                        if self.ui.neVersCheckBox.isChecked():
                            personne = self.cur.execute(
                                    "INSERT INTO contribuable (nom, prenom, nevers, lieu , sexe, adresse, cin, datecin, lieucin) "
                                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) returning idcontribuable",
                                    (data['nom'],data['prenom'], data['datenaissance'], data['lieunaissance'], data['sexe'], data['adresse'], data['cin'], data['datecin'], data['lieucin']))
                            print "Fin ajout contribuable"
                        else:
                            personne = self.cur.execute(
                                    "INSERT INTO contribuable (nom, prenom, datenaissance, lieu , sexe, adresse, cin, datecin, lieucin) "
                                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) returning idcontribuable",
                                    (data['nom'],data['prenom'], data['datenaissance'], data['lieunaissance'], data['sexe'], data['adresse'], data['cin'], data['datecin'], data['lieucin']))
                            print "Fin ajout contribuable"
                    except psycopg2.Error as e:
                        print e
                        if e.pgcode == "23505":
                            QMessageBox.critical(self, "Erreur",
                                                     u"Un contribuable possedant le même numero CIN existe déjà ")
                            self.connection.rollback()
                            self.close()
                            return
                else: # egale 0
                    if self.ui.neVersCheckBox.isChecked():
                        personne = self.cur.execute(
                            "UPDATE contribuable SET nom = %s, prenom = %s, nevers = %s, lieu = %s, sexe = %s, adresse = %s, cin = %s, datecin = %s, lieucin = %s WHERE idcontribuable = %s returning idcontribuable",
                            (data['nom'], data['prenom'], data['datenaissance'], data['lieunaissance'], data['sexe'],
                             data['adresse'], data['cin'], data['datecin'], data['lieucin'], self.idcontribuable))
                    else:
                        personne = self.cur.execute(
                            "UPDATE contribuable SET nom = %s, prenom = %s, datenaissance = %s, lieu = %s, sexe = %s, adresse = %s, cin = %s, datecin = %s, lieucin = %s WHERE idcontribuable = %s returning idcontribuable",
                            (data['nom'],data['prenom'], data['datenaissance'], data['lieunaissance'], data['sexe'], data['adresse'], data['cin'], data['datecin'], data['lieucin'], self.idcontribuable))

                self.connection.commit()
                self.idcontribuable = self.cur.fetchone()
                return True
                #print personne
            except psycopg2.Error as e:
                print e
                if e.pgcode == "23505":
                    QMessageBox.critical(self, "Erreur", u"Un contribuable possedant le même numero CIN existe déjà ")
                self.connection.rollback()
                return False

        if cin == 2:
            try:
                if self.consulter == 2:
                    if self.ui.neVersCheckBox.isChecked():
                        personne = self.cur.execute("INSERT INTO contribuable (nom, prenom, nevers, "
                                                    " lieu, sexe, adresse, numactenaissance, dateactenaissance, lieuactenaissance) "
                                                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) returning idcontribuable",
                                                    (data['nom'], data['prenom'], data['datenaissance'],
                                                     data['lieunaissance'], data['sexe'], data['adresse'],
                                                     data['actenaissance'], data['dateacte'], data['lieuacte']))
                    else:
                        personne = self.cur.execute("INSERT INTO contribuable (nom, prenom, datenaissance, "
                                                " lieu, sexe, adresse, numactenaissance, dateactenaissance, lieuactenaissance) "
                                                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) returning idcontribuable",
                                                (data['nom'],data['prenom'], data['datenaissance'], data['lieunaissance'], data['sexe'], data['adresse'], data['actenaissance'], data['dateacte'], data['lieuacte']))

                else:
                    if self.ui.neVersCheckBox.isChecked():
                        personne = self.cur.execute(
                            "UPDATE contribuable SET nom = %s, prenom = %s, nevers = %s, "
                            "lieu = %s, sexe = %s, adresse = %s, numactenaissance = %s, dateactenaissance = %s, lieuactenaissance = %s WHERE idcontribuable = %s returning idcontribuable",
                            (data['nom'], data['prenom'], data['datenaissance'], data['lieunaissance'], data['sexe'],
                             data['adresse'], data['actenaissance'], data['dateacte'], data['lieuacte'],
                             self.idcontribuable))
                    else:
                        personne = self.cur.execute("UPDATE contribuable SET nom = %s, prenom = %s, datenaissance = %s, "
                                                "lieu = %s, sexe = %s, adresse = %s, numactenaissance = %s, dateactenaissance = %s, lieuactenaissance = %s WHERE idcontribuable = %s returning idcontribuable",
                                                (data['nom'],data['prenom'], data['datenaissance'],data['lieunaissance'], data['sexe'], data['adresse'], data['actenaissance'], data['dateacte'], data['lieuacte'], self.idcontribuable))

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
                if self.consulter == 2:
                    personne = self.cur.execute("INSERT INTO contribuable (nom, prenom, datenaissance, "
                                                "lieu, sexe, adresse) VALUES (%s, %s, %s, %s, %s, %s) returning idcontribuable", (data['nom'],data['prenom'], data['datenaissance'], data['lieu'], data['sexe'], data['adresse']))

                else:
                    personne = self.cur.execute("UPDATE contribuable SET nom = %s, prenom = %s, datenaissance = %s, sexe = %s, adresse = %s WHERE idcontribuable = %s returning idcontribuable", (data['nom'],data['prenom'], data['datenaissance'], data['sexe'], data['adresse'], self.idcontribuable))

                self.connection.commit()
                self.idPersonne = self.cur.fetchone()
                return True
                #print personne
            except StandardError as e:
                print e
                self.connection.rollback()
                return False

    def initMasks(self):
        validatorAlpha = QRegExpValidator(globalvars.regexpAlpha)
        validatorAlphaNum = QRegExpValidator(globalvars.regexpAlphaNum)
        validatorNum = QRegExpValidator(globalvars.regexpNum)

        self.ui.lineEditNom.setValidator(validatorAlpha)
        self.ui.lineEditPrenom.setValidator(validatorAlpha)
        self.ui.lineEditAdresse.setValidator(validatorAlphaNum)
        #self.ui.nomDuPReLineEdit.setValidator(validatorAlpha)
        #self.ui.nomDeLaMReLineEdit.setValidator(validatorAlpha)
        self.ui.lineEditCIN1.setValidator(validatorNum)
        self.ui.lineEditCIN2.setValidator(validatorNum)
        self.ui.lineEditCIN3.setValidator(validatorNum)
        self.ui.lineEditCIN4.setValidator(validatorNum)
        self.ui.lineEditLieuCIN.setValidator(validatorAlphaNum)
        self.ui.lineEditNumActeNaissance.setValidator(validatorNum)
        self.ui.lineEditLieuActeNaissance.setValidator(validatorAlphaNum)
        #self.ui.lineEditCIN.setMaxLength(3)
        self.ui.lineEditCIN1.setMaxLength(3)
        self.ui.lineEditCIN2.setMaxLength(3)
        self.ui.lineEditCIN3.setMaxLength(3)
        self.ui.lineEditCIN4.setMaxLength(3)

    def nextFields(self):
        senderName = self.sender().objectName()
        if senderName == "lineEditCIN1" and self.sender().text().length() == 3:
            self.ui.lineEditCIN2.setFocus()
        if senderName == "lineEditCIN2" and self.sender().text().length() == 3:
            self.ui.lineEditCIN3.setFocus()
        if senderName == "lineEditCIN3" and self.sender().text().length() == 3:
            self.ui.lineEditCIN4.setFocus()

    def updateDateField(self):
        if self.ui.neVersCheckBox.isChecked():
            self.ui.dateEditActeNaissance.setDisplayFormat("yyyy")
            self.ui.dateEditActeNaissance.setCalendarPopup(False)
        else:
            self.ui.dateEditActeNaissance.setDisplayFormat("dd/MM/yyyy")
            self.ui.dateEditActeNaissance.setCalendarPopup(True)
