# -*- coding: utf-8 -*-
import os, os.path, sys
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *
from PyQt4 import QtCore, QtGui
import globalvars
from .Html2Pdf import Html2Pdf
import datetime, time
import os
import webbrowser
import tempfile
from random import randint
from AreaConvert import AreaConvert
from Etats.ListeToPrint import Ui_Dialog
from xlwt import *
import xlwt

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
        self.idsParcelletoPrint = []
        self.toutCocher = False
        #self.has_data_tab = []
        self.selectedId = ""
        self.connection = self.parent.connection
        self.idContribuable = None
        self.book = Workbook()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.initDB()
        self.identiTyForm = ""
        self.geom = ""
        self.idsfokontany = []
        self.registry = parent.registry
        self.ui.tableWidget.setSelectionBehavior(1)
        self.ui.tableWidget.setSelectionMode(1)
        #from Fiplof.Saisie.VoirListeContribuableRun import VoirListeContribuableRun
        #self.listeContribuable = VoirListeContribuableRun(self.connection)
        from Personnes.ListePersonnePqueRun import ListePersonnePqueRun
        self.listePersonne = ListePersonnePqueRun(self.connection)
        self.ui.pushButton_4.hide()
        self.ui.pushButton_11.hide()
        self.initDB()
        self.disableAll()
        self.initActions()
        self.fillFokontany()




    def initActions(self):
        print " init actions AT 16-04-2018"
        self.ui.pushButton.clicked.connect(self.ouvrirListeContribuable)
        #self.listeContribuable.ui.btnSelectionner.clicked.connect(self.getContribuableInfo)
        self.listePersonne.ui.btnSelectionner.clicked.connect(self.setIdContribuable)
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
        self.ui.checkBoxCocherTout.stateChanged.connect(self.updateCheck)
        self.ui.btnPrint.clicked.connect(self.doPrint)

    def updateListe(self):

        if self.selectedId == "":
            QtGui.QMessageBox.information(self, u"Données non séléctionnées",
                                          u"Veuillez au moins sélécionner une ligne")
        else :
            if  self.identiTyForm == 1 :
                from Fiplof.Saisie.InformationFiscaleRun import InformationFiscaleRun
                infoFisc = InformationFiscaleRun(self.connection, self, 1)
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

    def setIdContribuable(self):
        self.idContribuable = self.listePersonne.getIdPersonne()
        print "id contribuable = " + str(self.idContribuable)
        if self.idContribuable is not None:
            self.getContribuableById(self.idContribuable)
        self.listePersonne.close()

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
        self.cur.execute("SELECT pd.gid,pd.codeparcelle,pd.numero, f.nomfokontany  FROM parcelle_d pd, hameau h, fokontany f " \
              "WHERE pd.idhameau = h.idhameau " \
              "AND h.idfokontany = f.idfokontany " \
              "AND pd.codeparcelle IS NOT NULL  ")
        data = self.cur.fetchall()
        #print "data"
        self.showInTable(data)
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
            j = 0
            while j <= len(data[i]) - 1:
                if j == 0:
                    item = QtGui.QTableWidgetItem(True)
                    item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    if self.toutCocher:
                        item.setCheckState(QtCore.Qt.Checked)
                    else:
                        item.setCheckState(QtCore.Qt.Unchecked)
                    self.ui.tableWidget.setItem(rowPosition, j, item)
                    if self.ui.tableWidget.item(rowPosition, 0).checkState():
                        if data[i][0] not in self.idsParcelletoPrint:
                            self.idsParcelletoPrint.append(data[i][0])
                    else:
                        if data[i][0] in self.idsParcelletoPrint:
                            self.idsParcelletoPrint.remove(data[i][0])
                    print self.idsParcelletoPrint
                else:
                    #print str(data[i][j])
                    item = QtGui.QTableWidgetItem()
                    item.setText(_translate("", str(data[i][j]), None))
                    self.ui.tableWidget.setItem(rowPosition, j, item)
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

        if self.ui.tableWidget.item(row, 0).checkState():
            if self.idparcelle not in self.idsParcelletoPrint:
                self.idsParcelletoPrint.append(self.idparcelle)
        else:
            if self.idparcelle in self.idsParcelletoPrint:
                self.idsParcelletoPrint.remove(self.idparcelle)

        print self.idsParcelletoPrint


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
        SQL = "SELECT DISTINCT pd.gid,pd.codeparcelle,pd.numero, f.nomfokontany  FROM parcelle_d pd, hameau h, fokontany f, contribuables_parcelle c " \
              "WHERE pd.idhameau = h.idhameau " \
              "AND h.idfokontany = f.idfokontany " \
              "AND pd.codeparcelle IS NOT NULL  " \
              "AND pd.gid = c.idparcelle AND pd.id_commune = %s"
        listeParams.append(globalvars.id_commune)
        flag = 1
        if self.ui.checkBox.isChecked():
            contribuable = "%" + data['contribuable'] + "%"
            if self.ui.lineEdit.text() != "":
                if self.idContribuable is not None:
                    SQL = SQL + " AND c.idpersonne = %s "
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
        self.cur.execute("SELECT nompersonne, prenompersonne FROM personne WHERE idpersonne = %s", (id,))
        data = self.cur.fetchone()
        infoContrib = str(data[0]).strip() + " " + str(data[1]).strip()
        self.ui.lineEdit.setText(infoContrib)


    def updateCheck(self):
        rowCount = self.ui.tableWidget.rowCount()
        i = 0
        if self.ui.checkBoxCocherTout.isChecked():
            self.toutCocher = True
            while i < rowCount:
                item = QtGui.QTableWidgetItem(True)
                item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                item.setCheckState(QtCore.Qt.Checked)
                self.ui.tableWidget.setItem(i, 0, item)
                if self.ui.tableWidget.item(i, 0).checkState():
                    if self.idParcelles[i] not in self.idsParcelletoPrint:
                        self.idsParcelletoPrint.append(self.idParcelles[i])
                i = i + 1
        else:
            self.toutCocher = False
            while i < rowCount:
                item = QtGui.QTableWidgetItem(True)
                item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                item.setCheckState(QtCore.Qt.Unchecked)
                self.ui.tableWidget.setItem(i, 0, item)
                if self.idParcelles[i] in self.idsParcelletoPrint:
                    self.idsParcelletoPrint.remove(self.idParcelles[i])
                i = i + 1
        print self.idsParcelletoPrint

    def initDB(self):
        self.cur = self.connection.cursor()

    def __del__(self):
        self.cur.close()

    def doPrint(self):
        #print "liste"
        #print self.idsParcelletoPrint
        # print nomfeuille
        feuille = self.book.add_sheet("Beneficiaire", True)
        styleTitreAvecFondGris = Style.easyxf(
            'font: bold on, height 140; align: wrap on, vert centre, horiz center; pattern: pattern solid, fore_colour gray25; borders: left 2, right 2, top 2, bottom 2')
        ### TITRE ####
        feuille.write(0, 0, 'Code', styleTitreAvecFondGris)
        feuille.write(0, 1, 'Numero CF',styleTitreAvecFondGris )
        feuille.write(0, 2, "Numero Demande", styleTitreAvecFondGris)
        feuille.write(0, 3, "Region", styleTitreAvecFondGris)
        feuille.write(0, 4, "District", styleTitreAvecFondGris)
        feuille.write(0, 5, "Commune", styleTitreAvecFondGris)
        feuille.write(0, 6, "Fokontany", styleTitreAvecFondGris)
        feuille.write(0, 7, "Hameau", styleTitreAvecFondGris)
        feuille.write(0, 8, "Date Saisie", styleTitreAvecFondGris)
        feuille.write(0, 9, "Date Modification", styleTitreAvecFondGris)
        feuille.write(0, 10, "Nom ", styleTitreAvecFondGris)
        feuille.write(0, 11, "Prenom", styleTitreAvecFondGris)
        feuille.write(0, 12, "Sexe", styleTitreAvecFondGris)
        feuille.write(0, 13, "Date de naissance", styleTitreAvecFondGris)
        feuille.write(0, 14, "Numero CIN", styleTitreAvecFondGris)
        feuille.write(0, 15, "Date CIN", styleTitreAvecFondGris)
        feuille.write(0, 16, "Lieu CIN", styleTitreAvecFondGris)
        feuille.write(0, 17, "Adresse", styleTitreAvecFondGris)
        feuille.write(0, 18, "Surface", styleTitreAvecFondGris)
        feuille.write(0, 19, "Beneficiaire", styleTitreAvecFondGris)


        if self.idsParcelletoPrint is not None:
            i = 1
            for idparcelle in self.idsParcelletoPrint:
                #print idparcelle
                try:
                    self.cur.execute("SELECT DISTINCT pd.codeparcelle, pd.numero, pd.gid, "
                                     "pd.conversion, pd.etatparcelle_d, h.nomhameau, f.nomfokontany, cp.idpersonne, "
                                     " dmd.numdemande, pd.etatparcelle_d, pd.consistance, c.numerocertificat, cm.nomcommune, "
                                     "dt.nomdistrict, rg.nomregion, ST_Area(pd.geom) "
                                     "FROM hameau h, fokontany f, "
                                     "commune cm, district dt, region rg, "
                                     "parcelle_d pd LEFT JOIN demande dmd ON  pd.gid = dmd.gid, "
                                     "parcelle_d LEFT JOIN certificat c ON parcelle_d.idcertificat = c.idcertificat,"
                                     "parcelle_d pd1 LEFT JOIN contribuables_parcelle cp ON pd1.gid = cp.idparcelle "
                                     "WHERE pd.idhameau = h.idhameau "
                                     "AND h.idfokontany = f.idfokontany "
                                     "AND f.idcommune = cm.idcommune "
                                     "AND cm.iddistrict = dt.iddistrict "
                                     "AND dt.idregion = rg.idregion "
                                     "AND pd.codeparcelle IS NOT NULL "
                                     "AND pd.gid = %s AND parcelle_d.gid = %s AND pd1.gid = %s AND cp.contribuable = %s", (idparcelle,idparcelle, idparcelle, True))
                    results = self.cur.fetchone()
                    print results
                    print 'out'
                    #print results[0]
                    if results is not None:
                        preData = {}
                        contribuableData = {}
                        codeparcelle = str(results[0]).strip()
                        if results[1] is not None:
                            preData['numero'] = str(results[1]).strip()
                        else:
                            preData['numero'] = ""
                        if results[2] is not None:
                            preData['gid'] = str(results[2]).strip()
                        else:
                            preData['gid'] = ""
                        if results[3] is not None:
                            preData['conversion'] = results[3]

                        else:
                            preData['conversion'] = ""

                        if results[5] is not None:
                            preData['nomhameau'] = str(results[5]).strip()
                        else:
                            preData['nomhameau'] = ""
                        if results[6] is not None:
                            preData['nomfokontany'] = str(results[6]).strip()
                        else:
                            preData['nomfokontany']
                        if results[8] is not None:
                            preData['numdemande'] = str(results[8]).strip()
                        else:
                            preData['numdemande'] = ""

                        preData['titre'] = ""
                        preData['cadastre'] = ""
                        preData['certificat'] = ""
                        preData['tsyvitatitre'] = ""
                        preData['autre'] = ""
                        if results[9] is not None:
                            if results[9] == 0:
                                preData['autre'] = "X"
                            elif results[9] == 1:
                                preData['titre'] = "X"
                            elif results[9] == 2:
                                preData['cadastre'] = "X"
                            elif results[9] == 3:
                                preData['certificat'] = "X"
                        ##consistance
                        preData['consistance'] = ""
                        if results[10] is not None:
                            preData['consistance'] = str(results[10]).strip()
                        #Numero CF
                        if results[11] is not None:
                            preData['numCF'] = str(results[11]).strip()
                        else:
                            preData['numCF'] = ""
                        #Territoire
                        if results[12] is not None:
                            preData['commune'] = str(results[12]).strip()
                        else:
                            preData['commune'] = ""
                        if results[13] is not None:
                            preData['district'] = str(results[13]).strip()
                        else:
                            preData['district'] = ""
                        if results[14] is not None:
                            preData['region'] = str(results[14]).strip()
                        else:
                            preData['region'] = ""
                        if results[15] is not None:
                            preData['surface'] = float(results[15])
                        else:
                            preData['surface'] = ""
                        ### MPIFANILA
                        preData['Nord'] = ""
                        preData['Sud'] = ""
                        preData['Est'] = ""
                        preData['Ouest'] = ""
                        try:
                            self.cur.execute("SELECT DISTINCT pc.position, lp.description "
                                             "FROM limitesparcelle lp, pointscardinaux pc "
                                             "WHERE lp.idpointscardinaux = pc.idpointscardinaux "
                                             "AND lp.idparcelle = %s", (idparcelle,))
                            limites = self.cur.fetchall()
                            for limite in limites:
                                if limite[0] == "Nord":
                                    preData['Nord'] = str(limite[1])
                                if limite[0] == "Sud":
                                    preData['Sud'] = str(limite[1])
                                if limite[0] == "Est":
                                    preData['Est'] = str(limite[1])
                                if limite[0] == "Ouest":
                                    preData['Ouest'] = str(limite[1])
                        except StandardError as e:
                            print(e)
                            self.connection.rollback()

                        ####TRAITEMENT CONTRIBUABLE#####
                        if results[7] is not None:
                            idcontribuable = int(results[7])
                            try:
                                self.cur.execute("SELECT nompersonne, prenompersonne, "
                                                 " datenaissancepersonne, lieunaissancepersonne, "
                                                 "numcipersonne, datecipersonne, lieucipersonne, "
                                                 "numactenaissancepersonne, dateactenaissancepersonne, "
                                                 "lieuactenaissancepersonne, adressepersonne, sexepersonne "
                                                 " FROM personne WHERE idpersonne = %s", (idcontribuable,))
                                tempData = self.cur.fetchone()
                                if tempData is not None:
                                    if tempData[0] is not None:
                                        contribuableData['nom'] = tempData[0]
                                    else:
                                        contribuableData['nom'] = ""
                                    if tempData[1] is not None:
                                        contribuableData['prenom'] = tempData[1]
                                    else:
                                        contribuableData['prenom'] = ""

                                    contribuableData['benef'] = contribuableData['nom'] + " " + contribuableData['prenom']

                                    if tempData[2] is not None:
                                        contribuableData['datenaissance'] = tempData[2].strftime('%d/%m/%Y')
                                    else:
                                        contribuableData['datenaissance'] = ""
                                    if tempData[3] is not None:
                                        contribuableData['lieunaissance'] = str(tempData[3]).strip()
                                    else:
                                        contribuableData['lieunaissance'] = ""
                                    if tempData[4] is not None:
                                        contribuableData['numactenaiss'] = ""
                                        contribuableData['dateactenaissance'] = ""
                                        contribuableData['lieuactenaissance'] = ""
                                        contribuableData['cin'] = ""
                                        contribuableData['cin'] += str(tempData[4][0:3]).strip() + "-"
                                        contribuableData['cin'] += str(tempData[4][3:6]).strip() + "-"
                                        contribuableData['cin'] += str(tempData[4][6:9]).strip() + "-"
                                        contribuableData['cin'] += str(tempData[4][9:len(tempData[4])]).strip()
                                        if tempData[5] is not None:
                                            contribuableData['datecin'] = tempData[5].strftime('%d/%m/%Y')
                                        else:
                                            contribuableData['datecin'] = ""
                                        if tempData[6] is not None:
                                            contribuableData['lieucin'] = str(tempData[6]).strip()
                                        else:
                                            contribuableData['lieucin'] = ""
                                    else:
                                        contribuableData['cin'] = ""
                                        contribuableData['datecin'] = ""
                                        contribuableData['lieucin'] = ""
                                        if tempData[7] is not None:
                                            contribuableData['numactenaiss'] = str(tempData[7]).strip()
                                        else:
                                            contribuableData['numactenaiss'] = ""
                                        if tempData[8] is not None:
                                            contribuableData['dateactenaissance'] = tempData[8].strftime('%d/%m/%Y')
                                        else:
                                            contribuableData['dateactenaissance'] = ""
                                        if tempData[9] is not None:
                                            contribuableData['lieuactenaissance'] = str(tempData[9]).strip()
                                        else:
                                            contribuableData['lieuactenaissance'] = ""
                                    if tempData[10] is not None:
                                        contribuableData['adresse'] = tempData[10]
                                    else:
                                        contribuableData['adresse'] = ""
                                    if tempData[11] is not None:
                                        contribuableData['sexe'] = str(tempData[11]).strip()
                                    else:
                                        contribuableData['sexe'] = ""

                            except StandardError as e:
                                print(e)
                                self.connection.rollback()
                        else:
                            contribuableData['nom'] = ""
                            contribuableData['prenom'] = ""
                            contribuableData['datenaissance'] = ""
                            contribuableData['lieunaissance'] = ""
                            contribuableData['datecin'] = ""
                            contribuableData['cin'] = ""
                            contribuableData['lieucin'] = ""
                            contribuableData['numactenaiss'] = ""
                            contribuableData['dateactenaissance'] = ""
                            contribuableData['lieuactenaissance'] = ""
                            contribuableData['adresse'] = ""
                            contribuableData['sexe'] = ""


                        styleCodeParcelle = Style.easyxf('font: bold on, height 240; align: wrap on, vert centre, horiz center; borders: left 2, right 2, top 2, bottom 2')
                        #xlwt.add_palette_colour("custom_colour", 0x21)
                        #self.book.set_colour_RGB(0x21,204,255,204)
                        styleTitreSansFond = Style.easyxf('font: bold on, height 140; align: wrap on, vert centre, horiz center; borders: left 2, right 2, top 2, bottom 2')
                        styleDonneeSansFond = Style.easyxf(
                            'font: height 140; align: wrap on, vert centre, horiz left; borders: left 2, right 2, top 2, bottom 2')

                        styleTitreAvecFond = Style.easyxf('font: bold on, height 140; align: wrap on, vert centre, horiz center; pattern: pattern solid, fore_colour light_green; borders: left 2, right 2, top 2, bottom 2')
                        styleTitreAvecFondBrGreen = Style.easyxf(
                            'font: bold on, height 140; align: wrap on, vert centre, horiz center; pattern: pattern solid, fore_colour bright_green; borders: left 2, right 2, top 2, bottom 2')
                        styleTitreAvecFondBleu = Style.easyxf(
                            'font: bold on, height 140; align: wrap on, vert centre, horiz center; pattern: pattern solid, fore_colour ice_blue ; borders: left 2, right 2, top 2, bottom 2')

                        feuille.write(i, 0, codeparcelle, styleDonneeSansFond)
                        feuille.write(i, 1, preData['numCF'], styleDonneeSansFond)
                        feuille.write(i, 2, preData['numdemande'], styleDonneeSansFond)
                        feuille.write(i, 3, preData['region'], styleDonneeSansFond)
                        feuille.write(i, 4, preData['district'], styleDonneeSansFond)
                        feuille.write(i, 5, preData['commune'], styleDonneeSansFond)
                        feuille.write(i, 6, preData['nomfokontany'], styleDonneeSansFond)
                        feuille.write(i, 7, preData['nomhameau'], styleDonneeSansFond)
                        feuille.write(i, 8, "", styleDonneeSansFond)
                        feuille.write(i, 9, "", styleDonneeSansFond)
                        feuille.write(i, 10, contribuableData['nom'], styleDonneeSansFond)
                        feuille.write(i, 11, contribuableData['prenom'], styleDonneeSansFond)
                        feuille.write(i, 12, contribuableData['sexe'], styleDonneeSansFond)
                        feuille.write(i, 13, contribuableData['datenaissance'], styleDonneeSansFond)
                        feuille.write(i, 14, contribuableData['cin'], styleDonneeSansFond)
                        feuille.write(i, 15, contribuableData['datecin'], styleDonneeSansFond)
                        feuille.write(i, 16, contribuableData['lieucin'], styleDonneeSansFond)
                        feuille.write(i, 17, contribuableData['adresse'], styleDonneeSansFond)
                        feuille.write(i, 18, preData['surface'], styleDonneeSansFond)
                        feuille.write(i, 19, contribuableData['benef'], styleDonneeSansFond)

                except StandardError as e:
                    print(e)
                    self.connection.rollback()

                i = i + 1

            dst = os.path.join(tempfile.gettempdir(), str(randint(10000, 99999)) + "-" + "Liste des beneficiaires.xls")
            #dst = os.path.dirname(__file__) + "/" + str(randint(10000, 99999)) + "-" + "Registre de demande.xls"
            self.book.save(dst)
            os.startfile(dst)



