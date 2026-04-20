# coding: utf-8
import os, os.path, sys, psycopg2
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore
from qgis.gui import *

from .ConsultationProprietaire import Ui_Dialog

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s



class ProprietairesRun(QDialog):
    def __init__(self, connection, parent = None):
        QDialog.__init__(self)
        self.connection = connection
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setModal(True)
        self.initDB()
        self.numeroCertificat = None
        self.idpersonne = None
        self.idpersonnePque = None
        self.idparcelle = parent.gid
        self.parent = parent
        self.proprioPrincipale = None
        self.coproprietaire = None
        from .GestionProprietaireRun import GestionProprietaireRun
        self.proprio = GestionProprietaireRun(self.connection)
        from Personnes.PersonnePhysiqueRun import PersonnePhysiqueRun
        self.personne = PersonnePhysiqueRun(self.connection)
        self.idPersonnesPhysiques = []
        self.idPersonnesMorales = []
        self.initActions()

        self.proprietairePhysiques()

    def initActions(self):
        self.ui.pushButtonAjouter.clicked.connect(self.gererProprio)
        self.ui.tableWidgetPhysique.cellClicked.connect(self.selectionLigne)
        self.ui.tableWidgetMorale.cellClicked.connect(self.selectionLigneMorale)
        self.ui.pushButtonDetailsPhysique.clicked.connect(self.detailPersonnePque)
        self.ui.pushButtonDetailsMorale.clicked.connect(self.detailPersonneMorale)
        self.ui.pushButtonAnnuler.clicked.connect(self.close)
        self.proprio.listePersonne.ui.btnSelectionner.clicked.connect(self.getIdPersonnePhysique)
        self.proprio.listePersonneMorale.ui.pushButton_5.clicked.connect(self.getIdPersonneMorale)
        self.proprio.personne.ui.btnOk.clicked.connect(self.enregistrerPersonnePque)
        self.proprio.personneMorale.ui.btnOk.clicked.connect(self.enregistrerPersonneMorale)
        self.ui.pushButtonEnleverProprioPpque.clicked.connect(self.enleverProprietairePque)
        self.ui.pushButtonEnleverProprioMor.clicked.connect(self.enleverProprietaireMorale)

    def gererProprio(self):
        self.proprio.exec_()

    def ouvrirPersPque(self):
        try:
            self.personne.consultation(1)
            result = self.personne.exec_()
        except StandardError as e:
            print e

    def getIdPersonnePhysique(self):
        print "getIdPersonnePhysique getIdPersonnePhysique"
        previousPrincipaleProprio = self.getProprioPrincipale()
        previousCoproprio = self.getProprioPrincipale(1)
        self.ui.tableWidgetPhysique.setRowCount(0)
        if self.proprio.listePersonne.getIdPersonne() not in self.idPersonnesPhysiques:
            self.idPersonnesPhysiques.append(self.proprio.listePersonne.getIdPersonne())
        i = 0
        while i < len(self.idPersonnesPhysiques):
            self.cur.execute("SELECT p.idpersonne, p.nompersonne, p.prenompersonne, p.numcipersonne "
                         "FROM personne p "
                         "WHERE p.idpersonne = %s", (self.idPersonnesPhysiques[i],))
            results = self.cur.fetchone()
            rowPosition = self.ui.tableWidgetPhysique.rowCount()
            self.ui.tableWidgetPhysique.insertRow(rowPosition)
            j = 1
            while j <= (len(results) + 1):
                if j == 4:
                    item = QTableWidgetItem(True)
                    item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                    if len(self.idPersonnesPhysiques) == 1:
                        item.setCheckState(Qt.Checked)
                    elif self.idPersonnesPhysiques[i] == previousPrincipaleProprio:
                        item.setCheckState(Qt.Checked)
                    else:
                        item.setCheckState(Qt.Unchecked)
                    self.ui.tableWidgetPhysique.setItem(rowPosition, j-1, item)
                elif j == 5:
                    item = QTableWidgetItem(True)
                    item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                    if self.idPersonnesPhysiques[i] == previousCoproprio:
                        item.setCheckState(Qt.Checked)
                    else:
                        item.setCheckState(Qt.Unchecked)
                    self.ui.tableWidgetPhysique.setItem(rowPosition, j - 1, item)
                else:
                    self.ui.tableWidgetPhysique.setItem(rowPosition, j - 1, QTableWidgetItem(unicode(results[j])))
                j = j + 1
            i = i + 1
        self.proprio.listePersonne.close()
        self.proprio.close()


    def getIdPersonneMorale(self):
        self.ui.tableWidgetMorale.setRowCount(0)
        if self.proprio.listePersonneMorale.getIdPersonne() not in self.idPersonnesMorales:
            self.idPersonnesMorales.append(self.proprio.listePersonneMorale.getIdPersonne())
            #print self.idPersonnesMorales
        i = 0
        while i < len(self.idPersonnesMorales):
            self.cur.execute("SELECT p.idpersonnemorale, p.denomination, p.siege, tpm.type "
                             "FROM personnemorale p, typepersonnemorale tpm "
                             "WHERE p.idtype = tpm.idtype "
                         "AND p.idpersonnemorale = %s", (self.idPersonnesMorales[i],))
            results = self.cur.fetchone()
            rowPosition = self.ui.tableWidgetMorale.rowCount()
            self.ui.tableWidgetMorale.insertRow(rowPosition)
            j = 1
            while j < len(results):
                self.ui.tableWidgetMorale.setItem(rowPosition, j - 1, QTableWidgetItem(unicode(results[j])))
                j = j + 1
            i = i + 1
        self.proprio.listePersonneMorale.close()
        self.proprio.close()


    def getProprioPhysique(self):
        return self.idPersonnesPhysiques

    def getProprioMorale(self):
        return self.idPersonnesMorales

    def enregistrerPersonnePque(self):
        status = self.proprio.personne.readInput()
        if status:
            idPersonne = self.proprio.personne.getIdPersonne()
            self.idPersonnesPhysiques.append(idPersonne[0])
            self.proprio.personne.close()
            self.proprio.close()
            #rowPosition = self.ui.tableWidget.rowCount()
            #self.ui.tableWidget.insertRow(rowPosition)
            # idpersonnes.append(data[i][0])
            #self.ui.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(_fromUtf8("Personne Physique")))
            #self.ui.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(unicode(self.numeroCertificat)))

    def getProprioPrincipale(self, idx = 0):
        print "in get proprio principale"
        i = 0
        #if self.ui.tableWidgetPhysique.item(row, col).checkState() == 2:
            #print "cell checked"
            #rowChecked = row
        while i < self.ui.tableWidgetPhysique.rowCount():
            if idx == 0:
                if self.ui.tableWidgetPhysique.item(i, 3).checkState() == 2:
                    self.proprioPrincipale = self.idPersonnesPhysiques[i]
                    return self.proprioPrincipale
            if idx == 1:
                if self.ui.tableWidgetPhysique.item(i, 4).checkState() == 2:
                    self.coproprietaire = self.idPersonnesPhysiques[i]
                    return self.coproprietaire
            i = i + 1

    def enregistrerPersonneMorale(self):
        print "enreg personne morale"
        status = self.proprio.personneMorale.readInput()
        if status:
            print "personne morale bien enregistree"
            idPersonne = status
            print idPersonne
            self.idPersonnesMorales.append(idPersonne[0])
            print self.idPersonnesMorales
            self.proprio.personneMorale.close()
            self.proprio.close()
            #rowPosition = self.ui.tableWidget.rowCount()
            #self.ui.tableWidget.insertRow(rowPosition)
            # idpersonnes.append(data[i][0])
            #self.ui.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(_fromUtf8("Personne Morale")))

    def setNumCertificat(self, numero):
        self.numeroCertificat = numero


    def enleverProprietairePque(self):
        print "Enlever personne physique"
        reply = QMessageBox.question(self, "Confirmation",
                                     u"Etes vous sure de vouloir enlever ce propriétaire?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            line = self.ui.tableWidgetPhysique.selectedItems()
            print line[0]
            self.idPersonnesPhysiques.pop(line[0].row())
            print self.idPersonnesPhysiques
            self.ui.tableWidgetPhysique.removeRow(line[0].row())
            if self.ui.tableWidgetPhysique.rowCount() == 1:
                self.ui.tableWidgetPhysique.item(0, 3).setCheckState(Qt.Checked)
        else:
            return

    def enleverProprietaireMorale(self):
        print "Enlever personne morale"
        reply = QMessageBox.question(self, "Confirmation",
                                     u"Etes vous sure de vouloir enlever ce propriétaire?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            line = self.ui.tableWidgetMorale.selectedItems()
            print line[0].row()
            self.idPersonnesMorales.pop(line[0].row())
            print self.idPersonnesMorales
            self.ui.tableWidgetMorale.removeRow(line[0].row())
        else:
            return

    def detailPersonnePque(self):
        if self.idpersonnePque is None:
            QMessageBox.critical(self, "Erreur ", u"Séléctionner au moins une ligne")
        else:
            try:
                self.personne.consultation(2)
                result = self.personne.exec_()
            except StandardError as e:
                print e

    def detailPersonneMorale(self):
        if self.idpersonne is None:
            QMessageBox.critical(self, "Erreur ", u"Séléctionner au moins une ligne")
            return
        from .PersonneMoraleRun import PersonneMoraleRun
        self.personneMorale = PersonneMoraleRun(self.connection, self)
        self.personneMorale.consultation(2)
        self.personneMorale.ui.btnOk.clicked.connect(self.savePersonneMorale)
        try:
            result = self.personneMorale.exec_()
        except StandardError as e:
            print e

    def selectionLigne(self, row, col):
        self.idpersonnePque = self.idPersonnesPhysiques[row]
        self.personne.getPersonneById(self.idpersonnePque)
        if col == 3 or col == 4:
            self.updateStateCheck(row, col)
        #self.choix.getDemandeNum(numDemande, self.cur

    def updateStateCheck(self, row, col):
        #firstChecked = False
        #if firstChecked == False:
        rowChecked = None
        i = 0
        if self.ui.tableWidgetPhysique.item(row, col).checkState() == 2:
            print "cell checked"
            rowChecked = row
            while i < self.ui.tableWidgetPhysique.rowCount():
                if i != rowChecked:
                    self.ui.tableWidgetPhysique.item(i,col).setCheckState(QtCore.Qt.Unchecked)
                i = i + 1

    def selectionLigneMorale(self, row):
        self.idpersonne = self.idPersonnesMorales[row]
        #self.ui.lineEdit.setText(self.ui.tableWidget.item(row, 1).text())

    def initDB(self):
        self.cur = self.connection.cursor()

    def __del__(self):
        #self.parent.enregProprio()
        self.cur.close()



    def proprietairePhysiques(self):
        print "Personnes physiques"
        try:
            self.cur.execute("SELECT DISTINCT p.idpersonne, p.nompersonne, p.prenompersonne, p.numcipersonne, prd.representant, prd.estcoproprietaire "
                             "FROM personne p, proprietaireparcelle prd, parcelle_d pd "
                             "WHERE p.idpersonne = prd.idpersonne AND prd.idparcelle = pd.gid "
                             "AND pd.gid = %s",(self.idparcelle,))
            results = self.cur.fetchall()
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
                if j == 4 or j == 5:
                    item = QTableWidgetItem(True)
                    item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                    if len(data) == 1:
                        item.setCheckState(Qt.Checked)
                    elif data[i][j] is not None and data[i][j] == True:
                        item.setCheckState(Qt.Checked)
                    else:
                        item.setCheckState(Qt.Unchecked)
                    self.ui.tableWidgetPhysique.setItem(rowPosition, j - 1, item)
                    print item.checkState()

                else:
                    self.ui.tableWidgetPhysique.setItem(rowPosition, j - 1, QTableWidgetItem(unicode(data[i][j])))
                j = j + 1
            i = i + 1


