from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from .RechercheParcelle import Ui_Dialog

class RechercheParcelle(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        #self.parent = parent
        #print self.parent.txt
        self.ui.setupUi(self)
        self.initActions()

    def initActions(self):
        self.ui.checkBoxNumSection.stateChanged.connect(self.updateFieldsState)
        self.ui.checkBoxNomSection.stateChanged.connect(self.updateFieldsState)
        self.ui.checkBoxNumParcelle.stateChanged.connect(self.updateFieldsState)

    def updateFieldsState(self):
       self.ui.lineEditNumSection.setEnabled(self.ui.checkBoxNumSection.isChecked())
       self.ui.lineEditNomSection.setEnabled(self.ui.checkBoxNomSection.isChecked())
       self.ui.lineEditNumParcelle.setEnabled(self.ui.checkBoxNumParcelle.isChecked())
