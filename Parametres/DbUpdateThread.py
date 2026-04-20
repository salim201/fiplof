from PyQt4.QtCore import QThread, pyqtSignal
import subprocess
import os
from Configuration import DbConfig
import psycopg2

class DbUpdateThread(QThread):
    messageAddedSignal = pyqtSignal(str)
    doneSignal = pyqtSignal()

    def __init__(self, pgdump, filename, nomBase):
        QThread.__init__(self)
        self.db_config = DbConfig.DbConfig()
        self.pgdump, self.filename = pgdump, filename
        self.nomBase = nomBase
        self.connection = psycopg2.connect(database=self.db_config.db_name, user=self.db_config.db_user,
                                           password=self.db_config.db_pass, host=self.db_config.db_host)


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
        file_extension = open(self.filename, "r")
        sql = file_extension.read()
        self.executeSql(sql)
    '''
    def run_import(self):
        bat = self.create_batfile()
        proc = subprocess.Popen([bat], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        while True:
            output = proc.stdout.readline()
            if output == '' and proc.poll() is not None:
                break
            if output:
                self.messageAddedSignal.emit(output.strip())
        proc.poll()
        self.doneSignal.emit()
        os.remove(bat)
    '''
    def create_batfile(self):
        restore_exe = self.pgdump
        psql_exe = os.path.dirname(restore_exe) + "/psql.exe"
        dirname = os.path.dirname(__file__)

        file_extension = open(dirname + "/create_extension.sql", "r")
        content_extension = file_extension.read()
        print content_extension

        string_schema = "UPDATE pg_database SET datallowconn = 'false' WHERE datname = '"+self.nomBase+"';" \
        "\nSELECT pg_terminate_backend(pid)"\
        "\nFROM pg_stat_activity"\
        "\nWHERE datname = '"+self.nomBase+"';"\
        "\nDROP DATABASE IF EXISTS "+self.nomBase+";"\
        "\n--"\
        "\n-- TOC entry 4775 (class 1262 OID 93991)"\
        "\n-- Name: "+self.nomBase+"; Type: DATABASE; Schema: -; Owner: postgres"\
        "\n--" \
        "\n DROP USER IF EXISTS plof ;" \
        "\n CREATE ROLE plof LOGIN PASSWORD 'plof';" \
        "\nCREATE DATABASE "+self.nomBase+" WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'French_France.1252' LC_CTYPE = 'French_France.1252';" \
        "\nUPDATE pg_database SET datallowconn = 'true' WHERE datname = '" + self.nomBase + "';" \
        "\n\c "+self.nomBase+";"\
        "\nSET postgis.gdal_enabled_drivers = 'ENABLE_ALL';"\

        string_schema = string_schema + content_extension



        fichier = open(dirname + "/schema_plof.sql", "w")
        fichier.write(string_schema)
        fichier.close()
        schema_filename = dirname + "/schema_plof.sql"
        plof_schema = dirname + "/plof_schema.sql"
        bat = dirname + "/import.bat"
        fd = os.open(bat, os.O_WRONLY | os.O_CREAT)
        os.write(fd, "@echo on\n")
        os.write(fd, "SET PGPASSWORD=postgres\n")
        #os.write(fd, "\"%s\" -U postgres < \"%s\"\n" % (psql_exe, plof_schema))
        #os.write(fd, "\"%s\" --host localhost "
                     #"--port 5432 "
                     #"--username \"postgres\" --dbname \"%s\"  "
                     #"--verbose \"%s\"\n" % (restore_exe, self.db_config.db_name, self.filename))
        '''
        os.write(fd, "psql --host \"%s\" "
                     "--port \"%s\" "
                     "--username postgres "
                     "< \"%s\"\n" % (self.db_config.db_host, self.db_config.db_port, schema_filename))
        '''
        os.write(fd, "psql --host \"%s\" "
                     "--port \"%s\" "
                     "--username postgres -d \"%s\" "
                     "< \"%s\"\n" % (self.db_config.db_host,self.db_config.db_port, self.nomBase,self.filename))
        os.close(fd)
        return bat

    def execute(self, file):
        content = None
        print('Execute %s' % file)
        with open(file, 'r') as f:
            content = f.read()
            content = content.decode('utf-8-sig')
        if content is not None:
            return self.executeSql(content)

    def executeSql(self, sql):
        tab_sql = sql.split(';')
        res = False
        print tab_sql
        for sql_ in tab_sql:
            cursor = self.connection.cursor()
            try:
                print("Executing %s" % sql_.strip())
                cursor.execute(sql_.strip())
                self.connection.commit()
            except Exception as e:
                print(e)
                self.connection.rollback()
                if str(e).__contains__("already exists") or str(e).__contains__("null argument to internal routine")  or str(e).__contains__("empty query") or str(e).__contains__("used by a view") or str(e).__contains__("multiple primary keys"):
                    res = True
            #cursor.close()
