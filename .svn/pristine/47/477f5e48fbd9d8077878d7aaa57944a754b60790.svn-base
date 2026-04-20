import os, os.path, sys
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *

from VoirContribuable import Ui_Dialog


class VoirContribuableRun(QDialog):
    def __init__(self, connection):
        QDialog.__init__(self)
        print " VOIR LISTE CONTRIBUABLE"
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.connection = connection