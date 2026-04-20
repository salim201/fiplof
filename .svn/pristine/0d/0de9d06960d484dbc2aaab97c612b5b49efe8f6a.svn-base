from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from .ChoixTypeActe import Ui_Dialog

class ChoixTypeActe(QtGui.QDialog):
    def __init__(self,parent):
        print "init acte run"
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.parent = parent
        self.idActe = 0
        self.IdActePublic = 0
        self.IdActeDeces = 0
        self.IdActePrivee = 0
        self.idDecision = 0
        self.IdActePublic = 0
        self.details = []
#       print self.parent.txt
        self.id_projet = self.parent.id_projet
        self.connection = self.parent.connection
        self.ui.setupUi(self)
        self.ui.radioButtonActePublic.setChecked(True)
        self.ui.radioButtonNouveau.setChecked(True)
        self.initActions()

    def initActions(self):
        self.ui.btnOk.clicked.connect(self.typeActe)
        self.ui.btnAnnuler.clicked.connect(self.close)

    def typeActe(self):
        if self.ui.radioButtonNouveau.isChecked():
            if self.ui.radioButtonActePrive.isChecked():
                self.ouvrirActePrive()
            elif self.ui.radioButtonActePublic.isChecked():
                print "Nouvelle personne morale"
                self.ouvrirActePublic()
        elif self.ui.radioButtonExistant.isChecked():
            if self.ui.radioButtonActePrive.isChecked():
                self.chercherActePrive()
            elif self.ui.radioButtonActePublic.isChecked():
                self.chercherActePublic()


    def ouvrirActePrive(self):
        from .ActePriveRun import ActePrive
        acte = ActePrive(self)
        acte.exec_()

    def chercherActePublic(self):
        from .ListeActePublicsRun import ListeActePublics
        listeacte = ListeActePublics(self)
        listeacte.exec_()

    def chercherActePrive(self):
        from .ListeActePrivesRun import ListeActePrives
        listeacte = ListeActePrives(self)
        listeacte.exec_()

    def ouvrirActePublic(self):
        from .ActePublicsRun import ActePublic
        acte = ActePublic(self)
        acte.exec_()