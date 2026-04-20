# -*- coding: utf-8 -*-
from PyQt4 import Qt, QtGui, QtCore
from PyQt4.QtGui import QMessageBox
from PyQt4.Qt import QApplication
from .EtatAffichage import Ui_Dialog
import globalvars
from models.Commune import Commune
from models.District import District
from models.Region import Region
from models.Demande import Demande
from .Html2Pdf import Html2Pdf
import os
import os.path
import webbrowser
import tempfile
from random import randint
from Utils import Utils
import datetime
from xlwt import Workbook
from xlwt import Style
from PyPDF2 import PdfFileMerger
import psycopg2
import psycopg2.extras


class EtatAffichageRun(QtGui.QDialog):
    def __init__(self, parent, connection, template=None, orientation="Landscape", exportToRL=False, isPVRL = False):
        QtGui.QDialog.__init__(self, parent)
        self.setModal(True)
        self.connection, self.template, self.orientation = connection, template, orientation
        self.demandes = []
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.exportToRL = exportToRL
        self.isPVRL = isPVRL
        self.paths = []
        appStyle = """  
                QTableWidget 
                {

        	        alternate-background-color: #87cefa;
             	    background-color: white;
                }
                """

        if self.template == 'fanapahana.html':
            self.setWindowTitle(u'Fanapahana (Décision)')
        self.setStyleSheet(appStyle)
        self.init_actions()
        self.solotenaKaominina, self.solotenaKaomininaMpisolo, self.solotenaFkt, self.solotenaFktMpisolo, self.rad1, self.rad1Mpisolo, self.rad2, self.rad2Mpisolo, self.rad3, self.rad3Mpisolo, self.mpiasaBif, self.mpiasaBifMpisolo = '', '', '', '', '', '', '', '', '', '', '', ''
        self.ui.tableWidget.setAlternatingRowColors(True)
        self.ui.dateEditDemande.setDate(QtCore.QDate.currentDate())
        self.commune = Commune.findById(self.connection, globalvars.id_commune)
        self.district = District.findById(self.connection, self.commune.iddistrict)
        self.region = Region.findById(self.connection, self.district.idregion)
        self.ui.lineEditCommune.setText(self.commune.nomcommune)
        self.ui.checkBoxNumDecision.setChecked(False)
        self.ui.checkBoxDateDecision.setChecked(False)
        self.set_field_status()
        self.book = Workbook()
        self.book_to_export = Workbook()
        Utils.resizeTableWidgetColumn(self.ui.tableWidget, [1, 3], 200)
        self.nomHameau = ''
        self.nomFokontany = ''
        self.numDecision = ''
        self.dateDecision = ''
        self.dateReconnaissance = ''
        self.debutAffichage = ''
        self.finAffichage = ''
        self.nbrJour = 0
        self.metadata = {"numpages": 1}
        self.ui.labelCurrent.setText("1")
        self.update_navigation_buttons()
        if self.exportToRL:
            self.ui.pushButtonPrint.setText('Export EXCEL')
            self.setWindowTitle("Export pour Reconnaissance Locale")
        if self.isPVRL:
            self.ui.pushButtonPrint.setText('Export PVRL')
            self.setWindowTitle("Export PVRL")
            self.paths = []

    def set_field_status(self):
        self.ui.lineEditNumDemande.setEnabled(self.ui.checkBoxNumDemande.isChecked())
        self.ui.dateEditDemande.setEnabled(self.ui.checkBoxDateDemande.isChecked())
        self.ui.lineEditDemandeur.setEnabled(self.ui.checkBoxDemandeur.isChecked())
        self.ui.lineEditHameau.setEnabled(self.ui.checkBoxHameau.isChecked())
        self.ui.lineEditNumDecision.setEnabled(self.ui.checkBoxNumDecision.isChecked())
        self.ui.dateEditDecision.setEnabled(self.ui.checkBoxDateDecision.isChecked())

    def init_actions(self):
        self.ui.checkBoxNumDemande.stateChanged.connect(self.set_field_status)
        self.ui.checkBoxDateDemande.stateChanged.connect(self.set_field_status)
        self.ui.checkBoxDemandeur.stateChanged.connect(self.set_field_status)
        self.ui.checkBoxHameau.stateChanged.connect(self.set_field_status)
        self.ui.checkBoxNumDecision.stateChanged.connect(self.set_field_status)
        self.ui.checkBoxDateDecision.stateChanged.connect(self.set_field_status)
        self.ui.pushButtonFind.clicked.connect(self.find)
        self.ui.pushButtonCancel.clicked.connect(self.reject)
        if self.exportToRL:
            self.ui.pushButtonPrint.clicked.connect(self.exportXL)
        elif self.isPVRL:
            self.ui.pushButtonPrint.clicked.connect(self.exportPVRL)
        else:
            self.ui.pushButtonPrint.clicked.connect(self.doprint)
        self.ui.checkBoxCheckAll.stateChanged.connect(self.set_check_all)
        ''' Paginations '''
        self.ui.pushButtonNext.clicked.connect(self.goto_next)
        self.ui.pushButtonPrevious.clicked.connect(self.goto_previous)
        self.ui.pushButtonFirst.clicked.connect(self.goto_first)
        self.ui.pushButtonLast.clicked.connect(self.goto_last)
        self.ui.comboBoxPages.currentIndexChanged.connect(self.goto_page)

    def find(self):
        wheres = []
        if self.ui.checkBoxNumDemande.isChecked():
            t = "'%" + str(self.ui.lineEditNumDemande.text()).replace("'", "''") + "%'"
            wheres.append("(demande.numdemande LIKE " + t + " OR demande.numdemandepaps LIKE " + t + ")")
        if self.ui.checkBoxNumDecision.isChecked():
            #t = "'%" + str(self.ui.lineEditNumDemande.text()).replace("'", "''") + "%'"
            t ="'" + str(self.ui.lineEditNumDecision.text()).strip().upper().replace("'", "''") + "'"
            wheres.append("(UPPER(demande.numdecision) = " + t +  ")")
        if self.ui.checkBoxDateDemande.isChecked():
            wheres.append("CAST(demande.datedemande AS date) = '%s'" % (str(self.ui.dateEditDemande.date().toString("yyyy-MM-dd"))))
        if self.ui.checkBoxDateDecision.isChecked():
            wheres.append("CAST(demande.datedecision AS date) = '%s'" % (str(self.ui.dateEditDecision.date().toString("yyyy-MM-dd"))))
        if self.ui.checkBoxDemandeur.isChecked():
            wheres.append("LOWER(nom) LIKE '%" + str(self.ui.lineEditDemandeur.text()).lower().replace("'", "''") + "%'")
        if self.ui.checkBoxHameau.isChecked():
            wheres.append("(LOWER(codehameau) LIKE '%" +
                          str(self.ui.lineEditHameau.text()).replace("'", "''") + "%') OR (LOWER(nomhameau) LIKE '%" +
                          str(self.ui.lineEditHameau.text()).replace("'", "''") + "%')")
        wheres.append(
            "demande.idcommune  = '%s'" % (str(globalvars.id_commune)))
        page = int(self.ui.labelCurrent.text())
        #Pas besoin de pagination
        withLimite = False
        if self.isPVRL:
            self.demandes = Demande.find_where_PV(self.connection, self.metadata, wheres, page, False)
        else:
            self.demandes = Demande.find_where(self.connection, self.metadata, wheres, page, False)
        self.ui.tableWidget.setRowCount(len(self.demandes))
        for i, d in enumerate(self.demandes):
            if i == 0:
                self.numDecision = str(d.numdecision)
                self.nomHameau = str(d.nomhameau)
                self.nomFokontany = str(d.nomfokontany)
                if d.dateReconnaissance is not None:
                    self.dateReconnaissance = d.dateReconnaissance.strftime('%d/%m/%Y')
                if d.datedecision is not None:
                    self.dateDecision = d.datedecision.strftime('%d/%m/%Y')
                if d.debutaffichage is not None:
                    self.debutAffichage = d.debutaffichage.strftime('%d/%m/%Y')
                if d.finaffichage is not None:
                    self.finAffichage = d.finaffichage.strftime('%d/%m/%Y')
                self.nbrJour = d.nbreJour
                #MEMBRE CRL
                if len(d.membre_crl) > 0:
                    for dico in d.membre_crl:
                        for key, val in dico.items():
                            print key
                            if key == '2_t':
                                self.solotenaKaominina = val
                            if key == '2_f':
                                self.solotenaKaomininaMpisolo = val
                            if key == '3_t':
                                self.solotenaFkt = val
                            if key == '3_f':
                                self.solotenaFktMpisolo = val
                            if key == '4_t':
                                self.rad1 = val
                            if key == '4_f':
                                self.rad1Mpisolo = val
                            if key == '5_t':
                                self.rad2 = val
                            if key == '5_f':
                                self.rad2Mpisolo = val
                            if key == '6_t':
                                self.rad3 = val
                            if key == '6_f':
                                self.rad3Mpisolo = val
                            if key == '7_t':
                                self.mpiasaBif = val
                            if key == '7_f':
                                self.mpiasaBifMpisolo = val

            #print d.nomfokontany
            #n = str(d.numdemandepaps) if (d.numdemandepaps is not None and d.numdemandepaps != '') else str(d.numdemande)
            n = d.numdemande
            item = QtGui.QTableWidgetItem(True)
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Checked)
            self.ui.tableWidget.setItem(i, 0, item)
            self.ui.tableWidget.setItem(i, 1, QtGui.QTableWidgetItem(n))
            self.ui.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(str(d.datedemande)))
            self.ui.tableWidget.setItem(i, 3, QtGui.QTableWidgetItem(str(d.nom).decode('utf-8')))
            self.ui.tableWidget.setItem(i, 5, QtGui.QTableWidgetItem(str(d.adressepersonne)))
            self.ui.tableWidget.setItem(i, 6, QtGui.QTableWidgetItem(str(d.codehameau) + " - " + str(d.nomhameau)))
            self.ui.tableWidget.setItem(i, 7, QtGui.QTableWidgetItem(str(d.surface)))
        for i in range(1, 6):
            Utils.setTableWidgetColumnReadOnly(self.ui.tableWidget, i)
        self.update_navigation_buttons()
        if withLimite == True:
            self.fill_combo_pages()

    def doprint(self):
        rows = []
        commune = str(Utils.emptyifnull(self.commune, "nomcommune"))
        for idx, i in enumerate(self.demandes):
            nord = ''
            sud = ''
            est = ''
            ouest = ''
            if len(i.limites) > 0:
                for lim in i.limites:
                    for key, val in lim.items():
                        if key == '4':
                            nord = val
                        if key == '5':
                            sud = val
                        if key == '6':
                            est = val
                        if key == '11':
                            ouest = val

            c = self.ui.tableWidget.item(idx, 0).checkState()

            if c:
                #n = str(i.numdemandepaps) if (i.numdemandepaps is not None and i.numdemandepaps != '') else str(i.numdemande)
                n = str(i.numdemande)

                d = datetime.date.today()
                dic = {
                    "$kaominina": commune,
                    "$distrika": str(Utils.emptyifnull(self.district, "nomdistrict")),
                    "$faritra": str(Utils.emptyifnull(self.region, "nomregion")),
                    "$fokontany": self.nomFokontany,
                    "$vohitra": self.nomHameau,
                    "$numDecision": self.numDecision.upper(),
                    "$daatedecision": self.dateDecision,
                    "$daatereconnaissance": self.dateReconnaissance,
                    "$debutAffichage": self.debutAffichage,
                    "$finAffichage": self.finAffichage,
                    "$nbreJour": str(self.nbrJour),
                    "$kom": commune[:3].upper(),
                    "$annee": str(datetime.date.today().year),
                    "$date": d.strftime("%d/%m/%Y"),
                    "$solotenaKaominina": str(self.solotenaKaominina.split(':')[0]),
                    "$solotenaMpisoloKaominina": str(self.solotenaFktMpisolo.split(':')[0]),
                    "$solotenaFkt": str(self.solotenaFkt.split(':')[0]),
                    "$solotenaMpisoloFkt": str(self.solotenaFktMpisolo.split(':')[0]),
                    "$rad1": str(self.rad1.split(':')[0]),
                    "$rad2": str(self.rad2.split(':')[0]),
                    "$rad3": str(self.rad3.split(':')[0]),
                    "$radMpisolo1":str(self.rad1Mpisolo.split(':')[0]),
                    "$radMpisolo2":str(self.rad2Mpisolo.split(':')[0]),
                    "$radMpisolo3":str(self.rad3Mpisolo.split(':')[0]),
                    "$bif": str(self.mpiasaBif.split(':')[0]),
                    "$soloBif": str(self.mpiasaBifMpisolo.split(':')[0]),
                    "$rows": rows,
                }
                rows.append({
                    "id": i.iddemande,
                    "num": n,
                    "date": i.datedemande.strftime("%d/%m/%Y"),
                    "nom": str(i.nom).decode('utf-8'),
                    "adiresy": str(i.adresse).decode('utf-8'),
                    #"limite": i.limite,
                    "voisinNord": nord,
                    "voisinSud": sud,
                    "voisinEst": est,
                    "voisinOuest": ouest,
                    "codeParcelle": i.codeParcelle,
                    "planchePlof": i.codePlanche,
                    "surface": i.surface,
                    "hameau": str(i.codehameau) + " - " + str(i.nomhameau),
                    "adresse": str(i.adressepersonne),
                    "voisin_0_adresse": i.voisins[0]["adresse"] if len(i.voisins) > 0 else "-",
                    "voisin_0_nom": i.voisins[0]["nom"] if len(i.voisins) > 0 else "-",
                    "voisin_0_prenom": i.voisins[0]["prenom"] if len(i.voisins) > 1 else "-",
                    "voisin_1_adresse": i.voisins[1]["adresse"] if len(i.voisins) > 0 else "-",
                    "voisin_1_nom": i.voisins[1]["nom"] if len(i.voisins) > 0 else "-",
                    "voisin_1_prenom": i.voisins[1]["prenom"] if len(i.voisins) > 1 else "-",
                })
        converter = Html2Pdf()
        converter.setOrientation(orientation=self.orientation)
        src = os.path.dirname(__file__) + "/" + self.template
        print 'src loaded'
        dst = os.path.join(tempfile.gettempdir(), str(randint(10000, 99999)) + "-" + self.template + ".pdf")
        QApplication.setOverrideCursor(Qt.Qt.WaitCursor)
        try:
            converter.generate(html=src, pdf=dst, dictionnary=dic)
        except Exception as err:
            print "erreur creation pdf"
            print err
        webbrowser.open(dst)
        QApplication.restoreOverrideCursor()
        #PDF liste annexe
        if self.template == 'fanapahana.html':
            try:
                self.createXlsFile()
            except Exception as err:
                print "erreur excel"
                print err
            #template2 = 'listeannexe.html'
            #converter2 = Html2Pdf()
            #converter2.setOrientation(orientation=self.orientation)
            #src2 = os.path.dirname(__file__) + "/" + template2
            #dst2 = os.path.join(tempfile.gettempdir(), str(randint(10000, 99999)) + "-" + template2 + ".pdf")
            #QApplication.setOverrideCursor(Qt.Qt.WaitCursor)
            #converter2.generate(html=src2, pdf=dst2, dictionnary=dic)
            #webbrowser.open(dst2)
            #QApplication.restoreOverrideCursor()

    def set_check_all(self):
        checked = QtCore.Qt.Checked if self.ui.checkBoxCheckAll.isChecked() else QtCore.Qt.Unchecked
        for idx, i in enumerate(self.demandes):
            self.ui.tableWidget.item(idx, 0).setCheckState(checked)

    ''' ************************************ paginations ************************************ '''
    def goto_next(self):
        current = int(self.ui.labelCurrent.text()) + 1
        self.ui.labelCurrent.setText(str(current))
        self.find()

    def goto_previous(self):
        current = int(self.ui.labelCurrent.text()) - 1
        self.ui.labelCurrent.setText(str(current))
        self.find()

    def goto_first(self):
        self.ui.labelCurrent.setText("1")
        self.find()

    def goto_last(self):
        self.ui.labelCurrent.setText(str(self.metadata["numpages"]))
        self.find()

    def goto_page(self):
        index = self.ui.comboBoxPages.currentIndex() + 1
        self.ui.labelCurrent.setText(str(index))
        self.find()

    def update_navigation_buttons(self):
        current = int(self.ui.labelCurrent.text())
        self.ui.pushButtonFirst.setEnabled(current > 1)
        self.ui.pushButtonPrevious.setEnabled(current > 1)
        self.ui.pushButtonNext.setEnabled(current < self.metadata["numpages"])
        self.ui.pushButtonLast.setEnabled(current < self.metadata["numpages"])

    def fill_combo_pages(self):
        self.ui.comboBoxPages.blockSignals(True)
        self.ui.comboBoxPages.clear()
        current = int(self.ui.labelCurrent.text())
        for i in range(self.metadata["numpages"]):
            self.ui.comboBoxPages.addItem("%s/%s" % (i + 1, self.metadata["numpages"]))
        self.ui.comboBoxPages.setCurrentIndex(current - 1)
        self.ui.comboBoxPages.blockSignals(False)

    def createXlsFile(self):
        feuille = self.book.add_sheet("Liste" + str(randint(10000, 99999)), True)
        styleTitreAvecFondGris = Style.easyxf(
            'font: bold on, height 200; align: wrap on, vert centre, horiz center; pattern: pattern solid, fore_colour gray25; borders: left 2, right 2, top 2, bottom 2')
        styleDonneeSansFond = Style.easyxf(
            'font: height 200; align: wrap on, vert centre, horiz left; borders: left 2, right 2, top 2, bottom 2')
        ### TITRE ####
        commune = str(Utils.emptyifnull(self.commune, "nomcommune"))
        feuille.write_merge(0,0, 0, 6, u"Kaominina /Commune : " + commune + u"  Fokontany : " + self.nomFokontany + u" Vohitra / Hameau : " + self.nomHameau + "")
        feuille.write_merge(1, 1, 0, 6,u"LISITRA TOVANA MAHAKASIKA IREO MPANGATAKA KARA-TANY VOALAZA AMIN’NY FANAPAHANA laharana faha- " + self.numDecision + " . ")
        feuille.write_merge(2, 2, 0, 6,u"Liste annexe des demandeurs CF selon la decision communale ")
        feuille.write_merge(2, 2, 0, 6,u"natao ny " + self.dateDecision + u"  momba ny fitsirihana ifotony hatao amin’ny datin’ny  " + self.dateReconnaissance + " . ")
        feuille.write_merge(3, 3, 0, 1,u'du')
        feuille.write_merge(3, 3, 2, 3,u"pour la reconnaissance locale en date du")
        feuille.write(6, 4, u"MPIFANILA", styleTitreAvecFondGris)
        feuille.merge(6, 6, 4, 8)
        ##########ajouster la taille des colonenes
        feuille.col(0).width = (1 + len("Laharana TANY /")) * 256
        feuille.col(1).width = (1 + len("Laharana FANGATAHANA /")) * 256
        feuille.col(2).width = (1 + len("Datin'ny fangatahana /")) * 256
        feuille.col(3).width = (1 + len("ANARAN'NY MPANGATAKA KARATANY /")) * 256
        feuille.col(4).width = (1 + len("Adiresy / Adresse")) * 256
        feuille.col(5).width = (1 + len("Avaratra/Nord")) * 256
        feuille.col(6).width = (1 + len("Atsimo/Sud")) * 256
        feuille.col(7).width = (1 + len("Atsinana/Est")) * 256
        feuille.col(8).width = (1 + len("Andrefana/Ouest")) * 256
        feuille.col(9).width = (1 + len("KAODY PLANCHE PLOF")) * 256
        feuille.col(10).width = (1 + len("DATE RL ")) * 256
        #########fin ajustement de la taille des colonnes
        feuille.write(7, 0, u"Laharana TANY / Numero parcelle", styleTitreAvecFondGris)
        feuille.write(7, 1, u"Laharana FANGATAHANA / numero de demande", styleTitreAvecFondGris)
        feuille.write(7, 2, u"Datin'ny fangatahana / Date de demande", styleTitreAvecFondGris)
        feuille.write(7, 3, u"ANARAN'NY MPANGATAKA KARATANY / NOM DEMANDEUR", styleTitreAvecFondGris)
        feuille.write(7, 4, u"Adiresy / Adresse", styleTitreAvecFondGris)
        feuille.write(7, 5, u"Avaratra/Nord", styleTitreAvecFondGris)
        feuille.write(7, 6, u"Atsimo/Sud", styleTitreAvecFondGris)
        feuille.write(7, 7, u"Atsinana/Est", styleTitreAvecFondGris)
        feuille.write(7, 8, u"Andrefana/Ouest", styleTitreAvecFondGris)
        feuille.write(7, 9, u"KAODY PLANCHE PLOF", styleTitreAvecFondGris)
        feuille.write(7, 10, u"DATE RL ", styleTitreAvecFondGris)

        rows = []

        xl_curr_row = 8
        for idx, i in enumerate(self.demandes):


            c = self.ui.tableWidget.item(idx, 0).checkState()

            if c:
                nord = ''
                sud = ''
                est = ''
                ouest = ''
                for lim in i.limites:
                    for key, val in lim.items():
                        if key == '4':
                            nord = val
                        if key == '5':
                            sud = val
                        if key == '6':
                            est = val
                        if key == '11':
                            ouest = val
                #n = str(i.numdemandepaps) if (i.numdemandepaps is not None and i.numdemandepaps != '') else str(i.numdemande)
                n = i.numdemande

                d = datetime.date.today()

                feuille.write(xl_curr_row, 0, i.codeParcelle, styleDonneeSansFond)
                feuille.write(xl_curr_row, 1, n, styleDonneeSansFond)
                feuille.write(xl_curr_row, 2,i.datedemande.strftime("%d/%m/%Y"), styleDonneeSansFond)
                feuille.write(xl_curr_row, 3, str(i.nom).decode('utf-8'), styleDonneeSansFond)
                feuille.write(xl_curr_row, 4, str(i.adresse).decode('utf-8'), styleDonneeSansFond)
                feuille.write(xl_curr_row, 5, nord, styleDonneeSansFond)
                feuille.write(xl_curr_row, 6, sud, styleDonneeSansFond)
                feuille.write(xl_curr_row, 7, est, styleDonneeSansFond)
                feuille.write(xl_curr_row, 8, ouest, styleDonneeSansFond)
                feuille.write(xl_curr_row, 9, i.codePlanche, styleDonneeSansFond)
                feuille.write(xl_curr_row, 10, self.dateReconnaissance, styleDonneeSansFond)

                xl_curr_row = xl_curr_row + 1


        dst = os.path.join(tempfile.gettempdir(), str(randint(10000, 99999)) + "-" + "Liste_annexes_Decision_" + self.numDecision.replace('/', '_') + ".xls")
        # dst = os.path.dirname(__file__) + "/" + str(randint(10000, 99999)) + "-" + "Registre de demande.xls"
        self.book.save(dst)
        os.startfile(dst)

    def exportXL(self):
        feuille = self.book_to_export.add_sheet("Pour RL Liste" + str(randint(10000, 99999)), True)
        styleTitreAvecFondGris = Style.easyxf(
            'font: bold on, height 200; align: wrap on, vert centre, horiz center; pattern: pattern solid, fore_colour gray25; borders: left 2, right 2, top 2, bottom 2')
        styleTitreAvecFondOrange = Style.easyxf(
            'font: bold on, height 200; align: wrap on, vert centre, horiz center; pattern: pattern solid, fore_colour light_orange; borders: left 2, right 2, top 2, bottom 2')
        styleTitreAvecFondVert = Style.easyxf(
            'font: bold on, height 200; align: wrap on, vert centre, horiz center; pattern: pattern solid, fore_colour light_green; borders: left 2, right 2, top 2, bottom 2')
        styleTitreAvecFondMarron = Style.easyxf(
            'font: bold on, height 200; align: wrap on, vert centre, horiz center; pattern: pattern solid, fore_colour light_yellow; borders: left 2, right 2, top 2, bottom 2')
        styleTitreAvecFondIceBlue = Style.easyxf(
            'font: bold on, height 200; align: wrap on, vert centre, horiz center; pattern: pattern solid, fore_colour ice_blue; borders: left 2, right 2, top 2, bottom 2')
        styleTitreAvecFondBleu = Style.easyxf(
            'font: bold on, height 200; align: wrap on, vert centre, horiz center; pattern: pattern solid, fore_colour sky_blue; borders: left 2, right 2, top 2, bottom 2')
        styleDonneeSansFond = Style.easyxf(
            'font: height 200; align: wrap on, vert centre, horiz left; borders: left 2, right 2, top 2, bottom 2')
        ### TITRE ####
        region = str(Utils.emptyifnull(self.region, "nomregion"))
        district = str(Utils.emptyifnull(self.district, "nomdistrict"))
        commune = str(Utils.emptyifnull(self.commune, "nomcommune"))

        ##########ajouster la taille des colonenes
        entetes = ["FARITRA","DISTRIKA","KAOMININA","FOKONTANY","VOHITRA","TOERANA MISY NY TANY (LIEU DIT)","KAODY PLANCHE PLOF","ANARAN'NY MPANDRAY FANGATAHANA","ANARAN'NY MPANGATAKA KARATANY",
                   "LAHY / VAVY (L/V)","DATY NAHATERAHANA","NE VERS","LAHARAN'NY KARAPANONDRO","LAHARAN'NY KOPIA NAHATERAHANA","DATY NAHAZOANA KARAPANONDRO NA KOPIA","TOERANA NAHAZOANA KARAPANONDRO NA KOPIA",
                   "ADIRESY    ","SOKAJINTANY","ZAVA-MISY EO AMIN'NY TANY (CONSISTANCE)","LAHARANA TANY (CODE PARCELLE)","LAHARANA FANGATAHANA","DATIN'NY FANGATAHANA",
                   "MPIFANILA AVARATRA","MPIFANILA ATSIMO","MPIFANILA ATSINANANA","MPIFANILA ANDREFANA","NUMERO DECISION","DATE DECISION","DATE DEBUT AFFICHAGE",
                   "DATE FIN AFFICHAGE","DATE RECONNAISSANCE","SOLOTENA COMMUNE","NUMERO CIN SOLOTENA COMMUNE","SOLOTENA COMMUNE MPISOLO TOERANA","NUMERO CIN SOLOTENA COMMUNE MPISOLO TOERANA","SOLOTENA FOKONTANY",
                   "NUMERO CIN SOLOTENA FOKONTANY","SOLOTENA FOKONTANY MPISOLO TOERANA","NUMERO CIN SOLOTENA FOKONTANY MPISOLO TOERANA","RAIAMANDERNY 1","NUMERO CIN RAIAMANDERNY 1","RAIAMANDERNY 1 MPISOLO TOERANA",
                   "NUMERO CIN RAIAMANDERNY 1 MPISOLO TOERANA","RAIAMANDERNY 2","NUMERO CIN RAIAMANDERNY 2","RAIAMANDERNY 2 MPISOLO TOERANA","NUMERO CIN RAIAMANDERNY 2 MPISOLO TOERANA","RAIAMANDERNY 3",
                   "NUMERO CIN RAIAMANDERNY 3","RAIAMANDERNY 3 MPISOLO TOERANA","NUMERO CIN RAIAMANDERNY 3 MPISOLO TOERANA","MPIASAN'NY BIF","NUMERO CIN MPIASAN'NY BIF","MPIASAN'NY BIF MPISOLO TOERANA",
                   "NUMERO CIN MPIASAN'NY BIF MPISOLO TOERANA"]
        l = 0
        while (l < len(entetes) ):
            feuille.col(l).width = (1 + len(entetes[l])) * 256
            if l <= 7:
                feuille.write(0, l, entetes[l], styleTitreAvecFondOrange)
            if l >= 8 and l <= 16:
                feuille.write(0, l, entetes[l], styleTitreAvecFondVert)
            if l >= 17 and l <= 25:
                feuille.write(0, l, entetes[l], styleTitreAvecFondMarron)
            if l >= 26 and l <= 29:
                feuille.write(0, l, entetes[l], styleTitreAvecFondBleu)
            if l >= 30:
                feuille.write(0, l, entetes[l], styleTitreAvecFondIceBlue)
            l = l + 1

        rows = []

        xl_curr_row = 1
        for idx, i in enumerate(self.demandes):
            print "curr_idx = "
            print xl_curr_row


            c = self.ui.tableWidget.item(idx, 0).checkState()

            if c:
                #VOISINS
                nord = ''
                sud = ''
                est = ''
                ouest = ''
                for lim in i.limites:
                    for key, val in lim.items():
                        if key == '4':
                            nord = val
                        if key == '5':
                            sud = val
                        if key == '6':
                            est = val
                        if key == '11':
                            ouest = val

                # MEMBRE CRL
                if len(i.membre_crl) > 0:
                    for dico in i.membre_crl:
                        for key, val in dico.items():
                            print key
                            if key == '2_t':
                                self.solotenaKaominina = val
                            if key == '2_f':
                                self.solotenaKaomininaMpisolo = val
                            if key == '3_t':
                                self.solotenaFkt = val
                            if key == '3_f':
                                self.solotenaFktMpisolo = val
                            if key == '4_t':
                                self.rad1 = val
                            if key == '4_f':
                                self.rad1Mpisolo = val
                            if key == '5_t':
                                self.rad2 = val
                            if key == '5_f':
                                self.rad2Mpisolo = val
                            if key == '6_t':
                                self.rad3 = val
                            if key == '6_f':
                                self.rad3Mpisolo = val
                            if key == '7_t':
                                self.mpiasaBif = val
                            if key == '7_f':
                                self.mpiasaBifMpisolo = val
                #n = str(i.numdemandepaps) if (i.numdemandepaps is not None and i.numdemandepaps != '') else str(
                    #i.numdemande)
                n = i.numdemande

                d = datetime.date.today()
                k = 0
                while (k < len(i.demandeurs)):
                    feuille.write(xl_curr_row, 0, region, styleDonneeSansFond)
                    feuille.write(xl_curr_row, 1, district, styleDonneeSansFond)
                    feuille.write(xl_curr_row, 2, commune, styleDonneeSansFond)
                    feuille.write(xl_curr_row, 3, str(i.nomfokontany), styleDonneeSansFond)
                    feuille.write(xl_curr_row, 4, str(i.nomhameau), styleDonneeSansFond)
                    feuille.write(xl_curr_row, 5, str(i.lieudit), styleDonneeSansFond)
                    feuille.write(xl_curr_row, 6, str(i.codePlanche), styleDonneeSansFond)
                    feuille.write(xl_curr_row, 7, str(i.collecteur), styleDonneeSansFond)

                    #MOMBAN'NY MPANGATKA
                    if k == i.idx_dem_principale:
                        feuille.write(xl_curr_row, 8, str(i.nom), styleDonneeSansFond)
                        feuille.write(xl_curr_row, 9, i.genre, styleDonneeSansFond)
                        feuille.write(xl_curr_row, 10, i.dateNaissance, styleDonneeSansFond)
                        feuille.write(xl_curr_row, 11, i.ne_vers, styleDonneeSansFond)
                        feuille.write(xl_curr_row, 12, i.num_cin, styleDonneeSansFond)
                        feuille.write(xl_curr_row, 13, i.num_copie, styleDonneeSansFond)
                        feuille.write(xl_curr_row, 14, i.datepi, styleDonneeSansFond)
                        feuille.write(xl_curr_row, 15, i.lieupi, styleDonneeSansFond)
                        feuille.write(xl_curr_row, 16, i.adressepersonne, styleDonneeSansFond)

                    else:
                        feuille.write(xl_curr_row, 8, i.demandeurs[k]['nom'], styleDonneeSansFond)
                        genre = 'L'
                        if i.demandeurs[k]['genre'] == 'feminin':
                            genre = 'V'
                        feuille.write(xl_curr_row, 9, genre, styleDonneeSansFond)
                        datenaiss = ''
                        if i.demandeurs[k]['datenaissance'] != '1000-01-01':
                            datenaiss = datetime.datetime.strptime(i.demandeurs[k]['datenaissance'],('%Y-%m-%d')).strftime("%d/%m/%Y")
                        feuille.write(xl_curr_row, 10, datenaiss, styleDonneeSansFond)
                        feuille.write(xl_curr_row, 11, i.demandeurs[k]['nevers'], styleDonneeSansFond)
                        feuille.write(xl_curr_row, 12, i.demandeurs[k]['numci'], styleDonneeSansFond)
                        feuille.write(xl_curr_row, 13, i.demandeurs[k]['numacte'], styleDonneeSansFond)

                        datepi, numpi, lieupi = '','',''
                        if i.demandeurs[k]['numci'] != '':
                            if i.demandeurs[k]['dateci'] != '1000-01-01':
                                datepi = datetime.datetime.strptime(i.demandeurs[k]['dateci'], ('%Y-%m-%d')).strftime("%d/%m/%Y")
                            if i.demandeurs[k]['lieuci'] != '':
                                lieupi = i.demandeurs[k]['lieuci']
                        else:
                            if i.demandeurs[k]['numacte'] != '':
                                if i.demandeurs[k]['dateacte'] != '1000-01-01':
                                    datepi = datetime.datetime.strptime(i.demandeurs[k]['dateacte'],
                                                                    ('%Y-%m-%d')).strftime("%d/%m/%Y")
                                if i.demandeurs[k]['lieuacte'] != '':
                                    lieupi = i.demandeurs[k]['lieuacte']
                        feuille.write(xl_curr_row, 14, i.datepi, styleDonneeSansFond)
                        feuille.write(xl_curr_row, 15, i.lieupi, styleDonneeSansFond)
                        feuille.write(xl_curr_row, 16, i.demandeurs[k]['adresse'], styleDonneeSansFond)
                    #FARANY MOMBAN'NY MPANGATAKA
                    feuille.write(xl_curr_row, 17, i.categorie, styleDonneeSansFond)
                    feuille.write(xl_curr_row, 18, i.consistance, styleDonneeSansFond)
                    feuille.write(xl_curr_row, 19, i.codeParcelle , styleDonneeSansFond)
                    feuille.write(xl_curr_row, 20, i.numdemande, styleDonneeSansFond)
                    feuille.write(xl_curr_row, 21, i.datedemande.strftime('%d/%m/%Y'), styleDonneeSansFond)
                    feuille.write(xl_curr_row, 22, nord, styleDonneeSansFond)
                    feuille.write(xl_curr_row, 23, sud, styleDonneeSansFond)
                    feuille.write(xl_curr_row, 24, est, styleDonneeSansFond)
                    feuille.write(xl_curr_row, 25, ouest, styleDonneeSansFond)
                    feuille.write(xl_curr_row, 26, i.numdecision, styleDonneeSansFond)
                    feuille.write(xl_curr_row, 27, i.datedecision.strftime('%d/%m/%Y'), styleDonneeSansFond)
                    feuille.write(xl_curr_row, 28, i.debutaffichage.strftime('%d/%m/%Y'), styleDonneeSansFond)
                    feuille.write(xl_curr_row, 29, i.finaffichage.strftime('%d/%m/%Y'), styleDonneeSansFond)
                    if i.dateReconnaissance is not None:
                        feuille.write(xl_curr_row, 30, i.dateReconnaissance.strftime('%d/%m/%Y'), styleDonneeSansFond)
                    else:
                        feuille.write(xl_curr_row, 30, '', styleDonneeSansFond)
                    feuille.write(xl_curr_row, 31, self.solotenaKaominina.split(':')[0], styleDonneeSansFond)
                    feuille.write(xl_curr_row, 32, self.solotenaKaominina.split(':')[1], styleDonneeSansFond)
                    feuille.write(xl_curr_row, 33, self.solotenaKaomininaMpisolo.split(':')[0], styleDonneeSansFond)
                    feuille.write(xl_curr_row, 34, self.solotenaKaomininaMpisolo.split(':')[1], styleDonneeSansFond)
                    feuille.write(xl_curr_row, 35, self.solotenaFkt.split(':')[0], styleDonneeSansFond)
                    feuille.write(xl_curr_row, 36, self.solotenaFkt.split(':')[1], styleDonneeSansFond)
                    feuille.write(xl_curr_row, 37, self.solotenaFktMpisolo.split(':')[0], styleDonneeSansFond)
                    feuille.write(xl_curr_row, 38, self.solotenaFktMpisolo.split(':')[1], styleDonneeSansFond)
                    feuille.write(xl_curr_row, 39, self.rad1.split(':')[0], styleDonneeSansFond)
                    feuille.write(xl_curr_row, 40, self.rad1.split(':')[1], styleDonneeSansFond)
                    feuille.write(xl_curr_row, 41, self.rad1Mpisolo.split(':')[0], styleDonneeSansFond)
                    feuille.write(xl_curr_row, 42, self.rad1Mpisolo.split(':')[1], styleDonneeSansFond)
                    feuille.write(xl_curr_row, 43, self.rad2.split(':')[0], styleDonneeSansFond)
                    feuille.write(xl_curr_row, 44, self.rad2.split(':')[1], styleDonneeSansFond)
                    feuille.write(xl_curr_row, 45, self.rad2Mpisolo.split(':')[0], styleDonneeSansFond)
                    feuille.write(xl_curr_row, 46, self.rad2Mpisolo.split(':')[1], styleDonneeSansFond)
                    feuille.write(xl_curr_row, 47, self.rad3.split(':')[0], styleDonneeSansFond)
                    feuille.write(xl_curr_row, 48, self.rad3.split(':')[1], styleDonneeSansFond)
                    feuille.write(xl_curr_row, 49, self.rad3Mpisolo.split(':')[0], styleDonneeSansFond)
                    feuille.write(xl_curr_row, 50, self.rad3Mpisolo.split(':')[1], styleDonneeSansFond)
                    feuille.write(xl_curr_row, 51, self.mpiasaBif.split(':')[0], styleDonneeSansFond)
                    feuille.write(xl_curr_row, 52, self.mpiasaBif.split(':')[1], styleDonneeSansFond)
                    feuille.write(xl_curr_row, 53, self.mpiasaBifMpisolo.split(':')[0], styleDonneeSansFond)
                    feuille.write(xl_curr_row, 54, self.mpiasaBifMpisolo.split(':')[1], styleDonneeSansFond)

                    xl_curr_row = xl_curr_row + 1
                    k = k + 1

        dst = os.path.join(tempfile.gettempdir(),
                           str(randint(10000, 99999)) + "-" + "Export_pour_RL_" + self.numDecision.replace('/',
                                                                                                                   '_') + ".xls")
        # dst = os.path.dirname(__file__) + "/" + str(randint(10000, 99999)) + "-" + "Registre de demande.xls"
        self.book_to_export.save(dst)
        os.startfile(dst)

    def exportPVRL(self):
        print "APPEL EXPORT PVRL ***********************************************************************"
        self.merger = PdfFileMerger()
        rows = []
        commune = str(Utils.emptyifnull(self.commune, "nomcommune"))
        print "ETO E"
        for idx, i in enumerate(self.demandes):
            c = self.ui.tableWidget.item(idx, 0).checkState()

            if c:
                #VOISINS
                nord, sign_nord = '', ''
                sud, sign_sud = '', ''
                est, sign_est = '', ''
                ouest, sign_ouest = '', ''
                if len(i.limites) > 0:
                    for lim in i.limites:
                        for key, val in lim.items():
                            if key == '4':
                                path = str(self.readByte_sign_voisins(i.idparcelle, 4, str(val.split(':')[0]))).replace(
                                    '\\', '/')
                                tab = path.split('/')
                                sign_nord = str(tab[len(tab) - 1])
                                print "SIGNATURE NORD " + sign_nord
                                nord = val
                            if key == '5':
                                path = str(self.readByte_sign_voisins(i.idparcelle, 5, str(val.split(':')[0]))).replace(
                                    '\\', '/')
                                tab = path.split('/')
                                sign_sud = str(tab[len(tab) - 1])
                                sud = val
                            if key == '6':
                                path = str(self.readByte_sign_voisins(i.idparcelle, 6, str(val.split(':')[0]))).replace(
                                    '\\', '/')
                                tab = path.split('/')
                                sign_est = str(tab[len(tab) - 1])
                                est = val
                            if key == '11':
                                path = str(self.readByte_sign_voisins(i.idparcelle, 11, str(val.split(':')[0]))).replace(
                                    '\\', '/')
                                tab = path.split('/')
                                sign_ouest = str(tab[len(tab) - 1])
                                ouest = val

                # MEMBRE CRL
                if len(i.membre_crl) > 0:
                    for dico in i.membre_crl:
                        for key, val in dico.items():
                            print key
                            if key == '2_t':
                                self.solotenaKaominina = val
                            if key == '2_f':
                                self.solotenaKaominina = val
                            if key == '3_t':
                                self.solotenaFkt = val
                            if key == '3_f':
                                self.solotenaFkt = val
                            if key == '4_t':
                                self.rad1 = val
                            if key == '4_f':
                                self.rad1 = val
                            if key == '5_t':
                                self.rad2 = val
                            if key == '5_f':
                                self.rad2 = val
                            if key == '6_t':
                                self.rad3 = val
                            if key == '6_f':
                                self.rad3 = val
                            if key == '7_t':
                                self.mpiasaBif = val
                            if key == '7_f':
                                self.mpiasaBif = val

                # signature demandeur
                print "avant siganture"
                try:
                    path = str(self.readByteA(int(i.idDemandeurPrincipale))[0][2]).replace('\\', '/')
                    tab = path.split('/')
                    signature_demandeur = tab[len(tab) - 1]
                except Exception as err:
                    print err
                print signature_demandeur
                print "pres signature"
                # signature membre RL
                sign_commune, sign_fkt, sign_rad1, sign_rad2, sign_rad3, sign_bif = "", "", "", "", "", ""
                president, sign_president = "", ""
                if len(i.ids_crl) > 0:
                    for dico in i.ids_crl:
                        for key, val in dico.items():
                            # print key
                            if key == '2':
                                path = str(self.readByteA(int(val))[0][2]).replace('\\', '/')
                                tab = path.split('/')
                                sign_commune = tab[len(tab) - 1]

                                if int(val) == i.idPresidentCrl:
                                    president = self.solotenaKaominina
                                    sign_president = sign_commune
                            if key == '3':
                                path = str(self.readByteA(int(val))[0][2]).replace('\\', '/')
                                tab = path.split('/')
                                sign_fkt = tab[len(tab) - 1]

                                if int(val) == i.idPresidentCrl:
                                    president = self.solotenaFkt
                                    sign_president = sign_fkt
                            if key == '4':
                                path = str(self.readByteA(int(val))[0][2]).replace('\\', '/')
                                tab = path.split('/')
                                sign_rad1 = tab[len(tab) - 1]

                                if int(val) == i.idPresidentCrl:
                                    president = self.rad1
                                    sign_president = sign_rad1
                            if key == '5':
                                path = str(self.readByteA(int(val))[0][2]).replace('\\', '/')
                                tab = path.split('/')
                                sign_rad2 = tab[len(tab) - 1]

                                if int(val) == i.idPresidentCrl:
                                    president = self.rad2
                                    sign_president = sign_rad2
                            if key == '6':
                                path = str(self.readByteA(int(val))[0][2]).replace('\\', '/')
                                tab = path.split('/')
                                sign_rad3 = tab[len(tab) - 1]

                                if int(val) == i.idPresidentCrl:
                                    president = self.rad3
                                    sign_president = sign_rad3
                            if key == '7':
                                path = str(self.readByteA(int(val))[0][2]).replace('\\', '/')
                                tab = path.split('/')
                                sign_bif = tab[len(tab) - 1]

                                if int(val) == i.idPresidentCrl:
                                    president = self.mpiasaBif
                                    sign_president = sign_bif

                print self.solotenaKaominina
                # n = str(i.numdemandepaps) if (i.numdemandepaps is not None and i.numdemandepaps != '') else str(i.numdemande)
                n = str(i.numdemande)

                d = datetime.date.today()
                dic = {
                    "$kaominina": commune,
                    "$distrika": str(Utils.emptyifnull(self.district, "nomdistrict")),
                    "$faritra": str(Utils.emptyifnull(self.region, "nomregion")),
                    "$nudemande": n,
                    "$fokontany": str(i.nomfokontany),
                    "$vohitra": str(i.nomhameau),
                    "$lieudit": str(i.lieudit),
                    "$consistance": str(i.consistance),
                    "$numDecision": str(i.numdecision).upper(),
                    "$daatedecision": i.datedecision.strftime("%d/%m/%Y"),
                    "$daatereconnaissance": i.dateReconnaissance.strftime("%d/%m/%Y"),
                    "$debutAffichage": i.debutaffichage.strftime("%d/%m/%Y"),
                    "$finAffichage": i.finaffichage.strftime("%d/%m/%Y"),
                    "$nbreJour": str(self.nbrJour),
                    "$codeparcelle": str(i.codeParcelle),
                    "$kom": commune[:3].upper(),
                    "$plchePlof": str(i.codePlanche),
                    "$annee": str(datetime.date.today().year),
                    "$date": d.strftime("%d/%m/%Y"),
                    "$solotenaKaominina": str(self.solotenaKaominina.split(':')[0]),
                    #"$solotenaMpisoloKaominina": str(self.solotenaFktMpisolo.split(':')[0]),
                    "$solotenaFkt": str(self.solotenaFkt.split(':')[0]),
                    #"$solotenaMpisoloFkt": str(self.solotenaFktMpisolo.split(':')[0]),
                    "$rad1": str(self.rad1.split(':')[0]),
                    "$rad2": str(self.rad2.split(':')[0]),
                    "$rad3": str(self.rad3.split(':')[0]),
                    "$lpresident": str(president.split(':')[0]),
                    #"$radMpisolo1": str(self.rad1Mpisolo.split(':')[0]),
                    #"$radMpisolo2": str(self.rad2Mpisolo.split(':')[0]),
                    #"$radMpisolo3": str(self.rad3Mpisolo.split(':')[0]),
                    "$bif": str(self.mpiasaBif.split(':')[0]),
                    #"$soloBif": str(self.mpiasaBifMpisolo.split(':')[0]),
                    "$nmdemandeur": str(i.nom),
                    "$tanimboly": "X" if i.categorie == "TANIMBOLY" else "",
                    "$tanimbary": "X" if i.categorie == "TANIMBARY" else "",
                    "$taninkazo": "X" if i.categorie == "TANIN-KAZO" else "",
                    "$toeranafiompiana": "X" if i.categorie == "TOERANA FIOMPIANA" else "",
                    "$hafa": "X" if i.categorie == "HAFA" else "",
                    "$occupation": str(i.duree_occupation),
                    "$origine": str(i.origine),
                    "$aviscrl":str(i.avis_crl),
                    "$voisinNord": str(nord),
                    "$voisinSud": str(sud),
                    "$voisinEst": str(est),
                    "$voisinOuest": str(ouest),
                    "$charge": i.charge,
                    "$soniaDemandeur": "'images/" + signature_demandeur + "'" if signature_demandeur!='' else "'images/blank.jpg'",
                    "$soniaKaominina": "'images/" + sign_commune + "'" if sign_commune!='' else "'images/blank.jpg'",
                    "$soniaFkt": "'images/" + sign_fkt + "'" if sign_fkt!='' else "'images/blank.jpg'",
                    "$soniarad1": "'images/" + sign_rad1 + "'" if sign_rad1!='' else "'images/blank.jpg'",
                    "$soniarad2": "'images/" + sign_rad2 + "'" if sign_rad2!='' else "'images/blank.jpg'",
                    "$soniarad3": "'images/" + sign_rad3 + "'" if sign_rad3!='' else "'images/blank.jpg'",
                    "$soniabif": "'images/" + sign_bif + "'" if sign_bif!='' else "'images/blank.jpg'",
                    "$soniapresident": "'images/" + sign_president + "'" if sign_president != '' else "'images/blank.jpg'",
                    "$sonianord": "'images/" + sign_nord + "'" if sign_nord!='' else "'images/blank.jpg'",
                    "$soniasud": "'images/" + sign_sud + "'" if sign_sud!='' else "'images/blank.jpg'",
                    "$soniaest": "'images/" + sign_est + "'" if sign_est!='' else "'images/blank.jpg'",
                    "$soniaouest": "'images/" + sign_ouest + "'" if sign_ouest!='' else "'images/blank.jpg'",
                    "$rows": rows,
                }
                rows.append({
                    "id": i.iddemande,
                    "num": n,
                    "date": i.datedemande.strftime("%d/%m/%Y"),
                    "nom": str(i.nom).decode('utf-8'),
                    "adiresy": str(i.adresse).decode('utf-8'),
                    # "limite": i.limite,
                    "voisinNord": nord,
                    "voisinSud": sud,
                    "voisinEst": est,
                    "voisinOuest": ouest,
                    "codeParcelle": i.codeParcelle,
                    "planchePlof": i.codePlanche,
                    "surface": i.surface,
                    "hameau": str(i.codehameau) + " - " + str(i.nomhameau),
                    "adresse": str(i.adressepersonne),
                    "voisin_0_adresse": i.voisins[0]["adresse"] if len(i.voisins) > 0 else "-",
                    "voisin_0_nom": i.voisins[0]["nom"] if len(i.voisins) > 0 else "-",
                    "voisin_0_prenom": i.voisins[0]["prenom"] if len(i.voisins) > 1 else "-",
                    "voisin_1_adresse": i.voisins[1]["adresse"] if len(i.voisins) > 0 else "-",
                    "voisin_1_nom": i.voisins[1]["nom"] if len(i.voisins) > 0 else "-",
                    "voisin_1_prenom": i.voisins[1]["prenom"] if len(i.voisins) > 1 else "-",
                })
                converter = Html2Pdf()
                converter.setOrientation(orientation=self.orientation)
                src = os.path.dirname(__file__) + "/" + self.template
                print 'src loaded'
                dst = os.path.join(tempfile.gettempdir(), str(randint(10000, 99999)) + "-" + self.template + ".pdf")
                QApplication.setOverrideCursor(Qt.Qt.WaitCursor)
                try:
                    converter.generate(html=src, pdf=dst, dictionnary=dic)
                except Exception as err:
                    print "erreur creation pdf"
                    print err
                #webbrowser.open(dst)
                print "After generate"
                # webbrowser.open(dst)
                self.merger.append(dst)
                QApplication.restoreOverrideCursor()

        dstFinal = os.path.join(tempfile.gettempdir(), str(randint(10000, 99999)) + "-" + "PVRL.pdf")
        self.merger.write(dstFinal)
        print 'after merger write'
        webbrowser.open(dstFinal)
        # PDF liste annexe

    def readByteA(self, idpersonne):
        basepath = os.path.dirname(os.path.realpath(__file__))
        paths_to_return = []
        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cur.execute("SELECT * FROM blob_personne WHERE idpersonne = %s ",
                        (idpersonne,))
            res = cur.fetchall()
            print res
        except Exception as err:
            print (err)
            self.connection.rollback()

        path1 = None
        path2 = None
        path3 = None
        path4 = None
        path5 = None
        for colon in res:
            # name = colon[1]
            #Contenus
            file_cin_recto = colon['cin_recto']
            file_cin_verso = colon['cin_verso']
            file_signature = colon['signature']
            file_empreinte_d = colon['empreinte_d']
            file_empreinte_g = colon['empreinte_g']
            #print file_empreinte_d
            name_cin_recto = colon['cin_recto_name']
            name_cin_verso = colon['cin_verso_name']
            name_signature = colon['signature_name']
            name_empreinte_g = colon['empreinte_g_name']
            name_empreinte_d = colon['empreinte_d_name']
            #Extensions
            ext_cin_recto = colon['cin_recto_type']
            ext_cin_verso = colon['cin_verso_type']
            ext_signature = colon['signature_type']
            ext_empreinte_g = colon['empreinte_g_type']
            ext_empreinte_d = colon['empreinte_d_type']

            basepath = basepath + "/images/"
            print basepath

            print("Stocker le fichier sur le disque \n")
            if file_cin_recto is not None:
                path1 = os.path.join(basepath, name_cin_recto + "." + ext_cin_recto)
            if file_cin_verso is not None:
                path2 = os.path.join(basepath, name_cin_verso + "." + ext_cin_verso)
            if file_signature is not None:
                path3 = os.path.join(basepath, name_signature + "." + ext_signature)
            if file_empreinte_d is not None:
                path4 = os.path.join(basepath, name_empreinte_d + "." + ext_empreinte_d)
            if file_empreinte_g is not None:
                path5 = os.path.join(basepath, name_empreinte_g + "." + ext_empreinte_g)
            print ("after path def demandeurs")

        # Convertir les donnees binaires au format
        # approprie et les ecrire sur le disque dur
        if path1 is not None:
            try:
                with open(path1, 'wb') as myfile:
                    myfile.write(file_cin_recto)
                #print("Le fichier stockees dans: ", path1, "\n")
                #self.showInScene(path1,self.ui.graphicsViewCinRecto)
                self.paths.append(path1)
            except Exception as err:
                print (err)
        if path2 is not None:
            try:
                with open(path2, 'wb') as myfile:
                    myfile.write(file_cin_verso)
                #print("Le fichier stockees dans: ", path2, "\n")
                #self.showInScene(path2, self.ui.graphicsViewCinVerso)
                self.paths.append(path2)
            except Exception as err:
                print (err)
        if path3 is not None:
            try:
                with open(path3, 'wb') as myfile:
                    myfile.write(file_signature)
                #print("Le fichier stockees dans: ", path3, "\n")
                #self.showInScene(path3, self.ui.graphicsViewSignature, True)
                self.paths.append(path3)
            except Exception as err:
                print (err)
        if path4 is not None :
            with open(path4, 'wb') as myfile:
                myfile.write(file_empreinte_d)
            #print("Le fichier stockees dans: ", path4, "\n")
            #self.showInScene(path4, self.ui.graphicsViewEmpreinteD, True)
            self.paths.append(path4)
        if path5 is not None :
            try:
                with open(path5, 'wb') as myfile:
                    myfile.write(file_empreinte_g)
                #print("Le fichier stockees dans: ", path5, "\n")
                #self.showInScene(path5, self.ui.graphicsViewEmpreinteG, True)
                self.paths.append(path5)
            except Exception as err:
                print (err)
        print "AFTER OPENNING FILES"

        # fermeture de la connexion à la base de données
        cur.close()
        paths_to_return.append((path1, path2, path3, path4, path5))
        return paths_to_return

    def readByte_sign_voisins(self, idparcelle, idpoint, voisin):
        basepath = os.path.dirname(os.path.realpath(__file__))
        paths_to_return = []
        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cur.execute("SELECT * FROM blob_voisin WHERE idparcelle = %s AND idpoint = %s AND UPPER(TRIM(voisin)) =  %s",
                        (idparcelle,idpoint, voisin))
            res = cur.fetchall()
            print res
        except Exception as err:
            print (err)
            self.connection.rollback()

        path3 = None

        for colon in res:
            # name = colon[1]
            #Contenus

            file_signature = colon['signature_fic']


            name_signature = colon['signature_name']

            ext_signature = colon['signature_ext']

            basepath = basepath + "/images/"
            print basepath

            print("Stocker le fichier sur le disque \n")

            if file_signature is not None:
                path3 = os.path.join(basepath, name_signature + "." + ext_signature)

            print ("after path def voisins")

        # Convertir les donnees binaires au format
        # approprie et les ecrire sur le disque dur

        if path3 is not None:
            try:
                with open(path3, 'wb') as myfile:
                    myfile.write(file_signature)
                #print("Le fichier stockees dans: ", path3, "\n")
                #self.showInScene(path3, self.ui.graphicsViewSignature, True)
                self.paths.append(path3)
            except Exception as err:
                print (err)
                path3 = ""

        # fermeture de la connexion à la base de données
        cur.close()
        return path3

    def __del__(self):
        for path in self.paths:
            try:
                os.remove(path)
            except Exception as err:
                print err