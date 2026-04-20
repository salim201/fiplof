from PyQt4 import QtCore, QtGui 
from qgis.core import *
from qgis.gui import *
import os
import time
import datetime

from PyQt4 import QtGui, QtCore
import sys
import os
import os.path
import qgis
import psycopg2
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from PyQt4 import QtSql
from qgis.gui import *
from PyQt4 import QtGui, uic
from PyQt4.QtCore import *
import datetime
from datetime import *
from PyQt4 import QtGui, Qt
from Opposition import Ui_Opposition

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
class OppositionRunn(QtGui.QDialog): 

  def __init__(self,parent):
    QtGui.QDialog.__init__(self) 
    # Set up the user interface from Designer.

    self.clickID = ""
    self.row = 0
    self.column = 0
    self.opposition = []
    self.parent = parent
    self.connection = self.parent.connection
    self.idopposition = self.parent.idopposition
    self.iddemande = self.parent.iddemande
    self.ndemande = self.parent.numDemande
    self.dlg = ""
    self.ddDate = 0
    self.ui = Ui_Opposition(parent)
    self.ui.setupUi(self)


