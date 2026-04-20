from PyQt4 import QtCore, QtGui 
from qgis.core import *
from qgis.gui import *
from listeCommunes import Ui_Dialog

class commune(QtGui.QDialog): 
  def __init__(self): 
    QtGui.QDialog.__init__(self) 
    # Set up the user interface from Designer. 
    self.ui = Ui_Dialog() 
#    self.parent = parent
#    print self.parent.txt
    self.ui.setupUi(self)
