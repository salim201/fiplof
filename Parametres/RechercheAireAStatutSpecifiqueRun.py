from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from .RechercheAireAStatutSpecifique import Ui_Dialog

class RechercheAireAStatutSpecifique(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
    #    self.parent = parent
    #    print self.parent.txt
        self.ui.setupUi(self)
        self.initActions()

    def initActions(self):
        self.ui.btnListe.clicked.connect(self.ouvrirListeTypeAire)
        self.ui.checkBoxType.stateChanged.connect(self.updateFieldsState)
        self.ui.checkBoxNom.stateChanged.connect(self.updateFieldsState)

    def ouvrirListeTypeAire(self):
        from .ListeTypesAireRun import ListeTypesAire
        liste = ListeTypesAire()
        liste.exec_()

    def updateFieldsState(self):
        self.ui.comboBoxType.setEnabled(self.ui.checkBoxType.isChecked())
        self.ui.lineEditNom.setEnabled(self.ui.checkBoxNom.isChecked())


