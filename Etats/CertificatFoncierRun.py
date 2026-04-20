# coding: utf-8
from Etats.codegenerator.QrCodeGenerator import QrCodeGenerator
from PyQt4 import QtGui, QtCore
from .CertificatFoncier import Ui_Dialog
import psycopg2
import psycopg2.extras
from .Pdf import PlofPdf
from PyQt4.Qt import QApplication
from PyQt4 import Qt
import globalvars
import os
from .LayerPreview import LayerPreview
from Utilisateur import AccesManager
from Utils import Utils
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import QMessageBox
from models.ProjetCouche import ProjetCouche
import globalvars
import qgis

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class CertificatFoncierRun(QtGui.QDialog):
    def __init__(self, connection, idcertificat):
        QtGui.QDialog.__init__(self)
        self.setModal(True)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.connection, self.idcertificat = connection, idcertificat
        self.nompersonne = self.prenompersonne = self.cin = self.datecin = self.datecin = self.lieucin = ""
        self.adresse = self.numerocertificat = self.numerodemande = ""
        self.idParcelle = self.area = 0
        self.fillFields()
        self.pdf = None
        self.layerpreview = LayerPreview(self.connection, idcertificat)
        self.ui.horizontalLayoutPreview.addWidget(self.layerpreview)
        self.isprint = 0
        self.initActions()

    def closeEvent(self, event):
        self.layerpreview.deleteLayers()

    def initActions(self):
        manager = AccesManager.AccessManager(self, self.connection)
        manager.activate_widget("KARATANY/PRINT", self.ui.pushButtonImprimer)

        self.ui.pushButtonAnnuler.clicked.connect(self.close)
        self.ui.pushButtonImprimer.clicked.connect(self.doprint)
        #self.ui.pushButtonImprimer.clicked.connect(self.checkEmpietement)
        self.ui.pushButtonOperation.clicked.connect(self.operations)
        self.ui.pushButtonHistorique.clicked.connect(self.historique)
        self.ui.pushButtonProprietaires.clicked.connect(self.proprio)
        self.ui.pushButtonCharges.clicked.connect(self.charges)
        self.ui.pushButtonReperes.clicked.connect(self.reperes)

    def operations(self):
        from Certificat.OperationRun import OperationRun
        w = OperationRun(self.connection)
        w.exec_()

    def proprio(self):
        from Certificat.ConsultationProprietaireRun import ConsultationProprietaireRun
        w = ConsultationProprietaireRun(self.connection, self.idcertificat, 0)
        w.exec_()

    def historique(self):
        from Certificat.HistoriqueRun import HistoriqueRun
        w = HistoriqueRun(self.connection)
        w.exec_()

    def charges(self):
        from Certificat.ConsultationChargesRun import ConsultationChargesRun
        w = ConsultationChargesRun(self.connection, self.idcertificat)
        w.exec_()

    def reperes(self):
        from Certificat.ListeLimitesRun import ListeLimitesRun
        w = ListeLimitesRun(self.connection, self.idcertificat, self)
        w.ui.btnValider.clicked.connect(w.close)
        w.exec_()

    def fillFields(self):
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "SELECT C.*, P.*, "\
              "personne.*, " \
              "demande.consistance, " \
              " coalesce(H.nomhameau, '') nomhameau, coalesce(F.nomfokontany, '') nomfokontany," \
              " coalesce(M.nomcommune, '') nomcommune, coalesce(D.nomdistrict, '') nomdistrict," \
              " coalesce(R.nomregion, '') nomregion" \
              " FROM certificat C" \
              " LEFT JOIN parcelle_d P on P.idcertificat = C.idcertificat" \
              " LEFT JOIN proprietaireparcelle ON proprietaireparcelle.idparcelle = P.gid" \
              " LEFT JOIN demande ON demande.gid = P.gid" \
              " LEFT JOIN personne ON personne.idpersonne = proprietaireparcelle.idpersonne" \
              " LEFT JOIN hameau H on H.idhameau = P.idhameau" \
              " LEFT JOIN fokontany F on F.idfokontany = H.idfokontany" \
              " LEFT JOIN commune M on M.idcommune = F.idcommune" \
              " LEFT JOIN district D on D.iddistrict = M.iddistrict" \
              " LEFT JOIN region R on R.idregion = D.idregion" \
              " WHERE C.idcertificat = %s"
        cursor.execute(sql, (self.idcertificat,))
        rows = cursor.fetchall()
        cursor.close()
        if len(rows) == 0:
            return
        row = rows[0]
        self.ui.lineEditTypeCertificat.setText(row['typecertificat'])
        self.ui.lineEditNumCertificat.setText(str(row['numerocertificat']))
        self.ui.lineEditNumDemande.setText(row['numerodemande'])
        self.ui.lineEditConsistance.setText(str(row['consistance']))
        print("ROW SURFACE")
        print(row['surface'])
        self.ui.lineEditSurface.setText(str(row['surface'])+" m2")
        self.ui.lineEditEtat.setVisible(False)
        self.ui.label_6.setVisible(False)
        self.ui.lineEditReconnaissance.setText(str(row['datereconnaissance']))
        self.ui.lineEditInscription.setText(str(row['datecreation']))
        self.ui.lineEditEdition.setText(str(row['dateedition']))
        self.ui.lineEditDelivrance.setText(str(row['datedelivrance']))
        self.ui.lineEditRegion.setText(row['nomregion'])
        self.ui.lineEditDistrict.setText(row['nomdistrict'])
        self.ui.lineEditCommune.setText(row['nomcommune'])
        self.ui.lineEditFokontany.setText(row['nomfokontany'])
        self.ui.lineEditHameau.setText(row['nomhameau'])
        self.nompersonne = row['nompersonne']
        self.prenompersonne = row['prenompersonne']
        self.cin = row["numcipersonne"]
        self.lieucin = row['lieucipersonne']
        self.datecin = row['datecipersonne']
        self.adresse = row['adressepersonne']
        self.numerocertificat = row["numerocertificat"]
        self.numerodemande = row["numerodemande"]
        self.idParcelle = row["gid"]
        self.idCF = str(row['idcertificat'])

    def doprint(self):
        try:
            QApplication.setOverrideCursor(Qt.Qt.WaitCursor)
            filename = self.preview()
            from .PrintCertificatFoncier import PrintCertificatFoncier
            p = PrintCertificatFoncier(self.connection, self.idcertificat)
            qrCodeGenerator = QrCodeGenerator()
            p.setCodeImageGenerator(qrCodeGenerator)
            p.doprint(filename, self.area)
            self.updateCFWhenPrint()
            QApplication.restoreOverrideCursor()
        except Exception as err:
            print ("Erreur lors de l'impression CF " + str(err))

    def preview(self):
        filename = self.layerpreview.render()
        self.area = self.layerpreview.area
        return filename

    def getGeomWkt(self, idCF):
        cur = self.connection.cursor()
        try:
            cur.execute("SELECT ST_AsText(pd.geom) FROM parcelle_d pd WHERE pd.idcertificat = %s", (str(idCF),))
            res = cur.fetchone()
            return res[0]
        except Exception as err:
            print (err)

    def loadShapeFromFile(self, filename, label, strokeColor, fillColor):
        if filename is None or filename == "":
            return None
        layer = QgsVectorLayer(filename, label, "ogr")
        crs = QgsCoordinateReferenceSystem(globalvars.EPSG_SCR, QgsCoordinateReferenceSystem.EpsgCrsId)
        layer.setCrs(crs)
        if not layer.isValid():
            return None
        QgsMapLayerRegistry.instance().addMapLayer(layer)

        return layer

    def loadCouchesTitres(self):
        layers = []
        couches = ProjetCouche.find_by_projet_commune(self.connection, globalvars.id_projet_commune)
        couchesTitres = filter(lambda couche: (couche.type_couche == 'S'), couches)
        for couche in couchesTitres:
            if couche.plofpaps != 1:
                if couche.plofpaps != 2:  # non limite administrative
                    layer = self.loadShapeFromFile(couche.fichier, couche.libelle, couche.couleur_bg,
                                                   couche.remplissage)
                # self.addLabelToLayer(layer, couche.label_name)
                layers.append(layer)
        return layers

    def checkEmpietement(self):
        geom_wkt = self.getGeomWkt(self.idCF)
        geom = QgsGeometry.fromWkt(geom_wkt)
        print "in check empietement"
        empietement_plof = False
        try:
            titres = self.loadCouchesTitres()
        except Exception as err:
            print (err)
        for lay in titres:
            # print "LOADIND COUCHES TITRES"
            for elem in lay.getFeatures():
                # print "elem"
                geomTitre = elem.geometry()
                try:
                    intersect = geomTitre.intersection(geom)
                except Exception as err:
                    print (err)
                # print "INTERSECT"
                # print intersect
                intersection_geometry = QgsGeometry(intersect)
                if intersection_geometry is not None:
                    if intersection_geometry.wkbType() == QGis.WKBPolygon or intersection_geometry.wkbType() == QGis.WKBMultiPolygon:
                        empietement_plof = True
                        break
                if geomTitre.within(geom) or geom.within(geomTitre):
                    empietement_plof = True
                    break

        if empietement_plof:
            QMessageBox.critical(None, u"Empiètement", u"Impréssion impossible: empiètement sur couche plof detectée!")
        else:
            self.doprint()
    def updateCFWhenPrint(self):
        self.isprint = 1
        cursor = self.connection.cursor()
        try:
            cursor.execute("UPDATE certificat SET isprint=(%s)   WHERE idcertificat = (%s)",
                           (int(self.isprint), int(self.idcertificat)))
            self.connection.commit()
        except Exception as e:
            print(e.message)
            self.connection.rollback()
        cursor.close()
