from usecases.ogrimporter.IDataMapper import IDataMapper
import re
import psycopg2
import psycopg2.extras
from Configuration import DbConfig
db_config = DbConfig.DbConfig()



class VoisinsMapper(IDataMapper):
    def __init__(self):
        self.connection = psycopg2.connect(database=db_config.db_name, user=db_config.db_user,
                                       password=db_config.db_pass, host=db_config.db_host)
    def getDestinationTableName(self):
        return "limitesparcelle"

    def getSourceQuery(self):
        return 'SELECT * FROM limiteEtRepere'

    def map(self, row):
        return [
            {'idparcelle': self.__getIdParcelle(row)},
            {'idpointscardinaux': self.__getIdPoint(row)},
            {'description': row['description']}
        ]

    def __getIdPoint(self, row):
        # 1 Nord, 2 Sud, 3 Ouest, 4 Est, 10 Ouest
        position = ""
        if row['numeroPosition'] == 1:
            position = 'Nord'
        elif row['numeroPosition'] == 2:
            position = 'Sud'
        elif row['numeroPosition'] == 3 or row['numeroPosition'] == 10:
            position = 'Ouest'
        else:
            position = 'Est'

        cur = self.connection.cursor()
        try:
            cur.execute('SELECT idpointscardinaux FROM pointscardinaux WHERE TRIM(position) = %s', (str(position).strip(),))
            res = cur.fetchone()
            return res[0]
        except Exception as err:
            print(err)
            self.connection.rollback()

    def __getIdParcelle(self, row):
        cur = self.connection.cursor()
        try:
            cur.execute('SELECT gid FROM parcelle_d WHERE idcertificat = (SELECT idcertificat FROM certificat WHERE TRIM(numerocertificat) = %s)', (str(row['numeroCertificat']).strip(),))
            res = cur.fetchone()
            return res[0]
        except Exception as err:
            print(err)
            self.connection.rollback()

