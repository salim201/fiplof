# -*- coding: utf-8 -*-
import io
import sys
import os
import os.path
import csv
import psycopg2
from datetime import datetime
import time

dBName = "plof"
csv_idCommune = "G2"
pathToDir = "D:\CommuneOPROD\Commune-AMBATOMANGA"
i = 0


if dBName == "" and csv_idCommune == "":
    print ("Vous avez obliez de mentionner le nom de la base de données et/ou l'id de la commune dans le CSV")
    time.sleep(10)
else:

    connection = psycopg2.connect(database=dBName, user='postgres', password ='postgres', host='localhost')
    cursor = connection.cursor()


    def convertDate(date_time):
        if date_time is not None:
            format = '%Y-%m-%d'

            try:
                datetime_str = datetime.strptime(date_time, format)
                return datetime_str
            except Exception as e:
                print (e)
                return None

        else:
            return None

    def saveErrorLine(line, writer):
        writer.writerow(line)

    print ("DEBUT IMPORT PERSONNES PHYSIQUES")
    filePath = os.path.join(pathToDir, "persphys.csv")

    ##IMPORTER LES PERSONNES PHYSIQUES
    # f = io.open('C:\Users\Salim\Documents\CSVImport\persphys-error.csv', encoding='utf8').read()
    # fi = open('C:\Users\Salim\Documents\CSVImport\persphys-error.csv', 'r+', encoding='utf-8')
    with io.open(filePath, 'rt', encoding="utf-8") as f:

        fieldNames = ['id_persphys', 'nom', 'prenom', 'sexe', 'naissance_date', 'naissance_lieu', 'cni_num', 'cni_date',
                      'cni_lieu', 'acn_num', 'acn_date', 'acn_lieu', 'adresse', 'type_pi', 'nom_pere', 'nom_mere',
                      'd_naiss_approx', 'exist_tuteur', 'cin_ok']
        obj = csv.DictReader(f, fieldNames)
        filePath = os.path.join(pathToDir, "persphys-error-log.csv")
        fichiercsv = open(filePath, 'a')
        writer = csv.writer(fichiercsv)

        i = 0

        for ligne in obj:
            ligneToLog = [ligne['id_persphys'], ligne['nom'], ligne['prenom'], ligne['sexe'], ligne['naissance_date'],
                          ligne['naissance_lieu'], ligne['cni_num'], ligne['cni_date'], ligne['cni_lieu'], ligne['acn_num'],
                          ligne['acn_date'], ligne['acn_lieu'], ligne['adresse'], ligne['type_pi'], ligne['nom_pere'],
                          ligne['nom_mere'], ligne['d_naiss_approx'], ligne['exist_tuteur'], ligne['cin_ok']]
            # ligneToLog = ligne.values()
            nevers = 0

            if ligne['d_naiss_approx'] == 'True':
                annee_naissance = ligne['naissance_date'].split('-')
                nevers = annee_naissance[0]

            sit_matri = 1

            prenom = ""
            nom_pere = ""
            nom_mere = ""
            cni_lieu = ""
            adresse = ""
            naissance_lieu =""
            acn_lieu = ""

            #print "Nom personne"
            if ligne['prenom'] is not None:
                prenom = ligne['prenom']
            if ligne['nom_pere'] is not None:
                nom_pere = ligne['nom_pere']
            if ligne['nom_mere'] is not None:
                nom_mere = ligne['nom_mere']
            if ligne['cni_lieu'] is not None:
                cni_lieu = ligne['cni_lieu']
            if ligne['adresse'] is not None:
                adresse = ligne['adresse']
            if ligne['naissance_lieu'] is not None:
                naissance_lieu = ligne['naissance_lieu']
            if ligne['acn_lieu'] is not None:
                acn_lieu = ligne['acn_lieu']
                # print nom

            if ligne['sexe'] == 'H':
                ligne['sexe'] = 'masculin'
            else:
                ligne['sexe'] = 'feminin'

            date_naiss = convertDate(ligne['naissance_date'])
            date_ci = convertDate(ligne['cni_date'])
            date_acn = convertDate(ligne['acn_date'])

            try:
                if date_ci is not None and ligne['type_pi'] == 'cni':
                    cursor.execute(
                        "INSERT INTO personne(nompersonne, prenompersonne,datenaissancepersonne,sexepersonne,nevers,lieunaissancepersonne,numcipersonne, datecipersonne, lieucipersonne," \
                        " adressepersonne,situationmatrimoniale, nompere, nommere,csv_id) " \
                        "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                            ligne['nom'], prenom, date_naiss,
                            ligne['sexe'], nevers,
                            naissance_lieu,
                            ligne['cni_num'], date_ci,
                            cni_lieu,
                            adresse, sit_matri,
                            nom_pere,
                            nom_mere, ligne['id_persphys']))
                    connection.commit()

                elif date_ci is None and ligne['type_pi'] == 'cni':
                    cursor.execute(
                        "INSERT INTO personne(nompersonne, prenompersonne,datenaissancepersonne,sexepersonne,nevers,lieunaissancepersonne,numcipersonne, lieucipersonne," \
                        " adressepersonne,situationmatrimoniale, nompere, nommere,csv_id) " \
                        "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                            ligne['nom'], prenom, date_naiss,
                            ligne['sexe'], nevers,
                            naissance_lieu,
                            ligne['cni_num'],
                            cni_lieu,
                            adresse, sit_matri,
                            nom_pere,
                            nom_mere, ligne['id_persphys']))
                    connection.commit()

                elif date_acn is not None and ligne['type_pi'] == 'acte':
                    cursor.execute(
                        "INSERT INTO personne(nompersonne, prenompersonne,datenaissancepersonne,sexepersonne,nevers,lieunaissancepersonne,numactenaissancepersonne, dateactenaissancepersonne," \
                        " lieuactenaissancepersonne, adressepersonne,situationmatrimoniale, nompere, nommere,csv_id) " \
                        "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                            ligne['nom'], prenom, date_naiss,
                            ligne['sexe'], nevers,
                            naissance_lieu,
                            ligne['acn_num'], date_acn,
                            acn_lieu,
                            adresse, sit_matri,
                            nom_pere,
                            nom_mere, ligne['id_persphys']))
                    connection.commit()
                print (ligne)

            except Exception as e:
                saveErrorLine(ligneToLog, writer)
                #print ligneToLog
                #print "Personne csv_id:"
                #print ligne['id_persphys']
                print(e)
                connection.rollback()

        fichiercsv.close()
    print ("FIN IMPORT PERSONNE PHYSIQUE")
    # fin import personne physique
    #**************************************************************************************************************
    #IMPORT ENTITES ADMINISTRATIVES********************************************************************
    # import region
    print ("DEBUT IMPORT REGION")
    filePath = os.path.join(pathToDir, "region.csv")
    with open(filePath, 'rt', encoding="utf-8") as f:
        # creer un objet csv Ã  partir du fichier
        obj = csv.DictReader(f)
        filePath = os.path.join(pathToDir, "region-error-log.csv")
        fichiercsv = open(filePath, 'a')
        writer = csv.writer(fichiercsv)

        for ligne in obj:
            #print ligne
            ligneToLog = ligne.values()
            ligneToLogList = list(ligneToLog)

            try:
                cursor.execute(
                        "INSERT INTO region(coderegion, nomregion,csv_id)" \
                        " VALUES(%s,%s,%s)", (
                            ligne['code_region'], ligne['nom'],
                            ligne['id_region']))
                connection.commit()
                print (ligne)

            except Exception as e:
                saveErrorLine(ligneToLogList, writer)
                #print "Region csv_id"
                #print ligne['id_region']
                print (e)
                connection.rollback()

        fichiercsv.close()
    print ("FIN IMPORT REGION")
    # fin import region
    #*************************************************************************************************************

    print ("DEBUT IMPORT DISTRICT")
    filePath = os.path.join(pathToDir, "district.csv")
    #Import district
    def getIdRegion(csv_id):
        cur = connection.cursor()
        try:
            cur.execute("SELECT DISTINCT idregion FROM region WHERE csv_id = %s", (str(csv_id),))
            data = cur.fetchone()
            return data[0]
        except Exception as e:
            print (e)


    with open(filePath, 'rt', encoding="utf-8") as f:
        # creer un objet csv Ã  partir du fichier
        obj = csv.DictReader(f)
        filePath = os.path.join(pathToDir, "district-error-log.csv")
        fichiercsv = open(filePath, 'a')
        writer = csv.writer(fichiercsv)

        for ligne in obj:
            #print ligne
            ligneToLog = ligne.values()
            ligneToLogList = list(ligneToLog)

            idRegion = getIdRegion(ligne['id_region'])

            try:
                cursor.execute(
                        "INSERT INTO district(codedistrict, nomdistrict,csv_id, idregion) " \
                        " VALUES(%s,%s,%s, %s)", (
                            ligne['code_district'], ligne['nom'],
                            ligne['id_district'], str(idRegion)))
                connection.commit()
                print(ligne)

            except Exception as e:
                saveErrorLine(ligneToLogList, writer)
                #print "District csv_id"
                #print ligne['id_district']
                print (e)
                connection.rollback()

        fichiercsv.close()
    print ("FIN IMPORT DISTRICT")
    # fin import district
    #**********************************************************************
    print ("DEBUT IMPORT COMMUNE")
    filePath = os.path.join(pathToDir, "commune.csv")
    #Import Commune
    def getIdDistrict(csv_id):
        cur = connection.cursor()
        try:
            cur.execute("SELECT DISTINCT iddistrict FROM district WHERE csv_id = %s", (str(csv_id),))
            data = cur.fetchone()
            return data[0]
        except Exception as e:
            print (e)
            connection.rollback()

    with open(filePath, 'rt', encoding="utf-8") as f:
        # creer un objet csv Ã  partir du fichier
        obj = csv.DictReader(f)
        filePath = os.path.join(pathToDir, "commune-error-log.csv")
        fichiercsv = open(filePath, 'a')
        writer = csv.writer(fichiercsv)

        for ligne in obj:
            #print ligne
            ligneToLog = ligne.values()
            ligneToLogList = list(ligneToLog)

            idDistrict = getIdDistrict(ligne['id_district'])

            try:
                cursor.execute(
                        "INSERT INTO commune(codecommune, nomcommune,csv_id,iddistrict) " \
                        " VALUES(%s,%s,%s, %s)", (
                            ligne['code_commune'], ligne['nom'],
                            ligne['id_commune'], str(idDistrict)))
                connection.commit()
                print(ligne)

            except Exception as e:
                saveErrorLine(ligneToLogList, writer)
                #print "Commune csv_id"
                #print ligne['id_commune']
                print (e)
                connection.rollback()

        fichiercsv.close()
    print ("FIN IMPORT COMMUNE")
    #fin import commune
    #*****************************************************************************
    #Import fokontany
    print ("DEBUT IMPORT FOKONTANY")
    filePath = os.path.join(pathToDir, "fokontany.csv")
    def getIdCommune(csv_id):
        cur = connection.cursor()
        try:
            cur.execute("SELECT DISTINCT idcommune FROM commune WHERE csv_id = %s", (str(csv_id),))
            data = cur.fetchone()
            return data[0]
        except Exception as e:
            print (e)
            connection.rollback()

    with open(filePath, 'rt', encoding="utf-8") as f:
        # creer un objet csv Ã  partir du fichier
        obj = csv.DictReader(f)
        filePath = os.path.join(pathToDir, "fokontany-error-log.csv")
        fichiercsv = open(filePath, 'a')
        writer = csv.writer(fichiercsv)

        for ligne in obj:
            #print ligne
            ligneToLog = ligne.values()
            ligneToLogList = list(ligneToLog)

            idCommune = getIdCommune(ligne['id_commune'])

            try:
                cursor.execute(
                        "INSERT INTO fokontany(codefokontany, nomfokontany,csv_id,idcommune) " \
                        " VALUES(%s,%s,%s, %s)", (
                            ligne['code_fokontany'], ligne['nom'],
                            ligne['id_fokontany'], str(idCommune)))
                connection.commit()
                print(ligne)

            except Exception as e:
                saveErrorLine(ligneToLogList, writer)
                #print "Fokontany csv_id"
                #print ligne['id_fokontany']
                print (e)

        fichiercsv.close()
    print ("FIN IMPORT FOKONTANY")
    # fin import fokontany
    #*************************************************************
    #Import hameau
    print ("DEBUT IMPORT HAMEAU")
    filePath = os.path.join(pathToDir, "hameau.csv")
    def getIdFokontany(csv_id):
        cur = connection.cursor()
        try:
            cur.execute("SELECT DISTINCT idfokontany FROM fokontany WHERE csv_id = %s", (str(csv_id),))
            data = cur.fetchone()
            return data[0]
        except Exception as e:
            print (e)
            connection.rollback()

    with open(filePath, 'rt', encoding="utf-8") as f:
        # creer un objet csv Ã  partir du fichier
        obj = csv.DictReader(f)
        filePath = os.path.join(pathToDir, "hameau-error-log.csv")
        fichiercsv = open(filePath, 'a')
        writer = csv.writer(fichiercsv)

        for ligne in obj:
            #print ligne
            ligneToLog = ligne.values()
            ligneToLogList = list(ligneToLog)

            idFokontany = getIdFokontany(ligne['id_fokontany'])

            try:
                cursor.execute(
                        "INSERT INTO hameau(codehameau, nomhameau,csv_id,idfokontany) " \
                        " VALUES(%s,%s,%s, %s)", (
                            ligne['code_hameau'],ligne['nom'],
                            ligne['id_hameau'], str(idFokontany)))
                connection.commit()
                print(ligne)

            except Exception as e:
                saveErrorLine(ligneToLogList, writer)
                print ("Hameau csv_id")
                print (ligne['id_hameau'])
                print (e)

        fichiercsv.close()
    print ("FIN IMPORT HAMEAU")
    #FIN IMPORT ENTITES ADMINISTRATIVES

    #**************************************************************************************************************
    # IMPORT TYPE PERSONNE MORALE
    print ("DEBUT IMPORT PERSONNE MORALE")
    filePath = os.path.join(pathToDir, "lst_type_pm.csv")
    with open(filePath, 'rt', encoding="utf-8") as f:
        # creer un objet csv Ã  partir du fichier
        obj = csv.DictReader(f)
        filePath = os.path.join(pathToDir, "lst_type_pm-error-log.csv")
        fichiercsv = open(filePath, 'a')
        writer = csv.writer(fichiercsv)

        for ligne in obj:

            ligneToLog = [ligne['id_lst_type_pm'], ligne['valeur']]
            #ligneToLogList = list(ligneToLog)

            #idFokontany = getIdFokontany(ligne['id_fokontany'])

            try:
                cursor.execute(
                        "INSERT INTO typepersonnemorale(type, karazana,csv_id) " \
                        " VALUES(%s,%s,%s)", (
                            ligne['valeur'], ligne['valeur'],
                            ligne['id_lst_type_pm']))
                connection.commit()
                print(ligne)

            except Exception as e:
                saveErrorLine(ligneToLog, writer)
                #print "Liste PM csv_id"
                print (ligne['id_lst_type_pm'])
                print (e)

        fichiercsv.close()
    print ("FIN IMPORT PERSONNE MORALE")
    # fin import personne morale
    #************************************************************************************************************
    print ("IMPORT PERSONNE MORALE")
    filePath = os.path.join(pathToDir, "persmor.csv")
    def getIdTypePers(csv_id):
        cur = connection.cursor()
        try:
            cur.execute("SELECT DISTINCT idtype FROM typepersonnemorale WHERE csv_id = %s", (str(csv_id),))
            data = cur.fetchone()
            return data[0]
        except Exception as e:
            print (e)

    # IMPORT PERSONNE MORALE
    with open(filePath, 'rt', encoding="utf-8") as f:
        # creer un objet csv Ã  partir du fichier
        obj = csv.DictReader(f)

        filePath = os.path.join(pathToDir, "persmor-error-log.csv")
        fichiercsv = open(filePath, 'a')
        writer = csv.writer(fichiercsv)


        for ligne in obj:
            #print ligne
            ligneToLog = [ligne['id_persmor'],ligne['id_type_persmor'],ligne['denomination'],ligne['numero_pm'],ligne['date_acte'],ligne['adresse']]
            idTypePers = getIdTypePers(ligne['id_type_persmor'])
            #ligneToLogList = list(ligneToLog)
            date_acte = convertDate(ligne['date_acte'])

            #idFokontany = getIdFokontany(ligne['id_fokontany'])

            try:
                cursor.execute(
                        "INSERT INTO personnemorale(numeroproprietaire, denomination,datecreation,siege, idtype, csv_id) " \
                        " VALUES(%s,%s,%s,%s,%s,%s)", (
                            ligne['numero_pm'], ligne['denomination'], date_acte,ligne['adresse'],
                            str(idTypePers), ligne['id_persmor']))
                connection.commit()
                print(ligne)

            except Exception as e:
                saveErrorLine(ligneToLog, writer)
                #print "Liste PM csv_id"
                #print ligne['id_persmor']
                print (e)
                connection.rollback()

        fichiercsv.close()
    print ("FIN IMPORT PERSONNE MORALE")
    # FIN IMPORT PERSONNE MORALE
    #*****************************************IMPORT PARCELLE **********************************

    print ("DEBUT IMPORT PARCELLE")
    filePath = os.path.join(pathToDir, "parcelle_cf.csv")
    def getIdHameau(code_hameau, code_fkt, code_commune, code_district):
        cur = connection.cursor()
        try:
            cur.execute("SELECT h.idhameau, c.idcommune, c.csv_id FROM hameau h INNER JOIN fokontany f ON h.idfokontany = f.idfokontany "\
    "INNER JOIN commune c ON f.idcommune = c.idcommune INNER JOIN district d ON d.iddistrict = c.iddistrict "\
    "WHERE h.codehameau = %s AND f.codefokontany = %s AND c.codecommune = %s AND d.codedistrict = %s", (str(code_hameau),str(code_fkt),str(code_commune),str(code_district)))
            data = cur.fetchone()
            return data
        except Exception as e:
            print (e)
            connection.rollback()

    with open(filePath, 'rt', encoding="utf-8") as f:
        # creer un objet csv Ã  partir du fichier
        obj = csv.DictReader(f)

        filePath = os.path.join(pathToDir, "parcelle_cf-error-log.csv")
        fichiercsv = open(filePath, 'a')
        writer = csv.writer(fichiercsv)

        i = 0
        for ligne in obj:

            ligneToLog = [ligne['id_parcelle_cf'],ligne['c_district'],ligne['c_commune'],ligne['c_fokontany'],ligne['c_hameau'],ligne['num_parcelle'],ligne['c_parcelle'],ligne['anomalie'],ligne['limitrophe'],ligne['observation'],ligne['id_lot'],ligne['date_num'],ligne['utilisateur'],ligne['superficie'],ligne['coord_x'],ligne['coord_y'],ligne['geom'],ligne['cq0'],ligne['cq1'],ligne['cq2'],ligne['cqe'],ligne['type_op'],ligne['ocfm']]#,ligne['cod_parc_en_doublon'],ligne['editer_en_cf'],ligne['matching_saisie'],ligne['est_soumis_cqe'],ligne['soumis_cqe'],ligne['ftm_2009'],ligne['ftm_2021'],ligne['ctrl_com'],ligne['pass_cq2'],ligne['date_cq2'],ligne['pers_cq2'],ligne['analyse_com'],ligne['reponse_cqe']]
            datares = getIdHameau(ligne['c_hameau'], ligne['c_fokontany'],ligne['c_commune'],ligne['c_district'])
            idHameau = None
            idCommune = None
            consistance = 'Consistance'
            csv_idComDb = ""
            if datares is not None:
                idHameau = datares[0]
                idCommune = datares[1]
                csv_idComDb = datares[2]
            if csv_idCommune == csv_idComDb:
                if idCommune is not None:
                    try:
                        cursor.execute(
                            "INSERT INTO parcelle_d(geom, district, commune, fkt, consistance, id_commune, idhameau, csv_id, numero, codeparcelle, anomalie, limitrophe, observation, code_parcelle_en_doublon,editer_en_cf ) " \
                            " VALUES(ST_Transform(ST_GeometryN(%s, 1), "+str(globalvars.EPSG_SCR)+"),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                                ligne['geom'], ligne['c_district'],
                                ligne['c_commune'],
                                ligne['c_fokontany'], consistance, idCommune, idHameau,
                                ligne['id_parcelle_cf'], ligne['num_parcelle'], ligne['c_parcelle'],ligne['anomalie'],ligne['limitrophe'], ligne['observation'], ligne['cod_parc_en_doublon'], ligne['editer_en_cf']))
                        connection.commit()
                        print(ligne)

                    except Exception as e:
                        saveErrorLine(ligneToLog, writer)
                        #print "Liste parcelle_cf"
                        #print ligne['id_parcelle_cf']
                        print (e)
                        connection.rollback()

            #        i = i + 1
            #        if i > 1000:
            #            break

        fichiercsv.close()
    print("FIN IMPORT PARCELLE")
    # FIN IMPORT PARCELLE
    #***********************************************************************
    # Debut import demande
    print("DEBUT IMPORT DEMANDE")

    filePath = os.path.join(pathToDir, "demande.csv")
    def insertVoisins(idpointcard, idparcelle, desc):
        cur = connection.cursor()
        try:
            cur.execute(
                "INSERT INTO limitesparcelle(idpointscardinaux, idparcelle, description) VALUES(%s, %s,%s)",
                (str(idpointcard), str(idparcelle), str(desc)))
            connection.commit()
        except Exception as e:
            print(e)
            connection.rollback()


    def getGid(code_parcelle):
        cur = connection.cursor()
        try:
            cur.execute(
                "SELECT p.gid FROM parcelle_d p WHERE  p.codeparcelle = %s",
                (str(code_parcelle),))
            data = cur.fetchone()
            return data
        except Exception as e:
            print(e)
            connection.rollback()


    def getIdHameau2(csv_id_hameau):
        cur = connection.cursor()
        try:
            cur.execute("SELECT DISTINCT  r.nomregion, d.nomdistrict, f.idfokontany, c.idcommune  " \
                        "FROM hameau h INNER JOIN fokontany f ON f.idfokontany = h.idfokontany " \
                        "INNER JOIN commune c ON f.idcommune = c.idcommune " \
                        "INNER JOIN district d ON d.iddistrict = c.iddistrict " \
                        "INNER JOIN region r ON d.idregion = r.idregion " \
                        "WHERE h.csv_id = %s ", (str(csv_id_hameau),))
            data = cur.fetchone()
            return data
        except Exception as e:
            print(e)
            connection.rollback()


    def getIdPersonneFromDemande(id_parcelle):
        cur = connection.cursor()
        try:
            cur.execute(
                "SELECT DISTINCT idpersonne FROM avoir_demande  WHERE  idparcelle = %s",
                (str(id_parcelle),))
            data = cur.fetchall()
            return data
        except Exception as e:
            print(e)
            connection.rollback()


    def insertProprietaire(idpersonnes, idparcelle):
        cur = connection.cursor()
        i = 0
        representant = True
        for idpersonne in idpersonnes:
            try:
                if i > 0:
                    representant = False
                cur.execute(
                    "INSERT INTO proprietaireparcelle (idparcelle, idpersonne, representant) VALUES (%s, %s, %s)",
                    (str(idparcelle), str(idpersonne[0]), representant))
                connection.commit()
            except Exception as e:
                print(e)
                connection.rollback()

            i = i + 1


    with io.open(filePath, 'rt', encoding="utf-8") as f:
        # creer un objet csv Ã  partir du fichier
        obj = csv.DictReader(f)
        obj2 = csv.reader(f)
        print(obj)
        filePath = os.path.join(pathToDir, "demande-error-log.csv")
        fichiercsv = open(filePath, 'a')
        writer = csv.writer(fichiercsv)

        i = 0
        total = 0

        for ligne in obj:
            ligneToLog = [ligne['id_demande'], ligne['id_fiplof'], ligne['id_hameau'], ligne['num_parcelle'],
                              ligne['id_parcelle'], ligne['num_registre'],
                              ligne['id_registre'], ligne['date_demande'], ligne['lieu_dit'], ligne['code_equipe'],
                              ligne['planche_plof'], ligne['type_demandeur'],
                              ]

            datares = getGid(ligne['id_parcelle'])
            Gid = None
                # idCommune = None

            consistance = ligne['consistance']
            if datares is not None:
                Gid = datares[0]

            id_hameau = None
            nomregion = ""
            nomdistrict = ""
            id_fokontany = None
            id_commune = None
            id_projet = 1
            dataParc = getIdHameau2(ligne['id_hameau'])
            if dataParc is not None:
                nomregion = dataParc[0]
                nomdistrict = dataParc[1]
                id_fokontany = dataParc[2]
                id_commune = dataParc[3]
                # id_projet = dataParc[4]

            date_demande = convertDate(ligne['date_demande'])
            date_crl = convertDate(ligne['date_crl'])
            date_decision = convertDate(ligne['date_demande'])

                #Categorie
            categorie = ""
            if ligne['cat_riz']:
                categorie = "Tanimbary"
            elif ligne['cat_champ']:
                categorie = "Tanimboly"
            elif ligne['cat_etang']:
                categorie = "Dobo"
            elif ligne['cat_etable']:
                categorie = "Tany lava volo"
            elif ligne['cat_bois']:
                categorie = "Ala"
            else:
                categorie = "Hafa"

                # ligneToLogList = list(ligneToLog)
                # date_acte = convertDate(ligne['date_acte'])
                # print "Region " + nomregion + " District " + nomdistrict + " Fokontany " + str(id_fokontany)  + " Commune " +  str(id_commune) + " Projet " + str(id_projet)
                # idFokontany = getIdFokontany(ligne['id_fokontany'])
            if Gid is not None:
                    # resaka voisins
                if str(ligne['v_nord']) is not None:
                    insertVoisins(4, Gid, str(ligne['v_nord']))
                if str(ligne['v_sud']) is not None:
                    insertVoisins(5, Gid, str(ligne['v_sud']))
                if str(ligne['v_est']) is not None:
                    insertVoisins(6, Gid, str(ligne['v_est']))
                if str(ligne['v_ouest']) is not None:
                    insertVoisins(11, Gid, str(ligne['v_ouest']))

                #INSERTION DES DEMANDES
                try:
                    cursor.execute(
                            "INSERT INTO demande(numdemande, gid, datedemande, datereconnaissance, region, district, idfokontany, idcommune, cout, idprojet, datedecision, code_parcelle, csv_id, categorie, consistance,opposition,planche_plof,charges) " \
                            " VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)", (
                                str(ligne['id_registre']), str(Gid), date_demande, date_crl, nomregion,
                                str(nomdistrict), str(id_fokontany), str(id_commune), str(2000),
                                str(id_projet), date_decision, str(ligne['id_parcelle']),
                                str(ligne['id_demande']), categorie, consistance,ligne['opposition'], ligne['planche_plof'], ligne['charges']))
                    connection.commit()
                    print(ligne)

                except Exception as e:
                    saveErrorLine(ligneToLog, writer)
                    # print "Liste parcelle_cf"
                    print(ligne['id_demande'])
                    print(e)
                    connection.rollback()
                #INSERTION NUMDEMANDE DANS PARCELLE
                try:
                    cursor.execute(
                            "UPDATE parcelle_d SET numdemande = %s " \
                            " WHERE gid = %s", (
                                str(ligne['id_registre']), str(Gid)))
                    connection.commit()

                except Exception as e:
                    print(e)
                    connection.rollback()
                    #INSERTION CERTIFICAT
                numCF = ""
                id_certficatBd = None
                try:
                    numCF = ligne['id_certificat']
                except Exception as err:
                    pass
                if numCF != "":
                    try:
                        cursor.execute(
                                "INSERT INTO certificat(numerocertificat, numerodemande, datereconnaissance, idfokontany, idprojet, isprint,idcommune) " \
                                " VALUES(%s,%s,%s,%s,%s,%s,%s) returning idcertificat", (
                                    numCF, ligne['id_registre'], date_crl, str(id_fokontany),str(id_projet) ,str(0), str(id_commune)))
                        connection.commit()
                        res = cursor.fetchone()
                        id_certficatBd = res[0]
                        print("INSERTION CERTIFICAT")
                        print(ligne)

                    except Exception as e:
                        saveErrorLine(ligneToLog, writer)
                        # print "Liste parcelle_cf"
                        print(ligne['id_demande'])
                        print(e)
                        connection.rollback()

                    # INSERTION idcertificat DANS PARCELLE
                    if id_certficatBd is not None:
                        try:
                            cursor.execute(
                                    "UPDATE parcelle_d SET idcertificat = %s " \
                                        " WHERE gid = %s", (
                                            str(id_certficatBd), str(Gid)))
                            connection.commit()
                            idpersonness = getIdPersonneFromDemande(Gid)
                            insertProprietaire(idpersonness, Gid)
                        except Exception as e:
                            print(e)
                            connection.rollback()


            else:
                print("Gid is None")
                saveErrorLine(ligneToLog, writer)
                try:
                    cursor.execute(
                            "INSERT INTO demande_sans_geom(numdemande, datedemande, datereconnaissance, region, district, idfokontany, idcommune, cout, idprojet, datedecision, code_parcelle, csv_id, categorie, consistance,opposition,planche_plof,charges) " \
                            " VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s,%s, %s)", (
                                str(ligne['id_registre']), date_demande, date_crl,
                                str(nomregion),
                                str(nomdistrict), str(id_fokontany), str(id_commune),
                                str(2000),
                                str(id_projet), date_decision, str(ligne['id_parcelle']),
                                str(ligne['id_demande']), categorie, consistance,ligne['opposition'], ligne['planche_plof'], ligne['charges']))
                    connection.commit()
                    print("Insertion dans la table demande_sans_geom")
                except Exception as e:
                        # saveErrorLine(ligneToLog, writer)
                        # print "Liste parcelle_cf"
                    print(ligne['id_demande'])
                    print(e)
                    connection.rollback()
            #        i = i + 1
            #        if  i > 1000:
            #            break;

        fichiercsv.close()

    print("FIN DEMANDE")

    # *****************************fin import demande*************************************************************************************

    # Import proprietaire physique**********************************************************************************************************
    print("Debut import proprietaire physique")

    filePath = os.path.join(pathToDir, "proprietaire_pp.csv")
    def getIdDemande(id_demande_csv):
        cur = connection.cursor()
        try:
            cur.execute(
                "SELECT DISTINCT iddemande, gid FROM demande  WHERE  csv_id = %s",
                (str(id_demande_csv),))
            data = cur.fetchone()
            return data
        except Exception as e:
            print (e)
            connection.rollback()

    def getIdPersonne(id_personne_csv):
        cur = connection.cursor()
        try:
            cur.execute(
                "SELECT DISTINCT idpersonne FROM personne  WHERE  csv_id = %s",
                (str(id_personne_csv),))
            data = cur.fetchone()
            return data
        except Exception as e:
            print(e)
            connection.rollback()

    with io.open(filePath, 'rt', encoding="utf-8") as f:
        # creer un objet csv Ã  partir du fichier
        obj = csv.DictReader(f)
        filePath = os.path.join(pathToDir, "proprietaire_pp-error-log.csv")
        fichiercsv = open(filePath, 'a')
        writer = csv.writer(fichiercsv)

        i = 0
        for ligne in obj:

            ligneToLog = [ligne['id_proprietaire_pp'],ligne['id_demande'],ligne['id_persphys'],ligne['type_demandeur']]

            datademande = getIdDemande(ligne['id_demande'])
            datapers = getIdPersonne(ligne['id_persphys'])

            idparcelle = None
            iddemande = None
            idpersonne = None
            consistance = 'Consistance'
            if datademande is not None:
                iddemande = datademande[0]
                idparcelle = datademande[1]

            if datapers is not None:
                idpersonne = datapers[0]


            if iddemande is not None and idpersonne is not None:
                try:
                    cursor.execute(
                            "INSERT INTO avoir_demande(idpersonne, idparcelle, iddemande, csv_id) " \
                            " VALUES(%s,%s,%s,%s)", (
                                str(idpersonne),str(idparcelle),str(iddemande), ligne['id_proprietaire_pp']))
                    connection.commit()
                    print(ligne)

                except Exception as e:
                    saveErrorLine(ligneToLog, writer)
                    print (e)
                    connection.rollback()

    #        i = i + 1
    #        if i > 1000:
    #            break

        fichiercsv.close()
        print ("Fin import proprietaire physique")
    # *****************************fin import proprietaire physique*************************************************************************************
    #****************************Import proprietaire morale**********************************************************************************
#
#    # Import proprietaire physique**********************************************************************************************************
#    print ("Debut import proprietaire morale")
#
#    filePath = os.path.join(pathToDir, "proprietaire_pm.csv")
#    def getIdDemandeMor(id_demande_csv):
#        cur = connection.cursor()
#        try:
#            cur.execute(
#                "SELECT DISTINCT iddemande, gid FROM demande  WHERE  csv_id = %s",
#                (str(id_demande_csv),))
#            data = cur.fetchone()
#            return data
#        except Exception as e:
#            print(e)
#            connection.rollback()
#
#    def getIdPersonneMor(id_personnemorale_csv):
#        cur = connection.cursor()
#        try:
#            cur.execute(
#                "SELECT DISTINCT idpersonnemorale FROM personnemorale  WHERE  csv_id = %s",
#                (str(id_personnemorale_csv),))
#            data = cur.fetchone()
#            return data
#        except Exception as e:
#            print(e)
#            connection.rollback()
#
#    with io.open(filePath, 'rt', encoding="utf-8") as f:
#        # creer un objet csv Ã  partir du fichier
#        obj = csv.DictReader(f)
#        filePath = os.path.join(pathToDir, "proprietaire_pm-error-log.csv")
#        fichiercsv = open(filePath, 'a')
#        writer = csv.writer(fichiercsv)
#
#        i = 0
#        for ligne in obj:
#
#            ligneToLog = [ligne['id_proprietaire_pm'],ligne['id_demande'],ligne['id_persmor']]
#
#            datademande = getIdDemandeMor(ligne['id_demande'])
#            datapersMor = getIdPersonneMor(ligne['id_persmor'])
#
#            idparcelle = None
#            iddemande = None
#            idpersonneMorale = None
#            consistance = 'Consistance'
#            if datademande is not None:
#                iddemande = datademande[0]
#                idparcelle = datademande[1]
#
#            if datapers is not None:
#                idpersonneMorale = datapersMor[0]
#
#            if iddemande is not None and idpersonne is not None:
#                try:
#                    cursor.execute(
#                            "INSERT INTO personnemoraleparcelle(idpersonnemorale, idparcelle, iddemande, csv_id) " \
#                            " VALUES(%s,%s,%s,%s)", (
#                                str(idpersonneMorale),str(idparcelle),str(iddemande), ligne['id_persmor']))
#                    connection.commit()
#                    print(ligne)
#
#                except Exception as e:
#                    saveErrorLine(ligneToLog, writer)
#                    print (e)
#                    connection.rollback()
#
#    #        i = i + 1
#    #        if i > 1000:
#    #            break
#
#        fichiercsv.close()
#        print("Fin import proprietaire morale")
#    #*****************************************************************************************************
#    print("Import type anomalie")
#    filePath = os.path.join(pathToDir, "lst_type_anomalie.csv")
#    with io.open(filePath, 'rt', encoding="utf-8") as f:
#        # creer un objet csv Ã  partir du fichier
#        obj = csv.DictReader(f)
#        filePath = os.path.join(pathToDir, "lst_type_anomalie-error-log.csv")
#        fichiercsv = open(filePath, 'a')
#        writer = csv.writer(fichiercsv)
#
#        i = 0
#        for ligne in obj:
#
#            ligneToLog = [ligne['id_lst_type_anomalie'],ligne['valeur']]
#
#            try:
#                cursor.execute(
#                            "INSERT INTO type_anomalie(valeur, csv_id) " \
#                            " VALUES(%s,%s)", (
#                                str(ligne['valeur']),str(ligne['id_lst_type_anomalie'])))
#                connection.commit()
#                print(ligne)
#
#            except Exception as e:
#                saveErrorLine(ligneToLog, writer)
#                print(e)
#                connection.rollback()
#
#    #        i = i + 1
#    #        if i > 1000:
#    #            break
#
#        fichiercsv.close()
#        print("Fin import Type anomalie")
###**************************************************************************************
#    print("Import anomalie")
#    filePath = os.path.join(pathToDir, "anomalie.csv")
#    with io.open(filePath, 'rt', encoding="utf-8") as f:
#        # creer un objet csv Ã  partir du fichier
#        obj = csv.DictReader(f)
#        filePath = os.path.join(pathToDir, "anomalie-error-log.csv")
#        fichiercsv = open(filePath, 'a')
#        writer = csv.writer(fichiercsv)
#
#        i = 0
#        for ligne in obj:
#
#            ligneToLog = [ligne['id_anomalie'],ligne['id_lst_type_anomalie'],ligne['description'],ligne['resolu'],ligne['id_utilisateur'],ligne['id_demande'],ligne['date_anomalie']]
#
#            try:
#                cursor.execute(
#                    "INSERT INTO anomalie(description, resolu, csv_iddemande, csv_id, csv_id_type_anomalie) " \
#                    " VALUES(%s,%s,%s,%s,%s)", (
#                        str(ligne['description']), str(ligne['resolu']),str(ligne['id_demande']),str(ligne['id_anomalie']) , str(ligne['id_lst_type_anomalie'])))
#                connection.commit()
#                print(ligne)
#
#            except Exception as e:
#                saveErrorLine(ligneToLog, writer)
#                print(e)
#                connection.rollback()
#
#        #        i = i + 1
#        #        if i > 1000:
#        #            break
#
#        fichiercsv.close()
#        print("Fin import anomalie")
#