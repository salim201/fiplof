import os, os.path, sys
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *

from .opposition import Ui_Dialog


class OppositionRun(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.setModal(True)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.initActions()

    def initActions(self):
        self.ui.pushButtonFermer.clicked.connect(self.close)