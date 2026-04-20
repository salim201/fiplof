#coding: utf8
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
import psycopg2
import psycopg2.extras
import globalvars
import os
from Utils import Utils
from PyQt4.QtGui import QMessageBox
import datetime
import time

from AnnulerImport import Ui_Dialog

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class AnnulerImportRun(QDialog):
    def __init__(self, connection):
        QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.initActions()
        self.ui.tableWidgetImports.setSelectionBehavior(1)
        self.connection = connection
        self.ref_import = None
        self.ui.pushButtonRechercher.setEnabled(False)

    def initActions(self):
        self.ui.checkBox.stateChanged.connect(self.changeState)
        self.ui.checkBox_2.stateChanged.connect(self.changeState)
        self.ui.pushButtonAfficherTous.clicked.connect(self.showAll)
        self.ui.pushButtonRechercher.clicked.connect(self.rechercher)
        self.ui.tableWidgetImports.cellClicked.connect(self.selectionLigne)
        self.ui.pushButtonSupprimer.clicked.connect(self.delete_import)

    def changeState(self):
        self.ui.lineEditRefImport.setEnabled(self.ui.checkBox.isChecked())
        self.ui.dateEditDateImport.setEnabled(self.ui.checkBox_2.isChecked())

        if (self.ui.checkBox.isChecked() == False and self.ui.checkBox_2.isChecked() == False):
            self.ui.pushButtonRechercher.setEnabled(False)
        else:
            self.ui.pushButtonRechercher.setEnabled(True)

    def showAll(self):
        cur = self.connection.cursor()
        data = None
        try:
            cur.execute ('SELECT DISTINCT ref_import, date_import_inv FROM parcelle_d WHERE ref_import IS NOT NULL')
            data = cur.fetchall()
            print data
        except Exception as err:
            print(err)
            self.connection.rollback()
        cur.close()

        if data is not None:
            self.showInTable(data)

    def showInTable(self, data):
        self.ui.tableWidgetImports.setRowCount(0)
        i = 0
        while i < len(data):
            rowPosition = self.ui.tableWidgetImports.rowCount()
            self.ui.tableWidgetImports.insertRow(rowPosition)
            # self.idPersonnePhysiques.append(data[i][0])
            j = 0
            while j < len(data[i]):
                if j == 0 :
                    self.ui.tableWidgetImports.setItem(rowPosition, j, QTableWidgetItem(unicode(data[i][j])))
                else:
                    self.ui.tableWidgetImports.setItem(rowPosition, j, QTableWidgetItem(data[i][j].strftime('%d/%m/%Y')))
                j = j + 1
            i = i + 1

    def rechercher(self):
        ref = None
        date = None
        params = []
        SQL = "SELECT DISTINCT ref_import, date_import_inv FROM parcelle_d WHERE "
        if self.ui.checkBox.isChecked():
            #ref = self.ui.lineEditRefImport.text()
            ref = "%" + str(self.ui.lineEditRefImport.text()).strip().upper() + "%"
            SQL = SQL + "ref_import LIKE %s "
            params.append(ref)
        if self.ui.checkBox_2.isChecked():
            if self.ui.checkBox.isChecked():
                SQL = SQL + " and "
            SQL = SQL + " date_import_inv = %s "
            date = datetime.date(self.ui.dateEditDateImport.date().year(), self.ui.dateEditDateImport.date().month(), self.ui.dateEditDateImport.date().day())
            print date
            params.append(date)

        cur = self.connection.cursor()
        try:
            cur.execute(SQL, tuple(params))
            res = cur.fetchall()
            if res is not None:
                self.showInTable(res)
        except Exception as err:
            print (err)
            self.connection.rollback()
        cur.close()

    def selectionLigne(self, row):
        print row
        try:
            self.ref_import = str(self.ui.tableWidgetImports.item(row, 0).text()).strip()
            print self.ref_import
        except Exception as err:
            print(err)



    def delete_import(self):
        try:
            reply = QMessageBox.question(self, u"Confirmation",
                                                  u"Voulez-vous supprimer les données importés?",
                                                  QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        except Exception as err:
            print err
        if reply == QMessageBox.Yes:
            SQL1 = "DELETE  FROM limitesparcelle WHERE idparcelle IN (SELECT gid FROM parcelle_d  WHERE TRIM(ref_import) = %s AND numdemande is NULL  )"
            SQL2 = "DELETE  FROM avoir_demande WHERE idparcelle IN (SELECT gid FROM parcelle_d  WHERE TRIM(ref_import) = %s AND numdemande is NULL)"
            SQL3 = "DELETE  FROM demande WHERE gid IN (SELECT gid FROM parcelle_d  WHERE TRIM(ref_import) = %s AND numdemande is NULL)"
            SQL4 = "DELETE  FROM parcelle_d WHERE TRIM(ref_import) = %s AND numdemande is NULL"
            try:
                cur1 = self.connection.cursor()
                cur1.execute(SQL1, (self.ref_import,))
                self.connection.commit()
                print "delete SQL1"
            except Exception as err:
                print err
                self.connection.rollback()
            try:
                cur2 = self.connection.cursor()
                cur2.execute(SQL2, (self.ref_import,))
                self.connection.commit()
                print "delete SQL2"
            except Exception as err:
                print err
                self.connection.rollback()

            try:
                cur3 = self.connection.cursor()
                cur3.execute(SQL3, (self.ref_import,))
                self.connection.commit()
                print "delete SQL3"
            except Exception as err:
                print err

            try:
                cur4 = self.connection.cursor()
                cur4.execute(SQL4, (self.ref_import,))
                self.connection.commit()
                print "delete SQL4"
            except Exception as err:
                print err
                self.connection.rollback()

            #Requete
            self.showAll()
            QMessageBox.information(self,"Information", u"Suppréssion terminée")
        else:
            return





