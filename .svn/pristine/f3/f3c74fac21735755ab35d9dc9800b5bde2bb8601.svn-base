from PyQt4.QtGui import *
from PyQt4 import QtGui, QtCore
from qgis.core import *
from qgis.gui import *
import datetime, time

from .ConsultationLimites import Ui_Dialog

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class ConsultationLimitesRun(QDialog):
    def __init__(self, connection, idCertificat):
        QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Consultation Limites")
        self.connection = connection
        self.initDB()
        self.idCertificat = int(idCertificat)
        print "self.idCertificat = " + str(self.idCertificat)
        self.setModal(True)
        self.getAllLimites()

    def getAllLimites(self):
        self.cur.execute("select pc.idpointscardinaux, pc.position, pc.fanondroana, lp.description "
                         "from pointscardinaux pc, limitesparcelle lp, parcelle_d pd "
                         "WHERE lp.idparcelle = pd.gid "
                         "and lp.idpointscardinaux = pc.idpointscardinaux "
                         "and pd.idcertificat = %s", (self.idCertificat,))
        results = self.cur.fetchall()
        if results is not None:
            self.showInTable(results)

    def showInTable(self, data):
        self.ui.tableWidget.setRowCount(0)
        i = 0
        while i < len(data):
            rowPosition = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(rowPosition)
            #self.idPersonnePhysiques.append(data[i][0])
            j = 1
            while j < len(data[i]) :
                self.ui.tableWidget.setItem(rowPosition, j - 1, QtGui.QTableWidgetItem(unicode(data[i][j])))
                j = j + 1
            i = i + 1


    def initDB(self):
        self.cur = self.connection.cursor()

    def __del__(self):
        self.cur.close()