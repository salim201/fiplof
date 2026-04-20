from usecases.ogrimporter.IDataMapper import IDataMapper
import re
import globalvars
from models.Fokontany import Fokontany
import psycopg2
import psycopg2.extras
from Configuration import DbConfig
db_config = DbConfig.DbConfig()

class CertificateMapper(IDataMapper):
    def __init__(self, connection):  # type:(any)->None
        fokontanyModel = Fokontany(connection)
        self.importedFokontany = fokontanyModel.find_all()
        self.connection = psycopg2.connect(database=db_config.db_name, user=db_config.db_user,
                                           password=db_config.db_pass, host=db_config.db_host)

    def getDestinationTableName(self):
        return 'certificat'

    def getSourceQuery(self):
        return 'SELECT * FROM certificat'

    def map(self, row):
        fokontanyId = self.__getFokontanyId(row)
        return [
            {'numerocertificat': row['numeroCertificat']},
            {'numerodemande': row['numeroDemande']},
            {'typecertificat': row['typeCertificat']},
            {'datecreation': self.__parseDate(row['dateCreation'])},
            {'dateedition': self.__parseDate(row['dateEdition'])},
            {'datedelivrance': self.__parseDate(row['dateDelivrance'])},
            {'memo': row['memo_']},
            {'idprojet': globalvars.id_projet},
            {'idcommune': globalvars.id_commune},
           # {'idfokontany': fokontanyId},
            {'idfokontany': self.__getIdFokontany(row)},
            {'idhameau': self.__getIdHameau(row)},
            {'code_hameau': row['hameau']}
        ]

    def getUnicityCheckConditions(self, row):
        return [{'numerocertificat': row[0]}]

    def __parseDate(self, date):
        if not re.match('\d{4}/\d{2}/\d{2}', date):
            return None
        return re.sub('/', '-', date)

    def __getFokontanyId(self, row):
        fkt = filter(lambda r: r.codefokontany == '0%s' % row['fokotany'], self.importedFokontany)
        if len(fkt) == 0:
            return None
        return fkt[0].idfokontany

    def __getIdFokontany(self, row):
        code_fkt = str(row['fokotany']).strip().replace("'","''")
        cur = self.connection.cursor()
        try:
            cur.execute('SELECT idfokontany from fokontany WHERE TRIM(codefokontany) = %s', (code_fkt,))
            res = cur.fetchone()
            return res[0]
        except Exception as err:
            print (err)
            self.connection.rollback()
            return None

    def __getIdHameau(self, row):
        if self.__getIdFokontany(row) is not None:
            code_hameau = str(row['hameau']).strip().replace("'", "''")
            idfkt = int(self.__getIdFokontany(row))
            cur = self.connection.cursor()
            try:
                cur.execute('SELECT idhameau from hameau WHERE TRIM(codehameau) = %s and idfokontany = %s',
                            (code_hameau, idfkt))
                res = cur.fetchone()
                return res[0]
            except Exception as err:
                print (err)
                self.connection.rollback()
                return None
        else:
            return None
