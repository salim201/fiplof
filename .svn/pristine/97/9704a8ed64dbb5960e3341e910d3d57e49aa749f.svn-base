# -*- coding: utf-8 -*-

from Etats.codegenerator.ICodeImageGenerator import ICodeImageGenerator
from PyQt4 import QtGui, QtCore
from .Pdf import PlofPdf
import sys
import os
import psycopg2
import psycopg2.extras
import globalvars
import datetime
from datetime import datetime
from Utils import Utils

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class PrintCertificatFoncier:
    __codeImageGenerator = None # type: ICodeImageGenerator | None

    def __init__(self, connection, idcertificat):
        self.connection, self.idcertificat = connection, idcertificat
        self.row, self.pdf = None, None
        self.area = 0
        self.X = 0
        self.Y = 0
        self.nompersonne = self.prenompersonne = self.cin = self.lieucin = self.datecin = ""
        self.adresse = self.numerodemande = self.numerocertificat = ""
        self.has_consorts, self.allrows = False, []
        self.AreaCf = 0
        self.X_coord = 0
        self.Y_coord = 0

        self.voisins = []
        self.query()
        self.query_area()
        self.query_voisinage()

    def setCodeImageGenerator(self, codeImageGenerator): # type: (ICodeImageGenerator) -> None
        self.__codeImageGenerator = codeImageGenerator

    def check_if_it_has_proprio_morale(self):
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "SELECT * FROM public.personnemoraleparcelle_d WHERE idparcelle = (SELECT gid FROM parcelle_d WHERE idcertificat = %s)"
        rows = None
        try:
            cursor.execute(sql, (self.idcertificat,))
            rows = cursor.fetchall()
        except Exception as err:
            self.connection.rollback()
        cursor.close()
        if rows is not None and len(rows) > 0:
            return True
        else:
            return False

    def query(self):
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if self.check_if_it_has_proprio_morale():
            sql = "SELECT DISTINCT C.*, " \
                  "personnemorale.*, " \
                  " coalesce(H.nomhameau, '') nomhameau, coalesce(F.nomfokontany, '') nomfokontany," \
                  " coalesce(M.nomcommune, '') nomcommune, coalesce(D.nomdistrict, '') nomdistrict," \
                  " coalesce(R.nomregion, '') nomregion," \
                  " dmd.datedemande," \
                  " dmd.consistance," \
                  " dmd.categorie" \
                  " FROM certificat C" \
                  " INNER JOIN demande dmd ON C.numerodemande = dmd.numdemande " \
                  " LEFT JOIN parcelle_d P on P.idcertificat = C.idcertificat" \
                  " LEFT JOIN personnemoraleparcelle_d PPP ON PPP.idparcelle = P.gid" \
                  " LEFT JOIN personnemorale ON personnemorale.idpersonnemorale = PPP.idpersonne" \
                  " LEFT JOIN hameau H on H.idhameau = P.idhameau" \
                  " LEFT JOIN fokontany F on F.idfokontany = H.idfokontany" \
                  " LEFT JOIN commune M on M.idcommune = F.idcommune" \
                  " LEFT JOIN district D on D.iddistrict = M.iddistrict" \
                  " LEFT JOIN region R on R.idregion = D.idregion" \
                  " WHERE C.idcertificat = %s"
        else:
            sql = "SELECT DISTINCT C.*, " \
              "personne.*, " \
              " coalesce(H.nomhameau, '') nomhameau, coalesce(F.nomfokontany, '') nomfokontany," \
              " coalesce(M.nomcommune, '') nomcommune, coalesce(D.nomdistrict, '') nomdistrict," \
              " coalesce(R.nomregion, '') nomregion, coalesce(PPP.representant, False) representant, coalesce(PPP.estcoproprietaire, False) estcoproprietaire,"\
              " dmd.datedemande," \
              " dmd.consistance," \
              " dmd.categorie" \
              " FROM certificat C"\
              " INNER JOIN demande dmd ON C.numerodemande = dmd.numdemande "\
              " LEFT JOIN parcelle_d P on P.idcertificat = C.idcertificat" \
              " LEFT JOIN proprietaireparcelle PPP ON PPP.idparcelle = P.gid" \
              " LEFT JOIN personne ON personne.idpersonne = PPP.idpersonne" \
              " LEFT JOIN hameau H on H.idhameau = P.idhameau" \
              " LEFT JOIN fokontany F on F.idfokontany = H.idfokontany" \
              " LEFT JOIN commune M on M.idcommune = F.idcommune" \
              " LEFT JOIN district D on D.iddistrict = M.iddistrict" \
              " LEFT JOIN region R on R.idregion = D.idregion" \
              " WHERE C.idcertificat = %s"


        cursor.execute(sql, (self.idcertificat,))
        rows = cursor.fetchall()
        cursor.close()
        print 'toa ato le izy'
        print rows

        if len(rows) == 0:
            return
        i = 0
        if not self.check_if_it_has_proprio_morale():
            self.indexRepresentant = None
            self.indexCoproprio = None
            for data in rows:
                if data['representant']:
                    self.indexRepresentant = i
                if data['estcoproprietaire']:
                    self.indexCoproprio = i
                i += 1
            try:
                print 'tonga ato le izy'
                print "*****index representant****"
                print self.indexRepresentant
                if self.indexRepresentant == None:
                    self.indexRepresentant = 0

                self.row = rows[self.indexRepresentant]
                self.allrows = rows
                self.has_consorts = len(rows) > 1
                self.nompersonne = str(self.row['nompersonne']).decode('utf-8')
                self.prenompersonne = str(self.row['prenompersonne']).decode('utf-8')
                #self.cin = str(self.row["numcipersonne"][0:3]).strip() + "-"+str(self.row["numcipersonne"][3:6]).strip() + "-"+str(self.row["numcipersonne"][6:9]).strip() + "-"+str(self.row["numcipersonne"][9:len(self.row["numcipersonne"])]).strip()
                #if len(self.cin.strip()) == 0:
                self.cin = None
                if self.row["numactenaissancepersonne"] is not None:
                    self.cin = u"Copie n°: " + self.row["numactenaissancepersonne"]
                if self.row["numcipersonne"] is not None:
                    self.cin = str(self.row["numcipersonne"][0:3]).strip() + "-" + str(
                        self.row["numcipersonne"][3:6]).strip() + "-" + str(
                        self.row["numcipersonne"][6:9]).strip() + "-" + str(
                        self.row["numcipersonne"][9:len(self.row["numcipersonne"])]).strip()

                self.lieucin = None
                if self.row['lieuactenaissancepersonne'] is not None:
                    self.lieucin = self.row['lieuactenaissancepersonne']
                if self.row['lieucipersonne'] is not None:
                    self.lieucin = self.row['lieucipersonne']

                self.datecin = None
                if self.row['dateactenaissancepersonne'] is not None:
                    self.datecin = self.row['dateactenaissancepersonne']
                if self.row['datecipersonne'] is not None:
                    self.datecin = self.row['datecipersonne']

                self.adresse = str(self.row['adressepersonne']).decode('utf-8')
                self.numerocertificat = self.row["numerocertificat"]
                self.numerodemande = self.row["numerodemande"]
                #Recuperer le coproprio
                if self.indexCoproprio is not None:
                    self.has_consorts = (len(rows) - 1) > 1
                    self.row = rows[self.indexCoproprio]
                    self.nomPrenomCoproprio = unicode(self.row['nompersonne']) + unicode(" ") + unicode(self.row['prenompersonne'])
                    self.cinCoproprio = str(self.row["numcipersonne"][0:3]).strip() + "-"+str(self.row["numcipersonne"][3:6]).strip() + "-"+str(self.row["numcipersonne"][6:9]).strip() + "-"+str(self.row["numcipersonne"][9:len(self.row["numcipersonne"])]).strip()
            except StandardError as e:
                print e
        else:
            self.row = rows[0]
            self.allrows = rows

            self.numerocertificat = self.row["numerocertificat"]
            self.numerodemande = self.row["numerodemande"]

            for data in rows:
                self.denominationPM = data['denomination']
                self.dateCreationPM = data['datecreation']
                self.siegePM = data['siege']
                self.idTypePM = data['idtype']
                self.idRepresentantPM = data['idrepresentant']
                self.nomRepresentantPM = "----"
                if self.idRepresentantPM is not None:
                    self.nomRepresentantPM = self.getNomRepresentant(self.idRepresentantPM)

                self.nomTypePM = self.getNameType(self.idTypePM)[0]
                print ("nomTypePM " + self.nomTypePM)
                break

    def getNomRepresentant(self, idRepresentant):
        cur = self.connection.cursor()
        nom = ""
        try:
            cur.execute("SELECT CONCAT(pp.nompersonne,' ', pp.prenompersonne) FROM personne pp WHERE pp.idpersonne = %s", (idRepresentant,))
            res = cur.fetchone()
        except Exception as err:
            print ("Erreur de lecture nom representant " + str(err))

        if len(res) > 0:
            nom = res[0]

        return nom

    def getNameType(self, idtype):
        curs = self.connection.cursor()
        sql = "SELECT type FROM typepersonnemorale WHERE idtype = %s"
        res = None
        try:
            curs.execute(sql, (idtype,))
            res = curs.fetchone()
        except Exception as err:
            self.connection.rollback()

        return res

    def query_area(self):
        numdemande = self.numerodemande if self.numerodemande is not None else ""
        demande = numdemande.strip()
        cursor = self.connection.cursor()
        try :
            sql = "SELECT ST_Area(geom), ST_X(ST_Transform(ST_Centroid(geom), "+str(globalvars.EPSG_SCR)+")), ST_Y(ST_Transform(ST_Centroid(geom), "+str(globalvars.EPSG_SCR)+"))  FROM parcelle_d  WHERE numdemande=%s"
            cursor.execute(sql, (demande,))
            dm = cursor.fetchone()
            self.AreaCf = dm[0]
            self.X_coord = dm[1]
            self.Y_coord = dm[2]
        except StandardError as e:
            self.X_coord = 0
            self.Y_coord = 0
            self.AreaCf = 0
            print e
            self.connection.rollback()

    def query_voisinage(self):
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute(
                "select pc.idpointscardinaux, pc.position, pc.fanondroana, lp.description "
                "from pointscardinaux pc, limitesparcelle lp, parcelle_d pd "
                "WHERE lp.idparcelle = pd.gid "
                "and lp.idpointscardinaux = pc.idpointscardinaux "
                "and pd.idcertificat = %s order by pc.idpointscardinaux ASC ", (self.idcertificat,))
            self.voisins = cursor.fetchall()
        except Exception as e:
            print(e)
        cursor.close()

    def doprint(self, filename="", area=0):
        self.pdf = PlofPdf(format='a4', orientation='landscape')
        self.area = area
        self.page1(filename)
        self.page2()
        if self.has_consorts:
            self.page_consorts()
        print ' niala atove'
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * from certificat WHERE idcertificat = %s", [int(self.idcertificat)])
        dm = cursor.fetchone()
        if dm[0] is None:
            print("CF NULL")
        else:
            numCF = dm[0]
            print(dm[0])

        print("NUM CF")
        print(numCF)
        self.pdf.show(numCF.strip()+".pdf", True)
        from Projet.journalRunn import journal
        journal = journal(self.connection)
        journal.inserToJournal(globalvars.id_user, self.idcertificat, "Certificat", "Impression de certificat foncier")

    def page1(self, filename):
        if self.row is None:
            return
        self.pdf.add_page()
        self.pdf.split()
        self.pdf.set_column(1)
        self.pdf.set_line_width(0.5)
        self.pdf.fullwidthrect("Ampahany amin'ny sarin-tany", self.pdf.get_y(), border=0)
        self.pdf.rect(self.pdf.l_margin, self.pdf.get_y(), self.pdf.xm1, self.pdf.h - self.pdf.b_margin)
        self.pdf.rect(self.pdf.l_margin + 5, self.pdf.get_y() + 5, self.pdf.xm1 - 10,
                      self.pdf.h - self.pdf.b_margin - 10)
        self.pdf.set_line_width(0.2)

        w = (self.pdf.xm1 - self.pdf.l_margin) * self.pdf.k
        h = (self.pdf.h - self.pdf.b_margin - 10) * self.pdf.k
        if filename == "":
            filename = self.preview()
        if filename is not None:
            self.pdf.image(filename, self.pdf.l_margin + 5, self.pdf.t_margin + 11, w / self.pdf.k, h / self.pdf.k)
            os.remove(filename)
        self.pdf.image("./icone/north.png", self.pdf.xm1 + 11, self.pdf.h - 25, 7, 15)
        #self.pdf.image("./icone/LegendeF.png", self.pdf.xm1 - 30, self.pdf.h - 23, 20, 12)
        self.pdf.set_font("Arial", size=10)
        self.pdf.set_y(self.pdf.h - self.pdf.b_margin - 10)
        self.pdf.set_x(self.pdf.xm1 + 10)
        self.pdf.rotate(90)
        self.pdf.cell(150, 10, _fromUtf8("Projection utilisée pour les coordonnées cartographiques : LABORDE - MADAGASCAR"), 0)

        self.pdf.rotate(0)
        self.pdf.set_column(2)
        if self.row['isprint'] is None :
            print('is PRINT NONE')
        else :
            if self.row['isprint']:
                self.pdf.set_font("Arial", size=8)
                self.pdf.set_text_color(255, 0, 0)
                self.pdf.set_y(self.pdf.t_margin - 8)
                self.pdf.set_x(self.pdf.get_x_column())
                #Phase test
                #self.pdf.write(self.pdf.line_height, "-- Duplicata du %s --" % Utils.date_format(str(datetime.date.today())))
                self.pdf.set_text_color(0, 0, 0)

        self.pdf.fullwidthrect("REPOBLIKAN'I MADAGASIKARA\nFitiavana - Tanindrazana - Fandrosoana", self.pdf.t_margin,
                               0)
        self.pdf.line_break()
        self.pdf.label("FARITRA", u" (Région) : ", str(self.row['nomregion']))
        self.pdf.label("DISTRIKA", " (District) : ", str(self.row['nomdistrict']))
        self.pdf.label("KAOMININA", " (Commune) : ", str(self.row['nomcommune']))
        self.pdf.label("FOKONTANY", " (Quartier) : ", str(self.row["nomfokontany"]))

        self.pdf.line_break(5)
        self.pdf.set_x(10 + self.pdf.xm1 + self.pdf.l_margin * 2)
        self.pdf.set_font("Times", size=40, style="B")
        self.pdf.cell((self.pdf.w / 2) - self.pdf.l_margin * 2, 40, "KARATANY", 1, align="C")
        self.pdf.set_font("Times", size=24)
        self.pdf.line_break(2)
        self.pdf.set_x(10 + self.pdf.xm1 + self.pdf.l_margin * 2)
        self.pdf.cell((self.pdf.w / 2) - self.pdf.l_margin * 2, 30, "Certificat Foncier", 0, align="C")

        self.pdf.line_break(5)
        self.pdf.set_font("Times", size=10)
        self.pdf.set_x(10 + self.pdf.xm1 + self.pdf.l_margin * 2)
        self.pdf.cell((self.pdf.w / 2) - self.pdf.l_margin * 2, 30, u"KARATANY N°. : ................................................", 0, align="R")
        self.pdf.set_x(95 + self.pdf.xm1 + self.pdf.l_margin * 2)
        self.pdf.set_font("Times", size=10, style="B")
        self.pdf.cell((self.pdf.w / 2) - self.pdf.l_margin * 2, 28, self.numerocertificat, 0, align="L")
        self.pdf.line_break(1)

        self.pdf.set_font("Times", size=10)
        self.pdf.set_x(10 + self.pdf.xm1 + self.pdf.l_margin * 2)
        self.pdf.cell((self.pdf.w / 2) - self.pdf.l_margin * 2, 30, u"FANGATAHANA N°. : ................................................", 0, align="R")
        self.pdf.set_x(95 + self.pdf.xm1 + self.pdf.l_margin * 2)
        self.pdf.set_font("Times", size=10, style="B")
        self.pdf.cell((self.pdf.w / 2) - self.pdf.l_margin * 2, 28, self.numerodemande, 0, align="L")

        try:
            print("CERTIFICAT")
            print(self.numerocertificat)

            print("NOM")
            print(self.nompersonne)

            print("PRENOM")
            print(self.prenompersonne)

            print("CIN")
            print(self.cin)

            print("AREA")

            if self.nompersonne == None :
                self.nompersonne = " "

            if self.prenompersonne == None :
                self.prenompersonne = " "

            print(self.area)
            if self.cin == None :
                self.cin = "000 000 000 000"
            if self.area == None:
                self.area = ''
            else :
                area =  Utils.area_to_str(self.area)

            qrCodeTxt = self.__getQrCodeText()
            print ("qcode text")
            print(qrCodeTxt)
            if self.__codeImageGenerator != None :
                try:
                    generatedCodeImage = self.__codeImageGenerator.generateImage(qrCodeTxt)
                    self.pdf.image(generatedCodeImage, (self.pdf.w / 2) + self.pdf.l_margin, 150, 30, 30)
                except Exception as e:
                    print e
        except Exception as e:
            print(e)

    def page2(self):
        if self.row is None:
            return
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=12)

        self.pdf.split()

        self.pdf.set_column(1)
        self.pdf.fullwidthrect(u"MOMBAMOMBA NY TANY\nIdentité de la parcelle", self.pdf.get_y())

        #self.pdf.line_break()
        self.pdf.label("Faritra", u" (Région) : ", str(self.row['nomregion']))
        self.pdf.label("Distrika", " (District) : ", str(self.row['nomdistrict']))
        self.pdf.label("Kaominina", " (Commune) : ", str(self.row["nomcommune"]))
        self.pdf.label("Fokontany", " (Quartier) : ", str(self.row["nomfokontany"]))
        self.pdf.label("Tanana", " (Village) : ", str(self.row["nomhameau"]))
        self.pdf.line_break()

        self.pdf.label(u"Karatany n°", u" (Certificat n°) : ", self.numerocertificat)
        self.pdf.label(u"Fangatahana n°: ", "", self.numerodemande)
        self.pdf.label("Velarany", " (Superficie) : ", "%s" % Utils.area_to_str(self.AreaCf))
        self.pdf.label("Karazan-tany", u" (Catégorie) :", str(self.row["categorie"]))
        self.pdf.label("Zava-misy", " (Consistance) :", str(self.row["consistance"]))
        self.pdf.line_break()

        self.pdf.label("Mpifanila", " (Voisins)", "", False)
        
        points = {'Nord':'Avaratra', 'Sud':'Atsimo', 'Est':'Atsinanana', 'Ouest':'Andrefana'}
        print("---self.voisins---")
        print(self.voisins)
        for v in self.voisins:
            points.pop(str(v["position"]).strip())
            self.pdf.label(str(v["fanondroana"]).strip(), " (" + str(v["position"]).strip() + ") : ", str(v["description"]).strip().decode('utf-8'))
        for key, val in points.items():
            self.pdf.label(str(val).strip(), " (" + str(key).strip() + ") : ", " ")

        self.pdf.line_break()

        self.pdf.label("Zo aman'andraikitra", " (Charges et droits grevant la parcelle): ", "")
        charge = unicode(self.autreCharge()) +  unicode("\n") + unicode(self.hypotheque()) + unicode("\n") + unicode(self.servitude())
        if charge != "":
            self.pdf.label("", "", charge)
        else:
            self.pdf.label("", "", "")
            self.pdf.label("", "", "")
            self.pdf.label("", "", "")

        self.pdf.set_column(2)
        self.pdf.fullwidthrect(u"MOMBAMOMBA NY TOMPON-TANY\nIdentité du propriétaire", self.pdf.t_margin)
        #self.pdf.line_break()
        if not self.check_if_it_has_proprio_morale():
            self.pdf.label(
                "Anarana"
                , " (Nom) : "
                , "%s %s" % (_fromUtf8(self.nompersonne), "(et consorts *)" if self.has_consorts else "")
            )
            self.pdf.label("Fanampiny", u" (Prénom(s)) : ", _fromUtf8(self.prenompersonne))
            self.pdf.label(u"Karapanondro n°", " (CIN) : ", _fromUtf8(self.cin))
            if self.datecin:
                self.pdf.label("Tamin'ny", " (Du) : ", _fromUtf8(Utils.date_format(str(self.datecin))))
            else:
                self.pdf.label("Tamin'ny", " (Du) : ", "   ")
            self.pdf.label("Tao", " (A) : ", _fromUtf8(self.lieucin))
            self.pdf.label("Fonenana", " (Adresse) : ", _fromUtf8(self.adresse))

            if self.indexCoproprio is not None:
                self.pdf.label("Vady Mpiaratompo", u"(Copropriétaire): ",_fromUtf8(self.nomPrenomCoproprio))
                self.pdf.label(u"Karapanondro n°", " (CIN) : ", _fromUtf8(self.cinCoproprio))
                if (len(self.allrows) - 2) > 0:
                    texteConsorts = u"Fanamarihana: Ny takelaka fanampiny dia misy mpiaratompo miisa " + str(
                        len(self.allrows) - 2)
                    self.pdf.set_x(self.pdf.get_x_column())
                    self.pdf.write(self.pdf.line_height, texteConsorts)
                self.pdf.line_break(2)
            else:
                if len(self.allrows) > 1:
                    texteConsorts = u"Fanamarihana: Ny takelaka fanampiny dia misy mpiaratompo miisa " + str(
                        len(self.allrows) - 1)
                    self.pdf.set_x(self.pdf.get_x_column())
                    self.pdf.write(self.pdf.line_height, texteConsorts)
                self.pdf.line_break(2)
        else:
            self.pdf.label(
                "Anarana"
                , u"(Dénomintation) : "
                , "%s" % (_fromUtf8(self.denominationPM))
            )
            self.pdf.label("Karazany", u" (Type) : ", _fromUtf8(self.nomTypePM))
            self.pdf.label("Mpisolotena", u" (Représentant) : ", _fromUtf8(self.nomRepresentantPM))
            if self.dateCreationPM:
                self.pdf.label("Daty niorenana", " (Date de creation) : ", _fromUtf8(Utils.date_format(str(self.dateCreationPM))))
            else:
                self.pdf.label("Daty niorenana", " (Date de creation) : ", "   ")
            self.pdf.label("Adiresy", " (Adresse) : ", _fromUtf8(self.siegePM))

            self.pdf.line_break(2)

        self.pdf.fullwidthrect("FANKATOAVANA\nValidation ", self.pdf.get_y())
        self.pdf.line_break()
        self.pdf.label("Fitsirihina ifotony natao ny : ", "", Utils.date_format(str(self.row['datereconnaissance'])), True, False)
        self.pdf.set_font("Arial", size=12)
        self.pdf.set_x(self.pdf.get_x_column())
        self.pdf.write(self.pdf.line_height,u"(Reconnaissance locale effectuée le)" )

        self.pdf.line_break(3)
        self.pdf.label("Androany faha ", "", "",True, False)
        self.pdf.fullwidthrect("Ny Ben'ny Tanana,\nLe Maire, ", self.pdf.get_y(), border=0)

        qrCodeTxt = self.__getQrCodeText()
        if self.__codeImageGenerator != None:
            generatedCodeImage = self.__codeImageGenerator.generateImage(qrCodeTxt)
            try:
                self.pdf.image(generatedCodeImage, (self.pdf.w / 2) + 100, 170, 30, 30)
            except Exception as err:
                print (err)

    def page_consorts(self):
        self.pdf.add_page()
        self.pdf.set_column(1)
        self.pdf.set_font("Arial", size=12, style="B")
        self.pdf.cell(self.pdf.w - self.pdf.l_margin * 2, self.pdf.rect_height, 'CONSORTS * Karatany n° ' + self.numerocertificat, 1, 1, 'C')
        self.pdf.line_break()
        self.pdf.set_font("Arial", size=10)

        w1, w2, w3, w4, w5 = 110, 35, 20, 55, 60
        self.pdf.set_font("Arial", size=10, style='B')
        self.pdf.cell(w1, 10, 'Anarana', 1, 0, 'C')
        self.pdf.cell(w2, 10, 'Karapanondro', 1, 0, 'C')
        self.pdf.cell(w3, 10, "Tamin'ny", 1, 0, 'C')
        self.pdf.cell(w4, 10, 'Tao', 1, 0, 'C')
        self.pdf.cell(w5, 10, 'Fonenana', 1, 1, 'C')
        self.pdf.set_font("Arial", size=8)
        for idx, r in enumerate(self.allrows):
            if idx == self.indexRepresentant or idx == self.indexCoproprio:
                continue

            print 'tonga ato ve 0'
            self.pdf.cell(w1, 8, r['nompersonne'] + " " + r['prenompersonne'], 1, 0)
            try :
                if r['numcipersonne'] is not None:
                    self.pdf.cell(w2, 8, str(r["numcipersonne"][0:3]).strip() + "-"+str(r["numcipersonne"][3:6]).strip() + "-"+str(r["numcipersonne"][6:9]).strip() +
                                  "-"+str(r["numcipersonne"][9:len(r["numcipersonne"])]).strip(), 1, 0)
                    self.pdf.cell(w3, 8, "%s" % Utils.date_format(str(r['datecipersonne']), ), 1, 0)
                elif r['numactenaissancepersonne'] is not None:
                    self.pdf.cell(w2, 8, u"Copie n°: " + r['numactenaissancepersonne'] , 1, 0)
                    self.pdf.cell(w3, 8, "%s" % Utils.date_format(str(r['dateactenaissancepersonne']), ), 1, 0)
                else :
                    self.pdf.cell(w2, 8, '.....', 1, 0)
            except Exception as err:
                print (err)


            """if r['numcipersonne'] is not None:
                self.pdf.cell(w2, 8, str(r["numcipersonne"][0:3]).strip() + "-"+str(r["numcipersonne"][3:6]).strip() + "-"+str(r["numcipersonne"][6:9]).strip() + "-"+str(r["numcipersonne"][9:len(r["numcipersonne"])]).strip(), 1, 0)
                self.pdf.cell(w3, 8, "%s" % Utils.date_format(str(r['datecipersonne']), ), 1, 0)
            elif r['numactenaissancepersonne'] is not None:
                self.pdf.cell(w2, 8, u"Copie n°: " + r['numactenaissancepersonne'] , 1, 0)
                self.pdf.cell(w3, 8, "%s" % Utils.date_format(str(r['dateactenaissancepersonne']), ), 1, 0)
            else :
                self.pdf.cell(w2, 8, '.....', 1, 0)"""


            if r['lieucipersonne'] is not None :
                self.pdf.cell(w4, 8, r['lieucipersonne'], 1, 0)
            elif r['lieuactenaissancepersonne'] is not None :
                self.pdf.cell(w4, 8, r['lieuactenaissancepersonne'], 1, 0)
            else :
                self.pdf.cell(w4, 8, '.....', 1, 0)

            if r['adressepersonne'] is not None :
                self.pdf.cell(w5, 8, r['adressepersonne'], 1, 1)
            else :
                self.pdf.cell(w5, 8, '......', 1, 1)
            print 'tonga ato ve p'

    def preview(self):
        from LayerPreview import LayerPreview
        layerpreview = LayerPreview(self.connection, self.idcertificat)
        filename = layerpreview.render()
        self.area = layerpreview.area
        self.X = layerpreview.X
        self.Y = layerpreview.Y
        layerpreview.deleteLayers()
        return filename

    def autreCharge(self):
        print "autre charge"
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select a.idcharge, a.descriptioncharge, a.dateinscriptionregistre "
                             "FROM autrecharge a, parcelle_d pd , autrechargesparcelle_d apd "
                             "WHERE a.idcharge = apd.idcharge AND apd.idparcelle = pd.gid "
                             "AND pd.idcertificat = %s", (self.idcertificat,))
        results = cursor.fetchall()
        autreCharge = ""
        if len(results) > 0:
            autreCharge = unicode("Autre charge: ")
        for res in results:
            autreCharge = autreCharge + unicode(res['descriptioncharge']).strip() + "."
            print "autreCharge = " + autreCharge

        return autreCharge
                #######AFFICHAGE DES CHARGES EXISTANTES##########

    def hypotheque(self):
        print "hypoyheque"
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(
            "select h.idhypotheque, h.dateinscriptionregistre, (h.valeur::money::numeric::float8) AS valeur, h.creancier, h.duree,  h.dateradiation "
            "from hypotheque h, parcelle_d pd, hypothequeparcelle_d hpd "
            "WHERE h.idhypotheque = hpd.idhypotheque AND hpd.idparcelle = pd.gid "
                "AND pd.idcertificat = %s", (self.idcertificat,))
        results = cursor.fetchall()
        hypotheque = ""
        if len(results) > 0:
            hypotheque = unicode("Hypotheque: ")
        for res in results:
            hypotheque += unicode(res['creancier']).strip() + " mitentina " + unicode(res['valeur']).strip() + "."

        return hypotheque

    def servitude(self):
        print "servitude"
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(
            "select s.idservitude, s.numeroservitude, s.descriptionservitude, s.dateinscription, s.origine, s.datelevee "
            "FROM servitude s, parcelle_d pd, servitudeparcelle_d spd "
            "WHERE s.idservitude = spd.idservitude AND spd.idparcelle = pd.gid "
            "AND pd.idcertificat = %s", (self.idcertificat,))
        results = cursor.fetchall()
        servitude = ""
        if len(results) > 0:
            servitude = "Servitude: "
        for res in results:
            servitude += unicode(res['descriptionservitude']).strip()  + "."

        return servitude

    def __getQrCodeText(self):
        print ("call of qrcode Text")
        if not self.check_if_it_has_proprio_morale():
            dateDemande = self.row['datedemande'].strftime('%d/%m/%Y') if self.row['datedemande'] else ''
            dateReconnaissance = self.row['datereconnaissance'].strftime('%d/%m/%Y') if self.row['datereconnaissance'] else ''
            qrCodeTxt = "Karatany laharana: " + self.numerocertificat + "\nTompony: " + self.nompersonne + " " + self.prenompersonne + "\nKarapanondro: " + self.cin + "\nVelarany: " + Utils.area_to_str(self.AreaCf)
            qrCodeTxt = qrCodeTxt + "\n" + "Region: " + str(self.row['nomregion']) + " Distict: " + str(self.row['nomdistrict']) + " Commune: " + str(self.row['nomcommune'])
            qrCodeTxt = qrCodeTxt + "\n(X = " + str(self.X_coord) + "; Y = " + str(self.Y_coord) + ")"
            qrCodeTxt = qrCodeTxt + "\nDemande du: " + dateDemande + "\nRL du " + dateReconnaissance
            if (globalvars.groupe_id==14):
                qrCodeTxt = qrCodeTxt+" - DT"
            print 'ato ainny qrcode'
            print qrCodeTxt
            return qrCodeTxt

        else:
            dateDemande = self.row['datedemande'].strftime('%d/%m/%Y') if self.row['datedemande'] else ''
            dateReconnaissance = self.row['datereconnaissance'].strftime('%d/%m/%Y') if self.row[
                'datereconnaissance'] else ''
            qrCodeTxt = "Karatany laharana: " + self.numerocertificat + "\nTompony: " + self.denominationPM + " " + "\nKarazany: " + self.nomTypePM + " "+ "\nDaty niorenana: " + self.dateCreationPM.strftime('%d/%m/%Y') + " " + "\nAdiresy: " + self.siegePM + "\nMpisolotena: " + self.nomRepresentantPM + " " + "\nVelarany: " + Utils.area_to_str(
                self.AreaCf)
            qrCodeTxt = qrCodeTxt + "\n" + "Region: " + str(self.row['nomregion']) + " Distict: " + str(
                self.row['nomdistrict']) + " Commune: " + str(self.row['nomcommune'])
            qrCodeTxt = qrCodeTxt + "\n(X = " + str(self.X_coord) + "; Y = " + str(self.Y_coord) + ")"
            qrCodeTxt = qrCodeTxt + "\nDemande du: " + dateDemande + "\nRL du " + dateReconnaissance
            if (globalvars.groupe_id == 14):
                qrCodeTxt = qrCodeTxt + " - DT"
            print
            'ato ainny qrcode'
            print
            qrCodeTxt
            return qrCodeTxt
