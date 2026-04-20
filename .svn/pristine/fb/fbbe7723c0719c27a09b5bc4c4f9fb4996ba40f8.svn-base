import os, os.path, sys
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *

from .oppositions import Ui_Dialog


class OppositionsRun(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.setModal(True)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.initActions()

    def initActions(self):
        self.ui.pushButton.clicked.connect(self.ouvrirOpposition)
        self.ui.pushButton_2.clicked.connect(self.close)

    def ouvrirOpposition(self):
        from .OppositionRun import OppositionRun
        opposition = OppositionRun()
        result = opposition.exec_()