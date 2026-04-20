from PyQt4.QtCore import QThread, SIGNAL
from osgeo import gdal, ogr
import ogrinfo, time
import sys
import os
import globalvars


class ImporterThread(QThread):
    def __init__(self, filename, connection):
        QThread.__init__(self)
        self.filename, self.connection = filename, connection
        self.ogroutput, self.current_step = "ogr.log", -1
        self.newCode = None
        self.tabIdPersonne = []
        self.tabIdParcelle = []

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

        self.emit(SIGNAL("stepInit(int)"), self.current_step + 1)
        rows_parc = self.importParcelles(poDS)
        self.emit(SIGNAL("stepDone(int)"), self.current_step)

        self.emit(SIGNAL("stepInit(int)"), self.current_step + 1)
        rows_contribuable = self.importContribuable(poDS)
        self.emit(SIGNAL("stepDone(int)"), self.current_step)

        self.emit(SIGNAL("stepInit(int)"), self.current_step + 1)
        self.importLiaisonContribuableParcelle(poDS)
        #self.importParcelleDemande(poDS)
        self.emit(SIGNAL("stepDone(int)"), self.current_step)

        self.emit(SIGNAL("stepInit(int)"), self.current_step + 1)
        #self.importParcelleDemandeCertificatId(rows_cert)
        self.emit(SIGNAL("stepDone(int)"), self.current_step)

        self.emit(SIGNAL("stepInit(int)"), self.current_step + 1)
        #self.importDemande(rows_pers)
        self.emit(SIGNAL("stepDone(int)"), self.current_step)

        poDS.Destroy()

    def importParcelles(self, poDS):
        poResultSet = poDS.ExecuteSQL("SELECT FID, * FROM parcelles")
        if poResultSet is None:
            return
        original = sys.stdout
        sys.stdout = open(self.ogroutput, "w")
        ogrinfo.ReportOnLayer(poResultSet, None, None, None, {})
        sys.stdout = original
        #print sys.stdout
        self.current_step += 1
        return self.file2db(0, "parcelle_d", {
            "commune": 2
            , "fkt": 4
            , "codeparcelle": 8
            , "geom": 29
            , "nom_fkt": 4
            , "code_fkt": 5
            , "hameau": 6
            , "code_hameau": 7
            , "FID": 1
            , "id_contribuable": 13
        }, "codeparcelle", "geom", "codeparcelle", {"estfiscalite": 1, "id_commune": globalvars.id_commune}, ["nom_fkt", "code_fkt", "hameau", "code_hameau", "FID", "id_contribuable"])


    #def importCertificat(self, poDS):
        #poResultSet = poDS.ExecuteSQL("SELECT * FROM certificat", None, None)
        #if poResultSet is None:
            #return
        #original = sys.stdout
        #sys.stdout = open(self.ogroutput, "w")
        #ogrinfo.ReportOnLayer(poResultSet, None, None, None, {})
        #sys.stdout = original
        #self.current_step += 1
        #return self.file2db(0, "certificat", {
            #"numerocertificat": 1
            #, "numerodemande": 3
            #, "typecertificat": 4
            #, "datecreation": 7
            #, "dateedition": 6
            #, "datedelivrance": 5
            #, "memo": 17
        #}, "numerocertificat", "", "numerocertificat")

    #def importParcelleDemande(self, poDS):
        #poResultSet = poDS.ExecuteSQL("SELECT numeroDemande FROM parcelleDemande", None, None)
        #if poResultSet is None:
            #return
        #original = sys.stdout
        #sys.stdout = open(self.ogroutput, "w")
        #ogrinfo.ReportOnLayer( poResultSet, None, None, None, {} )
        #sys.stdout = original
        #self.current_step += 1
        #return self.file2db(1, "parcelle_d", {"numdemande": 1, "geom": 2}, "numdemande", "geom", "numdemande")

    #def importParcelleDemandeCertificatId(self, num_certificats):
        #cursor = self.connection.cursor()
        #self.current_step += 1
        #self.emit(SIGNAL("clearSubstep(int)"), self.current_step)
        #for num_certificat in num_certificats:
            #sql = "UPDATE parcelle_d P SET idcertificat = C.idcertificat, region = %s, district = %s, commune = %s FROM certificat C " \
            #+ " WHERE P.numdemande = C.numerodemande AND C.numerocertificat = %s" \
            #+ " RETURNING P.idcertificat, C.numerodemande"
            #try:
                #cursor.execute(sql, (globalvars.nomregion, globalvars.nomdistrict, globalvars.nomcommune, num_certificat['numeroCertificat'],))
                #rows = cursor.fetchall()
                #self.connection.commit()
                #for i in rows:
                    #self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, "certificat id %s est liee avec demande Num. %s" % (i[0],i[1]), "green")
            #except Exception as e:
                #self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, str(e), "red")
                #self.connection.rollback()
        #cursor.close()

    def importLiaisonContribuableParcelle(self, poDS):
        cursor = self.connection.cursor()
        #print "ID PARCELLES = " + str(self.tabIdParcelle)
        #print "ID Personnes = " + str(self.tabIdPersonne)
        for idparc in self.tabIdParcelle:
            #print "MANDALO IDPARC"
            if idparc['idContribuable'] is not None:
                #print "MANDALO IDPARC2"
                idpersonne = None
                for idpers in self.tabIdPersonne:
                    if idpers['oldId'] == idparc['idContribuable']:
                        idpersonne = idpers['newId']
                if idpersonne is not None:
                    try:
                        cursor.execute("INSERT INTO contribuables_parcelle (idpersonne, idparcelle, contribuable) VALUES(%s, %s, %s)", (idpersonne, idparc['newId'], True))
                        self.connection.commit()
                    except StandardError as e:
                        print(e)
                        self.connection.rollback()

        #print "Valeur de tabParcelle = " + str(self.tabIdParcelle)
        #print "Valeur de tabPersonne = " + str(self.tabIdPersonne)

        poResultSet = poDS.ExecuteSQL("SELECT * FROM avoir_parcelle", None, None)
        if poResultSet is None:
            return
        original = sys.stdout
        sys.stdout = open(self.ogroutput, "w")
        ogrinfo.ReportOnLayer(poResultSet, None, None, None, {})
        sys.stdout = original
        self.current_step += 1
        print "Appel de la fonction"
        return self.file2db(self.current_step, "contribuables_parcelle",
                            {"idpersonne": 1
                             ,"idparcelle": 2
                             }, "", "", "", {"contribuable": True}, ['idpersonne', 'idparcelle'])

    def importContribuable(self, poDS):
        poResultSet = poDS.ExecuteSQL("SELECT FID, * FROM contribuables", None, None)
        if poResultSet is None:
            return
        original = sys.stdout
        sys.stdout = open(self.ogroutput, "w")
        ogrinfo.ReportOnLayer( poResultSet, None, None, None, {} )
        sys.stdout = original
        self.current_step += 1
        return self.file2db(self.current_step, "personne",
                            {"numcipersonne": 4
                             ,"numactenaissancepersonne": 5
                             ,"datecipersonne": 6
                             ,"nompersonne": 7
                             ,"prenompersonne": 8
                             ,"adressepersonne": 9
                             ,"datenaissancepersonne": 10
                             ,"lieunaissancepersonne": 11
                             ,"sexepersonne": 13
                             ,"nompere": 18
                             ,"nommere": 17
                             ,"FID": 1
                             }, "nompersonne", "", "numcipersonne", {},['sexepersonne', 'FID'])


    def importFkt(self, poDS):
        poResultSet = poDS.ExecuteSQL("SELECT * FROM demandecertificat", None, None)
        if poResultSet is None:
            return
        original = sys.stdout
        sys.stdout = open(self.ogroutput, "w")
        ogrinfo.ReportOnLayer(poResultSet, None, None, None, {})
        sys.stdout = original
        self.file2db(self.current_step, "fokontany", {"codefokontany": 15}, "codefokontany", "", "codefokontany",
                     {"idcommune": globalvars.id_commune, "nomfokontany": ""})

    def importDemande(self, rows_dema):
        self.current_step += 1
        idcommune = globalvars.id_commune
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM commune  WHERE idcommune=%s", [int(idcommune)])
        dm = cursor.fetchone()
        iddistrict = 0
        idregion = 0
        if len(dm) >= 1:
            iddistrict = dm[1]
            cursor.execute("SELECT * FROM district  WHERE iddistrict=%s", [int(iddistrict)])
            dm = cursor.fetchone()
            idregion = dm[1]

        for index, row in enumerate(rows_dema):
            sql = "INSERT INTO demande(numdemande, nomdemandeur, gid, datedemande,idcommune, datereconnaissance, region, district, commune, idprojet, idfokontany)"
            sql += " SELECT %s, %s, parcelle_d.gid, %s, %s, %s, %s, %s, %s, %s, %s FROM parcelle_d WHERE numdemande = %s"
            try:
                if self.exists("demande", "numdemande", row['numeroDemande']):
                    self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, "Demande %s existe deja en base" % (row['numeroDemande']), "orange")
                else:
                    idfkt = self.select("fokontany", "idfokontany", "codefokontany = '%s' AND idcommune = '%s'" % (row['fokotany'], idcommune))
                    if idfkt is None:
                        continue
                    params = (row['numeroDemande'], row['listeDemandeurs'], row['dateDemande'],idcommune,row['dateReconnaissance'], globalvars.nomregion, globalvars.nomdistrict, globalvars.nomcommune, globalvars.id_projet, str(idfkt), row['numeroDemande'], )
                    cursor.execute(sql, params)
                    self.connection.commit()
                    self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, "Demande %s" % (row['numeroDemande']), "green")
            except Exception as e:
                self.connection.rollback()
                self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, str(e), "red")
            p = (index + 1) * 100 / len(rows_dema)
            self.emit(SIGNAL("progress(int)"), p)
        cursor.close()

    def importProprietaire(self, rows_pers):
        self.current_step += 1
        cursor = self.connection.cursor()
        numrec = 0
        for pers in rows_pers:
            sql = "SELECT P.* FROM proprietaireparcelle_d P JOIN personnephysique H ON H.idpersonne = P.idpersonne JOIN parcelle_d D on D.gid = P.idparcelle WHERE H.nompersonne = %s AND D.numdemande = %s"
            cursor.execute(sql, (pers['listeDemandeurs'], pers['numeroDemande']))
            res = cursor.fetchall()
            if len(res) > 0:
                self.emit(SIGNAL("addSubStep(int, QString, QString)"),self.current_step, "%s possede deja le certificat sur %s" % (pers['listeDemandeurs'], pers['numeroDemande']), "orange")
            else:
                try:
                    sql = """INSERT INTO proprietaireparcelle_d(idparcelle, idpersonne) SELECT P.gid, H.idpersonne 
                    FROM parcelle_d P, personnephysique H
                    WHERE P.numdemande = %s AND H.nompersonne = %s RETURNING proprietaireparcelle_d.*"""
                    cursor.execute(sql, (pers['numeroDemande'], pers['listeDemandeurs']))
                    res = cursor.fetchall()
                    self.connection.commit()
                    if len(res) > 0:
                        self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, "certificat %s cree pour %s" % (pers['numeroDemande'], pers['listeDemandeurs']), "green")
                    else:
                        self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, "Aucun certificat cree pour %s - %s" % (pers['listeDemandeurs'], pers['numeroDemande']), "red")
                except Exception as err:
                    self.emit(SIGNAL("addSubStep(int, QString, QString)"), self.current_step, str(err), "red")
                    self.connection.rollback()
            p = (numrec + 1) * 100 / len(rows_pers)
            self.emit(SIGNAL("progress(int)"), p)
            numrec += 1
        cursor.close()

    def file2db(self, step, table, columns, labelcolumn, geomcolumn, keycolumn, othervalues={}, fieldsToExcept = []):
        f = open(self.ogroutput, "r")
        lines = ""
        for line in f:
            lines += line
        splited = lines.split("\n\n")
        records = []
        for s in splited:
            if s != "":
                records.append(s)
        cursor = self.connection.cursor()
        item, keyvalue = "", ""
        returnvalues = []
        self.emit(SIGNAL("clearSubstep(int)"), step)
        compteur = 0
        for numrec, record in enumerate(records):
            idcontribuableSurTableParcelle = None
            if table == "personne":
                newIdPersonne = {}
                newIdPersonne.clear()
            if table == "parcelle_d":
                newIdParcelle = {}
                newIdParcelle.clear()
            fields = record.split("\n")
            values, values_placeholder, cols = [], [], []
            print "fields = " + str(fields)
            returnvalues.append({})
            for field in fields:
                t = field.split("=")
                if len(t) == 2:
                    #print "champ 1 = " + str(t[0].strip().split(" ")[0])
                    returnvalues[-1:][0][t[0].strip().split(" ")[0]] = t[1].strip()
            fokontany = []
            hameau = []
            idFkt = None
            idHameau = None
            for i in columns:
                cols.append(i)
                if i == geomcolumn:
                    v = fields[columns[i]].strip()
                    values_placeholder.append("ST_GeomFromText(%s, "+str(globalvars.EPSG_SCR)+")")
                elif i in fieldsToExcept:
                    cols.remove(i)
                    champ = fields[columns[i]].split("=")[0].strip().split(" ")[0]
                    vals = fields[columns[i]].split("=")[1].strip()
                    #print "MANDALO FIELD TO EXCEPT"
                    etatCodeFkt = False
                    etatNomFkt = False
                    etatCodeHameau = False
                    etatNomHameau = False
                    if champ == "fokontany":
                        fokontany.append(vals)
                    if champ == "code_fkt":
                        fokontany.append(vals)
                    if champ == "hameau":
                        hameau.append(vals)
                    if champ == "code_hameau":
                        hameau.append(vals)
                    print "champ = " + str()
                    if champ == "sexe":
                        sexe = ""
                        if vals == "1":
                            sexe = "masculin"
                        if vals == "2":
                            sexe = "feminin"
                        cols.append("sexepersonne")
                        values.append(sexe)
                        values_placeholder.append("%s")
                        print "Sexe personne = " + str(sexe)

                    if champ == "FID":
                        if table == "personne":
                            newIdPersonne['oldId'] = int(vals)
                        if table == "parcelle_d":
                            print "champ FID de la table parcelle"
                            newIdParcelle['oldId'] = int(vals)

                    #traitement de la relation contribuable et parcelle
                    if champ == "id_contribuable" and table == "contribuables_parcelle":
                        #print "TRAITEMENT CONTRIBUABLE"
                        for idpers in self.tabIdPersonne:
                            #print str(idpers)
                            if idpers['oldId'] == int(vals):
                                print "ID PERS NEW ID = " + str(idpers['newId'])
                                cols.append("idpersonne")
                                values.append(idpers['newId'])
                                values_placeholder.append("%s")

                    if champ == "id_contribuable" and table == "parcelle_d":
                        if vals != "(null)":
                            idcontribuableSurTableParcelle = int(vals)

                    if champ == "id_parcelle" and table == "contribuables_parcelle":
                        #print "TRAITEMENT PARCELLE"
                        for idparc in self.tabIdParcelle:
                            #print str(idparc)
                            if idparc['oldId'] == int(vals):
                                print "ID PARC NEW ID = " + str(idparc['newId'])
                                cols.append("idparcelle")
                                values.append(idparc['newId'])
                                values_placeholder.append("%s")

                    print "tableau fokontany = " + str(fokontany)
                    print "tableau hameau = " + str(hameau)
                    print len(fokontany)
                    if len(fokontany) == 2:
                        etatNomFkt = self.exists("fokontany", "nomfokontany", fokontany[1], {"idcommune": globalvars.id_commune})
                        etatCodeFkt = self.exists("fokontany", "codefokontany", fokontany[0], {"idcommune": globalvars.id_commune})
                        print "etat nom fkt = " + str(etatNomFkt) + " etat code fkt = " + str(etatCodeFkt)
                        print "*************************************************************************"
                        #fokontany.append(globalvars.id_commune)
                        if not etatCodeFkt  and not etatNomFkt : # code et nom non existant
                            try:
                                cursor.execute("INSERT INTO fokontany(nomfokontany, codefokontany, idcommune) VALUES(%s, %s, %s) returning idfokontany", (fokontany[1], fokontany[0],globalvars.id_commune))
                                self.connection.commit()
                                idFkt = cursor.fetchone()
                            except StandardError as e:
                                print (e)
                                self.connection.rollback()
                        if not etatCodeFkt and etatNomFkt: #code non existant et nom existant
                            try:
                                cursor.execute("SELECT idfokontany FROM fokontany WHERE nomfokontany = %s and idcommune", (fokontany[1],globalvars.id_commune))
                                idFkt = cursor.fetchone()
                            except StandardError as e:
                                print(e)
                                self.connection.rollback()
                        if etatCodeFkt and not etatNomFkt: #code existant mais nom non existant
                            #print "code existant et nom non existant, il faut changer le code"
                            from .codeRun import codeRun
                            code = codeRun(self.connection, "fokontany", fokontany[0], globalvars.id_commune, self)
                            code.exec_()
                            #code.ui.btnValider.clicked.connect(self.returnValue)
                            while self.newCode is None:
                                time.sleep(1)
                            valCode = self.newCode
                            print valCode
                            try:
                                cursor.execute("INSERT INTO fokontany(nomfokontany, codefokontany, idcommune) VALUES(%s, %s, %s) returning idfokontany", (fokontany[1], valCode,globalvars.id_commune))
                                self.connection.commit()
                                idFkt = cursor.fetchone()
                            except StandardError as e:
                                print(e)
                                self.connection.rollback()
                        if etatCodeFkt and etatNomFkt: # code existant et nom existant
                            try:
                                cursor.execute("SELECT idfokontany FROM fokontany WHERE nomfokontany = %s and idcommune = %s", (fokontany[1],globalvars.id_commune))
                                idFkt = cursor.fetchone()
                                print "si code et nom existe" + str(idFkt)
                            except StandardError as e:
                                print(e)
                                self.connection.rollback()
                        fokontany[:] = []
                        print "id fokontany = " + str(idFkt[0])
                    #FIN TRAITEMENT FOKONTANY
                    #DEBUT TRAITEMENT HAMEAU
                    if len(hameau) == 2:
                        #idHameau = None
                        if idFkt is not None:
                            etatNomHameau = self.exists("hameau", "nomhameau", hameau[1],
                                                     {"idfokontany": idFkt[0]})
                            etatCodeHameau = self.exists("hameau", "codehameau", hameau[0],
                                                      {"idfokontany": idFkt[0]})
                            # fokontany.append(globalvars.id_commune)
                            if not etatCodeHameau and not etatNomHameau:  # code et nom non existant
                                try:
                                    cursor.execute(
                                        "INSERT INTO hameau(nomhameau, codehameau, idfokontany) VALUES(%s, %s, %s) returning idhameau",
                                        (hameau[1], hameau[0], idFkt[0]))
                                    self.connection.commit()
                                    idHameau = cursor.fetchone()
                                except StandardError as e:
                                    print (e)
                                    self.connection.rollback()

                            if not etatCodeHameau and etatNomHameau:  # code non existant et nom existant
                                try:
                                    cursor.execute("SELECT idhameau FROM hameau WHERE nomhameau = %s and idfokontany = %s",
                                                        (hameau[1], idFkt[0]))
                                    idHameau = cursor.fetchone()
                                except StandardError as e:
                                    print(e)
                                    self.connection.rollback()
                            if etatCodeHameau and not etatNomHameau:  # code existant mais nom non existant
                                # print "code existant et nom non existant, il faut changer le code"
                                from .codeRun import codeRun
                                code = codeRun(self.connection, "hameau", hameau[0], idFkt[0], self)
                                code.exec_()
                                #code.ui.btnValider.clicked.connect(self.returnValue)
                                while self.newCode is None:
                                    time.sleep(1)
                                valCode = self.newCode
                                print valCode
                                try:
                                    cursor.execute(
                                        "INSERT INTO hameau(nomhameau, codehameau, idfokontany) VALUES(%s, %s, %s) returning idhameau",
                                        (fokontany[1], valCode, globalvars.id_commune))
                                    self.connection.commit()
                                    idHameau = cursor.fetchone()
                                except StandardError as e:
                                    print(e)
                                    self.connection.rollback()
                            if etatCodeHameau and etatNomHameau:  # code existant et nom existant
                                try:
                                    cursor.execute(
                                        "SELECT idhameau FROM hameau WHERE nomhameau = %s and idfokontany = %s",
                                        (hameau[1], idFkt[0]))
                                    idHameau = cursor.fetchone()
                                except StandardError as e:
                                    print(e)
                                    self.connection.rollback()
                        print "Id Hameau = " + str(idHameau)
                        if idHameau is not None:
                            cols.append("idhameau")
                            values_placeholder.append("%s")
                            values.append(idHameau[0])
                        hameau[:] = []

                    #print "****"
                else:
                    v = fields[columns[i]].split("=")[1].strip()
                    #print "champ = " + str(fields[columns[i]].split("=")[0].strip().split(" ")[0])
                    values_placeholder.append("%s")
                if i == labelcolumn:
                    item = v
                if i == keycolumn:
                    keyvalue = v
                if i not in fieldsToExcept:
                    values.append(v)

            for i in othervalues:
                cols.append(i)
                values.append(othervalues[i])
                values_placeholder.append("%s")

            sql = "INSERT INTO %s(%s) VALUES(%s)" % (table, ",".join(cols), ",".join(values_placeholder))
            if table == "personne":
                sql = "INSERT INTO %s(%s) VALUES(%s) returning idpersonne" % (table, ",".join(cols), ",".join(values_placeholder))
            if table == "parcelle_d":
                sql = "INSERT INTO %s(%s) VALUES(%s) returning gid" % (table, ",".join(cols), ",".join(values_placeholder))
            try:
                if self.exists(table, keycolumn, keyvalue):
                    self.emit(SIGNAL("addSubStep(int, QString, QString)"), step, "%s existe deja en base" % (keyvalue), "orange")
                else:
                    cursor.execute(sql, values)
                    self.connection.commit()
                    if table == "personne":
                        newIdPersonne['newId'] = cursor.fetchone()[0]

                    if table == "parcelle_d":
                        newIdParcelle['newId'] = cursor.fetchone()[0]
                        newIdParcelle['idContribuable'] = idcontribuableSurTableParcelle

                        #if idcontribuableSurTableParcelle is not None:

                    self.emit(SIGNAL("addSubStep(int, QString, QString)"), step, "%s inseree en base" % (item), "green")
            except Exception as e:
                self.connection.rollback()
                self.emit(SIGNAL("addSubStep(int, QString, QString)"), step, str(e), "red")
            p = (numrec + 1) * 100 / len(records)
            self.emit(SIGNAL("progress(int)"), p)
           # print "newIdParcelle = " + str(newIdParcelle)
            if table == "personne" and len(newIdPersonne) == 2:
                self.tabIdPersonne.append(newIdPersonne)
            if table == "parcelle_d" and len(newIdParcelle) == 3:
                self.tabIdParcelle.append(newIdParcelle)

        cursor.close()
        f.close()
        os.remove(self.ogroutput)
        print "tabIdParcelle = " + str(self.tabIdParcelle)
        #print "tabIdPersonne = " + str(tabIdPersonne)
        #print "return values = " + str(returnvalues)
        return returnvalues

    def exists(self, table, column, value, extrawhere = {}):
        if column != "":
            sql = "SELECT %s FROM %s WHERE %s=" % (column, table, column)
            cursor = self.connection.cursor()
            print len(extrawhere)
            if len(extrawhere) > 0:
                cursor.execute(sql + "%s and " + extrawhere.keys()[0]+ "= %s", (value,extrawhere.values()[0]))
            else:
                cursor.execute(sql + "%s", (value,))
            rows = cursor.fetchall()
            cursor.close()
            return len(rows) > 0
        else:
            return

    def select(self, table, column, where):
        sql = "SELECT %s FROM %s WHERE %s" % (column, table, where)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        if len(rows) > 0:
            return rows[0][0]
        return None

