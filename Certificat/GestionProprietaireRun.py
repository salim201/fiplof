import os, os.path, sys
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *

from .gestionProprietaire import Ui_Dialog

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class GestionProprietaireRun(QDialog):
    def __init__(self, connection):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.connection = connection
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.idActe = 0
        #self.db_config = db_config
        from Personnes.PersonnePhysiqueRun import PersonnePhysiqueRun
        self.personne = PersonnePhysiqueRun(self.connection)
        from Personnes.ListePersonnePqueRun import ListePersonnePqueRun
        self.listePersonne = ListePersonnePqueRun(self.connection)
        from .ListePersonneMoraleRun import ListePersonneMoraleRun
        self.listePersonneMorale = ListePersonneMoraleRun(self.connection)
        from .PersonneMoraleRun import PersonneMoraleRun
        self.personneMorale = PersonneMoraleRun(self.connection)
        self.initActions()
        self.setModal(True)
        self.ui.horizontalGroupBox.hide()
        self.ui.radioButtonNouveau.hide()
        self.ui.radioButtonExistant.hide()
        self.ui.radioButtonExistant.setChecked(True)
        self.ui.radioButtonPersPhysique.setChecked(True)

    def initActions(self):
        self.ui.btnOk.clicked.connect(self.typePersonne)
        self.ui.btnAnnuler.clicked.connect(self.close)

    def typePersonne(self):
        if self.ui.radioButtonNouveau.isChecked():
            if self.ui.radioButtonPersPhysique.isChecked():
                self.ouvrirPersonnePhysique()
            elif self.ui.radioButtonPersMorale.isChecked():
                print "Nouvelle personne morale"
                self.ouvrirPersonneMorale()
        elif self.ui.radioButtonExistant.isChecked():
            if self.ui.radioButtonPersPhysique.isChecked():
                self.chercherPersonnePque()
            elif self.ui.radioButtonPersMorale.isChecked():
                self.chercherPersonneMorale()


    def ouvrirPersonnePhysique(self):
        try:
            self.personne.consultation(0)
            result = self.personne.exec_()
        except StandardError as e:
            print e

    def chercherPersonnePque(self):
        self.listePersonne.exec_()

    def chercherPersonneMorale(self):
        self.listePersonneMorale.exec_()

    def ouvrirPersonneMorale(self):
        print "fonction ouvrir personne morale"
        self.personneMorale.consultation(0)
        print "apres appel consultation"
        try:
            print "executer personne morale"
            self.personneMorale.exec_()
        except StandardError as e:
            print e