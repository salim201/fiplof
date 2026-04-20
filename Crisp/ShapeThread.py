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
from xlrd import open_workbook
import xlrd
import io
import qgis
from qgis.core import *
from PyQt4 import QtCore, QtGui
from logs import xlsLogger

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


class ShapeThread(QThread):
    def __init__(self, filename, connection, iscorrection = False):
        QThread.__init__(self)
        self.filename, self.connection = filename, connection
        self.current_step =-1
        self.logger = xlsLogger.xlsLogger("Import_Shapefile")
        self.iscorrection = iscorrection

    def __del__(self):
        self.wait()

    def run(self):
        #print (self.filename)
        if self.filename == "":
            self.emit(SIGNAL("alert(QString)"), "Veuillez choisir un fichier")
            return
        self.idCommune = int(globalvars.id_commune)
        # poDS = ogr.Open(str(self.filename), False)
        # if poDS is None:
        # self.emit(SIGNAL("alert(QString)"), "Fichier ogr non valide")
        # return
        self.current_step = -1

        #IMPORT PARCELLE
        self.emit(SIGNAL("stepInit(int)"), self.current_step + 1)
        print("Debut import Parcelle")
        self.importParcelle()
        print("Fin import Parcelle")
        self.logger.write()
        self.emit(SIGNAL("stepDone(int)"), self.current_step)
        #FIN IMPORT PERSONNE PHYSIQUE


    def importParcelle(self):
        #Preparation log
        title = ["code_parcelle", "numero_demande", "etat_insertion", "erreur"]
        dataToLog = []
        #fin prep    log
        self.current_step = self.current_step + 1
        self.emit(SIGNAL("clearSubstep(int)"), self.current_step)
        cursor = self.connection.cursor()
        print ("IMPORT DEMANDE")
        self.emit(SIGNAL("clearSubstep(int)"), self.current_step)

        filename = _fromUtf8(self.filename)
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
            code_parcelle,numdemande, etatInsertion,erreur = " "," "," "," "
            dataToAppend = {}
            try:
                geometry = f.geometry()
                if geometry.wkbType() == QGis.WKBPolygon:
                    x = geometry.asPolygon()
                if geometry.wkbType() == QGis.WKBMultiPolygon:
                    x = geometry.asMultiPolygon()[0]

                attrs = f.attributes()
                size = len(attrs)
                print(attrs)
                try:
                    num = ""

                    codeParcelle = attrs[1].toPyObject()
                    print(codeParcelle)
                    print(" code parcelle--")
                    code_parcelle = str(codeParcelle)

                    # NumDemande = self.NumDemande+" "+str(attrs[2].toPyObject())
                    print('Geometry.exportToWkt()')
                    print(str(geometry.exportToWkt()))
                    where = "codeparcelle = '" + code_parcelle + "' and id_commune = " + str(self.idCommune)
                    if self.select("parcelle_d", "gid", where) is not None:
                        print "code parcelle existant"
                        if self.iscorrection:
                            exe = cursor.execute(
                                "UPDATE parcelle_d SET geom = ST_GeomFromText(%s, " + str(globalvars.EPSG_SCR) + ") ,surface = ST_Area(%s) WHERE codeparcelle  = %s AND id_commune = %s returning gid,surface",
                                (str(geometry.exportToWkt()), str(geometry.exportToWkt()), str(codeParcelle),
                                 self.idCommune))
                            self.connection.commit()
                            etatInsertion = "CODE PARCELLE EN DOUBLON MISE A JOUR REUSSIE"
                        else:
                            exe = cursor.execute(
                                "SELECT gid, surface FROM parcelle_d WHERE codeparcelle  = %s AND id_commune = %s ",
                                (str(codeParcelle),
                                 self.idCommune))
                            etatInsertion = "CODE PARCELLE EN DOUBLON"

                    else:
                        exe = cursor.execute(
                            "INSERT INTO parcelle_d (geom,surface ,codeparcelle,id_commune)VALUES (ST_GeomFromText(%s, " + str(
                                globalvars.EPSG_SCR) + "),ST_Area(%s), %s, %s) returning gid,surface",
                            (str(geometry.exportToWkt()), str(geometry.exportToWkt()), str(codeParcelle), self.idCommune))
                        self.connection.commit()
                        etatInsertion = "INSERTION  REUSSIE"
                    #self.logger.appendLine(code_parcelle=str(codeParcelle), etatInsertion="INSERTION REUSSIE")
                    self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step,
                              u"Parcelle %s insérée dans la base" % (str(codeParcelle)), "green")
                    print("AFTER commit")
                    dm = cursor.fetchone()
                    gid = dm[0]


                    #self.progress(p)

                    # #insert into table demande
                    # self.ui.numeroDemandeLineEdit.setText(
                    #     _fromUtf8(chDistrict + "-" + chCodeGuichet) + "-F-" + str(self.currentValDemande))
                except Exception as e:
                    TabCodeParcelle.append(codeParcelle)
                    self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, str(e), "red")
                    etatInsertion="ECHEC INSERTION"
                    erreur=str(e)
                    self.connection.rollback()
                    print(e)

            except Exception as e:
                print(e)
                etatInsertion="ECHEC INSERTION"
                erreur=str(e)
                print(' parcelle ayant des probleme de geometrie')

            if gid is not None:
                if code_parcelle == '':
                    codParcel = None
                else:
                    codParcel = code_parcelle

                try:
                    cur = self.connection.cursor()
                    cur.execute('INSERT INTO demande (code_parcelle, gid, idcommune) VALUES (%s, %s, %s)', (codParcel, gid, self.idCommune))
                    self.connection.commit()
                    #cur.close()
                except Exception as err:
                    print err
                    self.connection.rollback()

            p = (i + 1) * 100 / countFeatures
            self.emit(SIGNAL("progress(int)"), p)
            
            #Ligne dans LOg
            dataToLog.append({"code_parcelle": code_parcelle, "numero_demande": numdemande, "etat_insertion": etatInsertion,
                    "erreur": erreur})
            i = i + 1

        print(TabCodeParcelle)
        self.logger.addSheet(title=title, data = dataToLog, sheet_name="Log Import Shape")

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