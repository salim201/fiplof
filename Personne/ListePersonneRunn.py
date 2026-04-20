from PyQt4 import QtGui
from .ListePersonne import Ui_Dialog



class listePersonne(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setModal(True)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.initActions()

    def initActions(self):
        self.ui.pushButtonFermer.clicked.connect(self.close)
        self.ui.pushButtonAjouter.clicked.connect(self.openPhysique)
        self.ui.checkBoxNom.stateChanged.connect(self.updateFieldsState)
        self.ui.checkBoxPrenom.stateChanged.connect(self.updateFieldsState)
        self.ui.checkBoxNomPere.stateChanged.connect(self.updateFieldsState)
        self.ui.checkBoxNomMere.stateChanged.connect(self.updateFieldsState)
        self.ui.radioButtonCIN.clicked.connect(self.updateFieldsState)
        self.ui.radioButtonActe.clicked.connect(self.updateFieldsState)
        self.ui.radioButtonRien.clicked.connect(self.updateFieldsState)

    def updateFieldsState(self):
        self.ui.lineEditNom.setEnabled(self.ui.checkBoxNom.isChecked())
        self.ui.lineEditPrenom.setEnabled(self.ui.checkBoxPrenom.isChecked())
        self.ui.lineEditNomPere.setEnabled(self.ui.checkBoxNomPere.isChecked())
        self.ui.lineEditNomMere.setEnabled(self.ui.checkBoxNomMere.isChecked())
        cinEnabled = self.ui.radioButtonCIN.isChecked()
        self.ui.lineEditCIN1.setEnabled(cinEnabled)
        self.ui.lineEditCIN2.setEnabled(cinEnabled)
        self.ui.lineEditCIN3.setEnabled(cinEnabled)
        self.ui.lineEditCIN4.setEnabled(cinEnabled)
        self.ui.lineEditActe.setEnabled(self.ui.radioButtonActe.isChecked())

    def openPhysique(self):
        from .PersonneRunn import PersonneRunn
        P = PersonneRunn()
        P.show()
        result = P.exec_()