# coding: utf-8
import os, os.path, sys
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *

from .choixSurParcelleDemande import Ui_Dialog


class ChoixSurParcelleDmdRun(QDialog):
    def __init__(self, connection, canvas, parent):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.connection = connection
        self.canvas = canvas
        self.parent = parent
        self.newParcelleCF = self.parent.newParcelleCF
        self.fenRecherche = parent
        from .CreationInitialeRun import CreationInitialeRun
        self.creation = CreationInitialeRun(self.connection, self.canvas, parent)
        self.initActions()
        self.setModal(True)

    def initActions(self):
        self.ui.pushButton.clicked.connect(self.versCreation)
        self.ui.pushButton_2.clicked.connect(self.close)
        self.creation.ui.btnCreate.clicked.connect(self.certificatReady)

    def versCreation(self):
        if self.ui.radioButton.isChecked():
            print("nouvelle delimitation")
            self.parent.newParcelleCF = True
            self.fenRecherche.hide()

            self.hide()
            try:
                self.fenRecherche.parent.CreateNewParcelleCertificat(self.fenRecherche.iddemande,True)
            except StandardError as e:
                print e

            self.fenRecherche.close()
            self.close()
        elif self.ui.radioButton_2.isChecked():
            self.creation.show()
            result = self.creation.exec_()

    def certificatReady(self):
        self.creation.readInput()
        #self.creation.close()
        self.fenRecherche.close()
        self.close()
        #self.showAll()

    #def getDemandeNum(self, numDemande):
        #self.creation.getDemandeNum(numDemande)
