# coding: utf8
from PyQt4 import QtGui
from .AffichageCollectif import Ui_Dialog
import psycopg2
import psycopg2.extras
from Configuration import DbConfig

class AffichageCollectifRun(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setModal(True)
        config = DbConfig.DbConfig()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.initActions()
        self.connection = psycopg2.connect(database=config.db_name, user=config.db_user, password=config.db_pass,
                                           host=config.db_host)
        self.ui.territoire.fill(self.connection)


    def initActions(self):
        self.ui.pushButtonFermer.clicked.connect(self.close)
        self.ui.checkBoxNomDemandeur.stateChanged.connect(self.updateFieldsStatus)
        self.ui.checkBoxNumeroDemande.stateChanged.connect(self.updateFieldsStatus)
        self.ui.checkBoxDateDemande.stateChanged.connect(self.updateFieldsStatus)
        self.ui.checkBoxEtat.stateChanged.connect(self.updateFieldsStatus)

    def updateFieldsStatus(self):
        self.ui.lineEditNomDemandeur.setEnabled(self.ui.checkBoxNomDemandeur.isChecked())
        self.ui.lineEditNumeroDemande.setEnabled(self.ui.checkBoxNumeroDemande.isChecked())
        self.ui.dateEditDateDemande.setEnabled(self.ui.checkBoxDateDemande.isChecked())
        self.ui.comboBoxEtat.setEnabled(self.ui.checkBoxEtat.isChecked())