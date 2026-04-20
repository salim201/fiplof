from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import psycopg2
from PyQt4 import Qt, QtGui
from .compteur import Ui_Dialog
import globalvars


class CompteurRun(QDialog):
    def __init__(self, connection, parent):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle(u"Compteur Demande et Certificat")
        self.connection = connection
        self.parent = parent
        self.initActions()
        self.initMasks()
        self.getCompteur()
        # self.ui.pushButtonConnexion.triggered.connect(self.checkAccessFIPLOF)

    def initActions(self):
        self.ui.pushButtonQuitter.clicked.connect(self.close)
        self.ui.pushButtonModifier.clicked.connect(self.writeData)

    def getCompteur(self):
        cursor = self.connection.cursor()
        #globalvars.id_commune
        try:
            cursor.execute("SELECT cptdemande, cptcertificat FROM commune WHERE idcommune = %s", (globalvars.id_commune,))
            res = cursor.fetchone()
            print res
            self.ui.lineEditCptDemande.setText(str(res[0]))
            self.ui.lineEditCptCF.setText(str(res[1]))
        except Exception as err:
            print (err)
            self.connection.rollback()

    def writeData(self):
        if self.ui.lineEditCptDemande.text() != '' and self.ui.lineEditCptCF.text() != '':
            cursor = self.connection.cursor()
            try:
                cursor.execute("UPDATE commune SET cptdemande = %s, cptcertificat = %s WHERE idcommune = %s", (str(self.ui.lineEditCptDemande.text()).strip(), str(self.ui.lineEditCptCF.text()).strip(), globalvars.id_commune))
                self.connection.commit()
            except Exception as err:
                print (err)

        self.close()

    def initMasks(self):
        validatorNum = QRegExpValidator(globalvars.regexpNum)

        self.ui.lineEditCptDemande.setValidator(validatorNum)
        self.ui.lineEditCptCF.setValidator(validatorNum)



