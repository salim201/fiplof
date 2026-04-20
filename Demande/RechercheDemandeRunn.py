import os
import sys
import os
import os.path
import psycopg2
from PyQt4 import QtCore, QtGui

#from RechercheDemandeCertificat import Ui_Dialog
from ConsultationDemande import Ui_Dialog

# create the dialog for qgsPlof
class rechercheDemande(QtGui.QDialog):
  def __init__(self,parent,stateEdition = 0):
    QtGui.QDialog.__init__(self)
    self.setModal(True)
    self.parent = parent
    self.id_projet = self.parent.id_projet
    self.ui = Ui_Dialog (parent,stateEdition)
    self.ui.setupUi(self)
    self.setModal(True)

