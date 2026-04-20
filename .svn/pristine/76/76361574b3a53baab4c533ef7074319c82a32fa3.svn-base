from PyQt4 import QtGui
from .PersonnePhysique import Ui_PersonnePhysique


class PersonneRunn(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setModal(True)
        self.ui = Ui_PersonnePhysique()
        self.ui.setupUi(self)
        self.initActions()

    def initActions(self):
        self.ui.BTAnnuler.clicked.connect(self.close)
        self.ui.radioButtonRien.clicked.connect(self.updateFieldsState)
        self.ui.radioButtonCIN.clicked.connect(self.updateFieldsState)
        self.ui.radioButtonAN.clicked.connect(self.updateFieldsState)

    def updateFieldsState(self):
        cinEnabled = self.ui.radioButtonCIN.isChecked()
        anEnabled = self.ui.radioButtonAN.isChecked()
        self.ui.lineEditCIN1.setEnabled(cinEnabled)
        self.ui.lineEditCIN2.setEnabled(cinEnabled)
        self.ui.lineEditCIN3.setEnabled(cinEnabled)
        self.ui.lineEditCIN4.setEnabled(cinEnabled)
        self.ui.dateEditCIN.setEnabled(cinEnabled)
        self.ui.lineEditLieuCIN.setEnabled(cinEnabled)
        self.ui.lineEditNumeroAN.setEnabled(anEnabled)
        self.ui.dateEditAN.setEnabled(anEnabled)
        self.ui.lineEditLieuAN.setEnabled(anEnabled)