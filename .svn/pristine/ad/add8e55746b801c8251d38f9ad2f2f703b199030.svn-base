# coding: utf8
from PyQt4.QtCore import QThread, SIGNAL, QVariant
from PyQt4.QtGui import QMessageBox
from osgeo import gdal, ogr
from PyQt4 import QtSql
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
import csv
import tempfile
from logs import xlsLogger
#from Congiguration import DbConfig


class CorrectionOccupantThread(QThread):
    def __init__(self, filenames, connection, refimport = 0, steps = None):
        QThread.__init__(self)
        self.filenames, self.connection = filenames, connection
        self.refimport = refimport
        self.current_step =-1
        self.dataOccupantToRepair = []
        self.steps = steps
        self.logger = xlsLogger.xlsLogger("Correction Occupant")
        #self.db_config = DbConfig.DbConfig()

    def __del__(self):
        self.wait()

    def run(self):
        #print (self.filename)
        for filename in self.filenames.values():
            if filename == "":
                self.emit(SIGNAL("alert(QString)"), "Veuillez choisir un fichier pour chaque rubrique")
                return

        for step in self.steps:
            if str(step).strip() == u"Localités":
                # IMPORT LOCALITES
                self.emit(SIGNAL("stepInit(int)"), self.current_step + 1)
                print("Debut import localites")
                self.importLocalite()
                print("Fin import localites")
                #if str(step).strip() == str(self.steps[len(self.steps) - 1]).strip():
                    #self.logger.write()
                self.emit(SIGNAL("stepDone(int)"), self.current_step)
                # FIN IMPORT LOCALITES
            if str(step).strip() == u"Personne":
                #IMPORT PERSONNE PHYSIQUE
                self.emit(SIGNAL("stepInit(int)"), self.current_step + 1)
                print("Debut import Personne Physique")
                self.importPersonnePhysique()
                print("Fin import Personne Physique")
                if str(step).strip() == str(self.steps[len(self.steps) - 1]).strip():
                    self.logger.write()
                self.emit(SIGNAL("stepDone(int)"), self.current_step)
                #FIN IMPORT PERSONNE PHYSIQUE
            if str(step).strip() == u"Données parcellaire":
                #IMPORT DEMANDE
                self.emit(SIGNAL("stepInit(int)"), self.current_step + 1)
                print("Debut import DEMANDE")
                self.importDemande()
                print("Fin import DEMANDE")
                if str(step).strip() == str(self.steps[len(self.steps) - 1]).strip():
                    self.logger.write()
                self.emit(SIGNAL("stepDone(int)"), self.current_step)
                #FIN IMPORT DEMANDE
            if str(step).strip() == u"liaison personnes et parcelles":
                # IMPORT CODEMANDEUR
                self.emit(SIGNAL("stepInit(int)"), self.current_step + 1)
                print("Debut import occupants")
                self.importOccupants()
                print("Fin import CODEMANDEURS")
                if str(step).strip() == str(self.steps[len(self.steps) - 1]).strip():
                    self.logger.write()
                self.emit(SIGNAL("stepDone(int)"), self.current_step)
                # FIN IMPORT CODEMANDEUR


    def getIdParcelle(self, codeParcelle):

        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT gid FROM parcelle_d WHERE codeparcelle = %s AND id_commune = %s",
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
            cursor.execute("SELECT iddemande FROM demande WHERE code_parcelle = %s AND idcommune = %s",
                                             (codeParcelle,str(globalvars.id_commune)))
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


    def getidFkt(self, codeFkt, idcommune):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT f.idfokontany FROM fokontany f WHERE f.idcommune = %s AND f.codefokontany = %s",
                                             (idcommune,codeFkt))
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

    def updateNumDmdParcelle(self, numDemande, gid):
        curs = self.connection.cursor()
        try:
            curs.execute('UPDATE parcelle_d SET numdemande = %s WHERE gid = %s', (numDemande, gid))
            self.connection.commit()
        except Exception as err:
            print err

    def getCptDemande(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT cptdemande FROM commune WHERE idcommune = %s", (globalvars.id_commune,))
            res = cursor.fetchone()
            return res[0]
        except Exception as err:
            print(err)
            self.connection.rollback()
        cursor.close()

    def getCodesLoc(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT d.codedistrict, c.codeg FROM commune c INNER JOIN district d ON c.iddistrict = d.iddistrict WHERE idcommune = %s", (globalvars.id_commune,))
            res = cursor.fetchone()
            return res
        except Exception as err:
            print(err)
            self.connection.rollback()
        cursor.close()

    def updateCptDemande(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("UPDATE commune SET cptdemande = (SELECT (MAX(CAST(TRIM(SPLIT_PART(dmd.numdemande,'-','4')) as integer)) + 1) as ordre FROM demande dmd WHERE dmd.idcommune = %s)", (globalvars.id_commune,))
            self.connection.commit()
            #QMessageBox.information(None, 'Compteur Demande', u'Compteur demande mis à jour')
            print(u'compteur demande à jour')
        except Exception as err:
            #QMessageBox.critical(None, 'erreur', u'Numéro demande non conforme XXX-XX-F-XXX')
            self.connection.rollback()
            print(err)
        cursor.close()

    def getCptImport(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "SELECT cptimport FROM commune WHERE idcommune = %s"
                , (globalvars.id_commune,))
            res = cursor.fetchone()
            return res[0]
        except Exception as err:
            # QMessageBox.critical(None, 'erreur', u'Numéro demande non conforme XXX-XX-F-XXX')
            self.connection.rollback()
            print(err)
        cursor.close()

    def updateCptImport(self, cptImport):
        print "Call of update cptImport"
        cptImport = int(cptImport) + 1
        print "CptImport = " + str(cptImport)
        cursor = self.connection.cursor()
        try:
            cursor.execute("UPDATE commune SET cptimport = %s  WHERE idcommune = %s  ) "
                           "idcommune = %s", (cptImport,globalvars.id_commune))
            self.connection.commit()
            #QMessageBox.information(None, 'Compteur Demande', u'Compteur demande mis à jour')
            print(u'compteur import à jour')
        except Exception as err:
            #QMessageBox.critical(None, 'erreur', u'Numéro demande non conforme XXX-XX-F-XXX')
            self.connection.rollback()
            print(err)
        cursor.close()

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
            csv_personne_file = open(self.filenames['personne'], 'rb')
            csv_personne = csv.reader(csv_personne_file)

        except Exception as err:
            print ("Erreur:" + err)

        dir_path = ""
        try:
            dir_path = os.path.dirname(str(self.filenames['personne']))
            print dir_path
        except Exception as err:
            print (err)

        #csv_personne_copie = csv_personne

        #total_lignes = self.lenCsv(csv_personne_copie)
        #print "Total ligne"
        #print total_lignes
        total_lignes = self.lenCsv(csv_personne)

        csv_personne_file.seek(0)

        line = 0
        #csv_personne.seek(0)
        for data in csv_personne:
            print data
            if line > 0:
                datas = str(data[0]).split(";")
                etatInsertion, erreur, idxpers, nom_pers = '', '', '', ''

                print datas

                idpers_xl = datas[0].strip()
                idxpers = idpers_xl
                try:
                    nom = datas[1].strip().decode('utf-8')
                    prenoms = datas[2].strip().decode('utf-8')
                except Exception as err:
                    print (err)
                    erreur = erreur + u"Erreur sur l'enocodage du fichiers CSV empechant la prise en charge des accents au niveau du nom ou du prenom " + str(err)
                genre = datas[3].strip().decode('utf-8')
                # typeIdentite = sheet.cell_value(line, )

                sexe = ""
                if genre == "F":
                    sexe = "feminin"
                if genre == "H":
                    sexe = "masculin"

                #test type date
                #print nom
                nom_pers = nom
                #print prenoms

                #verification si date naissance approx
                date_naiss_appox = False
                date_naissance = None
                nevers = None
                print datas[5]
                print('apres date acte none')
                if datas[4].strip().decode('utf-8').upper() == 'OUI':
                    date_naiss_appox = True
                if date_naiss_appox:
                    date = self.traiter_date(datas[5].strip())
                    try:
                        nevers = date.strftime('%Y')
                    except Exception as err:
                        erreur = erreur + u" Erreur sur l'ecriture de la date de naissance : " + datas[5] +  str(err)
                    print nevers
                else:
                    date_naissance = self.traiter_date(datas[5].strip())
                    if date_naissance == None:
                        erreur = erreur + u"Erreur sur l'ecriture de la date de naissance ou date naissance vide : " + datas[5]
                print "date naissance"
                print date_naissance
                num_cin = None
                num_acte = None
                lieu_cin = None
                date_cin = None
                lieu_acte = None
                date_acte = None
                print "Datas de 9"
                print datas[9]
                if datas[7].strip().upper() == "CIN":
                    try:
                        num_cin = str(int(datas[8].replace(' ', ''))).strip()
                    except Exception as err:
                        erreur = "Erreur numero CIN : " + datas[8] + "Details : " + str(err) + "\n"

                    date_cin = self.traiter_date(datas[9].strip())
                    if date_cin == None:
                        erreur = "Erreur date CIN : " + str(datas[9]) + "\n"
                    lieu_cin = datas[10].strip().decode('utf-8')
                elif datas[7].upper().strip() == "ACTE_NAISSANCE":
                        try:
                            num_acte = str(int(datas[8])).strip()
                        except Exception as err:
                            erreur = "Erreur numero Acte de naissance " + str(datas[8]) + " \n"
                        date_acte = self.traiter_date(datas[9].strip())
                        if date_acte == None:
                            erreur = "Erreur date acte de naissance : " + str(datas[9]) + "\n"
                        lieu_acte = datas[10].strip().decode('utf-8')

                print "num_cin"
                print num_cin
                id_conjoint_xl = None
                adresse = datas[11].strip().decode('utf-8')
                #Traiter matrimoniale
                # etat_matri = sheet.cell_value(line, 35)
                sit_matri = 1
                if datas[12].strip().decode('utf-8').strip().lower() != "celibataire":
                    sit_matri = 1
                elif datas[12].strip().decode('utf-8').strip().lower() != "marié":
                    sit_matri = 2
                    id_conjoint_xl = datas[13].strip().decode('utf-8').strip()
                    #tokony misy fonction manao mise à jour idConjoint par personne
                elif datas[12].strip().decode('utf-8').strip().lower() != "veuf":
                    sit_matri = 3

                #print ("dans la boucle")
                # print(date_naissance)
                lieu_naissance = datas[6].strip().decode('utf-8')

                try:
                    nom_pere = datas[14].strip().decode('utf-8')
                    nom_mere = datas[15].strip().decode('utf-8')
                    adresse = datas[11].strip().decode('utf-8')
                except Exception as err:
                    print (err)
                    erreur = erreur + u"Erreur sur l'enocodage du fichiers CSV empechant la prise en charge des accents au niveau du nom des parents ou adresse" + str(err)



                # mariea = sheet.cell_value(line, 36)

                print "Adresse"
                print (adresse)
                print "Date CIN"
                #print datas[9]
                print(date_cin)

                cin_recto = datas[18].strip().encode('utf-8')
                nom_fic_cin_recto = None
                ext_cin_recto = None
                if cin_recto != '':
                    tab = cin_recto.replace('\\', '/').split('.')
                    ext_cin_recto = tab[len(tab) - 1]
                    tab_name_fic = tab[0].split('/')
                    nom_fic_cin_recto = tab_name_fic[len(tab_name_fic) - 1]
                    cin_rect = cin_recto.replace('\\', '/')
                    cin_recto = '/' + cin_rect

                cin_verso = datas[19].strip().encode('utf-8')
                nom_fic_cin_verso = None
                ext_cin_verso = None
                if cin_verso != '':
                    tab = cin_verso.replace('\\', '/').split('.')
                    ext_cin_verso = tab[len(tab) - 1]
                    tab_name_fic = tab[0].split('/')
                    nom_fic_cin_verso = tab_name_fic[len(tab_name_fic) - 1]
                    cin_vers = cin_verso.replace('\\', '/')
                    cin_verso = '/' + cin_vers

                nom_fic_signature = None
                ext_signature = None
                signature = datas[20].strip().encode('utf-8')
                if signature != '':
                    tab = signature.replace('\\', '/').split('.')
                    ext_signature = tab[len(tab) - 1]
                    tab_name_fic = tab[0].split('/')
                    nom_fic_signature = tab_name_fic[len(tab_name_fic) - 1]
                    # time.sleep(2)
                    signat = signature.replace('\\', '/')
                    signature = '/' + signat

                empreinte_d = datas[21].strip().encode('utf-8')
                empreinte_g = datas[22].strip().encode('utf-8')

                #Full path
                cin_recto_path = dir_path + cin_recto
                cin_verso_path = dir_path + cin_verso
                signature_path = dir_path + signature
                empreinte_d_path = dir_path + empreinte_d
                empreinte_g_path = dir_path + empreinte_g

                print "path defined"
                cin_recto_file, cin_verso_file, signature_file, empreinte_d_file, empreinte_g_file = None, None, None, None, None
                if cin_recto != '':
                    try:
                        cin_recto_file = open(cin_recto_path, 'rb').read()
                        print "Fichier cin1 ouvert"
                    except Exception as err:
                        print ("Erreur ouverture fichier" + err)
                if cin_verso != '':
                    try:
                        cin_verso_file = open(cin_verso_path, 'rb').read()
                        print "Fichier cin2 ouvert"
                    except Exception as err:
                        print ("Erreur ouverture fichier" + err)
                if signature != '':
                    try:
                        signature_file = open(signature_path, 'rb').read()
                        print "fichier signature ouvert"
                    except Exception as err:
                        print ("Erreur ouverture fichier" + err)
                if empreinte_d != '':
                    try:
                        empreinte_d_file = open(empreinte_d_path, 'rb').read()
                        print "Fichier empreinte ouvert"
                    except Exception as err:
                        print ("Erreur ouverture fichier" + err)
                if empreinte_g != '':
                    try:
                        empreinte_g_file = open(empreinte_g_path, 'rb').read()
                        print "Fichier empreinte 2 ouvert"
                    except Exception as err:
                        print ("Erreur ouverture fichier" + err)

                print ('tonga eto empreinte')
                # Insertion dans la base

                #Cas identité par cin cas mode correction
                #where = "csv_id = '" + str(idpers_xl) + "' and numcipersonne = '" + str(num_cin) + "'"
                where = "csv_id = '" + str(idpers_xl) + "'"
                idpersonne_to_update = self.select("personne", "idpersonne", where)
                if idpersonne_to_update is not None:
                    """if self.exists("personne", "csv_id", idpers_xl):
                    self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
                                          "Personne %s existe deja en base" % (idpers_xl), "orange")"""
                    #MANAO UPDATE
                    try:
                        cursor = self.connection.cursor()
                        cursor.execute ('UPDATE personne SET nompersonne = %s, prenompersonne = %s, sexepersonne = %s, '
                                            'datenaissancepersonne = %s, nevers = %s, lieunaissancepersonne = %s, numcipersonne =%s ,'
                                            'datecipersonne = %s , lieucipersonne = %s, numactenaissancepersonne = %s, '
                                            'dateactenaissancepersonne = %s,lieuactenaissancepersonne = %s, adressepersonne = %s, situationmatrimoniale = %s,'
                                            'nompere = %s, nommere = %s WHERE idpersonne = %s returning idpersonne',
                                            (nom, prenoms, sexe, date_naissance, nevers,lieu_naissance, num_cin, date_cin, lieu_cin,
                                             num_acte, date_acte,lieu_acte, adresse, sit_matri, nom_pere,
                                             nom_mere, idpersonne_to_update))
                        self.connection.commit()
                        etatInsertion = "MODIFICATION REUSSI"
                        res = cursor.fetchone()
                        if res is not None:
                            if self.exists("blob_personne", "idpersonne", str(res[0])):
                                self.insertBlobFiles(idpersonne=str(res[0]), cin_recto=cin_recto_file,
                                                     cin_verso=cin_verso_file, signature=signature_file,
                                                     edit_mode=1, ext_signature=ext_signature,
                                                     ext_cin_recto=ext_cin_recto, ext_cin_verso=ext_cin_verso,
                                                     nom_signature=nom_fic_signature,
                                                     nom_cin_recto=nom_fic_cin_recto,
                                                     nom_cin_verso=nom_fic_cin_verso)
                            else:
                                self.insertBlobFiles(idpersonne=str(res[0]), cin_recto=cin_recto_file,
                                                     cin_verso=cin_verso_file, signature=signature_file, edit_mode=0,
                                                     ext_signature=ext_signature, ext_cin_recto=ext_cin_recto,
                                                     ext_cin_verso=ext_cin_verso, nom_signature=nom_fic_signature,
                                                     nom_cin_recto=nom_fic_cin_recto, nom_cin_verso=nom_fic_cin_verso)
                        #self.insertBlobFiles(res[0], cin_recto_file, cin_verso_file, signature_file, empreinte_d_file, empreinte_g_file, 1)

                        self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
                                      u"Personne %s insérée dans la base" % (str(nom)), "green")
                    except Exception as err:
                        print(err)
                        self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, str(err), "red")
                        etatInsertion = "ECHEC DE MODIFICATION"
                        erreur = erreur + str(err)
                        self.connection.rollback()

                else:
                    try:
                        cursor = self.connection.cursor()
                        cursor.execute ('INSERT INTO personne (nompersonne, prenompersonne, sexepersonne, '
                                            'datenaissancepersonne, nevers, lieunaissancepersonne, numcipersonne,'
                                            'datecipersonne, lieucipersonne, numactenaissancepersonne, '
                                            'dateactenaissancepersonne,lieuactenaissancepersonne, adressepersonne, situationmatrimoniale,'
                                            'nompere, nommere, csv_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) returning idpersonne',
                                            (nom, prenoms, sexe, date_naissance, nevers,lieu_naissance, num_cin, date_cin, lieu_cin,
                                             num_acte, date_acte,lieu_acte, adresse, sit_matri, nom_pere,
                                             nom_mere, idpers_xl))
                        self.connection.commit()
                        etatInsertion = "INSERTION REUSSI"
                        res = cursor.fetchone()
                        if res is not None:
                            if self.exists("blob_personne", "idpersonne", str(res[0])):
                                self.insertBlobFiles(idpersonne=str(res[0]), cin_recto=cin_recto_file,
                                                     cin_verso=cin_verso_file, signature=signature_file,
                                                     edit_mode=1, ext_signature=ext_signature,
                                                     ext_cin_recto=ext_cin_recto, ext_cin_verso=ext_cin_verso,
                                                     nom_signature=nom_fic_signature,
                                                     nom_cin_recto=nom_fic_cin_recto,
                                                     nom_cin_verso=nom_fic_cin_verso)
                            else:
                                self.insertBlobFiles(idpersonne=str(res[0]), cin_recto=cin_recto_file,
                                                     cin_verso=cin_verso_file, signature=signature_file, edit_mode=0,
                                                     ext_signature=ext_signature, ext_cin_recto=ext_cin_recto,
                                                     ext_cin_verso=ext_cin_verso, nom_signature=nom_fic_signature,
                                                     nom_cin_recto=nom_fic_cin_recto, nom_cin_verso=nom_fic_cin_verso)
                        #self.insertBlobFiles(res[0], cin_recto_file, cin_verso_file, signature_file, empreinte_d_file, empreinte_g_file, 0)

                        self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
                                      u"Personne %s insérée dans la base" % (str(nom)), "green")
                    except psycopg2.Error as err:
                        print(err)
                        self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, str(err), "red")
                        self.connection.rollback()
                        if err.pgcode == "23505":
                            try:
                                cursor = self.connection.cursor()
                                cursor.execute(
                                    "SELECT idpersonne, COALESCE(nompersonne, ''), COALESCE(prenompersonne, ''), COALESCE(csv_id,'') FROM personne "
                                    "WHERE TRIM(numcipersonne) =%s",
                                    ( str(num_cin).strip(),))
                                #self.connection.commit()
                                res = cursor.fetchone()
                                if res is not None:
                                    etatInsertion = etatInsertion + u"Numero CIN déjà existant en base de données au nom de : "  + str(res[1]).strip() + " " + str(res[2]).strip() + " dont l'identifiant dans le CSV est " + str(res[3]).strip()
                                    csv_id_en_double = []
                                    csv_id_en_double.append(idpers_xl)
                                    csv_id_en_double.append(str(num_cin).strip())
                                    self.dataOccupantToRepair.append(csv_id_en_double)
                            except Exception as errr:
                                print errr
                                self.connection.rollback()

                        etatInsertion = etatInsertion + "\nECHEC INSERTION"
                        erreur = erreur + str(err)

                dataToLog.append(
                        {"idxl_personne": idxpers, "nom": nom_pers, "etat_insertion": etatInsertion,
                         "erreur": erreur})


            p = (line + 1) * 100 / total_lignes
            self.emit(SIGNAL("progress(int)"), p)
            line = line + 1

        self.logger.addSheet(title=title, data=dataToLog, sheet_name="Log Import Personne")

    def insertBlobFiles(self, idpersonne, cin_recto = None, cin_verso = None, signature = None, empreinte_d = None, empreinte_g = None, edit_mode = 0, ext_signature = None, ext_cin_recto = None, ext_cin_verso = None, nom_signature = None, nom_cin_recto = None, nom_cin_verso = None):
        print "INSERT BLOB FILES"
        cur = self.connection.cursor()
        if edit_mode == 0:
            try:
                cur.execute('INSERT INTO blob_personne (idpersonne,cin_recto , cin_verso, signature, empreinte_d, empreinte_g, '
                            'signature_type, cin_recto_type, cin_verso_type, signature_name, cin_recto_name, cin_verso_name ) '
                            'VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s) ',
                            (idpersonne, psycopg2.Binary(cin_recto), psycopg2.Binary(cin_verso),psycopg2.Binary(signature),
                             psycopg2.Binary(empreinte_d), psycopg2.Binary(empreinte_g), ext_signature, ext_cin_recto, ext_cin_verso,
                             nom_signature, nom_cin_recto, nom_cin_verso))
                self.connection.commit()
                print "INSERTION REUISSI"

            except Exception as err:
                print err

                self.connection.rollback()
        else:
            try:
                cur.execute(
                    'UPDATE blob_personne SET cin_recto = %s , cin_verso = %s, signature = %s, empreinte_d = %s, empreinte_g = %s, '
                    'signature_type = %s, cin_recto_type = %s, cin_verso_type = %s, signature_name = %s, cin_recto_name = %s, cin_verso_name = %s '
                    ' where idpersonne = %s',
                    ( psycopg2.Binary(cin_recto), psycopg2.Binary(cin_verso), psycopg2.Binary(signature),
                     psycopg2.Binary(empreinte_d), psycopg2.Binary(empreinte_g), ext_signature, ext_cin_recto,
                     ext_cin_verso,
                     nom_signature, nom_cin_recto, nom_cin_verso, idpersonne))
                self.connection.commit()
                print "MODIFICATION REUSSIE"

            except Exception as err:
                print err

                self.connection.rollback()

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
            csv_inventaire_file = open(self.filenames['parcelle'], 'rb')
            csv_inventaire = csv.reader(csv_inventaire_file, dialect='excel')

        except Exception as err:
            print ("Erreur:" + err)

        total_lignes = self.lenCsv(csv_inventaire)

        csv_inventaire_file.seek(0)

        line = 0
        cptDemande = self.getCptDemande()
        codesLoc = self.getCodesLoc()
        print "code localites"
        print codesLoc
        codeGuichet = str(codesLoc[1]).strip()
        codeDistrict = str(codesLoc[0]).strip()
        if len(codeGuichet) == 1:
            codeGuichet = '0' + codeGuichet

        dep = codeDistrict + '-' + codeGuichet + '-F-'
        print "dep"
        print dep
        print "dep"

        for data in csv_inventaire:
            if line > 0:
                etatInsertion, erreur, numDmd = '', '', ''
                numdemande = None
                datas = str(data[0]).split(";")
                print datas

                #INSERTION DES DEMANDES
                codeparcelle = datas[12].strip()
                print('codeParcelle == ' + codeparcelle)
                idParcelle = self.getIdParcelle(codeparcelle)
                #numdemande = str(sh_demande.cell_value(line, 20)).strip()
                dateinventaire = self.traiter_date(datas[13].strip())
                sujetDemande = False
                if datas[14].strip().upper() == "TRUE":
                    sujetDemande = True
                datedemande = self.traiter_date(datas[15].strip())
                if datedemande is None:
                    erreur = erreur + u"Erreur sur la date demande ou date demande non renseignée: " + str(datas[15]) + "\n"
                region = datas[0].strip()
                district = datas[1].strip()
                commune = datas[2].strip()
                fokontany = datas[3].strip()
                hameau = datas[4].strip()
                secteur = datas[5].strip()
                consistance = datas[18].strip()

                categorie = datas[17].strip()

                #Recuperation des voisins
                voisins = {}
                try:
                    voisins['est'] = datas[19].strip().decode('utf-8')
                    voisins['ouest'] = datas[20].strip().decode('utf-8')
                    voisins['nord'] = datas[21].strip().decode('utf-8')
                    voisins['sud'] = datas[22].strip().decode('utf-8')
                except Exception as err:
                    print (err)
                    erreur = erreur + u"Erreur sur l'enocodage du fichiers CSV empechant la prise en charge des accents au niveau des voisins " + str(err)



                codeCommune = datas[8].strip()
                codeFkt = datas[9].strip()
                codeHameau = datas[10].strip()

                #idCommune = self.getIdCommune(codeCommune)
                idCommune = globalvars.id_commune
                user_import = globalvars.id_user
                dateImport = datetime.now().date()

                id_fokontany = self.getidFkt(codeFkt=codeFkt, idcommune=idCommune)

                idHameau = self.getIdHameau(codeHameau, id_fokontany)

                print ('id_hameau=')
                print(idHameau)

                print ('idParcelle = ')
                print (idParcelle)
                #Recup idhameau + idcommune + idfokontany

                #Recup demandeur

                if idParcelle is not None:
                    if sujetDemande == True:
                        numdemande = dep + str(cptDemande)
                        print "numero demande = "
                        print numdemande
                        numDmd = numdemande
                        print "numero demande fin"
                        #update de la table parcelle_d
                    try:
                        cursor = self.connection.cursor()
                        cursor.execute('UPDATE parcelle_d SET region = %s, district = %s, commune = %s, id_commune = %s, idhameau = %s, consistance = %s, categorie = %s, date_inventaire = %s, sujet_demande = %s, '
                                       'user_import_inv = %s, date_import_inv = %s, inventaire = True, ref_import = %s '
                                           ' WHERE gid = %s',(region, district, commune, idCommune, idHameau, consistance, categorie, dateinventaire, sujetDemande, user_import, dateImport, self.refimport, idParcelle ))
                        self.connection.commit()

                    except Exception as err:
                        print(err)
                        self.connection.rollback()
                    #Insertion de la demande

                    if sujetDemande == True:
                        print ("su")
                        if self.exists("demande","gid",idParcelle):
                            num_dm = self.select("demande", "numdemande","gid = " + str(idParcelle))
                            if num_dm is not None:
                                numDmd = str(num_dm).strip()
                            try:
                                cursor = self.connection.cursor()
                                cursor.execute('UPDATE demande SET numdemande = %s, gid = %s, '
                                               'datedemande = %s, region = %s, '
                                               'district = %s, idfokontany = %s, idcommune = %s, cout = %s, consistance = %s,'
                                               'idprojet = %s, categorie = %s WHERE  code_parcelle = %s and numdemande IS NULL'
                                               ' returning gid',
                                               (numdemande, idParcelle, datedemande, region, district,
                                                id_fokontany, idCommune, 0, consistance, globalvars.id_projet,
                                                categorie, codeparcelle))
                                self.connection.commit()
                                print ("MISE A JOUR DEMANDE REUSSI")
                                etatInsertion = "MISE A JOUR DEMANDE REUSSI"
                                res = cursor.fetchone()
                                if res is not None:

                                    self.updateNumDmdParcelle(numdemande, res[0])

                                    cptDemande = cptDemande + 1
                                    self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
                                              u"Demande %s insérée dans la base" % (str(numdemande)), "green")

                            except Exception as err:
                                print (err)
                                self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, str(err),
                                          "red")
                                self.connection.rollback()
                                etatInsertion = "ECHEC MISE A JOUR DEMANDE "
                                erreur = erreur + str(err) + "\n"
                        else:
                            try:
                                cursor = self.connection.cursor()
                                cursor.execute('INSERT INTO demande (numdemande, gid, '
                                                   'datedemande, region, '
                                                   'district, idfokontany, idcommune, cout, consistance,'
                                                   'idprojet, categorie, code_parcelle) '
                                                   'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning gid',
                                                   (numdemande, idParcelle, datedemande, region, district,
                                                    id_fokontany, idCommune, 0, consistance, globalvars.id_projet, categorie, codeparcelle))
                                self.connection.commit()
                                print ("INSERTION DEMANDE REUSSI")
                                etatInsertion = "INSERTION DEMANDE REUSSI"
                                res = cursor.fetchone()

                                if res is not None:
                                    self.updateNumDmdParcelle(numdemande, res[0])

                                    cptDemande = cptDemande + 1
                                    self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
                                                  u"Demande %s insérée dans la base" % (str(numdemande)), "green")

                            except Exception as err:
                                print (err)
                                self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, str(err), "red")
                                self.connection.rollback()
                                etatInsertion = "ECHEC D'INSERTION DEMANDE "
                                erreur = erreur + str(err)
                        #insertion du proprietaire principale


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
                                    (val, str(idpoint), idParcelle))
                            else:
                                cursor.execute('INSERT INTO limitesparcelle(idpointscardinaux, idparcelle,description) '
                                               'VALUES(%s, %s, %s)', (str(idpoint), idParcelle, val))
                            self.connection.commit()
                        except Exception as err:
                            print (err)
                            self.connection.rollback()

                else:
                    print ("idParcelle is None")


                dataToLog.append(
                {"code_parcelle": codeparcelle, "numero_demande": numDmd, "etat_insertion": etatInsertion,
                 "erreur": erreur})

            p = (line + 1) * 100 / total_lignes
            self.emit(SIGNAL("progress(int)"), p)
            line = line + 1

        self.updateCptDemande()
        cptImport = self.getCptImport()
        self.updateCptImport(cptImport)
        self.logger.addSheet(title=title, data=dataToLog, sheet_name="Log Import Demande")

    def importOccupants(self):
        # Preparation log
        title = ["code_parcelle", "idpers_xl", "etat_insertion", "erreur"]
        dataToLog = []

        self.current_step = self.current_step + 1
        self.emit(SIGNAL("clearSubstep(int)"), self.current_step)
        cursor = self.connection.cursor()
        print ("IMPORT OOCUPANTS")
        self.emit(SIGNAL("clearSubstep(int)"), self.current_step)
        print ("signal")
        try:
            csv_occupant_file = open(self.filenames['occupant'], 'rb')
            csv_occupant = csv.reader(csv_occupant_file, dialect='excel')
        except Exception as err:
            print (err)

        total_lignes = self.lenCsv(csv_occupant)

        csv_occupant_file.seek(0)

        line = 0  # lignes
        for data in csv_occupant:
            if line > 0:
                etatInsertion, erreur = '', ''
                datas = str(data[0]).split(";")
                print datas

                codeParcelle = datas[0].strip()
                id_pes_xl = datas[1].strip()
                representant = True
                if datas[2].strip().upper() == "TRUE":
                    representant = True
                if datas[2].strip().upper() == "FALSE":
                    representant = True

                idParcelle = self.getIdParcelle(codeParcelle)
                print 'id_demande'
                id_demande = self.getIdDemande(codeParcelle)
                print id_demande
                idpersonne = self.getIdPersonne(id_pes_xl)

                print ('idparcelle')
                print (idParcelle)
                print ('id_demande')
                print (id_demande)
                print ('id_personne')
                print (idpersonne)

                for occ in self.dataOccupantToRepair:
                    """print "********************************************contenu occ par boucle****************************************************"
                    print occ"""
                    if str(occ[0]).strip() == id_pes_xl:
                        where = "numcipersonne = '" + str(occ[1]) + "'"
                        idpersonne = self.select("personne", "idpersonne", where)
                        idParcelle = self.getIdParcelle(codeParcelle)

                if id_demande is not None and idpersonne is not None and idParcelle is not None:
                    where = "idparcelle = '" + str(idParcelle) + "' and idpersonne = " + str(
                        idpersonne)
                    if self.select("avoir_demande", "iddemande", where) is not None:
                        try:
                            cursor = self.connection.cursor()
                            cursor.execute(
                                'DELETE FROM avoir_demande WHERE idparcelle = %s AND idpersonne = %s'
                                (idParcelle, idpersonne))
                            self.connection.commit()
                        except Exception as err:
                            print (err)
                            self.connection.rollback()

                    try:
                        cursor = self.connection.cursor()
                        cursor.execute('INSERT INTO avoir_demande(idparcelle, iddemande, idpersonne, representant) '
                                       'VALUES(%s, %s, %s, %s)',(idParcelle, id_demande, idpersonne, representant))
                        self.connection.commit()
                        etatInsertion = "INSERTION OCCUPANT REUSSI"
                    except psycopg2.Error as err:
                        etatInsertion = "ERREUR INSERTION OCCUPANT"
                        erreur = str(err)
                        print (err)
                        if err.pgcode == "23505":
                            self.connection.rollback()
                            self.updateAVD(idParcelle, id_demande, idpersonne, representant)
                        else:
                            self.connection.rollback()
                dataToLog.append(
                    {"code_parcelle": codeParcelle, "idpers_xl": str(id_pes_xl), "etat_insertion": etatInsertion,
                     "erreur": erreur})

                dataToLog.append(
                    {"code_parcelle": codeParcelle, "idpers_xl": str(id_pes_xl), "etat_insertion": etatInsertion,
                     "erreur": erreur})

                #### Cas ou deja transformé en CF
                if id_demande is not None and idpersonne is not None and idParcelle is not None:
                    where = "gid = '" + str(idParcelle) + "'"
                    if self.select("parcelle_d", "idcertificat", where) is not None:
                        try:
                            cursor = self.connection.cursor()
                            cursor.execute(
                                'DELETE FROM proprietaireparcelle WHERE idparcelle = %s AND idpersonne = %s'
                                (idParcelle, idpersonne))
                            self.connection.commit()
                        except Exception as err:
                            print (err)
                            self.connection.rollback()

                        try:
                            cursor = self.connection.cursor()
                            cursor.execute('INSERT INTO proprietaireparcelle(idparcelle, idpersonne, representant) '
                                           'VALUES(%s, %s, %s)',(idParcelle, idpersonne, representant))
                            self.connection.commit()
                            etatInsertion = "INSERTION PROPRIETAIRE REUSSI"
                        except psycopg2.Error as err:
                            etatInsertion = "ERREUR INSERTION PROPRIETAIRE"
                            erreur = str(err)
                            print (err)
                            if err.pgcode == "23505":
                                self.connection.rollback()
                                #self.updateAVD(idParcelle, id_demande, idpersonne, representant)
                            else:
                                self.connection.rollback()
                        dataToLog.append(
                            {"code_parcelle": codeParcelle, "idpers_xl": str(id_pes_xl), "etat_insertion": etatInsertion,
                            "erreur": erreur})

            p = (line + 1) * 100 / total_lignes
            self.emit(SIGNAL("progress(int)"), p)
            line = line + 1
        self.logger.addSheet(title=title, data=dataToLog, sheet_name="Log Import Occupant")

    def updateAVD(self, idParcelle, id_demande, idpersonne, representant):
        print "CALL OF UPDATE AVD"
        try:
            cursors = self.connection.cursor()
            cursors.execute('UPDATE avoir_demande SET iddemande = %s, representant = %s WHERE idparcelle = %s AND  idpersonne = %s'
                           , (id_demande, representant, idParcelle, idpersonne ))
            self.connection.commit()
            print "Modification ok"
        except Exception as err:
            print (err)
            self.connection.rollback()

    def importLocalite(self):
        # Preparation log
        title = ["nom_hameau", "nom_fokontany", "etat_insertion", "erreur"]
        dataToLog = []

        self.current_step = self.current_step + 1
        self.emit(SIGNAL("clearSubstep(int)"), self.current_step)
        cursor = self.connection.cursor()
        print ("IMPORT LOCALITES")
        self.emit(SIGNAL("clearSubstep(int)"), self.current_step)
        print ("signal")
        try:
            csv_localite_file = open(self.filenames['localite'], 'rb')
            fieldNames = ['Hameau','CodeHameau','Fokontany', 'CodeFokontany', 'Commune', 'CodeCommune','CodeGuichet']
            csv_localite = csv.reader(csv_localite_file,dialect='excel')
        except Exception as err:
            print ("Erreur:" + err)

        total_lignes = self.lenCsv(csv_localite)

        csv_localite_file.seek(0)

        line = 0
        for data in csv_localite:
            if line > 0:
                datas = str(data[0]).split(";")
                print datas
                nomHameau = datas[0].strip()
                codeHameau = datas[1].strip()
                nomFokontany = datas[2].strip()
                codeFokontany = datas[3].strip()
                nomCommune = datas[4].strip()
                codeCommune = datas[5].strip()
                codeGuichet = datas[6].strip()
                # INSERT FOKONTANY

                self.insertFkt(nomFkt=nomFokontany,
                                   codeFkt=codeFokontany, id_commune=globalvars.id_commune)

                # INSERT HAMEAU
                #get Id fokontany
                idFkt = self.getidFkt(codeFkt=codeFokontany,
                                          idcommune=globalvars.id_commune)
                if idFkt is not None:
                    self.insertHameau(nomHameau=nomHameau,
                                        codeHameau=codeHameau, id_fokontany=idFkt)

            p = (line + 1) * 100 / total_lignes
            self.emit(SIGNAL("progress(int)"), p)
            line = line + 1



    def insertFkt(self, nomFkt, codeFkt, id_commune):
        cur = self.connection.cursor()
        try:
            cur.execute("INSERT INTO fokontany (codefokontany, nomfokontany, idcommune) "
                        "VALUES (%s, %s,%s)", (codeFkt, nomFkt, id_commune))
            self.connection.commit()
        except Exception as err:
            print (err)
            self.connection.rollback()
        cur.close()

    def insertHameau(self, nomHameau, codeHameau, id_fokontany):
        cur = self.connection.cursor()
        try:
            cur.execute("INSERT INTO hameau (codehameau, nomhameau, idfokontany) "
                        "VALUES (%s, %s,%s)", (codeHameau, nomHameau, id_fokontany))
            self.connection.commit()
        except Exception as err:
            print (err)
            self.connection.rollback()
        cur.close()

    def checkCodeHamExists(self, codeHam, codeFokontany):
        cur = self.connection.cursor()
        ref = ""
        exists = False
        try:
            cur.execute("SELECT ham.codehameau, fkt.codefokontany FROM hameau ham INNER JOIN fokontany fkt ON "
                        "ham.idfokontany = fkt.idfokontany")
            res = cur.fetchall()
            for val in res:
                if len(str(val[1]).strip()) == 2:
                    if len (codeFokontany) == 1:
                        codeFokontany = "0" + codeFokontany
                ref = codeHam + codeFokontany
                ref_base = str(val[0]).strip() + str(val[1]).strip()
                if ref_base == ref:
                    exists =  True
        except Exception as err:
            print (err)
            self.connection.rollback()
        cur.close()
        return exists

    def checkCodeFktExists(self, codeFkt, codeCommune):
        print "call of checkCodeFkt"
        cur = self.connection.cursor()
        ref = codeFkt
        exists = False
        try:
            cur.execute(
                    "SELECT fkt.codefokontany FROM fokontany fkt WHERE fkt.idcommune = %s",(globalvars.id_commune,))
            res = cur.fetchall()
            print res
            for val in res:
                print str(val[0]).strip()
                print ref
                if str(val[0]).strip() == ref:
                    exists =  True
        except Exception as err:
            print (err)
            self.connection.rollback()
        cur.close()
        return exists

        # iteration sur les feuilles



    def traiter_date(self,str_date):
        temp_tab = str_date.split('-')
        if len(temp_tab) > 1:
            try:
                date = datetime.strptime(str_date, "%Y-%m-%d")
                return date.date()
            except Exception as err:
                print (err)
                return None
        temp_tab1 = str_date.split('/')
        if len(temp_tab1) > 1:
            try:
                date = datetime.strptime(str_date, "%d/%m/%Y")
                return date.date()
            except Exception as err:
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
            fileDirPath = str(self.filenames.toUtf8()).decode('utf-8')
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

    def lenCsv(self, csvFile):
        nbLines = 0
        for data in csvFile:
            nbLines = nbLines + 1

        return nbLines

    def readByteA(self, idpersonne):
        cur = self.connection.cursor()
        try:
            cur.execute("SELECT cin_recto::bytea , cin_verso::bytea, signature::bytea, empreinte_d::bytea, empreinte_g::bytea FROM blob_personne WHERE idpersonne = %s ",
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
            file_cin_recto = colon[0]
            file_cin_verso = colon[1]
            file_signature = colon[2]
            file_empreinte_d = colon[3]
            file_empreinte_g = colon[4]
            print("Stocker le fichier sur le disque \n")
            path1 = os.path.join(tempfile.gettempdir(), "temp_cin1" + ".jpg")
            path2 = os.path.join(tempfile.gettempdir(), "temp_cin2" + ".jpg")
            path3 = os.path.join(tempfile.gettempdir(), "temp_sign" + ".jpg")
            path4 = os.path.join(tempfile.gettempdir(), "temp_emp_d" + ".jpg")
            path5 = os.path.join(tempfile.gettempdir(), "temp_emp_g" + ".jpg")

        # Convertir les donnees binaires au format
        # approprie et les ecrire sur le disque dur
        if path1 is not None:
            try:
                with open(path1, 'wb') as myfile:
                    myfile.write(file_cin_recto)
                print("Le fichier stockees dans: ", path1, "\n")
            except Exception as err:
                print (err)
        if path2 is not None:
            try:
                with open(path2, 'wb') as myfile:
                    myfile.write(file_cin_verso)
                print("Le fichier stockees dans: ", path2, "\n")
            except Exception as err:
                print (err)
        if path3 is not None:
            try:
                with open(path3, 'wb') as myfile:
                    myfile.write(file_signature)
                print("Le fichier stockees dans: ", path3, "\n")
            except Exception as err:
                print (err)
        if path4 is not None:
            with open(path4, 'wb') as myfile:
                myfile.write(file_empreinte_d)
            print("Le fichier stockees dans: ", path4, "\n")
        if path5 is not None:
            try:
                with open(path5, 'wb') as myfile:
                    myfile.write(file_empreinte_g)
                print("Le fichier stockees dans: ", path5, "\n")
            except Exception as err:
                print (err)

        # fermeture de la connexion à la base de données
        cur.close()

    def readByteAData(self, idpersonne):
        print "READ BYTE ARRAY DATA"
        db = QtSql.QSqlDatabase.addDatabase('QPSQL')
        db.setHostName('localhost')
        db.setPort(5432)
        db.setDatabaseName("test_import_inventaire_4")

        print "config vita"
        path1 = None
        path2 = None
        path3 = None
        path4 = None
        path5 = None
        if db.open("postgres", "postgres"):
            print ("db opened")
            query = QtSql.QSqlQuery()
            print "Query initiated"
            query.prepare("SELECT cin_recto::bytea , cin_verso::bytea, signature::bytea, empreinte_d::bytea, empreinte_g::bytea FROM blob_personne WHERE idpersonne = :idpersonne ")
            query.bindValue(":idpersonne", idpersonne)
            print "Query prepared"
            query.exec_()
            print "Query executed"
            path1 = None
            path2 = None
            path3 = None
            path4 = None
            path5 = None
            while query.next():
                print "Query result"
                file_cin_recto = query.value(0)
                print "cin 2"
                file_cin_verso = query.value(1).toByteArray()
                print "signature"
                file_signature = query.value(2).toByteArray()
                print "empreinte 1"
                file_empreinte_d = query.value(3).toByteArray()
                print "empreinte 2"
                file_empreinte_g =  query.value(4).toByteArray()

                print("Stocker le fichier sur le disque \n")
                path1 = os.path.join(tempfile.gettempdir(), "tmp_cin1" + ".jpg")
                path2 = os.path.join(tempfile.gettempdir(), "tmp_cin2" + ".jpg")
                path3 = os.path.join(tempfile.gettempdir(), "tmp_sign" + ".jpg")
                path4 = os.path.join(tempfile.gettempdir(), "tmp_emp_d" + ".jpg")
                path5 = os.path.join(tempfile.gettempdir(), "tmp_emp_g" + ".jpg")


            #Ecrirure des fichiers
            if path1 is not None:
                try:
                    with open(path1, 'wb') as myfile:
                        myfile.write(file_cin_recto)
                    print("Le fichier stockees dans: ", path1, "\n")
                except Exception as err:
                    print (err)
            if path2 is not None:
                try:
                    with open(path2, 'wb') as myfile1:
                        myfile1.write(file_cin_verso)
                    print("Le fichier stockees dans: ", path2, "\n")
                except Exception as err:
                    print (err)
            if path3 is not None:
                try:
                    with open(path3, 'wb') as myfile2:
                        myfile2.write(file_signature)
                    print("Le fichier stockees dans: ", path3, "\n")
                except Exception as err:
                    print (err)
            if path4 is not None:
                with open(path4, 'wb') as myfile3:
                    myfile3.write(file_empreinte_d)
                print("Le fichier stockees dans: ", path4, "\n")
            if path5 is not None:
                try:
                    with open(path5, 'wb') as myfile4:
                        myfile4.write(file_empreinte_g)
                    print("Le fichier stockees dans: ", path5, "\n")
                except Exception as err:
                    print (err)

            db.close()
