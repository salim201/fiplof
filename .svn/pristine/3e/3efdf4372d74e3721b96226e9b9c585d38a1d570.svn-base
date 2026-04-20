# coding: utf-8
from PyQt4.QtGui import *

from .listeLimites import Ui_Dialog
from PyQt4 import QtCore, QtGui
import psycopg2

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s



class ListeLimitesRun(QDialog):
    def __init__(self, connection, idCF = None, parent = None):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setModal(True)
        self.connection = connection
        self.initDB()
#        from LimiteParcelleRun import LimiteParcelleRun
#        self.limite = LimiteParcelleRun(self.connection)
        self.limitesParcelle = []
        self.idPointCardinaux = []
        self.ui.btnAnnuler.clicked.connect(self.close)
        self.idparcelle = None
        self.numDemande = None
        self.idCertificat = None
        if idCF is not None:
            self.idCertificat = int(idCF)
            self.showAllLimites()
        else:
            if parent is not None:
                self.numDemande = parent.numDemande
                self.showAllLimites()
        if parent is not None:
            self.idparcelle = parent.idParcelle

        self.fillComboPosition()
        self.initActions()

    def initActions(self):
        #self.ui.btnAjouter.clicked.connect(self.ouvrirLimiteParcelle)
        self.ui.btnSupprimerLimite.clicked.connect(self.deleteLimite)
        self.ui.btnAjoutLimite.clicked.connect(self.addLimite)
        #self.limite.ui.btnOk.clicked.connect(self.enregLimites)

#    def ouvrirLimiteParcelle(self):
#        self.limite.show()
 #       result = self.limite.exec_()

#    def enregLimites(self):
#        data = self.limite.readInput()
#        limiteActuel = []
#        for value in data.values():
#            limiteActuel.append(value)

#        self.limitesParcelle.append(limiteActuel)
        #lastLimite = self.limite.ui.getLastInsert()
#        rowPosition = self.ui.tableWidget.rowCount()
#        self.ui.tableWidget.insertRow(rowPosition)
#        i = 0
#        while i < len(limiteActuel)-1:
#            self.ui.tableWidget.setItem(rowPosition, i + 1, QtGui.QTableWidgetItem(_fromUtf8(limiteActuel[i + 1])))
#            i = i + 1

#        self.limite.close()
#        print self.limitesParcelle

 #   def getAllLimites(self):
 #       return self.limitesParcelle

    def showAllLimites(self):
        results = None
        if self.idCertificat is not None:
            try:
                self.cur.execute("select pc.idpointscardinaux, pc.position, lp.description "
                                 "from pointscardinaux pc, limitesparcelle lp, parcelle_d pd "
                                 "WHERE lp.idparcelle = pd.gid "
                                 "and lp.idpointscardinaux = pc.idpointscardinaux "
                                 "and pd.idcertificat = %s", (self.idCertificat,))
                results = self.cur.fetchall()

            except StandardError as e:
                print (e)
                self.connection.rollback()
        else:
            try:
                self.cur.execute("select pc.idpointscardinaux, pc.position, lp.description "
                "from pointscardinaux pc, limitesparcelle lp, parcelle_d pd "
                "WHERE lp.idparcelle = pd.gid "
                "and lp.idpointscardinaux = pc.idpointscardinaux "
                "and pd.numdemande = %s", (self.numDemande,))

                results = self.cur.fetchall()

            except StandardError as e:
                print (e)
                self.connection.rollback()

        if results is not None:
            self.showInTable(results)

#    def showInTable(self, data):
        #self.ui.tableWidget.setRowCount(0)
#        i = 0
 #       while i < len(data):
#            rowPosition = self.ui.tableWidget.rowCount()
 #           self.ui.tableWidget.insertRow(rowPosition)
 #           #self.idPersonnePhysiques.append(data[i][0])
#            j = 1
#            while j < len(data[i]) :
 #               self.ui.tableWidget.setItem(rowPosition, j - 1, QtGui.QTableWidgetItem(unicode(data[i][j])))
 #               j = j + 1
 #           i = i + 1


    def showInTable(self, data):
        self.ui.tableWidgetLimites.setRowCount(0)
        i = 0
        while i < len(data):
            rowPosition = self.ui.tableWidgetLimites.rowCount()
            self.ui.tableWidgetLimites.insertRow(rowPosition)
            #self.idPersonnePhysiques.append(data[i][0])
            j = 1
            while j < len(data[i]) :
                self.ui.tableWidgetLimites.setItem(rowPosition, j - 1, QTableWidgetItem(unicode(data[i][j])))
                j = j + 1
            i = i + 1

    def initDB(self):
        self.cur = self.connection.cursor()

    def addLimite(self):
        limiteparcelle = []
        limiteparcelle.append(self.idPointCardinaux[self.ui.positionComboBox.currentIndex()])
        #self.limitesParcelle.append(self.ui.positionComboBox.itemData(1))
        #print self.idsPositions
        rowPosition = self.ui.tableWidgetLimites.rowCount()
        # idpersonnes.append(data[i][0])
        #self.listeIdConsorts.append(self.currData[0])
        #print self.listeIdConsorts
        if self.ui.descriptionLineEdit.text() != "":
            limiteparcelle.append(unicode(self.ui.descriptionLineEdit.text()).encode('utf-8'))
            self.limitesParcelle.append(limiteparcelle)
            try:
                self.cur.execute("INSERT INTO limitesparcelle(idpointscardinaux, idparcelle, description) VALUES(%s, %s, %s)",
                                 (limiteparcelle[0], self.idparcelle, limiteparcelle[1]))
                self.connection.commit()
                self.ui.tableWidgetLimites.insertRow(rowPosition)
                self.ui.tableWidgetLimites.setItem(rowPosition, 0, QTableWidgetItem(self.ui.positionComboBox.currentText()))
                self.ui.tableWidgetLimites.setItem(rowPosition, 1, QTableWidgetItem(self.ui.descriptionLineEdit.text()))
            except psycopg2.Error as e:
                print(e)
                if e.pgcode == "23505":
                    QMessageBox.critical(self, u"Erreur", u"La combinaison position et parcelle existe déjà")
                    self.connection.rollback()
        else:
            QMessageBox.critical(self, "Erreur", u"Le champ description doit être renseigné")

        #print self.limitesParcelle

        self.ui.descriptionLineEdit.clear()

    def deleteLimite(self):
        if self.ui.tableWidgetLimites.currentRow() == -1:
            QMessageBox.critical(self, u"Suppression d'une limire", u"Veuillez au moins séléctionner une ligne dans le tableau")
        else:
            row = self.ui.tableWidgetLimites.currentRow()
            position = self.ui.tableWidgetLimites.item(row, 0).data(0).toString()
            try:
                self.cur.execute("SELECT idpointscardinaux FROM pointscardinaux WHERE position = %s", (str(position),))
                idPointCardinal = self.cur.fetchone()
                print idPointCardinal
                self.ui.tableWidgetLimites.removeRow(row)
                try:
                    self.cur.execute("DELETE FROM limitesparcelle WHERE idpointscardinaux = %s AND idparcelle = %s",
                                     (idPointCardinal[0],self.idparcelle))
                    self.connection.commit()
                    # afficher les limites sur la parcelle ##
                    try:
                        self.cur.execute(
                            "SELECT pc.idpointscardinaux, pc.position, l.description FROM limitesparcelle l, pointscardinaux pc WHERE l.idpointscardinaux = pc.idpointscardinaux AND l.idparcelle = %s",
                            (self.idparcelle,))
                        limites = self.cur.fetchall()
                        print limites
                        self.showInTable(limites)
                        for limite in limites:
                            if limite not in self.infosBatiments:
                                self.limitesParcelle.append(limite)
                        print self.limitesParcelle
                        self.showInTable(limites)
                    except StandardError as e:
                        self.connection.rollback()
                        print(e)
                        # self.showInTableBatiment()
                except StandardError as e:
                    self.connection.rollback()
                    print(e)
            except StandardError as e:
                self.connection.rollback()
                print(e)

            print position

    def showInTable(self, data):
        self.ui.tableWidgetLimites.setRowCount(0)
        i = 0
        while i < len(data):
            rowPosition = self.ui.tableWidgetLimites.rowCount()
            self.ui.tableWidgetLimites.insertRow(rowPosition)
            #self.idPersonnePhysiques.append(data[i][0])
            j = 1
            while j < len(data[i]) :
                self.ui.tableWidgetLimites.setItem(rowPosition, j - 1, QTableWidgetItem(unicode(data[i][j])))
                j = j + 1
            i = i + 1

    def fillComboPosition(self):
        self.ui.positionComboBox.clear()
        self.cur.execute("SELECT * FROM pointscardinaux")
        results = self.cur.fetchall()
        for result in results:
            self.idPointCardinaux.append(result[0])
            self.ui.positionComboBox.addItem(str(result[1]), result[0])



    def __del__(self):
        self.cur.close()
