from usecases.ogrimporter.IDataMapper import IDataMapper
import re
import psycopg2
import psycopg2.extras
from Configuration import DbConfig
db_config = DbConfig.DbConfig()



class ProprietaireMapper(IDataMapper):
    def __init__(self):
        self.connection = psycopg2.connect(database=db_config.db_name, user=db_config.db_user,
                                       password=db_config.db_pass, host=db_config.db_host)
    def getDestinationTableName(self):
        return "proprietaireparcelle"

    def getSourceQuery(self):
        return 'SELECT * FROM proprietaire'

    def map(self, row):
        return [
            {'idparcelle': self.__getIdParcelle(row)},
            {'idpersonne': self.__getIdPersonne(row)},
            {'representant': self.__defineRepresentant(row)}
        ]

    def __getIdPersonne(self, row):
        cur = self.connection.cursor()
        try:
            cur.execute('SELECT idpersonne FROM personne WHERE csv_id = %s', (str(row['numeroProprietaire']).strip(),))
            res = cur.fetchone()
            return res[0]
        except Exception as err:
            print(err)
            self.connection.rollback()

    def __getIdParcelle(self, row):
        cur = self.connection.cursor()
        try:
            cur.execute('SELECT gid FROM parcelle_d WHERE idcertificat = (SELECT idcertificat FROM certificat WHERE numerocertificat = %s)', (str(row['numeroCertificat']).strip(),))
            res = cur.fetchone()
            return res[0]
        except Exception as err:
            print(err)
            self.connection.rollback()

    def __defineRepresentant(self, row):
        cur = self.connection.cursor()
        try:
            cur.execute(
                'SELECT COUNT(idpersonne) FROM proprietaireparcelle WHERE representant = %s and idparcelle = (SELECT gid FROM parcelle_d WHERE idcertificat = (SELECT idcertificat FROM certificat WHERE numerocertificat = %s))',
                (True, str(row['numeroCertificat']).strip()))
            res = cur.fetchone()
            if res[0] == 0:
                return True
            else:
                return False
        except Exception as err:
            print(err)
            self.connection.rollback()
            return None
