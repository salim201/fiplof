from PyQt4 import QtGui
from UiConfigGrid import Ui_Dialog


class ConfigGrid(QtGui.QDialog):
    def __init__(self, parent=0):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.init_actions()

    def init_actions(self):
        self.ui.pushButtonCancel.clicked.connect(self.reject)
        self.ui.pushButtonOK.clicked.connect(self.accept)

    def gridx(self):
        return self.ui.spinBoxGridX.value()

    def gridY(self):
        return self.ui.spinBoxGridY.value()
