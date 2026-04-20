#coding: utf-8
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
from qgis.core import *
from qgis.gui import *
import datetime, time
import globalvars, os, sys, psycopg2

from AreaConvert import AreaConvert
from .Statistiques import Ui_Dialog

class Statistiques(QDialog):
    def __init__(self, connection, parent):
        self.connection = connection
        QDialog.__init__(self)
        self.setModal(True)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        #self.canvas = canvas
        #self.tool = parent.tool
        self.senderName = self.sender().objectName()
        self.idparcelle = parent.idparcelle
        self.ui.dateEditAnnee.setDate(QDate.currentDate())
        self.ui.btnExportExcel.hide()

        self.initDB()
        self.fillStatistiques()
        self.initActions()

    def initActions(self):
        self.ui.btnRafraichirStat.clicked.connect(self.fillStatistiques)

    def initDB(self):
        self.cur = self.connection.cursor()

    def __del__(self):
        self.cur.close()
        #vtlayer = self.registry.mapLayersByName("Demandes Parcelle")[0]
        #self.canvas.setCurrentLayer(vtlayer)

    def fillStatistiques(self):
        #Nombre de parcelles FIPLOF
        try:
            self.cur.execute("SELECT COUNT(*) FROM parcelle_d WHERE estfiscalite = 1")
            nombre_parcelle = self.cur.fetchone()
            if nombre_parcelle is not None:
                self.ui.lineEditNombreparcelle.setText(str(nombre_parcelle[0]))

        except StandardError as e:
            print(e)
            self.connection.rollback()
        #Nombre SRI
        try:
            self.cur.execute("SELECT COUNT(*) FROM parcelle_d WHERE srisraparcelle = 'sri' ")
            nombre_sri = self.cur.fetchone()
            if nombre_sri is not None:
                self.ui.lineEditNombreSRI.setText(str(nombre_sri[0]))
        except StandardError as e:
            print(e)
            self.cur.connection.rollback()

        #Nombre SRA
        try:
            self.cur.execute("SELECT COUNT(*) FROM parcelle_d WHERE srisraparcelle = 'sra' ")
            nombre_sra = self.cur.fetchone()
            if nombre_sra is not None:
                self.ui.lineEditNombreSRA.setText(str(nombre_sra[0]))
        except StandardError as e:
            print(e)
            self.cur.connection.rollback()

        #Nombre contribuable
        try:
            self.cur.execute("SELECT COUNT(*) FROM parcelle_d WHERE idcontribuable IS NOT NULL")
            nombre_contribuable = self.cur.fetchone()
            if nombre_contribuable is not None:
                self.ui.lineEditNombreContribuable.setText(str(nombre_contribuable[0]))
        except StandardError as e:
            print(e)
            self.connection.rollback()
        #Nombre Certificat:
        try:
            self.cur.execute("SELECT COUNT(*) FROM parcelle_d WHERE etatparcelle_d = 3")
            nombre_certificat = self.cur.fetchone()
            if nombre_certificat is not None:
                self.ui.lineEditNombreCertificat.setText(str(nombre_certificat[0]))
        except StandardError as e:
            print(e)
            self.connection.rollback()

        self.fillTableParFokonatany()
        self.fillTableParConsistance()

    def fillTableParFokonatany(self):
        tableDataParFokontany = []

        try:
            self.cur.execute("SELECT idfokontany, nomfokontany FROM fokontany WHERE idcommune = %s", (globalvars.id_commune,))
            fokontany = self.cur.fetchall()
            for fkt in fokontany:
                dataParFokontany = []
                dataParFokontany.append(fkt[1])
                #Nombre de parcelle par fokontany
                try:
                    self.cur.execute("SELECT COUNT(*) FROM parcelle_d WHERE estfiscalite = 1 AND idhameau IN "
                                         "(SELECT idhameau FROM hameau WHERE idfokontany = %s)", (fkt[0],))
                    nbreparcelle = self.cur.fetchone()
                    if nbreparcelle is not None:
                        dataParFokontany.append(nbreparcelle[0])
                    else:
                        dataParFokontany.append(0)
                except StandardError as e:
                    print(e)
                    self.connection.rollback()

                #Nombre de certifiact par fokontany
                try:
                    self.cur.execute("SELECT COUNT(*) FROM parcelle_d WHERE etatparcelle_d = 3 AND idhameau IN "
                                         "(SELECT idhameau FROM hameau WHERE idfokontany = %s)", (fkt[0],))
                    nbreCertificat = self.cur.fetchone()
                    if nbreCertificat is not None:
                        dataParFokontany.append(nbreCertificat[0])
                    else:
                        dataParFokontany.append(0)
                except StandardError as e:
                    print(e)
                    self.connection.rollback()

                #Nombre de contribuable par fokontany
                try:
                    self.cur.execute("SELECT COUNT(*) FROM parcelle_d WHERE idcontribuable IS NOT NULL AND idhameau IN "
                                         "(SELECT idhameau FROM hameau WHERE idfokontany = %s)", (fkt[0],))
                    nbreContribuable = self.cur.fetchone()
                    if nbreContribuable is not None:
                        dataParFokontany.append(nbreContribuable[0])
                    else:
                        dataParFokontany.append(0)
                except StandardError as e:
                    print(e)
                    self.connection.rollback()

                #Nombre SRI
                try:
                    self.cur.execute("SELECT COUNT(*) FROM parcelle_d WHERE srisraparcelle = 'sri' AND idhameau IN "
                                         "(SELECT idhameau FROM hameau WHERE idfokontany = %s)", (fkt[0],))
                    nbreSRI = self.cur.fetchone()
                    if nbreSRI is not None:
                        dataParFokontany.append(nbreSRI[0])
                    else:
                        dataParFokontany.append(0)
                except StandardError as e:
                    print(e)
                    self.connection.rollback()

                #Nombre SRA
                try:
                    self.cur.execute("SELECT COUNT(*) FROM parcelle_d WHERE srisraparcelle = 'sra' AND idhameau IN "
                                         "(SELECT idhameau FROM hameau WHERE idfokontany = %s)", (fkt[0],))
                    nbreSRA = self.cur.fetchone()
                    if nbreSRA is not None:
                        dataParFokontany.append(nbreSRA[0])
                    else:
                        dataParFokontany.append(0)
                except StandardError as e:
                    print(e)
                    self.connection.rollback()

                tableDataParFokontany.append(dataParFokontany)
            print tableDataParFokontany
            self.showInTableFkt(tableDataParFokontany)

        except StandardError as e:
            print(e)
            self.connection.rollback()

    def showInTableFkt(self, data):
        i = 0
        self.ui.tableWidgetParFokonatany.setRowCount(0)
        while i < len(data):
            rowCount = self.ui.tableWidgetParFokonatany.rowCount()
            self.ui.tableWidgetParFokonatany.insertRow(rowCount)
            j = 0
            while j < len(data[i]):
                if j >= 0 and j <= 2:
                    self.ui.tableWidgetParFokonatany.setItem(i, j, QTableWidgetItem(str(data[i][j])))
                elif j == 3:
                    if data[i][1] != 0:
                        #print "pourcentage = " + str(data[i][1])
                        value = (float(data[i][2]) / float(data[i][1])) * 100
                        self.ui.tableWidgetParFokonatany.setItem(i, j, QTableWidgetItem(str(value)))
                    else:
                        value = 0
                        self.ui.tableWidgetParFokonatany.setItem(i, j, QTableWidgetItem(str(value)))
                elif j >= 4 and j <= 6:
                    self.ui.tableWidgetParFokonatany.setItem(i, j, QTableWidgetItem(str(data[i][j - 1])))
                j = j + 1
            i = i + 1

    def fillTableParConsistance(self):
        tableDataParConsistance = []
        try:
            self.cur.execute("SELECT idconsistance, libelleconsistance FROM consistance")
            consistances = self.cur.fetchall()
            for consistance in consistances:
                dataParConsistance = []
                dataParConsistance.append(str(consistance[1]))

                #Nombre de parcelle par consistance
                try:
                    self.cur.execute("SELECT COUNT(*) FROM parcelle_d WHERE estfiscalite = 1 AND id_consistance = %s "
                                     ,(consistance[0],))
                    nbreparcelle = self.cur.fetchone()
                    if nbreparcelle is not None:
                        dataParConsistance.append(nbreparcelle[0])
                    else:
                        dataParConsistance.append(0)
                except StandardError as e:
                    print(e)
                    self.connection.rollback()

                tableDataParConsistance.append(dataParConsistance)
            print tableDataParConsistance
            self.showInTableParConsistance(tableDataParConsistance)


        except StandardError as e:
            print(e)
            self.connection.rollback()

    def showInTableParConsistance(self, data):
        i = 0
        self.ui.tableWidgetParConsistance.setRowCount(0)
        while i < len(data):
            rowCount = self.ui.tableWidgetParConsistance.rowCount()
            self.ui.tableWidgetParConsistance.insertRow(rowCount)
            j = 0
            while j < len(data[i]):
                if j >= 0 and j <= 1:
                    self.ui.tableWidgetParConsistance.setItem(i, j, QTableWidgetItem(str(data[i][j])))

                j = j + 1
            i = i + 1





