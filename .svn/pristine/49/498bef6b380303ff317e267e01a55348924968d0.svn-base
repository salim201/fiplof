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

    def voirContribuable(self):
        self.contribuable.estConsultation(1)
        self.contribuable.exec_()

    def setIdContribuable(self):
        self.idContribuable = self.listePersonne.getIdPersonne()
        print "id contribuable = " + str(self.idContribuable)
        if self.idContribuable is not None:
            self.getContribuableById(self.idContribuable)
        self.listePersonne.close()

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
            self.cur.execute("SELECT pd.gid,pd.codeparcelle,pd.numero, f.nomfokontany  FROM parcelle_d pd, demande dmd, fokontany f " \
              "WHERE pd.gid = dmd.gid " \
              "AND dmd.idfokontany = f.idfokontany " \
              "AND pd.numdemande IS NOT NULL")
            data = self.cur.fetchall()
            print data
        #print "data"
            self.showInTable(data)
        except StandardError as e:
            print(e)
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
                    if data[i][j] is not None:
                        item.setText(_translate("", str(data[i][j]), None))
                    else:
                        item.setText(_translate("", "...", None))
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
        vtlayer = self.registry.mapLayersByName("Demandes Parcelle")[0]
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
        #SQL = "SELECT pd.gid,pd.codeparcelle,pd.numero, f.nomfokontany  FROM parcelle_d pd, hameau h, fokontany f " \
              #"WHERE pd.idhameau = h.idhameau " \
              #"AND h.idfokontany = f.idfokontany " \
              #"AND pd.numdemande IS NOT NULL AND pd.idcertificat IS NULL  " \
              #"AND pd.id_commune = %s "
        SQL = "SELECT pd.gid,pd.codeparcelle,pd.numero, f.nomfokontany  FROM parcelle_d pd, demande dmd, fokontany f " \
        "WHERE pd.gid = dmd.gid " \
        "AND dmd.idfokontany = f.idfokontany " \
        "AND pd.numdemande IS NOT NULL " \
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
        #self.cur.execute("SELECT p.nompersonne, p.prenompersonne FROM personne p INNER JOIN contribuables_parcelle cp ON p.idpersonne = cp.idpersonne WHERE idpersonne = %s AND contribuable = %s", (id,True))
        self.cur.execute(
            "SELECT p.nompersonne, p.prenompersonne FROM personne p INNER JOIN avoir_demande ad ON p.idpersonne = ad.idpersonne WHERE idpersonne = %s AND representant = %s",
            (id, True))
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
        print "liste"
        print self.idsParcelletoPrint
        print "liste OUT"
        #Recuperer le nom de la commune
        nomCommune = None
        try:
            self.cur.execute("SELECT nomcommune FROM commune WHERE idcommune = %s", (globalvars.id_commune, ))
            nomCommune = self.cur.fetchone()[0]
        except StandardError as e:
            print e
            self.connection.rollback()

        if self.idsParcelletoPrint is not None:
            for idparcelle in self.idsParcelletoPrint:
                #print idparcelle
                try:
                    #self.cur.execute("SELECT DISTINCT pd.codeparcelle, pd.numero, pd.gid, "
                                     #"pd.conversion, pd.etatparcelle_d, h.nomhameau, f.nomfokontany, ad.idpersonne, "
                                     #" dmd.numdemande, pd.etatparcelle_d, pd.consistance, c.numerocertificat, cm.nomcommune, "
                                     #"dt.nomdistrict, rg.nomregion, ST_Area(pd.geom), dmd.datedemande "
                                     #"FROM hameau h, fokontany f, avoir_demande ad, "
                                     #"commune cm, district dt, region rg, "
                                     #"parcelle_d pd LEFT JOIN demande dmd ON  pd.gid = dmd.gid, "
                                     #"parcelle_d LEFT JOIN certificat c ON parcelle_d.idcertificat = c.idcertificat "
                                     #"WHERE pd.idhameau = h.idhameau "
                                     #"AND h.idfokontany = f.idfokontany "
                                     #"AND f.idcommune = cm.idcommune "
                                     #"AND cm.iddistrict = dt.iddistrict "
                                     #"AND dt.idregion = rg.idregion "
                                     #"AND ad.idparcelle = pd.gid "
                                     #"AND pd.numdemande IS NOT NULL "
                                     #"AND pd.gid = %s AND parcelle_d.gid = %s"
                                     #" AND ad.representant = %s AND pd.id_commune = %s", (idparcelle,idparcelle, True, globalvars.id_commune))

                    self.cur.execute("SELECT DISTINCT pd.codeparcelle, pd.numero, pd.gid, "
                                     "pd.conversion, pd.etatparcelle_d, f.nomfokontany, f.nomfokontany, ad.idpersonne, "
                                     " dmd.numdemande, pd.etatparcelle_d, pd.consistance, pd.consistance, cm.nomcommune, "
                                     "dt.nomdistrict, rg.nomregion, ST_Area(pd.geom), dmd.datedemande, dmd.iddemande "
                                     "FROM hameau h, fokontany f, avoir_demande ad, "
                                     "commune cm, district dt, region rg, "
                                     "parcelle_d pd LEFT JOIN demande dmd ON  pd.gid = dmd.gid "
                                     "WHERE dmd.idfokontany = f.idfokontany "
                                     "AND dmd.numdemande = pd.numdemande "
                                     "AND f.idcommune = cm.idcommune "
                                     "AND cm.iddistrict = dt.iddistrict "
                                     "AND dt.idregion = rg.idregion "
                                     "AND ad.idparcelle = pd.gid "
                                     "AND pd.numdemande IS NOT NULL "
                                     "AND pd.gid = %s "
                                     "AND pd.id_commune = %s",
                                     (idparcelle, globalvars.id_commune))
                    results = self.cur.fetchone()

                    print results
                    print 'out'
                    #print results[0]
                    if results is not None:
                        preData = {}
                        batData = []
                        codeparcelle = None
                        if results[0] is not None:
                            codeparcelle = str(results[0]).strip()
                        else:
                            codeparcelle = str(results[8]).strip()
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
                            #preData['nomhameau'] = str(results[5]).strip() le hameau n'existe pas actuelle au niveau de la demande mais il faut l'ajouter au niveau de la demande lors des patch
                            preData['nomhameau'] = ""
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

                        if results[16] is not None:
                            preData['datedemande'] = results[16].strftime('%d/%m/%Y')
                        else:
                            preData['datedemande'] = ""

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

                        ####Traiter opposition ####
                        tempOpp = None
                        if results[17] is not None:
                            try:
                                self.cur.execute("SELECT description, dateopposition FROM oppositions WHERE iddemande = %s", (results[17], ))
                                tempOpp = self.cur.fetchall()
                            except StandardError as e:
                                print e
                                self.connection.rollback()

                        tabOpp = []
                        if tempOpp is not None:
                            for tempOp in tempOpp:
                                opposition = {}
                                opposition['desc'] = tempOp[0]
                                opposition['date'] = tempOp[1].strftime('%d/%m/%Y')
                                tabOpp.append(opposition)

                        print "Tab opposition = " + str(tabOpp)

                        ####TRAITEMENT CONTRIBUABLES#####
                        tempContribuables = None
                        try:
                            self.cur.execute("SELECT p.nompersonne, p.prenompersonne, "
                                             "p.datenaissancepersonne, p.lieunaissancepersonne, "
                                             "p.numcipersonne, p.datecipersonne, p.lieucipersonne, "
                                             "p.numactenaissancepersonne, p.dateactenaissancepersonne, "
                                             "p.lieuactenaissancepersonne, p.adressepersonne, ad.representant, "
                                             "p.sexepersonne, p.nompere, p.nommere "
                                             "FROM personne p INNER JOIN avoir_demande ad ON p.idpersonne = ad.idpersonne WHERE "
                                             "ad.idparcelle = %s", (idparcelle, ))
                            tempContribuables = self.cur.fetchall()
                        except StandardError as e:
                            print e
                            self.connection.rollback()

                        tabContribuables = []
                        if tempContribuables is not None:
                            for tempData in tempContribuables:
                                contribuableData = {}
                                if tempData[0] is not None:
                                    contribuableData['nom'] = tempData[0]
                                else:
                                    contribuableData['nom'] = ""
                                if tempData[1] is not None:
                                    contribuableData['prenom'] = tempData[1]
                                else:
                                    contribuableData['prenom'] = ""
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
                                if tempData[12] is not None:
                                    if tempData == "masculin":
                                        contribuableData['sexe'] = 'L'
                                    elif tempData == "feminin":
                                        contribuableData['sexe'] = 'V'
                                    else:
                                        contribuableData['sexe'] = ''
                                else:
                                    contribuableData['sexe'] = ''
                                if tempData[13] is not None:
                                    contribuableData['nompere'] = unicode(tempData[13]).strip()
                                else:
                                    contribuableData['nompere'] = ""
                                if tempData[14] is not None:
                                    contribuableData['nommere'] = unicode(tempData[14]).strip()
                                else:
                                    contribuableData['nommere'] = ""


                                tabContribuables.append(contribuableData)

                        print "table contribuables = " + str(tabContribuables)

                            ####TRAITEMENT BATIMENT#####

                        try:
                            self.cur.execute("SELECT c.libelleconsistance "
                                                     " FROM consistance c INNER JOIN batiment b ON c.idconsistance = b.idconsistance WHERE b.idparcelle = %s", (idparcelle,))
                            tempData = self.cur.fetchall()
                            print "Donnees batiment = " + str(tempData)
                            if tempData is not None:
                                for dt in tempData:
                                    batData.append(str(dt[0]).strip())

                        except StandardError as e:
                            print(e)
                            self.connection.rollback()



                        styleCodeParcelle = Style.easyxf('font: bold on, height 240; align: wrap on, vert centre, horiz center; borders: left 2, right 2, top 2, bottom 2')
                        #xlwt.add_palette_colour("custom_colour", 0x21)
                        #self.book.set_colour_RGB(0x21,204,255,204)
                        styleTitreSansFond = Style.easyxf('font: bold on, height 140; align: wrap on, vert centre, horiz center; borders: left 2, right 2, top 2, bottom 2')
                        styleDonneeSansFond = Style.easyxf(
                            'font: height 140; align: wrap on, vert centre, horiz left; borders: left 2, right 2, top 2, bottom 2')
                        styleTitreSouligne = Style.easyxf('font: bold on, height 150, underline on; align: wrap on, vert centre, horiz left')
                        #styleDonnees = Style.easyxf('font: bold on, height 140; align: wrap on, vert centre, horiz center; borders: left 1, right 1, top 1, bottom 1')

                        styleTitreAvecFond = Style.easyxf('font: bold on, height 140; align: wrap on, vert centre, horiz center; pattern: pattern solid, fore_colour light_green; borders: left 2, right 2, top 2, bottom 2')
                        styleTitreAvecFondBrGreen = Style.easyxf(
                            'font: bold on, height 140; align: wrap on, vert centre, horiz center; pattern: pattern solid, fore_colour bright_green; borders: left 2, right 2, top 2, bottom 2')
                        styleTitreAvecFondGris = Style.easyxf(
                            'font: bold on, height 140; align: wrap on, vert centre, horiz center; pattern: pattern solid, fore_colour gray25; borders: left 2, right 2, top 2, bottom 2')
                        styleTitreAvecFondBleu = Style.easyxf(
                            'font: bold on, height 140; align: wrap on, vert centre, horiz center; pattern: pattern solid, fore_colour ice_blue ; borders: left 2, right 2, top 2, bottom 2')
                        ### TITRE ####
                        ligne = 0
                        # print nomfeuille
                        feuille = None
                        print "codeparcelle = " + str(codeparcelle)
                        feuille = self.book.add_sheet(codeparcelle, True)

                        feuille.write(ligne, 0 ,'KAOMININA',styleTitreAvecFond)
                        feuille.write(ligne, 1, "FOKONTANY", styleTitreAvecFond)
                        feuille.merge(ligne, 0, 1, 3, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 4, 'VOHITRA', styleTitreAvecFond)
                        feuille.merge(ligne, 0, 4, 5, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 6, 'VAKIMPARITRA', styleTitreAvecFond)
                        feuille.merge(ligne, 0, 6, 7, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 8, "KAODIN'NY TANY", styleTitreAvecFond)
                        feuille.merge(ligne, 0, 8, 9, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 10, "LAHARAN'NY FANGATAHANA", styleTitreAvecFond)
                        feuille.merge(ligne, 0, 10, 11, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))

                        #feuille.write(0, 1, codeparcelle, styleCodeParcelle)
                        ### Ligne 1 ####
                        ligne = ligne + 1
                        feuille.write(ligne, 0, nomCommune, styleDonneeSansFond)
                        feuille.write(ligne, 1, preData['nomfokontany'], styleDonneeSansFond)
                        feuille.merge(ligne, ligne, 1, 3, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 4, preData['nomhameau'], styleDonneeSansFond)
                        feuille.merge(ligne, ligne, 4, 5, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 6, "Vakimparitra", styleDonneeSansFond)
                        feuille.merge(ligne, ligne, 6, 7, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 8, codeparcelle, styleTitreSansFond)
                        feuille.merge(ligne, ligne, 8, 9, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 10, preData['numdemande'],styleTitreSansFond )
                        feuille.merge(ligne, ligne, 10, 11,Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))

                        ###Ligne 2 ####
                        ligne = ligne + 1
                        feuille.write(ligne, 0, "Daty ny fangatahana", styleTitreAvecFond)
                        feuille.write(ligne, 1, preData['datedemande'],styleDonneeSansFond )
                        feuille.merge(ligne, ligne,1, 2,Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 3, "MPANAO FANISANA", styleTitreAvecFond)
                        feuille.merge(ligne, ligne, 3, 4, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 5, "", styleDonneeSansFond)
                        feuille.merge(ligne, ligne, 5, 8, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 9, "SONIA SR", styleTitreSansFond)
                        feuille.merge(ligne, ligne + 1, 9, 9, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 10, "", styleTitreSansFond)
                        feuille.merge(ligne, ligne + 1, 10, 11,  Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 12, "TETIK'ASA", styleTitreAvecFond)
                        feuille.merge(ligne, ligne, 12, 13, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne + 1, 12, "", styleDonneeSansFond)
                        feuille.merge(ligne + 1, ligne + 1, 12, 13, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))

                        ### Ligne 3 ###
                        ligne = ligne + 1
                        feuille.write(ligne, 0, "MOMBAMOMBAN'NY MPANGATAKA", styleTitreSouligne)
                        feuille.merge(ligne, ligne, 0, 1,  Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))

                        ### Ligne 4 ###
                        ligne = ligne + 1
                        feuille.write(ligne, 1, "OLON-TSOTRA",styleTitreSansFond )
                        feuille.merge(ligne, ligne, 1, 2, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))

                        ### Ligne 5 ###
                        ligne = ligne + 1
                        feuille.write(ligne, 1, "HAFA", styleTitreSansFond)
                        feuille.write(ligne, 2, "",styleTitreSansFond )
                        feuille.write(ligne, 3, "FIKAMBANANA",styleTitreSansFond)
                        feuille.write(ligne, 4, "",  styleTitreSansFond)
                        feuille.write(ligne, 5, "FIANGONANA",styleTitreSansFond )
                        feuille.write(ligne, 6, "", styleTitreSansFond)
                        feuille.write(ligne, 7, "SEKOLY", styleTitreSansFond)
                        feuille.write(ligne, 8, "", styleTitreSansFond)
                        feuille.write(ligne, 9, "FANJAKANA", styleTitreSansFond)
                        feuille.write(ligne, 10, "", styleTitreSansFond)

                        ### Ligne 6 ####
                        ligne = ligne + 1

                        ### Ligne 7 ###
                        ligne = ligne + 1
                        feuille.write(ligne, 0, "ANARANA", styleTitreSansFond)
                        feuille.merge(ligne, ligne, 0, 1, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 2, "FANAMPIN'ANARANA", styleTitreSansFond)
                        feuille.merge(ligne, ligne, 2, 4, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 5, "DATY NAHATERAHANA / NIORENANA", styleTitreSansFond)
                        feuille.write(ligne, 6, "TAO",styleTitreSansFond )
                        feuille.merge(ligne, ligne,6, 7, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 8, "LAHY / VAVY", styleTitreSansFond)
                        feuille.write(ligne, 9, u"CIN / ACTE N° / N° KOPIA", styleTitreSansFond)
                        feuille.merge(ligne, ligne, 9, 10,Style.easyxf(' borders: left 2, right 2, top 2, bottom 2') )
                        feuille.write(ligne, 11, "DATY NAHAZOANA / TOERANA", styleTitreSansFond)
                        feuille.write(ligne, 12, "(D)/(C) / (VD)/(T)", styleTitreSansFond)
                        feuille.write(ligne, 13, "RAY SY RENY", styleTitreSansFond)
                        feuille.write(ligne, 14, "ADIRESY", styleTitreSansFond)

                        #Boucle du tableau
                        ligne = ligne + 1
                        finboucle = ligne + 10
                        iterContribuable = 0
                        while ligne < finboucle:
                            if tabContribuables is not None:
                                if iterContribuable < len(tabContribuables):
                                    feuille.write(ligne, 0, tabContribuables[iterContribuable]['nom'], styleTitreSansFond)
                                    feuille.merge(ligne, ligne, 0, 1,
                                                  Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                                    feuille.write(ligne, 2,  tabContribuables[iterContribuable]['prenom'], styleTitreSansFond)
                                    feuille.merge(ligne, ligne, 2, 4,
                                                  Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                                    feuille.write(ligne, 5, tabContribuables[iterContribuable]['datenaissance'], styleTitreSansFond)
                                    feuille.write(ligne, 6, tabContribuables[iterContribuable]['lieunaissance'], styleTitreSansFond)
                                    feuille.merge(ligne, ligne, 6, 7,
                                                  Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                                    feuille.write(ligne, 8, tabContribuables[iterContribuable]['sexe'] , styleTitreSansFond)
                                    #identite
                                    if tabContribuables[iterContribuable]['cin'] != "":
                                        feuille.write(ligne, 9, tabContribuables[iterContribuable]['cin'], styleTitreSansFond)
                                    else:
                                        feuille.write(ligne, 9, tabContribuables[iterContribuable]['numactenaiss'],
                                                      styleTitreSansFond)
                                    feuille.merge(ligne, ligne, 9, 10,
                                                  Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                                    #"date et lieu identite"
                                    if tabContribuables[iterContribuable]['datecin'] != "":
                                        feuille.write(ligne, 11,tabContribuables[iterContribuable]['datecin'] , styleTitreSansFond)
                                    else:
                                        feuille.write(ligne, 11, tabContribuables[iterContribuable]['dateactenaissance'],
                                                      styleTitreSansFond)
                                    feuille.write(ligne, 12, "", styleTitreSansFond)
                                    #Ray sy reny
                                    feuille.write(ligne, 13, tabContribuables[iterContribuable]['nompere'] + " ; " + tabContribuables[iterContribuable]['nommere'], styleTitreSansFond)
                                    #adiresy
                                    feuille.write(ligne, 14, tabContribuables[iterContribuable]['adresse'], styleTitreSansFond)
                                else:
                                    feuille.write(ligne, 0, "", styleTitreSansFond)
                                    feuille.merge(ligne, ligne, 0, 1,
                                                  Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                                    feuille.write(ligne, 2, "", styleTitreSansFond)
                                    feuille.merge(ligne, ligne, 2, 4,
                                                  Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                                    feuille.write(ligne, 5, "", styleTitreSansFond)
                                    feuille.write(ligne, 6, "", styleTitreSansFond)
                                    feuille.merge(ligne, ligne, 6, 7,
                                                  Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                                    feuille.write(ligne, 8, "", styleTitreSansFond)
                                    feuille.write(ligne, 9, u"", styleTitreSansFond)
                                    feuille.merge(ligne, ligne, 9, 10,
                                                  Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                                    feuille.write(ligne, 11, "", styleTitreSansFond)
                                    feuille.write(ligne, 12, "", styleTitreSansFond)
                                    feuille.write(ligne, 13, "", styleTitreSansFond)
                                    feuille.write(ligne, 14, "", styleTitreSansFond)
                            else:
                                feuille.write(ligne, 0, "", styleTitreSansFond)
                                feuille.merge(ligne, ligne, 0, 1,
                                              Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                                feuille.write(ligne, 2, "", styleTitreSansFond)
                                feuille.merge(ligne, ligne, 2, 4,
                                              Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                                feuille.write(ligne, 5, "", styleTitreSansFond)
                                feuille.write(ligne, 6, "", styleTitreSansFond)
                                feuille.merge(ligne, ligne, 6, 7,
                                              Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                                feuille.write(ligne, 8, "", styleTitreSansFond)
                                feuille.write(ligne, 9, u"", styleTitreSansFond)
                                feuille.merge(ligne, ligne, 9, 10,
                                              Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                                feuille.write(ligne, 11, "", styleTitreSansFond)
                                feuille.write(ligne, 12, "", styleTitreSansFond)
                                feuille.write(ligne, 13, "", styleTitreSansFond)
                                feuille.write(ligne, 14, "", styleTitreSansFond)

                            ligne = ligne + 1
                            iterContribuable = iterContribuable + 1

                        #feuille.write(ligne, 0, "MOMBAMOBAN'ILAY TANY")

                        #ligne = ligne + 1

                        feuille.write(ligne, 0, "MOMBAMOMBAN'ILAY TANY", styleTitreAvecFondBleu)
                        feuille.merge(ligne, ligne, 0, 13, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        ### ligne 20 ###
                        ligne = ligne + 1
                        feuille.write(ligne, 0, "SATAN'NY TANY", styleTitreAvecFondBrGreen)
                        feuille.merge(ligne, ligne, 0, 1, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 3, "MPIFANILA TANY", styleTitreAvecFondBrGreen)
                        feuille.merge(ligne, ligne, 3, 6, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 8, "ZAVATRA MISY", styleTitreAvecFondBrGreen)
                        feuille.merge(ligne, ligne, 8, 9, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 11, "MOMBAN'NY TRANO", styleTitreAvecFondGris)
                        feuille.merge(ligne, ligne, 11, 13, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 14, "SARAN'NY KARATANY NALOA", styleTitreAvecFond)
                        feuille.merge(ligne, ligne, 14, 15, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne + 1, 14, "", styleTitreSansFond)
                        feuille.merge(ligne + 1, ligne + 2, 14, 15, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne + 3, 14, u"ROSIA N°", styleTitreAvecFond)
                        feuille.merge(ligne + 3, ligne + 3, 14, 15, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne + 4, 14, "", styleTitreSansFond)
                        feuille.merge(ligne + 4, ligne + 5, 14, 15, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))

                        # Ligne 21
                        ligne = ligne + 1
                        feuille.write(ligne, 0, "TITRA", styleTitreAvecFond)
                        feuille.write(ligne, 1, preData['titre'], styleTitreSansFond)
                        feuille.write(ligne, 3, "Avaratra", styleTitreAvecFond)
                        feuille.write(ligne, 4, preData['Nord'], styleDonneeSansFond)
                        feuille.merge(ligne, ligne, 4, 6, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 8, preData['consistance'], styleDonneeSansFond)
                        feuille.merge(ligne, ligne, 8, 9, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 11, u"N°", styleTitreAvecFond)
                        feuille.write(ligne, 12, "Sokajy", styleTitreAvecFond)
                        feuille.merge(ligne, ligne, 12, 13, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        # Ligne 22
                        ligne = ligne + 1
                        feuille.write(ligne, 0, "KADASITRA", styleTitreAvecFond)
                        feuille.write(ligne, 1, preData['cadastre'], styleTitreSansFond)
                        feuille.write(ligne, 3, "Andrefana", styleTitreAvecFond)
                        feuille.write(ligne, 4, preData['Ouest'], styleDonneeSansFond)
                        feuille.merge(ligne, ligne, 4, 6, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 8, "FAHARETAN'NY FANAJARIANA", styleTitreAvecFond)
                        feuille.merge(ligne, ligne, 8, 9, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 11, u"T1", styleTitreAvecFond)
                        if len(batData) >= 1:
                            feuille.write(ligne, 12, batData[0], styleDonneeSansFond)
                        else:
                            feuille.write(ligne, 12, "", styleDonneeSansFond)
                        feuille.merge(ligne, ligne, 12, 13, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        # Ligne 23
                        ligne = ligne + 1
                        feuille.write(ligne, 0, "KARATANY", styleTitreAvecFond)
                        feuille.write(ligne, 1, preData['certificat'], styleTitreSansFond)
                        feuille.write(ligne, 3, "Atsimo", styleTitreAvecFond)
                        feuille.write(ligne, 4, preData['Sud'], styleDonneeSansFond)
                        feuille.merge(ligne, ligne, 4, 6, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 8, "", styleDonneeSansFond)
                        feuille.merge(ligne, ligne, 8, 9, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 11, u"T2", styleTitreAvecFond)
                        try :
                            if len(batData) >= 2:
                                feuille.write(ligne, 12, batData[1], styleDonneeSansFond)
                            else:
                                feuille.write(ligne, 12, "", styleDonneeSansFond)
                        except Exception as e:
                            pass
                        # feuille.write(18, 12, "", styleDonneeSansFond)
                        feuille.merge(ligne, ligne, 12, 13, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        # Ligne 24
                        ligne = ligne + 1
                        feuille.write(ligne, 0, "TSY VITA TITRA", styleTitreAvecFond)
                        feuille.write(ligne, 1, preData['tsyvitatitre'], styleTitreSansFond)
                        feuille.write(ligne, 3, "Atsinanana", styleTitreAvecFond)
                        feuille.write(ligne, 4, preData['Est'], styleDonneeSansFond)
                        feuille.merge(ligne, ligne, 4, 6, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        #feuille.write(ligne, 8, "Vola naloa", styleTitreAvecFond)
                        #feuille.write(ligne, 9, u"Quittance n°", styleTitreAvecFond)
                        # feuille.merge(18, 18, 8, 9, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 11, u"T3", styleTitreAvecFond)
                        if len(batData) >= 3:
                            feuille.write(ligne, 12, batData[2], styleDonneeSansFond)
                        else:
                            feuille.write(ligne, 12, "", styleDonneeSansFond)
                        feuille.merge(ligne, ligne, 12, 13, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        # Ligne 25
                        ligne = ligne + 1
                        feuille.write(ligne, 0, "HAFA", styleTitreAvecFond)
                        feuille.write(ligne, 1, preData['autre'], styleTitreSansFond)
                        # feuille.write(19, 3, "Atsinanana", styleTitreAvecFond)
                        # feuille.write(19, 4, "", styleDonneeSansFond)
                        # feuille.merge(19, 19, 4, 6, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        #feuille.write(ligne, 8, "", styleDonneeSansFond)
                        #feuille.write(ligne, 9, "", styleDonneeSansFond)
                        # feuille.merge(18, 18, 8, 9, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 11, u"T4", styleTitreAvecFond)
                        if len(batData) >= 4:
                            feuille.write(ligne, 12, batData[3], styleDonneeSansFond)
                        else:
                            feuille.write(ligne, 12, "", styleDonneeSansFond)
                        feuille.merge(ligne, ligne, 12, 13, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        # Ligne 27
                        ligne = ligne + 2
                        feuille.write(ligne, 0, "FANAPAHANA", styleTitreAvecFondBrGreen)
                        feuille.merge(ligne, ligne, 0, 1, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 3, "FANOHANANA", styleTitreAvecFondBrGreen)
                        feuille.merge(ligne, ligne, 3, 7, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        # Ligne 28
                        ligne = ligne + 1
                        feuille.write(ligne, 0, "Laharana", styleTitreAvecFond)
                        feuille.write(ligne, 1, "Daty", styleTitreAvecFond)
                        feuille.write(ligne, 3, "ANARAN'NY MPANOHANA", styleTitreAvecFond)
                        feuille.merge(ligne, ligne, 3, 4, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 5, "Antony", styleTitreAvecFond)
                        feuille.merge(ligne, ligne, 5, 6, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 7, "Daty", styleTitreAvecFond)
                        # Ligne 29
                        ligne = ligne + 1
                        feuille.write(ligne, 0, "", styleDonneeSansFond)
                        feuille.write(ligne, 1, "", styleDonneeSansFond)
                        feuille.write(ligne, 3, "", styleDonneeSansFond)
                        feuille.merge(ligne, ligne, 3, 4, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        if len(tabOpp) > 0:
                            i = 0
                            while i < len(tabOpp):
                                feuille.write(ligne + i, 5, tabOpp[i]['desc'], styleDonneeSansFond)
                                i += 1
                        feuille.merge(ligne, ligne, 5, 6, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        if len(tabOpp) > 0:
                            i = 0
                            while i < len(tabOpp):
                                feuille.write(ligne + i, 7, tabOpp[i]['date'], styleDonneeSansFond)
                                i += 1
                        # ligne 30
                        ligne = ligne + 1
                        feuille.write(ligne, 3, "", styleDonneeSansFond)
                        feuille.merge(ligne, ligne, 3, 4, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 5, "", styleDonneeSansFond)
                        feuille.merge(ligne, ligne, 5, 6, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        # Ligne 27
                        ligne = ligne + 1
                        feuille.write(ligne, 0, "FITSIRIHANA", styleTitreAvecFondBrGreen)
                        feuille.merge(ligne, ligne, 0, 1, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 3, "", styleDonneeSansFond)
                        feuille.merge(ligne, ligne, 3, 4, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 5, "", styleDonneeSansFond)
                        feuille.merge(ligne, ligne, 5, 6, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        # Ligne 28
                        ligne = ligne + 1
                        feuille.write(ligne, 0, "Laharana", styleTitreAvecFond)
                        feuille.write(ligne, 1, "Daty", styleTitreAvecFond)
                        feuille.write(ligne, 3, "", styleDonneeSansFond)
                        feuille.merge(ligne, ligne, 3, 4, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne, 5, "", styleDonneeSansFond)
                        feuille.merge(ligne, ligne, 5, 6, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        # Ligne 29
                        ligne = ligne + 1
                        feuille.write(ligne, 0, "", styleDonneeSansFond)
                        feuille.write(ligne, 1, "", styleDonneeSansFond)
                        # Extra line
                        texte = "Ireo voalaza anarana ato dia manao fangatahana karatany amin'ity tany voalaza ity." \
                                "Raha mihoatra ny olona iray (01) ny mpangataka dia adika amin'ny takelaka fanampiny ny lisitra sy ny mombamomba ireo mpiara mangataka ary ny soniany SONIAN'NY MPANGATAKA"
                        feuille.write(26, 8, texte, styleTitreSansFond)
                        feuille.merge(26, 32, 8, 13, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                        feuille.write(ligne + 2, 0, "FANAMARIHANA : LAHY (L) / VAVY (v) MPANGATAKA (D)/ MPIARAMANGATAKA(C)  /VADY MIARA TOMPONY(VD)/ MPIANTOKA(T)", styleTitreSansFond)
                        feuille.merge(ligne + 2, ligne + 2, 0, 13,  Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))

                        if iterContribuable < len(tabContribuables):
                            feuilleFicheCodemandeur = self.book.add_sheet(str(codeparcelle) + "-codem", True)
                            ligne = 0 #Retour a zero de la variable ligne
                            feuilleFicheCodemandeur.write(ligne, 0, 'KAOMININA', styleTitreAvecFond)
                            feuilleFicheCodemandeur.write(ligne, 1, "FOKONTANY", styleTitreAvecFond)
                            feuilleFicheCodemandeur.merge(ligne, 0, 1, 3, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                            feuilleFicheCodemandeur.write(ligne, 4, 'VOHITRA', styleTitreAvecFond)
                            feuilleFicheCodemandeur.merge(ligne, 0, 4, 5, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                            feuilleFicheCodemandeur.write(ligne, 6, 'VAKIMPARITRA', styleTitreAvecFond)
                            feuilleFicheCodemandeur.merge(ligne, 0, 6, 7, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                            feuilleFicheCodemandeur.write(ligne, 8, "KAODIN'NY TANY", styleTitreAvecFond)
                            feuilleFicheCodemandeur.merge(ligne, 0, 8, 9, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                            feuilleFicheCodemandeur.write(ligne, 10, "LAHARAN'NY FANGATAHANA", styleTitreAvecFond)
                            feuilleFicheCodemandeur.merge(ligne, 0, 10, 11, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))

                            # feuille.write(0, 1, codeparcelle, styleCodeParcelle)
                            ### Ligne 1 ####
                            ligne = ligne + 1
                            feuilleFicheCodemandeur.write(ligne, 0, nomCommune, styleDonneeSansFond)
                            feuilleFicheCodemandeur.write(ligne, 1, preData['nomfokontany'], styleDonneeSansFond)
                            feuilleFicheCodemandeur.merge(ligne, ligne, 1, 3, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                            feuilleFicheCodemandeur.write(ligne, 4, preData['nomhameau'], styleDonneeSansFond)
                            feuilleFicheCodemandeur.merge(ligne, ligne, 4, 5, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                            feuilleFicheCodemandeur.write(ligne, 6, "Vakimparitra", styleDonneeSansFond)
                            feuilleFicheCodemandeur.merge(ligne, ligne, 6, 7, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                            feuilleFicheCodemandeur.write(ligne, 8, codeparcelle, styleTitreSansFond)
                            feuilleFicheCodemandeur.merge(ligne, ligne, 8, 9, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                            feuilleFicheCodemandeur.write(ligne, 10, preData['numdemande'], styleTitreSansFond)
                            feuilleFicheCodemandeur.merge(ligne, ligne, 10, 11, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))

                            ###Ligne 2 ####
                            ligne = ligne + 1
                            feuilleFicheCodemandeur.write(ligne, 0, "Daty ny fangatahana", styleTitreAvecFond)
                            feuilleFicheCodemandeur.write(ligne, 1, "", styleDonneeSansFond)
                            feuilleFicheCodemandeur.merge(ligne, ligne, 1, 2, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                            feuilleFicheCodemandeur.write(ligne, 3, "MPANAO FANISANA", styleTitreAvecFond)
                            feuilleFicheCodemandeur.merge(ligne, ligne, 3, 4, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                            feuilleFicheCodemandeur.write(ligne, 5, "", styleDonneeSansFond)
                            feuilleFicheCodemandeur.merge(ligne, ligne, 5, 8, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                            feuilleFicheCodemandeur.write(ligne, 9, "SONIA SR", styleTitreSansFond)
                            feuilleFicheCodemandeur.merge(ligne, ligne + 1, 9, 9,
                                          Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                            feuilleFicheCodemandeur.write(ligne, 10, "", styleTitreSansFond)
                            feuilleFicheCodemandeur.merge(ligne, ligne + 1, 10, 11,
                                          Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                            feuilleFicheCodemandeur.write(ligne, 12, "TETIK'ASA", styleTitreAvecFond)
                            feuilleFicheCodemandeur.merge(ligne, ligne, 12, 13, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                            feuilleFicheCodemandeur.write(ligne + 1, 12, "", styleDonneeSansFond)
                            feuilleFicheCodemandeur.merge(ligne + 1, ligne + 1, 12, 13,
                                          Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))

                            ### Ligne 3 ###
                            ligne = ligne + 1
                            feuilleFicheCodemandeur.write(ligne, 0, "MOMBAMOMBAN'NY MPANGATAKA", styleTitreSouligne)
                            feuilleFicheCodemandeur.merge(ligne, ligne, 0, 1, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))

                            ### Ligne 4 ###
                            ligne = ligne + 1
                            feuilleFicheCodemandeur.write(ligne, 1, "OLON-TSOTRA", styleTitreSansFond)
                            feuilleFicheCodemandeur.merge(ligne, ligne, 1, 2, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))

                            ### Ligne 5 ###
                            ligne = ligne + 1
                            feuilleFicheCodemandeur.write(ligne, 1, "HAFA", styleTitreSansFond)
                            feuilleFicheCodemandeur.write(ligne, 2, "", styleTitreSansFond)
                            feuilleFicheCodemandeur.write(ligne, 3, "FIKAMBANANA", styleTitreSansFond)
                            feuilleFicheCodemandeur.write(ligne, 4, "", styleTitreSansFond)
                            feuilleFicheCodemandeur.write(ligne, 5, "FIANGONANA", styleTitreSansFond)
                            feuilleFicheCodemandeur.write(ligne, 6, "", styleTitreSansFond)
                            feuilleFicheCodemandeur.write(ligne, 7, "SEKOLY", styleTitreSansFond)
                            feuilleFicheCodemandeur.write(ligne, 8, "", styleTitreSansFond)
                            feuilleFicheCodemandeur.write(ligne, 9, "FANJAKANA", styleTitreSansFond)
                            feuilleFicheCodemandeur.write(ligne, 10, "", styleTitreSansFond)

                            ### Ligne 6 ####
                            ligne = ligne + 1

                            ### Ligne 7 ###
                            ligne = ligne + 1
                            feuilleFicheCodemandeur.write(ligne, 0, "ANARANA", styleTitreSansFond)
                            feuilleFicheCodemandeur.merge(ligne, ligne, 0, 1, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                            feuilleFicheCodemandeur.write(ligne, 2, "FANAMPIN'ANARANA", styleTitreSansFond)
                            feuilleFicheCodemandeur.merge(ligne, ligne, 2, 4, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                            feuilleFicheCodemandeur.write(ligne, 5, "DATY NAHATERAHANA / NIORENANA", styleTitreSansFond)
                            feuilleFicheCodemandeur.write(ligne, 6, "TAO", styleTitreSansFond)
                            feuilleFicheCodemandeur.merge(ligne, ligne, 6, 7, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                            feuilleFicheCodemandeur.write(ligne, 8, "LAHY / VAVY", styleTitreSansFond)
                            feuilleFicheCodemandeur.write(ligne, 9, u"CIN / ACTE N° / N° KOPIA", styleTitreSansFond)
                            feuilleFicheCodemandeur.merge(ligne, ligne, 9, 10, Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                            feuilleFicheCodemandeur.write(ligne, 11, "DATY NAHAZOANA / TOERANA", styleTitreSansFond)
                            feuilleFicheCodemandeur.write(ligne, 12, "(D)/(C) / (VD)/(T)", styleTitreSansFond)
                            feuilleFicheCodemandeur.write(ligne, 13, "RAY SY RENY", styleTitreSansFond)
                            feuilleFicheCodemandeur.write(ligne, 14, "ADIRESY", styleTitreSansFond)

                            # Boucle du tableau
                            ligne = ligne + 1
                            finboucle = ligne + 10
                            while ligne < finboucle:
                                feuilleFicheCodemandeur.write(ligne, 0, "", styleTitreSansFond)
                                feuilleFicheCodemandeur.merge(ligne, ligne, 0, 1,
                                              Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                                feuilleFicheCodemandeur.write(ligne, 2, "", styleTitreSansFond)
                                feuilleFicheCodemandeur.merge(ligne, ligne, 2, 4,
                                              Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                                feuilleFicheCodemandeur.write(ligne, 5, "", styleTitreSansFond)
                                feuilleFicheCodemandeur.write(ligne, 6, "", styleTitreSansFond)
                                feuilleFicheCodemandeur.merge(ligne, ligne, 6, 7,
                                              Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                                feuilleFicheCodemandeur.write(ligne, 8, "", styleTitreSansFond)
                                feuilleFicheCodemandeur.write(ligne, 9, u"", styleTitreSansFond)
                                feuilleFicheCodemandeur.merge(ligne, ligne, 9, 10,
                                              Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))
                                feuilleFicheCodemandeur.write(ligne, 11, "", styleTitreSansFond)
                                feuilleFicheCodemandeur.write(ligne, 12, "", styleTitreSansFond)
                                feuilleFicheCodemandeur.write(ligne, 13, "", styleTitreSansFond)
                                feuilleFicheCodemandeur.write(ligne, 14, "", styleTitreSansFond)

                                ligne = ligne + 1

                            feuilleFicheCodemandeur.write(ligne + 2, 0,
                                          "FANAMARIHANA : LAHY (L) / VAVY (v) MPANGATAKA (D)/ MPIARAMANGATAKA(C)  /VADY MIARA TOMPONY(VD)/ MPIANTOKA(T)",
                                          styleTitreSansFond)
                            feuilleFicheCodemandeur.merge(ligne + 2, ligne + 2, 0, 13,
                                          Style.easyxf(' borders: left 2, right 2, top 2, bottom 2'))

                except StandardError as e:
                    print(e)
                    self.connection.rollback()
            print datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            dst = os.path.join(tempfile.gettempdir(), datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "-" + "Registre de demande.xls")
            #dst = os.path.dirname(__file__) + "/" + str(randint(10000, 99999)) + "-" + "Registre de demande.xls"
            self.book.save(dst)
            os.startfile(dst)



