import psycopg2
import psycopg2.extras


class Certificat:
    def __init__(self):
        self.numerocertificat, self.numerodemande, self.datereconnaissance, self.typecertificat, self.datecreation = \
            "", "", "", "", ""
        self.datedelivrance, self.memo, self.idcertificat = "", "", 0

    def map(self, res):
        self.numerocertificat, self.numerodemande, self.datereconnaissance, \
            self.typecertificat, self.datecreation, self.datedelivrance, self.memo, self.idcertificat = \
            res['numerocertificat'], res['numerodemande'], res['datereconnaissance'], \
            res['typecertificat'], res['datecreation'], res['datedelivrance'], res['memo'], res['idcertificat']

    @staticmethod
    def find_all(connection):
        results = []
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT * FROM certificat JOIN parcelle_d p ON p.numdemande = certificat.numerodemande")
            rows = cursor.fetchall()
            for r in rows:
                d = Certificat()
                d.map(r)
                results.append(d)
        except Exception as e:
            print(e)
        cursor.close()
        return results

    @staticmethod
    def find_by_num(connection, numero):
        results = []
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("""SELECT * FROM certificat
                JOIN parcelle_d p ON p.numdemande = certificat.numerodemande
                WHERE numerocertificat LIKE %s""", (numero,))
            rows = cursor.fetchall()
            for r in rows:
                d = Certificat()
                d.map(r)
                results.append(d)
        except Exception as e:
            print(e)
        cursor.close()
        return results
