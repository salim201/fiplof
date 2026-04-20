from PyQt4 import QtCore, QtGui 
#from RechercheDemandeCertificat import Ui_Dialog
from ConsultationDemande import Ui_Dialog

# create the dialog for qgsPlof
class rechercheDemande(QtGui.QDialog):
  def __init__(self): 
    QtGui.QDialog.__init__(self)
    self.setModal(True)
    self.ui = Ui_Dialog ()
    self.ui.setupUi(self)
    self.setModal(True)