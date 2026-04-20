# -*- coding: utf-8 -*-
import os, os.path, sys
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *
from PyQt4 import QtCore, QtGui
import globalvars

from Liste import Ui_Dialog
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class ListeRun(QDialog):
    def __init__(self,parent):
        print "listeRun en cours"
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.parent = parent
        self.canvas = self.parent.canvas
        self.idParcelles = []
        #self.has_data_tab = []
        self.selectedId = ""
        self.connection = self.parent.connection
        self.idContribuable = None
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.initDB()
        self.identiTyForm = ""
        self.geom = ""
        self.idsfokontany = []
        self.registry = parent.registry
        self.ui.tableWidget.setSelectionBehavior(1)
        self.ui.tableWidget.setSelectionMode(1)
        from Fiplof.Saisie.VoirListeContribuableRun import VoirListeContribuableRun
        self.listeContribuable = VoirListeContribuableRun(self.connection)
        self.ui.pushButton_4.hide()
        self.ui.pushButton_11.hide()
        self.disableAll()
        self.initActions()
        self.fillFokontany()




    def initActions(self):
        print " init actions AT 16-04-2018"
        self.ui.pushButton.clicked.connect(self.ouvrirListeContribuable)
        self.listeContribuable.ui.btnSelectionner.clicked.connect(self.getContribuableInfo)
        self.ui.pushButton_2.clicked.connect(self.readInput)
        self.ui.pushButton_3.clicked.connect(self.updateListe)
        self.ui.tableWidget.cellClicked.connect(self.selectionLigne)
        #self.ui.pushButtonConnexion.clicked.connect(self.checkAccessFIPLOF)
        self.ui.checkBox.stateChanged.connect(self.updateFieldsState)
        self.ui.checkBox_2.stateChanged.connect(self.updateFieldsState)
        self.ui.checkBox_3.stateChanged.connect(self.updateFieldsState)
        self.ui.checkBox_4.stateChanged.connect(self.updateFieldsState)
        self.ui.pushButton_10.clicked.connect(self.close)
        self.ui.lineEdit_4.textEdited.connect(self.readInput)

    def updateListe(self):

        if self.selectedId == "":
            QtGui.QMessageBox.information(self, u"Données non séléctionnées",
                                          u"Veuillez au moins séléctionner une ligne")
        else :
            if  self.identiTyForm == 1 :
                from Fiplof.Saisie.InformationFiscaleRun import InformationFiscaleRun
                infoFisc = InformationFiscaleRun(self.connection, self, 1)
                if infoFisc.ui.comboCategorieParcelle.count() == 0 or infoFisc.ui.comboCategorieBatiment.count() == 0:
                    QMessageBox.critical(self, "Erreur", u"Veuillez d'abord configiurer les categories au niveau du menu Impot foncier > Paramètres > Catégories")
                    return
                else:
                    result = infoFisc.exec_()
            else :
                print " form saisie parcelle"
                from Fiplof.Saisie.CodeParcelleRun import CodeParcelleRun
                cdParcelle = CodeParcelleRun(self.connection, self.geom)
                if cdParcelle.exec_():
                    print "zoom to "
                    #canvas = self.MainWindow.canvas
                    #cLayer = canvas.currentLayer()
                    #cLayer.triggerRepaint()

    def test(self):
        print "test"

    def voirContribuable(self):
        self.contribuable.estConsultation(1)
        self.contribuable.exec_()

    def modifierContribuable(self):
        self.contribuable.estConsultation(0)
        self.contribuable.ui.btnOk.clicked.connect(self.enregConsorts)
        self.contribuable.exec_()

    def initDB(self):
        self.cur = self.connection.cursor()

    def showAll(self):
        # self.cur.execute("SELECT idcertificat, numerodemande, datereconnaissance FROM certificat")
        #print " Show all actions"
        try:
            self.cur.execute("SELECT pd.gid,pd.codeparcelle,pd.numero, f.nomfokontany, pd.idcertificat  FROM parcelle_d pd, hameau h, fokontany f " \
                  "WHERE pd.idhameau = h.idhameau " \
                  "AND h.idfokontany = f.idfokontany " \
                  "AND pd.codeparcelle IS NOT NULL "
                             "AND pd.id_commune", (globalvars.id_commune, ))
            data = self.cur.fetchall()
            #print "data"
            self.showInTable(data)
        except StandardError as e:
            print e
            self.connection.rollback()
        # rint len(data[0])

    def showInTable(self, data):
        self.idParcelles[:] = []
        #self.has_data_tab[:] = []
        self.ui.tableWidget.setRowCount(0)
        i = 0
        i = 0
        j = 0
        nb_row = len(data)
        lignes = len(data)
        columns = 5

        #self.ui.tableWidget.setRowCount(nb_row)
        #self.ui.tableWidget.setColumnCount(columns)
        while i < len(data):
            #print data
            rowPosition = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(rowPosition)
            self.idParcelles.append(data[i][0])
            j = 1
            while j <= len(data[i]) - 1:
                item = QtGui.QTableWidgetItem()
                #print str(data[i][j])
                item.setText(_translate("", str(data[i][j]), None))
                self.ui.tableWidget.setItem(rowPosition, j-1, item)
                j = j + 1
            i = i + 1


    def defineFormRender(self):

        self.cur.execute("SELECT estfiscalite,geom FROM parcelle_d where gid =%s",(self.selectedId,))
        #cursor.execute("SELECT * FROM demande WHERE iddemande=%s", (iddemande,))
        data = self.cur.fetchone()
        self.identiTyForm = int(data[0])
        self.geom = data[1]

    def zoomToSelLayer(self):
        vtlayer = self.registry.mapLayersByName("Fiscalite")[0]
        self.canvas.setCurrentLayer(vtlayer)

        cLayer = self.canvas.currentLayer()
        for layer in self.canvas.layers():
            if layer.type() == layer.VectorLayer:
                layer.removeSelection()
        self.canvas.refresh()
        cLayer.select(int(self.selectedId))
        self.canvas.zoomToSelected(cLayer)

    def selectionLigne(self, row):
        self.selectedId = self.idParcelles[row]
        self.idparcelle = self.selectedId
        #print " self.selectedId in"
        self.defineFormRender()
        self.zoomToSelLayer()




        #print " self.selectedId out"

        #self.contribuable.getContribuableById(self.selectedId)

        # print numDemande
        # canvas = qgis.utils.iface.mapCanvas()
        # cLayer = canvas.currentLayer()
        # mc = qgis.utils.iface.mapCanvas()
        # for layer in mc.layers():
        # if layer.type() == layer.VectorLayer:
        # layer.removeSelection()

        # mc.refresh()
        # cLayer.select(int(ID))
        #        cLayer.select(496)

        # canvas.zoomToSelected(cLayer)

    def readInput(self):
        data = {}
        data['contribuable'] = str(self.ui.lineEdit.text()).strip().upper()
        data['codeparcelle'] = str(self.ui.lineEdit_4.text()).upper()
        data['fokontany'] = str(self.ui.comboBox.currentText()).strip().upper()
        data['numparcelle'] = str(self.ui.lineEdit_5.text()).strip().upper()
        self.rechercher(data)

    def rechercher(self, data):
        print "ENTRER DANS LA CONCTION DE RECHERCHE"
        flag = 0
        listeParams = []
        SQL = "SELECT pd.gid,pd.codeparcelle,pd.numero, f.nomfokontany  FROM parcelle_d pd, hameau h, fokontany f " \
              "WHERE pd.idhameau = h.idhameau " \
              "AND h.idfokontany = f.idfokontany " \
              "AND pd.codeparcelle IS NOT NULL " \
              "AND pd.id_commune = %s "
        listeParams.append(globalvars.id_commune)
        flag = 1
        if self.ui.checkBox.isChecked():
            contribuable = "%" + data['contribuable'] + "%"
            if self.ui.lineEdit.text() != "":
                if self.idContribuable is not None:
                    SQL = SQL + " AND idcontribuable = %s "
                    listeParams.append(self.idContribuable)
                    flag = 1
        if self.ui.checkBox_3.isChecked(): #recherche sur le code parcelle
            codeparcelle ="%" + data['codeparcelle'] + "%"
            print codeparcelle
            SQL = SQL + " AND UPPER(codeparcelle) LIKE %s "
            listeParams.append(codeparcelle)
            flag = 1

        if flag == 1:
            params = tuple(listeParams)
            self.cur.execute(SQL, params)
            results = self.cur.fetchall()
            print results
            self.showInTable(results)

        else:
            print SQL
            self.cur.execute(SQL)
            results = self.cur.fetchall()
            print results
            self.showInTable(results)

    def updateFieldsState(self):
        self.ui.lineEdit.setEnabled(self.ui.checkBox.isChecked())
        self.ui.comboBox.setEnabled(self.ui.checkBox_2.isChecked())
        self.ui.lineEdit_4.setEnabled(self.ui.checkBox_3.isChecked())
        self.ui.lineEdit_5.setEnabled(self.ui.checkBox_4.isChecked())

    def disableAll(self):
        self.ui.lineEdit.setDisabled(True)
        self.ui.comboBox.setDisabled(True)
        self.ui.lineEdit_4.setDisabled(True)
        self.ui.lineEdit_5.setDisabled(True)
        #self.ui.lineEditCIN2.setDisabled(True)
        #self.ui.lineEditCIN3.setDisabled(True)
        #self.ui.lineEditCIN4.setDisabled(True)

    def selectContribuable(self):
        return self.selectedId

    def isFromConsort(self, value=False):
        if value:
            self.contribuable.ui.btnConsorts.hide()
            self.contribuable.ui.btnRecherche.hide()
        else:
            self.contribuable.ui.btnConsorts.show()
            self.contribuable.ui.btnRecherche.show()

    def enregConsorts(self):
        self.contribuable.writeConsorts()
        self.contribuable.close()

    def ajoutContribuable(self):
        self.contribuable.estConsultation(2)
        # self.contribuable.ui.btnOk.clicked.connect(self.enregContribuable)
        self.contribuable.exec_()

    def enregContribuable(self):
        if self.contribuable.writeContribuable():
            self.contribuable.close()
            self.showAll()

    def __del__(self):
        self.cur.close()
        vtlayer = self.registry.mapLayersByName("Demandes Parcelle")[0]
        self.canvas.setCurrentLayer(vtlayer)

    def fillFokontany(self):
        self.idsfokontany[:] = []
        self.ui.comboBox.clear()
        try:
            self.cur.execute("SELECT idfokontany, nomfokontany FROM fokontany where idcommune = %s", (globalvars.id_commune,))
            fkts = self.cur.fetchall()
            for fkt in fkts:
                self.ui.comboBox.addItem(fkt[1])
                self.idsfokontany.append(fkt[0])
        except StandardError as e:
            print(e)
            self.connection.rollback()

    def ouvrirListeContribuable(self):
        self.listeContribuable.isFromConsort()
        self.listeContribuable.exec_()

    def getContribuableInfo(self):
        idContribuable = self.listeContribuable.selectContribuable()
        self.idContribuable =  idContribuable
        self.getContribuableById(idContribuable)
        self.listeContribuable.close()

    def getContribuableById(self, id):
        self.cur.execute("SELECT nom, prenom FROM contribuable WHERE idcontribuable = %s", (id,))
        data = self.cur.fetchone()
        infoContrib = str(data[0]).strip() + " " + str(data[1]).strip()
        self.ui.lineEdit.setText(infoContrib)



