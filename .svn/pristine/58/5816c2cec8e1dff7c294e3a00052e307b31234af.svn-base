# coding: utf-8
from PyQt4.QtGui import *
from PyQt4 import Qt, QtGui, QtCore
from PyQt4.Qt import QApplication
from qgis.core import *
from qgis.gui import *
import datetime, time
import globalvars
import os
import webbrowser
import tempfile
from random import randint
from AreaConvert import AreaConvert
from Utils import Utils
from models.Demande import Demande
from  role_crl import Ui_Dialog
from models.RoleCrl import RoleCrl
import globalvars

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
class role_crlRun(QDialog):
    def __init__(self, parent, connection, edition):
        QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.connection = connection
        self.nomprenom=""
        self.titulaireornot=True
        RoleCrlModel = RoleCrl(connection)
        self.allroleCrl= RoleCrlModel.find_all()
        print self.allroleCrl
        from Personnes.ListePersonnePqueRun import ListePersonnePqueRun
        self.framepers = ListePersonnePqueRun(self.connection)
        self.framepers.ui.btnSelectionner.clicked.connect(self.selPersonne)
        self.crlrole,self.crltitulaire,self.crlsuppleant="","",""
        self.initDB()
        self.initActions()

    def initDB(self):
        self.cursor = self.connection.cursor()

    def initActions(self):
        print "test"
        for i, d in enumerate(self.allroleCrl):
            self.ui.comboBoxRoleCrl.addItem(d.libelle_role,d.id_role)
        self.ui.toolButtonajouttitualire.clicked.connect(self.opentitulaire)
        self.ui.toolButtonajoutsuppleant.clicked.connect(self.opensuppleant)
        #self.ui.pushButton.clicked.connect(self.ajoutclr)

    def opentitulaire(self):
        self.titulaireornot = True
        print self.titulaireornot
        try :
            self.framepers.exec_()
        except Exception as err:
            print err

    def opensuppleant(self):
        self.titulaireornot = False
        print self.titulaireornot
        try :
            self.framepers.exec_()
        except Exception as err:
            print err

    def selPersonne(self):
        print 'jfidfjkds'
        self.crlrole =self.ui.comboBoxRoleCrl.currentText()
        print self.framepers.getIdPersonne()
        try:
            self.cursor.execute("SELECT idpersonne,nompersonne,prenompersonne,numcipersonne,numactenaissancepersonne FROM personne WHERE idpersonne = %s", (self.framepers.idpersonne,))
            personne = self.cursor.fetchone()
            print " self.cursor.fetchone() "
            print personne
            nomper = str(personne[1])
            prenompers = str(personne[2])
            cinpers = str(personne[3])
            numactepers = str(personne[4])
            idpers = personne[0]
            self.nomprenom = nomper + '' + prenompers
            if len(cinpers) != 0:
                self.nomprenom = nomper + ' ' + prenompers + '- cin :' + cinpers
            else:
                self.nomprenom = nomper + ' ' + prenompers + '- copie ' + numactepers
            print "nomprenom"
            print  self.titulaireornot
            print  self.nomprenom
            if self.titulaireornot==True :
                self.ui.lineEditTitulaire.setText(self.nomprenom)
                self.crltitulaire=self.nomprenom
                globalvars.idpersrolTitulaire = self.framepers.idpersonne
            else :
                self.ui.lineEditSuppleant.setText(self.nomprenom)
                self.crlsuppleant= self.nomprenom
                globalvars.idpersrolSupleant = self.framepers.idpersonne
        except Exception as err:
                print err
                return
        self.framepers.close()