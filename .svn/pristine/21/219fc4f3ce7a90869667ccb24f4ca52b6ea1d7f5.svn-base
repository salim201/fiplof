from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from .RechercheDmdeTerrainDomaniale import Ui_Dialog

class RechercheDmdeTerrainDomaniale(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        #self.parent = parent
        #print self.parent.txt
        self.ui.setupUi(self)
        self.initActions()

    def initActions(self):
        self.ui.checkBoxNumDemande.stateChanged.connect(self.updateFieldsState)
        self.ui.checkBoxNomProprieteCible.stateChanged.connect(self.updateFieldsState)
        self.ui.checkBoxNomDemandeur.stateChanged.connect(self.updateFieldsState)

    def updateFieldsState(self):
        self.ui.lineEditNumDemande.setEnabled(self.ui.checkBoxNumDemande.isChecked())
        self.ui.lineEditNomProprieteCible.setEnabled(self.ui.checkBoxNomProprieteCible.isChecked())
        self.ui.lineEditNomDemandeur.setEnabled(self.ui.checkBoxNomDemandeur.isChecked())

