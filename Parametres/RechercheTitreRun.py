from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from .RechercheTitre import Ui_Dialog
import globalvars

class RechercheTitre(QtGui.QDialog):
    def __init__(self, connection):
        QtGui.QDialog.__init__(self)
    #   Set up the user interface from Designer.
        self.ui = Ui_Dialog()
#       self.parent = parent
#       print self.parent.txt
        self.ui.setupUi(self)
        self.connection = connection
        self.initActions()
        self.initDB()
        self.titrePath = self.getShapepath()
        print self.titrePath

    def initActions(self):
        self.ui.checkBoxNumTitre.stateChanged.connect(self.updateFieldsState)
        self.ui.checkBoxNomPropriete.stateChanged.connect(self.updateFieldsState)
        self.ui.checkBoxNomProprietaire.stateChanged.connect(self.updateFieldsState)

    def updateFieldsState(self):
        self.ui.lineEditNumTitre.setEnabled(self.ui.checkBoxNumTitre.isChecked())
        self.ui.lineEditNomPropriete.setEnabled(self.ui.checkBoxNomPropriete.isChecked())
        self.ui.lineEditNomProprietaire.setEnabled(self.ui.checkBoxNomProprietaire.isChecked())

    def initDB(self):
        self.cur = self.connection.cursor()

    def __del__(self):
        self.cur.close()
        #vtlayer = self.registry.mapLayersByName("Demandes Parcelle")[0]
        #self.canvas.setCurrentLayer(vtlayer)

    def getShapepath(self):
        try:
            self.cur.execute("SELECT pc.fichier FROM projetcouche pc, projet_commune pcm  WHERE pc.idprojet_commune = pcm.idprojet_commune AND pcm.idprojet = %s AND pcm.idcommune = %s AND pc.libelle = 'Titre Foncier' ",
                             (globalvars.id_projet, globalvars.id_commune))
            filePath = self.cur.fetchone()
            print globalvars.id_projet
            print globalvars.id_commune
            print filePath
            return filePath[0]
        except StandardError as e:
            print(e)
            self.connection.rollback()
            return

