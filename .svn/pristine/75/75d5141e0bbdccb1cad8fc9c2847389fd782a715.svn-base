from PyQt4.QtGui import *
from PyQt4 import QtGui, QtCore
import datetime, time

from .ConsultationCharges import Ui_Dialog

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class ChargesRun(QDialog):
    def __init__(self, connection, idCF = None):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setModal(True)
        self.idCertificat = idCF


        print("setup ui charges")
        self.connection = connection
        self.initDB()
        self.ui.btnAnnuler.clicked.connect(self.close)
        from .TypeChargeRun import TypeChargeRun
        self.typeCharge = TypeChargeRun(self.connection)
        self.idAutreCharges = []
        self.idServitude = []
        self.idHypotheque = []
        self.initActions()
        self.ui.btnDetailsServitude.hide()
        self.ui.btnDetailsHypotheque.hide()
        self.ui.btnDetailsAutre.hide()
        if self.idCertificat is not None:
            self.autreCharge()
            self.hypotheque()
            self.servitude()

    def initActions(self):
        self.ui.btnAjouter.clicked.connect(self.choixCharge)
        self.typeCharge.autresCharges.ui.btnOk.clicked.connect(self.traiterAutreCharges)
        self.typeCharge.servitude.ui.btnOk.clicked.connect(self.traiterNouvelleServitude)
        self.typeCharge.hypotheque.ui.btnOk.clicked.connect(self.traiterHypotheque)
        self.ui.btnEnleverAutre.clicked.connect(self.enleverAutreCharge)
        self.ui.btnEnleverHypotheque.clicked.connect(self.enleverHypotheque)
        self.ui.btnEnleverServitude.clicked.connect(self.enleverServitude)

    def choixCharge(self):
        self.typeCharge.show()
        result = self.typeCharge.exec_()

    def traiterAutreCharges(self):
        #self.ui.tableWidgetAutreCharge.setRowCount(0)
        self.typeCharge.autresCharges.readInput()
        if self.typeCharge.autresCharges.getLastInsert() not in self.idAutreCharges:
            self.idAutreCharges.append(self.typeCharge.autresCharges.getLastInsert())
        i = 0
        while i < len(self.idAutreCharges):
            try:
                self.cur.execute("select a.idcharge, a.descriptioncharge, a.dateinscriptionregistre "
                                 "FROM autrecharge a "
                                 "WHERE a.idcharge = %s ", (self.idAutreCharges[i],))
                results = self.cur.fetchone()
                rowPosition = self.ui.tableWidgetAutreCharge.rowCount()
                self.ui.tableWidgetAutreCharge.insertRow(rowPosition)
                j = 1
                while j < len(results):
                    if j == 2:
                        if results[j] is not None:
                            self.ui.tableWidgetAutreCharge.setItem(rowPosition, j - 1,
                                                                   QtGui.QTableWidgetItem(results[j].strftime('%d/%m/%Y')))
                    else:
                        if results[j] is not None:
                            self.ui.tableWidgetAutreCharge.setItem(rowPosition, j - 1,
                                                                   QtGui.QTableWidgetItem(unicode(results[j])))
                    j = j + 1
                i = i + 1
            except Exception as err:
                print err
                self.connection.rollback()

        self.typeCharge.autresCharges.close()
        self.typeCharge.close()

    def traiterNouvelleServitude(self):
        print "Traitement servitude"
        #self.ui.tableWidgetServitude.setRowCount(0)
        self.typeCharge.servitude.readInput()
        if self.typeCharge.servitude.getLastInsert() not in self.idServitude:
            self.idServitude.append(self.typeCharge.servitude.getLastInsert())
        print self.idServitude
        i = 0
        while i < len(self.idServitude):
            try:
                self.cur.execute("select s.idservitude, s.numeroservitude, s.descriptionservitude, s.dateinscription, s.origine, s.datelevee "
                             "FROM servitude s "
                             "WHERE s.idservitude = %s", (self.idServitude[i],))
                results = self.cur.fetchone()
                rowPosition = self.ui.tableWidgetServitude.rowCount()
                self.ui.tableWidgetServitude.insertRow(rowPosition)
                j = 1
                while j < len(results):
                    if j == 3 or j == 5:
                        if results[j] is not None:
                            self.ui.tableWidgetServitude.setItem(rowPosition, j - 1,
                                                                 QtGui.QTableWidgetItem(results[j].strftime('%d/%m/%Y')))
                    else:
                        if results[j] is not None:
                            self.ui.tableWidgetServitude.setItem(rowPosition, j - 1,
                                                                 QtGui.QTableWidgetItem(unicode(results[j])))
                    j = j + 1

            except StandardError as e:
                print e
                self.connection.rollback()
            i = i + 1

        self.typeCharge.servitude.close()
        self.typeCharge.close()

    def traiterHypotheque(self):
        #self.ui.tableWidgetHypotheque.setRowCount(0)
        print "traiter hypotheques"
        id = self.typeCharge.hypotheque.readInput()
        print "idhypotheque"
        print id
        print "fin idhypotheque"
        if id not in self.idHypotheque:
            self.idHypotheque.append(id)
        i = 0
        while i < len(self.idHypotheque):
            try:
                self.cur.execute("select h.idhypotheque, h.dateinscriptionregistre, h.valeur::money::numeric::float8, h.creancier, h.duree,  h.dateradiation "
                             "from hypotheque h "
                             "WHERE h.idhypotheque = %s ", (self.idHypotheque[i],))
                results = self.cur.fetchone()
                rowPosition = self.ui.tableWidgetHypotheque.rowCount()
                print rowPosition
                self.ui.tableWidgetHypotheque.insertRow(rowPosition)
                j = 1
                while j < len(results):
                    if j == 1 or j == 5:
                        print results[j]
                        if results[j] is not None:
                            self.ui.tableWidgetHypotheque.setItem(rowPosition, j - 1, QtGui.QTableWidgetItem(results[j].strftime('%d/%m/%Y')))
                    else:
                        #print _fromUtf8(data[j])
                        if results [j] is not None:
                            print results[j]
                            self.ui.tableWidgetHypotheque.setItem(rowPosition, j - 1, QtGui.QTableWidgetItem(unicode(results[j])))
                    j = j + 1
                i = i + 1
            except Exception as err:
                print err
                self.connection.rollback()

        self.typeCharge.hypotheque.close()
        self.typeCharge.close()

    def getIdAutreCharges(self):
        return self.idAutreCharges

    def getIdServitude(self):
        return self.idServitude

    def getIdHypotheque(self):
        return self.idHypotheque

    def autreCharge(self):
        print "autre charge"
        try:
            self.cur.execute("select a.idcharge, a.descriptioncharge, a.dateinscriptionregistre "
                                 "FROM autrecharge a, parcelle_d pd , autrechargesparcelle_d apd "
                                 "WHERE a.idcharge = apd.idcharge AND apd.idparcelle = pd.gid "
                                 "AND pd.idcertificat = %s",(self.idCertificat,))
            results = self.cur.fetchall()
            if results is not None:
                self.showInTableAutreCharge(results)
        except Exception as err:
            print err
            self.connection.rollback()


#######AFFICHAGE DES CHARGES EXISTANTES##########
    def hypotheque(self):
        print "hypoyheque"
        try:
            self.cur.execute("select h.idhypotheque, h.dateinscriptionregistre, h.valeur::money::numeric::float8, h.creancier, h.duree,  h.dateradiation "
                             "from hypotheque h, parcelle_d pd, hypothequeparcelle_d hpd "
                             "WHERE h.idhypotheque = hpd.idhypotheque AND hpd.idparcelle = pd.gid "
                             "AND pd.idcertificat = %s",(self.idCertificat,))
            results = self.cur.fetchall()
            #print results
            if results is not None:
                self.showInTableHypotheque(results)
        except Exception as err:
            print err
            self.connection.rollback()

    def servitude(self):
        print "servitude"
        try:
            self.cur.execute("select s.idservitude, s.numeroservitude, s.descriptionservitude, s.dateinscription, s.origine, s.datelevee "
                             "FROM servitude s, parcelle_d pd, servitudeparcelle_d spd "
                             "WHERE s.idservitude = spd.idservitude AND spd.idparcelle = pd.gid "
                             "AND pd.idcertificat = %s",(self.idCertificat,))
            results = self.cur.fetchall()
            if results is not None:
                self.showInTableServitude(results)
        except Exception as err:
            print err
            self.connection.rollback()

    def showInTableAutreCharge(self, data):
        self.idAutreCharges[:] = []
        #self.ui.tableWidgetAutreCharge.setRowCount(0)
        i = 0
        while i < len(data):
            self.idAutreCharges.append(data[i][0])
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
        #self.ui.tableWidgetHypotheque.setRowCount(0)
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
        #self.ui.tableWidgetServitude.setRowCount(0)
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

    def enleverAutreCharge(self):
        print "Enlever autre charge"
        reply = QMessageBox.question(self, "Confirmation",
                                         u"Etes vous sure de vouloir enlever cette charge?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            line = self.ui.tableWidgetAutreCharge.selectedItems()
            print line[0].row()
            self.idAutreCharges.pop(line[0].row())
            print self.idAutreCharges
            self.ui.tableWidgetAutreCharge.removeRow(line[0].row())
        else:
            return

    def enleverHypotheque(self):
        print "Enlever hypotheque"
        reply = QMessageBox.question(self, "Confirmation",
                                         u"Etes vous sure de vouloir enlever cette hypotheque?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            line = self.ui.tableWidgetHypotheque.selectedItems()
            print line[0].row()
            self.idHypotheque.pop(line[0].row())
            print self.idHypotheque
            self.ui.tableWidgetHypotheque.removeRow(line[0].row())
        else:
            return

    def enleverServitude(self):
        print "Enlever servitude"
        reply = QMessageBox.question(self, "Confirmation",
                                         u"Etes vous sure de vouloir enlever cette servitude?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            line = self.ui.tableWidgetServitude.selectedItems()
            print line[0].row()
            self.idServitude.pop(line[0].row())
            print self.idServitude
            self.ui.tableWidgetServitude.removeRow(line[0].row())
        else:
            return

#########FIN AFFICHAGE DES CHARGES EXISTANTES#######

    def initDB(self):
        self.cur = self.connection.cursor()

    def __del__(self):
        self.cur.close()