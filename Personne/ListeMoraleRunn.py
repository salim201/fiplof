from PyQt4 import QtGui
from .ListeMorale import Ui_Dialog


class lmorale(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setModal(True)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.initActions()

    def initActions(self):
        self.ui.pushButtonFermer.clicked.connect(self.close)
        self.ui.checkBoxType.stateChanged.connect(self.updateFieldsStatus)
        self.ui.checkBoxDenomination.stateChanged.connect(self.updateFieldsStatus)

    def updateFieldsStatus(self):
        self.ui.comboBoxType.setEnabled(self.ui.checkBoxType.isChecked())
        self.ui.lineEditDenomination.setEnabled(self.ui.checkBoxDenomination.isChecked())