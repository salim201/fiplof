# coding: utf-8
from PyQt4.QtGui import *
from PyQt4 import Qt, QtGui, QtCore
from PyQt4.Qt import QApplication
from qgis.core import *
from qgis.gui import *
import datetime, time
import globalvars
import os
import webbrowser
import tempfile
from random import randint
from AreaConvert import AreaConvert
from Utils import Utils
from  crl import Ui_Dialog

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
class CrlRun(QDialog):
    def __init__(self, connection, canvas, parent,slf = None):
        self.connection = connection
        QDialog.__init__(self)
        self.setModal(True)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.canvas = canvas
        self.idsFokontany = []
        self.idsHameau = []
        self.initDB()
        self.initActions()
        self.fillFokontany()

    def initDB(self):
        self.cursor = self.connection.cursor()


    def initActions(self):
        self.ui.checkBoxNumDecision.clicked.connect(self.changeFieldsStatus)
        self.ui.checkBoxFkt.clicked.connect(self.changeFieldsStatus)
        self.ui.checkBoxHameau.clicked.connect(self.changeFieldsStatus)
        self.ui.comboBoxFokontany.currentIndexChanged.connect(self.fillHameau)
        self.ui.pushButtonRechercher.clicked.connect(self.rechercher)
        self.ui.tableWidgetDemande.cellClicked.connect(self.onDemandeClicked)
        self.ui.tableWidgetDemande.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

    def changeFieldsStatus(self):
        self.ui.lineEditNumeroDecision.setEnabled(self.ui.checkBoxNumDecision.isChecked())
        self.ui.comboBoxFokontany.setEnabled(self.ui.checkBoxFkt.isChecked())
        self.ui.comboBoxHameau.setEnabled(self.ui.checkBoxHameau.isChecked())

    def fillFokontany(self):
        self.ui.comboBoxFokontany.clear()
        self.idsFokontany = []
        self.cursor.execute(
            "SELECT nomfokontany, idfokontany FROM fokontany WHERE idcommune = %s",
            (globalvars.id_commune,))
        fkts = self.cursor.fetchall()
        for fkt in fkts:
            self.ui.comboBoxFokontany.addItem(fkt[0], fkt[1])
            self.idsFokontany.append(fkt[1])

    def fillHameau(self):
        self.ui.comboBoxHameau.clear()
        self.idsHameau = []
        if self.ui.comboBoxFokontany.currentIndex() != -1 and len(self.idsFokontany) > 0:
            idfokontany = self.idsFokontany[self.ui.comboBoxFokontany.currentIndex()]
            self.cursor.execute(
                "SELECT nomhameau, idhameau FROM hameau WHERE idfokontany = %s",
                (idfokontany,))
            hmx = self.cursor.fetchall()
            for hm in hmx:
                self.ui.comboBoxHameau.addItem(hm[0], hm[1])
                self.idsHameau.append(hm[1])

    def onDemandeClicked(self, row, col):
        print "onDemandeClicked row=%d col=%d" % (row, col)
        self.ui.tableWidgetCRL.setRowCount(0)
        item = self.ui.tableWidgetDemande.item(row, 1)
        if item is None:
            print "item at row %d col 1 is None" % row
            return
        text = unicode(item.text())
        print "iddemande text='%s'" % text
        try:
            iddemande = int(text)
        except:
            print "cannot parse iddemande"
            return

        try:
            self.cursor.execute(
                "SELECT rc.libelle_role, "
                "COALESCE(p1.nompersonne, '') || ' ' || COALESCE(p1.prenompersonne, '') AS titulaire_nom, "
                "COALESCE(p2.nompersonne, '') || ' ' || COALESCE(p2.prenompersonne, '') AS suppleant_nom, "
                "dc1.idpersonne AS id_titulaire, "
                "dc2.idpersonne AS id_suppleant "
                "FROM role_crl rc "
                "LEFT JOIN demande_crl dc1 ON dc1.id_role = rc.id_role "
                "  AND dc1.iddemande = %s AND dc1.titulaire = true "
                "LEFT JOIN personne p1 ON p1.idpersonne = dc1.idpersonne "
                "LEFT JOIN demande_crl dc2 ON dc2.id_role = rc.id_role "
                "  AND dc2.iddemande = %s AND dc2.titulaire = false "
                "LEFT JOIN personne p2 ON p2.idpersonne = dc2.idpersonne "
                "WHERE dc1.idpersonne IS NOT NULL OR dc2.idpersonne IS NOT NULL "
                "ORDER BY rc.id_role",
                (iddemande, iddemande))
            rows = self.cursor.fetchall()
            print "found %d CRL rows" % len(rows)
        except Exception as e:
            print "SQL error: %s" % str(e)
            self.connection.rollback()
            return

        self.ui.tableWidgetCRL.setRowCount(len(rows))
        for i, r in enumerate(rows):
            for j in range(5):
                val = r[j]
                self.ui.tableWidgetCRL.setItem(
                    i, j, QtGui.QTableWidgetItem("" if val is None else unicode(val)))

    def rechercher(self):
        self.ui.tableWidgetDemande.setRowCount(0)
        self.cursor = self.connection.cursor()
        params = []

        sql = ("SELECT d.iddemande, d.datedemande, d.numdemande, d.numdecision, "
               "d.datedecision, d.debut_affichage, d.fin_affichage, "
               "d.datereconnaissance, d.cqe "
               "FROM demande d "
               "INNER JOIN parcelle_d pd ON d.gid = pd.gid")

        conditions = []
        if self.ui.checkBoxNumDecision.isChecked():
            text = unicode(self.ui.lineEditNumeroDecision.text()).strip()
            if text:
                conditions.append("d.numdecision LIKE %s")
                params.append("%" + text + "%")

        if self.ui.checkBoxFkt.isChecked():
            idx = self.ui.comboBoxFokontany.currentIndex()
            if idx != -1 and len(self.idsFokontany) > 0:
                conditions.append("d.idfokontany = %s")
                params.append(self.idsFokontany[idx])

        if self.ui.checkBoxHameau.isChecked():
            idx = self.ui.comboBoxHameau.currentIndex()
            if idx != -1 and len(self.idsHameau) > 0:
                conditions.append("pd.idhameau = %s")
                params.append(self.idsHameau[idx])

        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        sql += " ORDER BY d.iddemande ASC"

        try:
            self.cursor.execute(sql, params)
            rows = self.cursor.fetchall()
        except Exception as e:
            print(e)
            self.connection.rollback()
            return

        print "rechercher found %d rows" % len(rows)
        self.ui.tableWidgetDemande.setRowCount(len(rows))
        for i, r in enumerate(rows):
            item = QtGui.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.ui.tableWidgetDemande.setItem(i, 0, item)

            for j in range(1, 9):
                val = r[j - 1]
                text = "" if val is None else unicode(val)
                self.ui.tableWidgetDemande.setItem(
                    i, j, QtGui.QTableWidgetItem(text))

            cq = "OUI" if r[8] else "NON" if r[8] is not None else ""
            self.ui.tableWidgetDemande.setItem(
                i, 9, QtGui.QTableWidgetItem(cq))
