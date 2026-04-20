# coding: utf8
from PyQt4.QtCore import QThread, SIGNAL, pyqtSignal
# import ogrinfo
import sys
import os
import os.path
from qgis.core import *
from PyQt4 import QtCore, QtGui
from logs import xlsLogger
import subprocess
from Configuration import DbConfig
import datetime
import globalvars
import tempfile

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


class ExportDataThread(QThread):
    messageAddedSignal = pyqtSignal(str)
    doneSignal = pyqtSignal()

    def __init__(self, pgdump, filename, connection, isGuData):
        QThread.__init__(self)
        self.filename, self.connection = filename, connection
        self.dirname = filename
        self.dstfile = ""
        self.pgdump = pgdump
        self.current_step = -1
        self.db_config = DbConfig.DbConfig()
        self.isGuData = isGuData
        self.logger = xlsLogger.xlsLogger("Export DATA")

    def __del__(self):
        self.wait()

    def run(self):
        if self.filename == "":
            self.emit(SIGNAL("alert(QString)"), "Veuillez choisir un dossier")
            return

        self.current_step = -1

        self.emit(SIGNAL("stepInit(int)"), self.current_step + 1)
        date_jour = datetime.datetime.now().strftime("%Y-%m-%d")
        nom_commune = "comm_" + self.get_commune_name().replace(" ","_").lower() + "_"
        if self.isGuData:
            try:
                self.dstfile = str(os.path.join(str(self.dirname), nom_commune + date_jour + "_guichet_unique.7z"))
                self.filename = os.path.join(tempfile.gettempdir(), str(nom_commune + date_jour + "_guichet_unique.sql"))
            except Exception as err:
                print ('erreur path join')
                print (err)
            #self.filename = self.dirname + "/titre.sql"
            print ("***************filename****************")
            print (self.filename)
            try:
                self.run_dump()
            except Exception as err:
                print ("Erreur run dump " + str(err))
        else:
            try:
                self.dstfile = str(os.path.join(str(self.dirname), nom_commune + date_jour + "_guichet_foncier.7z"))
                self.filename = os.path.join(tempfile.gettempdir(),
                                             str(nom_commune + date_jour + "_guichet_foncier.sql"))
            except Exception as err:
                print ('erreur path join')
                print (err)
            # self.filename = self.dirname + "/titre.sql"
            print ("***************filename****************")
            print (self.filename)
            print (self.db_config.db_pass)
            try:
                self.run_dump()
            except Exception as err:
                print ("Erreur run dump " + str(err))
        #self.generateSqlText()

    def run_dump(self):
        os.putenv("PGPASSWORD", self.db_config.db_pass)
        print ("openning subprocess")
        print('in run dump ' + self.filename)
        if not os.path.exists(self.pgdump):
            print ("*****Path not existing*****")
            if os.path.exists("C:\\Program Files\\PostgreSQL\\15\\bin\\pg_dump.exe"):
                self.pgdump = "C:\\Program Files\\PostgreSQL\\15\\bin\\pg_dump.exe"
            else:
                if os.path.exists("C:\\Program Files\\PostgreSQL\\9.3\\bin\\pg_dump.exe"):
                    self.pgdump = "C:\\Program Files\\PostgreSQL\\9.3\\bin\\pg_dump.exe"
                else:
                    if os.path.exists("C:\\Program Files(x86)\\PostgreSQL\\9.3\\bin\\pg_dump.exe"):
                        self.pgdump = "C:\\Program Files(x86)\\PostgreSQL\\9.3\\bin\\pg_dump.exe"
        print ("****************self.pgdump******************")
        print (self.pgdump)

        if self.isGuData:
            proc = subprocess.Popen(
                [
                    "%s" % (self.pgdump,),
                    "-U", self.db_config.db_user,
                    "-c",
                    "-d", self.db_config.db_name,
                    "-t", "titre",
                    "-t", "vw_titre",
                    "-t", "pk_titre",
                    "-t", "cadastre",
                    "-t", "vw_cadastre",
                    "-t", "pk_cadastre",
                    "-t", "demandefn",
                    "-t", "vw_demandefn",
                    "-t", "pk_demandefn",
                    "-t", "terain_status_specifique",
                    "-t", "vw_tss",
                    "-t", "pk_tss",
                    "-t", "z_certifiable",
                    "-t", "vw_z_certifiable",
                    "-t", "z_certifiable_pkey",
                    "-f", self.filename,
                    "--verbose"
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True
            )
        else:
            proc = subprocess.Popen(
                [
                    "%s" % (self.pgdump,),
                    "-U", self.db_config.db_user,
                    "-c",
                    "-d", self.db_config.db_name,
                    "-t", "region",
                    "-t", "district",
                    "-t", "commune",
                    "-t", "projet",
                    "-t", "projet_commune",
                    "-t", "projetcouche",
                    "-t", "fokontany",
                    "-t", "hameau",
                    "-t", "acteprive",
                    "-t", "actepublic",
                    "-t", "type_anomalie",
                    "-t", "anomalie",
                    "-t", "autrecharge",
                    "-t", "beneficiaire",
                    "-t", "categorie",
                    "-t", "classe",
                    "-t", "consistance",
                    "-t", "consistance_batiment",
                    "-t", "contribuable",
                    "-t", "demande_sans_geom",
                    "-t", "fokontany",
                    "-t", "hypotheque",
                    "-t", "impot",
                    "-t", "impot_minimum",
                    "-t", "menage",
                    "-t", "parcellegrevees",
                    "-t", "path_personne",
                    "-t", "avoirconjoint",
                    "-t", "personne",
                    "-t", "rejet",
                    "-t", "role_crl",
                    "-t", "servitude",
                    "-t", "document",
                    "-t", "type_document",
                    "-t", "typeforfaitaire",
                    "-t", "parcelle",
                    "-t", "hameau",
                    "-t", "certificat",
                    "-t", "vw_certificat",
                    "-t", "vw_shape_certificat",
                    "-t", "parcelle_d",
                    "-t", "demande",
                    "-t", "vw_demande",
                    "-t", "vw_shape_demande",
                    "-t", "autrechargesparcelle_d",
                    "-t", "avoir_demande",
                    "-t", "batiment",
                    "-t", "blob_personne",
                    "-t", "blob_history",
                    "-t", "limitesparcelle",
                    "-t", "blob_voisin",
                    "-t", "categorieforfaitaire",
                    "-t", "classecategorieforfaitaire",
                    "-t", "consistanceforfaitaire",
                    "-t", "contribuableconsorts",
                    "-t", "contribuables_parcelle",
                    "-t", "demande_anomalie",
                    "-t", "demande_crl",
                    "-t", "demande",
                    "-t", "fi_paiement_impot",
                    "-t", "historique",
                    "-t", "hypothequeparcelle_d",
                    "-t", "impot_batiment",
                    "-t", "impot_contribuable",
                    "-t", "impot_parcelle",
                    "-t", "impotparcelle",
                    "-t", "journal",
                    "-t", "operationsub",
                    "-t", "oppositions",
                    "-t", "personne_menage",
                    "-t", "personne_morale",
                    "-t", "personnemoraleparcelle_d",
                    "-t", "proprietaireparcelle",
                    "-t", "servitudebeneficiaire",
                    "-t", "servitudeparcelle_d",
                    "-t", "servitudeparcellegrevees",
                    "-t", "actepublicsubsequente",
                    "-t", "acteprivesubsequente",
                    "-t", "proprietaireparcelle_d",
                    "-t", "avoir_dmd",
                    "-t", "personnemoraleparcelle",
                    "-t", "actedecessubsequente",
                    "-t", "decisionsubsequente",
                    "-t", "operationsubsequente",
                    "-t", "vw_fiscalite",
                    "-f", self.filename,
                    "--verbose"
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True
            )
        while True:
            output = proc.stdout.readline()
            if output == '' and proc.poll() is not None:
                break
            if output:
                print (output)
                pass
                #self.messageAddedSignal.emit(output.strip())
        proc.poll()
        self.compressFile()
        print ("after polling the process")
        self.doneSignal.emit()

    def compressFile(self):
        #dst = self.filename.replace("sql", "7z")
        directory_of_file = os.path.dirname(__file__)
        tab_dir = directory_of_file.split("\\")
        last_elt = tab_dir[(len(tab_dir) - 1)]
        directory = ""
        i = 0
        for tab in tab_dir:
            if i == 0:
                directory = tab
            else:
                if i == len(tab_dir) - 1:
                    directory = directory + "\\7z"
                else:
                    directory = directory + "\\" + tab
            i = i + 1

        print ("*****************path of 7z***********************")
        print (directory)
        file_to_exec = directory + "\\7z.exe"
        proc = subprocess.Popen(
            [
                "%s" % (file_to_exec,),
                "a", self.dstfile,
                " ",self.filename,
                "-pSaveF1pl0xchange@interc0L1ne0ff",
                "-sdel"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True
        )
        while True:
            output = proc.stdout.readline()
            if output == '' and proc.poll() is not None:
                break
            if output:
                pass
                #self.messageAddedSignal.emit(output.strip())
        proc.poll()
        #os.popen()

    def generateSqlText(self):
        fields = self.getAllFieldsOfTable("parcelle_d")
        print "*****FIELDS*************"
        tuples_fields = tuple(fields)
        print tuples_fields
        datas = self.getAllDataOfTable("parcelle_d")
        print "*********DATA**************"
        print datas[0]
        self.generateInsertScript("parcelle_d", tuples_fields,datas[0])
        self.doneSignal.emit()

    def getAllFieldsOfTable(self, tablename):
        cursor = self.connection.cursor()
        fields = []
        rows = None
        try:
            cursor.execute('SELECT attname FROM pg_class, pg_attribute WHERE pg_class.relname = %s '
                           'and pg_class.relfilenode = pg_attribute.attrelid '
                           'and pg_attribute.attnum > 0', (tablename,))
            rows = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(e)
            self.connection.rollback()

        for row in rows:
            fields.append(row[0])

        return fields

    def getAllDataOfTable(self, tablename):
        cursor = self.connection.cursor()
        rows = None
        try:
            cursor.execute("SELECT * FROM " + tablename)
            rows = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(e)
            self.connection.rollback()

        return rows

    def generateInsertScript(self, tablename, fields, data):
        #sql_delete = "DELETE FROM " + tablename + ";\n"
        sql_insert = "INSERT INTO " + tablename + " " + str(fields) + " VALUES " + str(data) + ";"
        print sql_insert

    def get_commune_name(self):
        res = None
        try:
            cur = self.connection.cursor()
            cur.execute("SELECT nomcommune from commune where idcommune = %s", (globalvars.id_commune,))
            res = cur.fetchone()
        except Exception as err:
            print ("Erreur get nomcommune " + str(err))
        if res is not None:
            return str(res[0]).strip()
        else:
            return ""

