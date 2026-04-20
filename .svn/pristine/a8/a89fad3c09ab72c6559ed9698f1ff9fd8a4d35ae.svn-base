from usecases.ogrimporter.IDataMapper import IDataMapper
import re


class PersonMapper(IDataMapper):
    def getDestinationTableName(self):
        return "personne"

    def getSourceQuery(self):
        return 'SELECT * FROM personnePhysique'

    def map(self, row):
        return [
            {'nompersonne': row['nom']},
            {'prenompersonne': row['prenom']},
            {'sexepersonne': self.__getSexe(row)},
            {"datenaissancepersonne": self.__getBirthDate(row)},
            {"ogr_id": row['numeroProprietaire']},
            {"numcipersonne": self.__getNumCI(row)},
            {"datecipersonne": self.__getDateCin(row)},
            {"lieucipersonne": row['lieuCIN']},
            {"adressepersonne": row['adresse']},
            {"nompere": row['nomPere']},
            {"nommere": row['nomMere']},
            {"numactenaissancepersonne": row['numeroActNaiss']},
            {"dateactenaissancepersonne": self.__getDateActeNaissance(row)},
            {"lieuactenaissancepersonne": row['lieuActNaiss']},
            {"situationmatrimoniale": self.__getSitMatri(row)},
            {"csv_id": str(row['numeroProprietaire']).strip()}
        ]

    def getUnicityCheckConditions(self, row):
        return [{'ogr_id': row[4]}]

    def __getSexe(self, row):
        if row['sexe'] == 'M':
            return 'masculin'
        return 'feminin'

    def __getBirthDate(self, row):
        if not re.match('\d{2}/\d{2}/\d{4}', row['dateNaissance']):
            return None
        parts = re.split('[/\s]', row['dateNaissance'])
        return "%s-%s-%s" % (parts[2], parts[1], parts[0])

    def __getDateCin(self, row):
        if row['numeroCIN'] != '':
            parts = re.split('T', row['dateCIN'])
            return parts[0]
        else:
            return None

    def __getDateActeNaissance(self, row):
        if row['numeroActNaiss'] != '':
            return re.split('T', row['dateActNaiss'])[0]
        else:
            return None

    def __getSitMatri(self, row):
        if row['situation'] == '0':
            return 1
        else:
            return 2
    def __getNumCI(self,row):
        if str(row['numeroCIN']).strip() == '':
            return None
        else:
            return str(row['numeroCIN']).strip()
