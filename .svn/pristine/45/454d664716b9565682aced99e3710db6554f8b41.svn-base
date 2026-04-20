from PyQt4.QtGui import *

from .DemandeursCertificat import Ui_Dialog


class DemandeursCertificatRun(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.setModal(True)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.initActions()

    def initActions(self):
        self.ui.pushButtonFermer.clicked.connect(self.close)