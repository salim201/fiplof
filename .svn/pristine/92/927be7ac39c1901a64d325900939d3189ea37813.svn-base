import os, os.path, sys
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *

from .typeCharge import Ui_Dialog

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class TypeChargeRun(QDialog):
    def __init__(self, connection):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setModal(True)
        self.setWindowTitle("Type des charges")
        self.connection = connection
        from .ServitudePassageRun import ServitudePassageRun
        self.servitude = ServitudePassageRun(connection)
        from .AutresChargesRun import AutresChargesRun
        self.autresCharges = AutresChargesRun(connection)
        from .HypothequesRun import HypothequesRun
        self.hypotheque = HypothequesRun(connection)
        #Cacher jusqu'a nouvel ordre
        self.ui.radioBtnServExistant.hide()
        self.ui.radioBtnNewServ.setChecked(True)
        self.initActions()

    def initActions(self):
        self.ui.btnOk.clicked.connect(self.choixCharges)
        self.ui.btnAnnuler.clicked.connect(self.close)

    def choixCharges(self):
        if self.ui.radioBtnNewServ.isChecked():
            self.servitude.show()
            self.servitude.exec_()
        if self.ui.radioBtnAutre.isChecked():
            self.autresCharges.show()
            self.autresCharges.exec_()
        if self.ui.radioBtnHypo.isChecked():
            self.hypotheque.show()
            self.hypotheque.exec_()
        if self.ui.radioBtnServExistant.isChecked():
            print "Servitude existant choisi"