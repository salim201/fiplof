# coding: utf-8
import os
from PyQt4.QtGui import *
from PgCrud import PgColumn, PgSql
from Etats import Pdf
from Etats.Html2Pdf import Html2Pdf
from AreaConvert import AreaConvert
import datetime, time
import tempfile
from random import randint
from .ListeAvisImposition import Ui_Dialog
from .AvisImpotLangueRunn import AvisImpotLangueRunn
import webbrowser
from PyPDF2 import PdfFileMerger
from models.Commune import Commune
import globalvars
from Utils import Utils

class ListeAvisImpositionRun(QDialog):
    def __init__(self, connection):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.connection = connection
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.territoire.connection = connection
        self.initActions()
        self.pdf = None
        self.cell_height = 5
        self.rows = []
        self.dataparcelle=[]
        self.dataImpotBat = []
        self.dataImpotPar = []
        self.donnees = []
        self.contribuable=[]
        self.categorieift=[]
        self.infoCommune=[]
        self.commune=""
        self.maire=""
        self.initDB()

    def initDB(self):
        self.cur = self.connection.cursor()

    def __del__(self):
        self.cur.close()

    def initActions(self):
        self.ui.checkBoxNom.stateChanged.connect(self.updateFieldsStatus)
        self.ui.checkBoxAnnee.stateChanged.connect(self.updateFieldsStatus)
        self.ui.checkBoxCIN.stateChanged.connect(self.updateFieldsStatus)
        self.ui.pushButtonRechercher.clicked.connect(self.rechercher)
        self.ui.pushButtonAvisImposition.clicked.connect(self.langChoice)
        self.ui.pushButtonFermer.clicked.connect(self.reject)
        self.ui.tableWidget.itemClicked.connect(self.selectionChanged)
        #self.ui.pushButtonAvisImposition.setEnabled(True)

    def selectionChanged(self):
        self.ui.pushButtonAvisImposition.setEnabled(len(self.ui.tableWidget.selectedIndexes()) > 0)

    def updateFieldsStatus(self):
        self.ui.lineEditNom.setEnabled(self.ui.checkBoxNom.isChecked())
        self.ui.lineEditAnnee.setEnabled(self.ui.checkBoxAnnee.isChecked())
        self.ui.lineEditCIN.setEnabled(self.ui.checkBoxCIN.isChecked())

    def rechercher(self):
        sql = "select DISTINCT CONCAT(P2.nompersonne, ' ', P2.prenompersonne) as nom, P2.datenaissancepersonne, P2.lieunaissancepersonne, P2.numcipersonne, " \
              "ic.hetratany::numeric, ic.hetratrano::numeric, ic.hetratany::numeric + ic.hetratrano::numeric, " \
              "C.nomcommune , cp.idpersonne " \
              "from contribuables_parcelle cp " \
              "INNER JOIN personne P2 ON cp.idpersonne = P2.idpersonne, " \
              "personne P3 INNER JOIN impot_contribuable ic ON P3.idpersonne = ic.idpersonne, " \
              "contribuables_parcelle cp1 INNER JOIN parcelle_d pd ON cp1.idparcelle = pd.gid " \
              "inner join hameau h on h.idhameau = pd.idhameau " \
              "inner join fokontany f on f.idfokontany = h.idfokontany " \
              "inner join commune C on C.idcommune = f.idcommune "
        wheres = []
        values = []
        wheres.append("cp.contribuable = 'True'")
        wheres.append("P2.idpersonne = P3.idpersonne")
        wheres.append("cp.idparcelle = cp1.idparcelle")
        #wheres.append("ic.")
        if self.ui.checkBoxNom.isChecked() and self.ui.lineEditNom.text() != "":
            wheres.append("upper(P2.nom) LIKE upper(%s)")
            values.append("%" + str(self.ui.lineEditNom.text()) + "%")
        if self.ui.checkBoxCIN.isChecked() and self.ui.lineEditCIN.text() != "":
            wheres.append("P2.CIN LIKE %s")
            values.append("%" + str(self.ui.lineEditCIN.text()).replace("-", "") + "%")
        pgsql = PgSql.Table(self.connection, "")
        self.rows = pgsql.fillTableWithSql(self.ui.tableWidget, sql, wheres, values, ["Nom", "Date de Naissance", "Lieu Naissance", "cin", "Hetra (tany)", "Hetra (trano)", "Total"])

    def langChoice(self):
        self.donnees = []
        try:
            lang = AvisImpotLangueRunn(self)
            print 'self aloha'
            lang.exec_()
        except StandardError as e:
            print 'erreur ato hiditra am lanque'
            print e

    def getInfo(self,row):
        i = 1
        idcontribuable = int(row["idpersonne"])
        print "MODE DE CALCUL"
        print idcontribuable
        modeDeCalcul = 1
        self.dataparcelle
        self.donnees=[]
        try:
            self.cur.execute(
                " SELECT nompersonne, prenompersonne, numcipersonne,  adressepersonne"
                " FROM personne where idpersonne=%s ", (idcontribuable,))
            self.contribuable = self.cur.fetchone()
            print self.contribuable
        except StandardError as e:
            print (e)

        try:
            print  '----- récupération parcelle par contribuable --------'
            self.cur.execute("SELECT pd.codeparcelle, cat.idcategorie, ST_Area(pd.geom),pd.surface,pd.fkt,pd.fi_forfait,cat.typeimposition,"
                             " ip.hetratany::numeric, pd.consistance, pd.gid , pd.idclasse,cat.v_surface,cat.v_venale,cat.taux,COALESCE(ip.montant_paye::numeric,0),ip.hetratany::numeric-COALESCE(ip.montant_paye::numeric,0) as reste "
                             "FROM parcelle_d pd LEFT JOIN categorie cat ON pd.idcategorie = cat.idcategorie,"
                                 "contribuables_parcelle cp INNER JOIN parcelle_d pd1 ON cp.idparcelle = pd1.gid,"
                                 "impot_parcelle ip INNER JOIN parcelle_d pd2 ON ip.idparcelle = pd2.gid" 
                            " WHERE cp.idpersonne = %s AND cp.contribuable = true AND pd.gid = pd2.gid AND pd.gid = pd1.gid", (idcontribuable,))
            self.dataparcelle = self.cur.fetchall()
            print "data parcelle = " + str(self.dataparcelle)

            date = annee = datetime.datetime.now()
            annee = datetime.datetime.now().strftime('%Y')
            anneanterieur = ()
            anneavant = int(annee)
            for x in range(1, 4):
                anneavant = anneavant - 1
                anneanterieur = anneanterieur + (str(anneavant),)

            for dataP in self.dataparcelle:
                impotparanterieur=0
                # -----------------------------------info sur Parcelle -----------------------------------------#
                print "data parcelle concernée= " + str(dataP[5])
                self.dataImpotPar.append(i)
                self.dataImpotPar.append('TERRAIN')
                self.dataImpotPar.append(dataP[4])
                self.getCategorie('ift')
                valeurariary=""
                catp=""
                catpar = self.categorieift.index(int(dataP[1]))
                if dataP[5] == 'surface':
                    print 'surface'
                    catp= str(catpar) + " / " + str(dataP[2])
                    valeurariary=str(dataP[11])
                if dataP[5] == 'classe':
                    print 'classe'
                    catp = str(catpar) + " / " + str(dataP[2])
                    self.cur.execute(
                        "SELECT valeurariary "
                        "FROM classecategorieforfaitaire  "
                        "where idcategorie=%s AND  idclasse=%s  AND iftifpb='ift'", (int(dataP[1]), int(dataP[10])))
                    print 'valeur valeurariary'
                    valeurariary = self.cur.fetchone()[0]
                    print  str(valeurariary)
                surfnonconverti=dataP[2]
                if dataP[5] == 'valeur_venale':
                    print 'valeur venale'
                    calcupr = surfnonconverti * float(dataP[13])
                    catp = str(catpar) + " / " + str(calcupr)
                    valeurariary=str(int(dataP[13]))
                self.dataImpotPar.append(catp)
                self.dataImpotPar.append(valeurariary)
                # impot anterieur
                self.cur.execute(
                    " SELECT SUM(hetratany::numeric - COALESCE(montant_paye::numeric,0)) FROM impot_parcelle"
                    " WHERE idparcelle =%s AND annee IN %s ", (int(dataP[9]), anneanterieur))
                res = self.cur.fetchone()
                print res
                print  'impotparanterieur***********************************'
                if res[0] is None:
                    impotparanterieur=0
                else :
                    impotparanterieur = res[0]

                print impotparanterieur
                self.dataImpotPar.append(str(impotparanterieur))
                self.dataImpotPar.append(str(dataP[7]))
                sstpar=float(impotparanterieur)+float(dataP[7])
                self.dataImpotPar.append(str(sstpar))
                self.donnees.append(self.dataImpotPar)

                print '-----donnees  avant batiment'
                print self.donnees
                #-----------------------------------info sur les batiments -----------------------------------------#

                batiments = []
                try:
                    self.cur.execute(" SELECT DISTINCT b.codebatiment, b.surfacebatiment,b.idcategorie, b.idclasse, b.fi_forfait, b.nbpiecebatiment, b.locationbatiment, "
                                     "ib.hetratrano::numeric,cat.v_surface,cat.v_venale,cat.taux,ib.montant_paye::numeric,ib.hetratrano::numeric- COALESCE(ib.montant_paye::numeric,0) "
                                         "FROM batiment b, parcelle_d pd,categorie cat, impot_batiment ib  "
                                         "WHERE b.idparcelle = pd.gid AND pd.gid = %s "
                                         "AND b.idcategorie = cat.idcategorie "
                                     "AND ib.codebatiment = b.codebatiment AND ib.annee=%s", (dataP[9],annee))

                    batiments = self.cur.fetchall()
                    print "IO NY BATIMENT"
                    print batiments
                    print "FIN BATIMENT"
                except StandardError as e:
                    print e
                i = i + 1
                if len(batiments) > 0:
                    for bat in batiments:
                        impotanterieur=0
                        self.dataImpotBat=[]
                        bac = AreaConvert()
                        surafceBatTemp = bac.convertAreaToHa(bat[1])
                        surfaceBat = surafceBatTemp
                        surfnonconverti=float(bat[1])
                        impotBatiment = 0
                        velaranySyEfitra=""
                        if bat[4] is not None:
                            impotBatiment = bat[7]
                        #valImpotBat = valImpotBat + impotBatiment
                        self.dataImpotBat.append(i)
                        self.dataImpotBat.append("BATIMENT")
                        self.dataImpotBat.append(dataP[4])
                        self.getCategorie('ifpb')
                        cat = self.categorieift.index(int(bat[2]))
                        print 'categorie'+ str(cat)
                        if bat[4]=='surface':
                            print 'surface'
                            velaranySyEfitra = str(cat)+ " / " +str(surfnonconverti)
                            valeurariary=bat[8]
                        if bat[4]=='classe' :
                            print 'classe'
                            #print bat[2]
                            #print bat[3]
                            velaranySyEfitra = str(cat) + " / " + str(surfnonconverti)
                            self.cur.execute(
                                "SELECT valeurariary "
	                            "FROM classecategorieforfaitaire  "
	                            "where idcategorie=%s AND  idclasse=%s  AND iftifpb='ifpb'", (bat[2],bat[3]))
                            print 'valeur valeurariary'
                            resval = self.cur.fetchone()
                            valeurariary=resval[0]
                        if bat[4] == 'valeur_locative':
                            print 'valeur locative'
                            valeur=surfnonconverti*float(bat[9])
                            velaranySyEfitra = str(cat) + " / " + str(valeur)
                            valeurariary = str(int(bat[10]))
                        self.dataImpotBat.append(velaranySyEfitra)
                        self.dataImpotBat.append(valeurariary)
                        # impot anterieur
                        self.cur.execute(
                            " SELECT SUM(ib.hetratrano::numeric) as ss_total FROM batiment b, parcelle_d pd,categorie cat, impot_batiment ib "
                            " WHERE b.idparcelle = pd.gid AND pd.gid =%s "
                            " AND b.idcategorie = cat.idcategorie "
                            " AND ib.codebatiment = b.codebatiment AND annee IN %s ", (dataP[9], anneanterieur))
                        res = self.cur.fetchone()
                        impotanterieur = res[0]
                        if impotanterieur is None:
                            impotanterieur = 0
                        print '-----------------impotanterieur--------------------'
                        print impotanterieur
                        self.dataImpotBat.append(str(impotanterieur))
                        self.dataImpotBat.append(str(bat[12]))
                        #total impot
                        sstotbat=impotanterieur+int(bat[7])
                        self.dataImpotBat.append(sstotbat)
                        print "DATA BATIMENT IMPOT"
                        print self.dataImpotBat
                        print "FIN"
                        self.donnees.append(self.dataImpotBat)
                        i = i + 1
                i=i+1
        except StandardError as e:
            print (e)
            self.connection.rollback()

    def doprintLangue(self, langue=None):
        self.merger = PdfFileMerger()
        self.infoCommune = Commune.findById(self.connection,globalvars.id_commune)
        self.commune = str(Utils.emptyifnull(self.infoCommune, "nomcommune"))
        self.maire = str(Utils.emptyifnull(self.infoCommune, "maire"))
        try:
            indexes = self.ui.tableWidget.selectionModel().selectedRows()
            date = annee = datetime.datetime.now()
            annee = datetime.datetime.now().strftime('%Y')
            dateavis=datetime.datetime.now().strftime('%d-%m-%Y')
            anneeavis=datetime.datetime.now().strftime('%Y')
            for index in indexes:
                row = self.rows[index.row()]
                self.contribuable=[]
                self.getInfo(row)
                all_soustotal = []
                total=0
                for oneInfo in self.donnees :
                    print '------test info-----'
                    tanytrano = ""
                    total=total+float(oneInfo[7])
                    if langue == 'MALAGASY':
                        if oneInfo[1]=="TERRAIN" :
                            tanytrano = "TANY"
                        if oneInfo[1]=="BATIMENT" :
                            tanytrano="TRANO"
                        self.template = 'avis_imposition_v2_MG.html'
                    else:
                        tanytrano=oneInfo[1]
                        self.template = 'avis_imposition_v2_FR.html'
                    all_soustotal.append({
                        "num":  oneInfo[0],
                        "type_ppt": tanytrano,
                        "emplacement":  oneInfo[2],
                        "calcul":  oneInfo[3],
                        "tarif":  oneInfo[4],
                        "impot_anterieur":  oneInfo[5],
                        "impot_anneeencours":  oneInfo[6],
                        "sstotal": oneInfo[7]
                    })
                    print all_soustotal
                totalenchifre=str(total)
                totalenlettre=int(total)
                if langue == 'MALAGASY':
                    totalenlettre=self.convertir_en_lettres_mg(totalenlettre)
                else:
                    totalenlettre=self.convertir_en_lettres_fr(totalenlettre)
                print self.contribuable[0]
                nom=str(self.contribuable[0])
                prenom=str(self.contribuable[1])
                cin=str(self.contribuable[2])
                adr=str(self.contribuable[3])
                maire=str(self.maire)
                commune=str(self.commune)
                dic = {
                        "$commune": commune,
                        "$ref": "",
                        "$NR": "",
                        "$nom_c": nom,
                        "$prenom_c":prenom,
                        "$cin_c":cin,
                        "$adr_c":adr,
                        "$fkt_c":"",
                        "$maire":maire,
                        "$anneavis":  anneeavis,
                        "$date": dateavis,
                        "$total": totalenchifre,
                        "$lettre":totalenlettre,
                        "$infoimpot": all_soustotal
                   }

                converter = Html2Pdf()
                converter.setOrientation(orientation='portrait')
                src = os.path.dirname(__file__) + "/" + self.template
                print src
                dst = os.path.join(tempfile.gettempdir(), str(randint(10000, 99999)) + "-" + self.template + ".pdf")
                print "Before Generate"
                converter.generate(html=src, pdf=dst, dictionnary=dic)
                print "After generate"
                self.merger.append(dst)
        except Exception as err:
            print(err)
        try:
            dstFinal = os.path.join(tempfile.gettempdir(), str(randint(10000, 99999)) + "-" + "Avis_imposition.pdf")
            self.merger.write(dstFinal)
            print 'after merger write'
            webbrowser.open(dstFinal)
            QApplication.restoreOverrideCursor()
        except Exception as err:
            print(err)

    def getCategorie(self,type):
        self.categorieift=[]
        try:
            self.cur.execute(
                "SELECT idcategorie, libellecategorie, typeimposition, v_surface, valeur_location_ha, u_surface, v_venale, u_venale, taux"
	            "  FROM public.categorie where typeimposition=%s order by idcategorie",
                (type,))
            categorie=self.cur.fetchall()
            self.categorieift.append(0)
            if len(categorie) > 0:
                for cat in categorie:
                    self.categorieift.append(int(cat[0]))
                    print self.categorieift
            print self.categorieift
        except Exception as err:
            print(err)

    def doprint(self):
        indexes = self.ui.tableWidget.selectionModel().selectedRows()
        self.cell_height_1 = 4
        self.pdf = Pdf.PlofPdf(format='a4', orientation='landscape')
        self.pdf.l_margin = self.pdf.r_margin = 5
        self.pdf.t_margin = 4
        self.pdf.b_margin = 1
        i = 0
        for index in indexes:
            if i % 3 == 0 :
                self.pdf.add_page()
            self.tableau(index.row())
            i += 1
        self.pdf.show("avis_imposition.pdf")

    def tableau(self, rownum):
        dataBatimentToPrint = []
        self.dataImpotBat[:] = []
        i = 1

        if str(self.ui.lineEditAnnee.text()) != "":
            annee = str(self.ui.lineEditAnnee.text())
        else:
            annee = datetime.datetime.now().strftime('%Y')
        if rownum > len(self.rows) - 1:
            return
        row = self.rows[rownum]
        ac = AreaConvert()
        idcontribuable = row["idpersonne"]
        print "MODE DE CALCUL"
        print idcontribuable
        modeDeCalcul = 1
        print modeDeCalcul
        dataParcelle = []
        try:
            self.cur.execute("SELECT pd.codeparcelle, cat.idcategorie, ST_Area(pd.geom), ip.hetratany::numeric, pd.consistance, pd.gid "
                             " FROM parcelle_d pd LEFT JOIN categorie cat ON pd.idcategorie = cat.idcategorie,"
                                 " contribuables_parcelle cp INNER JOIN parcelle_d pd1 ON cp.idparcelle = pd1.gid,"
                                 "impot_parcelle ip INNER JOIN parcelle_d pd2 ON ip.idparcelle = pd2.gid "
                             "WHERE cp.idpersonne = %s AND cp.contribuable = %s AND pd.gid = pd2.gid AND pd.gid = pd1.gid", (idcontribuable,True))

            dataParcelle = self.cur.fetchall()
            print "data parcelle = " + str(dataParcelle)
            for dataP in dataParcelle:
                self.donnees[:] = []
                batiments = []
                try:
                    self.cur.execute("SELECT b.codebatiment, b.surfacebatiment, b.nbpiecebatiment, b.locationbatiment, ib.hetratrano::numeric "
                                         "FROM batiment b, parcelle_d pd,categorie cat, impot_batiment ib  "
                                         "WHERE b.idparcelle = pd.gid AND pd.gid = %s "
                                         "AND b.idcategorie = cat.idcategorie "
                                     "AND ib.codebatiment = b.codebatiment", (dataP[5],))

                    batiments = self.cur.fetchall()
                    print "IO NY BATIMENT"
                    print batiments
                    print "FIN BATIMENT"
                except StandardError as e:
                    print e
                if len(batiments) > 0:
                    for bat in batiments:
                        bac = AreaConvert()
                        surafceBatTemp = bac.convertAreaToHa(bat[1])
                        surfaceBat = surafceBatTemp
                        impotBatiment = 0
                        if bat[4] is not None:
                            impotBatiment = bat[4]
                        #valImpotBat = valImpotBat + impotBatiment
                        self.dataImpotBat.append(i)
                        velaranySyEfitra = str(surfaceBat)+ " / " + str(bat[2])
                        self.dataImpotBat.append(velaranySyEfitra)
                        self.dataImpotBat.append(impotBatiment)
                        print "DATA BATIMENT IMPOT"
                        print self.dataImpotBat
                        print "FIN"
                        i = i + 1
                        self.donnees.append(self.dataImpotBat)

        except StandardError as e:
            print (e)
            self.connection.rollback()
        j = 0
        while j <= len(self.dataImpotBat) - 3:
            dataBatimentToPrint.append(self.dataImpotBat[j:j+3])
            j = j + 3
        print "info batiment"
        print dataBatimentToPrint
        print "fin info batiment"
        # ligne 1
        self.pdf.set_font("Arial", size=7, style='B')
        self.pdf.cell(80, self.cell_height_1, "REPOBLIKAN'I MADAGASIKARA", 1, 0, 'C')
        self.pdf.cell(90, self.cell_height_1, "REPOBLIKAN'I MADAGASIKARA", 1, 0, 'C')
        self.pdf.cell(68, self.cell_height_1, "TANY", 1, 0, 'C')
        self.pdf.cell(7, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(42, self.cell_height_1, "TRANO", 1, 1, 'C')

        # ligne 2
        self.pdf.set_font("Arial", size=7)
        self.pdf.mcell(40, self.cell_height_1, "Fitiavana - Tanindrazana - Fandrosoana", 1)
        self.pdf.cell(20, self.cell_height_1 * 2, "IFT", 1, 0, 'C')
        self.pdf.cell(20, self.cell_height_1 * 2, "IFPB", 1, 0, 'C')
        self.pdf.mcell(46, self.cell_height_1, "Fitiavana - Tanindrazana - Fandrosoana", 1)
        self.pdf.cell(44, self.cell_height_1 * 3, row["nom"], 1, 0, 'C')
        self.pdf.set_font("Arial", size=7, style="B")
        self.pdf.cell(10, self.cell_height_1 * 2, "N", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1 * 2, "Sokajy", 1, 0, 'C')
        self.pdf.mcell(15, self.cell_height_1, "Velarany (a)", 1)
        self.pdf.cell(20, self.cell_height_1 * 2, "Zavamisy", 1, 0, 'C')
        self.pdf.mcell(13, self.cell_height_1, "Hetra (Ar)", 1)
        self.pdf.cell(7, self.cell_height_1 * 2, "T", 1, 0, 'C')
        self.pdf.cell(13, self.cell_height_1 * 2, "Sokajy", 1, 0, 'C')
        self.pdf.mcell(14, self.cell_height_1, "Velarany / Efitra", 1)
        self.pdf.cell(15, self.cell_height_1 * 2, "Hetra (Ar)", 1, 1, 'C')

        # ligne 3
        self.pdf.set_font("Arial", size=7)
        self.pdf.cell(40, self.cell_height_1, "Hetra "+ annee, 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(46, self.cell_height_1, row["nomcommune"] if row["nomcommune"] is not None else "", 1, 0, 'C')
        self.pdf.cell(44, self.cell_height_1, "", 0, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, str([0][0]) if len(dataParcelle) >= 1 else "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, unicode(dataParcelle[0][1]) if len(dataParcelle) >= 1 else "", 1, 0, 'C')
        self.pdf.cell(15, self.cell_height_1, str(ac.convertAreaToA(dataParcelle[0][2])) if len(dataParcelle) >= 1 else "" , 1, 0, 'C')
        self.pdf.cell(20, self.cell_height_1, unicode(dataParcelle[0][4]) if len(dataParcelle) >= 1 else "", 1, 0, 'C')
        hetratany = None
        if len(dataParcelle) >= 1:
            if dataParcelle[0][3] is not None:
                hetratany = dataParcelle[0][3]

        self.pdf.cell(13, self.cell_height_1, str(hetratany) if hetratany is not None else "", 1, 0, 'C')
        self.pdf.cell(7, self.cell_height_1, str(dataBatimentToPrint[0][0]) if len(dataBatimentToPrint) >= 1 else "", 1, 0, 'C')
        self.pdf.cell(13, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(14, self.cell_height_1, str(dataBatimentToPrint[0][1]) if len(dataBatimentToPrint) >= 1 else "", 1, 0, 'C')
        self.pdf.cell(15, self.cell_height_1, str(round(float(dataBatimentToPrint[0][2]), 2)) if len(dataBatimentToPrint) >= 1 else "", 1, 1, 'C')

        # ligne 4
        self.pdf.cell(40, self.cell_height_1, row["nomcommune"] if row["nomcommune"] is not None else "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(46, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(44, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, str(dataParcelle[1][0]) if len(dataParcelle) >= 2 else "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, unicode(dataParcelle[1][1]) if len(dataParcelle) >= 2 else "", 1, 0, 'C')
        self.pdf.cell(15, self.cell_height_1, str(ac.convertAreaToA(dataParcelle[1][2])) if len(dataParcelle) >= 2 else "" , 1, 0, 'C')
        self.pdf.cell(20, self.cell_height_1, unicode(dataParcelle[1][4]) if len(dataParcelle) >= 2 else "", 1, 0, 'C')
        hetratany = None
        if len(dataParcelle) >= 2:
            if dataParcelle[1][3] is not None:
                hetratany = dataParcelle[1][3]

        self.pdf.cell(13, self.cell_height_1, str(hetratany) if hetratany is not None else "", 1, 0, 'C')
        self.pdf.cell(7, self.cell_height_1, str(dataBatimentToPrint[1][0]) if len(dataBatimentToPrint) >= 2 else "", 1, 0, 'C')
        self.pdf.cell(13, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(14, self.cell_height_1, str(dataBatimentToPrint[1][1]) if len(dataBatimentToPrint) >= 2 else "", 1, 0, 'C')
        self.pdf.cell(15, self.cell_height_1, str(round(float(dataBatimentToPrint[1][2]), 2)) if len(dataBatimentToPrint) >= 2 else "", 1, 1, 'C')

        # ligne 5
        self.pdf.cell(40, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.set_font("Arial", size=7, style="B")
        self.pdf.cell(46, self.cell_height_1, "FILAZANA FANDOAVAN-KETRA", 1, 0, 'C')
        self.pdf.set_font("Arial", size=7)
        self.pdf.cell(14, self.cell_height_1, "Teraka tao", 1, 0, 'C')
        self.pdf.cell(30, self.cell_height_1, row["lieunaissancepersonne"] if row["lieunaissancepersonne"] is not None else "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, str(dataParcelle[2][0]) if len(dataParcelle) >= 3 else "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, unicode(dataParcelle[2][1]) if len(dataParcelle) >= 3 else "", 1, 0, 'C')
        self.pdf.cell(15, self.cell_height_1, str(ac.convertAreaToA(dataParcelle[2][2])) if len(dataParcelle) >= 3 else "" , 1, 0, 'C')
        self.pdf.cell(20, self.cell_height_1, unicode(dataParcelle[2][4]) if len(dataParcelle) >= 3 else "", 1, 0, 'C')
        hetratany = None
        if len(dataParcelle) >= 3:
            if dataParcelle[2][3] is not None:
                hetratany = dataParcelle[2][3]

        self.pdf.cell(13, self.cell_height_1, str(hetratany) if hetratany is not None else "", 1, 0, 'C')
        self.pdf.cell(7, self.cell_height_1, str(dataBatimentToPrint[2][0]) if len(dataBatimentToPrint) >= 3 else "", 1, 0, 'C')
        self.pdf.cell(13, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(14, self.cell_height_1, str(dataBatimentToPrint[2][1]) if len(dataBatimentToPrint) >= 3 else "", 1, 0, 'C')
        self.pdf.cell(15, self.cell_height_1, str(round(float(dataBatimentToPrint[2][2]), 2)) if len(dataBatimentToPrint) >= 3 else "", 1, 1, 'C')

        # ligne 6
        self.pdf.cell(40, self.cell_height_1 * 3, row["nom"], 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(22, self.cell_height_1, "Laharana :", 1, 0, 'L')
        self.pdf.cell(24, self.cell_height_1, "1", 1, 0, 'C')
        self.pdf.cell(14, self.cell_height_1, "Ny :", 1, 0, 'R')
        self.pdf.cell(30, self.cell_height_1, row["datenaissancepersonne"].strftime("%d/%m/%Y"), 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, str(dataParcelle[3][0]) if len(dataParcelle) >= 4 else "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, unicode(dataParcelle[3][1]) if len(dataParcelle) >= 4 else "", 1, 0, 'C')
        self.pdf.cell(15, self.cell_height_1, str(ac.convertAreaToA(dataParcelle[3][2])) if len(dataParcelle) >= 4 else "" , 1, 0, 'C')
        self.pdf.cell(20, self.cell_height_1, unicode(dataParcelle[3][4]) if len(dataParcelle) >= 4 else "", 1, 0, 'C')
        hetratany = None
        if len(dataParcelle) >= 4:
            if dataParcelle[3][3] is not None:
                hetratany = dataParcelle[3][3]

        self.pdf.cell(13, self.cell_height_1, str(hetratany) if hetratany is not None else "", 1, 0, 'C')
        self.pdf.cell(7, self.cell_height_1, str(dataBatimentToPrint[3][0]) if len(dataBatimentToPrint) >= 4 else "", 1, 0, 'C')
        self.pdf.cell(13, self.cell_height_1,  "", 1, 0, 'C')
        self.pdf.cell(14, self.cell_height_1, str(dataBatimentToPrint[3][1]) if len(dataBatimentToPrint) >= 4 else "", 1, 0, 'C')
        self.pdf.cell(15, self.cell_height_1, str(round(float(dataBatimentToPrint[3][2]), 2)) if len(dataBatimentToPrint) >= 4 else "", 1, 1, 'C')

        # ligne 7
        self.pdf.cell(40, self.cell_height_1, "", 0, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(22, self.cell_height_1, "Taona:", 1, 0, 'L')
        self.pdf.set_font("Arial", size=7, style="B")
        self.pdf.cell(24, self.cell_height_1, annee, 1, 0, 'C')
        self.pdf.set_font("Arial", size=7)
        self.pdf.cell(14, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(30, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, str(dataParcelle[4][0]) if len(dataParcelle) >= 5 else "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, unicode(dataParcelle[4][1]) if len(dataParcelle) >= 5 else "", 1, 0, 'C')
        self.pdf.cell(15, self.cell_height_1, str(ac.convertAreaToA(dataParcelle[4][2])) if len(dataParcelle) >= 5 else "" , 1, 0, 'C')
        self.pdf.cell(20, self.cell_height_1, unicode(dataParcelle[4][4]) if len(dataParcelle) >= 5 else "", 1, 0, 'C')
        hetratany = None
        if len(dataParcelle) >= 5:
            if dataParcelle[4][3] is not None:
                hetratany = dataParcelle[4][3]

        self.pdf.cell(13, self.cell_height_1, str(hetratany) if hetratany is not None else "", 1, 0, 'C')
        self.pdf.cell(7, self.cell_height_1, str(dataBatimentToPrint[4][0]) if len(dataBatimentToPrint) >= 5 else "", 1, 0, 'C')
        self.pdf.cell(13, self.cell_height_1,  "", 1, 0, 'C')
        self.pdf.cell(14, self.cell_height_1, str(dataBatimentToPrint[4][1]) if len(dataBatimentToPrint) >= 5 else "", 1, 0, 'C')
        self.pdf.cell(15, self.cell_height_1, str(round(float(dataBatimentToPrint[4][2]), 2)) if len(dataBatimentToPrint) >= 5 else "", 1, 1, 'C')

        # ligne 8
        self.pdf.cell(40, self.cell_height_1, "", 0, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(46, self.cell_height_1, "Daty:", 1, 0, 'L')
        self.pdf.cell(14, self.cell_height_1, "CIN:", 1, 0, 'R')
        self.pdf.cell(30, self.cell_height_1, row["numcipersonne"], 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, str(dataParcelle[5][0]) if len(dataParcelle) >= 6 else "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, unicode(dataParcelle[5][1]) if len(dataParcelle) >= 6 else "", 1, 0, 'C')
        self.pdf.cell(15, self.cell_height_1, str(ac.convertAreaToA(dataParcelle[5][2])) if len(dataParcelle) >= 6 else "" , 1, 0, 'C')
        self.pdf.cell(20, self.cell_height_1, unicode(dataParcelle[5][4]) if len(dataParcelle) >= 6 else "", 1, 0, 'C')
        hetratany = None
        if len(dataParcelle) >= 6:
            if dataParcelle[5][3] is not None:
                hetratany = dataParcelle[5][3]

        self.pdf.cell(13, self.cell_height_1, str(hetratany) if hetratany is not None else "", 1, 0, 'C')
        self.pdf.cell(7, self.cell_height_1, str(dataBatimentToPrint[5][0]) if len(dataBatimentToPrint) >= 6 else "", 1, 0, 'C')
        self.pdf.cell(13, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(14, self.cell_height_1, str(dataBatimentToPrint[5][1]) if len(dataBatimentToPrint) >= 6 else "", 1, 0, 'C')
        self.pdf.cell(15, self.cell_height_1, str(round(float(dataBatimentToPrint[5][2]), 2)) if len(dataBatimentToPrint) >= 6 else "", 1, 1, 'C')

        # ligne 9
        self.pdf.cell(15, self.cell_height_1, "Teraka tao:", 1, 0, 'C')
        self.pdf.cell(25, self.cell_height_1, row["lieunaissancepersonne"] if row["lieunaissancepersonne"] is not None else "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(46, self.cell_height_1 * 6, "Ny Ben'ny Tanana", 1, 0, 'C')
        self.pdf.cell(14, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(30, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, str(dataParcelle[6][0]) if len(dataParcelle) >= 7 else "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, unicode(dataParcelle[6][1]) if len(dataParcelle) >= 7 else "", 1, 0, 'C')
        self.pdf.cell(15, self.cell_height_1,
                      str(ac.convertAreaToA(dataParcelle[6][2])) if len(dataParcelle) >= 7 else "", 1, 0, 'C')
        self.pdf.cell(20, self.cell_height_1, unicode(dataParcelle[6][4]) if len(dataParcelle) >= 7 else "", 1, 0, 'C')
        hetratany = None
        if len(dataParcelle) >= 7:
            if dataParcelle[6][3] is not None:
                hetratany = dataParcelle[6][3]

        self.pdf.cell(13, self.cell_height_1, str(hetratany) if hetratany is not None else "", 1, 0, 'C')
        self.pdf.cell(7, self.cell_height_1, str(dataBatimentToPrint[6][0]) if len(dataBatimentToPrint) >= 7 else "", 1, 0, 'C')
        self.pdf.cell(13, self.cell_height_1,  "", 1, 0, 'C')
        self.pdf.cell(14, self.cell_height_1, str(dataBatimentToPrint[6][1]) if len(dataBatimentToPrint) >= 7 else "", 1, 0, 'C')
        self.pdf.cell(15, self.cell_height_1, str(round(float(dataBatimentToPrint[6][2]), 2)) if len(dataBatimentToPrint) >= 7 else "", 1, 1, 'C')

        # ligne 10
        self.pdf.cell(15, self.cell_height_1, "Ny :", 1, 0, 'R')
        self.pdf.cell(25, self.cell_height_1, row["datenaissancepersonne"].strftime('%d/%m/%Y'), 1, 0, 'R')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(46, self.cell_height_1, "", 0, 0, 'C')
        self.pdf.cell(14, self.cell_height_1, "Adiresy:", 1, 0, 'R')
        self.pdf.cell(30, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, str(dataParcelle[7][0]) if len(dataParcelle) >= 8 else "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, unicode(dataParcelle[7][1]) if len(dataParcelle) >= 8 else "", 1, 0, 'C')
        self.pdf.cell(15, self.cell_height_1,
                      str(ac.convertAreaToA(dataParcelle[7][2])) if len(dataParcelle) >= 8 else "", 1, 0, 'C')
        self.pdf.cell(20, self.cell_height_1, unicode(dataParcelle[7][4]) if len(dataParcelle) >= 8 else "", 1, 0, 'C')
        hetratany = None
        if len(dataParcelle) >= 8:
            if dataParcelle[7][3] is not None:
                hetratany = dataParcelle[7][3]

        self.pdf.cell(13, self.cell_height_1, str(hetratany) if hetratany is not None else "", 1, 0, 'C')
        self.pdf.cell(7, self.cell_height_1, str(dataBatimentToPrint[7][0]) if len(dataBatimentToPrint) >= 8 else "", 1, 0, 'C')
        self.pdf.cell(13, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(14, self.cell_height_1, str(dataBatimentToPrint[7][1]) if len(dataBatimentToPrint) >= 8 else "", 1, 0, 'C')
        self.pdf.cell(15, self.cell_height_1, str(round(float(dataBatimentToPrint[7][2]), 2)) if len(dataBatimentToPrint) >= 8 else "", 1, 1, 'C')

        # ligne 11
        self.pdf.cell(15, self.cell_height_1, "CIN :", 1, 0, 'R')
        self.pdf.cell(25, self.cell_height_1, row["numcipersonne"], 1, 0, 'R')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(46, self.cell_height_1, "", 0, 0, 'C')
        self.pdf.cell(14, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(30, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, str(dataParcelle[8][0]) if len(dataParcelle) >= 9 else "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, unicode(dataParcelle[8][1]) if len(dataParcelle) >= 9 else "", 1, 0, 'C')
        self.pdf.cell(15, self.cell_height_1,
                      str(ac.convertAreaToA(dataParcelle[8][2])) if len(dataParcelle) >= 9 else "", 1, 0, 'C')
        self.pdf.cell(20, self.cell_height_1, unicode(dataParcelle[8][4]) if len(dataParcelle) >= 9 else "", 1, 0, 'C')
        hetratany = None
        if len(dataParcelle) >= 9:
            if dataParcelle[8][3] is not None:
                hetratany = dataParcelle[8][3]

        self.pdf.cell(13, self.cell_height_1, str(hetratany) if hetratany is not None else "", 1, 0, 'C')
        self.pdf.cell(7, self.cell_height_1, str(dataBatimentToPrint[8][0]) if len(dataBatimentToPrint) >= 9 else "", 1,0, 'C')
        self.pdf.cell(13, self.cell_height_1,  "", 1, 0, 'C')
        self.pdf.cell(14, self.cell_height_1, str(dataBatimentToPrint[8][1]) if len(dataBatimentToPrint) >= 9 else "",1, 0, 'C')
        self.pdf.cell(15, self.cell_height_1,str(round(float(dataBatimentToPrint[8][2]), 2)) if len(dataBatimentToPrint) >= 9 else "", 1, 1,'C')

        # ligne 12
        self.pdf.cell(15, self.cell_height_1, "Adiresy :", 1, 0, 'R')
        self.pdf.cell(25, self.cell_height_1, "", 1, 0, 'R')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(46, self.cell_height_1, "", 0, 0, 'C')
        self.pdf.cell(44, self.cell_height_1, "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, str(dataParcelle[9][0]) if len(dataParcelle) >= 10 else "", 1, 0, 'C')
        self.pdf.cell(10, self.cell_height_1, unicode(dataParcelle[9][1]) if len(dataParcelle) >= 10 else "", 1, 0, 'C')
        self.pdf.cell(15, self.cell_height_1,
                      str(ac.convertAreaToA(dataParcelle[9][2])) if len(dataParcelle) >= 10 else "", 1, 0, 'C')
        self.pdf.cell(20, self.cell_height_1, unicode(dataParcelle[9][4]) if len(dataParcelle) >= 10 else "", 1, 0, 'C')
        hetratany = None
        if len(dataParcelle) >= 10:
            if dataParcelle[9][3] is not None:
                hetratany = dataParcelle[9][3]

        self.pdf.cell(13, self.cell_height_1, str(hetratany) if hetratany is not None else "", 1, 0, 'C')
        self.pdf.cell(7, self.cell_height_1, str(dataBatimentToPrint[9][0]) if len(dataBatimentToPrint) >= 10 else "", 1,0, 'C')
        self.pdf.cell(13, self.cell_height_1,   "", 1, 0, 'C')
        self.pdf.cell(14, self.cell_height_1, str(dataBatimentToPrint[9][1]) if len(dataBatimentToPrint) >= 10 else "",1, 0, 'C')
        self.pdf.cell(15, self.cell_height_1,str(round(float(dataBatimentToPrint[9][2]), 2)) if len(dataBatimentToPrint) >= 10 else "", 1, 1,'C')

        # ligne 12
        self.pdf.cell(15, self.cell_height_1 * 2, "Daty :", 1, 0, 'R')
        self.pdf.cell(25, self.cell_height_1 * 2, "Quitt :", 1, 0, 'L')
        self.pdf.cell(20, self.cell_height_1 * 2, str(row["hetratany"]), 1, 0, 'C')
        self.pdf.cell(20, self.cell_height_1 * 2, str(row["hetratrano"]), 1, 0, 'C')
        self.pdf.cell(46, self.cell_height_1 * 2, "", 0, 0, 'C')
        self.pdf.mcell(64, self.cell_height_1,
                       "Iangaviana ianao handoa ny vola mitentina "+ str(round(float(row["hetratany"]) + float(row["hetratrano"]), 2)) + " Ar ao anatin'ny telo volana", 1, 'C')
        self.pdf.set_font('Arial', size=7, style='B')
        self.pdf.cell(35, self.cell_height_1 * 2, "Totaliny", 1, 0, 'C')
        self.pdf.cell(13, self.cell_height_1 * 2, str(row["hetratany"]), 1, 0, 'C')
        self.pdf.cell(34, self.cell_height_1 * 2, "Totaliny", 1, 0, 'C')
        self.pdf.cell(15, self.cell_height_1 * 2, str(row["hetratrano"]), 1, 1, 'C')

        self.pdf.write(1, "\n")

    def convertir_en_lettres_fr(self, montant):
        unite = ["", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf"]
        dizaine = ["", "dix", "vingt", "trente", "quarante", "cinquante", "soixante", "soixante", "quatre-vingt",
                   "quatre-vingt"]
        dizaine_spec = ["", "onze", "douze", "treize", "quatorze", "quinze", "seize"]
        if montant == 0:
            return "zero"
        else:
            texte = ""
            millions = montant // 1000000
            montant %= 1000000
            milliers = montant // 1000
            montant %= 1000
            centaines = montant // 100
            montant %= 100
            dizaines = montant // 10
            unite_montant = montant % 10

        if millions > 0:
            if millions < 1000:
                texte += self.convertir_en_lettres_fr(millions) + " million"
                if millions > 1:
                    texte += "s"
            if millions >= 1000:
                texte += self.convertir_en_lettres_fr(millions / 1000) + " milliard"
                if millions / 1000 > 1000:
                    texte += "s"
                if millions % 1000 > 0:
                    texte += " "
                    texte += self.convertir_en_lettres_fr(millions % 1000) + " million"
                    if millions > 1:
                        texte += "s"
            texte += " "

        if milliers > 0:
            if milliers == 1:
                texte += "mille"
            else:
                texte += self.convertir_en_lettres_fr(milliers) + " mille"
            if milliers > 1:
                texte += "s"
            texte += " "

        if centaines > 0:
            if centaines == 1:
                texte += "cent "
            else:
                texte += unite[centaines] + " cent "

        if dizaines == 1:
            if 0 < unite_montant < 7:
                texte += dizaine_spec[unite_montant]
            elif unite_montant > 6:
                texte += dizaine[dizaines]
                if dizaines == 7:
                    texte += "-dix "
                if dizaines == 9:
                    texte += "-dix "
                if unite_montant > 0:
                    if dizaines > 0:
                        texte += "-"
                    texte += unite[unite_montant]
            else:
                texte += dizaine[dizaines]
        else:
            texte += dizaine[dizaines]

            if unite_montant > 0:
                if dizaines == 7 and unite_montant > 6:
                    texte += "-dix"
                if dizaines == 9 and unite_montant > 6:
                    texte += "-dix"
                if dizaines > 0:
                    if unite_montant == 1 and dizaines != 9 and dizaines != 8:
                        texte += " et "
                    else:
                        texte += "-"
                if unite_montant < 7 and dizaines == 7:
                    texte += dizaine_spec[unite_montant]
                elif unite_montant < 7 and dizaines == 9:
                    texte += dizaine_spec[unite_montant]
                else:
                    texte += unite[unite_montant]
            else:
                if dizaines == 7:
                    texte += "-dix"
                if dizaines == 9:
                    texte += "-dix"

        return texte.strip()

    def convertir_en_lettres_mg(self, montant):
        # Listes représentant les mots pour les nombres en malgache
        unites = ["", "iray", "roa", "telo", "efatra", "dimy", "enina", "fito", "valo", "sivy"]
        dizaines = ["", "folo", "roapolo", "telopolo", "efapolo", "dimampolo", "enimpolo", "fitopolo", "valopolo",
                    "sivy folo"]

        if montant == 0:
            return ""
        else:
            texte = ""

        # Extraire les parties en millions, milliers, centaines, dizaines et unités
        partie_millions = montant // 1000000
        montant %= 1000000
        partie_milliers = montant // 1000
        montant %= 1000
        partie_centaines = montant // 100
        montant %= 100
        partie_dizaines = montant // 10  # 1.1
        partie_unites = montant % 10  # 1

        # Traiter les parties dizaines et unités
        if partie_dizaines > 0:
            if partie_unites > 0:
                if partie_unites == 1:
                    texte += "iraika amby "
                elif partie_centaines > 0 and partie_unites == 1 or partie_unites == 1:
                    texte += "iraika amby "
                else:
                    # Ajouter les unités et le séparateur si les dizaines et les unités sont présentes
                    texte += unites[partie_unites] + " amby "
            if partie_centaines > 1 or partie_milliers > 0 or partie_millions > 0:
                texte += dizaines[partie_dizaines] + " sy "
            else:
                texte += dizaines[partie_dizaines] + " "
        else:
            if partie_centaines > 1 or partie_milliers > 0 or partie_millions > 0:
                if partie_unites > 0:
                    texte += unites[partie_unites] + " sy "
            else:
                texte += unites[partie_unites] + " "
                # Seules les unités sont présentes

        # Traiter la partie en centaines
        if partie_centaines > 0:
            if partie_dizaines > 0 or partie_unites > 0:
                if partie_centaines == 1:
                    texte += " amby "
            if partie_centaines == 1:
                texte += "zato "
                if partie_milliers > 0:
                    texte += "sy "
            elif partie_centaines == 2 or partie_centaines == 3:
                texte += unites[partie_centaines] + "njato "
                if partie_milliers > 0:
                    texte += "sy "
            elif partie_centaines == 4:
                texte += "efajato "
                if partie_milliers > 0:
                    texte += "sy "
            elif partie_centaines == 5:
                texte += "dimanjato "
                if partie_milliers > 0:
                    texte += "sy "
            elif partie_centaines == 6:
                texte += "eninjato "
                if partie_milliers > 0:
                    texte += "sy "
            elif 6 < partie_centaines < 9:
                texte += unites[partie_centaines] + "njato "
                if partie_milliers > 0:
                    texte += "sy "
            elif partie_centaines == 9:
                texte += "sivinjato "
                if partie_milliers > 0:
                    texte += "sy "

        # Traiter la partie en milliers
        if partie_milliers > 0:
            if partie_milliers == 1:
                texte += "arivo"
            elif 1 < partie_milliers < 10:
                texte += self.convertir_en_lettres_mg(partie_milliers) + " arivo "
            elif 10 <= partie_milliers < 100:
                texte += self.convertir_en_lettres_mg(int(partie_milliers % 10) * 1000)
                if partie_milliers % 10 > 0:
                    texte += " sy "
                texte += self.convertir_en_lettres_mg(partie_milliers // 10) + " alina"
            elif partie_milliers >= 100:
                texte += self.convertir_en_lettres_mg(int(partie_milliers % 100) * 1000)
                if partie_milliers % 100 > 0:
                    texte += " sy "
                texte += self.convertir_en_lettres_mg(partie_milliers // 100) + " hetsy"
            texte += " "

        # Traiter la partie en millions
        if partie_millions > 0:
            if partie_dizaines > 0 or partie_unites > 0 or partie_centaines > 0 or partie_milliers > 0:
                texte += " sy "
            texte += self.convertir_en_lettres_mg(partie_millions) + " tapitrisa"
            texte += " "

        return texte.strip()









