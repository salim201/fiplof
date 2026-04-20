import os, os.path, sys
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *
from PyQt4 import QtGui, QtCore
import psycopg2, time, datetime, globalvars

from .PersonneMorale import Ui_Dialog
from Utilisateur import AccesManager

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class PersonneMoraleRun(QDialog):
    def __init__(self, connection, parent = None):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setModal(True)
        self.connection = connection
        from .ListeTypePersonneMoraleRun import ListeTypePersonneMoraleRun
        self.typePersonneMorale = ListeTypePersonneMoraleRun(self.connection)
        self.typePersonneMorale.listChanged.connect(self.fillComboType)
        self.initActions()
        self.initDB()
        self.consulter = 0
        self.isValid = True
        self.missedFields = []
        self.idTypes = []
        self.fillComboType()
        self.initMasks()
        self.parent = parent

        self.ui.btnAnnuler.clicked.connect(self.close)
        self.getPersonneById()
        #self.ui.btnOk.clicked.connect(self.enregAndClose)

 #   def enregAndClose(self):
       # self.readInput()
       # self.close()

    def initActions(self):
        self.ui.btnListe.clicked.connect(self.listerTypeMorale)
        self.ui.btnAnnuler.clicked.connect(self.reject)
        #self.ui.toolBtnCalendrier.clicked.connect(self.showCalWid) #date creation personne
        self.ui.btnOk.clicked.connect(self.readInput)

    def listerTypeMorale(self):
        self.typePersonneMorale.exec_()

    def fillComboType(self):
        self.ui.comboBoxType.clear()
        self.cur.execute("SELECT * FROM typepersonnemorale")
        data = self.cur.fetchall()
        print data
        i = 0
        while i < len(data):
            self.idTypes.append(int(data[i][0]))
            self.ui.comboBoxType.addItem(_fromUtf8(data[i][1]))
            i = i + 1


    def initDB(self):
        self.cur = self.connection.cursor()
        # revenir au fichier de depart


    def readInput(self):
        if self.consulter == 1:
            self.close()
        else:

            data = {}
            index = self.ui.comboBoxType.currentIndex()
            data['type'] = self.idTypes[index]
            print data['type']
            if self.ui.lineEditNom.text() != "":
                data['denomination'] = unicode(self.ui.lineEditNom.text()).encode('utf-8')
            else:
                self.missedFields.append("Nom")
                self.isValid = False
            data['datecreation'] = datetime.date(self.ui.dateEditCreation.date().year(), self.ui.dateEditCreation.date().month(), self.ui.dateEditCreation.date().day())
            if self.ui.lineEditSiege.text() != "":
                data['siege'] = unicode(self.ui.lineEditSiege.text()).encode('utf-8')
            else:
                self.missedFields.append("siege")
                self.isValid = False
            data['obs'] = unicode(self.ui.textEdit.toPlainText()).encode('utf-8')

            if self.isValid:
                if self.insertData(data):
                    self.accept()
            else:
                print "erreur"
                message = "Les champs suivants sont obligatoires "
                for value in self.missedFields:
                    message = message + value + ",  "
                qmessage = QString(message)
                self.messageErreur(qmessage)
                return False

    def insertData(self, data):
        if self.consulter == 0:
            print(data)
            try:
                self.cur.execute("INSERT INTO personnemorale (denomination, datecreation, siege, observation, idtype) VALUES (%s, %s, %s, %s, %s) returning idpersonnemorale",(data['denomination'], data['datecreation'], data['siege'], data['obs'], data['type']))
                self.connection.commit()
                print "avant fetch"
                self.idPersonne = self.cur.fetchone()
                print "apres fetch"
                return self.idPersonne
                #return True
            except StandardError as e:
                print e
                self.connection.rollback()
                return False

        else:
            try:
                self.cur.execute("UPDATE personnemorale SET denomination = %s, datecreation = %s, siege = %s, observation = %s, idtype = %s WHERE idpersonnemorale = %s returning idpersonnemorale",(data['denomination'], data['datecreation'], data['siege'], data['obs'], data['type'], self.idPersonne))
                self.connection.commit()
                #self.idPersonne = self.cur.fetchone()
                self.idPersonne = self.cur.fetchone()
                return self.idPersonne
            except StandardError as e:
                print e
                self.connection.rollback()
                return False


    def getPersonneById(self):
        print "get by id"
        if self.parent:
            idpersonne = self.parent.idpersonne
            print idpersonne
            try:
                self.cur.execute( "SELECT DISTINCT pm.idpersonnemorale, pm.denomination, pm.datecreation, pm.siege, pm.observation, pm.idtype, tpm.type, tpm.idtype, COALESCE(CONCAT(pp.nompersonne,' ',pp.prenompersonne), '') as personne_representant, pm.idrepresentant FROM typepersonnemorale tpm, personnemorale pm LEFT JOIN personne pp ON pm.idrepresentant=pp.idpersonne WHERE pm.idtype=tpm.idtype AND pm.idpersonnemorale = %s", (idpersonne,))
                data = self.cur.fetchone()
                print "apres fetchone"
                self.idPersonne = data[0]
                self.ui.lineEditNom.setText(unicode(data[1]))
                self.ui.dateEditCreation.setDate(data[2])
                self.ui.lineEditSiege.setText(unicode(data[3]))
                self.ui.textEdit.setText(unicode(data[4]))
                self.ui.lineEditNomRepresentant.setText(data[8])
                if data[9] is not None:
                    self.idRepresentant = data[9]
                index = int(data[7]) - 1
                self.ui.comboBoxType.setCurrentIndex(index)
                print data
            except StandardError as e:
                print e

    def consultation(self, value):
        if value == 1:
            self.ui.lineEditSiege.setEnabled(False)
            self.ui.lineEditNom.setEnabled(False)
            self.ui.dateEditCreation.setEnabled(False)
            self.ui.btnOk.setEnabled(False)
            self.ui.textEdit.setEnabled(False)
            self.consulter = value
        elif value == 0 or value == 2:
            self.ui.lineEditSiege.setEnabled(True)
            self.ui.lineEditNom.setEnabled(True)
            self.ui.dateEditCreation.setEnabled(True)
            self.ui.btnOk.setEnabled(True)
            self.ui.textEdit.setEnabled(True)
            self.consulter = value
            print "modification ou ajout"
            if value == 0:
                self.viderChamps()
        manager = AccesManager.AccessManager(self, self.connection)
        manager.activate_widget("PERSONNE_MORALE/EDIT", self.ui.btnOk)

    def viderChamps(self):
        self.ui.lineEditSiege.clear()
        self.ui.lineEditNom.clear()
        self.ui.textEdit.clear()
        self.ui.dateEditCreation.setDate(QDate.currentDate())


    def initMasks(self):
        validatorAlpha = QRegExpValidator(globalvars.regexpAlpha)
        validatorAlphaNum = QRegExpValidator(globalvars.regexpAlphaNum)
        validatorNum = QRegExpValidator(globalvars.regexpNum)
        print "mask"

        self.ui.lineEditNom.setValidator(validatorAlphaNum)
        self.ui.lineEditSiege.setValidator(validatorAlphaNum)

    def messageErreur(self, message):
        self.isValid = True
        msgBox = QtGui.QMessageBox()
        msgBox.setText(message)
        msgBox.setModal(True)
        msgBox.show()
        msgBox.exec_()

    def getIdPersonne(self):
        return self.idPersonne