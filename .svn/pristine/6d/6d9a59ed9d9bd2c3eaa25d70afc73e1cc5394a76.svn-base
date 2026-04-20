# coding: utf8
from PyQt4.QtCore import QThread, SIGNAL
from osgeo import gdal, ogr
#import ogrinfo
import sys
import os
import os.path
import globalvars
from datetime import datetime
import psycopg2
import time
import xlrd
from xlrd import open_workbook
import io
from logs import xlsLogger


class ImporterThreadHameau(QThread):
    def __init__(self, filename, connection):
        QThread.__init__(self)
        self.filename, self.connection = filename, connection
        self.logger = xlsLogger.xlsLogger("Import_LOCALITE_PLOF_REP")
        self.current_step =-1
        self.nom, self.etatInsertion, self.erreur = '','',''

    def __del__(self):
        self.wait()

    def run(self):
        # print (self.filename)
        if self.filename == "":
            self.emit(SIGNAL("alert(QString)"), "Veuillez choisir un dossier")
            return
        # poDS = ogr.Open(str(self.filename), False)
        # if poDS is None:
        # self.emit(SIGNAL("alert(QString)"), "Fichier ogr non valide")
        # return

        #IMPORT PERSONNE PHYSIQUE
        self.emit(SIGNAL("stepInit(int)"), self.current_step + 1)
        #print("Debut import Personne Physique")
        #self.importPersonnePhysique()
        #print("Fin import Personne Physique")

        print("Debut import Fokontany")
        self.importFkt()
        print("Fin import Fokontany")

        self.emit(SIGNAL("stepDone(int)"), self.current_step)

        self.emit(SIGNAL("stepInit(int)"), self.current_step + 1)
        print("Debut import Hameau")
        self.importHameau()
        print("Fin import Hameau")

        #self.updateProprietaire()
        self.emit(SIGNAL("stepDone(int)"), self.current_step)

        self.emit(SIGNAL("stepInit(int)"), self.current_step + 1)
        # print("Debut import Personne Physique")
        # self.importPersonnePhysique()
        # print("Fin import Personne Physique")

        print("Debut import Consistance")
        self.importConsistance()
        print("Fin import Hameau")

        # self.updateProprietaire()
        self.emit(SIGNAL("stepDone(int)"), self.current_step)
        #FIN IMPORT PERSONNE PHYSIQUE

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

    def getIdFkt(self, codefkt):
        cur = self.connection.cursor()
        code_fkt = str(codefkt).strip()
        try:
            cur.execute('SELECT idfokontany from fokontany WHERE TRIM(codefokontany) = %s', (code_fkt,))
            res = cur.fetchone()
            return res[0]
        except Exception as err:
            print "*******************erreur recup id fokontany**************"
            print(err)
            self.connection.rollback()
            return None

    def importFkt(self):
        self.current_step = self.current_step + 1
        self.emit(SIGNAL("clearSubstep(int)"), self.current_step)
        cursor = self.connection.cursor()
        print ("IMPORT FOKONTANY")
        self.emit(SIGNAL("clearSubstep(int)"), self.current_step)
        print ("signal")
        #fileDirPath = ""
        try:
            wb = open_workbook(self.filename, encoding_override="utf8")
        except Exception as err:
            print (err)
            pass
        sheet = wb.sheet_by_index(2)
        total_lignes = sheet.nrows
        sheet.cell_value(0, 0)

        line = 0 #lignes
        print ('nombre ligne')
        print (sheet.nrows)
        while line < sheet.nrows:
            col = 0
            if line >= 1:
                print line
                # rcin = sheet.cell_value(line,2)
                nomFkt = str(sheet.cell_value(line, 1)).decode('utf-8').strip().replace("'","''")
                codeFkt = str(sheet.cell_value(line, 2)).decode('utf-8').strip().replace("'","''")

                print 'else'
                cursor = self.connection.cursor()
                where = "codefokontany = '" + codeFkt + "' and idcommune = " + str(globalvars.id_commune)
                if self.select("fokontany", "idfokontany", where) is not None:
                        print (u"Fokontany déjà  en base")
                else:
                    try:
                        cursor.execute('INSERT INTO fokontany (codefokontany, nomFokontany, idcommune) '
                                               'VALUES(%s,%s,%s)',(codeFkt,nomFkt,globalvars.id_commune))
                        self.connection.commit()
                        self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
                                              "Fokontany %s" % (nomFkt), "green")
                    except Exception as err:
                        self.connection.rollback()
                        # self.saveErrorLine(ligneToLog, writer)
                        self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, str(err), "red")
                        print(err)

            p = (line + 1) * 100 / total_lignes
            self.emit(SIGNAL("progress(int)"), p)
            line = line + 1


    def importHameau(self):
        title = ["code_hameau", "nom_hameau", "etat_insertion", "erreur"]
        dataToLog = []
        self.current_step = self.current_step + 1
        self.emit(SIGNAL("clearSubstep(int)"), self.current_step)
        cursor = self.connection.cursor()
        print ("IMPORT HAMEAU")
        self.emit(SIGNAL("clearSubstep(int)"), self.current_step)
        print ("signal")

        try:
            wb = open_workbook(self.filename, encoding_override="utf8")
        except Exception as err:
            print (err)
            pass

        sheet = wb.sheet_by_index(0)
        total_lignes = sheet.nrows
        sheet.cell_value(0, 0)

        line = 0 #lignes
        print ('nombre ligne')
        print (sheet.nrows)
        while line < sheet.nrows:
            col = 0
            if line >= 1:
                print line
                # rcin = sheet.cell_value(line,2)
                idHameau = str(sheet.cell_value(line, 1)).decode('utf-8')
                nomHameau = str(sheet.cell_value(line, 2)).decode('utf-8').replace("'","''")
                codeHameau = str(sheet.cell_value(line, 3)).decode('utf-8').replace("'","''")
                codeFkt = str(sheet.cell_value(line, 4)).decode('utf-8').replace("'","''")
                idFkt = None
                idFkt = self.getIdFkt(codeFkt)

                print("ID HAMEAU")
                print(idHameau)

                print 'else'
                cursor = self.connection.cursor()

                if idFkt is not None:
                    where = "codehameau = '" + codeHameau + "' and idfokontany = " + str(idFkt)
                    if self.select("hameau", "idhameau", where) is not None:
                        print (u"hameau" + codeHameau + " code fokontany " + codeFkt + " ligne " + str(line) + u" existe déjà  dans la base ")
                    else:
                        try:
                            cursor.execute('INSERT INTO hameau (codehameau, nomhameau, idfokontany) '
                                               'VALUES(%s,%s,%s)',(codeHameau,nomHameau,idFkt))
                            self.connection.commit()
                            self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
                                              "Personne %s" % (idHameau), "green")
                        except Exception as err:
                            self.connection.rollback()
                            print "**************erreur import hameau******************"
                            print err
                            # self.saveErrorLine(ligneToLog, writer)
                            self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, str(err), "red")
                            print(err)
                else:
                    try:
                        cursor.execute('INSERT INTO hameau (codehameau, nomhameau) '
                                           'VALUES(%s,%s)',(codeHameau,nomHameau))
                        self.connection.commit()
                        self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
                                          "Personne %s" % (idHameau), "green")
                    except Exception as err:
                        self.connection.rollback()
                        print "**************erreur import hameau******************"
                        print err
                        # self.saveErrorLine(ligneToLog, writer)
                        self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, str(err), "red")
                        print(err)

            p = (line + 1) * 100 / total_lignes
            self.emit(SIGNAL("progress(int)"), p)
            line = line + 1


    def importConsistance(self):
        self.current_step = self.current_step + 1
        self.emit(SIGNAL("clearSubstep(int)"), self.current_step)
        cursor = self.connection.cursor()
        print ("IMPORT consistance")
        self.emit(SIGNAL("clearSubstep(int)"), self.current_step)
        print ("signal")

        try:
            wb = open_workbook(self.filename, encoding_override="utf8")
        except Exception as err:
            print (err)
            pass

        sheet = wb.sheet_by_index(1)
        total_lignes = sheet.nrows
        sheet.cell_value(0, 0)

        line = 0 #lignes
        print ('nombre ligne')
        print (sheet.nrows)
        while line < sheet.nrows:
            col = 0
            if line >= 1:
                print line
                # rcin = sheet.cell_value(line,2)
                id = sheet.cell_value(line, 0)
                consistance_parc = str(sheet.cell_value(line, 1)).decode('utf-8').replace("'","''")
                consistance_bat = str(sheet.cell_value(line, 2)).decode('utf-8').replace("'","''")
                print 'eto'
                cursor = self.connection.cursor()
                if self.exists("consistance", "idconsistance", id):
                    try:
                        cursor.execute('UPDATE consistance SET libelleconsistance = %s, parcelleoubatiment = %s WHERE idconsistance = %s',(consistance_parc,consistance_bat,id))
                        self.connection.commit()
                        self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
                                          "Consistance %s" % (consistance_parc), "green")
                    except Exception as err:
                        self.connection.rollback()
                        # self.saveErrorLine(ligneToLog, writer)
                        self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, str(err), "red")
                        print(err)
                else:
                    try:
                        cursor.execute('INSERT INTO consistance (idconsistance, libelleconsistance, parcelleoubatiment) '
                                           'VALUES(%s,%s,%s)',(id,consistance_parc,consistance_bat))
                        self.connection.commit()
                        self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
                                          "Consistance %s" % (consistance_parc), "green")
                    except Exception as err:
                        self.connection.rollback()
                        # self.saveErrorLine(ligneToLog, writer)
                        self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, str(err), "red")
                        print(err)

            p = (line + 1) * 100 / total_lignes
            self.emit(SIGNAL("progress(int)"), p)
            line = line + 1


    def importPersonnePhysique(self):
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

        sheet = wb.sheet_by_index(0)
        total_lignes = sheet.nrows
        sheet.cell_value(0, 0)

        line = 0 #lignes
        print ('nombre ligne')
        print (sheet.nrows)
        while line < sheet.nrows:
            col = 0
            if line >= 1:

                # rcin = sheet.cell_value(line,2)
                nom = str(sheet.cell_value(line, 0)).decode('utf-8')
                prenoms = str(sheet.cell_value(line, 1)).decode('utf-8')
                # typeIdentite = sheet.cell_value(line, )
                num_cin = self.stripSpace(sheet.cell_value(line, 5))
                genre = str(sheet.cell_value(line, 2)).decode('utf-8')
                sexe = ""
                if genre == "F":
                    sexe = "feminin"
                elif genre == "M":
                    sexe = "masculin"
                else:
                    sexe = self.retsexe(num_cin)

                # num_cin = sheet.cell_value(line, 2)
                lieu_cin = str(sheet.cell_value(line, 7)).decode('utf-8')
                # date mila traitena manokana
                date_naissance = ""
                nevers = None
                num_acte = None
                date_acte = None
                lieu_acte = None
                if str(sheet.cell_value(line, 8)).strip()!='':
                    num_acte = str(sheet.cell_value(line, 8)).strip()
                if str(sheet.cell_value(line, 9)).strip()!='':
                    date_acte = self.traiter_date(str(sheet.cell_value(line, 9)).strip())
                if str(sheet.cell_value(line, 10)).strip()!= '':
                    lieu_acte = self.traiter_date(str(sheet.cell_value(line, 10)).strip())

                if (sheet.cell_value(line, 3)!= ""):
                    if (str(sheet.cell_value(line, 3)).lower().__contains__("vers")):
                        print "Ne vers"
                        never_s = str(sheet.cell_value(line, 3)).split(' ')
                        nevers = never_s[1]
                    else:
                        date_naissance = self.traiter_date(sheet.cell_value(line, 3))

                #print ("dans la boucle")
                # print(date_naissance)
                #lieu_naissance = str(sheet.cell_value(line, 6)).decode('utf-8')

                nom_pere = sheet.cell_value(line, 14)
                nom_mere = sheet.cell_value(line, 15)
                # etat_matri = sheet.cell_value(line, 35)
                sit_matri = 1
                if str(sheet.cell_value(line, 13))!= "1":
                    sit_matri = 2

                # mariea = sheet.cell_value(line, 36)
                adresse = str(sheet.cell_value(line, 11))
                print "Adresse"
                print (adresse)
                date_cin = self.traiter_date(sheet.cell_value(line, 6))
                print "Date CIN"
                print(date_cin)
                print "Date naissance"
                print (date_naissance)
                # Insertion dans la base

                #Cas date_naissance vide
                if (date_naissance is None or date_naissance ==''):
                    print ("Cas date naissance none")
                    if self.exists("personne", "numcipersonne", num_cin):
                        self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
                                  "Personne %s existe deja en base" % (num_cin), "orange")
                        cursor = self.connection.cursor()
                        try:
                            cursor.execute(
                                "UPDATE personne SET  prenompersonne = %s, datecipersonne=%s,nevers = %s, "
                                "lieucipersonne = %s, adressepersonne = %s, nompere = %s, nommere = %s, "
                                "numactenaissancepersonne = %s, dateactenaissancepersonne = %s, lieuactenaissancepersonne = %s,situationmatrimoniale = %s WHERE numcipersonne = %s",(
                                    prenoms,
                                    date_cin,
                                    nevers,
                                    lieu_cin,
                                    adresse,
                                    nom_pere,
                                    nom_mere,
                                    num_acte,
                                    date_acte,
                                    lieu_acte,
                                    sit_matri,
                                    num_cin
                                ))
                            self.connection.commit()
                            self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
                                      "Personne %s" % (num_cin), "green")
                        except Exception as err:
                            self.connection.rollback()
                            # self.saveErrorLine(ligneToLog, writer)
                            self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, str(err), "red")
                            print(err)

                    else:
                        cursor = self.connection.cursor()
                        try:
                            cursor.execute(
                                "UPDATE personne SET "
                                "nompersonne = %s, "
                                "prenompersonne = %s ,"
                                "sexepersonne = %s,"
                                "numcipersonne = %s,"
                                " lieucipersonne = %s,"
                                " adressepersonne = %s,"
                                "situationmatrimoniale = %s, "
                                "datecipersonne = %s, nevers = %s,"
                                "nompere = %s, "
                                "nommere = %s,"
                                "numactenaissancepersonne = %s, dateactenaissancepersonne = %s, lieuactenaissancepersonne = %s "
                                "WHERE UPPER(TRIM(nompersonne)) = UPPER(TRIM(CONCAT(%s,' ',%s)))" , (
                                    nom, prenoms,
                                    sexe,
                                    num_cin,
                                    lieu_cin,
                                    adresse, sit_matri,
                                    date_cin,
                                    nevers,
                                    nom_pere,
                                    nom_mere,
                                    num_acte,
                                    date_acte,
                                    lieu_acte,
                                    nom, prenoms
                                ))
                            self.connection.commit()
                            self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
                                      "Personne %s" % (num_cin), "green")
                        except Exception as err:
                            self.connection.rollback()
                            # self.saveErrorLine(ligneToLog, writer)
                            self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, str(err), "red")
                            print(err)
                else: #cas date naissance non vide
                    if self.exists("personne", "numcipersonne", num_cin):
                        self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
                                  "Personne %s existe deja en base" % (num_cin), "orange")
                        cursor = self.connection.cursor()
                        try:
                            cursor.execute(
                                "UPDATE personne SET  prenompersonne = %s, datenaissancepersonne = %s, datecipersonne=%s,nevers = %s, "
                                "lieucipersonne = %s, adressepersonne = %s WHERE numcipersonne = %s",(
                                    prenoms,
                                    date_naissance,
                                    date_cin,
                                    nevers,
                                    lieu_cin,
                                    adresse,
                                    num_cin
                                ))
                            self.connection.commit()
                            self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
                                      "Personne %s" % (num_cin), "green")
                        except Exception as err:
                            self.connection.rollback()
                            # self.saveErrorLine(ligneToLog, writer)
                            self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, str(err), "red")
                            print(err)

                    else:
                        cursor = self.connection.cursor()
                        try:
                            cursor.execute(
                                "UPDATE personne SET "
                                "nompersonne = %s, "
                                "prenompersonne = %s ,"
                                "sexepersonne = %s,"
                                "numcipersonne = %s,"
                                " lieucipersonne = %s,"
                                " adressepersonne = %s,"
                                "situationmatrimoniale = %s, "
                                "datenaissancepersonne = %s, "
                                "datecipersonne = %s, nevers = %s "
                                "WHERE TRIM(nompersonne) = TRIM(CONCAT(%s,' ',%s))" , (
                                    nom, prenoms,
                                    sexe,
                                    num_cin,
                                    lieu_cin,
                                    adresse, sit_matri,
                                    date_naissance,
                                    date_cin,
                                    nevers,
                                    nom, prenoms
                                ))
                            self.connection.commit()
                            self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
                                      "Personne %s" % (num_cin), "green")
                        except Exception as err:
                            self.connection.rollback()
                            # self.saveErrorLine(ligneToLog, writer)
                            self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, str(err), "red")
                            print(err)
            p = (line + 1) * 100 / total_lignes
            self.emit(SIGNAL("progress(int)"), p)
            line = line + 1


    def traiter_date(self,date_chaine):
        try:
            return datetime.strptime(date_chaine,'%d/%m/%Y').date()
        except Exception as err:
            print (err)
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

        try:
            wb = open_workbook(self.filename, encoding_override="utf8")
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
