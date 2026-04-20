#coding: utf-8
from usecases.migration.IMigrationRepository import IMigrationRepository
from PyQt4.QtGui import *
import subprocess
import os
from Configuration import DbConfig


class MigrationPgRepository(IMigrationRepository):
    DEFAULT_LAST_EXECUTED_FILE = 'sql/2022-08-06-Suppression-geometrie-invalide.sql'
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.db_config = DbConfig.DbConfig()
        self.__createMigrationTable()

    def getLastExecutedFile(self):
        self.cursor.execute("SELECT filename FROM migration_history")
        res = self.cursor.fetchone()
        if res is not None:
            return res[0]
        return None

    def execute(self, file):
        content = None
        print('Execute %s' % file)
        with open(file, 'r') as f:
            content = f.read()
            content = content.decode('utf-8-sig')
        if content is not None:
            if not content.__contains__('$$'):
                return self.executeSql(content)
            else:
                return self.run_import(file)
    def saveLastExecutedFile(self, file):
        self.executeSql("DELETE FROM migration_history")
        self.executeSql("INSERT INTO migration_history(filename, migration_date) VALUES('%s', now());" % (file))

    def __migrationTableExists(self):
        self.cursor.execute("SELECT EXISTS (SELECT * FROM pg_tables WHERE schemaname='public' AND tablename='migration_history')");
        res = self.cursor.fetchone()
        return res[0]


    def __createMigrationTable(self):
        if not self.__migrationTableExists():
            self.executeSql("CREATE TABLE IF NOT EXISTS migration_history(filename character varying(128), migration_date timestamp);")
            self.executeSql("INSERT INTO migration_history(filename, migration_date) VALUES('%s', now());" % (self.DEFAULT_LAST_EXECUTED_FILE))\

    def executeSql(self, sql):
        tab_sql = sql.split(';')
        res = False
        for sql_ in tab_sql:
            try:
                print("Executing %s" % sql_.strip())
                self.cursor.execute(sql_.strip())
                self.connection.commit()
                res =  True
            except Exception as e:
                print(e)
                self.connection.rollback()
                if (sql_.__contains__('DROP') or sql_.__contains__('drop')) and (str(e).__contains__("does not exist") or str(e).__contains__("n'existe pas")):
                    res = True
                elif str(e).__contains__("valeur_ha") or str(e).__contains__("already exists") or str(e).__contains__(u"existe déjà") or str(e).__contains__("null argument to internal routine") or str(e).__contains__("argument nul") or str(e).__contains__("empty query") or str(e).__contains__(u"requête vide") or str(e).__contains__("used by a view") or str(e).__contains__(u"utilisé par une vue") or str(e).__contains__("multiple primary keys") or str(e).__contains__(u"clés primaires multiple"):
                    res = True
                else:
                    erreur = u"Des erreurs lors de la mise à jour de la base de données. Cette erreur peut declencher un disfonctionnement dans FIPLOF. Une maintenance de la base est nécéssaire pour que la mise à jour de la base soit possible. \nDétails de l'erreur :\n" + str(e)
                    QMessageBox.warning(None, "Attention!", erreur)
                    return False
        return res

    def create_batfile(self, file):
        #restore_exe = self.pgdump
        #psql_exe = os.path.dirname(restore_exe) + "/psql.exe"
        dirname = os.path.dirname(__file__)
        bat = dirname + "/import.bat"
        fd = os.open(bat, os.O_WRONLY | os.O_CREAT)
        os.write(fd, "@echo on\n")
        # os.write(fd, "SET PGPASSWORD=postgres\n" % self.db_config.db_pass)
        os.write(fd, "SET PGPASSWORD=%s\n" % (self.db_config.db_pass,))

        os.write(fd, "psql --host %s "
                     "--port %s "
                     "--username %s -d %s "
                     "-f \"%s\"\n" % (self.db_config.db_host, self.db_config.db_port, self.db_config.db_user, self.db_config.db_name, file))


        os.close(fd)
        return bat

    def run_import(self, file):
        bat = self.create_batfile(file)
        proc = subprocess.Popen([bat], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        while True:
            output = proc.stdout.readline()
            if output == '' and proc.poll() is not None:
                break
            if output:
                print(output.strip())
        proc.poll()
        os.remove(bat)
        return True

