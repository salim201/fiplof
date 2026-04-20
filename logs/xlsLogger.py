# -*- coding: utf-8 -*-
import globalvars
import os
import os.path
import webbrowser
import tempfile
from random import randint
import datetime
from xlwt import Workbook
from xlwt import Style

class xlsLogger():
    def __init__(self, filename):
        self.title = ["code_parcelle", "numero_demande", "Etat insertion", "Erreur"]
        self.tabVal = []
        self.filename = filename
        self.book = Workbook()

    def appendLine(self, code_parcelle = '', numdemande = '', etatInsertion = '', erreur  = ''):
        self.tabVal.append({"code_parcelle": code_parcelle, "numero_demande": numdemande, "etat_insertion":etatInsertion, "erreur":erreur})


    def addSheet(self, title, data, sheet_name):
        book = Workbook()
        feuille = self.book.add_sheet(sheet_name + str(randint(10000, 99999)), True)
        styleTitreAvecFondGris = Style.easyxf(
            'font: bold on, height 200; align: wrap on, vert centre, horiz center; pattern: pattern solid, fore_colour gray25; borders: left 2, right 2, top 2, bottom 2')
        styleDonneeSansFond = Style.easyxf(
            'font: height 200; align: wrap on, vert centre, horiz left; borders: left 2, right 2, top 2, bottom 2')
        l = 0
        while (l < len(title)):
            if l == 3 or l == 2:
                feuille.col(l).width = (100 + len(title[l])) * 256
            else:
                feuille.col(l).width = (1 + len(title[l])) * 256
            feuille.write(0, l, title[l], styleTitreAvecFondGris)
            l = l + 1

        xl_curr_row = 0
        print "Len TabVal************************************"
        print len(data)
        while xl_curr_row < len(data):
            for key, val in data[xl_curr_row].items():
                i = 0
                while i  < len(title):
                    if str(key).strip() == str(title[i]).strip():
                        feuille.write(xl_curr_row + 1, i, str(val).decode('utf-8'), styleDonneeSansFond)
                        break
                    i = i + 1

            xl_curr_row = xl_curr_row + 1

    def addSheetShapePLOF(self, title, data, sheet_name):
        book = Workbook()
        feuille = self.book.add_sheet(sheet_name + str(randint(10000, 99999)), True)
        styleTitreAvecFondGris = Style.easyxf(
            'font: bold on, height 200; align: wrap on, vert centre, horiz center; pattern: pattern solid, fore_colour gray25; borders: left 2, right 2, top 2, bottom 2')
        styleDonneeSansFond = Style.easyxf(
            'font: height 200; align: wrap on, vert centre, horiz left; borders: left 2, right 2, top 2, bottom 2')
        l = 0
        while (l < len(title)):
            feuille.col(l).width = (50 + len(title[l])) * 256
            feuille.write(0, l, title[l], styleTitreAvecFondGris)
            l = l + 1

        xl_curr_row = 0
        print "Len TabVal************************************"
        print len(data)
        while xl_curr_row < len(data):
            for key, val in data[xl_curr_row].items():
                i = 0
                while i  < len(title):
                    
                    if str(key).strip() == str(title[i]).strip():
                        feuille.write(xl_curr_row + 1, i, str(val).decode('utf-8'), styleDonneeSansFond)
                        break
                    i = i + 1

            xl_curr_row = xl_curr_row + 1

    def write(self):
        print ("ecriture du log")
        dst = os.path.join(tempfile.gettempdir(),
                           str(randint(10000, 99999)) + "-" + "Log_" + self.filename + ".xls")
        # dst = os.path.dirname(__file__) + "/" + str(randint(10000, 99999)) + "-" + "Registre de demande.xls"
        try:
            self.book.save(dst)
        except Exception as err:
            print err
        os.startfile(dst)



