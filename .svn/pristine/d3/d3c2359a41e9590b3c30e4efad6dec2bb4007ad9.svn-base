# -*- coding: utf-8 -*-
from PyQt4.QtCore import QThread, pyqtSignal
import subprocess
import os
from Configuration import DbConfig
import psycopg2
from logs import xlsLogger

class SeparationBaseThread(QThread):
    messageAddedSignal = pyqtSignal(str)
    doneSignal = pyqtSignal()
    updateProgreesSignal = pyqtSignal(int)

    def __init__(self, pgdump, filename, nomBase, communes, connexion):
        QThread.__init__(self)
        self.db_config = DbConfig.DbConfig()
        self.pgdump, self.filename = pgdump, filename
        self.nomBase = nomBase
        self.communes = communes
        self.connexion = connexion
        self.logger = xlsLogger.xlsLogger("Separation_Base")
        self.nomdebase, self.etatInsertion, self.erreur = '', '', ''

    def __del__(self):
        self.wait()

    def run(self):
        if "dump" in self.pgdump:
            self.run_dump()
            print self.nomBase
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

    def do_copy(self, commune, nomBase):
        texte = "Copie informations de la commune " + str(commune[3]) + " vers la base " + str(nomBase)
        self.messageAddedSignal.emit(texte)
        self.copyInfo(commune, str(nomBase))

    def run_import(self):
        title = ["nom_commune", "nom_base", "etat_creation", "erreur"]
        dataToLog = []
        print "**************************************Call of run import*****************************************"

        i = 0
        cpt = 1
        for db_name in self.nomBase:
            self.etatInsertion = ""
            cur = self.connexion.cursor()
            res = None
            try:
                cur.execute("select datname from pg_database where datname = %s", (db_name,))
                res = cur.fetchone()
            except Exception as err:
                print err
            if res is not None:
                self.etatInsertion = "La base " + db_name + u" existe déjà"
            else :
                bat = self.create_batfile(str(db_name))
                proc = subprocess.Popen([bat], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                p_float = float(float(cpt)/float(len(self.nomBase))) * 100
                p_int = int(p_float)
                while True:
                    output = proc.stdout.readline()
                    if output == '' and proc.poll() is not None:
                        break
                    if output:
                        #print output.strip()
                        self.messageAddedSignal.emit(output.strip())
                proc.poll()
                os.remove(bat)
                self.etatInsertion = u"Créaion base réussie "
            p_float = float(float(cpt) / float(len(self.nomBase))) * 100
            p_int = int(p_float)
            self.updateProgreesSignal.emit(p_int)
            self.do_copy(self.communes[i], db_name)
            self.etatInsertion = self.etatInsertion + " ,  Tenatative de Copie des information"
            dataToLog.append({"nom_commune": str(self.communes[i][3]), "nom_base": db_name,
                              "etat_creation": self.etatInsertion,
                              "erreur": self.erreur})
            if p_int == 100:
                self.logger.addSheet(title=title, data=dataToLog, sheet_name="Log Separation Base")
                self.logger.write()
                self.doneSignal.emit()
            i = i + 1
            cpt = cpt + 1



        self.doneSignal.emit()

    def create_batfile(self, db_name):
        restore_exe = self.pgdump
        psql_exe = os.path.dirname(restore_exe) + "/psql.exe"
        dirname = os.path.dirname(__file__)

        file_extension = open(dirname + "/create_extension.sql", "r")
        content_extension = file_extension.read()
        print content_extension


        string_schema = "UPDATE pg_database SET datallowconn = 'false' WHERE datname = '"+db_name+"';" \
        "\nSELECT pg_terminate_backend(pid)"\
        "\nFROM pg_stat_activity"\
        "\nWHERE datname = '"+db_name+"';"\
        "\nDROP DATABASE IF EXISTS "+db_name+";"\
        "\n--"\
        "\n-- TOC entry 4775 (class 1262 OID 93991)"\
        "\n-- Name: "+db_name+"; Type: DATABASE; Schema: -; Owner: postgres"\
        "\n--" \
        "\n DROP USER IF EXISTS plof ;" \
        "\n CREATE ROLE plof LOGIN PASSWORD 'plof';" \
        "\nCREATE DATABASE "+db_name+" WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'French_France.1252' LC_CTYPE = 'French_France.1252';" \
        "\nUPDATE pg_database SET datallowconn = 'true' WHERE datname = '" + db_name + "';" \
        "\n\c "+db_name+";"\
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
        os.write(fd, "psql --host \"%s\" "
                     "--port \"%s\" "
                     "--username postgres "
                     "< \"%s\"\n" % (self.db_config.db_host, self.db_config.db_port, schema_filename))
        os.write(fd, "psql --host \"%s\" "
                     "--port \"%s\" "
                     "--username postgres -d \"%s\" "
                     "< \"%s\"\n" % (self.db_config.db_host,self.db_config.db_port, db_name,self.filename))
        os.close(fd)
        return bat


    def copyInfo(self, commune, data_base_name):
        #creation nouvelle connexion
        new_connexion = None
        try:
            new_connexion = psycopg2.connect(database=data_base_name, user=self.db_config.db_user, password=self.db_config.db_pass, host=self.db_config.db_host)
            texte = u"Connexion à la base " + str(data_base_name) + " reussie!"
            self.messageAddedSignal.emit(texte)
        except Exception as err:
            self.messageAddedSignal.emit(str(err))

        if new_connexion is not None:
            #REGION DISTRICT COMMUNE
            data_RDC = self.getRDC(commune)
            print "*****************data RDC***************"
            print data_RDC
            self.setRDC(new_connexion, data_RDC)
            #FIN REGION DISTRICT COMMUNE

            # PROJET et Projet couche
            data_projet = self.getProjet(commune)
            print "*****************data Projet***************"
            print data_projet
            if data_projet is not None:
                self.setProjet(new_connexion, data_projet)
                #Recuperation du projet couche
                data_projet_couche = self.getProjetCouche(data_projet[6])

                print "************data projet couche****************"

                for dt_proj_couche in data_projet_couche:
                    self.setProjetCouche(new_connexion, dt_proj_couche)

                ############get all fokontany #######
                data_fkt = self.getFokontany(commune[0])
                if data_fkt is not None:
                    for fkt in data_fkt:
                        self.setFokontany(new_connexion, fkt)
                        #get all Hameau for every fokontany
                        data_hameau = self.getHameau(fkt[0])
                        if data_hameau is not None:
                            for ham in data_hameau:
                                self.setHameau(new_connexion, ham)

                #################CONSISTANCE###################
                data_consistance = self.getConsistance()
                if data_consistance is not None:
                    for dt_con in data_consistance:
                        self.setConsistance(new_connexion, dt_con)
                ###################CERTIFICAT#############
                data_cf = self.getCertificat(commune[0])
                if data_cf is not None:
                    for dt_cf in data_cf:
                        self.setCertificat(new_connexion, dt_cf)

                ################GROUPE#######################
                data_groupe = self.getGroupe()
                if data_groupe is not None:
                    for dt_gr in data_groupe:
                        self.setGroupe(new_connexion, dt_gr)
                #############UTILISATEUR############################
                data_user = self.getUser()
                if data_user is not None:
                    for dt_user in data_user:
                        self.setUser(new_connexion, dt_user)
                #############PARCELLE############################
                data_parcelle = self.getParcelle(commune[0])
                #print data_parcelle
                if data_parcelle is not None:
                    for dt_parc in data_parcelle:
                        self.setParcelle(new_connexion, dt_parc)

                ##########DEMANDE#####################################
                data_demande = self.getDemande(commune[0])
                # print data_parcelle
                if data_demande is not None:
                    for dt_dm in data_demande:
                        self.setDemande(new_connexion, dt_dm)

                ##########PERSONNE#####################################
                data_personne = self.getPersonne()
                # print data_parcelle
                if data_personne is not None:
                    for dt_pers in data_personne:
                        self.setPersonne(new_connexion, dt_pers)

                ##########AVOIR DEMANDE#####################################
                data_avd = self.getAvoirDemande(commune[0])
                # print data_parcelle
                if data_avd is not None:
                    for dt_avd in data_avd:
                        self.setAvoirDemande(new_connexion, dt_avd)

                ##########PROPRIETAIRE#####################################
                data_proprietaire = self.getProprietaire(commune[0])
                # print data_parcelle
                if data_proprietaire is not None:
                    for dt_prop in data_proprietaire:
                        self.setProprietaire(new_connexion, dt_prop)

                ##########VOISINS#####################################
                data_voisins = self.getVoisins(commune[0])
                # print data_parcelle
                if data_voisins is not None:
                    for dt_voisins in data_voisins:
                        self.setVoisins(new_connexion, dt_voisins)

                ##########DEMANDE CRL#####################################
                data_CRL = self.getCRL(commune[0])
                # print data_parcelle
                if data_CRL is not None:
                    for dt_CRL in data_CRL:
                        self.setCRL(new_connexion, dt_CRL)

                ##########blob personne#####################################
                data_blob_pers = self.getBlobPersonne()
                # print data_parcelle
                if data_blob_pers is not None:
                    for dt_blob_pers in data_blob_pers:
                        self.setBlobPersonne(new_connexion, dt_blob_pers)

                ##########blob voisins#####################################
                data_blob_voisin = self.getBlobVoisins(commune[0])
                # print data_parcelle
                if data_blob_voisin is not None:
                    for dt_blob_vois in data_blob_voisin:
                        self.setBlobVoisins(new_connexion, dt_blob_vois)
            else:
                new_connexion.rollback()
                return

    def getBlobVoisins(self, idcommune):
        print "call of getBlobVoisins"
        res = None
        try:
            cur = self.connexion.cursor()
            cur.execute(
                'SELECT * FROM blob_voisin WHERE idparcelle IN  (SELECT gid FROM parcelle_d WHERE id_commune =  %s)', (str(idcommune))
            )
            res = cur.fetchall()
            cur.close()
        except Exception as err:
            print "getBlobVoisins "
            print err
        return res


    def setBlobVoisins(self, new_connex, data):
        curs = new_connex.cursor()
        try:
            curs.execute(
                "INSERT INTO blob_personne(idpoint, idparcelle, voisin, signature_fic, signature_name, signature_ext) "
                "VALUES (%s, %s, %s,%s, %s, %s)",
                (data[0], data[1], data[2],data[3], data[4], data[5]))
            new_connex.commit()
        except Exception as err:
            print "setBlobVoisins"
            print err
            new_connex.rollback()

        try:
            curs.execute("SELECT setval('blob_personne_idblob_seq', %s, TRUE)", (str(data[0]),))
            new_connex.commit()
        except Exception as err:
            print err
            new_connex.rollback()


    def getBlobPersonne(self):
        print "call of getBlobPersonne"
        res = None
        try:
            cur = self.connexion.cursor()
            cur.execute(
                'SELECT * FROM blob_personne '
            )
            res = cur.fetchall()
            cur.close()
        except Exception as err:
            print "getBlobPersonne "
            print err
        return res


    def setBlobPersonne(self, new_connex, data):
        curs = new_connex.cursor()
        try:
            curs.execute(
                "INSERT INTO blob_personne(idblob, idpersonne,cin_recto, cin_verso, signature, empreinte_d, empreinte_g, cin_recto_name, cin_recto_type, cin_verso_name, cin_verso_type, "
                " signature_name, signature_type, empreinte_d_name, empreinte_d_type, empreinte_g_name, empreinte_g_type,photo_demandeur, photo_demandeur_type ) "
                "VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s,%s, %s)",
                (data[0], data[1], data[2],data[3], data[4], data[5],data[6],data[7], data[8], data[9],data[10], data[11], data[12],data[13],data[14],
                 data[15], data[16],data[17], data[18]))
            new_connex.commit()
        except Exception as err:
            print "setBlobPersonne"
            print err
            new_connex.rollback()

        try:
            curs.execute("SELECT setval('blob_personne_idblob_seq', %s, TRUE)", (str(data[0]),))
            new_connex.commit()
        except Exception as err:
            print err
            new_connex.rollback()


    def getCRL(self, idcommune):
        print "call of getCRL"
        res = None
        try:
            cur = self.connexion.cursor()
            cur.execute(
                'SELECT * FROM demande_crl WHERE iddemande IN (SELECT iddemande FROM demande WHERE idcommune =  %s)', (str(idcommune),)
            )
            res = cur.fetchall()
            cur.close()
        except Exception as err:
            print "getCRL "
            print err
        return res


    def setCRL(self, new_connex, data):
        curs = new_connex.cursor()
        try:
            curs.execute(
                "INSERT INTO demande_crl(idpersonne, iddemande,id_role, rl, affiche, titulaire, president ) "
                "VALUES (%s, %s, %s,%s, %s, %s, %s)",
                (data[0], data[1], data[2],data[3], data[4], data[5],data[6]))
            new_connex.commit()
        except Exception as err:
            print "setCRL"
            print err
            new_connex.rollback()


    def getVoisins(self, idcommune):
        print "call of getVoisins"
        res = None
        try:
            cur = self.connexion.cursor()
            cur.execute(
                'SELECT * FROM limitesparcelle WHERE idparcelle IN (SELECT gid FROM parcelle_d WHERE id_commune =  %s)', (str(idcommune),)
            )
            res = cur.fetchall()
            cur.close()
        except Exception as err:
            print "getVoisins "
            print err
        return res


    def setVoisins(self, new_connex, data):
        curs = new_connex.cursor()
        try:
            curs.execute(
                "INSERT INTO limitesparcelle(idpointscardinaux, idparcelle,description ) "
                "VALUES (%s, %s, %s)",
                (data[0], data[1], data[2]))
            new_connex.commit()
        except Exception as err:
            print "setVoisins"
            print err
            new_connex.rollback()


    def getProprietaire(self, idcommune):
        print "call of getProprietaire"
        res = None
        try:
            cur = self.connexion.cursor()
            cur.execute(
                'SELECT * FROM proprietaireparcelle WHERE idparcelle IN (SELECT gid FROM parcelle_d WHERE id_commune =  %s)', (str(idcommune),)
            )
            res = cur.fetchall()
            cur.close()
        except Exception as err:
            print "getProprietaire "
            print err
        return res


    def setProprietaire(self, new_connex, data):
        curs = new_connex.cursor()
        try:
            curs.execute(
                "INSERT INTO proprietaireparcelle(idpersonne, idparcelle,representant,contribuable, estcoproprietaire ) "
                "VALUES (%s, %s, %s,%s, %s)",
                (data[0], data[1], data[2], data[3], data[4]))
            new_connex.commit()
        except Exception as err:
            print "setProprietaire"
            print err
            new_connex.rollback()



    def getAvoirDemande(self, idcommune):
        print "call of getAvoirDemande"
        res = None
        try:
            cur = self.connexion.cursor()
            cur.execute(
                'SELECT * FROM avoir_demande WHERE idparcelle IN (SELECT gid FROM parcelle_d WHERE id_commune =  %s)', (str(idcommune),)
            )
            res = cur.fetchall()
            cur.close()
        except Exception as err:
            print "getAvoirDemande "
            print err
        return res


    def setAvoirDemande(self, new_connex, data):
        curs = new_connex.cursor()
        try:
            curs.execute(
                "INSERT INTO avoir_demande(idpersonne, iddemande, idparcelle,representant,csv_id ) "
                "VALUES (%s, %s, %s,%s, %s)",
                (data[0], data[1], data[2], data[3], data[4]))
            new_connex.commit()
        except Exception as err:
            print "setAvoirDemande"
            print err
            new_connex.rollback()



    def getPersonne(self):
        print "call of get personne"
        res = None
        try:
            cur = self.connexion.cursor()
            cur.execute(
                'SELECT * FROM personne'
            )
            res = cur.fetchall()
            cur.close()
        except Exception as err:
            print "getPersonne "
            print err
        return res


    def setPersonne(self, new_connex, data):
        curs = new_connex.cursor()
        try:
            curs.execute(
                "INSERT INTO personne(idpersonne, nompersonne, prenompersonne,sexepersonne,datenaissancepersonne, nevers, lieunaissancepersonne, numcipersonne, datecipersonne, lieucipersonne, numactenaissancepersonne, "
                " dateactenaissancepersonne,lieuactenaissancepersonne, adressepersonne,situationmatrimoniale, nompere,"
                "nommere, csv_id, rcin_personne, ogr_id, handicap, niveau_education, possede_emploi, migrant,date_arrivee, conjoint ) "
                "VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s)",
                (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11]
                 , data[12], data[13], data[14], data[15], data[16], data[17], data[18], data[19], data[20], data[21], data[22], data[23]
                 , data[24], data[25]))
            new_connex.commit()
        except Exception as err:
            print "setPersonne"
            print err
            new_connex.rollback()

        # update des sequences
        try:
            curs.execute("SELECT setval('personne_idpersonne_seq', %s, TRUE)", (str(data[0]),))
            new_connex.commit()
        except Exception as err:
            print err
            new_connex.rollback()

    def getDemande(self, idcommune):
        print "call of get demande"
        res = None
        try:
            cur = self.connexion.cursor()
            cur.execute(
                'SELECT * FROM demande where idcommune = %s', (str(idcommune),)
            )
            res = cur.fetchall()
            cur.close()
        except Exception as err:
            print "getDemande "
            print err
        return res


    def setDemande(self, new_connex, data):
        curs = new_connex.cursor()
        try:
            curs.execute(
                "INSERT INTO demande(iddemande, numdemande, nomdemandeur,gid,datedemande, datereconnaissance, region, district, commune, fokontany, idfokontany, "
                " idcommune,idrejet, cout,consistance, idprojet,"
                "datedecision, csv_id, code_parcelle, categorie, opposition, planche_plof, charges, numdecision,debut_affichage, fin_affichage, numero_demande_lrsys,"
                "pvrl, cqe, date_cqe, resp_cqe,user_cqe, lieudit, collecteur_demande, duree_occupation, origine, avis_crl, texte_crl ) "
                "VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s,%s, %s, %s, %s,%s, %s, %s,%s, %s,%s, %s, %s)",
                (data[0], data[2], data[3], data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[16], data[17]
                 , data[18], data[19], data[20], data[21], data[23], data[24], data[25], data[26], data[27], data[28], data[29], data[30]
                 , data[31], data[32], data[33], data[34], data[35], data[36], data[37], data[38], data[39]
                 , data[40], data[41], data[42], data[43], data[44]))
            new_connex.commit()
        except Exception as err:
            print "setDemande"
            print err
            new_connex.rollback()

        # update des sequences
        try:
            curs.execute("SELECT setval('iddemande_seq', %s, TRUE)", (str(data[0]),))
            new_connex.commit()
        except Exception as err:
            print err
            new_connex.rollback()

    def getParcelle(self, idcommune):
        print "call of get Parcelle"
        res = None
        try:
            cur = self.connexion.cursor()
            cur.execute(
                'SELECT * FROM parcelle_d where id_commune = %s', (str(idcommune),)
            )
            res = cur.fetchall()
            cur.close()
        except Exception as err:
            print "getParcelle "
            print err
        return res


    def setParcelle(self, new_connex, data):
        curs = new_connex.cursor()
        try:
            curs.execute(
                "INSERT INTO parcelle_d(gid, geom, numdemande, nomdemandeur, surface,region, district, commune, fkt, "
                "consistance, idcertificat, idhameau,codeparcelle, estfiscalite,idcontribuable, grille,"
                "has_data, id_consistance, id_commune, csv_id, anomalie, limitrophe,inventaire, sujet_demande, date_inventaire,"
                "user_import_inv, date_import_inv, ref_import, categorie) "
                "VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s,%s, %s, %s)",
                (data[0], data[2], data[3], data[4], data[5], data[13], data[14], data[15], data[16], data[17], data[19], data[20]
                 , data[26], data[28], data[29], data[30], data[31], data[35], data[37], data[38], data[39], data[40], data[44], data[45]
                 , data[46], data[47], data[48], data[49], data[50]))
            new_connex.commit()
        except Exception as err:
            print "setParcelle"
            print err
            new_connex.rollback()

        # update des sequences
        try:
            curs.execute("SELECT setval('parcelle_d_id_seq', %s, TRUE)", (str(data[0]),))
            new_connex.commit()
        except Exception as err:
            print err
            new_connex.rollback()

    def setGroupe(self, new_connex, data):
        curs = new_connex.cursor()
        try:
            curs.execute(
                "INSERT INTO groupe(id, nom, description) "
                "VALUES (%s, %s, %s)",
                (data[0], data[1], data[2]))
            new_connex.commit()
        except Exception as err:
            print "setGroupe"
            print err
            new_connex.rollback()

        # update des sequences
        try:
            curs.execute("SELECT setval('groupe_id_seq', %s, TRUE)", (str(data[0]),))
            new_connex.commit()
        except Exception as err:
            print err
            new_connex.rollback()

    def getGroupe(self):
         res = None
         try:
             cur = self.connexion.cursor()
             cur.execute(
                 'SELECT * FROM groupe'
             )
             res = cur.fetchall()
             cur.close()
         except Exception as err:
             print "getGroupe"
             print err
         return res


    def setUser(self, new_connex, data):
        curs = new_connex.cursor()
        try:
            curs.execute(
                "INSERT INTO utilisateur(idutilisateur, nomutilisateur, prenomutilisateur,"
                " loginutilisateur, passwordutilisateur, telephone, adresse, fonction,loginufiplof,"
                " passwdfiplof, groupe_id ) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (data[0], data[1], data[2], data[3], data[4], data[6],data[7], data[8],data[9], data[10], data[11]))
            new_connex.commit()
        except Exception as err:
            print "setUser"
            print err
            new_connex.rollback()

        # update des sequences
        try:
            curs.execute("SELECT setval('utilisateur_id_seq', %s, TRUE)", (str(data[0]),))
            new_connex.commit()
        except Exception as err:
            print err
            new_connex.rollback()

    def getUser(self):
         res = None
         try:
             cur = self.connexion.cursor()
             cur.execute(
                 'SELECT * FROM utilisateur'
             )
             res = cur.fetchall()
             cur.close()
         except Exception as err:
             print "getUser"
             print err
         return res

    def setCertificat(self, new_connex, data):
        curs = new_connex.cursor()
        try:
            curs.execute(
                "INSERT INTO certificat(numerocertificat, numerodemande, datereconnaissance,"
                " typecertificat, datecreation, idcertificat, idfokontany, idprojet,isprint,"
                " idcommune, idhameau, code_hameau ) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (data[0], data[1], data[2], data[3], data[4], data[8],data[9], data[10],data[11], data[12], data[13], data[14]))
            new_connex.commit()
        except Exception as err:
            print "setCertificat"
            print err
            new_connex.rollback()

        # update des sequences
        try:
            curs.execute("SELECT setval('certificat_idcertificat_seq', %s, TRUE)", (str(data[8]),))
            new_connex.commit()
        except Exception as err:
            print err
            new_connex.rollback()

    def getCertificat(self, idcommune):
        res = None
        try:
            cur = self.connexion.cursor()
            cur.execute(
                'SELECT * FROM certificat WHERE idcommune = %s ORDER BY idcertificat', (str(idcommune),)
            )
            res = cur.fetchall()
            cur.close()
        except Exception as err:
            print "getCertificat"
            print err
        return res

    def setConsistance(self, new_connex, data):
        curs = new_connex.cursor()
        try:
            curs.execute("INSERT INTO consistance(idconsistance, libelleconsistance, parcelleoubatiment, valeurariary, valeurariary_ifpb) "
                         "VALUES (%s, %s, %s, %s, %s)", (data[0], data[1], data[2], data[3], data[4]))
            new_connex.commit()
        except Exception as err:
            print "setConsistance"
            print err
            new_connex.rollback()

        # update des sequences
        try:
            curs.execute("SELECT setval('consistance_id_seq', %s, TRUE)", (str(data[0]),))
            new_connex.commit()
        except Exception as err:
            print err
            new_connex.rollback()

    def getConsistance(self):
        res = None
        try:
            cur = self.connexion.cursor()
            cur.execute(
                'SELECT * FROM consistance  ORDER BY idconsistance'
                )
            res = cur.fetchall()
            cur.close()
        except Exception as err:
            print "getConsistance"
            print err
        return res


    def getParcelles(self, idcommune):
        res = None
        try:
            cur = self.connexion.cursor()
            cur.execute(
                'SELECT * FROM parcelle_d p  WHERE p.id_commune = %s ORDER BY p.gid',
                (str(idcommune),))
            res = cur.fetchall()
            cur.close()
        except Exception as err:
            print "getHameau"
            print err
        return res

    def setHameau(self, new_connex, data):
        curs = new_connex.cursor()
        try:
            curs.execute("INSERT INTO hameau(idhameau, idfokontany, codehameau, nomhameau) "
                         "VALUES (%s, %s, %s, %s)", (data[0], data[1], data[2], data[3]))
            new_connex.commit()
        except Exception as err:
            print "setHameau"
            print err
            new_connex.rollback()

        # update des sequences
        try:
            curs.execute("SELECT setval('hameau_id_seq', %s, TRUE)", (str(data[0]),))
            new_connex.commit()
        except Exception as err:
            print err
            new_connex.rollback()

    def getHameau(self, idfokontany):
        res = None
        try:
            cur = self.connexion.cursor()
            cur.execute(
                'SELECT * FROM hameau h  WHERE h.idfokontany = %s ORDER BY h.idhameau',
                (str(idfokontany),))
            res = cur.fetchall()
            cur.close()
        except Exception as err:
            print "getHameau"
            print err
        return res

    def setFokontany(self, new_connex, data):
        curs = new_connex.cursor()
        try:
            curs.execute("INSERT INTO fokontany(idfokontany, idcommune, codefokontany, nomfokontany) "
                         "VALUES (%s, %s, %s, %s)", (data[0], data[1], data[2], data[3]))
            new_connex.commit()
        except Exception as err:
            print "setFokontany"
            print err
            new_connex.rollback()

        # update des sequences
        try:
            curs.execute("SELECT setval('fokontany_id_seq', %s, TRUE)", (str(data[0]),))
            new_connex.commit()
        except Exception as err:
            print err
            new_connex.rollback()


    def getFokontany(self, idcommune):
        res = None
        try:
            cur = self.connexion.cursor()
            cur.execute(
                'SELECT * FROM fokontany f  WHERE f.idcommune = %s ORDER BY f.idfokontany',
                (str(idcommune),))
            res = cur.fetchall()
            cur.close()
        except Exception as err:
            print "getFokontany"
            print err
        return res

    def setProjetCouche(self, new_connex, data):
        curs = new_connex.cursor()
        # PROJET COUCHE
        try:
            curs.execute(
                "INSERT INTO projetcouche (id, idprojet_commune, libelle, type_couche, fichier, couleur_bg, ordre, label_name, show_label, "
                "font, font_size, font_size_map_unit, font_color, show_stroke, stroke_width, stroke_color, remplissage, plofpaps)"
                "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (data[0], data[1], data[2], data[3], data[4], data[5],data[6], data[7], data[8], data[9], data[10], data[11],
                 data[12], data[13], data[14], data[15], data[16], data[17]))
            new_connex.commit()
        except Exception as err:
            print "setProjetCouche"
            print err
            new_connex.rollback()

        # update des sequences
        try:
            curs.execute("SELECT setval('projetcouche_id_seq', %s, TRUE)", (str(data[0]),))
            new_connex.commit()
        except Exception as err:
            print err
            new_connex.rollback()

    def getProjetCouche(self, idprojet_commune):
        res = None
        try:
            cur = self.connexion.cursor()
            cur.execute(
                'SELECT * FROM projetcouche p  WHERE p.idprojet_commune = %s ORDER BY p.id',
                (str(idprojet_commune),))
            res = cur.fetchall()
            cur.close()
        except Exception as err:
            print "getProjetCouche"
            print err
        return res

    def getProjet(self, commune):
        print "*****************idcommune******************************"
        print commune[0]
        res = None
        try:
            cur = self.connexion.cursor()
            cur.execute(
                'SELECT * FROM projet p INNER JOIN projet_commune pc ON p.idprojet = pc.idprojet INNER JOIN commune c ON pc.idcommune = c.idcommune WHERE c.idcommune = %s ',
                (str(commune[0]),))
            res = cur.fetchone()
            cur.close()
        except Exception as err:
            print err
        return res

    def setProjet(self, new_connex, data):
        curs = new_connex.cursor()
        #PROJET
        try:
            curs.execute("INSERT INTO projet (idprojet, date_lancement, date_premier_import, date_dernier_import, langue, nom) "
                         "VALUES(%s, %s, %s, %s, %s, %s)", (str(data[0]), data[1], data[2],data[3], str(data[4]), str(data[5])))
            new_connex.commit()
        except Exception as err:
            print "Projet error"
            print err
            new_connex.rollback()

        # update des sequences
        try:
            curs.execute("SELECT setval('projet_idprojet_seq', %s, TRUE)", (str(data[0]),))
            new_connex.commit()
        except Exception as err:
            print err
            new_connex.rollback()
        #PROJET COMMUNE
        try:
            curs.execute("INSERT INTO projet_commune (idprojet_commune, idcommune, idprojet, fond_image, couche_titres, couche_cadastres, couche_limites) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s)", (str(data[6]), str(data[7]), str(data[8]),data[9], data[10], data[11], data[12]))
            new_connex.commit()
        except Exception as err:
            print "Projet Commune error"
            print err
            new_connex.rollback()

        # update des sequences
        try:
            curs.execute("SELECT setval('projet_commune_idprojet_commune_seq', %s, TRUE)", (str(data[6]),))
            new_connex.commit()
        except Exception as err:
            print err
            new_connex.rollback()

    def getRDC(self, commune):
        res = None
        try:
            cur = self.connexion.cursor()
            cur.execute('select * from region r INNER JOIN district d ON r.idregion = d.idregion INNER JOIN commune c ON c.iddistrict = d.iddistrict WHERE idcommune = %s',
                        (str(commune[0]),))
            res  = cur.fetchone()
            cur.close()
        except Exception as err:
            print err
        return res

    def setRDC(self, new_connex, data):
        curs = new_connex.cursor()
        try:
            curs.execute("INSERT INTO region (idregion, coderegion, nomregion) "
                         "VALUES(%s, %s, %s)", (str(data[0]), str(data[1]), str(data[2])))
            new_connex.commit()
        except Exception as err:
            print err
            new_connex.rollback()

        try:
            curs.execute("INSERT INTO district (iddistrict, codedistrict, nomdistrict, idregion) "
                         "VALUES(%s, %s, %s, %s)", (str(data[6]), str(data[8]), str(data[9]), str(data[7])))
            new_connex.commit()
        except Exception as err:
            print err
            new_connex.rollback()
        try:
            curs.execute("INSERT INTO commune (idcommune, iddistrict, codecommune, "
                         "nomcommune, cptcertificat, cptimport, cptdemande, codeg) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (str(data[13]), str(data[14]), str(data[15]), str(data[16]), str(data[19]), str(data[20]), str(data[21]), str(data[22])))
            new_connex.commit()
        except Exception as err:
            print err
            new_connex.rollback()

        #update des sequences
        try:
            curs.execute("SELECT setval('region_id_seq', %s, TRUE)", (str(data[0]),))
            new_connex.commit()
        except Exception as err:
            print err
            new_connex.rollback()

        try:
            curs.execute("SELECT setval('district_id_seq', %s, TRUE)", (str(data[6]),))
            new_connex.commit()
        except Exception as err:
            print err
            new_connex.rollback()

        try:
            curs.execute("SELECT setval('commune_id_seq', %s, TRUE)", (str(data[13]),))
            new_connex.commit()
        except Exception as err:
            print err
            new_connex.rollback()




