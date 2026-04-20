#coding: utf-8
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
from qgis.core import *
from qgis.gui import *
import datetime, time
import globalvars, os, sys, psycopg2

from AreaConvert import AreaConvert
from .NumeroCF import Ui_Dialog

class NumeroCF(QDialog):
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
        self.registry = parent.registry
        self.canvas = parent.canvas
        self.idFokontany = parent.singleIdFokontany
        self.idHameau = parent.singleIdHameau
        self.idProjet = globalvars.id_projet
        self.parent = parent
        self.idContribuable = parent.idContribuable
        self.canvas = parent.canvas
        self.numDemande = None
        self.otherData = {}
        self.initDB()
        self.currValDemande = 0
        self.initActions()
        self.generateNumCF()

        #self.initPreview()

    def initActions(self):
        self.ui.btnAnnuler.clicked.connect(self.closeAndDel)
        self.ui.btnOk.clicked.connect(self.createCF)

    def initDB(self):
        self.cur = self.connection.cursor()

    def __del__(self):
        self.cur.close()
        vtlayer = self.registry.mapLayersByName("Demandes Parcelle")[0]
        self.canvas.setCurrentLayer(vtlayer)

    def generateNumCF(self):
        idcommune = None
        data = {}
        try:
            self.cur.execute("SELECT f.codefokontany, f.nomfokontany, "
                             "c.codecommune, c.nomcommune ,"
                             "d.codedistrict, d.nomdistrict, "
                             "c.idcommune, r.nomregion , c.codeg, c.cptdemande, c.cptcertificat "
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
            data['cptcertificat'] = res[10]

            print "DATA"
            print data

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

        ### Recuperation  du numero de la demande ###
        self.demandeData = []
        self.idCF = None
        self.datecreation = datetime.date.today()
        print self.datecreation
        try:
            self.cur.execute("SELECT pd.numdemande, pd.has_data, pd.conversion, dmd.datereconnaissance FROM parcelle_d pd INNER JOIN demande dmd ON pd.gid = dmd.gid WHERE pd.gid = %s", (self.idparcelle,))
            self.demandeData = self.cur.fetchone()
        except StandardError as e:
            self.connection.rollback()
            print(e)
        if self.demandeData[0] is not None:
            self.ui.lineEditNumDmede.setText(str(self.demandeData[0]).strip())
            self.ui.lineEditNumDmede.setReadOnly(True)

            try:
                self.cur.execute("INSERT INTO certificat (numerodemande, typecertificat, datecreation, datereconnaissance, idfokontany, idprojet) VALUES (%s, %s, %s, %s, %s, %s) returning idcertificat",(self.demandeData[0],
                                                                                                                                                        "Certificat foncier",self.datecreation,self.demandeData[3], self.idFokontany, self.idProjet))
                self.connection.commit()
                self.idCF = idCertificat = self.cur.fetchone()
            except StandardError as e:
                self.connection.rollback()
                print(e)

        if self.idCF[0] is not None:
            #NOUVEAU numCF
            chDistrict = str(unicode(data['codedistrict'])).strip().encode('utf-8')
            # chCommune = str(self.codecommune).strip()
            chCodeGuichet = str(unicode(data['codeg'])).strip().encode('utf-8')
            self.currValDemande = str(unicode(data['cptcertificat'])).strip().encode('utf-8')

            print "self.idCF[0] is not None:"
            print self.currValDemande

            numCert = chDistrict + "-" + chCodeGuichet + "-KT-" + str(self.currValDemande)
            self.ui.lineEditNumCF.setText(numCert)
            self.ui.lineEditNumCF.setReadOnly(True)
            print "avant readonly"

            #ancien NUM cf
            #self.ui.lineEditNumCF.setText(
            #    unicode(data['codedistrict']).strip().encode('utf-8') + unicode(data['codecommune']).strip().encode(
            #        'utf-8') + unicode("_").encode('utf-8') + unicode(data['codefokontany']).strip().encode(
            #        'utf-8') + unicode("-KT-").encode('utf-8') + str(self.idCF[0]).strip().encode('utf-8'))


            self.numCF = str(self.ui.lineEditNumCF.text()).strip()

        ######CREATION NUMDEMANDE##########
        #chDistrict+chCommune+"_"+chFkt)+"-F-"+str(self.parent.currvalDemande)
        #self.ui.lineEditNumDmede.setText(unicode(data['codedistrict']).strip().encode('utf-8') + unicode(data['codecommune']).strip().encode('utf-8') + unicode("_").encode('utf-8') +  unicode(data['codefokontany']).strip().encode('utf-8') + unicode("-F-").encode('utf-8') + str(self.idparcelle).strip().encode('utf-8'))
        #self.numDemande = str(self.ui.lineEditNumDmede.text()).strip()
        self.otherData = data

    def createCF(self):

        print "self.currValDemande"
        print self.currValDemande
        if self.idCF is not None:
            listeDesContribuables = []
            try:
                self.cur.execute("UPDATE certificat set numerocertificat = %s WHERE idcertificat = %s", (self.numCF, self.idCF))
                self.connection.commit()

                # update compteur demande
                self.currValDemande = int(self.currValDemande) + 1
                self.cur.execute("UPDATE commune SET cptcertificat=(%s)  WHERE idcommune = (%s)",
                                 (int(self.currValDemande), int(globalvars.id_commune)))
                self.connection.commit()

            except StandardError as e:
                self.connection.rollback()
                print(e)
            try:
                self.cur.execute("UPDATE parcelle_d SET conversion = %s, idcertificat = %s, etatparcelle_d = %s WHERE gid = %s",(2, self.idCF, 3, self.idparcelle))
                self.connection.commit()


            except StandardError as e:
                self.connection.rollback()
                print(e)
        ##Gerer les proprios##
            try:
                self.cur.execute("SELECT * FROM avoir_demande WHERE idparcelle = %s", (self.idparcelle,))
                demandeurs = self.cur.fetchall()
                for demandeur in demandeurs:
                    try:
                        self.cur.execute(
                            "INSERT INTO proprietaireparcelle (idpersonne, idparcelle, representant) VALUES(%s, %s, %s)",
                            (demandeur[0], self.idparcelle, demandeur[3]))
                        self.connection.commit()
                    except StandardError as e:
                        self.connection.rollback()
                        print(e)
            except StandardError as e:
                print(e)
                self.connection.rollback()


        vtlayer = self.registry.mapLayersByName("Certificats")[0]
        self.canvas.setCurrentLayer(vtlayer)
        QMessageBox.information(self, "Conversion en Certificat foncier", u"Conversion en certificat foncier terminée")
        self.refreshCanvas()
        #self.parent.parent.close()
        self.parent.updateFields()
        self.close()


    def closeAndDel(self):
        if self.idCF is not None:
            try:
                self.cur.execute("DELETE FROM certificat WHERE idcertificat = %s",(self.idCF,))
                self.connection.commit()
            except StandardError as e:
                self.connection.rollback()
                print(e)

    def refreshCanvas(self):

        for layer in self.canvas.layers():
            if layer.type() == layer.VectorLayer:
                layer.removeSelection()
                layer.triggerRepaint()

        self.canvas.refresh()
