# -*- coding: utf-8 -*-
import os, os.path, sys, psycopg2
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *
import datetime, time
from psycopg2.extensions import *

from .RecalculImpot import Ui_Dialog
from AreaConvert import AreaConvert


class RecalculImpotRun(QDialog):
    def __init__(self, connection):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.progressBar.hide()
        self.ui.progressBar.setValue(0)
        self.connection = connection
        self.initDB()
        self.idsContribuables = None
        self.idsParcelles = None
        self.initActions()
        self.minIft = 0.0
        self.minIfpb = 0.0
        self.getMinImpot()
        #self.ui.comboBoxForfait.removeItem(2)
        self.ui.label.hide()
        self.ui.comboBoxForfait.hide()
        from .resCalculImpotRun import resCalculImpotRun
        self.calc = resCalculImpotRun(self.connection)
        #print datetime.datetime.now().strftime('%Y')
        self.annee = int(datetime.datetime.now().strftime('%Y'))

    def initActions(self):
        #Bouton charger
        self.ui.pushButton.clicked.connect(self.getNombreContribuableEtParcelles)
        #Bouton calculer
        self.ui.pushButton_2.clicked.connect(self.calculImpot)

    def getNombreContribuableEtParcelles(self):
        print "eto ilay izy no atao"
        try:
            self.cur.execute("SELECT DISTINCT p.idpersonne, p.nompersonne, p.prenompersonne FROM personne p INNER JOIN contribuables_parcelle cp ON p.idpersonne = cp.idpersonne WHERE cp.contribuable = %s", (True,))
            self.idsContribuables = self.cur.fetchall()
            print self.idsContribuables
        except StandardError as e:
            print e
        try:
            self.cur.execute("SELECT DISTINCT gid FROM parcelle_d pd INNER JOIN contribuables_parcelle cp ON pd.gid = cp.idparcelle")
            self.idsParcelles = self.cur.fetchall()
            print self.idsParcelles
        except StandardError as e:
            print e
        nbrContribuable = len(self.idsContribuables)
        nbrParcelle = len(self.idsParcelles)
        self.ui.lineEdit_13.setText(str(nbrContribuable))
        self.ui.lineEdit_8.setText(str(nbrParcelle))

    def calculImpot(self):
        donneesImpot = []
        impotParContribuable = []
        donneesImpot[:] = []
        self.calc.ui.tableWidget.setRowCount(0)
        self.calc.resetAllImpot()

        self.ui.progressBar.show()
        self.ui.progressBar.setValue(0)
        print "Eto no manao calcul Impot"
        i = 1
        #k = 0
        for idcontribuable in self.idsContribuables:
            valeurImpot = 0
            valImpotBat = 0
            valImpotParcelle = 0
            #impotBatiment[:] = []
            #Calcul de l'impot sur parcelle
            #**************************RECUPERATION DES DONNEES DE LA PARCELLE*******************#
            dataImpot = None
            cur = self.connection.cursor()
            try:
                cur.execute("SELECT DISTINCT pd.gid, ST_Area(pd.geom), pd.idcategorie, pd.idclasse, pd.fi_forfait,cp.idpersonne, c.typeimposition, c.v_surface,c.u_surface, c.v_venale, c.u_venale, c.taux "
                        "FROM parcelle_d pd "
                        "INNER JOIN categorie c ON c.idcategorie = pd.idcategorie, "
                        "contribuables_parcelle cp "
                        "WHERE cp.idparcelle = pd.gid AND cp.idpersonne = %s AND cp.contribuable = %s", (idcontribuable[0],True))
                dataImpot = cur.fetchall()
            except Exception as err:
                print "Erreur recup impot"
                print err

            if dataImpot is not None:
                ######## CALCUL DE L'IMPOT DE CHAQUE CONTRIBUABLE#######
                j = 0
                for values in dataImpot:
                    impotParContribuable[:] = []
                    impotParContribuable.append(idcontribuable[0])
                    nomEtPrenom = idcontribuable[1] + " " + idcontribuable[2]
                    impotParContribuable.append(nomEtPrenom)

                    impotParcelle = 0.0
                    impotBatiment = 0.0

                    #***************CALCUL IMPOT PARCELLE******************#
                    #Forfait par surface
                    if str(values[4]).strip() == "surface":
                        if values[7] is not None and values[8] is not None:
                            #surface fois impot par surface
                            if str(values[8]).strip() == "Ar/m2":
                                impotParcelle =  (float(values[1]) * float(values[7]))

                            if str(values[8]).strip() == "Ar/a":
                                impotParcelle =  (float(values[1]) * float(values[7])/float(100))

                            if str(values[8]).strip() == "Ar/ha":
                                impotParcelle =  (float(values[1]) * float(values[7])/float(10000))

                    #Forfait par classe
                    if str(values[4]).strip() == "classe":
                        impotParcelle =  self.getValClasse(idcategorie=values[2], idclasse=values[3])

                    #Forfait par valeur venale
                    if str(values[4]).strip() == "valeur_venale":
                        if values[9] is not None and values[10] is not None:
                            #surface * valeur venale par surface * taux
                            if str(values[10]).strip() == "Ar/m2":
                                impotParcelle =  ((float(values[1]) * float(values[9])) * float(values[11])/100)

                            if str(values[10]).strip() == "Ar/a":
                                impotParcelle =  ((float(values[1]) * float(values[9])/float(100)) * float(values[11])/100)

                            if str(values[8]).strip() == "Ar/ha":
                                impotParcelle =  ((float(values[1]) * float(values[9])/float(10000)) * float(values[11])/100)


                    if impotParcelle < self.minIft:
                        impotParcelle = self.minIft

                    self.writeImpotParcelle(float(round(impotParcelle)), self.annee, values[0])
                    valImpotParcelle = valImpotParcelle + float(round(impotParcelle))
                    #***************FIN CALCUL IMPOT PARCELLE*****************#

                    #*********CALCUL IMPOT BATIMENT***********************************#
                    curs = self.connection.cursor()
                    try:
                        curs.execute("SELECT b.codebatiment, b.surfacebatiment, b.nbpiecebatiment, b.locationbatiment, b.idcategorie, b.fi_forfait, b.idclasse, cat.v_surface, cat.u_surface, cat.v_venale, "
                                     "cat.u_venale, cat.taux, b.idclasse "
                                                     "FROM batiment b, parcelle_d pd, categorie cat "
                                                     "WHERE b.idparcelle = pd.gid AND pd.gid = %s "
                                                     "AND b.idcategorie = cat.idcategorie", (values[0],))
                        batiments = curs.fetchall()
                    except Exception as err:
                        print "erreur recup batiment"
                        print err

                    if len(batiments) > 0:
                        for bat in batiments:
                            impotBatiment = 0.0
                            #Par surface
                            if str(bat[5]).strip() == "surface":
                                print "*************bat par surface***************"
                                impotBatiment =  (float(bat[1]) * float(bat[7]))

                            #Par classe
                            if str(bat[5]).strip() == "classe":
                                impotBatiment = self.getValClasse(idcategorie=bat[4], idclasse=bat[6])
                            #Par valeur locative
                            if str(bat[5]).strip() == "valeur_locative":
                                if str(bat[10]).strip() == "Ar/m2":
                                    impotBatiment = ((float(bat[1]) * float(bat[9])) * float(bat[11])/100)
                                if str(bat[10]).strip() == u"Ar/Pièces":
                                    impotBatiment =  ((float(bat[2]) * float(bat[9])) * float(bat[11])/100)

                            #Verification impot batiment
                            if impotBatiment < self.minIfpb:
                                impotBatiment = self.minIfpb

                            self.writeImpotBatiment(float(round(impotBatiment)), self.annee, bat[0])

                            valImpotBat = valImpotBat + float(round(impotBatiment))
                    valeurImpot = valImpotBat + valImpotParcelle

                    j = j + 1
                    print "tour " + str(j)
            impotParContribuable.append(valeurImpot)
            impotParContribuable.append(valImpotParcelle)
            impotParContribuable.append(valImpotBat)
            self.ui.textEdit.append(nomEtPrenom + "\n")
            #self.writeHetrantany(impotParContribuable)
            self.calc.setNewValImpot(impotParContribuable)
            self.writeImpotContribuable(valImpotBat, valImpotParcelle, self.annee, idcontribuable[0])
            valeurProgress = (float(i) / len(self.idsContribuables)) * 100

            print "impot par contribuable"
            print impotParContribuable

            print "Donnees impot"
            print donneesImpot
            print i
            print len(self.idsContribuables)
            print valeurProgress
            self.ui.progressBar.setValue(valeurProgress)
            i = i + 1

        self.calc.totalImpot()
        self.calc.exec_()

    def initDB(self):
        self.cur = self.connection.cursor()

    def __del__(self):
        self.cur.close()

    def writeHetrantany(self, tabImpot):
        print "ATO AM WRITE HETRATANY"
        try:
            print tabImpot
            self.cur.execute("UPDATE contribuable SET hetratany = %s, hetratrano = %s, modecalcul = %s WHERE idcontribuable = %s", (tabImpot[3],tabImpot[4],self.ui.comboBoxForfait.currentIndex() + 1, tabImpot[0]))
            self.connection.commit()
        except StandardError as e:
            print e
            self.connection.rollback()

    def RecheckDiffToPaiement(self, hetratotal, idpersonne, annee):
        payee = 0.0
        try:
            cur = self.connection.cursor()
            cur.execute("SELECT montantpaye::numeric FROM impot_contribuable WHERE idpersonne = %s AND annee = %s", (idpersonne, annee))
            res = cur.fetchone()
            if res is not None:
                payee = float(res[0])
        except Exception as err:
            print err
            self.connection.rollback()

        return hetratotal - payee


    def writeImpotContribuable(self, hetratrano, hetratany, annee, idpersonne):

        hetratotal = hetratany + hetratrano
        etatpaiement = 0
        if self.RecheckDiffToPaiement(hetratotal,idpersonne, annee) > 0:
            if hetratotal == self.RecheckDiffToPaiement(hetratotal,idpersonne, annee):
                etatpaiement = 0
            else:
                etatpaiement = 1
        if self.RecheckDiffToPaiement(hetratotal,idpersonne, annee) == 0:
            etatpaiement = 2

        try:
            self.cur.execute('INSERT INTO impot_contribuable (hetratrano,hetratany, annee, etatpaiement, idpersonne) VALUES(%s, %s, %s, %s, %s)',
                             (hetratrano, hetratany, annee, etatpaiement, idpersonne))
            self.connection.commit()
        except psycopg2.Error as e:
            #print e.pgcode
            if e.pgcode == "23505":
                self.connection.rollback()
                try:
                    self.cur.execute('UPDATE impot_contribuable SET hetratrano = %s, hetratany = %s, etatpaiement = %s WHERE idpersonne = %s AND annee = %s', (hetratrano,hetratany,etatpaiement, idpersonne, annee))
                    self.connection.commit()
                except StandardError as e:
                    print(e)
                    self.connection.rollback()
            else:
                print (e)
                self.connection.rollback()
            #self.connection.rollback()

    def writeImpotParcelle(self, valimpot, annee, idparcelle):
        try:
            self.cur.execute('INSERT INTO impot_parcelle (hetratany, annee, idparcelle) VALUES(%s, %s, %s)',
                             (valimpot, annee, idparcelle))
            self.connection.commit()
        except psycopg2.Error as e:
            if e.pgcode == "23505":
                self.connection.rollback()
                #print "IN ERROR 2305"
                try:
                    self.cur.execute('UPDATE impot_parcelle SET hetratany = %s WHERE annee = %s AND idparcelle = %s', (valimpot,annee, idparcelle))
                    self.connection.commit()
                except StandardError as e:
                    print(e)
                    self.connection.rollback()
            else:
                print(e)
                self.connection.rollback()
            #self.connection.rollback()


    def writeImpotBatiment(self, valimpot, annee, codebatiment):
        print "******************in write impot batiment***************"
        try:
            self.cur.execute('INSERT INTO impot_batiment (hetratrano, annee, codebatiment) VALUES(%s, %s, %s)',
                             (valimpot, annee, codebatiment))
            self.connection.commit()
        except psycopg2.Error as e:
            #print e.pgcode
            if e.pgcode == "23505":
                self.connection.rollback()
                print "Update in"
                try:
                    self.cur.execute('UPDATE impot_batiment SET hetratrano = %s WHERE annee = %s AND codebatiment = %s', (valimpot,annee, codebatiment))
                    self.connection.commit()
                except StandardError as e:
                    print(e)
                    self.connection.rollback()
            else:
                print(e)
                self.connection.rollback()
            #self.connection.rollback()

    def getMinImpot(self):
        cur = self.connection.cursor()
        currentDateTime = datetime.datetime.now()
        date = currentDateTime.date()
        annee = str(date.strftime("%Y"))
        try:
            cur.execute("SELECT * from impot_minimum WHERE annee = %s", (annee,))
            res = cur.fetchall()
            if res is not None:
                for re in res:
                    if str(re[1]).strip() == "ift":
                        self.minIft = float(re[2])
                    if str(re[1]).strip() == "ifpb":
                        self.minIfpb = float(re[2])
        except Exception as err:
            print "erreur recup min impot"
            print err

    def getValClasse(self, idcategorie = None, idclasse = None):
        val = 0.0
        if idcategorie is not None and idclasse is not None:
            cur = self.connection.cursor()
            try:
                cur.execute("SELECT valeurariary FROM public.classecategorieforfaitaire WHERE idclasse = %s AND idcategorie =  %s", (idclasse, idcategorie))
                res = cur.fetchone()
                val = float(res[0])
            except Exception as err:
                print "erreur get val classe"
                print err
        return val



