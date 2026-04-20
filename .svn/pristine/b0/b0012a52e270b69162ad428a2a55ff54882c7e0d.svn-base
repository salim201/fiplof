# coding: utf-8
from PyQt4.QtGui import *
from PyQt4 import Qt, QtGui, QtCore
from PyQt4.Qt import QApplication
from .AvisImpotLangue import Ui_Dialog

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class AvisImpotLangueRunn (QDialog):
#    def __init__(self, connection, canvas, parent):
    def __init__(self, parent):
        QDialog.__init__(self)
        self.setModal(True)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle(u" CHOIX e")
        self.parent = parent
        self.initActions()

    def initActions(self):
        self.ui.pushButton_OK.clicked.connect(self.readInput)

    def readInput(self):
        langue='MALAGASY'
        if self.ui.radioButton_FR.isChecked():
            langue = 'FRENCH'
        self.hide()
        try:
            self.parent.doprintLangue(langue)  #Fiplof.CalculImpot.ListeAvisImpositionRun.ListeAvisImpositionRun
        except StandardError as e:
            print 'erreur ato hiditra am langue'
            print e
        self.close()