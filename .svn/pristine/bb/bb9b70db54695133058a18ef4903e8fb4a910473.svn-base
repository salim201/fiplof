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
#from Configuration import ParamsConfig
from Configuration import IntercoConfig
import datetime
import globalvars
import hashlib

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class AutoBackupThread(QThread):
    messageAddedSignal = pyqtSignal(str)
    doneSignal = pyqtSignal()

    def __init__(self, pgdump, dirname, connection, parent):
        QThread.__init__(self)
        self.filename, self.connection = None, connection
        self.parent = parent
        self.dirname = dirname
        self.pgdump = pgdump
        self.current_step = -1
        self.db_config = DbConfig.DbConfig()
        self.interco_config = IntercoConfig.IntercoConfig()

    def __del__(self):
        self.wait()

    def run(self):
        if self.filename == "":
            self.emit(SIGNAL("alert(QString)"), "Veuillez choisir un dossier")
            return

        self.current_step = -1

        self.emit(SIGNAL("stepInit(int)"), self.current_step + 1)
        date_jour = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        nom_commune = "_comm_" + self.get_commune_name().replace(" ", "_").lower()
        if self.interco_config.auto_save_path != None and os.path.exists(str(self.interco_config.auto_save_path)):
            self.dirname = self.interco_config.auto_save_path

        self.filename = str(os.path.join(str(self.dirname), date_jour + nom_commune + "_autobackup.sql"))
        self.parent.filename = self.filename

        try:
            self.run_dump()
        except Exception as err:
            print (err)

    def run_dump(self):
        os.putenv("PGPASSWORD", self.db_config.db_pass)
        if not os.path.exists(self.pgdump):
            if os.path.exists("C:\\Program Files\\PostgreSQL\\15\\bin\\pg_dump.exe"):
                self.pgdump = "C:\\Program Files\\PostgreSQL\\15\\bin\\pg_dump.exe"
            else:
                if os.path.exists("C:\\Program Files\\PostgreSQL\\9.3\\bin\\pg_dump.exe"):
                    self.pgdump = "C:\\Program Files\\PostgreSQL\\9.3\\bin\\pg_dump.exe"
                else:
                    if os.path.exists("C:\\Program Files(x86)\\PostgreSQL\\9.3\\bin\\pg_dump.exe"):
                        self.pgdump = "C:\\Program Files(x86)\\PostgreSQL\\9.3\\bin\\pg_dump.exe"

        proc = subprocess.Popen(
            [
                "%s" % (self.pgdump,),
                "-U", self.db_config.db_user,
                "-h", self.db_config.db_host,
                "--file", self.filename,
                "--format", "p",
                "--blobs",
                #"--create",
                "--verbose",
                "%s" % self.db_config.db_name
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
                self.messageAddedSignal.emit(output.strip())
        proc.poll()
        self.doneSignal.emit()

    def get_commune_name(self):
        res = None
        try:
            cur = self.connection.cursor()
            cur.execute("SELECT nomcommune from commune where idcommune = %s", (globalvars.id_commune,))
            res = cur.fetchone()
            cur.close()
        except Exception as err:
            print ("Erreur get nomcommune " + str(err))
            self.connection.rollback()
        if res is not None:
            return str(res[0]).strip()
        else:
            return ""