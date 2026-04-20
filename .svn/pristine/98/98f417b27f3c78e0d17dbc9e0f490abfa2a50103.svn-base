import psycopg2
import psycopg2.extras
import globalvars
from datetime import datetime


class Demande:
    def __init__(self):
        self.iddemande, self.numdemande, self.nomdemandeur, self.adressepersonne = "", "", "", ""
        self.numdemandepaps, self.limite = "", ""
        self.nom, self.surface = "", 0
        self.codehameau, self.nomfokontany, self.nomhameau = "", "",""
        self.voisins = []
        self.numdecision,self.datedecision="",""
        self.debutaffichage, self.finaffichage = "", ""
        self.dateReconnaissance = ''
        self.datedemande=''
        self.nbreJour = 0
        self.codeParcelle = ''
        self.codePlanche = ''
        self.adresse = ''
        self.limites = []
        self.membre_crl = []
        self.lieudit = ''
        self.collecteur = ''
        self.genre = 'L'
        self.dateNaissance = ''
        self.ne_vers = ''
        self.num_cin = ''
        self.num_copie = ''
        self.datepi = ''
        self.lieupi = ''
        self.categorie = ''
        self.consistance = ''
        self.demandeurs = []
        self.idx_dem_principale = 0
        self.duree_occupation = ''
        self.origine = ''
        self.avis_crl = ''
        self.charge = ''
        self.ids_crl = []
        self.idDemandeurPrincipale = None
        self.idparcelle = None
        self.idPresidentCrl = None

    @staticmethod
    def findBetween(connection, date1, date2):
        demandes = []
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT * FROM demande WHERE datedemande BETWEEN %s AND %s", (date1, date2))
            rows = cursor.fetchall()
            for r in rows:
                d = Demande()
                d.map(r)
                demandes.append(d)
        except Exception as e:
            print(e)
        cursor.close()
        return demandes

    @staticmethod
    def find_where(connection, metadata, wheres=[], page=1, withLimit = True):
        metadata["numpages"] = 2
        offset = (page - 1) * globalvars.LimitSelect
        demandes = []
        where = ""
        if len(wheres) > 0:
            where = "WHERE " + " AND ".join(wheres)
        sql = """WITH Q1 AS (
            SELECT demande.iddemande, STRING_AGG(CONCAT(P.nompersonne,' ', coalesce(P.prenompersonne,''))||'<FIELD>' || P.sexepersonne||'<FIELD>' || coalesce(P.datenaissancepersonne,'1000-01-01')||'<FIELD>' 
                           || coalesce(P.nevers,0)||'<FIELD>' || coalesce(P.numcipersonne,'')||'<FIELD>' || 
                           coalesce(P.numactenaissancepersonne,'')||'<FIELD>' || coalesce(P.datecipersonne,'1000-01-01')||'<FIELD>' || coalesce(P.lieucipersonne,'')||'<FIELD>' || coalesce(P.dateactenaissancepersonne,'1000-01-01')||
                           '<FIELD>' || coalesce(P.lieuactenaissancepersonne,'')||'<FIELD>' || coalesce(P.adressepersonne,'')||'<FIELD>' || coalesce(A.representant,'FALSE') ,'<ROW>') AS demandeurs 
                           FROM demande 
                           LEFT JOIN avoir_demande A on A.iddemande = demande.iddemande 
                           LEFT JOIN personne P on P.idpersonne = A.idpersonne 
                           GROUP BY demande.iddemande
        ),
         Q2 AS (
            SELECT demande.iddemande, STRING_AGG(L.idpointscardinaux || '<FIELD>' || L.description, '| ') AS limite
            FROM demande
            LEFT JOIN limitesparcelle L on L.idparcelle = demande.gid 
            GROUP BY demande.iddemande
        ), Q3 AS (
            SELECT demande.iddemande, STRING_AGG(V.nom || '<FIELD>' || coalesce(v.prenom, '') || '<FIELD>' || v.adresse, '<ROW>') AS voisins
            FROM demande
            LEFT JOIN voisinparcelle VP on VP.iddemande = demande.iddemande
            LEFT JOIN voisins V on V.idvoisin = VP.idvoisin
            GROUP BY demande.iddemande
        ), Q4 AS (
        SELECT  demande.iddemande, STRING_AGG(CONCAT(p.nompersonne,' ', coalesce(p.prenompersonne,'')) || '<FIELD>' || p.numcipersonne || '<FIELD>' || dc.titulaire || '<FIELD>' || rc.id_role || '<FIELD>' || rc.libelle_role, '<ROW>') AS membre_crl 
         FROM demande
         JOIN demande_crl dc ON demande.iddemande = dc.iddemande 
         JOIN personne p ON p.idpersonne = dc.idpersonne 
         JOIN role_crl rc ON dc.id_role = rc.id_role 
         GROUP BY demande.iddemande
         )

        SELECT demande.*, st_area(P.geom) as surface, Q1.demandeurs, Q1.*, Q2.limite, COALESCE(H.codehameau, '') AS codehameau
        , COALESCE(H.nomhameau, '') AS nomhameau, Q3.voisins, Q4.membre_crl
        FROM demande
        JOIN Q1 ON Q1.iddemande = demande.iddemande
        JOIN Q2 ON Q2.iddemande = demande.iddemande
        JOIN Q3 ON Q3.iddemande = demande.iddemande
        JOIN Q4 ON Q4.iddemande = demande.iddemande
        JOIN parcelle_d P on P.gid = demande.gid
        LEFT JOIN hameau H on H.idhameau = P.idhameau
        %s
        """ % where
        sql_count = "WITH Q AS (%s) SELECT COUNT(*) AS num FROM Q" % sql
        if withLimit == True:
            sql += " LIMIT " + str(globalvars.LimitSelect) + " OFFSET " + str(offset)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            if len (rows) <= 0:
                print ("**************RESULTAT DE LE REQUETE VIDE**************")
            for r in rows:
                d = Demande()
                d.map(r)
                demandes.append(d)
        except Exception as e:
            connection.rollback()
            print(e)
        try:
            cursor.execute(sql_count)
            row = cursor.fetchone()
            metadata["numpages"] = (int(row["num"]) / globalvars.LimitSelect) + 1
        except Exception as e:
            connection.rollback()
            print(e)
        cursor.close()
        return demandes

    @staticmethod
    def find_by_id(connection, iddemande):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT * FROM demande WHERE iddemande=%s", (iddemande,))
            res = cursor.fetchone()
            t = Demande()
            t.map(res)
            return t
        except Exception as e:
            print(e)
        cursor.close()
        return None

    def map(self, res):
        self.iddemande, self.numdemande, self.nomdemandeur, self.datedemande = \
            res["iddemande"], res["numdemande"], res["nomdemandeur"], res["datedemande"]
        self.numdemandepaps, self.limite = res["numdemandepaps"], res["limite"]
        if res['demandeurs'] is not None:
            tab = res['demandeurs'].split("<ROW>")
            for i in tab:
                (nom, genre, datenaissance, nevers, numci, numacte, dateci, lieuci, dateacte, lieuacte, adresse, representant) = i.split("<FIELD>")
                self.demandeurs.append({'nom':nom, 'genre':genre, 'datenaissance':datenaissance, 'nevers':nevers, 'numci':numci, 'numacte':numacte, 'dateci':dateci, 'lieuci':lieuci, 'dateacte':dateacte, 'lieuacte':lieuacte, 'adresse':adresse, 'representant':representant})
        print self.demandeurs
        idx_dem = 0
        for dem in self.demandeurs:
            if dem['representant'] == 'true':
                print dem['representant']
                break
            idx_dem = idx_dem + 1
        if idx_dem >= len(self.demandeurs):
            idx_dem = 0

        self.idx_dem_principale = idx_dem
        self.nom = self.demandeurs[idx_dem]['nom']
        # print self.nom
        self.adresse = self.demandeurs[idx_dem]['adresse']
        #print self.adresse
        self.surface = res["surface"]
        self.codehameau, self.nomhameau = res["codehameau"], res["nomhameau"]
        self.adressepersonne = self.demandeurs[idx_dem]['adresse']
        self.numdecision = res['numdecision']
        self.datedecision = res['datedecision']
        self.nomfokontany = res['fokontany']
        self.dateReconnaissance = res['datereconnaissance']
        self.debutaffichage = res['debut_affichage']
        self.finaffichage = res['fin_affichage']
        self.codeParcelle = res['code_parcelle']
        if res['avis_crl'] is not None:
            if res['avis_crl'] == True:
                self.avis_crl = "Ny mpikambana ao amin'ny kaomity mpitsirika dia miara-manaiky fa azo omena ny Karatrany"
            else:
                self.avis_crl = ""
        if res['duree_occupation'] is not None:
            self.duree_occupation = str(res['duree_occupation'])
        if res['origine'] is not None:
            self.origine = str(res['origine'])
        if res['consistance'] is not None:
            self.consistance = res['consistance']
        if res['planche_plof'] is not None:
            self.codePlanche = res['planche_plof']
        if res['categorie'] is not None:
            self.categorie = res['categorie']
        if self.demandeurs[idx_dem]['genre'] == 'feminin':
            self.genre = 'V'
        if self.demandeurs[idx_dem]['datenaissance'] != '1000-01-01':
            self.dateNaissance = datetime.strptime(self.demandeurs[idx_dem]['datenaissance'],('%Y-%m-%d')).strftime("%d/%m/%Y")
        else:
            if self.demandeurs[idx_dem]['nevers'] != '':
                self.ne_vers = self.demandeurs[idx_dem]['nevers']

        if self.demandeurs[idx_dem]['numci'] != '':
            self.num_cin = self.demandeurs[idx_dem]['numci']
            if self.demandeurs[idx_dem]['dateci'] != '1000-01-01':
                self.datepi = datetime.strptime(self.demandeurs[idx_dem]['dateci'],('%Y-%m-%d')).strftime("%d/%m/%Y")
            if self.demandeurs[idx_dem]['lieuci'] != '':
                self.lieupi = self.demandeurs[idx_dem]['lieuci']

        else:
            if self.demandeurs[idx_dem]['numacte'] != '':
                self.num_copie = self.demandeurs[idx_dem]['numacte']
                if self.demandeurs[idx_dem]['dateacte'] != '1000-01-01':
                    self.datepi = datetime.strptime(self.demandeurs[idx_dem]['dateacte'],('%Y-%m-%d')).strftime("%d/%m/%Y")
                if self.demandeurs[idx_dem]['lieuacte'] != '':
                    self.lieupi = self.demandeurs[idx_dem]['lieuacte']


        try:
            self.lieudit = res['lieudit']
        except Exception as err:
            pass
        try:
            self.collecteur = res['collecteur_demande']
        except Exception as err:
            pass

        if res['fin_affichage'] is not None and res['debut_affichage'] is not None:
            delta = res['fin_affichage'] - res['debut_affichage']
            self.nbreJour = delta.days
        if res["voisins"] is not None:
            tab = res["voisins"].split("<ROW>")
            for i in tab:
                (nom, prenom, adresse) = i.split("<FIELD>")
                self.voisins.append({'nom': nom, 'prenom': prenom, 'adresse': adresse})
        print(self.voisins)
        if res['limite'] is not None:
            tab = res["limite"].split("|")
            for i in tab:
                (idpoint, description) = i.split("<FIELD>")
                self.limites.append({idpoint.strip():description.strip()})
        print self.limites

        #Membre CRL

        if res['membre_crl'] is not None:
            tab = res["membre_crl"].split("<ROW>")
            for i in tab:
                (nom, numci, titulaire, id_role, role) = i.split("<FIELD>")
                print titulaire
                key = str(id_role)
                if titulaire == 'true':
                    key = key+'_t'
                if titulaire == 'false':
                    key = key+'_f'
                cin_nom = nom + ':' + numci
                self.membre_crl.append({key: cin_nom})
        print self.membre_crl

    @staticmethod
    def updateDecision(self, connection):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        #cursor = connection.cursor()
        print("----test---")
        try:
            sql="UPDATE demande SET numdecision= %s, datedecision=%s WHERE iddemande=%s"
            #print sql
            cursor.execute(sql,(self.numdecision,self.datedecision,self.iddemande))
            connection.commit()
            return True
        except Exception as e:
            print(e)
            print("---EXCEPTION TO UPDATE")
            cursor.close()
            connection.rollback()
            return False

    @staticmethod
    def updateAffichage(self, connection):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # cursor = connection.cursor()
        print("----modele date affichage---")
        try:
            sql = "UPDATE demande SET debut_affichage= %s, fin_affichage=%s WHERE iddemande=%s AND cqe is null or cqe is false "
            #print sql
            cursor.execute(sql, (self.debutaffichage, self.finaffichage, self.iddemande))
            connection.commit()
            return True
        except Exception as e:
            print(e)
            print("---EXCEPTION TO UPDATE")
            cursor.close()
            connection.rollback()
            return False

    @staticmethod
    def updatedateRL(self,connection):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # cursor = connection.cursor()
        print("----test---")
        try:
            sql = "UPDATE demande SET datereconnaissance= %s WHERE iddemande=%s"
            #print sql
            cursor.execute(sql, (self.datereconnaissance, self.iddemande))
            connection.commit()
            return True
        except Exception as e:
            print(e)
            print("---EXCEPTION TO UPDATE")
            cursor.close()
            connection.rollback()
            return False

    @staticmethod
    def updatedatDemande(self,connection):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # cursor = connection.cursor()
        print("----demande---")
        try:
            sql = "UPDATE demande SET datedemande= %s WHERE iddemande=%s"
            # print sql
            cursor.execute(sql, (self.datedemande, self.iddemande))
            connection.commit()
            return True
        except Exception as e:
            print(e)
            print("---EXCEPTION TO UPDATE date demande")
            cursor.close()
            connection.rollback()
            return False

    @staticmethod
    def select_dmd(connection, metadata, wheres=[], page=1, withLimit=True):
        #print 'ato am select'
        metadata["numpages"] = 2
        offset = (page - 1) * globalvars.LimitSelect
        demandes = []
        where = ""
        print "ato am selec"
        if len(wheres) > 0:
            where = "WHERE " + " "+ wheres
            print 'where %s', (where)
        sql = """WITH Q1 AS (
                SELECT demande.iddemande, STRING_AGG(CONCAT(P.nompersonne,' ', coalesce(P.prenompersonne,''))||'<FIELD>' || P.sexepersonne||'<FIELD>' || coalesce(P.datenaissancepersonne,'1000-01-01')||'<FIELD>' 
                               || coalesce(P.nevers,0)||'<FIELD>' || coalesce(P.numcipersonne,'')||'<FIELD>' || 
                               coalesce(P.numactenaissancepersonne,'')||'<FIELD>' || coalesce(P.datecipersonne,'1000-01-01')||'<FIELD>' || coalesce(P.lieucipersonne,'')||'<FIELD>' || coalesce(P.dateactenaissancepersonne,'1000-01-01')||
                               '<FIELD>' || coalesce(P.lieuactenaissancepersonne,'')||'<FIELD>' || coalesce(P.adressepersonne,'')||'<FIELD>' || coalesce(P.nompere,'')||'<FIELD>' || coalesce(P.nommere,'')||'<FIELD>' || coalesce(P.conjoint,'')||'<FIELD>' || P.idpersonne||
                               '<FIELD>' || coalesce(A.representant,'FALSE') ,'<ROW>') AS demandeurs 
                               FROM demande 
                               LEFT JOIN avoir_demande A on A.iddemande = demande.iddemande 
                               LEFT JOIN personne P on P.idpersonne = A.idpersonne 
                               GROUP BY demande.iddemande
            )

            SELECT demande.*, Q1.demandeurs, Q1.*,COALESCE(H.codehameau, '') AS codehameau
            , COALESCE(H.nomhameau, '') AS nomhameau
            FROM demande
            JOIN Q1 ON Q1.iddemande = demande.iddemande
            JOIN parcelle_d P on P.gid = demande.gid
            LEFT JOIN hameau H on H.idhameau = P.idhameau
            %s
            """ % where
        sql_count = "WITH Q AS (%s) SELECT COUNT(*) AS num FROM Q" % sql
        if withLimit == True:
            sql += " LIMIT " + str(globalvars.LimitSelect) + " OFFSET " + str(offset)
        print'--------sql'
        #print sql
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            for r in rows:
                d = Demande()
                d.maplisting(r)
                demandes.append(d)
        except Exception as e:
            connection.rollback()
            print(e)
        cursor.close()
        #print '--------demandes---------'
        #print demandes
        return demandes


    def maplisting(self, res):
        #print "ato amin mplisting"
        try :
            self.iddemande, self.numdemande, self.nomdemandeur, self.datedemande = \
                res["iddemande"], res["numdemande"], res["nomdemandeur"], res["datedemande"]
            self.numdemandepaps= res["numdemandepaps"]
            if res['demandeurs'] is not None:
                tab = res['demandeurs'].split("<ROW>")
                for i in tab:

                    (
                    nom, genre, datenaissance, nevers, numci, numacte, dateci, lieuci, dateacte, lieuacte, adresse, nompere,
                    nommere, conjoint,idpersonne,
                    representant) = i.split("<FIELD>")
                    self.demandeurs.append(
                        {'nom': nom, 'genre': genre, 'datenaissance': datenaissance, 'nevers': nevers, 'numci': numci,
                         'numacte': numacte, 'dateci': dateci, 'lieuci': lieuci, 'dateacte': dateacte,
                         'lieuacte': lieuacte, 'adresse': adresse, 'nompere': nompere, 'nommere': nommere,
                         'conjoint': conjoint,'idpersonne':idpersonne, 'representant': representant})
            #print self.demandeurs
            idx_dem = 0
            for dem in self.demandeurs:
                if dem['representant'] == 'true':
                    print dem['representant']
                    break
                idx_dem = idx_dem + 1
            if idx_dem >= len(self.demandeurs):
                idx_dem = 0

            self.idx_dem_principale = idx_dem
            self.nom = self.demandeurs[idx_dem]['nom']
            self.idx_idpersonne_principale=self.demandeurs[idx_dem]['idpersonne']
            # print self.nom
            self.adresse = self.demandeurs[idx_dem]['adresse']
            # print self.adresse
            # self.surface = res["surface"]
            self.codehameau, self.nomhameau = res["codehameau"], res["nomhameau"]
            self.adressepersonne = self.demandeurs[idx_dem]['adresse']
            self.numdecision = res['numdecision']
            self.datedecision = res['datedecision']
            self.nomfokontany = res['fokontany']
            if res['fokontany'] is None:
                self.nomfokontany = ""
            self.dateReconnaissance = res['datereconnaissance']
            self.debutaffichage = res['debut_affichage']
            self.finaffichage = res['fin_affichage']
            self.codeParcelle = res['code_parcelle']
            if res['code_parcelle'] is None:
                self.codeParcelle = ""
            if res['consistance'] is not None:
                self.consistance = res['consistance']
            if res['planche_plof'] is not None:
                self.codePlanche = res['planche_plof']
            if res['categorie'] is not None:
                self.categorie = res['categorie']
            if self.demandeurs[idx_dem]['genre'] == 'feminin':
                self.genre = 'V'
            if self.demandeurs[idx_dem]['datenaissance'] != '1000-01-01':
                self.dateNaissance = datetime.strptime(self.demandeurs[idx_dem]['datenaissance'],
                                                       ('%Y-%m-%d')).strftime("%d/%m/%Y")
            else:
                if self.demandeurs[idx_dem]['nevers'] != '':
                    self.ne_vers = self.demandeurs[idx_dem]['nevers']

            if self.demandeurs[idx_dem]['numci'] != '':
                self.num_cin = self.demandeurs[idx_dem]['numci']
                if self.demandeurs[idx_dem]['dateci'] != '1000-01-01':
                    self.datepi = datetime.strptime(self.demandeurs[idx_dem]['dateci'], ('%Y-%m-%d')).strftime(
                        "%d/%m/%Y")
                if self.demandeurs[idx_dem]['lieuci'] != '':
                    self.lieupi = self.demandeurs[idx_dem]['lieuci']

            else:
                if self.demandeurs[idx_dem]['numacte'] != '':
                    self.num_copie = self.demandeurs[idx_dem]['numacte']
                    if self.demandeurs[idx_dem]['dateacte'] != '1000-01-01':
                        self.datepi = datetime.strptime(self.demandeurs[idx_dem]['dateacte'], ('%Y-%m-%d')).strftime(
                            "%d/%m/%Y")
                    if self.demandeurs[idx_dem]['lieuacte'] != '':
                        self.lieupi = self.demandeurs[idx_dem]['lieuacte']

            try:
                self.lieudit = res['lieudit']
                if res['lieudit'] is None:
                    self.lieudit = ""
            except Exception as err:
                pass
            try:
                self.collecteur = res['collecteur_demande']
                if res['collecteur_demande'] is None:
                    self.collecteur = ""
            except Exception as err:
                pass

            if res['fin_affichage'] is not None and res['debut_affichage'] is not None:
                delta = res['fin_affichage'] - res['debut_affichage']
                self.nbreJour = delta.days

        except Exception as e:
            print "errer ato amin mplisting"
            print(e)

    @staticmethod
    def find_where_PV(connection, metadata, wheres=[], page=1, withLimit=True):
        metadata["numpages"] = 2
        offset = (page - 1) * globalvars.LimitSelect
        demandes = []
        where = ""
        if len(wheres) > 0:
            where = "WHERE " + " AND ".join(wheres)
        sql = """WITH Q1 AS (
                SELECT demande.iddemande, STRING_AGG(CONCAT(P.nompersonne,' ', coalesce(P.prenompersonne,''))||'<FIELD>' || P.sexepersonne||'<FIELD>' || coalesce(P.datenaissancepersonne,'1000-01-01')||'<FIELD>' 
                               || coalesce(P.nevers,0)||'<FIELD>' || coalesce(P.numcipersonne,'')||'<FIELD>' || 
                               coalesce(P.numactenaissancepersonne,'')||'<FIELD>' || coalesce(P.datecipersonne,'1000-01-01')||'<FIELD>' || coalesce(P.lieucipersonne,'')||'<FIELD>' || coalesce(P.dateactenaissancepersonne,'1000-01-01')||
                               '<FIELD>' || coalesce(P.lieuactenaissancepersonne,'')||'<FIELD>' || coalesce(P.adressepersonne,'')||'<FIELD>' || coalesce(A.representant,'FALSE') ||'<FIELD>' || P.idpersonne,'<ROW>') AS demandeurs 
                               FROM demande 
                               LEFT JOIN avoir_demande A on A.iddemande = demande.iddemande 
                               LEFT JOIN personne P on P.idpersonne = A.idpersonne 
                               GROUP BY demande.iddemande
            ),
             Q2 AS (
                SELECT demande.iddemande, STRING_AGG(L.idpointscardinaux || '<FIELD>' || L.description, '| ') AS limite
                FROM demande
                LEFT JOIN limitesparcelle L on L.idparcelle = demande.gid 
                GROUP BY demande.iddemande
            ), Q3 AS (
                SELECT demande.iddemande, STRING_AGG(V.nom || '<FIELD>' || coalesce(v.prenom, '') || '<FIELD>' || v.adresse, '<ROW>') AS voisins
                FROM demande
                LEFT JOIN voisinparcelle VP on VP.iddemande = demande.iddemande
                LEFT JOIN voisins V on V.idvoisin = VP.idvoisin
                GROUP BY demande.iddemande
            ), Q4 AS (
            SELECT  demande.iddemande, STRING_AGG(CONCAT(p.nompersonne,' ', coalesce(p.prenompersonne,'')) || '<FIELD>' || p.numcipersonne || '<FIELD>' || dc.titulaire || '<FIELD>' || rc.id_role || '<FIELD>' || rc.libelle_role || '<FIELD>' || dc.idpersonne || '<FIELD>' || dc.president, '<ROW>') AS membre_crl 
             FROM demande
             JOIN demande_crl dc ON demande.iddemande = dc.iddemande 
             JOIN personne p ON p.idpersonne = dc.idpersonne 
             JOIN role_crl rc ON dc.id_role = rc.id_role WHERE dc.rl = TRUE
             GROUP BY demande.iddemande
             ),Q5 AS (
             SELECT  demande.iddemande, a.descriptioncharge 
             FROM autrecharge a 
             JOIN autrechargesparcelle_d ad on  a.idparcelle = ad.idparcelle 
             JOIN parcelle_d pd ON ad.idparcelle = pd.gid 
             JOIN demande on demande.gid = pd.gid
             )

            SELECT demande.*, st_area(P.geom) as surface, Q1.demandeurs, Q1.*, Q2.limite, COALESCE(H.codehameau, '') AS codehameau
            , COALESCE(H.nomhameau, '') AS nomhameau, Q3.voisins, Q4.membre_crl, Q5.*
            FROM demande
            JOIN Q1 ON Q1.iddemande = demande.iddemande
            JOIN Q2 ON Q2.iddemande = demande.iddemande
            JOIN Q3 ON Q3.iddemande = demande.iddemande
            LEFT JOIN Q5 ON Q5.iddemande = demande.iddemande
            JOIN Q4 ON Q4.iddemande = demande.iddemande
            JOIN parcelle_d P on P.gid = demande.gid
            LEFT JOIN hameau H on H.idhameau = P.idhameau
            %s
            """ % where
        sql_count = "WITH Q AS (%s) SELECT COUNT(*) AS num FROM Q" % sql
        if withLimit == True:
            sql += " LIMIT " + str(globalvars.LimitSelect) + " OFFSET " + str(offset)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            for r in rows:
                d = Demande()
                d.mapPVRL(r)
                demandes.append(d)
        except Exception as e:
            connection.rollback()
            print(e)
        try:
            cursor.execute(sql_count)
            row = cursor.fetchone()
            metadata["numpages"] = (int(row["num"]) / globalvars.LimitSelect) + 1
        except Exception as e:
            connection.rollback()
            print(e)
        cursor.close()
        return demandes

    def mapPVRL(self, res):
        self.iddemande, self.numdemande, self.nomdemandeur, self.datedemande = \
            res["iddemande"], res["numdemande"], res["nomdemandeur"], res["datedemande"]
        self.numdemandepaps, self.limite = res["numdemandepaps"], res["limite"]
        self.idparcelle = res['gid']
        if res['demandeurs'] is not None:
            tab = res['demandeurs'].split("<ROW>")
            for i in tab:
                (nom, genre, datenaissance, nevers, numci, numacte, dateci, lieuci, dateacte, lieuacte, adresse, representant, idpersonne) = i.split("<FIELD>")
                self.demandeurs.append({'nom':nom, 'genre':genre, 'datenaissance':datenaissance, 'nevers':nevers, 'numci':numci, 'numacte':numacte, 'dateci':dateci, 'lieuci':lieuci, 'dateacte':dateacte, 'lieuacte':lieuacte, 'adresse':adresse, 'representant':representant, 'idpersonne': idpersonne})
        print self.demandeurs
        idx_dem = 0
        for dem in self.demandeurs:
            if dem['representant'] == 'true':
                print dem['representant']
                break
            idx_dem = idx_dem + 1
        if idx_dem >= len(self.demandeurs):
            idx_dem = 0

        self.idx_dem_principale = idx_dem
        self.nom = self.demandeurs[idx_dem]['nom']
        self.idDemandeurPrincipale = self.demandeurs[idx_dem]['idpersonne']
        print "demandeur principale"
        print self.idDemandeurPrincipale
        # print self.nom
        self.adresse = self.demandeurs[idx_dem]['adresse']
        print "CHARGE ***********************************************************"
        if res['descriptioncharge'] is not None:
            self.charge = str(res['descriptioncharge'])
        print self.charge
        #print self.adresse
        self.surface = res["surface"]
        self.codehameau, self.nomhameau = res["codehameau"], res["nomhameau"]
        self.adressepersonne = self.demandeurs[idx_dem]['adresse']
        self.numdecision = res['numdecision']
        self.datedecision = res['datedecision']
        self.nomfokontany = res['fokontany']
        self.dateReconnaissance = res['datereconnaissance']
        self.debutaffichage = res['debut_affichage']
        self.finaffichage = res['fin_affichage']
        self.codeParcelle = res['code_parcelle']
        if res['texte_crl'] is not None:
            self.avis_crl = res['texte_crl']

        if res['duree_occupation'] is not None:
            self.duree_occupation = str(res['duree_occupation'])
        if res['origine'] is not None:
            self.origine = str(res['origine'])
        if res['consistance'] is not None:
            self.consistance = res['consistance']
        if res['planche_plof'] is not None:
            self.codePlanche = res['planche_plof']
        if res['categorie'] is not None:
            self.categorie = res['categorie']
        if self.demandeurs[idx_dem]['genre'] == 'feminin':
            self.genre = 'V'
        if self.demandeurs[idx_dem]['datenaissance'] != '1000-01-01':
            self.dateNaissance = datetime.strptime(self.demandeurs[idx_dem]['datenaissance'],('%Y-%m-%d')).strftime("%d/%m/%Y")
        else:
            if self.demandeurs[idx_dem]['nevers'] != '':
                self.ne_vers = self.demandeurs[idx_dem]['nevers']

        if self.demandeurs[idx_dem]['numci'] != '':
            self.num_cin = self.demandeurs[idx_dem]['numci']
            if self.demandeurs[idx_dem]['dateci'] != '1000-01-01':
                self.datepi = datetime.strptime(self.demandeurs[idx_dem]['dateci'],('%Y-%m-%d')).strftime("%d/%m/%Y")
            if self.demandeurs[idx_dem]['lieuci'] != '':
                self.lieupi = self.demandeurs[idx_dem]['lieuci']

        else:
            if self.demandeurs[idx_dem]['numacte'] != '':
                self.num_copie = self.demandeurs[idx_dem]['numacte']
                if self.demandeurs[idx_dem]['dateacte'] != '1000-01-01':
                    self.datepi = datetime.strptime(self.demandeurs[idx_dem]['dateacte'],('%Y-%m-%d')).strftime("%d/%m/%Y")
                if self.demandeurs[idx_dem]['lieuacte'] != '':
                    self.lieupi = self.demandeurs[idx_dem]['lieuacte']


        try:
            self.lieudit = res['lieudit']
        except Exception as err:
            pass
        try:
            self.collecteur = res['collecteur_demande']
        except Exception as err:
            pass

        if res['fin_affichage'] is not None and res['debut_affichage'] is not None:
            delta = res['fin_affichage'] - res['debut_affichage']
            self.nbreJour = delta.days
        if res["voisins"] is not None:
            tab = res["voisins"].split("<ROW>")
            for i in tab:
                (nom, prenom, adresse) = i.split("<FIELD>")
                self.voisins.append({'nom': nom, 'prenom': prenom, 'adresse': adresse})
        print(self.voisins)
        if res['limite'] is not None:
            tab = res["limite"].split("|")
            for i in tab:
                (idpoint, description) = i.split("<FIELD>")
                self.limites.append({idpoint.strip():description.strip()})
        print self.limites

        #Membre CRL

        if res['membre_crl'] is not None:
            tab = res["membre_crl"].split("<ROW>")
            for i in tab:
                (nom, numci, titulaire, id_role, role, idpers, president) = i.split("<FIELD>")
                print idpers
                key = str(id_role)
                key_idpers = str(id_role)
                if titulaire == 'true':
                    key = key+'_t'
                if titulaire == 'false':
                    key = key+'_f'
                if president == 'true':
                    self.idPresidentCrl = int(idpers)
                cin_nom = nom + ':' + numci
                self.membre_crl.append({key: cin_nom})
                self.ids_crl.append({key_idpers:idpers})
        print self.membre_crl

    @staticmethod
    def select_by_id(connection,id):
        data=[]
        SQL = "SELECT d.iddemande,d.numdemande, d.datedemande, d.datereconnaissance, " \
              "pd.gid, ST_Area(pd.geom),d.idfokontany, d.consistance, f.nomfokontany , " \
              "d.categorie, ST_AsText(pd.geom), d.datedecision, d.numdecision,pd.codeparcelle FROM parcelle_d pd, demande d, fokontany f WHERE d.gid = pd.gid AND d.idfokontany  = f.idfokontany AND d.iddemande = %s;"
        param = (id,)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute(SQL, param)
            data = cursor.fetchone()
            print data
        except StandardError as e:
            print e+' erreur selection demande'
        return data