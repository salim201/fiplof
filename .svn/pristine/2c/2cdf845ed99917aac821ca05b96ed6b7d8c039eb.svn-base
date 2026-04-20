from PyQt4 import QtGui, QtCore
from .piece_identification import Ui_Form

class PieceIdentificationWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(PieceIdentificationWidget, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.updateFieldsStatus()
        self.initActions()

    def initActions(self):
        self.ui.radioButtonCIN.clicked.connect(self.updateFieldsStatus)
        self.ui.radioButtonActe.clicked.connect(self.updateFieldsStatus)
        self.ui.radioButtonRien.clicked.connect(self.updateFieldsStatus)

    def updateFieldsStatus(self):
        self.ui.tab.setEnabled(self.ui.radioButtonCIN.isChecked())
        self.ui.tab_2.setEnabled(self.ui.radioButtonActe.isChecked())
        if (self.ui.radioButtonCIN.isChecked()):
            self.ui.tabWidget.setCurrentWidget(self.ui.tab)
        if(self.ui.radioButtonActe.isChecked()):
            self.ui.tabWidget.setCurrentWidget(self.ui.tab_2)