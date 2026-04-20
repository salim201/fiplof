# coding: utf-8
from PyQt4.QtGui import *
from PyQt4 import Qt, QtGui, QtCore
from PyQt4.Qt import QApplication
from .num_debut_page import Ui_Dialog

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class NumDebut_PageRun(QDialog):
#    def __init__(self, connection, canvas, parent):
    def __init__(self, parent):
        QDialog.__init__(self)
        self.setModal(True)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle(u"Numéro début page du Registre")
        self.parent = parent
        self.ui.pushButton.clicked.connect(self.setNumPage)
        self.numPage = 1
        self.ui.spinBoxNumPageDebut.setValue(self.numPage)

    def setNumPage(self):
        self.numPage = self.ui.spinBoxNumPageDebut.value()
        self.parent.numDebutPage = self.numPage
        self.hide()
        self.parent.doPrint()
        self.close()
