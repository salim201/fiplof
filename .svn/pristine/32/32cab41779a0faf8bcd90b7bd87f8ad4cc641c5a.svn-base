import psycopg2
import psycopg2.extras


class ProprietaireParcelled:
    def __init__(self):
        self.idparcelle, self.idpersonne, self.nom, self.prenom, self.cin = 0, 0, "", "", ""

    def map(self, res):
        self.idparcelle, self.idpersonne, self.nom, self.prenom, self.cin = \
            res['idparcelle'], res['idpersonne'], res['nompersonne'], res['prenompersonne'], res['numcipersonne']

    @staticmethod
    def find_by_parcelleid(connection, idparcelle):
        results = []
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT P.*, P1.nompersonne, P1.prenompersonne, P1.numcipersonne "
                           "FROM proprietaireparcelle_d P "
                           "JOIN personnephysique P1 on P1.idpersonne = P.idpersonne "
                           "WHERE P.idparcelle = %s", (idparcelle,))
            rows = cursor.fetchall()
            for r in rows:
                d = ProprietaireParcelled()
                d.map(r)
                results.append(d)
        except Exception as e:
            print(e)
        cursor.close()
        return results

