from PyQt4 import QtCore, QtGui 
from .CreaDemande import Ui_CreationDemande
# create the dialog for qgsPlof
class Ui_CreateDemandeParcelle(QtGui.QDialog):
  def __init__(self,parent): 
    QtGui.QDialog.__init__(self) 
    # Set up the user interface from Designer. 
#    global iddmd
#    iddmd = iddemande
#    print parent.iddemande 
    dialog = self
    self.ui = Ui_CreationDemande(parent)
    self.parent = parent
    self.id_projet = self.parent.id_projet
    self.ui.setupUi(self)
#    print iddemande