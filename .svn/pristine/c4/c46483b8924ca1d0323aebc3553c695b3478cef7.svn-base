import os, os.path, sys, psycopg2, time, datetime
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *

from .ConsultationDemande import Ui_Dialog

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class ConsultationDmdRun(QDialog):
    def __init__(self, connection):
        QDialog.__init__(self)
        self.setModal(True)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.connection = connection
        self.initDB()
        self.initActions()
        from .OppositionsRun import OppositionsRun
        self.oppositions = OppositionsRun()
        from .DemandeursCertificatRun import DemandeursCertificatRun
        self.demandeurs = DemandeursCertificatRun()
        from .PageHtmlRun import PageHtmlRun
        self.html = PageHtmlRun()

    def initActions(self):
        self.ui.pushButton_2.clicked.connect(self.ouvrirOppositions)
        self.ui.pushButton.clicked.connect(self.ouvrirDemandeurs)
        self.ui.pushButton_4.clicked.connect(self.ouvrirExpHtml)
        self.ui.pushButton_3.clicked.connect(self.close)

    def ouvrirOppositions(self):
        self.oppositions.show()
        result = self.oppositions.exec_()

    def ouvrirDemandeurs(self):
        self.demandeurs.show()
        result = self.demandeurs.exec_()

    def ouvrirExpHtml(self):
        self.html.show()
        result = self.html.exec_()

    def getDemandeNum(self, numDemande):
        print numDemande
        self.ui.lineEditNumDemande.setText(numDemande)
        #SQL = "SELECT c.idcertificat, c.numerodemande, c.datereconnaissance, " \
              #"p.idparcelle, p.codeparcelle, p.idhameau, p.numeroparcelle," \
              #"h.idhameau, h.nomhameau, h.idfokontany," \
              #"f.idfokontany, f.idcommune, f.codefokontany, f.nomfokontany," \
              #"comm.idcommune, comm.iddistrict, comm.codecommune, comm.nomcommune, " \
              #"dist.iddistrict, dist.idregion, dist.codedistrict, dist.nomdistrict, " \
              #"reg.idregion, reg.coderegion, reg.nomregion," \
              #"cons.idconsistance, cons.libelleconsistance,  p.idconsistance " \
              #"FROM certificat c , parcelle p, hameau h, fokontany f , commune comm, district dist, region reg, consistance cons " \
              #"WHERE p.idcertificat = c.idcertificat " \
              #"AND p.idhameau = h.idhameau " \
              #"AND f.idfokontany = h.idfokontany " \
              #"AND comm.idcommune = f.idcommune " \
              #"AND comm.iddistrict = dist.iddistrict " \
              #"AND dist.idregion = reg.idregion " \
              #"AND cons.idconsistance = p.idconsistance " \
              #"AND numerodemande = %s;"

        SQL = "SELECT * FROM parcelle_d WHERE numdemande = %s "
        param = (numDemande,)
        self.cur.execute(SQL, param)
        data = self.cur.fetchall()
        print data
        self.showInfo(data)

    def showInfo(self, data):
        #self.ui.lineEditNumDemande.setText(data[0][3])
        if data[0][10]:
            self.ui.dateEditDateDemande.setText(data[0][10].strftime('%d/%m/%Y'))
        if data[0][11]:
            self.ui.dateEditDateReconnaissance.setText(data[0][11].strftime('%d/%m/%Y'))
        self.ui.comboBoxConsistance.clear()
        self.ui.comboBoxConsistance.addItem(data[0][17])
        self.ui.rGionComboBox.clear()
        self.ui.rGionComboBox.addItem(data[0][13])
        self.ui.districtComboBox.clear()
        self.ui.districtComboBox.addItem(data[0][14])
        self.ui.communeComboBox.clear()
        self.ui.communeComboBox.addItem(data[0][15])
        self.ui.fokontanyComboBox.clear()
        self.ui.fokontanyComboBox.addItem(data[0][16])
        self.ui.lineEditPrix.setText(_fromUtf8(str(data[0][12])))
        self.ui.lineEditEtat.setText(data[0][9])

    def initDB(self):
        self.cur = self.connection.cursor()
        # revenir au fichier de depart


    def __del__(self):
        self.cur.close()
