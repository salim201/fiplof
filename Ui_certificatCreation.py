from PyQt4 import QtCore, QtGui 
from certificatCreation import Ui_Dialog
# create the dialog for qgsPlof
class Ui_certificatCreation(QtGui.QDialog):
  def __init__(self):
    QtGui.QDialog.__init__(self)
    # Set up the user interface from Designer. 
    self.ui = Ui_Dialog ()
    self.ui.setupUi(self)