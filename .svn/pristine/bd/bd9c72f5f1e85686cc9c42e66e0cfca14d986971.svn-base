# coding: utf8
from PyQt4.QtCore import QThread, SIGNAL
from osgeo import gdal, ogr
import ogrinfo
import sys
import os
import os.path
import globalvars
from datetime import datetime
import psycopg2
import time
import csv
import io
import tempfile
from random import randint
from PyQt4.Qt import QApplication
from Etats.Html2Pdf import Html2Pdf
import webbrowser


class PrintRddThread(QThread):
    def __init__(self, idsDemandes, merger, connection):
        QThread.__init__(self)
        self.idsDmdtoPrint, self.merger, self.connection = idsDemandes, merger, connection
        #self.ogroutput, self.current_step = "ogr.log", -1

    def __del__(self):
        self.wait()

    def run(self):
        nbr_dmd_par_page = 3
        nbr_page = 0
        if (len(self.idsDmdtoPrint) % nbr_dmd_par_page) == 0:
            nbr_page = (len(self.idsDmdtoPrint) / nbr_dmd_par_page)
        else:
            nbr_page = (len(self.idsDmdtoPrint) / nbr_dmd_par_page) + 1
        num_page = 1
        print "Nombre page rdd"
        print (nbr_page)
        print "Fin nombre page rdd"
        infosCF = []
        dic = None
        from Projet.journalRunn import journal
        journal = journal(self.connection)
        journal.inserToJournal(globalvars.id_user, 0, u"Demande",
                               u"Impression de Registre de Demande")

        compteur_demande = 0
        compteur_impression = 0
        demandes_to_print = []

        for idDmdtoPrint in self.idsDmdtoPrint:
            compteur_demande = compteur_demande + 1
            proprio = []
            infoProprio = {}
            aire = None
            emplacementParcelle = {}
            limitesparcelle = {}
            limitesparcelle['nord'] = ""
            limitesparcelle['sud'] = ""
            limitesparcelle['est'] = ""
            limitesparcelle['ouest'] = ""
            emplacementParcelle['hameau'] = ""
            emplacementParcelle['fokontany'] = ""
            emplacementParcelle['commune'] = ""
            emplacementParcelle['district'] = ""
            limitesparcelle['nord'] = ""
            limitesparcelle['sud'] = ""
            limitesparcelle['est'] = ""
            limitesparcelle['ouest'] = ""
            charge = ""

            try:
                self.cur.execute(
                    "SELECT dmd.numdemande, dmd.datedemande, pd.gid, pd.idhameau, pd.id_commune, dmd.datedecision, dmd.consistance, dmd.categorie, dmd.numdecision, dmd.datereconnaissance FROM demande dmd, parcelle_d pd WHERE dmd.gid = pd.gid AND dmd.iddemande = %s ORDER BY numdemande ASC",
                    (idDmdtoPrint,))
                infosCF = self.cur.fetchone()
                print "Information CF " + str(infosCF)
                if infosCF is not None:
                    idparcelle = int(infosCF[2])
                    ### Traitement des proprietaires du certificat ###
                    try:
                        self.cur.execute("SELECT DISTINCT nompersonne, prenompersonne,"
                                         " datenaissancepersonne, lieunaissancepersonne, "
                                         " sexepersonne, adressepersonne, numcipersonne, "
                                         " datecipersonne, lieucipersonne, numactenaissancepersonne, "
                                         " dateactenaissancepersonne, lieuactenaissancepersonne, "
                                         " situationmatrimoniale, nompere, nommere, nevers "
                                         "FROM personne ppq, avoir_demande ppd "
                                         "WHERE ppq.idpersonne = ppd.idpersonne AND ppd.idparcelle = %s", (idparcelle,))
                        dataProprio = self.cur.fetchall()
                        print "Proprietaires  = " + str(dataProprio)
                        if dataProprio is not None:
                            i = 1
                            # infoProprio = {}
                            for data in dataProprio:
                                infoProprio['num'] = i
                                print 'len data proprio'
                                print len(dataProprio)
                                if i == 1:

                                    if data[0] is not None or data[1] is not None:
                                        infoProprio['nom'] = self.takeCareOfAccent(
                                            unicode(data[0]).encode('utf-8').strip())
                                        infoProprio['prenom'] = self.takeCareOfAccent(
                                            unicode(data[1]).encode('utf-8').strip())
                                    else:
                                        infoProprio['nom'] = ""
                                    if data[15] is not None:
                                        infoProprio['datenaissance'] = str(data[15])
                                    elif data[2] is not None:
                                        infoProprio['datenaissance'] = data[2].strftime('%d/%m/%Y')
                                    else:
                                        infoProprio['datenaissance'] = ""
                                    if data[3] is not None:
                                        infoProprio['lieunaissance'] = self.takeCareOfAccent(
                                            unicode(data[3]).encode('utf-8').strip())
                                    else:
                                        infoProprio['lieunaissance'] = ""
                                    if data[5] is not None:
                                        infoProprio['adresse'] = self.takeCareOfAccent(
                                            unicode(data[5]).encode('utf-8').strip())
                                    else:
                                        infoProprio['adresse'] = ""
                                    if data[6] is not None:
                                        infoProprio['numpiece'] = unicode(data[6])[0:3].strip() + "-" + unicode(
                                            data[6])[3:6].strip() + "-" + unicode(data[6])[6:9].strip() + "-" + unicode(
                                            data[6])[9:].strip()
                                        if data[8] is not None:
                                            infoProprio['lieupiece'] = self.takeCareOfAccent(
                                                unicode(data[8]).encode('utf-8').strip())
                                        else:
                                            infoProprio['lieupiece'] = ""
                                        if data[7] is not None:
                                            infoProprio['datepiece'] = data[7].strftime('%d/%m/%Y')
                                        else:
                                            infoProprio['datepiece'] = ''
                                    elif data[9] is not None:
                                        infoProprio['numpiece'] = self.takeCareOfAccent(unicode(data[9]).strip())
                                        if data[11] is not None:
                                            infoProprio['lieupiece'] = self.takeCareOfAccent(
                                                unicode(data[11]).encode('utf-8').strip())
                                        else:
                                            infoProprio['lieupiece'] = ""
                                        if data[10] is not None:
                                            infoProprio['datepiece'] = data[10].strftime('%d/%m/%Y')
                                        else:
                                            infoProprio['datepiece'] = ''
                                    else:
                                        infoProprio['numpiece'] = ""
                                        infoProprio['lieupiece'] = ""
                                    if data[12] is not None:
                                        if data[12] == 1:
                                            infoProprio['matrimoniale'] = "Tsy manambady"
                                        elif data[12] == 2:
                                            infoProprio['matrimoniale'] = "Manambady"
                                        elif data[12] == 3:
                                            infoProprio['matrimoniale'] = "Maty vady"
                                    else:
                                        infoProprio['matrimoniale'] = ""
                                    if data[13] is not None:
                                        infoProprio['nompere'] = self.takeCareOfAccent(
                                            unicode(data[13]).encode('utf-8').strip())
                                        # print "Nom Pere = " + infoProprio['nompere']
                                    else:
                                        infoProprio['nompere'] = ""
                                    if data[14] is not None:
                                        infoProprio['nommere'] = self.takeCareOfAccent(
                                            unicode(data[14]).encode('utf-8').strip())
                                    else:
                                        infoProprio['nommere'] = ""

                                    infoProprio['consorts'] = ""
                                    if len(dataProprio) > 1:
                                        infoProprio['consorts'] = "  et consorts"

                                    proprio.append({
                                        "numero": infoProprio['num'],
                                        "nom": infoProprio['nom'],
                                        "prenom": infoProprio['prenom'],
                                        "numpiece": infoProprio['numpiece'],
                                        "datepiece": infoProprio['datepiece'],
                                        "lieupiece": infoProprio['lieupiece'],
                                        "datenaiss": infoProprio['datenaissance'],
                                        "lieunaiss": infoProprio['lieunaissance'],
                                        "nopere": infoProprio['nompere'],
                                        "no_mere": infoProprio['nommere'],
                                        "matrimoniale": infoProprio['matrimoniale'],
                                        "adresse": infoProprio['adresse'],
                                        "consorts": infoProprio['consorts']
                                    })
                                if i > 1:
                                    break;
                                i = i + 1

                    except StandardError as e:
                        print(e)
                        self.connection.rollback()
                    ###Fin traitement proprietaire###
                    ###Traitement momban'ny tany###

                    if infosCF[3] is not None:  # raha misy hameau
                        try:
                            self.cur.execute(
                                "SELECT h.nomhameau, h.codehameau, f.nomfokontany, f.codefokontany, c.nomcommune, c.codecommune, d.codedistrict FROM hameau h, fokontany f, commune c, district d, parcelle_d pd "
                                "WHERE h.idfokontany = f.idfokontany "
                                "AND f.idcommune = c.idcommune "
                                "AND c.iddistrict = d.iddistrict "
                                "AND pd.idhameau = h.idhameau "
                                "AND pd.gid = %s", (idparcelle,))
                            results = self.cur.fetchone()
                            if results is not None:
                                emplacementParcelle['hameau'] = self.takeCareOfAccent(
                                    unicode(results[0]).encode('utf-8').strip())
                                emplacementParcelle['codehameau'] = self.takeCareOfAccent(
                                    unicode(results[1]).encode('utf-8').strip())
                                emplacementParcelle['codefkt'] = self.takeCareOfAccent(
                                    unicode(results[3]).encode('utf-8').strip())
                                emplacementParcelle['fokontany'] = self.takeCareOfAccent(
                                    unicode(results[2]).encode('utf-8').strip())
                                emplacementParcelle['commune'] = self.takeCareOfAccent(
                                    unicode(results[4]).encode('utf-8').strip())
                                emplacementParcelle['codecommune'] = self.takeCareOfAccent(
                                    unicode(results[5]).encode('utf-8').strip())
                                emplacementParcelle['codedistrict'] = self.takeCareOfAccent(
                                    unicode(results[6]).encode('utf-8').strip())
                        except StandardError as e:
                            print(e)
                            self.connection.rollback()
                    elif infosCF[4] is not None:  # raha tsy misy hameau
                        try:
                            self.cur.execute(
                                "SELECT f.nomfokontany, f.codefokontany, c.nomcommune, c.codecommune, d.codedistrict FROM fokontany f, commune c, district d, certificat cert "
                                "WHERE f.idcommune = c.idcommune "
                                "AND c.iddistrict = d.iddistrict "
                                "AND f.idfokontany = cert.idfokontany "
                                "AND cert.idfokontany = %s", (int(infosCF[4]),))
                            results = self.cur.fetchone()
                            if results is not None:
                                emplacementParcelle['hameau'] = ""
                                emplacementParcelle['fokontany'] = self.takeCareOfAccent(
                                    unicode(results[0]).encode('utf-8').strip())
                                emplacementParcelle['codefkt'] = self.takeCareOfAccent(
                                    unicode(results[1]).encode('utf-8').strip())
                                emplacementParcelle['codecommune'] = self.takeCareOfAccent(
                                    unicode(results[3]).encode('utf-8').strip())
                                emplacementParcelle['codedistrict'] = self.takeCareOfAccent(
                                    unicode(results[4]).encode('utf-8').strip())
                        except StandardError as e:
                            print(e)
                            self.connection.rollback()
                    else:
                        emplacementParcelle['hameau'] = ""
                        emplacementParcelle['fokontany'] = ""
                        emplacementParcelle['commune'] = ""
                        emplacementParcelle['codehameau'] = ""
                        emplacementParcelle['codefkt'] = ""
                        emplacementParcelle['codecommune'] = ""
                        emplacementParcelle['codedistrict'] = ""
                    ###Limites de la parcelle ###
                    try:
                        self.cur.execute("SELECT LOWER(pc.position), lm.description "
                                         "FROM pointscardinaux pc, limitesparcelle lm, parcelle_d pd "
                                         "WHERE lm.idparcelle = pd.gid "
                                         "AND pc.idpointscardinaux = lm.idpointscardinaux "
                                         "AND lm.idparcelle = %s", (idparcelle,))
                        results = self.cur.fetchall()
                        # print results
                        if results is not None:
                            for res in results:
                                if str(res[0]).strip() == "nord":
                                    print "Mandalo ato"
                                    if res[1] is not None:
                                        limitesparcelle['nord'] = self.takeCareOfAccent(
                                            unicode(res[1]).encode('utf-8').strip())
                                    else:
                                        limitesparcelle['nord'] = ""
                                elif str(res[0]).strip() == "sud":
                                    if res[1] is not None:
                                        limitesparcelle['sud'] = self.takeCareOfAccent(
                                            unicode(res[1]).encode('utf-8').strip())
                                    else:
                                        limitesparcelle['sud'] = ""
                                elif str(res[0]).strip() == "est":
                                    if res[1] is not None:
                                        limitesparcelle['est'] = self.takeCareOfAccent(
                                            unicode(res[1]).encode('utf-8').strip())
                                    else:
                                        limitesparcelle['est'] = ""
                                elif str(res[0]).strip() == "ouest":
                                    if res[1] is not None:
                                        limitesparcelle['ouest'] = self.takeCareOfAccent(
                                            unicode(res[1]).encode('utf-8').strip())
                                    else:
                                        limitesparcelle['ouest'] = ""
                            print limitesparcelle
                        else:
                            limitesparcelle['nord'] = ""
                            limitesparcelle['sud'] = ""
                            limitesparcelle['est'] = ""
                            limitesparcelle['ouest'] = ""

                    except StandardError as e:
                        print(e)
                        self.connection.rollback()
                    ###Charges de la parcelle###
                    ##Autre charges
                    try:
                        self.cur.execute("SELECT ac.descriptioncharge, ac.dateinscriptionregistre "
                                         "FROM autrecharge ac, autrechargesparcelle_d acp "
                                         "WHERE ac.idcharge = acp.idcharge "
                                         "AND acp.idparcelle = %s", (idparcelle,))
                        autreCharge = self.cur.fetchall()
                        for chg in autreCharge:
                            print chg[0]
                            charge = charge + "Vesatra " + unicode(chg[0]).encode('utf-8').strip() + " tamin'ny " + chg[
                                1].strftime('%d/%m/%Y') + "<br/>"
                        # print autreCharge
                    except StandardError as e:
                        print(e)
                        self.connection.rollback()
                    ##Hypotheque
                    try:
                        self.cur.execute("SELECT h.descriptionhypotheque, h.valeur, "
                                         "h.creancier, h.dateinscriptionregistre, "
                                         "h.dateradiation "
                                         "FROM hypotheque h, hypothequeparcelle_d hp "
                                         "WHERE h.idhypotheque = hp.idhypotheque "
                                         "AND hp.idparcelle = %s", (idparcelle,))
                        hypotheque = self.cur.fetchall()
                        for hyp in hypotheque:
                            charge = charge + "Hypotheque " + unicode(hyp[0]).encode(
                                'utf-8').strip() + " mitentina " + str(hyp[1]).strip() + " ao amin'ny " + unicode(
                                hyp[2]).encode('utf-8').strip() + " tamin'ny " + hyp[3].strftime('%d/%m/%Y') + "<br/>"
                        # print hypotheque
                    except StandardError as e:
                        print(e)
                        self.connection.rollback()
                    ##Servitude
                    try:
                        self.cur.execute("SELECT s.descriptionservitude, s.dateinscription, "
                                         "s.datelevee, s.origine "
                                         "FROM servitude s, servitudeparcelle_d sp "
                                         "WHERE s.idservitude = sp.idservitude "
                                         "AND sp.idparcelle = %s", (idparcelle,))
                        servitude = self.cur.fetchall()
                        for ser in servitude:
                            charge = charge + "Hypotheque " + str(ser[0]).encode('utf-8').strip() + " tamin'ny " + ser[
                                1].strftime('%d/%m/%Y') + "<br/>"

                        # print servitude
                    except StandardError as e:
                        print(e)
                        self.connection.rollback()

            except StandardError as e:
                print(e)
                self.connection.rollback()
            print charge
            numDmde = ""
            # numCF = ""
            dateDmde = ""
            AireHa = str(0)
            AireCa = str(0)
            AireA = str(0)
            # print infosCF
            if infosCF != None:
                numDmde = str(infosCF[0]).strip()
                # numCF = str(infosCF[0]).strip()
                dateDmde = infosCF[1].strftime('%d/%m/%Y')
                dateDecision = infosCF[5].strftime('%d/%m/%Y')
                consistance = ""
                categorie = ""
                numDecision = ""
                if infosCF[6] is not None:
                    consistance = "\t\t" + str(infosCF[6]).strip()
                if infosCF[7] is not None:
                    categorie = str(infosCF[7]).strip()
                if infosCF[8] is not None:
                    numDecision = infosCF[8].strip()
                dateReconnaissance = ""
                dateFinAffichage = ""
                if infosCF[9] is not None:
                    dateReconnaissance = infosCF[9].strftime('%d/%m/%Y')
                    dateFinAffichage = (infosCF[9] - datetime.timedelta(-1)).strftime('%d/%m/%Y')

                # infoPersonne = infoProprio['nom']  + " " + infoProprio['prenom'] + " CIN: " + infoProprio['numpiece'] #+ " natao tao " + infoProprio['lieupiece'] + "<br>Teraka ny " + infoProprio['datenaissance'] + " tao " + infoProprio['lieunaissance']+ "<br>Zanak'i " + infoProprio['nompere'] + " sy " + infoProprio['nommere']

                print infoProprio

            dic = {
                # "$numCF": numCF,
                "numDmde": numDmde,
                "dateDmde": dateDmde,
                "dateDecision": dateDecision,
                "numDecision": numDecision,
                "dateReconnaissance": dateReconnaissance,
                "dateAffichage": dateFinAffichage,
                "consistance": consistance,
                "categorie": categorie,
                "proprios": proprio,
                "nord": limitesparcelle['nord'],
                "sud": limitesparcelle['sud'],
                "est": limitesparcelle['est'],
                "ouest": limitesparcelle['ouest'],
            }
            dic_Key = 1
            if ((compteur_demande % nbr_dmd_par_page) <= nbr_dmd_par_page):
                key = "$" + str(dic_Key)
                print "mandalo modulo"
                demandes_to_print.append(dic)
                # dic_Key = dic_Key + 1
            launch_print = False
            if compteur_demande % nbr_dmd_par_page == 0:
                launch_print = True
            if compteur_demande == len(self.idsDmdtoPrint):
                launch_print = True

            proprioVide = []
            proprioVide.append({
                "numero": "",
                "nom": "",
                "prenom": "",
                "numpiece": "",
                "lieupiece": "",
                "datenaiss": "",
                "lieunaiss": "",
                "nopere": "",
                "no_mere": "",
                "matrimoniale": "",
                "adresse": "",
                "consorts": ""

            })

            if launch_print:
                print 'numpage'
                print num_page
                dic_to_print = {}
                if len(demandes_to_print) == 1:
                    dic_to_print = {
                        "$numDmde1": demandes_to_print[0]['numDmde'],
                        "$dateDmde1": demandes_to_print[0]['dateDmde'],
                        "$dateDecision1": demandes_to_print[0]['dateDecision'],
                        "$numDecision1": str(demandes_to_print[0]['numDecision']),
                        "$dateReconnaissance1": demandes_to_print[0]['dateReconnaissance'],
                        "$dateAffichage1": demandes_to_print[0]['dateAffichage'],
                        "$consistance1": demandes_to_print[0]['consistance'],
                        "$categorie1": demandes_to_print[0]['categorie'],
                        "$proprios1": demandes_to_print[0]['proprios'],
                        "$nord1": demandes_to_print[0]['nord'],
                        "$sud1": demandes_to_print[0]['sud'],
                        "$est1": demandes_to_print[0]['est'],
                        "$ouest1": demandes_to_print[0]['ouest'],
                        "$numDmde2": "",
                        "$dateDmde2": "",
                        "$dateDecision2": "",
                        "$numDecision2": "",
                        "$dateReconnaissance2": "",
                        "$dateAffichage2": "",
                        "$consistance2": "",
                        "$categorie2": "",
                        "$proprios2": proprioVide,
                        "$nord2": "",
                        "$sud2": "",
                        "$est2": "",
                        "$ouest2": "",
                        "$numDmde3": "",
                        "$dateDmde3": "",
                        "$dateDecision3": "",
                        "$numDecision3": "",
                        "$dateReconnaissance3": "",
                        "$dateAffichage3": "",
                        "$consistance3": "",
                        "$categorie3": "",
                        "$proprios3": proprioVide,
                        "$nord3": "",
                        "$sud3": "",
                        "$est3": "",
                        "$ouest3": "",
                        "$num_page": str(num_page)

                    }

                elif len(demandes_to_print) == 2:
                    dic_to_print = {
                        "$numDmde1": demandes_to_print[0]['numDmde'],
                        "$dateDmde1": demandes_to_print[0]['dateDmde'],
                        "$dateDecision1": demandes_to_print[0]['dateDecision'],
                        "$numDecision1": str(demandes_to_print[0]['numDecision']),
                        "$dateReconnaissance1": demandes_to_print[0]['dateReconnaissance'],
                        "$dateAffichage1": demandes_to_print[0]['dateAffichage'],
                        "$consistance1": demandes_to_print[0]['consistance'],
                        "$categorie1": demandes_to_print[0]['categorie'],
                        "$proprios1": demandes_to_print[0]['proprios'],
                        "$nord1": demandes_to_print[0]['nord'],
                        "$sud1": demandes_to_print[0]['sud'],
                        "$est1": demandes_to_print[0]['est'],
                        "$ouest1": demandes_to_print[0]['ouest'],
                        "$numDmde2": demandes_to_print[1]['numDmde'],
                        "$dateDmde2": demandes_to_print[1]['dateDmde'],
                        "$dateDecision2": demandes_to_print[1]['dateDecision'],
                        "$numDecision2": str(demandes_to_print[1]['numDecision']),
                        "$dateReconnaissance2": demandes_to_print[1]['dateReconnaissance'],
                        "$dateAffichage2": demandes_to_print[1]['dateAffichage'],
                        "$consistance2": demandes_to_print[1]['consistance'],
                        "$categorie2": demandes_to_print[1]['categorie'],
                        "$proprios2": demandes_to_print[1]['proprios'],
                        "$nord2": demandes_to_print[1]['nord'],
                        "$sud2": demandes_to_print[1]['sud'],
                        "$est2": demandes_to_print[1]['est'],
                        "$ouest2": demandes_to_print[1]['ouest'],
                        "$numDmde3": "",
                        "$dateDmde3": "",
                        "$dateDecision3": "",
                        "$numDecision3": "",
                        "$dateReconnaissance3": "",
                        "$dateAffichage3": "",
                        "$consistance3": "",
                        "$categorie3": "",
                        "$proprios3": proprioVide,
                        "$nord3": "",
                        "$sud3": "",
                        "$est3": "",
                        "$ouest3": "",
                        "$num_page": str(num_page)

                    }
                elif len(demandes_to_print) == 3:
                    dic_to_print = {
                        "$numDmde1": demandes_to_print[0]['numDmde'],
                        "$dateDmde1": demandes_to_print[0]['dateDmde'],
                        "$dateDecision1": demandes_to_print[0]['dateDecision'],
                        "$numDecision1": str(demandes_to_print[0]['numDecision']),
                        "$dateReconnaissance1": demandes_to_print[0]['dateReconnaissance'],
                        "$dateAffichage1": demandes_to_print[0]['dateAffichage'],
                        "$consistance1": demandes_to_print[0]['consistance'],
                        "$categorie1": demandes_to_print[0]['categorie'],
                        "$proprios1": demandes_to_print[0]['proprios'],
                        "$nord1": demandes_to_print[0]['nord'],
                        "$sud1": demandes_to_print[0]['sud'],
                        "$est1": demandes_to_print[0]['est'],
                        "$ouest1": demandes_to_print[0]['ouest'],
                        "$numDmde2": demandes_to_print[1]['numDmde'],
                        "$dateDmde2": demandes_to_print[1]['dateDmde'],
                        "$dateDecision2": demandes_to_print[1]['dateDecision'],
                        "$numDecision2": str(demandes_to_print[1]['numDecision']),
                        "$dateReconnaissance2": demandes_to_print[1]['dateReconnaissance'],
                        "$dateAffichage2": demandes_to_print[1]['dateAffichage'],
                        "$consistance2": demandes_to_print[1]['consistance'],
                        "$categorie2": demandes_to_print[1]['categorie'],
                        "$proprios2": demandes_to_print[1]['proprios'],
                        "$nord2": demandes_to_print[1]['nord'],
                        "$sud2": demandes_to_print[1]['sud'],
                        "$est2": demandes_to_print[1]['est'],
                        "$ouest2": demandes_to_print[1]['ouest'],
                        "$numDmde3": demandes_to_print[2]['numDmde'],
                        "$dateDmde3": demandes_to_print[2]['dateDmde'],
                        "$dateDecision3": demandes_to_print[2]['dateDecision'],
                        "$numDecision3": str(demandes_to_print[2]['numDecision']),
                        "$dateReconnaissance3": demandes_to_print[2]['dateReconnaissance'],
                        "$dateAffichage3": demandes_to_print[2]['dateAffichage'],
                        "$consistance3": demandes_to_print[2]['consistance'],
                        "$categorie3": demandes_to_print[2]['categorie'],
                        "$proprios3": demandes_to_print[2]['proprios'],
                        "$nord3": demandes_to_print[2]['nord'],
                        "$sud3": demandes_to_print[2]['sud'],
                        "$est3": demandes_to_print[2]['est'],
                        "$ouest3": demandes_to_print[2]['ouest'],
                        "$num_page": str(num_page)

                    }

                num_page = num_page + 1
                dic_Key = 0
                print 'demandes to print'
                print dic_to_print
                print 'demande to print'
                converter = Html2Pdf()
                # print (converter)
                print "After Html2Pdf"
                converter.setOrientation(orientation="Landscape")
                converter.setFormat(format="A3")
                converter.setMarginLeft(margin=25)
                print "After format"
                src = os.path.dirname(__file__) + "\\" + self.template
                print src
                dst = os.path.join(tempfile.gettempdir(), str(randint(10000, 99999)) + "-" + self.template + ".pdf")
                QApplication.setOverrideCursor(Qt.Qt.WaitCursor)
                print "Before Generate"
                try:
                    converter.generate(html=src, pdf=dst, dictionnary=dic_to_print)
                except Exception as err:
                    print(err)

                print "After generate"
                # webbrowser.open(dst)
                self.merger.append(dst)
                # webbrowser.open(dst)
                QApplication.restoreOverrideCursor()
                print 'avant clear'
                try:
                    del demandes_to_print[:]
                except Exception as err:
                    print(err)
                print 'after clear'
                print demandes_to_print
                self.setEnabled(True)

        dstFinal = os.path.join(tempfile.gettempdir(), str(randint(10000, 99999)) + "-" + "Registre Demande.pdf")
        self.merger.write(dstFinal)
        print 'after merger write'
        self.emit(SIGNAL("finished()"))
        webbrowser.open(dstFinal)
