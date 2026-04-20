#coding: utf-8
from PyQt4.QtGui import *
from PyQt4 import QtGui, QtCore
from qgis.core import *
from qgis.gui import *
import datetime, time, os, sys
import globalvars, psycopg2

from .modeedition import Ui_Dialog


class modeeditionRun(QDialog):
    def __init__(self, connection,canvas, parent):
        self.connection = connection
        QDialog.__init__(self)
        self.setModal(True)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.canvas = canvas
        self.registry = parent.registry
        #self.shape_prop_titre = parent.shape_prop_titre
        self.parent = parent
        self.tool = parent.tool
        #self.idaire = parent.idAire
        #self.filenamepreview = ""
        #self.ui.btnCreer.setText("Modifier les informations")
        self.senderName = self.sender().objectName()
        self.ui.radioButton.setChecked(True)
        #self.initDB()
        self.initActions()
        #self.initPreview()
        #self.readData()
        #if edit == 0:
            #self.ui.btnCreer.hide()

    def initActions(self):
        self.ui.pushButton_2.clicked.connect(self.close)
        self.ui.pushButton.clicked.connect(self.choixEdition)

    def choixEdition(self):
        if self.senderName == "actionEdition_3": #Action edition des aire a statuts specifiques
            if self.ui.radioButton.isChecked(): #edition des informations
                from RecherchePropositionAireRun import RecherchePropositionAire
                proposition = RecherchePropositionAire(self.connection, self.canvas, self, 1)
                proposition.exec_()
            elif self.ui.radioButton_2.isChecked(): #Edition de la geometrie
                from RecherchePropositionAireRun import RecherchePropositionAire
                proposition = RecherchePropositionAire(self.connection, self.canvas, self, 2)
                proposition.exec_()

        elif self.senderName == "actionEdition_2":
            if self.ui.radioButton.isChecked():
                from RecherchePropositionDomaineRun import RecherchePropositionDomaine
                domaine = RecherchePropositionDomaine(self.connection, self.canvas, self, 1)
                domaine.exec_()
            elif self.ui.radioButton_2.isChecked():
                from RecherchePropositionDomaineRun import RecherchePropositionDomaine
                domaine = RecherchePropositionDomaine(self.connection, self.canvas, self, 2)
                domaine.exec_()

        elif self.senderName == "actionEdition":
            if self.ui.radioButton.isChecked():
                from RecherchePropositionTitreRun import RecherchePropositionTitre
                titre = RecherchePropositionTitre(self.connection, self.canvas, self, 1)
                titre.exec_()
            elif self.ui.radioButton_2.isChecked():
                from RecherchePropositionTitreRun import RecherchePropositionTitre
                titre = RecherchePropositionTitre(self.connection, self.canvas, self, 2)
                titre.exec_()
        self.close()

