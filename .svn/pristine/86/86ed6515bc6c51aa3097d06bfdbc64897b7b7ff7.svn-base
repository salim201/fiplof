# coding: utf-8
from PyQt4.QtGui import *
from PyQt4 import Qt, QtGui, QtCore
from PyQt4.Qt import QApplication
from qgis.core import *
from qgis.gui import *
import datetime, time
import globalvars
import os
import webbrowser
import tempfile
from random import randint
from AreaConvert import AreaConvert
from Utils import Utils
from  crl import Ui_Dialog

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
class CrlRun(QDialog):
    def __init__(self, connection, canvas, parent,slf = None):
        self.connection = connection
        QDialog.__init__(self)
        self.setModal(True)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.canvas = canvas
        self.initDB()

    def initDB(self):
        self.cursor = self.connection.cursor()

