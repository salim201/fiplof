from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from .Proprio import Ui_Dialog

class Proprio(QtGui.QDialog):
    def __init__(self,parent):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.parent = parent
#       print self.parent.txt
        self.id_projet = self.parent.id_projet
        self.connection = self.parent.connection
        #self.connection = self.parent.connection
        #self.cur = self.parent.connection.cursor()
        self.ui.setupUi(self)
        self.initActions()

    def initActions(self):

        validator = QtGui.QDoubleValidator()
        #self.ui.lineEditNumDecision.setValidator(validator)
        #self.ui.lineEditNumDecision.setValidator(validator)

        #self.ui.dateEditDecision.setDisplayFormat("dd/MM/yyyy")
        #self.ui.dateEditDecision.setDate(QDate.currentDate())

        self.ui.add.clicked.connect(self.gestionProprio)
        self.ui.detailsAncien.clicked.connect(self.PersonneDetails)

        #self.ui.btnOk.clicked.connect(self.enregistrer)


    def PersonneDetails(self):
        from .PersonnePhysiqueRun import PersonnePhysique
        GP = PersonnePhysique(self.parent)
        GP.exec_()

    def gestionProprio(self):
        from Certificat.GestionProprietaireRun import GestionProprietaireRun
        GP = GestionProprietaireRun(self.connection)
        GP.exec_()

    def enregistrer(self):
        print "enregistrer"
        if not self.check():
            return

        self.save()
        self.accept()


    def check(self):
        print "demande"


    def save(self):

        import time
        import datetime
        try:
            print "try in"
        except Exception as e:
            print e





