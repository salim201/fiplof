import os, os.path, sys
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *

from .PageHtml import Ui_Dialog


class PageHtmlRun(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.setModal(True)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.btnFermer.clicked.connect(self.close)