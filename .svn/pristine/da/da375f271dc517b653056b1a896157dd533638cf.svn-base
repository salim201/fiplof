# coding: utf8
from PyQt4.QtCore import QThread, SIGNAL, QVariant
from PyQt4.QtGui import QMessageBox
from osgeo import gdal, ogr
from PyQt4 import QtSql
#import ogrinfo
import sys
import zlib
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
import qgis
from qgis.core import *
#from Congiguration import DbConfig
from logs import xlsLogger

from PyQt4 import QtCore, QtGui

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


class ImportImageThread(QThread):
    def __init__(self, filenames, connection, steps = None):
        QThread.__init__(self)
        self.filenames, self.connection = filenames, connection
        self.current_step =-1
        self.steps = steps
        self.logger = xlsLogger.xlsLogger("Import_Photo")
        self.idpersonne, self.etatInsertion, self.erreur = '','',''
        self.codeparcelle_precedente= ""
        self.codeparcelle_actuelle = ""
        #self.db_config = DbConfig.DbConfig()

    def __del__(self):
        self.wait()

    def run(self):
        #print (self.filename)
        for filename in self.filenames.values():
            if filename == "":
                self.emit(SIGNAL("alert(QString)"), "Veuillez choisir un dossier")
                return

        for step in self.steps:
            if str(step).strip() == u"Identites des demandeurs":
                #IMPORT listing
                self.emit(SIGNAL("stepInit(int)"), self.current_step + 1)
                print("Debut import Identite")
                self.importIdentitePersonne()
                print("Fin import Identite")
                if str(step).strip() == str(self.steps[len(self.steps) - 1]).strip():
                    pass
                    #self.logger.write()
                self.emit(SIGNAL("stepDone(int)"), self.current_step)
                #FIN IMPORT Listing
            if str(step).strip() == u"Signature des voisins":
                # IMPORT shapefile
                self.emit(SIGNAL("stepInit(int)"), self.current_step + 1)
                print("Debut import signature voisins")
                self.importSignatureVoisins()
                print("Fin import signature voisins")
                if str(step).strip() == str(self.steps[len(self.steps) - 1]).strip():
                    pass
                    #self.logger.write()
                self.emit(SIGNAL("stepDone(int)"), self.current_step)
                # FIN IMPORT LOCALITES

    def importIdentitePersonne(self):
        print (self.filenames['images'])
        dataToLog = []
        cur = self.connection.cursor()
        try:
            cur.execute("SELECT idpersonne, cin_recto, cin_verso, signature FROM path_personne")
            res = cur.fetchall()
            if res is not None:
                self.prepare_blob_personne(res)
        except Exception as err:
            print ('erreur lecture path_personne ' + str(err))
            self.connection.rollback()

    def prepare_blob_personne(self, data):
        title = ["id_personne", "etat_insertion", "erreur"]
        print ('data personne')
        print data
        dataToLog = []
        self.current_step = self.current_step + 1
        self.emit(SIGNAL("clearSubstep(int)"), self.current_step)

        total = len(data)
        line = 0
        for val in data:
            # Lecture signature
            nom_fic_signature = None
            ext_signature = None
            signature = ''
            if val[3] is not None:
                signature = str(val[3]).decode('utf-8').strip()
                tab = signature.replace('\\', '/').split('.')
                if len(tab) > 1:
                    ext_signature = tab[len(tab) - 1]
                tab_name_fic = tab[0].split('/')
                nom_fic_signature = tab_name_fic[len(tab_name_fic) - 1]
                # time.sleep(2)
                signat = signature.replace('\\', '/')
                signature = '/' + signat

            nom_fic_cin_recto = None
            ext_cin_recto = None
            cin_recto = ''
            if val[1] is not None:
                cin_recto = str(val[1]).decode('utf-8').strip()
                tab = cin_recto.replace('\\', '/').split('.')
                if len(tab) > 1:
                    ext_cin_recto = tab[len(tab) - 1]
                tab_name_fic = tab[0].split('/')
                nom_fic_cin_recto = tab_name_fic[len(tab_name_fic) - 1]
                cin_rect = cin_recto.replace('\\', '/')
                cin_recto = '/' + cin_rect

            nom_fic_cin_verso = None
            cin_verso = ''
            ext_cin_verso = None
            if val[2] is not None:
                cin_verso = str(val[2]).decode('utf-8').strip()
                tab = cin_verso.replace('\\', '/').split('.')
                if len(tab) > 1:
                    ext_cin_verso = tab[len(tab) - 1]
                tab_name_fic = tab[0].split('/')
                nom_fic_cin_verso = tab_name_fic[len(tab_name_fic) - 1]
                cin_vers = cin_verso.replace('\\', '/')
                cin_verso = '/' + cin_vers

            print cin_recto

            print cin_verso

            # Full path

            signature_path = str(self.filenames['images']).replace('\\', '/') + signature
            cin_recto_path = str(self.filenames['images']).replace('\\', '/') + cin_recto
            cin_verso_path = str(self.filenames['images']).replace('\\', '/') + cin_verso

            print "path defined"
            print signature_path
            signature_file = None
            cin_recto_file = None
            cin_verso_file = None
            if signature != '' and os.path.isfile(signature_path):
                try:
                    signature_file = open(signature_path, 'rb').read()
                    print "fichier signature ouvert"
                except Exception as err:
                    print ("Erreur ouverture fichier signature" + err)

            if cin_recto != '' and os.path.isfile(cin_recto_path):
                try:
                    cin_recto_file = open(cin_recto_path, 'rb').read()
                    print "fichier cin_recto ouvert"
                except Exception as err:
                    print ("Erreur ouverture fichier cin recto" + err)

            if cin_verso != '' and os.path.isfile(cin_verso_path):
                try:
                    cin_verso_file = open(cin_verso_path, 'rb').read()
                    print "fichier cin_verso ouvert"
                except Exception as err:
                    print ("Erreur ouverture fichier cin verso" + err)

            if signature_file is not None or cin_recto_file is not None or cin_verso_file is not None:
                if self.exists("blob_personne", "idpersonne", str(val[0])):
                    self.insertBlobFiles(idpersonne=val[0], cin_recto=cin_recto_file,
                                         cin_verso=cin_verso_file, signature=signature_file,
                                         edit_mode=1, ext_signature=ext_signature,
                                         ext_cin_recto=ext_cin_recto, ext_cin_verso=ext_cin_verso,
                                         nom_signature=nom_fic_signature,
                                         nom_cin_recto=nom_fic_cin_recto,
                                         nom_cin_verso=nom_fic_cin_verso)
                    # self.etatInsertion = self.etatInsertion + '\n INSERTION IDENTITES REUSSI'
                else:
                    self.insertBlobFiles(idpersonne=val[0], cin_recto=cin_recto_file, cin_verso=cin_verso_file,
                                         signature=signature_file, edit_mode=0, ext_signature=ext_signature,
                                         ext_cin_recto=ext_cin_recto, ext_cin_verso=ext_cin_verso,
                                         nom_signature=nom_fic_signature, nom_cin_recto=nom_fic_cin_recto,
                                         nom_cin_verso=nom_fic_cin_verso)
                    # self.etatInsertion = self.etatInsertion + '\n MODIFICATION IDENTITES REUSSI'
            dataToLog.append({ "id_personne": val[0],
                              "etat_insertion": self.etatInsertion,
                              "erreur": self.erreur})
            line = line + 1
            p = (line) * 100 / total

            self.emit(SIGNAL("progress(int)"), p)
        self.logger.addSheet(title=title, data=dataToLog, sheet_name="Log Import Identite personne")

    def importSignatureVoisins(self):
        cur = self.connection.cursor()
        try:
            cur.execute("SELECT idpointscardinaux, idparcelle, description, path_file FROM limitesparcelle")
            res = cur.fetchall()
            if res is not None:
                self.prepare_data_voisin(res)
        except Exception as err:
            print ('erreur lecture limites ' + str(err))
            self.connection.rollback()

    def prepare_data_voisin(self, data):
        self.current_step = self.current_step + 1
        self.emit(SIGNAL("clearSubstep(int)"), self.current_step)

        total = len(data)
        line = 0
        for val in data:
            dic_voisins = {}
            # if val[0] == 4: #Nord
            #     dic_voisins['nord'] = str(val[2]).strip()
            # if val[0] == 5: #Sud
            #     dic_voisins['sud'] = str(val[2]).strip()
            # if val[0] == 6: #Est
            #     dic_voisins['est'] = str(val[2]).strip()
            # if val[0] == 11: #Ouest
            #     dic_voisins['ouest'] = str(val[2]).strip()

            self.insertIntoBlobVoisin(val[0], val[1], val[2], val[3])

            line = line + 1
            p = (line) * 100 / total

            self.emit(SIGNAL("progress(int)"), p)


    def insertIntoBlobVoisin(self, idPoint, idparcelle, voisin, signature):
        #print "appel insertion signatures voisins"
        if voisin != '' and voisin is not None and signature is not None:
            # tab_voisin = voisins.split(':')
            # tab_signature = signatures.split(':')
            # print "signature anaty excel sy signature anaty tab"
            # print signatures
            # print tab_signature
            # if len(tab_voisin) > 0:
            #     if len(tab_signature) == len(tab_voisin):
            #         i = 0
            #         for voisin in tab_voisin:
            #             signature = tab_signature[i]
            infoFic = self.getFileDetails(signature)
            print infoFic
            #             self.writeBlobInDB(idPoint, idparcelle, voisin, infoFic)
            #             i = i + 1
            #     elif len(tab_signature) < len(tab_voisin):
            #         i = 0
            #         for voisin in tab_voisin:
            #             if i < len(tab_signature):
            #                 signature = tab_signature[i]
            #                 infoFic = self.getFileDetails(signature)
            #                 print infoFic
            try:
                self.writeBlobInDB(idPoint, idparcelle, voisin, infoFic)
            except Exception as err:
                print "erreur " + str(err)

    def getFileDetails(self, signature):
        # print "appel de getfileDetails"
        # print "param"
        # print signature
        # Lecture signature
        #infoFichier = {}
        nom_fic_signature = ''
        ext_signature = ''
        #signature = ''
        if signature != '':
            tab = signature.replace('\\', '/').split('.')
            print "tab signature"
            print tab
            if len(tab) > 1:
                ext_signature = tab[len(tab) - 1]
            tab_name_fic = tab[0].split('/')
            nom_fic_signature = tab_name_fic[len(tab_name_fic) - 1]
            # time.sleep(2)
            signat = signature.replace('\\', '/')
            signature = '/' + signat

        infoFichier = {'nom_fic':nom_fic_signature, 'path_to':signature, 'extension':ext_signature}
        return infoFichier

    def writeBlobInDB(self, idPoint, idparcelle, voisin, infoFic):
        # print "ecriture dans la base"
        # print infoFic

        #preparation du fichier
        signature_file = None
        # dir_path = os.path.dirname(str(self.filenames['image']))
        signature_path = None
        try:
            signature_path = str(self.filenames['images']).replace('\\', '/') + infoFic['path_to']
        except Exception as err:
            print err
        print ("path is")
        print signature_path
        print ("path is")
        if os.path.isfile(signature_path):
            try:
                signature_file = open(signature_path, 'rb').read()
                print "fichier signature ouvert"
            except Exception as err:
                print ("Erreur ouverture fichier signature" + err)

        if signature_file is not None:
            cur = self.connection.cursor()
            try:
                cur.execute("INSERT INTO blob_voisin (idpoint, idparcelle, voisin, signature_fic, signature_name, signature_ext) VALUES (%s,%s,%s,%s,%s,%s)",
                            (idPoint,idparcelle, voisin,psycopg2.Binary(signature_file), infoFic['nom_fic'], infoFic['extension']))
                self.connection.commit()
                print "INSERTION SONIA VOISIN"
            except psycopg2.Error as err:
                self.connection.rollback()
                if err.pgcode == "23505":
                    try:
                        cur.execute(
                            "UPDATE blob_voisin SET signature_fic = %s, signature_name = %s, signature_ext = %s WHERE idpoint = %s  AND idparcelle = %s AND voisin = %s ",
                            (psycopg2.Binary(signature_file), infoFic['nom_fic'],
                             infoFic['extension'],idPoint, idparcelle, voisin))
                        self.connection.commit()
                        print "MAJ SONIA VOISIN"
                    except Exception as err:
                        print err
                        self.connection.rollback()
            except Exception as err:
                print err
        else:
            cur = self.connection.cursor()
            try:
                cur.execute(
                    "UPDATE blob_voisin SET signature_fic = NULL, signature_name = NULL, signature_ext = NULL WHERE idpoint = %s  AND idparcelle = %s AND voisin = %s ",
                    (idPoint, idparcelle, voisin))
                self.connection.commit()
                print "MAJ SONIA VOISIN"
            except Exception as err:
                print err
                self.connection.rollback()
    # def importListing(self):
    #     title = ["code_parcelle", "numero_demande", "etat_insertion", "erreur"]
    #     dataToLog = []
    #     self.current_step = self.current_step + 1
    #     self.emit(SIGNAL("clearSubstep(int)"), self.current_step)
    #     cursor = self.connection.cursor()
    #     print ("IMPORT DEMANDE")
    #     self.emit(SIGNAL("clearSubstep(int)"), self.current_step)
    #     print ("signal")
    #     dir_path = ""
    #     try:
    #         dir_path = os.path.dirname(str(self.filenames['listing']))
    #         print dir_path
    #     except Exception as err:
    #         print (err)
    #
    #     try:
    #         wb = open_workbook(self.filenames['listing'], encoding_override="utf8")
    #     except Exception as err:
    #         print (err)
    #     sh_demande = None
    #     sh_codemandeurs = None
    #     # sh_demande = None
    #     # sh_crl = None
    #     # sh_hameau = None
    #
    #     # iteration sur les feuilles
    #
    #     curSheet = 0
    #     sh_demande = wb.sheet_by_index(curSheet)
    #
    #     #INSERTION DES DEMANDES
    #     if sh_demande is not None:
    #         total_lignes = sh_demande.nrows
    #         sh_demande.cell_value(0, 0)
    #
    #         line = 0  # lignes
    #         print ('nombre ligne')
    #         print (sh_demande.nrows)
    #         while line < sh_demande.nrows:
    #             print ('debut boucle')
    #             col = 0
    #             if line >= 1:
    #                 self.etatInsertion = ''
    #                 self.numdemande = ''
    #                 self.erreur = ''
    #                 print ('pass')
    #                 print line
    #                 dataPersonne = {}
    #                 dataParcelle = {}
    #
    #                 dataParcelle['region'] = str(sh_demande.cell_value(line, 0)).strip()
    #                 print "*******************region***************************"
    #
    #                 dataParcelle['district'] = str(sh_demande.cell_value(line, 1)).strip()
    #                 print "*******************district***************************"
    #                 print str(sh_demande.cell_value(line, 2)).strip().upper()
    #                 dataParcelle['commune'] = str(sh_demande.cell_value(line, 2)).strip().upper()
    #                 print (dataParcelle['commune'])
    #                 print "*******************commune***************************"
    #                 dataParcelle['fokontany'] = str(sh_demande.cell_value(line, 3)).strip().upper().decode('utf-8').replace("'","''")
    #                 print "*******************fokontany***************************"
    #                 dataParcelle['hameau'] = str(sh_demande.cell_value(line, 4)).strip().upper().decode('utf-8').replace("'","''")
    #                 print "*******************hameau***************************"
    #                 dataParcelle['lieudit'] = str(sh_demande.cell_value(line, 5)).strip().replace("'", "\'").replace("'","''")
    #                 print "*******************lieudit***************************"
    #                 dataParcelle['codePlanche'] = str(sh_demande.cell_value(line, 6)).strip()
    #                 print "*******************codeplanche***************************"
    #                 dataParcelle['collecteur_demande'] = str(sh_demande.cell_value(line, 7)).strip().replace("'", "\'")
    #                 print "*******************collecteur***************************"
    #                 dataPersonne['nom_prenom'] = str(sh_demande.cell_value(line, 8)).strip().upper().replace("'", "\'")
    #                 print "*******************noms***************************"
    #                 dataPersonne['genre'] = str(sh_demande.cell_value(line, 9)).strip()
    #                 print "*******************genre***************************"
    #                 print 'after genre'
    #
    #                 print dataParcelle['hameau']
    #
    #                 #Check commune
    #                 nomCommuneFromDb = None
    #                 nom_commune_from_db = self.select("commune", "nomcommune",
    #                                                  "idcommune = " + str(
    #                                                     globalvars.id_commune))
    #                 print "****************nom commune****************"
    #                 print nom_commune_from_db
    #                 if str(nom_commune_from_db).strip().upper() == dataParcelle['commune']:
    #                     nomCommuneFromDb = str(nom_commune_from_db)
    #                 #nomCommuneFromDb
    #                 if nomCommuneFromDb is None:
    #                     self.emit(SIGNAL("alertToQuit(QString)"),
    #                               u"La commune %s  n'est pas associée au projet sur lequel vous êtes connecté , Veuillez vérifier les paramètres de FIPLOF et réessayer l'import" % (
    #                                   dataParcelle['commune'],))
    #                     break
    #                 else:
    #                     #Check fokontany
    #                     print nomCommuneFromDb
    #                     nomFokontanyFromDb = self.select('fokontany', 'UPPER(TRIM(nomfokontany))', "UPPER(TRIM(nomfokontany)) ='" + dataParcelle['fokontany'] + "' and idfokontany = " + str(self.idFkt))
    #                     print nomFokontanyFromDb
    #                     if nomFokontanyFromDb is None:
    #                         self.emit(SIGNAL("alertToQuit(QString)"),
    #                                   u"Veuillez choisir le bon fokontany ou si le fokontany %s  n'existe pas dans la commune %s alors veuillez l'ajouter dans les paramètres de FIPLOF et réessayer l'import" % (
    #                                   dataParcelle['fokontany'], dataParcelle['commune']))
    #                         break
    #                     else:
    #                     #Check Hameau
    #                         ham = self.getIdHameau(idfkt= self.idFkt, nomHameau= dataParcelle['hameau'])
    #                         if ham is not None:
    #                             self.idHam = ham[0]
    #
    #
    #                         print "idHameau = " + str(self.idHam)
    #
    #                         if self.idHam is  None:
    #                             self.emit(SIGNAL("alertToQuit(QString)"),
    #                                       u"Le hameau %s n'existe pas dans le fokontany %s au niveau de FIPLOF, Veuillez vérifier les paramètres de FIPLOF et réessayer l'import" % (dataParcelle['hameau'], dataParcelle['fokontany']))
    #                             break
    #
    #                         print('ici')
    #                         print sh_demande.cell_value(line, 10)
    #                         dataPersonne['date_naissance'] = self.traiter_date(sh_demande,line,10,wb)
    #                         if str(sh_demande.cell_value(line, 11)).strip() == '':
    #                             dataPersonne['nevers'] = None
    #                         else:
    #                             nevers_ = self.traiter_date(sh_demande,line,11,wb)
    #                             if nevers_ is not None:
    #                                 dataPersonne['nevers'] = int(nevers_.year)
    #                                 print "*********************nes vers year******************"
    #                                 print dataPersonne['nevers']
    #                             else:
    #                                 if sh_demande.cell_type(line, 11) == 1:
    #                                     try:
    #                                         tab = str(sh_demande.cell_value(line, 11)).split('/')
    #                                         if len(tab) > 1:
    #                                             dataPersonne['nevers'] = int(tab[len(tab)-1])
    #                                         else:
    #                                             dataPersonne['nevers'] = int(str(sh_demande.cell_value(line, 11)).strip())
    #                                     except Exception as err:
    #                                         print err
    #                                         try:
    #                                             tab = str(sh_demande.cell_value(line, 11)).split('-')
    #                                             if len(tab) > 1:
    #                                                 dataPersonne['nevers'] = int(tab[0])
    #                                             else:
    #                                                 dataPersonne['nevers'] = int(str(sh_demande.cell_value(line, 11)).strip())
    #                                         except Exception as err:
    #                                             print err
    #                                             dataPersonne['nevers'] = None
    #                                     print "*********************nes vers chaine******************"
    #                                     print dataPersonne['nevers']
    #                                 elif sh_demande.cell_type(line, 11) == 2:
    #                                     try:
    #                                         dataPersonne['nevers'] = int(sh_demande.cell_value(line,11))
    #                                     except Exception as err:
    #                                         print err
    #                                         dataPersonne['nevers'] = None
    #                                 else:
    #                                     dataPersonne['nevers'] = None
    #
    #                         #dataPersonne['nevers'] = str(sh_demande.cell_value(line, 10)).strip()
    #                         #dataPersonne['cin_ou_acte'] = str(sh_demande.cell_value(line, 11)).strip()
    #                         dataPersonne['num_pi'] = ''
    #                         dataPersonne['num_copie'] = ''
    #
    #                         if sh_demande.cell_type(line, 12) == 2 or sh_demande.cell_type(line, 12) == 1:
    #                             dataPersonne['num_pi'] = str(int(sh_demande.cell_value(line,12)))
    #                         if sh_demande.cell_type(line, 12) == 0:
    #                             if sh_demande.cell_type(line, 13) != 0:
    #                                 if sh_demande.cell_type(line,13) == 2:
    #                                     dataPersonne['num_copie'] = str(int(sh_demande.cell_value(line,13)))
    #                                 else:
    #                                     dataPersonne['num_copie'] = str(sh_demande.cell_value(line, 13)).strip()
    #                         dataPersonne['date_pi'] = self.traiter_date(sh_demande,line,14,wb)
    #                         print dataPersonne['date_pi']
    #                         dataPersonne['lieu_pi'] = str(sh_demande.cell_value(line,15)).strip().replace("'", "\'").decode('utf-8')
    #                         dataPersonne['adresse'] = str(sh_demande.cell_value(line, 16)).strip().replace("'", "\'").decode('utf-8')
    #                         dataParcelle['categorie'] = str(sh_demande.cell_value(line,17)).strip().upper().replace("'", "\'")
    #                         dataParcelle['consistance'] = str(sh_demande.cell_value(line, 18)).strip().replace("'", "\'")
    #                         dataParcelle['code_parcelle'] = str(sh_demande.cell_value(line, 19)).strip()
    #                         self.codeparcelle_actuelle = dataParcelle['code_parcelle']
    #                         dataParcelle['num_demande'] = str(sh_demande.cell_value(line,20)).strip()
    #                         print ('insert categorie')
    #                         try:
    #                             self.insertToCategorie(str(sh_demande.cell_value(line,17)).strip().upper())
    #                         except Exception as err:
    #                             print 'erreur categorie'
    #                             print err
    #                         print ('fin insert categorie')
    #
    #                         dataParcelle['date_demande'] = self.traiter_date(sh_demande,line,21,wb)
    #                         if dataParcelle['date_demande'] is None:
    #                             self.erreur = self.erreur + "Erreur sur la date de demande\n"
    #                         print dataParcelle['date_demande']
    #                         id_personne = self.insertPersonne(dataPersonne)
    #                         print 'after id personne'
    #
    #                         id_parcelle = self.insertDataParcelle(dataParcelle)
    #                         print ('*************************************id_parcelle = **************************')
    #                         print id_parcelle
    #                         #self.codeparcelle_precedente = dataParcelle['parcelle']
    #
    #                         id_demande = self.insertDataDemande(dataParcelle, id_parcelle)
    #                         '''if id_demande is not None:
    #                             etat_insertion = etat_insertion + " INSERTION OU MODIFICATION DEMANDE REUSSIE \n"
    #                         '''
    #                         print ('id_demande = ')
    #                         print id_demande
    #
    #
    #                         print('codeParcelle == ' + dataParcelle['code_parcelle'])
    #                         #idParcelle = self.getIdParcelle(code_parcelle)
    #
    #                         #Recuperation des voisins
    #                         voisins = {}
    #                         voisins['nord'] = str(sh_demande.cell_value(line, 22)).decode('utf-8').strip()
    #                         voisins['sud'] = str(sh_demande.cell_value(line, 23)).decode('utf-8').strip()
    #                         voisins['est'] = str(sh_demande.cell_value(line, 24)).decode('utf-8').strip()
    #                         voisins['ouest'] = str(sh_demande.cell_value(line, 25)).decode('utf-8').strip()
    #
    #                         #Lecture signature
    #                         nom_fic_signature = None
    #                         ext_signature = None
    #                         signature = ''
    #                         if sh_demande.cell_type(line, 26) != 0:
    #                             signature = str(sh_demande.cell_value(line, 26)).decode('utf-8').strip()
    #                             tab = signature.replace('\\', '/').split('.')
    #                             ext_signature = tab[len(tab) - 1]
    #                             tab_name_fic = tab[0].split('/')
    #                             nom_fic_signature = tab_name_fic[len(tab_name_fic) - 1]
    #                             #time.sleep(2)
    #                             signat = signature.replace('\\', '/')
    #                             signature = '/' + signat
    #
    #                         nom_fic_cin_recto = None
    #                         ext_cin_recto = None
    #                         cin_recto = ''
    #                         if sh_demande.cell_type(line, 27) != 0:
    #                             cin_recto = str(sh_demande.cell_value(line, 27)).decode('utf-8').strip()
    #                             tab = cin_recto.replace('\\', '/').split('.')
    #                             ext_cin_recto = tab[len(tab) - 1]
    #                             tab_name_fic = tab[0].split('/')
    #                             nom_fic_cin_recto = tab_name_fic[len(tab_name_fic) - 1]
    #                             cin_rect = cin_recto.replace('\\', '/')
    #                             cin_recto = '/' + cin_rect
    #
    #                         nom_fic_cin_verso = None
    #                         cin_verso = ''
    #                         ext_cin_verso = None
    #                         if sh_demande.cell_type(line, 28) != 0:
    #                             cin_verso = str(sh_demande.cell_value(line, 28)).decode('utf-8').strip()
    #                             tab = cin_verso.replace('\\', '/').split('.')
    #                             ext_cin_verso = tab[len(tab) - 1]
    #                             tab_name_fic = tab[0].split('/')
    #                             nom_fic_cin_verso = tab_name_fic[len(tab_name_fic) - 1]
    #                             cin_vers = cin_verso.replace('\\', '/')
    #                             cin_verso = '/' + cin_vers
    #
    #                         print cin_recto
    #
    #                         print cin_verso
    #
    #                         # Full path
    #
    #                         signature_path = dir_path + signature
    #                         cin_recto_path = dir_path + cin_recto
    #                         cin_verso_path = dir_path + cin_verso
    #
    #
    #                         print "path defined"
    #                         print signature_path
    #                         signature_file = None
    #                         cin_recto_file = None
    #                         cin_verso_file = None
    #                         if signature != '' and os.path.isfile(signature_path):
    #                             try:
    #                                 signature_file = open(signature_path, 'rb').read()
    #                                 print "fichier signature ouvert"
    #                             except Exception as err:
    #                                 print ("Erreur ouverture fichier signature" + err)
    #
    #                         if cin_recto != '' and os.path.isfile(cin_recto_path):
    #                             try:
    #                                 cin_recto_file = open(cin_recto_path, 'rb').read()
    #                                 print "fichier cin_recto ouvert"
    #                             except Exception as err:
    #                                 print ("Erreur ouverture fichier cin recto" + err)
    #
    #                         if cin_verso != '' and os.path.isfile(cin_verso_path):
    #                             try:
    #                                 cin_verso_file = open(cin_verso_path, 'rb').read()
    #                                 print "fichier cin_verso ouvert"
    #                             except Exception as err:
    #                                 print ("Erreur ouverture fichier cin verso" + err)
    #
    #                         if signature_file is not None or cin_recto_file is not None or cin_verso_file is not None :
    #                             if self.exists("blob_personne","idpersonne", str(id_personne)):
    #                                 self.insertBlobFiles(idpersonne=id_personne, cin_recto=cin_recto_file,
    #                                                      cin_verso=cin_verso_file, signature=signature_file,
    #                                                      edit_mode=1, ext_signature=ext_signature,
    #                                                      ext_cin_recto=ext_cin_recto, ext_cin_verso=ext_cin_verso,
    #                                                      nom_signature=nom_fic_signature,
    #                                                      nom_cin_recto=nom_fic_cin_recto,
    #                                                      nom_cin_verso=nom_fic_cin_verso)
    #                             else:
    #                                 self.insertBlobFiles(idpersonne = id_personne,cin_recto = cin_recto_file, cin_verso = cin_verso_file, signature = signature_file, edit_mode = 0, ext_signature=ext_signature, ext_cin_recto=ext_cin_recto, ext_cin_verso=ext_cin_verso, nom_signature=nom_fic_signature, nom_cin_recto=nom_fic_cin_recto, nom_cin_verso=nom_fic_cin_verso)
    #
    #                         print ('tonga eto signature')
    #                         #fin lecture siganture
    #
    #                         # insertion des voisins
    #                         for key, val in voisins.items():
    #                             idpoint = None
    #                             if key == 'nord':
    #                                 idpoint = 4
    #                             if key == 'sud':
    #                                 idpoint = 5
    #                             if key == 'est':
    #                                 idpoint = 6
    #                             if key == 'ouest':
    #                                 idpoint = 11
    #                             where = ''
    #                             where = "idparcelle = '" + str(id_parcelle) + "' and idpointscardinaux = " + str(idpoint)
    #                             if self.select("limitesparcelle", "idparcelle", where) is None:
    #                                 try:
    #                                     cursor = self.connection.cursor()
    #                                     cursor.execute('INSERT INTO limitesparcelle(idpointscardinaux, idparcelle,description) '
    #                                                    'VALUES(%s, %s, %s)', (str(idpoint), id_parcelle, val))
    #                                     self.connection.commit()
    #                                     cursor.close()
    #                                     self.etatInsertion = self.etatInsertion + "INSERTION VOISINS REUSSI\n"
    #                                 except Exception as err:
    #                                     print (err)
    #                                     self.connection.rollback()
    #                                     cursor.close()
    #                                     self.erreur  = self.erreur + "Erreur sur insertion voisins "+ str(err)
    #                             else:
    #                                 try:
    #                                     cursor = self.connection.cursor()
    #                                     cursor.execute('UPDATE limitesparcelle set description = %s WHERE idpointscardinaux = %s AND idparcelle = %s',(val, str(idpoint), id_parcelle))
    #                                     self.connection.commit()
    #                                     cursor.close()
    #                                     self.etatInsertion = self.etatInsertion + "MODIFICATION VOISINS REUSSI\n"
    #                                 except Exception as err:
    #                                     print (err)
    #                                     self.connection.rollback()
    #                                     cursor.close()
    #                                     self.erreur  = self.erreur + "Erreur sur MODIFICATION voisins "+ str(err)
    #                         #insertion avoir_demande
    #                         print "avant representant"
    #                         # representant = not self.getIfHasRepresentant(idparcelle=id_parcelle)
    #                         try:
    #                             if self.codeparcelle_precedente == dataParcelle['code_parcelle']:
    #                                 representant = False
    #                             else:
    #                                 representant = True
    #                                 self.setFalseAllRepresentant(id_parcelle)
    #                             print "apres representant"
    #                         except Exception as err:
    #                             print str(err)
    #
    #                         print "representant"
    #                         print representant
    #                         where = "idparcelle = '" + str(id_parcelle) + "' and idpersonne = " + str(id_personne)
    #                         if self.select("avoir_demande", "idparcelle", where) is None:
    #                             try:
    #                                 cursor = self.connection.cursor()
    #                                 cursor.execute('INSERT INTO avoir_demande(idpersonne, idparcelle,iddemande, representant) '
    #                                                'VALUES(%s, %s, %s, %s)', (id_personne, id_parcelle, id_demande, representant))
    #                                 self.connection.commit()
    #                                 self.etatInsertion = self.etatInsertion + "INSERTION AVOIR DEMANDE OK\n"
    #                                 cursor.close()
    #                             except Exception as err:
    #                                 print (err)
    #                                 self.connection.rollback()
    #                                 self.erreur  = self.erreur + "Erreur sur insertion avoir demande "+ str(err)
    #                                 cursor.close()
    #                         else:
    #                             try:
    #                                 cursor = self.connection.cursor()
    #                                 cursor.execute('UPDATE avoir_demande SET iddemande = %s, representant = %s WHERE idpersonne = %s AND idparcelle = %s'
    #                                                , ( id_demande, representant, id_personne, id_parcelle))
    #                                 self.connection.commit()
    #                                 self.etatInsertion = self.etatInsertion + "MODIFICATION AVOIR DEMANDE OK\n"
    #                                 cursor.close()
    #                             except Exception as err:
    #                                 print (err)
    #                                 self.connection.rollback()
    #                                 self.erreur  = self.erreur + "Erreur sur MODIFICATION avoir demande "+ str(err)
    #                                 cursor.close()
    #                         #***********Traitement si demande deja CF******************
    #                         where_cf = "gid = '" + str(id_parcelle) + "' and idcertificat IS NOT NULL"
    #                         if self.select("parcelle_d", "gid", where_cf) is not None:
    #                             print ("CF existe")
    #                             if self.select("proprietaireparcelle", "idparcelle", where) is None:
    #                                 try:
    #                                     cursor = self.connection.cursor()
    #                                     cursor.execute(
    #                                         'INSERT INTO proprietaireparcelle(idpersonne, idparcelle, representant) '
    #                                         'VALUES(%s, %s, %s)',
    #                                         (id_personne, id_parcelle, representant))
    #                                     self.connection.commit()
    #                                     self.etatInsertion = self.etatInsertion + "INSERTION PROPRIETAIRE OK\n"
    #                                     cursor.close()
    #                                 except Exception as err:
    #                                     print (err)
    #                                     self.connection.rollback()
    #                                     self.erreur = self.erreur + "Erreur sur insertion INSERTION PROPRIETAIRE " + str(err)
    #                                     cursor.close()
    #                             else:
    #                                 try:
    #                                     cursor = self.connection.cursor()
    #                                     cursor.execute(
    #                                         'UPDATE proprietaireparcelle SET representant = %s WHERE idpersonne = %s AND idparcelle = %s'
    #                                         , (representant, id_personne, id_parcelle))
    #                                     self.connection.commit()
    #                                     self.etatInsertion = self.etatInsertion + "MODIFICATION PROPRIETAIRE OK\n"
    #                                     cursor.close()
    #                                 except Exception as err:
    #                                     print (err)
    #                                     self.connection.rollback()
    #                                     self.erreur = self.erreur + "Erreur sur MODIFICATION PROPRIETAIRE " + str(err)
    #                                     cursor.close()
    #                             #***************fin traitement si CF existe*****************************
    #
    #                 dataToLog.append({"code_parcelle": dataParcelle['code_parcelle'], "numero_demande": self.numdemande, "etat_insertion": self.etatInsertion,
    #              "erreur": self.erreur})
    #             self.codeparcelle_precedente = self.codeparcelle_actuelle
    #             line = line + 1
    #             p = (line) * 100 / total_lignes
    #
    #             self.emit(SIGNAL("progress(int)"), p)
    #     self.logger.addSheet(title=title, data=dataToLog, sheet_name="Log Import Listing")        #i = i + 1
    #
    # def updateParcelleDemande(self, numdemande, idparcelle):
    #     cur = self.connection.cursor()
    #     try:
    #         cur.execute('UPDATE parcelle_d set numdemande = %s where gid = %s', (numdemande, idparcelle))
    #         self.connection.commit()
    #     except Exception as err:
    #         print err
    #         self.connection.rollback()
    #     cur.close()
    #
    #
    # def insertDataParcelle(self, data):
    #     #cur = self.connection.cursor()
    #     where = "codeparcelle = '" + data['code_parcelle'] + "' and id_commune = " + str(globalvars.id_commune)
    #     if self.select("parcelle_d", "gid", where) is not None:
    #         self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
    #                   "Parcelle %s existe deja en base" % (data['code_parcelle']), "orange")
    #         cur = self.connection.cursor()
    #         try:
    #             #Ovana update ny eto
    #             cur.execute('UPDATE parcelle_d set district = %s, commune = %s, fkt = %s, consistance = %s, idhameau = %s, codeparcelle = %s, id_commune = %s, ref_import = %s, categorie = %s, inventaire = %s where codeparcelle = %s returning gid', (data['district'], data['commune'], data['fokontany'], data['consistance'], self.idHam, data['code_parcelle'], globalvars.id_commune, self.refimport, data['categorie'], True, data['code_parcelle']))
    #             res = cur.fetchone()
    #             self.etatInsertion = self.etatInsertion + "MISE A JOUR TABLE PARCELLE REUSSIE\n"
    #             cur.close()
    #             return res[0]
    #         except Exception as err:
    #             print err
    #             self.connection.rollback()
    #             self.etatInsertion = self.etatInsertion + "ECHEC MISE A JOUR TABLE PARCELLE \n"
    #             self.erreur = self.erreur + "ERREUR MAJ PARCELLE " + str(err)
    #             cur.close()
    #             return None
    #
    #     else:
    #         try:
    #             cur = self.connection.cursor()
    #             cur.execute('INSERT INTO parcelle_d (district, commune, fkt, consistance, idhameau, codeparcelle, id_commune, ref_import, categorie, inventaire) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) returning gid ',
    #                        (data['district'], data['commune'], data['fokontany'], data['consistance'], self.idHam, data['code_parcelle'], globalvars.id_commune, self.refimport, data['categorie'], True))
    #             self.connection.commit()
    #             self.etatInsertion = self.etatInsertion + "INSERTION DANS LA TABLE PARCELLE REUSSIE\n"
    #             res = cur.fetchone()
    #             cur.close()
    #             return  res[0]
    #         except Exception as err:
    #             print err
    #             self.connection.rollback()
    #             self.etatInsertion = self.etatInsertion + "ECHEC INSERTION TABLE PARCELLE \n"
    #             self.erreur = self.erreur + "ERREUR INSERTION TABLE PARCELLE " + str(err)
    #             if str(err).__contains__('Key (gid)'):
    #                 self.etatInsertion = self.etatInsertion + "ERRUR Key gid\n"
    #                 try:
    #                     self.etatInsertion = self.etatInsertion + "try update sequence\n"
    #                     currs = self.connection.cursor()
    #                     currs.execute("SELECT max(gid) + 1 FROM parcelle_d ")
    #                     max_id = str(currs.fetchone()[0])
    #                     sql = "alter sequence parcelle_d_id_seq restart with " + max_id
    #                     curs = self.connection.cursor()
    #                     curs.execute(sql)
    #                     self.connection.commit()
    #                     self.etatInsertion = self.etatInsertion + "sequence updated\n"
    #
    #                     curss = self.connection.cursor()
    #                     curss.execute('INSERT INTO parcelle_d (district, commune, fkt, consistance, idhameau, codeparcelle, id_commune, ref_import, categorie, inventaire) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) returning gid ',
    #                     (data['district'], data['commune'], data['fokontany'], data['consistance'], self.idHam, data['code_parcelle'], globalvars.id_commune, self.refimport, data['categorie'], True))
    #                     self.connection.commit()
    #                     self.etatInsertion = self.etatInsertion + "INSERTION PARCELLE REUSSIE\n"
    #                     self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
    #                               u"PARCELLE %s insérée dans la base" % (str(data['code_parcelle'])), "green")
    #                     res = curss.fetchone()
    #
    #                     return res[0]
    #                 except Exception as error:
    #                     print (error)
    #                     self.erreur = self.erreur + u"Erreur sur manip sequence\n" + str(error)
    #             #cur.close()
    #             return None
    #
    #
    # def getCodesLoc(self):
    #     cursor = self.connection.cursor()
    #     try:
    #         cursor.execute("SELECT d.codedistrict, c.codeg FROM commune c INNER JOIN district d ON c.iddistrict = d.iddistrict WHERE idcommune = %s", (globalvars.id_commune,))
    #         res = cursor.fetchone()
    #         cursor.close()
    #         codeG = str(res[1]).strip()
    #         if res[1] < 10:
    #             codeG = '0'+codeG
    #         return str(res[0]).strip()+'-'+codeG
    #     except Exception as err:
    #         print(err)
    #         self.connection.rollback()
    #         cursor.close()
    #         return None
    #
    #
    # def generateNumDemande(self):
    #     print 'call of generate demande'
    #     cptDemande = self.getCptDemande()
    #     print 'compteur demande'
    #     print cptDemande
    #     prefix = self.getCodesLoc()
    #     print 'code loc'
    #     print prefix
    #     numdemande = prefix + '-F-' + str(cptDemande)
    #     return numdemande
    #
    # def insertDataDemande(self, data, idparcelle):
    #     print '*********************************call of duty********************************'
    #     iddemande = None
    #     if idparcelle is not None:
    #         if self.exists('demande', 'gid', str(idparcelle)):
    #             self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
    #                     "Demande %s existe deja en base" % (idparcelle), "orange")
    #             cur = self.connection.cursor()
    #
    #             try:
    #                 cur.execute('select iddemande, numdemande from demande where gid = %s and numdemande IS NOT NULL', (idparcelle,))
    #                 res = cur.fetchone()
    #                 cur.close()
    #                 if res is not None:
    #                     self.updateParcelleDemande(res[1], idparcelle)
    #                     self.numdemande = str(res[1])
    #                     iddemande =  res[0]
    #
    #             except Exception as err:
    #                 print err
    #                 self.connection.rollback()
    #                 cur.close()
    #
    #             #Cas gid existant mais numdemande non existant
    #             if self.numdemande is None or self.numdemande.strip() == '':
    #                 num_demande = self.generateNumDemande()
    #                 print "************************existe**************************************************"
    #                 print "******************generated numdemande*******************"
    #                 print num_demande
    #                 if num_demande is None:
    #                     return
    #                 print 'numdemande = '
    #                 print num_demande
    #                 curs = self.connection.cursor()
    #                 try:
    #                     curs.execute(
    #                         'UPDATE demande SET region = %s,numdemande = %s, datedemande = %s, district = %s, commune = %s, fokontany = %s, idfokontany = %s, idcommune = %s, '
    #                         'consistance = %s, idprojet = %s, code_parcelle = %s, categorie = %s, planche_plof = %s, lieudit = %s, collecteur_demande = %s WHERE gid = %s AND numdemande IS NULL returning iddemande ',
    #                         (self.region, num_demande, data['date_demande'], data['district'], data['commune'],
    #                         data['fokontany'], self.idFkt, globalvars.id_commune, data['consistance'], globalvars.id_projet,
    #                         data['code_parcelle'], data['categorie'], data['codePlanche'], data['lieudit'],
    #                         data['collecteur_demande'], idparcelle))
    #                     self.connection.commit()
    #                     self.etatInsertion = self.etatInsertion + "MISE A JOUR DEMANDE REUSSIE\n"
    #                     res = curs.fetchone()
    #                     curs.close()
    #                     self.updateCptDemande()
    #                     self.updateParcelleDemande(num_demande, idparcelle)
    #                     self.numdemande = num_demande
    #                     iddemande = res[0]
    #                 except Exception as err:
    #                     print err
    #                     self.connection.rollback()
    #                     self.etatInsertion = self.etatInsertion + "ECHEC MISE A JOUR DEMANDE\n"
    #                     self.erreur = self.erreur + "ERREUR MISE A JOUR DEMANDE :" + str(err) + "\n"
    #                     cur.close()
    #             else: #Cas numdemande existe
    #                 curs = self.connection.cursor()
    #                 try:
    #                     curs.execute(
    #                         'UPDATE demande SET region = %s, datedemande = %s, district = %s, commune = %s, fokontany = %s, idfokontany = %s, idcommune = %s, '
    #                         'consistance = %s, idprojet = %s, code_parcelle = %s, categorie = %s, planche_plof = %s, lieudit = %s, collecteur_demande = %s WHERE gid = %s AND numdemande IS NOT NULL returning iddemande ',
    #                         (self.region, data['date_demande'], data['district'], data['commune'],
    #                         data['fokontany'], self.idFkt, globalvars.id_commune, data['consistance'],
    #                         globalvars.id_projet,
    #                         data['code_parcelle'], data['categorie'], data['codePlanche'], data['lieudit'],
    #                         data['collecteur_demande'], idparcelle))
    #                     self.connection.commit()
    #                     self.etatInsertion = self.etatInsertion + "MISE A JOUR DEMANDE REUSSIE\n"
    #                     res = curs.fetchone()
    #                     curs.close()
    #                     self.updateCptDemande()
    #                     #self.updateParcelleDemande(num_demande, idparcelle)
    #                     #self.numdemande = num_demande
    #                     if res is not None:
    #                         iddemande = res[0]
    #                 except Exception as err:
    #                     print err
    #                     self.connection.rollback()
    #                     self.etatInsertion = self.etatInsertion + "ECHEC MISE A JOUR DEMANDE\n"
    #                     self.erreur = self.erreur + "ERREUR MISE A JOUR DEMANDE :" + str(err) + "\n"
    #                     cur.close()
    #
    #         else:
    #             print 'call of duty 2'
    #             num_demande = self.generateNumDemande()
    #             if num_demande is None:
    #                 return
    #             print 'numdemande = '
    #             print num_demande
    #             cur = self.connection.cursor()
    #             try:
    #                 cur.execute(
    #                     'INSERT INTO demande (region,numdemande, gid, datedemande, district, commune, fokontany, idfokontany, idcommune, consistance, idprojet, code_parcelle, categorie, planche_plof, lieudit, collecteur_demande) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) returning iddemande ',
    #                     (self.region,num_demande, idparcelle, data['date_demande'], data['district'], data['commune'], data['fokontany'], self.idFkt, globalvars.id_commune, data['consistance'], globalvars.id_projet,
    #                     data['code_parcelle'], data['categorie'], data['codePlanche'], data['lieudit'], data['collecteur_demande']))
    #                 self.connection.commit()
    #                 self.etatInsertion = self.etatInsertion + "INSERTION DEMANDE REUSSIE\n"
    #                 self.numdemande = num_demande
    #                 res = cur.fetchone()
    #                 cur.close()
    #                 self.updateCptDemande()
    #                 self.updateParcelleDemande(num_demande, idparcelle)
    #                 if res is not None:
    #                     iddemande = res[0]
    #             except Exception as err:
    #                 print err
    #                 self.connection.rollback()
    #                 self.etatInsertion = self.etatInsertion + "ECHEC insertion DEMANDE\n"
    #                 self.erreur = self.erreur + "ERREUR insertion DEMANDE :" + str(err) + "\n"
    #                 cur.close()
    #                 if str(err).__contains__('Key (iddemande)'):
    #                     self.etatInsertion = self.etatInsertion + "ERREUR Key iddemande\n"
    #                     try:
    #                         self.etatInsertion = self.etatInsertion + "try update sequence\n"
    #                         currs = self.connection.cursor()
    #                         currs.execute("SELECT max(iddemande) + 1 FROM demande ")
    #                         max_id = str(currs.fetchone()[0])
    #                         sql = "alter sequence iddemande_seq restart with " + max_id
    #                         curs = self.connection.cursor()
    #                         curs.execute(sql)
    #                         self.connection.commit()
    #                         self.etatInsertion = self.etatInsertion + "sequence updated\n"
    #
    #                         curss = self.connection.cursor()
    #                         curss.execute('INSERT INTO demande (region,numdemande, gid, datedemande, district, commune, fokontany, idfokontany, idcommune, consistance, idprojet, code_parcelle, categorie, planche_plof, lieudit, collecteur_demande) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) returning iddemande ',
    #                         (self.region,num_demande, idparcelle, data['date_demande'], data['district'], data['commune'], data['fokontany'], self.idFkt, globalvars.id_commune, data['consistance'], globalvars.id_projet,
    #                         data['code_parcelle'], data['categorie'], data['codePlanche'], data['lieudit'], data['collecteur_demande']))
    #                         self.connection.commit()
    #                         self.etatInsertion = self.etatInsertion + "INSERTION PARCELLE REUSSIE\n"
    #                         self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
    #                                   u"Demande %s insérée dans la base" % (str(num_demande)), "green")
    #                         res = curss.fetchone()
    #                         return res[0]
    #                     except Exception as error:
    #                         print (error)
    #                         self.erreur = self.erreur + u"Erreur sur manip sequence\n" + str(error)
    #
    #         return iddemande
    #     else:
    #         return None
    #
    #
    #
    # def insertPersonne(self, data):
    #     sexe = 'masculin'
    #     isCin = True
    #     nom = ''
    #     prenoms = ''
    #     for key, val in data.items():
    #         if key == 'genre':
    #             if val == 'L':
    #                 sexe = 'masculin'
    #             if val == 'V':
    #                 sexe = 'feminin'
    #         if key == 'nom_prenom':
    #             tab_val = val.split(' ')
    #             nom = tab_val[0]
    #             prenoms = val.replace(nom, '', 1)
    #
    #     #cur = self.connection.cursor()
    #     print 'call of insertPersonne'
    #
    #     if self.exists("personne", "numcipersonne", data['num_pi']):
    #         self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
    #                   "Personne %s existe deja en base" % (data['num_pi']), "orange")
    #         idpers = None
    #         try:
    #             cursor = self.connection.cursor()
    #             cursor.execute('select idpersonne from personne where numcipersonne = %s', (data['num_pi'],))
    #             res = cursor.fetchone()
    #             self.etatInsertion  = self.etatInsertion + u"Personne ayant le même numero CIN existe déjà dans la base et son identifiant a été recupéré\n"
    #             idpers  = res[0]
    #         except Exception as err:
    #             print err
    #             self.connection.rollback()
    #             self.erreur = self.erreur  + u"Erreur de lecture info sur personne physique\n" + str(err)
    #
    #         if idpers is not None:    # MANAO UPDATE
    #             if data['num_pi'] != '':
    #                 print "num_pi"
    #                 try:
    #                     cursor = self.connection.cursor()
    #                     cursor.execute('UPDATE personne SET nompersonne = %s, prenompersonne = %s, sexepersonne = %s, '
    #                                    'datenaissancepersonne = %s, nevers = %s,numcipersonne = %s,'
    #                                    'datecipersonne = %s, lieucipersonne = %s,  adressepersonne = %s'
    #                                    ' where idpersonne = %s',
    #                                    (nom, prenoms, sexe, data['date_naissance'], data['nevers'], data['num_pi'],
    #                                     data['date_pi'], data['lieu_pi'],
    #                                     data['adresse'], str(idpers)))
    #                     self.connection.commit()
    #                     self.etatInsertion = self.etatInsertion + "MISE A PERSONNE REUSSIE\n"
    #                     self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
    #                               u"Personne %s insérée dans la base" % (str(nom)), "green")
    #                     #res = cursor.fetchone()
    #                     #return res[0]
    #                 except Exception as err:
    #                     print(err)
    #                     self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, str(err), "red")
    #                     self.connection.rollback()
    #                     self.etatInsertion = self.etatInsertion + "ECHEC MISE A JOUR PERSONNE\n"
    #                     self.erreur = self.erreur + u"Erreur insertion info sur personne physique\n" + str(err)
    #                     return None
    #             else:
    #                 if data['num_copie'] != '':
    #                     print "copie"
    #                     print data['num_copie']
    #                     result = self.checkUniquePersonne(data)
    #                     if result is not None:
    #                         # print result[0]
    #                         # time.sleep(2)
    #                         return result[0]
    #                     else:
    #                         try:
    #                             cursor = self.connection.cursor()
    #                             cursor.execute('UPDATE personne SET nompersonne = %s, prenompersonne = %s, sexepersonne = %s, '
    #                                            'datenaissancepersonne = %s, nevers = %s,numactenaissancepersonne = %s,'
    #                                            'dateactenaissancepersonne = %s, lieuactenaissancepersonne = %s,  adressepersonne = %s'
    #                                            ' WHERE idpersonne = %s',
    #                                            (nom, prenoms, sexe, data['date_naissance'], data['nevers'],
    #                                             data['num_copie'],
    #                                             data['date_pi'], data['lieu_pi'],
    #                                             data['adresse'], str(idpers)))
    #                             self.connection.commit()
    #                             self.etatInsertion = self.etatInsertion + "MISE A JOUR PERSONNE REUSSIE\n"
    #                             self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
    #                                       u"Personne %s insérée dans la base" % (str(nom)), "green")
    #                             res = cursor.fetchone()
    #                             return res[0]
    #                         except Exception as err:
    #                             print(err)
    #                             self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, str(err),
    #                                       "red")
    #                             self.connection.rollback()
    #                             self.etatInsertion = self.etatInsertion + "ECHEC MISE A JOUR PERSONNE\n"
    #                             self.erreur = self.erreur + u"Erreur insertion info sur personne physique\n" + str(err)
    #                             return None
    #         return idpers
    #     # if non existe en base
    #     else:
    #         print "non existe"
    #         if data['num_pi'] != '':
    #             print "num_pi"
    #             try:
    #                 cursor = self.connection.cursor()
    #                 cursor.execute('INSERT INTO personne (nompersonne, prenompersonne, sexepersonne, '\
    #                                'datenaissancepersonne, nevers,numcipersonne,'\
    #                                'datecipersonne, lieucipersonne,  adressepersonne'\
    #                                ') VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s) returning idpersonne',
    #                                (nom, prenoms, sexe, data['date_naissance'], data['nevers'], data['num_pi'], data['date_pi'], data['lieu_pi'],
    #                                 data['adresse']))
    #                 self.connection.commit()
    #                 self.etatInsertion = self.etatInsertion + "INSERTION PERSONNE REUSSIE\n"
    #                 self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
    #                           u"Personne %s insérée dans la base" % (str(nom)), "green")
    #                 res = cursor.fetchone()
    #                 return res[0]
    #             except Exception as err:
    #                 print(err)
    #                 self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, str(err), "red")
    #                 self.connection.rollback()
    #                 self.etatInsertion = self.etatInsertion + "ECHEC INSERTION PERSONNE Numpi existant\n"
    #                 self.erreur = self.erreur + u"Erreur insertion info sur personne physique\n" + str(err)
    #                 if str(err).__contains__('Key (idpersonne)'):
    #                     self.etatInsertion = self.etatInsertion + "Key idpersonne\n"
    #                     try:
    #                         self.etatInsertion = self.etatInsertion + "try update sequence\n"
    #                         currs = self.connection.cursor()
    #                         currs.execute("SELECT max(idpersonne) + 1 FROM personne ")
    #                         max_id = str(currs.fetchone()[0])
    #                         sql = "alter sequence personne_idpersonne_seq restart with " + max_id
    #                         curs = self.connection.cursor()
    #                         curs.execute(sql)
    #                         self.connection.commit()
    #                         self.etatInsertion = self.etatInsertion + "sequence updated\n"
    #
    #                         curss = self.connection.cursor()
    #                         curss.execute('INSERT INTO personne (nompersonne, prenompersonne, sexepersonne, '\
    #                                    'datenaissancepersonne, nevers,numcipersonne,'\
    #                                    'datecipersonne, lieucipersonne,  adressepersonne'\
    #                                    ') VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s) returning idpersonne',
    #                                    (nom, prenoms, sexe, data['date_naissance'], data['nevers'], data['num_pi'], data['date_pi'], data['lieu_pi'],
    #                                     data['adresse']))
    #                         self.connection.commit()
    #                         self.etatInsertion = self.etatInsertion + "INSERTION PERSONNE REUSSIE\n"
    #                         self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
    #                                   u"Personne %s insérée dans la base" % (str(nom)), "green")
    #                         res = curss.fetchone()
    #
    #                         return res[0]
    #                     except Exception as error:
    #                         print (error)
    #                         self.erreur = self.erreur + u"Erreur sur manip sequence\n" + str(error)
    #
    #                 return None
    #         else:
    #             if data['num_copie'] != '':
    #                 print "copie"
    #                 print data['num_copie']
    #                 result = self.checkUniquePersonne(data)
    #                 if result is not None:
    #                     #print result[0]
    #                     #time.sleep(2)
    #                     return result[0]
    #                 else:
    #                     try:
    #                         cursor = self.connection.cursor()
    #                         cursor.execute('INSERT INTO personne (nompersonne, prenompersonne, sexepersonne, '\
    #                                        'datenaissancepersonne, nevers,numactenaissancepersonne,'\
    #                                        'dateactenaissancepersonne, lieuactenaissancepersonne,  adressepersonne'\
    #                                        ') VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s) returning idpersonne',
    #                                        (nom, prenoms, sexe, data['date_naissance'], data['nevers'], data['num_copie'],
    #                                         data['date_pi'], data['lieu_pi'],
    #                                         data['adresse']))
    #                         self.connection.commit()
    #                         self.etatInsertion = self.etatInsertion + "INSERTION PERSONNE REUSSIE\n"
    #                         self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
    #                                   u"Personne %s insérée dans la base" % (str(nom)), "green")
    #                         res = cursor.fetchone()
    #                         return res[0]
    #                     except Exception as err:
    #                         print(err)
    #                         self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, str(err), "red")
    #                         self.connection.rollback()
    #                         self.etatInsertion = self.etatInsertion + "ECHEC INSERTION PERSONNE numpi non existant\n"
    #                         self.erreur = self.erreur + u"Erreur insertion info sur personne physique\n" + str(err)
    #                         if str(err).__contains__('Key (idpersonne)'):
    #                             self.etatInsertion = self.etatInsertion + "Key idpersonne\n"
    #                             try:
    #                                 self.etatInsertion = self.etatInsertion + "try update sequence\n"
    #                                 currs = self.connection.cursor()
    #                                 currs.execute("SELECT max(idpersonne) + 1 FROM personne ")
    #                                 max_id = str(currs.fetchone()[0])
    #                                 sql = "alter sequence personne_idpersonne_seq restart with " + max_id
    #                                 curs = self.connection.cursor()
    #                                 curs.execute(sql)
    #                                 self.connection.commit()
    #                                 self.etatInsertion = self.etatInsertion + "sequence updated\n"
    #
    #                                 curss = self.connection.cursor()
    #                                 curss.execute('INSERT INTO personne (nompersonne, prenompersonne, sexepersonne, '\
    #                                            'datenaissancepersonne, nevers,numcipersonne,'\
    #                                            'datecipersonne, lieucipersonne,  adressepersonne'\
    #                                            ') VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s) returning idpersonne',
    #                                            (nom, prenoms, sexe, data['date_naissance'], data['nevers'], data['num_pi'], data['date_pi'], data['lieu_pi'],
    #                                             data['adresse']))
    #                                 self.connection.commit()
    #                                 self.etatInsertion = self.etatInsertion + "INSERTION PERSONNE REUSSIE\n"
    #                                 self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
    #                                           u"Personne %s insérée dans la base" % (str(nom)), "green")
    #                                 res = curss.fetchone()
    #
    #                                 return res[0]
    #                             except Exception as error:
    #                                 print (error)
    #                                 self.erreur = self.erreur + u"Erreur sur manip sequence\n" + str(error)
    #                         return None



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

    def getCptDemande(self):
        print 'call of getCptDemande'
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT cptdemande FROM commune WHERE idcommune = %s", (globalvars.id_commune,))
            res = cursor.fetchone()
            return res[0]
        except Exception as err:
            print(err)
            self.connection.rollback()
        cursor.close()

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
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            cursor.close()
            if len(rows) > 0:
                return rows[0][0]
            return None
        except Exception as err:
            print err
            self.connection.rollback()

    def traiter_date(self,sheet, line, col, wb):
        date = None
        if sheet.cell_type(line, col) == 3 or sheet.cell_type(line,col) == 5:  # verification si la cellule est une date
            print "in date type"
            try:
                date = datetime(*xlrd.xldate.xldate_as_tuple(sheet.cell_value(line, col), wb.datemode))
                date = date.date()
            except Exception as err:
                print err

        elif sheet.cell_type(line, col) == 1: #Si chaine de ceractere
            print "chaine le date"
            print str(sheet.cell_value(line, col)).strip()
            try:
                date = datetime.strptime(str(sheet.cell_value(line, col)).strip(), '%d/%m/%Y').date()
            except Exception as err:
                print err
                try:
                    date = datetime.strptime(str(sheet.cell_value(line, col)).strip(), '%Y-%m-%d').date()
                except Exception as err:
                    print err

        else:
            pass

        return date


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
                self.etatInsertion = self.etatInsertion + "INSERTION SIGNATURE REUSSIE\n"
            except Exception as err:
                print err
                self.etatInsertion = self.etatInsertion + "ECHEC INSERTION SIGNATURE \n"
                self.erreur = self.erreur + "ERREUR SIGNATURE " + str(err) + "\n"
                self.connection.rollback()
        else:
            try:
                cur.execute(
                    'UPDATE blob_personne SET cin_recto = %s , cin_verso = %s, signature = %s, empreinte_d = %s, empreinte_g = %s, '
                    'signature_type = %s, cin_recto_type = %s, cin_verso_type = %s, signature_name = %s, cin_recto_name = %s, cin_verso_name = %s '
                    ' where idpersonne = %s',
                    (psycopg2.Binary(cin_recto), psycopg2.Binary(cin_verso), psycopg2.Binary(signature),
                     psycopg2.Binary(empreinte_d), psycopg2.Binary(empreinte_g), ext_signature, ext_cin_recto,
                     ext_cin_verso,
                     nom_signature, nom_cin_recto, nom_cin_verso, idpersonne))
                self.connection.commit()
                print "MODIFICATION REUSSIE"
                self.etatInsertion = self.etatInsertion + "MODIFICATION SIGNATURE REUSSIE\n"
            except Exception as err:
                print err
                self.etatInsertion = self.etatInsertion + "ECHEC MODIFICATION SIGNATURE \n"
                self.erreur = self.erreur + "ERREUR SIGNATURE " + str(err) + "\n"
                self.connection.rollback()

    def importParcelle(self):
        # Preparation log
        title = ["code_parcelle", "numero_demande", "etat_insertion", "erreur"]
        dataToLog = []
        # fin prep    log
        self.current_step = self.current_step + 1
        self.emit(SIGNAL("clearSubstep(int)"), self.current_step)
        #cursor = self.connection.cursor()
        print ("IMPORT DEMANDE")
        self.emit(SIGNAL("clearSubstep(int)"), self.current_step)

        filename = _fromUtf8(self.filenames['shape'])
        TabCodeParcelle = []

        layer = QgsVectorLayer(filename, "dataFromPLOFPapers", "ogr")
        features = layer.getFeatures()
        countFeatures = layer.featureCount()
        print("countFeatures")
        print(countFeatures)
        cursor = self.connection.cursor()
        i = 0

        for f in features:
            gid = None
            code_parcelle, numdemande, etatInsertion, erreur = "", "", "", ""
            try:
                geometry = f.geometry()
                if geometry.wkbType() == QGis.WKBPolygon:
                    x = geometry.asPolygon()
                if geometry.wkbType() == QGis.WKBMultiPolygon:
                    x = geometry.asMultiPolygon()[0]

                attrs = f.attributes()
                size = len(attrs)
                print(attrs)

                codeParcelle = attrs[1].toPyObject()
                code_parcelle = str(codeParcelle)
                print(codeParcelle)
                print(" code parcelle--")

                # NumDemande = self.NumDemande+" "+str(attrs[2].toPyObject())
                print('Geometry.exportToWkt()')
                print(str(geometry.exportToWkt()))

                where = "codeparcelle = '" + str(codeParcelle) + "' and id_commune = " + str(globalvars.id_commune)
                if self.select("parcelle_d", "gid", where) is not None:
                    print 'exists'
                    try:
                        #cursor = self.connection.cursor()
                        cursor.execute('update parcelle_d set geom = ST_GeomFromText(%s, %s), surface = ST_Area(%s) where codeparcelle = %s AND id_commune = %s returning gid,surface', (str(geometry.exportToWkt()),str(globalvars.EPSG_SCR), str(geometry.exportToWkt()), str(codeParcelle), globalvars.id_commune))
                        self.connection.commit()
                        dm = cursor.fetchone()
                        gid = dm[0]
                        etatInsertion = "MISE A JOUR REUSSIE"
                    except Exception as err:
                        print err
                        self.connection.rollback()
                        etatInsertion = "ERREUR DE MISE A JOUR"
                        erreur = erreur + str(err) + "\n"

                else:
                    print 'not exists'
                    try:

                        exe = cursor.execute("INSERT INTO parcelle_d (geom,surface ,codeparcelle,id_commune)VALUES (ST_GeomFromText(%s, " + str(globalvars.EPSG_SCR) + "),ST_Area(%s), %s, %s) returning gid,surface",
                            (str(geometry.exportToWkt()), str(geometry.exportToWkt()), str(codeParcelle), globalvars.id_commune))
                        self.connection.commit()
                        self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
                                  u"Parcelle %s insérée dans la base" % (str(codeParcelle)), "green")
                        print("AFTER commit")
                        dm = cursor.fetchone()
                        gid = dm[0]
                        etatInsertion = "INSERTION REUSSIE"

                        # self.progress(p)

                        # #insert into table demande
                        # self.ui.numeroDemandeLineEdit.setText(
                        #     _fromUtf8(chDistrict + "-" + chCodeGuichet) + "-F-" + str(self.currentValDemande))
                    except Exception as e:
                        TabCodeParcelle.append(codeParcelle)
                        self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, str(e), "red")
                        self.connection.rollback()
                        etatInsertion = "ERREUR INSERTION"
                        erreur = erreur + str(e) + "\n"
                        if str(err).__contains__('Key (gid)'):
                            self.etatInsertion = self.etatInsertion + "ERRUR Key gid\n"
                            try:
                                self.etatInsertion = self.etatInsertion + "try update sequence\n"
                                currs = self.connection.cursor()
                                currs.execute("SELECT max(gid) + 1 FROM parcelle_d ")
                                max_id = str(currs.fetchone()[0])
                                sql = "alter sequence parcelle_d_id_seq restart with " + max_id
                                curs = self.connection.cursor()
                                curs.execute(sql)
                                self.connection.commit()
                                self.etatInsertion = self.etatInsertion + "sequence updated\n"

                                curss = self.connection.cursor()
                                curss.execute("INSERT INTO parcelle_d (geom,surface ,codeparcelle,id_commune)VALUES (ST_GeomFromText(%s, " + str(globalvars.EPSG_SCR) + "),ST_Area(%s), %s, %s) returning gid,surface",
                                (str(geometry.exportToWkt()), str(geometry.exportToWkt()), str(codeParcelle), globalvars.id_commune))
                                self.connection.commit()
                                self.etatInsertion = self.etatInsertion + "INSERTION PARCELLE REUSSIE\n"
                                self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
                                          u"PARCELLE %s insérée dans la base" % (str(codeParcelle)), "green")
                                res = curss.fetchone()
                                return res[0]
                            except Exception as error:
                                print (error)
                                self.erreur = self.erreur + u"Erreur sur manip sequence\n" + str(error)
                        print(e)

            except Exception as e:
                print(e)
                print(' parcelle ayant des probleme de geometrie')
                etatInsertion = "ERREUR INSERTION"
                erreur = erreur + str(err) + "\n"


            if gid is not None:
                if code_parcelle == '':
                    codParcel = None
                else:
                    codParcel = code_parcelle

                try:
                    cur = self.connection.cursor()
                    cur.execute('INSERT INTO demande (code_parcelle, gid, idcommune) VALUES (%s, %s, %s)', (codParcel, str(gid), str(globalvars.id_commune)))
                    self.connection.commit()
                    #cur.close()
                except Exception as err:
                    print err
                    self.connection.rollback()

            p = (i + 1) * 100 / countFeatures
            self.emit(SIGNAL("progress(int)"), p)
            dataToLog.append(
                {"code_parcelle": code_parcelle, "numero_demande": numdemande, "etat_insertion": etatInsertion,
                 "erreur": erreur})
            i = i + 1

        print(TabCodeParcelle)
        self.logger.addSheet(title=title, data=dataToLog, sheet_name="Log Import Shape")

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

    def getIdHameau(self, idfkt = None, nomHameau = ''):
        print "call getIdHameau"
        if idfkt is not None and nomHameau != '':
            curs = self.connection.cursor()
            try:
                print 'in try'
                curs.execute("SELECT idhameau FROM hameau where nomhameau = %s and idfokontany = %s",(nomHameau,str(idfkt)))
                res = curs.fetchone()
                print 'after fetch'
                #cur.close()
                return res
            except Exception as err:
                print "Erreur lecture Hameau ImportListingThread " + err
                self.connection.rollback()
                return None
        else:
            return None

    def checkUniquePersonne(self, params):
        cur = self.connection.cursor()
        try:
            cur.execute("SELECT idpersonne FROM personne WHERE  numactenaissancepersonne =  %s and dateactenaissancepersonne = %s and lieuactenaissancepersonne = %s", (params['num_copie'], params['date_pi'], params['lieu_pi']))
            res = cur.fetchone()
            return res
        except Exception as err:
            print "Erreur checkUniquePersonne ImportListingDemande " + str(err)
            self.connection.rollback()
            return None

    def setFalseAllRepresentant(self, idparcelle):
        cur = self.connection.cursor()
        try:
            cur.execute("UPDATE avoir_demande SET representant = FALSE  WHERE idparcelle = %s ", (idparcelle,))
            print ('set false all representant OK')
        except Exception as err:
            print "Erreur set false representant KO " + err
            self.connection.rollback()

        try:
            cur.execute("UPDATE proprietaireparcelle SET representant = FALSE  WHERE idparcelle = %s ", (idparcelle,))
            print ('set false all representant proprio OK')
        except Exception as err:
            print "Erreur set false representant proprio KO " + err
            self.connection.rollback()

    def getIfHasRepresentant(self, idparcelle):
        cur = self.connection.cursor()
        yes = False
        try:
            cur.execute("SELECT iddemande FROM avoir_demande WHERE idparcelle = %s and representant IS TRUE", (idparcelle,))
            res = cur.fetchone()
            if res is not None:
                if len(res) > 0:
                    yes = True
        except Exception as err:
            print "Erreur getIfHasRepresentant " + err
            self.connection.rollback()
        return yes






