# coding: utf-8
from PyQt4.QtCore import QThread, pyqtSignal
import subprocess
import os
from Configuration import DbConfig
import psycopg2
import globalvars

class DbExportThread(QThread):
    messageAddedSignal = pyqtSignal(str)
    doneSignal = pyqtSignal()

    def __init__(self, pgdump, filename, nomBase, isImportData = False):
        QThread.__init__(self)
        self.db_config = DbConfig.DbConfig()
        self.pgdump, self.filename = pgdump, filename.decode('utf-8')
        self.nomBase = str(nomBase)
        self.isImportData = isImportData

    def __del__(self):
        self.wait()

    def run(self):
        if "dump" in self.pgdump:
            self.run_dump()
        else:
            self.run_import()

    def run_dump(self):
        os.putenv("PGPASSWORD", self.db_config.db_pass)
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

    def run_import(self):
        if self.isImportData:
            nom_commune = self.get_nom_commune()
            res = self.compare_filename_to_commune(nom_commune, self.filename)
            if not res:
                print res
                self.messageAddedSignal.emit(u"La commune correspondant au fichier n'existe pas dans la base de données")
                self.doneSignal.emit()
                return
        bat = self.create_batfile()
        proc = subprocess.Popen([bat], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        while True:
            output = proc.stdout.readline()
            if output == '' and proc.poll() is not None:
                break
            if output:
                self.messageAddedSignal.emit(output.strip())
                print(output.strip())
        proc.poll()
        self.doneSignal.emit()
        os.remove(bat)

    def create_batfile(self):
        restore_exe = self.pgdump
        psql_exe = os.path.dirname(restore_exe) + "/psql.exe"
        dirname = os.path.dirname(__file__)

        file_extension = open(dirname + "/create_extension.sql", "r")
        content_extension = file_extension.read()
        print content_extension

        if not self.isImportData:
            string_schema = "UPDATE pg_database SET datallowconn = 'false' WHERE datname = '"+self.nomBase+"';" \
            "\nSELECT pg_terminate_backend(pid)"\
            "\nFROM pg_stat_activity"\
            "\nWHERE datname = '"+self.nomBase+"';"\
            "\nDROP DATABASE IF EXISTS "+self.nomBase+";"\
            "\n--"\
            "\n-- TOC entry 4775 (class 1262 OID 93991)"\
            "\n-- Name: "+self.nomBase+"; Type: DATABASE; Schema: -; Owner: "+self.db_config.db_user+""\
            "\n--" \
            "\n DROP USER IF EXISTS plof ;" \
            "\n CREATE ROLE plof LOGIN PASSWORD 'plof';" \
            "\nCREATE DATABASE "+self.nomBase+" WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'French_France.1252' LC_CTYPE = 'French_France.1252';" \
            "\nUPDATE pg_database SET datallowconn = 'true' WHERE datname = '" + self.nomBase + "';" \
            "\n\c "+self.nomBase+";"\
            "\nSET postgis.gdal_enabled_drivers = 'ENABLE_ALL';"\

            string_schema = string_schema + content_extension
        else:
            string_schema = "UPDATE pg_database SET datallowconn = 'false' WHERE datname = '" + self.nomBase + "';" \
            "\nSELECT pg_terminate_backend(pid)" \
            "\nFROM pg_stat_activity" \
            "\nWHERE datname = '" + self.nomBase + "';" \
            "\nUPDATE pg_database SET datallowconn = 'true' WHERE datname = '" + self.nomBase + "';" \
            "\n\c " + self.nomBase + ";" \

            string_schema.replace('postgres', self.db_config.db_user)




        fichier = open(dirname + "/schema_plof.sql", "w")
        fichier.write(string_schema)
        fichier.close()
        schema_filename = dirname + "/schema_plof.sql"
        plof_schema = dirname + "/plof_schema.sql"
        bat = dirname + "/import.bat"
        fd = os.open(bat, os.O_WRONLY | os.O_CREAT)
        os.write(fd, "@echo on\n")
        # os.write(fd, "SET PGPASSWORD=postgres\n" % self.db_config.db_pass)
        os.write(fd, "SET PGPASSWORD=%s\n" % (self.db_config.db_pass,))

        #os.write(fd, "\"%s\" -U postgres < \"%s\"\n" % (psql_exe, plof_schema))
        #os.write(fd, "\"%s\" --host localhost "
                     #"--port 5432 "
                     #"--username \"postgres\" --dbname \"%s\"  "
                     #"--verbose \"%s\"\n" % (restore_exe, self.db_config.db_name, self.filename))


        os.write(fd, "psql --host %s "
                         "--port %s "
                         "--username %s "
                         "-f \"%s\"\n" % (self.db_config.db_host, self.db_config.db_port, self.db_config.db_user, schema_filename))




        os.write(fd, "psql --host %s "
                     "--port %s "
                     "--username %s -d %s "
                     "-f \"%s\"\n" % (self.db_config.db_host, self.db_config.db_port, self.db_config.db_user, self.nomBase, self.filename))



        os.close(fd)
        return bat

    def get_nom_commune(self):
        connection = psycopg2.connect(database=self.db_config.db_name, user=self.db_config.db_user,
                                      password=self.db_config.db_pass, host=self.db_config.db_host)
        res = None
        try:
            cur = connection.cursor()
            cur.execute("SELECT nomcommune FROM commune WHERE idcommune = %s", (globalvars.id_commune,))
            res = cur.fetchone()
        except Exception as err:
            print ("Error to get the name of the commune " + str(err))
        if res is None:
            return ""
        else:
            return str(res[0]).strip()


    def compare_filename_to_commune(self, nom_commune, nom_fichier):
        print ("***********FILENAME*********")
        print (nom_fichier)

        nom_comm = nom_commune.replace(" ", "_").lower()
        tab_fic = nom_fichier.split("/")

        print (tab_fic)
        fic = tab_fic[len(tab_fic) - 1]
        print (fic)
        if nom_comm in fic:
            return True
        else:
            return False
