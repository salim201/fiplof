# -*- coding: utf-8 -*-

import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.core import *
from qgis.gui import *

from ..BatchDemandeRun import BatchDemandeRun
from ..ListeDossierExterneRun import ListeDossierExterneRun
from ..EnvoiMiseAJourRun import EnvoiMiseAJourRun
from ..SuiviRun import SuiviRun
from ..db_utils import connection_is_broken, reconnect_connection

class BatchDemandeController:
    def __init__(self, parent):
        print("--------------------------------------akfopdfdjfdsjfdsfdsfds-----------------------------")
        self.parent = parent
        self.connection = parent.connection

    def _ensureConnection(self):
        if connection_is_broken(self.connection):
            print("Connexion BD perdue, reconnexion en cours...")
            self.connection = reconnect_connection()
            self.parent.connection = self.connection

          
    def showBatchDemande(self):
        """Affiche la fenêtre de batch demande"""
        try:
            self._ensureConnection()
            print("Batch Demande - Interopérabilité")
            batchDialog = BatchDemandeRun(self.connection)
            batchDialog.exec_()
        except Exception as er:
            print("Erreur dans batchDemande:", str(er))
            
    def getBatchDemandeInstance(self):
        """Retourne une instance de BatchDemandeRun"""
        self._ensureConnection()
        return BatchDemandeRun(self.connection)

    def showListeDossierATransformer(self):
        """Affiche la fenêtre de batch demande"""
        try:
            self._ensureConnection()
            print("Liste  Dossier à transformer - Interopérabilité")
            batchDialog = ListeDossierExterneRun(self.connection)
            batchDialog.exec_()
        except Exception as er:
            print("Erreur dans batchDemande:", str(er))

    def showEnvoiMiseAJour(self):
        """Affiche la fenêtre d'envoi mise à jour"""
        try:
            self._ensureConnection()
            print("Envoi Mise à Jour - Interopérabilité")
            dialog = EnvoiMiseAJourRun(self.connection)
            dialog.exec_()
        except Exception as er:
            print("Erreur dans envoiMiseAJour:", str(er))

    def showSuivi(self):
        """Affiche la fenêtre de suivi"""
        try:
            self._ensureConnection()
            print("Suivi - Interopérabilité")
            dialog = SuiviRun(self.connection)
            dialog.exec_()
        except Exception as er:
            print("Erreur dans showSuivi:", str(er))
  