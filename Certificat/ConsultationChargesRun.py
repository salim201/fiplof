from PyQt4.QtGui import *
from PyQt4 import QtGui, QtCore
from qgis.core import *
from qgis.gui import *
import datetime, time

from .ConsultationCharges import Ui_Dialog

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class ConsultationChargesRun(QDialog):
    def __init__(self, connection, idCertificat):
        QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Consultation charges")
        self.connection = connection
        self.initDB()
        self.idCertificat = int(idCertificat)
        print "self.idCertificat = " + str(self.idCertificat)
        self.setModal(True)
        self.ui.btnAjouter.hide()
        self.ui.btnValider.hide()
        self.ui.btnEnleverAutre.hide()
        self.ui.btnEnleverHypotheque.hide()
        self.ui.btnEnleverServitude.hide()
        self.ui.btnDetailsAutre.hide()
        self.ui.btnDetailsHypotheque.hide()
        self.ui.btnDetailsServitude.hide()
        self.ui.tableWidgetAutreCharge.setSelectionMode(1)
        self.ui.tableWidgetAutreCharge.setSelectionBehavior(1)
        self.ui.tableWidgetHypotheque.setSelectionMode(1)
        self.ui.tableWidgetHypotheque.setSelectionBehavior(1)
        self.ui.tableWidgetServitude.setSelectionMode(1)
        self.ui.tableWidgetServitude.setSelectionBehavior(1)
        self.idAutreCharge = []
        self.idHypotheque = []
        self.idServitude = []
        self.autreCharge()
        self.hypotheque()
        self.servitude()

    def autreCharge(self):
        print "autre charge"
        self.cur.execute("select a.idcharge, a.descriptioncharge, a.dateinscriptionregistre "
                             "FROM autrecharge a, parcelle_d pd , autrechargesparcelle_d apd "
                             "WHERE a.idcharge = apd.idcharge AND apd.idparcelle = pd.gid "
                             "AND pd.idcertificat = %s",(self.idCertificat,))
        results = self.cur.fetchall()
        if results is not None:
            self.showInTableAutreCharge(results)

    def hypotheque(self):
        print "hypoyheque"
        self.cur.execute("select h.idhypotheque, h.dateinscriptionregistre, h.valeur::money::numeric::float8, h.creancier, h.duree,  h.dateradiation "
                         "from hypotheque h, parcelle_d pd, hypothequeparcelle_d hpd "
                         "WHERE h.idhypotheque = hpd.idhypotheque AND hpd.idparcelle = pd.gid "
                         "AND pd.idcertificat = %s",(self.idCertificat,))
        results = self.cur.fetchall()
        #print results
        if results is not None:
            self.showInTableHypotheque(results)

    def servitude(self):
        print "servitude"
        self.cur.execute("select s.idservitude, s.numeroservitude, s.descriptionservitude, s.dateinscription, s.origine, s.datelevee "
                         "FROM servitude s, parcelle_d pd, servitudeparcelle_d spd "
                         "WHERE s.idservitude = spd.idservitude AND spd.idparcelle = pd.gid "
                         "AND pd.idcertificat = %s",(self.idCertificat,))
        results = self.cur.fetchall()
        if results is not None:
            self.showInTableServitude(results)

    def showInTableAutreCharge(self, data):
        self.idAutreCharge[:] = []
        self.ui.tableWidgetAutreCharge.setRowCount(0)
        i = 0
        while i < len(data):
            self.idAutreCharge.append(data[i][0])
            rowPosition = self.ui.tableWidgetAutreCharge.rowCount()
            self.ui.tableWidgetAutreCharge.insertRow(rowPosition)
            j = 1
            while j < len(data[i]):
                if j == 2:
                    if data[i][j] is not None:
                        self.ui.tableWidgetAutreCharge.setItem(rowPosition, j - 1,
                                                               QtGui.QTableWidgetItem(data[i][j].strftime('%d/%m/%Y')))
                else:
                    if data[i][j] is not None:
                        self.ui.tableWidgetAutreCharge.setItem(rowPosition, j - 1,
                                                               QtGui.QTableWidgetItem(unicode(data[i][j])))
                j = j + 1
            i = i + 1

    def showInTableHypotheque(self, data):
        self.idHypotheque[:] = []
        self.ui.tableWidgetHypotheque.setRowCount(0)
        i = 0
        while i < len(data):
            rowPosition = self.ui.tableWidgetHypotheque.rowCount()
            self.idHypotheque.append(data[i][0])
            self.ui.tableWidgetHypotheque.insertRow(rowPosition)
            j = 1
            while j < len(data[i]):
                if j == 1 or j == 5:
                    print data[i][j]
                    if data[i][j] is not None:
                        self.ui.tableWidgetHypotheque.setItem(rowPosition, j - 1, QtGui.QTableWidgetItem(data[i][j].strftime('%d/%m/%Y')))
                else:
                    #print _fromUtf8(data[j])
                    if data [i][j] is not None:
                        print data[i][j]
                        self.ui.tableWidgetHypotheque.setItem(rowPosition, j - 1, QtGui.QTableWidgetItem(unicode(data[i][j])))
                j = j + 1
            i = i + 1

    def showInTableServitude(self, data):
        self.idServitude[:] = []
        self.ui.tableWidgetServitude.setRowCount(0)
        i = 0
        while i < len(data):
            rowPosition = self.ui.tableWidgetServitude.rowCount()
            self.idServitude.append(data[i][0])
            self.ui.tableWidgetServitude.insertRow(rowPosition)
            j = 1
            while j < len(data[i]):
                if j == 3 or j == 5:
                    if data[i][j] is not None:
                        self.ui.tableWidgetServitude.setItem(rowPosition, j - 1,
                                                                 QtGui.QTableWidgetItem(data[i][j].strftime('%d/%m/%Y')))
                else:
                    if data[i][j] is not None:
                        self.ui.tableWidgetServitude.setItem(rowPosition, j - 1, QtGui.QTableWidgetItem(unicode(data[i][j])))
                j = j + 1
            i = i + 1

    def initDB(self):
        self.cur = self.connection.cursor()

    def __del__(self):
        self.cur.close()