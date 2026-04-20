from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from .RecherchePerimetreCadastre import Ui_Dialog

class RecherchePerimetreCadastre(QtGui.QDialog):
    def __init__(self):
      QtGui.QDialog.__init__(self)
    #   Set up the user interface from Designer.
      self.ui = Ui_Dialog()
#     self.parent = parent
#     print self.parent.txt
      self.ui.setupUi(self)
      self.initActions()

    def initActions(self):
        self.ui.checkBoxNomOperation.stateChanged.connect(self.updateFieldsState)
        self.ui.checkBoxNumArrete.stateChanged.connect(self.updateFieldsState)

    def updateFieldsState(self):
        self.ui.lineEditNomOperation.setEnabled(self.ui.checkBoxNomOperation.isChecked())
        self.ui.lineEditNumArrete.setEnabled(self.ui.checkBoxNumArrete.isChecked())