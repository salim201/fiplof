import os, os.path, sys, time, datetime
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *

from .hypothques import Ui_Dialog

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class HypothequesRun(QDialog):
    def __init__(self, connection):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.connection = connection
        self.setModal(True)
        self.initDB()
        #self.initActions()


    def readInput(self):
        print "read input"
        data = {}
        data['dateinscriptionregistre'] = datetime.date(self.ui.dateEditInscription.date().year(), self.ui.dateEditInscription.date().month(), self.ui.dateEditInscription.date().day())
        print "apres date"
        data['duree'] = unicode(self.ui.lineEditDuree.text()).encode('utf-8')
        print "apres duree"
        data['valeur'] = float(self.ui.lineEditValeur.text())
        data['creancier'] = unicode(self.ui.lineEdit_4.text()).encode('utf-8')
        data['description'] = unicode(self.ui.textEditDesc.toPlainText()).encode('utf-8')
        data['dateradiation'] = datetime.date(self.ui.dateEditRadiation.date().year(), self.ui.dateEditRadiation.date().month(), self.ui.dateEditRadiation.date().day())
        value =  self.writeData(data)
        return value

    def initDB(self):
        self.cur = self.connection.cursor()

    def writeData(self, data):
        print "writeData"
        temp = data['description']
        data['description'] = str(temp).replace("'", "\'")
        temp = data['creancier']
        data['creancier'] = str(temp).replace("'", "\'")
        try:
            charge = self.cur.execute("INSERT INTO hypotheque (dateinscriptionregistre, duree, valeur, creancier, descriptionhypotheque, dateradiation) VALUES (%s, %s, %s, %s, %s, %s) returning idhypotheque", (data['dateinscriptionregistre'], data['duree'], data['valeur'], data['creancier'], data['description'], data['dateradiation'] ))
            self.connection.commit()
            id = self.cur.fetchone()
            return id[0]
        except StandardError as e:
            self.connection.rollback()
            print e
            return False

    #def getLastInsert(self):
        #print "get last insert"
        #try:
            #self.cur.execute("SELECT idhypotheque FROM hypotheque ORDER BY idhypotheque DESC LIMIT 1")
            #lastCharge = self.cur.fetchone()
            #return lastCharge[0]
        #except StandardError as e:
            #print e
            #return 0

    def __del__(self):
        self.cur.close()

