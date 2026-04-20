import os
import sys
import os
import os.path
import psycopg2
import qgis
#from qgis.utils import iface
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
from qgis.gui import *
import time
import datetime
import globalvars
from PyQt4 import QtGui, Qt
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, Qt
from PyQt4 import QtCore, QtGui
from PyQt4 import QtGui, Qt
from PyQt4 import Qt, QtGui
import psycopg2
from psycopg2 import extras
from Utils import Utils
from PyQt4.QtCore import *
import globalvars

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

from ReglementForm import Ui_Reglement

class Reglement(QtGui.QDialog):

  def __init__(self,parent):
    QtGui.QDialog.__init__(self)
    # Set up the user interface from Designer.
    self.parent = parent
    self.ui = Ui_Reglement()
    self.ui.setupUi(self)
    self.coddistrict = 0
    self.codecommune = 0
    self.idfokontany = 0
    self.iddemande = 0
    self.idopposition = self.parent.idopposition
    self.connection = ""
    self.ddDate = 0
    self.connection = self.parent.connection
    self.cursor = self.connection.cursor()
    self.gid = self.parent.gid
    self.ui.dateReglementDateEdit.setDisplayFormat("dd/MM/yyyy")
    self.ui.dateReglementDateEdit.setDate(QDate.currentDate())
    #        self.dateDemandeLineEdit.setInputMask(_fromUtf8(""))
    self.ui.dateReglementDateEdit.setEnabled(True)
    self.ui.dateReglementDateEdit.setCalendarPopup(True)
    self.ui.save.clicked.connect(self.add)
    self.etatopposition = 1
    self.setModal(True)


  def add(self):
      import sys
      reload(sys)
      sys.setdefaultencoding('utf8')
      nature = str(self.ui.natureComboBox.currentText())
      description = str(self.ui.textEdit.toPlainText())
      self.dateRegle = str(self.ui.dateReglementDateEdit.text())
      dtOpp = self.dateRegle.split('/')
      dateReglement = datetime.date(int(dtOpp[2]), int(dtOpp[1]), int(dtOpp[0]))
      print "add"
      try:
          self.cursor.execute("UPDATE oppositions  SET etatopposition = %s, datereglement = %s, naturereglement =  %s, descriptionreglement = %s WHERE idopposition = %s",(self.etatopposition,dateReglement,nature,description, str(self.idopposition)))
          self.connection.commit()

          msgBox = QtGui.QMessageBox()
          msgBox.setText("Modficiation  reussi")
          self.parent.loadOpposition(self.connection)
      except Exception as err:
          print err
          self.connection.rollback()
      self.close()

