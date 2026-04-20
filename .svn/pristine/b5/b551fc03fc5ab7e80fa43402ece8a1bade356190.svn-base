# coding: utf8
from PyQt4.QtCore import QThread, SIGNAL
from PyQt4.QtGui import QMessageBox
from osgeo import gdal, ogr
#import ogrinfo
import sys
import os
import os.path
import globalvars
from datetime import datetime
import psycopg2
import time
from xlrd import open_workbook
import xlrd
import io
from logs import xlsLogger


class ImporterThreadFromField(QThread):
    def __init__(self, filename, connection):
        QThread.__init__(self)
        self.filename, self.connection = filename, connection
        self.current_step =-1
        self.logger = xlsLogger.xlsLogger("Import_Data_Terrain")

    def __del__(self):
        self.wait()

    def run(self):
        #print (self.filename)
        if self.filename == "":
            self.emit(SIGNAL("alert(QString)"), "Veuillez choisir un fichier")
            return
        # poDS = ogr.Open(str(self.filename), False)
        # if poDS is None:
        # self.emit(SIGNAL("alert(QString)"), "Fichier ogr non valide")
        # return

        #IMPORT PERSONNE PHYSIQUE
        self.emit(SIGNAL("stepInit(int)"), self.current_step + 1)
        print("Debut import Personne Physique")
        self.importPersonnePhysique()
        print("Fin import Personne Physique")
        self.emit(SIGNAL("stepDone(int)"), self.current_step)
        #FIN IMPORT PERSONNE PHYSIQUE

        #IMPORT LOCALITES
        self.emit(SIGNAL("stepInit(int)"), self.current_step + 1)
        print("Debut import localites")
        self.inportLocalite()
        print("Fin import localites")
        self.emit(SIGNAL("stepDone(int)"), self.current_step)
        #FIN IMPORT LOCALITES

        #IMPORT DEMANDE
        self.emit(SIGNAL("stepInit(int)"), self.current_step + 1)
        print("Debut import DEMANDE")
        self.importDemande()
        print("Fin import DEMANDE")
        self.emit(SIGNAL("stepDone(int)"), self.current_step)
        #FIN IMPORT DEMANDE

        # IMPORT CODEMANDEUR
        self.emit(SIGNAL("stepInit(int)"), self.current_step + 1)
        print("Debut import CODEMANDEURS")
        self.importCodemandeurs()
        print("Fin import CODEMANDEURS")

        self.logger.write()

        self.emit(SIGNAL("stepDone(int)"), self.current_step)
        # FIN IMPORT CODEMANDEUR

    def getIdParcelle(self, codeParcelle):

        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT gid FROM parcelle_d WHERE codeparcelle = %s and id_commune =  %s",
                                             (codeParcelle,str(globalvars.id_commune)))
            dt = cursor.fetchone()
            return dt[0]
        except StandardError as err:
            print (err)
            self.connection.rollback()
            return None

    def getIdDemande(self, codeParcelle):

        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT iddemande FROM demande WHERE code_parcelle = %s and idcommune =  %s",
                                             (codeParcelle, str(globalvars.id_commune)))
            dt = cursor.fetchone()
            return dt[0]
        except StandardError as err:
            print (err)
            self.connection.rollback()
            return None


    def getIdCommune(self, codeCommune):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT idcommune FROM commune WHERE codecommune = %s",
                                             (codeCommune,))
            dt = cursor.fetchone()
            return dt[0]
        except StandardError as err:
            print (err)
            self.connection.rollback()
            return None


    def getidFkt(self, codeFkt, codeCommune):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT f.idfokontany FROM fokontany f INNER JOIN commune c ON f.idcommune = c.idcommune WHERE c.codecommune = %s AND f.codefokontany = %s",
                                             (codeCommune,codeFkt))
            dt = cursor.fetchone()
            return dt[0]
        except StandardError as err:
            print (err)
            self.connection.rollback()
            return None


    def getIdPersonne(self, idPers_xl):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT idpersonne FROM personne WHERE csv_id = %s", (idPers_xl,))
            dt = cursor.fetchone()
            return dt[0]
        except Exception as err:
            print (err)
            self.connection.rollback()
            return  None

    def getIdHameau(self, codeHameau, idFokontany):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT h.idhameau FROM hameau h INNER JOIN fokontany f ON f.idfokontany = h.idfokontany WHERE h.codehameau = %s AND f.idfokontany = %s",
                                             (codeHameau,idFokontany))
            dt = cursor.fetchone()
            return dt[0]
        except StandardError as err:
            print (err)
            self.connection.rollback()
            return None

    def updateCptDemande(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("UPDATE commune SET cptdemande = (SELECT (MAX(CAST(TRIM(SPLIT_PART(dmd.numdemande,'-','4')) as integer)) + 1) as ordre FROM demande dmd WHERE TRIM(SPLIT_PART(dmd.numdemande,'-','4')) <> '' )")
            self.connection.commit()
            #QMessageBox.information(None, 'Compteur Demande', u'Compteur demande mis à jour')
            print(u'compteur demande à jour')
        except Exception as err:
            #QMessageBox.critical(None, 'erreur', u'Numéro demande non conforme XXX-XX-F-XXX')
            self.connection.rollback()
            print(err)

    def updateProprietaire(self):
        cursor = self.connection.cursor()
        res = None
        try:

            cursor.execute('SELECT idpersonne, idparcelle FROM proprietaireparcelle')
            res = cursor.fetchall()
            self.connection.commit()
        except Exception as err:
            print(err)
            self.connection.rollback()

        if res is not None:
            for result in res:
                print result[0]
                try:
                    cursor.execute(
                        'SELECT COUNT(idpersonne) FROM proprietaireparcelle WHERE representant = True and idparcelle = %s',(result[1],))
                    nbrDmd = cursor.fetchone()
                    if nbrDmd[0] == 0:
                        try:
                            cursor.execute('UPDATE proprietaireparcelle SET representant=True WHERE idparcelle=%s and idpersonne = %s',
                                           (result[1], result[0]))
                            self.connection.commit()
                        except Exception as err:
                            print (err)
                            self.connection.rollback()
                except Exception as err:
                    print(err)
                    self.connection.rollback()


    def importPersonnePhysique(self):
        # Preparation log
        title = ["idxl_personne", "nom", "etat_insertion", "erreur"]
        dataToLog = []
        # fin prep    log
        self.current_step = self.current_step + 1
        self.emit(SIGNAL("clearSubstep(int)"), self.current_step)
        cursor = self.connection.cursor()
        print ("IMPORT PERSONNE")
        self.emit(SIGNAL("clearSubstep(int)"), self.current_step)
        print ("signal")
        try:
            wb = open_workbook(self.filename, encoding_override="utf8")
        except Exception as err:
            print (err)
            pass
        sh_personne = None
        #sh_demande = None
        #sh_crl = None
        #sh_hameau = None

        #iteration sur les feuilles
        curSheet = 0
        while curSheet <  wb.nsheets:
            sh = wb.sheet_by_index(curSheet)
            if str(sh.name).strip().upper() == "PERSONNE":
                sh_personne = sh
            curSheet = curSheet + 1

        if sh_personne is not None:
            total_lignes = sh_personne.nrows
            sh_personne.cell_value(0, 0)
            line = 0 #lignes
            print ('nombre ligne')
            print (sh_personne.nrows)
            while line < sh_personne.nrows:
                col = 0
                if line >= 1:
                    etatInsertion, erreur, idxpers, nom_pers = '', '', '', ''

                    idpers_xl = sh_personne.cell_value(line, 0)
                    idxpers = str(idpers_xl)
                    nom = str(sh_personne.cell_value(line, 1)).decode('utf-8')
                    nom_pers = nom
                    prenoms = str(sh_personne.cell_value(line, 2)).decode('utf-8')
                    genre = str(sh_personne.cell_value(line, 3)).decode('utf-8')
                    # typeIdentite = sheet.cell_value(line, )
                    sexe = ""
                    if genre == "F":
                        sexe = "feminin"
                    elif genre == "H":
                        sexe = "masculin"
                    else:
                        sexe = self.retsexe(num_cin)
                    #test type date
                    print nom
                    print prenoms

                    #verification si date naissance approx
                    date_naiss_appox = False
                    date_naissance = None
                    nevers = None
                    if str(sh_personne.cell_value(line, 4).decode('utf-8')).strip() == 'oui':
                        date_naiss_appox = True
                    if date_naiss_appox:
                        date = self.traiter_date(sh_personne, line, 5, wb)
                        nevers = date.strftime('%Y')
                        print nevers
                    else:
                        date_naissance = self.traiter_date(sh_personne,line, 5, wb)
                    print "date naissance"
                    print date_naissance
                    num_cin = None
                    num_acte = None
                    lieu_cin = None
                    date_cin = None
                    lieu_acte = None
                    date_acte = None
                    if str(sh_personne.cell_value(line,7)).upper() == "CIN":
                        if sh_personne.cell_type(line,8) == 2:
                            num_cin = str(int(sh_personne.cell_value(line,8)))
                            date_cin = self.traiter_date(sh_personne,line, 9, wb)
                            lieu_cin = str(sh_personne.cell_value(line, 10)).decode('utf-8')
                    elif str(sh_personne.cell_value(line,7)).upper().strip() == "ACTE_NAISSANCE":
                        if sh_personne.cell_type(line,8) == 2:
                            num_acte = str(int(sh_personne.cell_value(line,8)))
                            date_acte = self.traiter_date(sh_personne, line, 9, wb)
                            lieu_acte = str(sh_personne.cell_value(line, 10)).decode('utf-8')

                    print "num_cin"
                    print num_cin
                    id_conjoint_xl = None
                    adresse = str(sh_personne.cell_value(line, 11)).decode('utf-8')
                    #Traiter matrimoniale
                    # etat_matri = sheet.cell_value(line, 35)
                    sit_matri = 1
                    if str(sh_personne.cell_value(line, 12)).decode('utf-8').strip().lower() != "celibataire":
                        sit_matri = 1
                    elif str(sh_personne.cell_value(line, 12)).decode('utf-8').strip().lower() != "marié":
                        sit_matri = 2
                        id_conjoint_xl = str(sh_personne.cell_value(line, 13)).decode('utf-8').strip()
                        #tokony misy fonction manao mise à jour idConjoint par personne
                    elif str(sh_personne.cell_value(line, 12)).decode('utf-8').strip().lower() != "veuf":
                        sit_matri = 3

                    #print ("dans la boucle")
                    # print(date_naissance)
                    lieu_naissance = str(sh_personne.cell_value(line, 6)).decode('utf-8')

                    nom_pere = sh_personne.cell_value(line, 14)
                    nom_mere = sh_personne.cell_value(line, 15)

                    # mariea = sheet.cell_value(line, 36)
                    adresse = str(sh_personne.cell_value(line, 11))
                    print "Adresse"
                    print (adresse)
                    print "Date CIN"
                    print(date_cin)
                    # Insertion dans la base

                    #Cas identité par cin

                    if self.exists("personne", "numcipersonne", num_cin):
                        self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
                                          "Personne %s existe deja en base" % (num_cin), "orange")
                    else:
                        try:
                            cursor = self.connection.cursor()
                            cursor.execute ('INSERT INTO personne (nompersonne, prenompersonne, sexepersonne, '
                                            'datenaissancepersonne, nevers, lieunaissancepersonne, numcipersonne,'
                                            'datecipersonne, lieucipersonne, numactenaissancepersonne, '
                                            'dateactenaissancepersonne,lieuactenaissancepersonne, adressepersonne, situationmatrimoniale,'
                                            'nompere, nommere, csv_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                                            (nom, prenoms, sexe, date_naissance, nevers,lieu_naissance, num_cin, date_cin, lieu_cin,
                                             num_acte, date_acte,lieu_acte, adresse, sit_matri, nom_pere,
                                             nom_mere, idpers_xl))
                            self.connection.commit()
                            etatInsertion = "INSERTION REUSSI"
                            self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
                                      u"Personne %s insérée dans la base" % (str(nom)), "green")
                        except Exception as err:
                            print(err)
                            self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, str(err), "red")
                            self.connection.rollback()
                            etatInsertion = "ECHEC INSERTION"
                            erreur = str(err)

                    dataToLog.append(
                        {"idxl_personne": idxpers, "nom": nom_pers, "etat_insertion": etatInsertion,
                         "erreur": erreur})

                p = (line + 1) * 100 / total_lignes
                self.emit(SIGNAL("progress(int)"), p)
                line = line + 1

        self.logger.addSheet(title=title, data=dataToLog, sheet_name="Log Import Personne")

    def importDemande(self):
        # Preparation log
        title = ["code_parcelle", "numero_demande", "etat_insertion", "erreur"]
        dataToLog = []
        self.current_step = self.current_step + 1
        self.emit(SIGNAL("clearSubstep(int)"), self.current_step)
        cursor = self.connection.cursor()
        print ("IMPORT DEMANDE")
        self.emit(SIGNAL("clearSubstep(int)"), self.current_step)
        print ("signal")
        try:
            wb = open_workbook(self.filename, encoding_override="utf8")
        except Exception as err:
            print (err)
            pass
        sh_demande = None
        sh_codemandeurs = None
        # sh_demande = None
        # sh_crl = None
        # sh_hameau = None

        # iteration sur les feuilles

        curSheet = 0
        while curSheet < wb.nsheets:
            sh = wb.sheet_by_index(curSheet)
            if str(sh.name).strip().upper() == "DEMANDE":
                sh_demande = sh
            if str(sh.name).strip().upper() == "CO-DEMANDEURS":
                sh_codemandeurs = sh
            curSheet = curSheet + 1

        #INSERTION DES DEMANDES
        if sh_demande is not None:
            total_lignes = sh_demande.nrows
            sh_demande.cell_value(0, 0)

            line = 0  # lignes
            print ('nombre ligne')
            print (sh_demande.nrows)
            while line < sh_demande.nrows:
                col = 0
                if line >= 1:
                    etatInsertion, erreur, numDmd = '', '', ''
                    codeParcelle = ""
                    if sh_demande.cell_type(line, 12) == 2:
                        codeParcelle = str(int(sh_demande.cell_value(line, 12))).strip()
                    else:
                        codeParcelle = str(sh_demande.cell_value(line, 12)).strip()
                    print('codeParcelle == ' + codeParcelle)
                    idParcelle = self.getIdParcelle(codeParcelle)
                    numdemande = str(sh_demande.cell_value(line, 20)).strip()
                    datedemande = self.traiter_date(sh_demande,line,13,wb)
                    datereconnaissance = self.traiter_date(sh_demande,line,15,wb)
                    date_deb_Affichage = self.traiter_date(sh_demande,line,16,wb)
                    date_fin_Affichage = self.traiter_date(sh_demande, line, 17, wb)
                    region = str(sh_demande.cell_value(line, 0)).decode('utf-8').strip()
                    district = str(sh_demande.cell_value(line, 1)).decode('utf-8').strip()
                    consistance = str(sh_demande.cell_value(line, 23)).strip()

                    datedecision = self.traiter_date(sh_demande,line, 14, wb)
                    categorie = str(sh_demande.cell_value(line, 22)).decode('utf-8').strip()
                    self.insertToCategorie(categorie)
                    num_decision = str(sh_demande.cell_value(line, 18)).decode('utf-8').strip()

                    #Recuperation des voisins
                    voisins = {}
                    voisins['est'] = str(sh_demande.cell_value(line, 24)).decode('utf-8').strip()
                    voisins['ouest'] = str(sh_demande.cell_value(line, 25)).decode('utf-8').strip()
                    voisins['nord'] = str(sh_demande.cell_value(line, 26)).decode('utf-8').strip()
                    voisins['sud'] = str(sh_demande.cell_value(line, 27)).decode('utf-8').strip()

                    #Demandeurs
                    id_demaneur_xl = str(sh_demande.cell_value(line, 28)).decode('utf-8').strip()

                    codeCommune = str(sh_demande.cell_value(line, 8)).decode('utf-8').strip()
                    codeFkt = str(sh_demande.cell_value(line, 9)).decode('utf-8').strip()
                    codeHameau = str(sh_demande.cell_value(line, 10)).decode('utf-8').strip()

                    #idCommune = self.getIdCommune(codeCommune)
                    idCommune = globalvars.id_commune

                    id_fokontany = self.getidFkt(codeFkt, codeCommune)

                    idHameau = self.getIdHameau(codeHameau, id_fokontany)

                    print ('id_hameau=')
                    print(idHameau)

                    print ('idParcelle = ')
                    print (idParcelle)
                    #Recup idhameau + idcommune + idfokontany

                    #Recup demandeur

                    if idParcelle is not None:
                        #update de la table parcelle_d
                        try:
                            cursor = self.connection.cursor()
                            cursor.execute('UPDATE parcelle_d SET numdemande = %s, consistance = %s, idhameau = %s, id_commune = %s'
                                           ' WHERE gid = %s',(numdemande, consistance, idHameau, idCommune, idParcelle))
                            self.connection.commit()

                        except Exception as err:
                            print(err)
                            self.connection.rollback()
                        #Insertion de la demande
                        where = "code_parcelle = '" + codeParcelle + "' and idcommune = " + str(idCommune)
                        if self.select("demande", "iddemande", where) is not None:
                            print "code parcelle existant dans demande"
                            try:
                                cursor = self.connection.cursor()
                                cursor.execute('UPDATE demande SET numdemande = %s, gid = %s, '
                                               'datedemande = %s, datereconnaissance = %s, region = %s, '
                                               'district = %s, idfokontany = %s, idcommune = %s, cout = %s, consistance = %s,'
                                               'idprojet = %s, datedecision = %s, categorie = %s, numdecision = %s, debut_affichage = %s, fin_affichage = %s '
                                               'WHERE code_parcelle = %s returning iddemande',
                                               (numdemande, idParcelle, datedemande, datereconnaissance, region,
                                                district,
                                                id_fokontany, idCommune, 0, consistance, globalvars.id_projet,
                                                datedecision, categorie, num_decision, date_deb_Affichage,
                                                date_fin_Affichage, codeParcelle))
                                self.connection.commit()
                                self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
                                          u"Demande %s insérée dans la base" % (str(numdemande)), "green")
                                etatInsertion = "MISE A JOUR REUSSI"
                            except Exception as err:
                                print (err)
                                self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, str(err),
                                          "red")
                                self.connection.rollback()
                        else:
                            try:
                                cursor = self.connection.cursor()
                                cursor.execute('INSERT INTO demande (numdemande, gid, '
                                               'datedemande, datereconnaissance, region, '
                                               'district, idfokontany, idcommune, cout, consistance,'
                                               'idprojet, datedecision, categorie, code_parcelle, numdecision, debut_affichage, fin_affichage) '
                                               'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning iddemande',
                                               (numdemande, idParcelle, datedemande, datereconnaissance, region, district,
                                                id_fokontany, idCommune, 0, consistance, globalvars.id_projet, datedecision, categorie, codeParcelle, num_decision,date_deb_Affichage, date_fin_Affichage))
                                self.connection.commit()
                                etatInsertion = "INSERTION REUSSI"
                                self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
                                          u"Demande %s insérée dans la base" % (str(numdemande)), "green")

                            except Exception as err:
                                print (err)
                                self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, str(err), "red")
                                self.connection.rollback()
                                etatInsertion = "ERREUR INSERTION"
                                erreur = str(err)
                        #insertion du proprietaire principale
                        id_proprio_principale = self.getIdPersonne(id_demaneur_xl)
                        id_demande = self.getIdDemande(codeParcelle)
                        print ('id_demande')
                        print (id_demande)
                        print ('id_proprio_principale')
                        print (id_proprio_principale)
                        representant = True

                        where = "idparcelle = '" + str(idParcelle) + "' and idpersonne = " + str(
                            id_proprio_principale) + " and representant IS " + str(representant).upper()
                        if self.select("avoir_demande", "iddemande", where) is not None:
                            try:
                                cursor.execute(
                                    'DELETE FROM avoir_demande WHERE representant IS %s AND idparcelle = %s AND idpersonne = %s  ',
                                    (representant, idParcelle, id_proprio_principale,))
                                self.connection.commit()
                            except Exception as err:
                                print err
                                self.connection.rollback()

                        try:
                            cursor = self.connection.cursor()


                            cursor.execute('INSERT INTO avoir_demande(idparcelle, iddemande, idpersonne, representant) '
                                               'VALUES(%s, %s, %s, %s)',(idParcelle, id_demande, id_proprio_principale, representant))
                            self.connection.commit()
                        except Exception as err:
                            print (err)
                            self.connection.rollback()

                        #insertion des voisins
                        for key, val in voisins.items():
                            idpoint = None
                            if key == 'nord':
                                idpoint =  4
                            if key == 'sud':
                                idpoint = 5
                            if key == 'est':
                                idpoint = 6
                            if key == 'ouest':
                                idpoint = 11

                            try:
                                cursor = self.connection.cursor()
                                where = "idpointscardinaux = '" + str(idpoint) + "' and idparcelle = " + str(
                                    idParcelle)
                                if self.select("limitesparcelle", "description", where) is not None:
                                    cursor.execute(
                                        'UPDATE limitesparcelle SET description = %s WHERE idpointscardinaux = %s AND idparcelle = %s ',
                                         (val, str(idpoint), idParcelle ))
                                else:
                                    cursor.execute('INSERT INTO limitesparcelle(idpointscardinaux, idparcelle,description) '
                                               'VALUES(%s, %s, %s)',(str(idpoint), idParcelle, val))
                                self.connection.commit()
                            except Exception as err:
                                print (err)
                                self.connection.rollback()

                    else:
                        print ("idParcelle is None")

                    dataToLog.append(
                        {"code_parcelle": codeParcelle, "numero_demande": str(numdemande), "etat_insertion": etatInsertion,
                         "erreur": erreur})

                p = (line + 1) * 100 / total_lignes
                self.emit(SIGNAL("progress(int)"), p)
                line = line + 1

        self.updateCptDemande()
        self.logger.addSheet(title=title, data=dataToLog, sheet_name="Log Import Demande")

    def importCodemandeurs(self):
            self.current_step = self.current_step + 1
            self.emit(SIGNAL("clearSubstep(int)"), self.current_step)
            cursor = self.connection.cursor()
            print ("IMPORT CODEMANDEURS")
            self.emit(SIGNAL("clearSubstep(int)"), self.current_step)
            print ("signal")

            try:
                wb = open_workbook(self.filename, encoding_override="utf8")
            except Exception as err:
                print (err)
                pass
            sh_codemandeurs = None

            # iteration sur les feuilles

            curSheet = 0
            while curSheet < wb.nsheets:
                sh = wb.sheet_by_index(curSheet)
                if str(sh.name).strip().upper() == "CO-DEMANDEURS":
                    sh_codemandeurs = sh
                curSheet = curSheet + 1

            if sh_codemandeurs is not None:
                total_lignes = sh_codemandeurs.nrows
                sh_codemandeurs.cell_value(0, 0)

                line = 0  # lignes
                print ('nombre ligne')
                print (sh_codemandeurs.nrows)
                while line < sh_codemandeurs.nrows:
                    col = 0
                    if line >= 1:
                        codeParcelle = str(sh_codemandeurs.cell_value(line, 0)).strip()
                        id_pes_xl = str(sh_codemandeurs.cell_value(line, 1)).strip()
                        idParcelle = self.getIdParcelle(codeParcelle)
                        id_demande = self.getIdDemande(codeParcelle)
                        idpersonne = self.getIdPersonne(id_pes_xl)

                        print ('idparcelle')
                        print (idParcelle)
                        print ('id_demande')
                        print (id_demande)
                        print ('id_personne')
                        print (idpersonne)

                        where = "idparcelle = '" + str(idParcelle) + "' and idpersonne = " + str(
                            idpersonne)
                        if self.select("avoir_demande", "iddemande", where) is not None:
                            try:
                                cursor = self.connection.cursor()
                                cursor.execute('DELETE FROM avoir_demande WHERE idparcelle = %s AND idpersonne = %s  AND representant IS NOT TRUE'
                                               (idParcelle, idpersonne))
                                self.connection.commit()
                            except Exception as err:
                                print (err)
                                self.connection.rollback()
                        try:
                            cursor = self.connection.cursor()
                            cursor.execute('INSERT INTO avoir_demande(idparcelle, iddemande, idpersonne) '
                                           'VALUES(%s, %s, %s)',(idParcelle, str(id_demande), idpersonne))
                            self.connection.commit()
                        except Exception as err:
                            print (err)
                            self.connection.rollback()

                    p = (line + 1) * 100 / total_lignes
                    self.emit(SIGNAL("progress(int)"), p)
                    line = line + 1

    def inportLocalite(self):
        self.current_step = self.current_step + 1
        self.emit(SIGNAL("clearSubstep(int)"), self.current_step)
        cursor = self.connection.cursor()
        print ("IMPORT LOCALITES")
        self.emit(SIGNAL("clearSubstep(int)"), self.current_step)
        print ("signal")
        try:
            wb = open_workbook(self.filename, encoding_override="utf8")
        except Exception as err:
            print (err)
            pass
        sh_localites = None

        # iteration sur les feuilles

        curSheet = 0
        while curSheet < wb.nsheets:
            sh = wb.sheet_by_index(curSheet)
            if str(sh.name).strip().upper() == "LOCALITES":
                sh_localites = sh
            curSheet = curSheet + 1

        if sh_localites is not None:
            total_lignes = sh_localites.nrows
            sh_localites.cell_value(0, 0)

            line = 0  # lignes
            print ('nombre ligne')
            print (sh_localites.nrows)
            while line < sh_localites.nrows:
                col = 0
                if line >= 1:
                    nomHameau = str(sh_localites.cell_value(line, 0)).decode('utf-8').strip()
                    codeHameau = str(sh_localites.cell_value(line, 1)).decode('utf-8').strip()
                    nomFokontany = str(sh_localites.cell_value(line, 2)).decode('utf-8').strip()
                    codeFokontany = str(sh_localites.cell_value(line, 3)).decode('utf-8').strip()
                    nomCommune = str(sh_localites.cell_value(line, 4)).decode('utf-8').strip()
                    codeCommune = str(sh_localites.cell_value(line, 5)).decode('utf-8').strip()
                    if len(codeCommune) == 1:
                        codeCommune = codeCommune
                    #INSERT FOKONTANY
                    id_commune = self.getIdCommune(codeCommune)
                    print ('id_commune =')
                    print (id_commune)

                    try:
                        cursor = self.connection.cursor()
                        cursor.execute('INSERT INTO fokontany (idcommune, codefokontany, nomfokontany) '
                                       'VALUES (%s, %s, %s)',
                                       (id_commune, codeFokontany, nomFokontany))
                        self.connection.commit()
                    except Exception as err:
                        print(err)
                        self.connection.rollback()

                    #INSERT HAMEAU
                    id_FKT = self.getidFkt(codeFokontany, codeCommune)

                    try:
                        cursor = self.connection.cursor()
                        cursor.execute('INSERT INTO hameau (idfokontany, codehameau, nomhameau) '
                                       'VALUES (%s, %s, %s)',
                                       (id_FKT, codeHameau, nomHameau))
                        self.connection.commit()
                    except Exception as err:
                        print(err)
                        self.connection.rollback()

                p = (line + 1) * 100 / total_lignes
                self.emit(SIGNAL("progress(int)"), p)
                line = line + 1

    def traiter_date(self,sheet, line, col, wb):
        if sheet.cell_type(line, col) == 3 or sheet.cell_type(line,col) == 5:  # verification si la cellule est une date
            print "in date type"
            try:
                date = datetime(*xlrd.xldate.xldate_as_tuple(sheet.cell_value(line, col), wb.datemode))
                return date.date()
            except Exception as err:
                print err
                return None
        else:
            return None

    def getIdTypePM(self,label):
        cursor = self.connection.cursor()
        try:
            cursor.execute('SELECT idtype FROM typepersonnemorale WHERE type = %s', (label,))
            res = cursor.fetchone()
            return res[0]
        except Exception as err:
            print (err)
            self.connection.rollback()

    def importPersonneMorale(self):
        self.current_step = self.current_step + 1
        self.emit(SIGNAL("clearSubstep(int)"), self.current_step)
        cursor = self.connection.cursor()
        print ("IMPORT PERSONNE MORALE")
        self.emit(SIGNAL("clearSubstep(int)"), self.current_step)
        print ("signal")
        fileDirPath = ""
        try:
            fileDirPath = str(self.filename.toUtf8()).decode('utf-8')
            print(fileDirPath)
        except Exception as err:
            print(err)
        # print(fileDirPath)
        filePath = os.path.join(fileDirPath, "PM.xls")
        print (filePath)
        try:
            wb = open_workbook(filePath)
        except Exception as err:
            print (err)
            pass
        sheet = wb.sheet_by_index(0)
        total_lignes = sheet.nrows
        sheet.cell_value(0, 0)

        line = 0 #lignes
        while line < sheet.nrows:
            col = 0
            if line > 0:
                rcin = sheet.cell_value(line,2)
                denomination = sheet.cell_value(line, 17)
                nom_mandataire = sheet.cell_value(line, 20)
                typeDeclarant = sheet.cell_value(line, 19)
                date_creation = sheet.cell_value(line, 21) #annee creation
                date_creation = date_creation + '-01-01'
                observation = sheet.cell_value(line, 22)
                siege = sheet.cell_value(line, 23)
                typePM = sheet.cell_value(line, 18)
                self.importTypePm(typePM)
                id_type_pm = self.getIdTypePM(typePM)

                if self.exists("personnemorale", "rcin_pm", rcin):
                    self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
                              "Personne morale %s existe deja en base" % (rcin), "orange")
                else:
                    cursor = self.connection.cursor()
                    try:
                        cursor.execute(
                            "INSERT INTO personnemorale(denomination, datecreation,siege,observation,idtype,rcin_pm, mandataire, type_declarant" \
                            " ) " \
                            "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", (
                                denomination, date_creation, siege,
                                observation,
                                str(id_type_pm),
                                rcin, nom_mandataire,
                                typeDeclarant))
                        self.connection.commit()
                        self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
                                  "Personne %s" % (rcin), "green")
                    except Exception as err:
                        self.connection.rollback()
                        #self.saveErrorLine(ligneToLog, writer)
                        self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, str(err), "red")
                        print(err)

            p = (line + 1) * 100 / total_lignes
            self.emit(SIGNAL("progress(int)"), p)
            line = line + 1

    def exists(self, table, column, value):
        sql = "SELECT %s FROM %s WHERE %s=" % (column, table, column)
        cursor = self.connection.cursor()
        cursor.execute(sql + "%s", (value,))
        rows = cursor.fetchall()
        cursor.close()
        return len(rows) > 0

    def select(self, table, column, where):
        sql = "SELECT %s FROM %s WHERE %s" % (column, table, where)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        if len(rows) > 0:
            return rows[0][0]
        return None


    def saveErrorLine(self, line, writer):
        try:
            writer.writerow(line)
        except Exception as e:
            self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, str(e), "red")

    def stripSpace(self, chaine):
        chaineret = ""
        for c in chaine:
            if c != " ":
                chaineret = chaineret + c
        #print (chaineret)
        return chaineret
    def retsexe(self, chaine):
        i = 0
        sexe = "masculin"
        for c in chaine:
            if i == 5:
                if c == "2":
                    sexe = "feminin"
            i = i + 1
        return sexe

    def insertToCategorie(self, categorie):
        print 'call of insert categorie'
        cur = self.connection.cursor()
        res = None
        try:
            cur.execute('SELECT UPPER(TRIM(libelleconsistance)) FROM consistance WHERE UPPER(TRIM(libelleconsistance)) = %s', (categorie,))
            res = cur.fetchall()
            if len(res) == 0:
                res = None

        except Exception as err:
            print err
            self.connection.rollback()
        if res is None:
            curex = self.connection.cursor()
            try:
                curex.execute('INSERT INTO consistance (libelleconsistance, parcelleoubatiment) VALUES (%s,%s)',
                    (categorie,categorie))
                self.connection.commit()
                print ('insertion consistance categorie')

            except Exception as err:
                print err
                self.connection.rollback()
        #cur.close()