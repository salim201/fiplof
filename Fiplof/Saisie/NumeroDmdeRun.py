#coding: utf-8
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
from qgis.core import *
from qgis.gui import *
import datetime, time
import globalvars, os, sys, psycopg2

from AreaConvert import AreaConvert
from .Numero import Ui_Dialog

class NumeroDmde(QDialog):
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
        self.idFokontany = parent.singleIdFokontany
        self.idHameau = parent.singleIdHameau
        self.idProjet = globalvars.id_projet
        self.registry = parent.registry
        #self.canvas = parent.canvas
        self.parent = parent
        self.idContribuable = parent.idContribuable
        self.canvas = parent.canvas
        self.numDemande = None
        self.currValDemande = 0
        self.otherData = {}
        self.initDB()
        self.initActions()
        self.generateNumDemande()

        self.ui.dateEditDemande.setDate(QDate.currentDate())
        #self.initPreview()

    def initActions(self):
        self.ui.btnAnnuler.clicked.connect(self.close)
        self.ui.btnOk.clicked.connect(self.createDemande)

    def initDB(self):
        self.cur = self.connection.cursor()

    def __del__(self):
        self.cur.close()
        vtlayer = self.registry.mapLayersByName("Demandes Parcelle")[0]
        self.canvas.setCurrentLayer(vtlayer)

    def generateNumDemande(self):
        idcommune = None
        data = {}
        try:
            self.cur.execute("SELECT f.codefokontany, f.nomfokontany, "
                             "c.codecommune, c.nomcommune ,"
                             "d.codedistrict, d.nomdistrict, "
                             "c.idcommune, r.nomregion ,c.codeg,c.cptdemande "
                             "FROM fokontany f, commune c, district d, region r "
                             "WHERE c.idcommune = f.idcommune "
                             "AND d.iddistrict = c.iddistrict AND r.idregion = d.idregion "
                             "AND f.idfokontany = %s",(self.idFokontany,))
            res = self.cur.fetchone()
            data['codefokontany'] = res[0]
            data['nomfokontany'] = res[1]
            data['codecommune'] = res[2]
            data['nomcommune'] = res[3]
            data['codedistrict'] = res[4]
            data['nomdistrict'] = res[5]
            data['idcommune'] = res[6]
            data['nomregion'] = res[7]
            data['codeg'] = res[8]
            data['cptdemande'] = res[9]

        except StandardError as e:
            self.connection.rollback()
            print(e)
        try:
            self.cur.execute("SELECT codehameau, nomhameau FROM hameau WHERE idhameau = %s",(self.idHameau,))
            res = self.cur.fetchone()
            data['codehameau'] = res[0]
            data['nomhameau'] = res[1]
        except StandardError as e:
            self.connection.rollback()
            print(e)

        ######CREATION NUMDEMANDE##########
        #chDistrict+chCommune+"_"+chFkt)+"-F-"+str(self.parent.currvalDemande)
        #ANCIEN num demande
        #self.ui.lineEditNumDmede.setText(unicode(data['codedistrict']).strip().encode('utf-8') + unicode(data['codecommune']).strip().encode('utf-8') + unicode("_").encode('utf-8') +  unicode(data['codefokontany']).strip().encode('utf-8') + unicode("-F-").encode('utf-8') + str(self.idparcelle).strip().encode('utf-8'))


        #NOUVEAU numDemande
        print "DATA"
        print data

        chDistrict = str(unicode(data['codedistrict'])).strip().encode('utf-8')
        #chCommune = str(self.codecommune).strip()
        chCodeGuichet = str(unicode(data['codeg'])).strip().encode('utf-8')
        self.currValDemande = str(unicode(data['cptdemande'])).strip().encode('utf-8')
        # chfkt = str(idfkt.strip())
        # self.currentValDemande
        self.ui.lineEditNumDmede.setText(chDistrict + "-" + chCodeGuichet + "-F-" + self.currValDemande)
        self.ui.lineEditNumDmede.setReadOnly(True)

        self.numDemande = str(self.ui.lineEditNumDmede.text()).strip()
        self.otherData = data

    def createDemande(self):

        print "globalvars.id_commune INNNN"
        print globalvars.id_commune
        print int(self.currValDemande)

        demandeur = []
        idDemandeur = None
        idDemande = None
        dateDemande = datetime.date(self.ui.dateEditDemande.date().year(), self.ui.dateEditDemande.date().month(), self.ui.dateEditDemande.date().day())
        dateReconnissance = dateDemande + datetime.timedelta(15)
        print dateReconnissance
        try:
            self.cur.execute("INSERT INTO demande (gid, datedemande, datereconnaissance, region, district, idfokontany, idcommune, idprojet, numdemande) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) returning iddemande",
                             (self.idparcelle, dateDemande, dateReconnissance, self.otherData['nomregion'],self.otherData['nomdistrict'], self.idFokontany, self.otherData['idcommune'], self.idProjet, self.numDemande))
            self.connection.commit()
            idDemande = self.cur.fetchone()
        except StandardError as e:
            self.connection.rollback()
            print(e)

        try:
            self.cur.execute("UPDATE parcelle_d SET conversion = %s, numdemande = %s WHERE gid = %s", (1, self.numDemande, self.idparcelle))
            self.connection.commit()

            #update compteur demande
            self.currValDemande = int(self.currValDemande) + 1
            self.cur.execute("UPDATE commune SET cptdemande=(%s)  WHERE idcommune = (%s)",
                                (int(self.currValDemande), int(globalvars.id_commune)))
            self.connection.commit()



        except StandardError as e:
            self.connection.rollback()
            print(e)

        #try:
            #self.cur.execute("SELECT nom, prenom FROM contribuable WHERE idcontribuable = %s", (self.idContribuable,))
            #demandeur = self.cur.fetchone()
            #try:
                #self.cur.execute("INSERT INTO demandeur_d (nom, prenom) VALUES(%s, %s) returning iddemandeur",(demandeur[0], demandeur[1]))
                #self.connection.commit()
                #idDemandeur = self.cur.fetchone()
            #except StandardError as e:
                #self.connection.rollback()
        #except StandardError as e:
            #self.connection.rollback()
            #print(e)
        #TRAITEMENT DES DEMANDEURS
        try:
            self.cur.execute("SELECT * FROM contribuables_parcelle WHERE idparcelle = %s", (self.idparcelle,))
            contribs = self.cur.fetchall()
            for contrib in contribs:
                try:
                    self.cur.execute("INSERT INTO avoir_demande (idpersonne, iddemande, idparcelle, representant) VALUES(%s, %s, %s, %s)", (contrib[0], idDemande, self.idparcelle, contrib[2]))
                    self.connection.commit()
                except StandardError as e:
                    self.connection.rollback()
                    print(e)
        except StandardError as e:
            print(e)
            self.connection.rollback()

        vtlayer = self.registry.mapLayersByName("Demandes Parcelle")[0]
        self.canvas.setCurrentLayer(vtlayer)
        QMessageBox.information(self, "Conversion en demande", u"Conversion en demande terminée")
        self.refreshCanvas()
        print self.parent.parent.objectName()
        #self.parent.parent.close()
        self.parent.updateFields()
        self.close()


    def refreshCanvas(self):

        for layer in self.canvas.layers():
            if layer.type() == layer.VectorLayer:
                layer.removeSelection()
                layer.triggerRepaint()

        self.canvas.refresh()
