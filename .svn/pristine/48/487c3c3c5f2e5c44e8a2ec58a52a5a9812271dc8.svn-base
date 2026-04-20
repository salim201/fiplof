# -*- coding: utf-8 -*-
import os, os.path, sys
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *

from .limiteParcelle import Ui_Dialog
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class LimiteParcelleRun(QDialog):
    def __init__(self, connection):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setModal(True)
        self.connection = connection
        self.ui.btnAnnuler.clicked.connect(self.close)
        from .ListePointsCardinauxRun import ListePointsCardinauxRun
        self.listePtsCard = ListePointsCardinauxRun(self.connection)
        self.initActions()
        self.initDB()
        self.readPointsCardinaux()
        #self.idPointsCardinaux = []

    def initActions(self):
        self.ui.btnListe.clicked.connect(self.listerPtCard)
        self.listePtsCard.ui.BTEnregistrer.clicked.connect(self.savePtsCard)
        #self.comboBoxPosition.currentIndexChanged.connect(self.gererLimites)

    def listerPtCard(self):
        self.listePtsCard.show()
        result = self.listePtsCard.exec_()

    def initDB(self):
        self.cur = self.connection.cursor()

    def readPointsCardinaux(self):
        self.ui.comboBoxPosition.clear()
        self.cur.execute("SELECT idpointscardinaux, position FROM pointscardinaux ORDER BY idpointscardinaux")
        pointsCardinaux = self.cur.fetchall()
        self.idPointsCardinaux = []
        i = 0
        while i < len(pointsCardinaux):
            self.idPointsCardinaux.append(pointsCardinaux[i][0])
            self.ui.comboBoxPosition.addItem(_fromUtf8(pointsCardinaux[i][1]))
            i = i +1

    def savePtsCard(self):
        self.listePtsCard.ui.savePtsCard()
        self.readPointsCardinaux()
        self.listePtsCard.close()

    def readInput(self):
        data = {}
        data['idPointCardinal'] = self.idPointsCardinaux[self.ui.comboBoxPosition.currentIndex()]
        data['position'] = unicode(self.ui.comboBoxPosition.currentText()).encode('utf-8')
        data['description'] = unicode(self.ui.textEdit.toPlainText()).encode('utf-8')
        return data

    #def writeData(self, data):
        #Stocker les données dans un tableau au lieu de l'enregistrer dans la BDD
        #idLimite = None
        #lastid = self.cur.execute("INSERT INTO limitesparcelle (idpointscardinaux, description) VALUES (%s, %s) RETURNING idpointscardinaux", (data['idPointCardinal'], data['description']))
        #self.conn.commit()
        #print lastid

    #def getLastInsert(self):
        #self.cur.execute("SELECT idpointscardianux, description FROM limitesparcelle ORDER BY idpointscardianux DESC LIMIT 1")
        #data = self.cur.fetchone()

    def __del__(self):
        self.cur.close()

