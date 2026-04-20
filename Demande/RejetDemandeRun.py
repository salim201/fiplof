import os
import sys
import os
import os.path
import psycopg2
import qgis
from PyQt4 import QtCore, QtGui
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtCore import QFileInfo
import time
import datetime, globalvars
import datetime
from datetime import date

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

import psycopg2
from psycopg2 import extras
from Utils import Utils
from PyQt4.QtCore import *



import qgis
import psycopg2
from qgis.core import *

from qgis.gui import *
import os
#from qgis.gui import QgisInterface
import psycopg2
import psycopg2.extras
#import  processing

import sys
from rejet import Ui_Rejet


class  RejetDemandeRun(QtGui.QDialog):
    def __init__(self,parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.iddemande = self.parent.iddemande
        self.connection = self.parent.connection

        self.connection = self.parent.connection

        print "id demande in"
        print self.iddemande
        print "id demande out"
        # Set up the user interface from Designer.
        self.ui = Ui_Rejet()
        self.ui.setupUi(self)
        self.initActions()

    def initActions(self):
        self.ui.pushButton_2.clicked.connect(self.save)

    def enregistrer(self):
        #if not self.check():
        #    return
        self.save()
        #self.accept()
        self.close()

    def check(self):
        if self.ui.nomLineEdit.text() == "":
            QtGui.QMessageBox.warning(self, "FIPLOF", "Veuillez remplir ce champ")
            self.ui.nomLineEdit.setFocus(Qt.Qt.OtherFocusReason)
            return False
        if self.ui.codeLineEdit.text() == "":
            QtGui.QMessageBox.warning(self, "FIPLOF", "Veuillez remplir ce champ")
            self.ui.codeLineEdit.setFocus(Qt.Qt.OtherFocusReason)
            return False
        return True


    def save(self):


        typeRejet = str(self.ui.typeRejetComboBox.currentText())
        dateRejet = self.ui.dateRejetDateEdit.text()
        dtR = dateRejet.split('/')
        DtRj = datetime.date(int(dtR[2]),int(dtR[1]), int(dtR[0]))
        motifRejet = str(self.ui.textEdit.toPlainText())
        cursor = self.connection .cursor()
        try:
            print " enter"
            exe = cursor.execute("INSERT INTO rejet (typerejet,daterejet,motifrejet)"
                                 " VALUES (%s,%s,%s) RETURNING idrejet ",
                (typeRejet,DtRj,motifRejet))
            self.connection.commit()
            print "after"
            idRejet = cursor.fetchone()[0]
            print "ligne rejet in"
            print idRejet

            #update Demande
            cursor.execute("UPDATE demande SET idrejet=(%s) WHERE iddemande = (%s)", (idRejet,self.iddemande))
            self.connection.commit()
        except:
            self.connection.rollback()
        cursor.close()
        print " cursor.close() "
        self.close()

