# coding: utf-8
from PyQt4.QtGui import *
from PyQt4 import QtGui, QtCore
from qgis.core import *
from qgis.gui import *

from .EditionContribuable import Ui_Dialog

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s



class EditionConsorts(QDialog):
    def __init__(self, connection, idparcelle =None, edition = 0, parent = None):
        QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.connection = connection
        #self.idPersonnePhysiques = []
        #self.idPersonneMorales = []
        self.initDB()
        self.idparcelle = idparcelle
        self.setModal(True)
        self.edition = edition
        self.idPersonnesPhysiques = []
        self.idPersonnesMorales = []
        self.idpersonne = None
        self.idpersonnePque = None
        self.proprioPrincipale = None
        self.setWindowTitle("Edition Contribuable")
        if parent is not None:
            self.idContribuable = parent.idContribuable
            print "id contribuable to edit " + str(self.idContribuable)
        else:
            self.idContribuable = None
            print "id contribuable to edit " + str(self.idContribuable)

        from Personnes.PersonnePhysiqueRun import PersonnePhysiqueRun
        self.personne = PersonnePhysiqueRun(self.connection)

        self.initActions()
        self.ui.tableWidgetPhysique.setSelectionMode(1)
        self.ui.tableWidgetPhysique.setSelectionBehavior(1)
        self.proprietairePhysiques()

    def initActions(self):
        if self.edition != 0:
            self.ui.pushButtonAjouter.clicked.connect(self.ouvrirListePersPque)
            #self.proprio.listePersonneMorale.ui.pushButton_5.clicked.connect(self.getIdPersonneMorale)
            #self.proprio.personne.ui.btnOk.clicked.connect(self.enregistrerPersonnePque)
            #self.proprio.personneMorale.ui.btnOk.clicked.connect(self.enregistrerPersonneMorale)
            self.ui.pushButtonEnleverProprioPpque.clicked.connect(self.enleverProprietairePque)
        self.ui.pushButtonAnnuler.clicked.connect(self.close)
        self.ui.pushButtonDetailsPhysique.clicked.connect(self.detailPersonnePque)
        self.ui.tableWidgetPhysique.cellClicked.connect(self.selectionLigne)
        #self.ui.tableWidgetMorale.cellClicked.connect(self.selectionLigneMorale)

    def proprietairePhysiques(self):
        print "Personnes physiques"
        print self.idContribuable
        try:
            self.cur.execute("SELECT DISTINCT p.idpersonne, p.nompersonne, p.prenompersonne, p.numcipersonne, p.adressepersonne "
                             "FROM personne p, contribuables_parcelle prd, parcelle_d pd "
                             "WHERE p.idpersonne = prd.idpersonne AND prd.idparcelle = %s AND p.idpersonne != %s ",(self.idparcelle,self.idContribuable))
            results = self.cur.fetchall()
            print results
            self.showInTablePhysique(results)
        except Exception as e:
            print(e)
            self.connection.rollback()

    def showInTablePhysique(self, data):
        self.idPersonnesPhysiques[:] = []
        self.ui.tableWidgetPhysique.setRowCount(0)
        i = 0
        while i < len(data):
            rowPosition = self.ui.tableWidgetPhysique.rowCount()
            self.ui.tableWidgetPhysique.insertRow(rowPosition)
            self.idPersonnesPhysiques.append(data[i][0])
            j = 1
            while j < len(data[i]) :
                self.ui.tableWidgetPhysique.setItem(rowPosition, j - 1, QtGui.QTableWidgetItem(unicode(data[i][j])))
                j = j + 1
            i = i + 1

    #def ouvrirPersPque(self):
        #try:
            #self.personne.consultation(1)
            #result = self.personne.exec_()
        #except StandardError as e:
            #print e
    def setIdContribuableToPass(self, idcontribuable):
        self.idContribuable = idcontribuable

    def ouvrirListePersPque(self):
        from Personnes.ListePersonnePqueRun import ListePersonnePqueRun
        self.listePersonne = ListePersonnePqueRun(self.connection, False, None, self.idContribuable)
        self.listePersonne.ui.btnSelectionner.clicked.connect(self.getIdPersonnePhysique)
        self.listePersonne.exec_()

    def getIdPersonnePhysique(self):
        #previousPrincipaleProprio = self.getProprioPrincipale()
        self.ui.tableWidgetPhysique.setRowCount(0)
        print "    def getIdPersonnePhysique(self):"
        if self.listePersonne.getIdPersonne() not in self.idPersonnesPhysiques:
            self.idPersonnesPhysiques.append(self.listePersonne.getIdPersonne())
        i = 0
        while i < len(self.idPersonnesPhysiques):
            self.cur.execute("SELECT DISTINCT p.idpersonne, p.nompersonne, p.prenompersonne, p.numcipersonne, p.adressepersonne "
                         "FROM personne p "
                         "WHERE p.idpersonne = %s", (self.idPersonnesPhysiques[i],))
            results = self.cur.fetchone()
            rowPosition = self.ui.tableWidgetPhysique.rowCount()
            self.ui.tableWidgetPhysique.insertRow(rowPosition)
            j = 1
            while j < len(results):
                self.ui.tableWidgetPhysique.setItem(rowPosition, j - 1, QTableWidgetItem(unicode(results[j])))
                j = j + 1
            i = i + 1
        self.listePersonne.close()
        #self.proprio.close()


    def getProprioPhysique(self):
        return self.idPersonnesPhysiques


    def enregistrerPersonnePque(self):
        status = self.personne.readInput()
        if status:
            idPersonne = self.personne.getIdPersonne()
            self.idPersonnesPhysiques.append(idPersonne[0])
            self.personne.close()
            self.close()
            #rowPosition = self.ui.tableWidget.rowCount()
            #self.ui.tableWidget.insertRow(rowPosition)
            # idpersonnes.append(data[i][0])
            #self.ui.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(_fromUtf8("Personne Physique")))
            #self.ui.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(unicode(self.numeroCertificat)))

    def enleverProprietairePque(self):
        print "Enlever consort"
        reply = QMessageBox.question(self, "Confirmation",
                                     u"Etes vous sure de vouloir enlever ce consort?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            line = self.ui.tableWidgetPhysique.selectedItems()
            print line[0]
            self.idPersonnesPhysiques.pop(line[0].row())
            print self.idPersonnesPhysiques
            self.ui.tableWidgetPhysique.removeRow(line[0].row())
        else:
            return


    def selectionLigne(self, row, col):
        self.idpersonnePque = self.idPersonnesPhysiques[row]
        self.personne.getPersonneById(self.idpersonnePque)
        #if col == 3:
            #self.updateStateCheck(row, col)
        #print "row = " + str(row) + "col = " + str(col)

    def setIdParcelle(self, idparcelle):
        self.idparcelle = idparcelle
        print "Id parcelle on Edition Consorts = " + str(self.idparcelle)

    def detailPersonnePque(self):
        if self.idpersonnePque is None:
            QMessageBox.critical(self, "Erreur ", u"Séléctionner au moins une ligne")
        else:
            try:
                self.personne.consultation(2)
                result = self.personne.exec_()
            except StandardError as e:
                print e

    def initDB(self):
        self.cur = self.connection.cursor()

    def __del__(self):
        self.cur.close()