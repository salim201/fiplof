from PyQt4.QtCore import QThread, SIGNAL
from osgeo import ogr
import ogrinfo
import globalvars
from usecases.ogrimporter.OgrImporter import IQueryDefinition, OgrImporter, IDataMapper
from adapters.ogr import CertificateMapper, CommuneMapper, FokontanyMapper, ParcelleDemandeMapper, PersonMapper, TempProprietaireMapper, DemandeMapper, VoisinsMapper
import psycopg2.extras


class ImporterThread(QThread):
    def __init__(self, filename, connection):
        QThread.__init__(self)
        self.filename, self.connection = filename, connection
        self.ogroutput, self.current_step = "ogr.log", -1

    def __del__(self):
        self.wait()

    def run(self):
        if self.filename == "":
            self.emit(SIGNAL("alert(QString)"), "Veuillez choisir un dossier")
            return
        ogrinfo.bVerbose = False
        poDS = ogr.Open(str(self.filename), False)
        if poDS is None:
            self.emit(SIGNAL("alert(QString)"), "Fichier ogr non valide")
            return

        #self.importUsingMapper(FokontanyMapper.FokontanyMapper())
        certificats = self.importUsingMapper(CertificateMapper.CertificateMapper(self.connection))
        self.importUsingMapper(ParcelleDemandeMapper.ParcelleDemandeMapper())
        #self.importUsingMapper(CommuneMapper.CommuneMapper())
        self.importUsingMapper(PersonMapper.PersonMapper())

        self.__emitStepInit()
        self.importParcelleDemandeCertificatId(certificats)
        self.__emitStepDone()

        self.__emitStepInit()
        #self.importDemande(certificats)
        self.importUsingMapper(DemandeMapper.DemandeMapper())
        self.__emitStepDone()

        tempProprios = self.importUsingMapper(TempProprietaireMapper.TempProprietaireMapper(self.connection))

        self.__emitStepInit()
        self.fillAvoirDemande(tempProprios)
        self.updateAvoirDemande()
        self.__emitStepDone()

        self.__emitStepInit()
        self.importProprietaire(tempProprios)
        self.__emitStepDone()

        self.updateCertificatRL()
        self.updateConsistanceParcelle_d()

        self.rectifierProprietaireManquant()

        self.__emitStepInit()
        self.importUsingMapper(VoisinsMapper.VoisinsMapper())
        self.__emitStepDone()

        poDS.Destroy()

    def __emitStepInit(self):
        self.emit(SIGNAL("stepInit(int)"), self.current_step + 1)

    def __emitStepDone(self):
        self.emit(SIGNAL("stepDone(int)"), self.current_step)

    def __emitSuccess(self, message):  # type:(str) ->None
        self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, message, "green")

    def __emitError(self, errorMessage):  # type:(str)->None
        self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, errorMessage, "red")

    def __emitWarning(self, warningMessage):  # type:(str)->None
        self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, warningMessage, "orange")

    def __emitClearSubstep(self):
        self.current_step += 1
        self.emit(SIGNAL("clearSubstep(int)"), self.current_step)

    def importUsingMapper(self, mapper):  # type:(IDataMapper)->list[dict]
        self.__emitStepInit()
        importer = OgrImporter(str(self.filename), ogr, mapper)
        queryDefinitions = importer.getSqlStatementsFromOGR()
        result = self.executeQueryDefinition(queryDefinitions)
        self.__emitStepDone()
        return result

    def importParcelleDemandeCertificatId(self, certificats):
        cursor = self.connection.cursor()
        self.__emitClearSubstep()
        for certificat in certificats:
            sql = "UPDATE parcelle_d P SET idcertificat = C.idcertificat, region = %s, district = %s, commune = %s, idhameau = C.idhameau FROM certificat C " \
                + " WHERE P.numdemande = C.numerodemande AND C.numerocertificat = %s" \
                + " RETURNING P.idcertificat, C.numerodemande"
            try:
                cursor.execute(sql, (globalvars.nomregion, globalvars.nomdistrict, globalvars.nomcommune, certificat['numerocertificat'],))
                rows = cursor.fetchall()
                self.connection.commit()
                for i in rows:
                    self.__emitSuccess("certificat id %s est liee avec demande Num. %s" % (i[0], i[1]))
            except Exception as e:
                self.__emitError(str(e))
                self.connection.rollback()
        cursor.close()

    def importDemande(self, certificates):  # type:(list[dict]) -> None
        cursor = self.connection.cursor()
        self.__emitClearSubstep()

        for index, row in enumerate(certificates):
            numeroDemande = row['numerodemande'].strip()
            sql = "INSERT INTO demande(numdemande, gid, datedemande, idcommune, region, district, idprojet, idfokontany)"
            sql += " SELECT %s, parcelle_d.gid, %s, %s, %s, %s, %s, %s FROM parcelle_d WHERE numdemande = %s"
            try:
                if self.exists("demande", "numdemande", numeroDemande):
                    self.__emitWarning("Demande %s existe deja en base" % (numeroDemande))
                else:
                    params = (numeroDemande, row['datecreation'], globalvars.id_commune, globalvars.nomregion,
                              globalvars.nomdistrict, globalvars.id_projet, str(row['idfokontany']), numeroDemande, )
                    cursor.execute(sql, params)
                    self.connection.commit()
                    self.__emitSuccess("Demande %s" % (numeroDemande))
            except Exception as e:
                self.connection.rollback()
                self.__emitError(str(e))
            p = (index + 1) * 100 / len(certificates)
            self.emit(SIGNAL("progress(int)"), p)
        cursor.close()

    def fillAvoirDemande(self, tempProprios):
        print ('FILL AVOIR DEMANDE')
        self.__emitClearSubstep()
        numrec = 0
        for pers in tempProprios:
            res = []
            '''
            try:
                cursor = self.connection.cursor()
                sql = "SELECT P.* FROM avoir_demande P JOIN personne H ON H.idpersonne = P.idpersonne JOIN parcelle_d D on D.gid = P.idparcelle WHERE H.ogr_id = %s"
                cursor.execute(sql, (pers['numeroproprietaire'],))
                res = cursor.fetchall()
                print(res)
                cursor.close()
            except Exception as e:
                print("Checking proprio : %s" % str(e))
                self.connection.rollback()
            if len(res) > 0:
                self.__emitWarning(
                    "%s possede deja la demande sur %s" % (pers['numeroproprietaire'], pers['numerodemande']))
            else:
                try:
                    cursor = self.connection.cursor()
                    sql = """INSERT INTO avoir_demande(idparcelle, idpersonne, iddemande, representant)
                            SELECT P.gid, H.idpersonne, D.iddemande ,true
                            FROM parcelle_d P, personne H, demande D
                            WHERE P.numdemande = %s AND H.ogr_id = %s AND D.numdemande = %s RETURNING avoir_demande.*"""
                    cursor.execute(sql, (pers['numerodemande'], pers['numeroproprietaire'], pers['numerodemande'],))
                    res = cursor.fetchall()
                    self.connection.commit()
                    if len(res) > 0:
                        self.__emitSuccess(
                            "demande %s cree pour %s" % (pers['numerodemande'], pers['numeroproprietaire']))
                    else:
                        self.__emitError(
                            "Aucun demande cree pour %s - %s" % (pers['numeroproprietaire'], pers['numerodemande']))
                    cursor.close()
                except Exception as err:
                    self.__emitError(str(err))
                    self.connection.rollback()
            '''
            try:
                cursor = self.connection.cursor()
                sql = """INSERT INTO avoir_demande(idparcelle, idpersonne, iddemande, representant)
                                        SELECT P.gid, H.idpersonne, D.iddemande ,true
                                        FROM parcelle_d P, personne H, demande D
                                        WHERE P.numdemande = %s AND H.ogr_id = %s AND D.numdemande = %s RETURNING avoir_demande.*"""
                cursor.execute(sql, (pers['numerodemande'], pers['numeroproprietaire'], pers['numerodemande'],))
                res = cursor.fetchall()
                self.connection.commit()
                if len(res) > 0:
                    self.__emitSuccess(
                        "demande %s cree pour %s" % (pers['numerodemande'], pers['numeroproprietaire']))
                else:
                    self.__emitError(
                        "Aucun demande cree pour %s - %s" % (pers['numeroproprietaire'], pers['numerodemande']))
                cursor.close()
            except Exception as err:
                self.__emitError(str(err))
                self.connection.rollback()

            p = (numrec + 1) * 100 / len(tempProprios)
            self.emit(SIGNAL("progress(int)"), p)
            numrec += 1
        #cursor.close()
        print ("FIN FILL AVOIR DEMANDE")

    def importProprietaire(self, tempProprios):
        self.__emitClearSubstep()
        numrec = 0
        for pers in tempProprios:
            res = []
            '''
            try:
                cursor = self.connection.cursor()
                sql = "SELECT P.* FROM proprietaireparcelle P JOIN personne H ON H.idpersonne = P.idpersonne JOIN parcelle_d D on D.gid = P.idparcelle WHERE H.ogr_id = %s"
                cursor.execute(sql, (pers['numeroproprietaire'],))
                res = cursor.fetchall()
                cursor.close()
            except Exception as e:
                print("Checking proprio : %s" % str(e))
                self.connection.rollback()
            if len(res) > 0:
                self.__emitWarning("%s possede deja le certificat sur %s" % (pers['numeroproprietaire'], pers['numerodemande']))
            else:
                try:
                    cursor = self.connection.cursor()
                    sql = """INSERT INTO proprietaireparcelle(idparcelle, idpersonne, representant)
                    SELECT P.gid, H.idpersonne, true 
                    FROM parcelle_d P, personne H
                    WHERE P.numdemande = %s AND H.ogr_id = %s RETURNING proprietaireparcelle.*"""
                    cursor.execute(sql, (pers['numerodemande'], pers['numeroproprietaire'],))
                    res = cursor.fetchall()
                    self.connection.commit()
                    if len(res) > 0:
                        self.__emitSuccess("certificat %s cree pour %s" % (pers['numerodemande'], pers['numeroproprietaire']))
                    else:
                        self.__emitError("Aucun certificat cree pour %s - %s" % (pers['numeroproprietaire'], pers['numerodemande']))
                    cursor.close()
                except Exception as err:
                    self.__emitError(str(err))
                    self.connection.rollback()
            '''
            try:
                cursor = self.connection.cursor()
                sql = """INSERT INTO proprietaireparcelle(idparcelle, idpersonne, representant)
                                SELECT P.gid, H.idpersonne, true 
                                FROM parcelle_d P, personne H
                                WHERE P.numdemande = %s AND H.ogr_id = %s RETURNING proprietaireparcelle.*"""
                cursor.execute(sql, (pers['numerodemande'], pers['numeroproprietaire'],))
                res = cursor.fetchall()
                self.connection.commit()
                if len(res) > 0:
                    self.__emitSuccess(
                        "certificat %s cree pour %s" % (pers['numerodemande'], pers['numeroproprietaire']))
                else:
                    self.__emitError(
                        "Aucun certificat cree pour %s - %s" % (pers['numeroproprietaire'], pers['numerodemande']))
                cursor.close()
            except Exception as err:
                self.__emitError(str(err))
                self.connection.rollback()

            p = (numrec + 1) * 100 / len(tempProprios)
            self.emit(SIGNAL("progress(int)"), p)
            numrec += 1
        #cursor.close()

    def exists(self, table, column, value):
        sql = "SELECT %s FROM %s WHERE %s=" % (column, table, column)
        cursor = self.connection.cursor()
        cursor.execute(sql + "%s", (value,))
        rows = cursor.fetchall()
        cursor.close()
        return len(rows) > 0

    def executeQueryDefinition(self, queryDefinitions):  # type:(list[IQueryDefinition]) -> None
        self.__emitClearSubstep()
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        results = []
        for index, definition in enumerate(queryDefinitions):
            try:
                if self.recordExists(definition):
                    self.__emitWarning("L'enregistrement %s existe deja en base" % (definition.parameters[0]))
                else:
                    cursor.execute(definition.query, definition.parameters)
                    self.connection.commit()
                    results.append(cursor.fetchone())
                    self.__emitSuccess("%s inseree en base" % (definition.parameters[0]))
            except Exception as e:
                print(str(e))
                self.connection.rollback()
                self.__emitError(str(e))
            p = (index + 1) * 100 / len(queryDefinitions)
            self.emit(SIGNAL("progress(int)"), p)
        cursor.close()
        return results

    def recordExists(self, queryDefinition):  # type:(IQueryDefinition) -> bool
        if queryDefinition.unicityCheckQuery == '':
            return False
        count = 0
        cursor = self.connection.cursor()
        try:
            cursor.execute(queryDefinition.unicityCheckQuery, queryDefinition.unicityCheckParameters)
            res = cursor.fetchone()
            count = res[0]
        except Exception as e:
            print(queryDefinition.unicityCheckQuery, e)
            self.connection.rollback()
        cursor.close()
        return count > 0

    def updateCertificatRL(self):
        # Update de la table certificat
        cur = self.connection.cursor()
        try:
            cur.execute(
                'UPDATE certificat SET datereconnaissance = (SELECT datereconnaissance FROM demande where numdemande = numerodemande)')
            self.connection.commit()
        except Exception as err:
            print (err)
            self.connection.rollback()
        cur.close()

    def updateConsistanceParcelle_d(self):
        cur = self.connection.cursor()
        try:
            cur.execute(
                'UPDATE parcelle_d SET consistance = D.consistance, cout = D.cout FROM demande D Where parcelle_d.numdemande=D.numdemande')
            self.connection.commit()
        except Exception as err:
            print(err)
            self.connection.rollback()
        cur.close()

    def updateAvoirDemande(self):
        # Update de la table avoir_demande
        curs = self.connection.cursor()
        try:
            curs.execute(
                "insert into avoir_demande (idpersonne,iddemande,idparcelle) select P.idpersonne,d.iddemande , d.gid from  demande as d inner join personne as P  on TRIM(CONCAT(UPPER(P.nompersonne),' ',UPPER(P.prenompersonne))) = UPPER(TRIM(d.nomdemandeur))")
            self.connection.commit()
        except Exception as err:
            print(err)
            self.connection.rollback()
        curs.close()

    def rectifierProprietaireManquant(self):
        curs = self.connection.cursor()
        try:
            curs.execute(
                "INSERT INTO avoir_demande (idparcelle, iddemande, idpersonne,representant) SELECT d.gid, d.iddemande, idpersonne, TRUE FROM demande d, personne p WHERE gid NOT IN (SELECT idparcelle FROM avoir_demande) AND d.nomdemandeur IS NOT NULL AND UPPER(TRIM(CONCAT(p.nompersonne,' ',p.prenompersonne))) = UPPER(TRIM (d.nomdemandeur)) ORDER BY p.idpersonne")
            self.connection.commit()
        except Exception as err:
            print(err)
            self.connection.rollback()
        curs.close()

        cur2 = self.connection.cursor()
        try:
            cur2.execute(
                "INSERT INTO proprietaireparcelle (idparcelle, idpersonne, representant) SELECT d.gid, idpersonne, TRUE FROM demande d, personne p WHERE gid NOT IN (SELECT idparcelle FROM proprietaireparcelle) AND d.nomdemandeur IS NOT NULL AND UPPER(TRIM(CONCAT(p.nompersonne,' ',p.prenompersonne))) = UPPER(TRIM (d.nomdemandeur)) ORDER BY p.idpersonne")
            self.connection.commit()
        except Exception as err:
            print(err)
            self.connection.rollback()
        cur2.close()

        cur3 = self.connection.cursor()
        try:
            cur3.execute(
                "INSERT INTO avoir_demande (idparcelle, iddemande, idpersonne,representant) SELECT d.gid, d.iddemande, pp.idpersonne, TRUE FROM demande d, proprietaireparcelle pp WHERE gid NOT IN (SELECT idparcelle FROM avoir_demande) AND pp.idparcelle = d.gid ORDER BY pp.idpersonne")
            self.connection.commit()
        except Exception as err:
            print(err)
            self.connection.rollback()
        cur3.close()