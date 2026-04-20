# coding: utf-8
from PyQt4.QtGui import *
from PyQt4 import Qt
from PyQt4 import QtGui
import datetime
from .ConfigCategories import Ui_Dialog
import psycopg2
import psycopg2.extras
from Utils import Utils
import globalvars


class ConfigCategoriesRun(QDialog):
    def __init__(self, connection):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.connection = connection
        self.classeRanges = ["A", "B", "C", "D", "E"]
        self.ui = Ui_Dialog()
        QApplication.setOverrideCursor(Qt.Qt.WaitCursor)
        self.ui.setupUi(self)
        self.initCategories()
        self.initClasses()
        self.initConsistances()
        self.initConsistanceBat()
        self.initActions()
        self.addWidgetTable()
        try:
            self.initMasks()
        except Exception as err:
            print err
        self.ui.tabWidget_2.removeTab(3)
        self.ui.tabWidget_3.removeTab(3)
        QApplication.restoreOverrideCursor()

    def initActions(self):
        self.ui.pushButtonAnnuler.clicked.connect(self.reject)
        self.ui.pushButtonOK.clicked.connect(self.save)
        self.ui.tableWidgetIFTSurface.itemChanged.connect(self.updateIFTVenale)
        self.ui.tableWidgetIFPBSurface.itemChanged.connect(self.updateIFPBVenale)
        self.getMinImpot()

    def initCategories(self):
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "SELECT * FROM categorie ORDER BY idcategorie"
        res = False
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            res = True
        except Exception as e:
            print(e)
        cursor.close()
        if res:
            self.fillTableSurfaces(rows)
            self.fillTableVenale(rows)

    def initClasses(self):
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "SELECT * FROM classecategorieforfaitaire"
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            self.fillTableClasses(rows)
        except Exception as e:
            print(e)
        cursor.close()

    def initConsistances(self):
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "SELECT * FROM consistance ORDER BY libelleconsistance"
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            self.fillTableIFTConsistances(rows)
        except Exception as e:
            print(e)
        cursor.close()

    def initConsistanceBat(self):
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "SELECT * FROM consistance_batiment ORDER BY consistance"
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            self.fillTableIFPBConsistances(rows)
        except Exception as e:
            print(e)
        cursor.close()

    def fillTableSurfaces(self, rows):
        self.ui.tableWidgetIFTSurface.setColumnHidden(0, True)
        self.ui.tableWidgetIFPBSurface.setColumnHidden(0, True)
        self.ui.tableWidgetIFPBSurface.setColumnHidden(3, True)
        for row in rows:
            i = row["idcategorie"]
            type_imposition = str(row["typeimposition"]).strip()
            if type_imposition.lower() == "ift":
                itemid1 = QtGui.QTableWidgetItem(str(row["idcategorie"]))
                itemlabel1 = QtGui.QTableWidgetItem(unicode(row["libellecategorie"]).strip())
                itemvalue1 = QtGui.QTableWidgetItem(str(row["v_surface"]))
                self.setComboIdx("comboBoxIFTSurfaceUniteC", str(i), str(row['u_surface']).strip())
                self.ui.tableWidgetIFTSurface.setItem(i - 1, 0, itemid1)
                self.ui.tableWidgetIFTSurface.setItem(i - 1, 1, itemlabel1)
                self.ui.tableWidgetIFTSurface.setItem(i - 1, 2, itemvalue1)
            if type_imposition.lower() == "ifpb":
                '''print "type ifpb"
                print type_imposition
                print i'''
                itemid2 = QtGui.QTableWidgetItem(str(row["idcategorie"]))
                itemlabel2 = QtGui.QTableWidgetItem(unicode(row["libellecategorie"]).strip())
                itemvalue2 = QtGui.QTableWidgetItem(str(row["v_surface"]))
                '''print itemid2
                print itemlabel2
                print itemvalue2'''
                self.setComboIdx("comboBoxIFPBSurfaceUniteC", str(i-6), str(row['u_surface']).strip())
                self.removeEltFromCombo("comboBoxIFPBSurfaceUniteC", str(i-6),"Ar/a")
                self.removeEltFromCombo("comboBoxIFPBSurfaceUniteC", str(i-6),"Ar/ha")
                print "******fin item value*****"
                self.ui.tableWidgetIFPBSurface.setItem(i - 7, 0, itemid2)
                self.ui.tableWidgetIFPBSurface.setItem(i - 7, 1, itemlabel2)
                self.ui.tableWidgetIFPBSurface.setItem(i - 7, 2, itemvalue2)
            #itemvalue3 = QtGui.QTableWidgetItem(str(row["valeur_location_ha"]))


            #self.ui.tableWidgetIFPBSurface.setItem(i - 1, 3, itemvalue3)
        Utils.setTableWidgetColumnReadOnly(self.ui.tableWidgetIFTv_venale, 1)
        Utils.setTableWidgetColumnReadOnly(self.ui.tableWidgetIFPBv_venale, 1)
        Utils.resizeTableWidgetColumn(self.ui.tableWidgetIFTSurface, [2], 100)
        Utils.resizeTableWidgetColumn(self.ui.tableWidgetIFPBSurface, [2, 3], 200)

    def fillTableClasses(self, rows):
        for row in rows:
            if(len(self.classeRanges) < row["idclasse"]):
                continue
            if str(row['iftifpb']).strip().lower() == "ift":
                nameval = "lineEditIFTVal" + str(row["idcategorie"]) + self.classeRanges[row["idclasse"] - 1]
                namedeb = "lineEditDebutIFTC" + str(row["idcategorie"]) + self.classeRanges[row["idclasse"] - 1]
                namefin = "lineEditFinIFTC" + str(row["idcategorie"]) + self.classeRanges[row["idclasse"] - 1]
                self.setVal(nameval, row["valeurariary"])
                self.setTextValue(namedeb, row["debut"])
                self.setTextValue(namefin, row["fin"])
                self.removeEltFromCombo("comboBoxUniteIFTc", self.classeRanges[row["idclasse"] - 1], u"Pièces")
                self.setComboIdx("comboBoxUniteIFTc", self.classeRanges[row["idclasse"] - 1], row['unite'])

            if str(row['iftifpb']).strip().lower() == "ifpb":
                valcat = int(row["idcategorie"]) - 6
                '''print "valcat = " + str(valcat)'''
                namevalifpb = "lineEditIFTVal" + str(valcat) + self.classeRanges[row["idclasse"] - 1] + "_2"
                namedebifpb = "lineEditDebutIFPBC" + str(valcat) + self.classeRanges[row["idclasse"] - 1]
                namefinifpb = "lineEditFinIFPBC" + str(valcat) + self.classeRanges[row["idclasse"] - 1]
                self.setVal(namevalifpb, row["valeurariary"])
                self.setTextValue(namedebifpb, row["debut"])
                self.setTextValue(namefinifpb, row["fin"])
                self.removeEltFromCombo("comboBoxUniteIFPBc", self.classeRanges[row["idclasse"] - 1], "a")
                self.removeEltFromCombo("comboBoxUniteIFPBc", self.classeRanges[row["idclasse"] - 1], "Ha")
                self.setComboIdx("comboBoxUniteIFPBc", self.classeRanges[row["idclasse"] - 1], row['unite'])

    def fillTableIFTConsistances(self, rows):
        i = 0
        self.ui.tableWidgetIFTConsistance.setRowCount(len(rows))
        #self.ui.tableWidgetIFPBConsistance.setRowCount(len(rows))
        self.ui.tableWidgetIFTConsistance.setColumnHidden(0, True)
        #self.ui.tableWidgetIFPBConsistance.setColumnHidden(0, True)
        for row in rows:
            itemid = QtGui.QTableWidgetItem(str(row["idconsistance"]))
            itemlabel = QtGui.QTableWidgetItem(unicode(row["libelleconsistance"]))
            itemvalue = QtGui.QTableWidgetItem(str(row["valeurariary"]))
            #itemid2 = QtGui.QTableWidgetItem(str(row["idconsistance"]))
            #itemlabel2 = QtGui.QTableWidgetItem(unicode(row["libelleconsistance"]))
            #itemvalue2 = QtGui.QTableWidgetItem(str(row["valeurariary"]))
            #itemvalue3 = QtGui.QTableWidgetItem(str(row["valeurariary_ifpb"]))
            self.ui.tableWidgetIFTConsistance.setItem(i, 0, itemid)
            self.ui.tableWidgetIFTConsistance.setItem(i, 1, itemlabel)
            self.ui.tableWidgetIFTConsistance.setItem(i, 2, itemvalue)
            i += 1
        Utils.setTableWidgetColumnReadOnly(self.ui.tableWidgetIFTConsistance, 1)
        #Utils.setTableWidgetColumnReadOnly(self.ui.tableWidgetIFPBConsistance, 1)
        #Utils.setTableWidgetColumnReadOnly(self.ui.tableWidgetIFPBConsistance, 2)
        Utils.resizeTableWidgetColumn(self.ui.tableWidgetIFTConsistance, [2], 200)
        #Utils.resizeTableWidgetColumn(self.ui.tableWidgetIFPBConsistance, [2, 3], 200)

    def fillTableIFPBConsistances(self, rows):
        i = 0
        #self.ui.tableWidgetIFTConsistance.setRowCount(len(rows))
        self.ui.tableWidgetIFPBConsistance.setRowCount(len(rows))
        #self.ui.tableWidgetIFTConsistance.setColumnHidden(0, True)
        self.ui.tableWidgetIFPBConsistance.setColumnHidden(0, True)
        for row in rows:
            #itemid = QtGui.QTableWidgetItem(str(row["idconsistance"]))
            #itemlabel = QtGui.QTableWidgetItem(unicode(row["libelleconsistance"]))
            #itemvalue = QtGui.QTableWidgetItem(str(row["valeurariary"]))
            itemid2 = QtGui.QTableWidgetItem(str(row["id"]))
            itemlabel2 = QtGui.QTableWidgetItem(unicode(row["consistance"]))
            itemvalue2 = QtGui.QTableWidgetItem(str(row["valeurariary"]))
            itemvalue3 = QtGui.QTableWidgetItem(str(row["valeur_location"]))
            #self.ui.tableWidgetIFTConsistance.setItem(i, 0, itemid)
            #self.ui.tableWidgetIFTConsistance.setItem(i, 1, itemlabel)
            #self.ui.tableWidgetIFTConsistance.setItem(i, 2, itemvalue)
            self.ui.tableWidgetIFPBConsistance.setItem(i, 0, itemid2)
            self.ui.tableWidgetIFPBConsistance.setItem(i, 1, itemlabel2)
            self.ui.tableWidgetIFPBConsistance.setItem(i, 2, itemvalue2)
            self.ui.tableWidgetIFPBConsistance.setItem(i, 3, itemvalue3)
            i += 1
        #Utils.setTableWidgetColumnReadOnly(self.ui.tableWidgetIFTConsistance, 1)
        Utils.setTableWidgetColumnReadOnly(self.ui.tableWidgetIFPBConsistance, 1)
        #Utils.setTableWidgetColumnReadOnly(self.ui.tableWidgetIFPBConsistance, 2)
        #Utils.resizeTableWidgetColumn(self.ui.tableWidgetIFTConsistance, [2], 200)
        Utils.resizeTableWidgetColumn(self.ui.tableWidgetIFPBConsistance, [2, 3], 200)

    def save(self):
        QApplication.setOverrideCursor(Qt.Qt.WaitCursor)
        self.saveSurface()
        self.saveClasse()
        self.saveConsistances()
        self.saveVenale()
        self.saveMinImpot()
        QApplication.restoreOverrideCursor()
        self.accept()

    def saveMinImpot(self):
        min_ift = str(self.ui.lineEditMinIft.text())
        min_ifpb = str(self.ui.lineEditMinIfpb.text())
        currentDateTime = datetime.datetime.now()
        date = currentDateTime.date()
        annee = str(date.strftime("%Y"))
        if min_ifpb=="" or  min_ift=="" :
            QMessageBox.critical(self, u"Erreur les impôts minimums", u"Veuillez saisir les informations sur les minimums Impôts ")
            return
        #sql = """INSERT INTO categorie(idcategorie,libellecategorie,typeimposition,v_surface, u_surface)
        #                        VALUES(%s,%s,'ift',%s,%s)"""
        sql="""
            UPDATE public.impot_minimum
                    SET  valeur=%s, annee=%s
                    WHERE  type='ift' AND annee=%s;
            INSERT INTO public.impot_minimum(
                    valeur,type, annee)
                    SELECT %s, 'ift', %s 
                    WHERE NOT EXISTS(SELECT * FROM public.impot_minimum WHERE type='ift' AND annee=%s);
            """
        valueift = [ min_ift,annee,annee, min_ift, annee,annee]
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, valueift)
            self.connection.commit()
        except Exception as e:
            print(e)
            self.connection.rollback()
        cursor.close()

        sql = """
                    UPDATE public.impot_minimum
                            SET  valeur=%s, annee=%s
                            WHERE  type='ifpb' AND annee=%s;
                    INSERT INTO public.impot_minimum(
                            valeur,type,annee)
                            SELECT %s,'ifpb',%s
                            WHERE NOT EXISTS(SELECT * FROM public.impot_minimum WHERE type='ifpb' AND annee=%s);
                    """
        valueifpb = [min_ifpb, annee, annee, min_ifpb, annee, annee]
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, valueifpb)
            self.connection.commit()
        except Exception as e:
            print(e)
            self.connection.rollback()
        cursor.close()

        print '------------vita---------------'

    def getMinImpot(self):
        currentDateTime = datetime.datetime.now()
        date = currentDateTime.date()
        annee = str(date.strftime("%Y"))

        try:
            sql = "SELECT valeur FROM public.impot_minimum where type='ift' and  annee='" + annee+"'"
            cursor = self.connection.cursor()
            cursor.execute (sql)
            res = cursor.fetchone()
            #print '---res--------------------------------------------------------------------------------------------'
            #res =float(res[0])
            if res is not None:
                self.ui.lineEditMinIft.setText(str(res[0]))
        except Exception as err:
            print (err)
            cursor.close()

        try:
            sql = "SELECT valeur FROM public.impot_minimum where type='ifpb' and annee='" + annee+"'"
            cursor = self.connection.cursor()
            cursor.execute(sql)
            res = cursor.fetchone()
            if res is not None:
                self.ui.lineEditMinIfpb.setText(str(res[0]))
        except Exception as err:
            print (err)
            cursor.close()


    def saveSurface(self):
        for i in range(0, self.ui.tabWidget.count()):
            if i == 0:
                for i in range(0, 6):
                    idcategorie = Utils.getTableWidgetCellIntvalue(self.ui.tableWidgetIFTSurface, i, 0)
                    label = Utils.getTableWidgetCellStrValue(self.ui.tableWidgetIFTSurface, i, 1)
                    value = Utils.getTableWidgetCellIntvalue(self.ui.tableWidgetIFTSurface, i, 2)
                    value2 = Utils.getTableWidgetCellIntvalue(self.ui.tableWidgetIFPBSurface, i, 3)
                    unite = self.getComboVal("comboBoxIFTSurfaceUniteC", str(i+1))
                    if idcategorie > 0:
                        sql = """UPDATE categorie SET libellecategorie=%s, v_surface=%s, typeimposition = %s, u_surface = %s
                        WHERE idcategorie = %s"""
                        values = [label, value, 'ift',unite, idcategorie]
                    else:
                        sql = """INSERT INTO categorie(idcategorie,libellecategorie,typeimposition,v_surface, u_surface)
                        VALUES(%s,%s,'ift',%s,%s)"""
                        values = [i + 1, label, value, unite]
                    cursor = self.connection.cursor()
                    try:
                        cursor.execute(sql, values)
                        self.connection.commit()
                    except Exception as e:
                        print(e)
                        self.connection.rollback()
                    cursor.close()
            if i == 1:
                j = 0
                for i in range(6, 12):
                    idcategorie = 0
                    if self.exists("categorie", "idcategorie", i+1):
                        idcategorie = i + 1
                    #idcategorie = Utils.getTableWidgetCellIntvalue(self.ui.tableWidgetIFPBSurface, j, 0)

                    label = Utils.getTableWidgetCellStrValue(self.ui.tableWidgetIFPBSurface, j, 1)
                    value = Utils.getTableWidgetCellIntvalue(self.ui.tableWidgetIFPBSurface, j, 2)
                    value2 = Utils.getTableWidgetCellIntvalue(self.ui.tableWidgetIFPBSurface, j, 3)
                    j = j + 1
                    unite = self.getComboVal("comboBoxIFPBSurfaceUniteC", str(j))
                    if idcategorie > 0:
                        sql = """UPDATE categorie SET libellecategorie=%s, v_surface=%s, typeimposition = %s, u_surface = %s
                        WHERE idcategorie = %s"""
                        values = [label, value, 'ifpb',unite, idcategorie]
                    else:
                        sql = """INSERT INTO categorie(idcategorie,libellecategorie,typeimposition,v_surface, u_surface)
                        VALUES(%s,%s,'ifpb',%s,%s)"""
                        values = [i + 1, label, value, unite]
                    cursor = self.connection.cursor()
                    try:
                        cursor.execute(sql, values)
                        self.connection.commit()
                    except Exception as e:
                        print(e)
                        self.connection.rollback()
                    cursor.close()

    def getClasseRange(self, c):
        if c in self.classeRanges:
            return self.classeRanges.index(c) + 1

    def getLineEditVal(self, basename, idcategorie, classename):
        lineEdits = self.ui.tabWidget.findChildren(QtGui.QLineEdit, basename + str(idcategorie) + classename)
        for lineEdit in lineEdits:
            try:
                v = int(lineEdit.text())
                return v
            except Exception:
                return 0
        return 0

    def setVal(self, name, value):
        lineEdits = self.ui.tabWidget.findChildren(QtGui.QLineEdit, name)
        for lineEdit in lineEdits:
            lineEdit.setText(str(value))

    def setTextValue(self, name, value):
        lineEdits = self.ui.tabWidget.findChildren(QtGui.QLineEdit, name)
        for lineEdit in lineEdits:
            lineEdit.setText(str(value))

    def saveClasse(self):
        lineEdits = self.ui.tabWidget_2.findChildren(QtGui.QLineEdit)
        cursor = self.connection.cursor()
        for lineEdit in lineEdits:
            for i in range(0, self.ui.tabWidget.count()):
                if i == 0:
                    if "IFTVal" in lineEdit.objectName():
                        #lineEditIfpbs = self.ui.tabWidget.findChildren(QtGui.QLineEdit, lineEdit.objectName() + "_2")
                        sub = str(lineEdit.objectName()).replace("lineEditIFTVal", "")
                        idcategorie = sub[0]
                        classename = sub[1]
                        idclasse = self.getClasseRange(classename)
                        val = Utils.getLineEditIntValue(lineEdit)
                        deb = self.getLineEditVal("lineEditDebutIFTC", idcategorie, classename)
                        fin = self.getLineEditVal("lineEditFinIFTC", idcategorie, classename)
                        unite = self.getComboVal("comboBoxUniteIFTc", classename)
                        #val_ifpb = Utils.getLineEditIntValue(lineEditIfpbs[0])
                        #deb_ifpb = self.getLineEditVal("lineEditDebutIFPBC", idcategorie, classename)
                        #fin_ifpb = self.getLineEditVal("lineEditFinIFPBC", idcategorie, classename)
                        sql = "UPDATE classecategorieforfaitaire SET valeurariary = %s, debut = %s, fin = %s, iftifpb = 'ift', unite =  %s"\
                              " WHERE idcategorie = %s AND idclasse = %s ;" \
                              "INSERT INTO classecategorieforfaitaire(idcategorie, idclasse, iftifpb, debut, fin, valeurariary, unite)" \
                              " SELECT %s, %s, %s, %s, %s, %s, %s" \
                              " WHERE NOT EXISTS(" \
                              "     SELECT 1 FROM classecategorieforfaitaire" \
                              "     WHERE idcategorie = %s AND idclasse = %s " \
                              ")"
                        values = [val, deb, fin, unite,
                                  idcategorie, idclasse,
                                  idcategorie, idclasse, 'ift', deb, fin, val,unite,
                                  idcategorie, idclasse]
                        try:
                            cursor.execute(sql, values)
                            self.connection.commit()
                        except psycopg2.ProgrammingError as e:
                            print(e)
                            self.connection.rollback()
                if i == 1:
                    if "IFTVal" in lineEdit.objectName():
                        lineEditIfpbs = self.ui.tabWidget.findChildren(QtGui.QLineEdit, lineEdit.objectName() + "_2")
                        sub = str(lineEdit.objectName()).replace("lineEditIFTVal", "")
                        valEditCat = sub[0]
                        idcategorie = int(sub[0]) + 6
                        classename = sub[1]
                        idclasse = self.getClasseRange(classename)
                        unite = self.getComboVal("comboBoxUniteIFPBc", classename)

                        #val = Utils.getLineEditIntValue(lineEdit)
                        #deb = self.getLineEditVal("lineEditDebutIFTC", idcategorie, classename)
                        #fin = self.getLineEditVal("lineEditFinIFTC", idcategorie, classename)
                        val = Utils.getLineEditIntValue(lineEditIfpbs[0])

                        deb = self.getLineEditVal("lineEditDebutIFPBC", valEditCat, classename)
                        fin = self.getLineEditVal("lineEditFinIFPBC", valEditCat, classename)


                        sql = "UPDATE classecategorieforfaitaire SET valeurariary = %s, debut = %s, fin = %s, iftifpb = 'ifpb', unite = %s "\
                              " WHERE idcategorie = %s AND idclasse = %s ;" \
                              "INSERT INTO classecategorieforfaitaire(idcategorie, idclasse, iftifpb, debut, fin, valeurariary, unite)" \
                              " SELECT %s, %s, %s, %s, %s, %s, %s" \
                              " WHERE NOT EXISTS(" \
                              "     SELECT 1 FROM classecategorieforfaitaire" \
                              "     WHERE idcategorie = %s AND idclasse = %s " \
                              ")"
                        values = [val, deb, fin, unite,
                                  idcategorie, idclasse,
                                  idcategorie, idclasse, 'ifpb', deb, fin, val, unite,
                                  idcategorie, idclasse]
                        try:
                            cursor.execute(sql, values)
                            self.connection.commit()
                        except psycopg2.ProgrammingError as e:
                            print(e)
                            self.connection.rollback()
        cursor.close()

    def saveConsistances(self):
        cursor = self.connection.cursor()
        for i in range(0, self.ui.tableWidgetIFTConsistance.rowCount()):
            itemid = Utils.getTableWidgetCellIntvalue(self.ui.tableWidgetIFTConsistance, i, 0)
            value = Utils.getTableWidgetCellIntvalue(self.ui.tableWidgetIFTConsistance, i, 2)
            #value_ifpb = Utils.getTableWidgetCellIntvalue(self.ui.tableWidgetIFPBConsistance, i, 3)
            #sql = "UPDATE consistance SET valeurariary = %s, valeurariary_ifpb = %s WHERE idconsistance = %s"
            sql = "UPDATE consistance SET valeurariary = %s WHERE idconsistance = %s"
            values = [value, itemid]
            try:
                cursor.execute(sql, values)
                self.connection.commit()
            except Exception as e:
                print(e)
                self.connection.rollback()

        for i in range(0, self.ui.tableWidgetIFPBConsistance.rowCount()):
            itemid = Utils.getTableWidgetCellIntvalue(self.ui.tableWidgetIFPBConsistance, i, 0)
            value = Utils.getTableWidgetCellIntvalue(self.ui.tableWidgetIFPBConsistance, i, 2)
            value_location = Utils.getTableWidgetCellIntvalue(self.ui.tableWidgetIFPBConsistance, i, 3)
            #sql = "UPDATE consistance SET valeurariary = %s, valeurariary_ifpb = %s WHERE idconsistance = %s"
            sql = "UPDATE consistance_batiment SET valeurariary = %s, valeur_location = %s WHERE id = %s"
            values = [value, value_location, itemid]
            try:
                cursor.execute(sql, values)
                self.connection.commit()
            except Exception as e:
                print(e)
                self.connection.rollback()
        cursor.close()

    def exists(self, table, col, value):
        cur = self.connection.cursor()
        state = False
        try:
            sql = "select * from " + table + " where " + col + " = " + str(value)
            cur.execute (sql)
            res = cur.fetchone()
            if res is not None:
                state = True
        except Exception as err:
            print (err)
        cur.close()
        return state

    def addWidgetTable(self):
        Utils.resizeTableWidgetColumn(self.ui.tableWidgetIFTSurface, [3], 150)
        Utils.resizeTableWidgetColumn(self.ui.tableWidgetIFTv_venale, [3], 150)
        Utils.resizeTableWidgetColumn(self.ui.tableWidgetIFPBSurface, [3], 150)
        Utils.resizeTableWidgetColumn(self.ui.tableWidgetIFPBv_venale, [3], 150)

        # Add widget to table IFT comboBoxIFPBSurfaceUniteface
        self.ui.tableWidgetIFTSurface.setCellWidget(0,3,self.ui.comboBoxIFTSurfaceUniteC1)
        self.ui.tableWidgetIFTSurface.setCellWidget(1,3,self.ui.comboBoxIFTSurfaceUniteC2)
        self.ui.tableWidgetIFTSurface.setCellWidget(2,3,self.ui.comboBoxIFTSurfaceUniteC3)
        self.ui.tableWidgetIFTSurface.setCellWidget(3,3,self.ui.comboBoxIFTSurfaceUniteC4)
        self.ui.tableWidgetIFTSurface.setCellWidget(4,3,self.ui.comboBoxIFTSurfaceUniteC5)
        self.ui.tableWidgetIFTSurface.setCellWidget(5,3,self.ui.comboBoxIFTSurfaceUniteC6)

        # Add widget to table IFT Valeur Venale
        self.ui.tableWidgetIFTv_venale.setCellWidget(0,3,self.ui.comboBoxIFTV_venaleUniteC1)
        self.ui.tableWidgetIFTv_venale.setCellWidget(1,3,self.ui.comboBoxIFTV_venaleUniteC2)
        self.ui.tableWidgetIFTv_venale.setCellWidget(2,3,self.ui.comboBoxIFTV_venaleUniteC3)
        self.ui.tableWidgetIFTv_venale.setCellWidget(3,3,self.ui.comboBoxIFTV_venaleUniteC4)
        self.ui.tableWidgetIFTv_venale.setCellWidget(4,3,self.ui.comboBoxIFTV_venaleUniteC5)
        self.ui.tableWidgetIFTv_venale.setCellWidget(5,3,self.ui.comboBoxIFTV_venaleUniteC6)

        # Add widget to table IFPB Surface
        self.ui.tableWidgetIFPBSurface.setCellWidget(0,4,self.ui.comboBoxIFPBSurfaceUniteC1)
        self.ui.tableWidgetIFPBSurface.setCellWidget(1,4,self.ui.comboBoxIFPBSurfaceUniteC2)
        self.ui.tableWidgetIFPBSurface.setCellWidget(2,4,self.ui.comboBoxIFPBSurfaceUniteC3)
        self.ui.tableWidgetIFPBSurface.setCellWidget(3,4,self.ui.comboBoxIFPBSurfaceUniteC4)
        self.ui.tableWidgetIFPBSurface.setCellWidget(4,4,self.ui.comboBoxIFPBSurfaceUniteC5)
        self.ui.tableWidgetIFPBSurface.setCellWidget(5,4,self.ui.comboBoxIFPBSurfaceUniteC6)

        # Add widget to table IFPB Valeur Venale
        self.ui.tableWidgetIFPBv_venale.setCellWidget(0,4,self.ui.comboBoxIFPBV_venaleUniteC1)
        self.ui.tableWidgetIFPBv_venale.setCellWidget(1,4,self.ui.comboBoxIFPBV_venaleUniteC2)
        self.ui.tableWidgetIFPBv_venale.setCellWidget(2,4,self.ui.comboBoxIFPBV_venaleUniteC3)
        self.ui.tableWidgetIFPBv_venale.setCellWidget(3,4,self.ui.comboBoxIFPBV_venaleUniteC4)
        self.ui.tableWidgetIFPBv_venale.setCellWidget(4,4,self.ui.comboBoxIFPBV_venaleUniteC5)
        self.ui.tableWidgetIFPBv_venale.setCellWidget(5,4,self.ui.comboBoxIFPBV_venaleUniteC6)

    def getComboVal(self, basename, classename):

        name = basename + classename
        comBos = self.ui.tabWidget.findChildren(QtGui.QComboBox, name)

        for comBo in comBos:

            try:
                v = str(comBo.currentText()).encode('utf-8')
                return v
            except Exception as err:
                print err
                return ''
        return ''

    def setComboIdx(self, basename, classename, unite):

        name = basename + classename
        comBos = self.ui.tabWidget.findChildren(QtGui.QComboBox, name)

        for comBo in comBos:
            try:
                comBo.setCurrentIndex(comBo.findText(unite))

            except Exception as err:
                comBo.setCurrentIndex(0)
                print err

    def fillTableVenale(self, rows):
        self.ui.tableWidgetIFTv_venale.setColumnHidden(0, True)
        self.ui.tableWidgetIFPBv_venale.setColumnHidden(0, True)
        self.ui.tableWidgetIFPBv_venale.setColumnHidden(3, True)
        for row in rows:
            i = row["idcategorie"]
            type_imposition = str(row["typeimposition"]).strip()
            if type_imposition.lower() == "ift":
                itemid1 = QtGui.QTableWidgetItem(str(row["idcategorie"]))
                itemlabel1 = QtGui.QTableWidgetItem(unicode(row["libellecategorie"]).strip())
                itemvalue1 = QtGui.QTableWidgetItem(str(row["v_venale"]))
                itemTaux = QtGui.QTableWidgetItem(str(row["taux"]))
                self.setComboIdx("comboBoxIFTV_venaleUniteC", str(i), str(row['u_venale']).strip())
                self.ui.tableWidgetIFTv_venale.setItem(i - 1, 0, itemid1)
                self.ui.tableWidgetIFTv_venale.setItem(i - 1, 1, itemlabel1)
                self.ui.tableWidgetIFTv_venale.setItem(i - 1, 2, itemvalue1)
                self.ui.tableWidgetIFTv_venale.setItem(i - 1, 4, itemTaux)
            if type_imposition.lower() == "ifpb":

                itemid2 = QtGui.QTableWidgetItem(str(row["idcategorie"]))
                itemlabel2 = QtGui.QTableWidgetItem(unicode(row["libellecategorie"]).strip())
                itemvalue2 = QtGui.QTableWidgetItem(str(row["v_venale"]))
                itemTaux = QtGui.QTableWidgetItem(str(row["taux"]))

                self.removeEltFromCombo("comboBoxIFPBV_venaleUniteC",  str(i-6), "Ar/a")
                self.removeEltFromCombo("comboBoxIFPBV_venaleUniteC",  str(i-6), "Ar/ha")
                self.setComboIdx("comboBoxIFPBV_venaleUniteC", str(i-6), str(row['u_venale']).strip())
                '''print "******fin item value*****"'''
                self.ui.tableWidgetIFPBv_venale.setItem(i - 7, 0, itemid2)
                self.ui.tableWidgetIFPBv_venale.setItem(i - 7, 1, itemlabel2)
                self.ui.tableWidgetIFPBv_venale.setItem(i - 7, 2, itemvalue2)
                self.ui.tableWidgetIFPBv_venale.setItem(i - 7, 5, itemTaux)
            #itemvalue3 = QtGui.QTableWidgetItem(str(row["valeur_location_ha"]))


            #self.ui.tableWidgetIFPBSurface.setItem(i - 1, 3, itemvalue3)
        #Utils.setTableWidgetColumnReadOnly(self.ui.tableWidgetIFPBSurface, 1)
        #Utils.setTableWidgetColumnReadOnly(self.ui.tableWidgetIFPBSurface, 2)
        Utils.resizeTableWidgetColumn(self.ui.tableWidgetIFTv_venale, [2], 100)
        Utils.resizeTableWidgetColumn(self.ui.tableWidgetIFPBv_venale, [2, 3], 200)

    def saveVenale(self):
        for i in range(0, self.ui.tabWidget.count()):
            if i == 0:
                for i in range(0, 6):
                    idcategorie = Utils.getTableWidgetCellIntvalue(self.ui.tableWidgetIFTv_venale, i, 0)
                    label = Utils.getTableWidgetCellStrValue(self.ui.tableWidgetIFTv_venale, i, 1)
                    value = Utils.getTableWidgetCellIntvalue(self.ui.tableWidgetIFTv_venale, i, 2)
                    taux = Utils.getTableWidgetCellFloatValue(self.ui.tableWidgetIFTv_venale, i, 4)
                    #value2 = Utils.getTableWidgetCellIntvalue(self.ui.tableWidgetIFPBSurface, i, 3)
                    unite = self.getComboVal("comboBoxIFTV_venaleUniteC", str(i+1))
                    if idcategorie > 0:
                        sql = """UPDATE categorie SET libellecategorie=%s, v_venale=%s, typeimposition = %s, u_venale = %s, taux = %s
                        WHERE idcategorie = %s"""
                        values = [label, value, 'ift',unite, taux, idcategorie]
                    else:
                        sql = """INSERT INTO categorie(idcategorie,libellecategorie,typeimposition,v_venale, u_venale,taux)
                        VALUES(%s,%s,'ift',%s,%s, %s)"""
                        values = [i + 1, label, value, unite]
                    cursor = self.connection.cursor()
                    try:
                        cursor.execute(sql, values)
                        self.connection.commit()
                    except Exception as e:
                        print(e)
                        self.connection.rollback()
                    cursor.close()
            if i == 1:
                j = 0
                for i in range(6, 12):
                    idcategorie = 0
                    if self.exists("categorie", "idcategorie", i+1):
                        idcategorie = i + 1
                    #idcategorie = Utils.getTableWidgetCellIntvalue(self.ui.tableWidgetIFPBSurface, j, 0)

                    label = Utils.getTableWidgetCellStrValue(self.ui.tableWidgetIFPBv_venale, j, 1)
                    value = Utils.getTableWidgetCellIntvalue(self.ui.tableWidgetIFPBv_venale, j, 2)
                    value2 = Utils.getTableWidgetCellIntvalue(self.ui.tableWidgetIFPBv_venale, j, 3)
                    taux = Utils.getTableWidgetCellFloatValue(self.ui.tableWidgetIFPBv_venale, j, 5)
                    j = j + 1
                    unite = self.getComboVal("comboBoxIFPBV_venaleUniteC", str(j))
                    if idcategorie > 0:
                        sql = """UPDATE categorie SET libellecategorie=%s, v_venale=%s, typeimposition = %s, u_venale = %s, taux = %s
                        WHERE idcategorie = %s"""
                        values = [label, value, 'ifpb',unite, taux, idcategorie]
                    else:
                        sql = """INSERT INTO categorie(idcategorie,libellecategorie,typeimposition,v_venale, u_venale, taux)
                        VALUES(%s,%s,'ifpb',%s,%s,%s)"""
                        values = [i + 1, label, value, unite, taux]
                    cursor = self.connection.cursor()
                    try:
                        cursor.execute(sql, values)
                        self.connection.commit()
                    except Exception as e:
                        print(e)
                        self.connection.rollback()
                    cursor.close()

    def removeEltFromCombo(self, basename, classename, toremove):

        name = basename + classename
        comBos = self.ui.tabWidget.findChildren(QtGui.QComboBox, name)

        for comBo in comBos:
            #print comBo.objectName()
            try:
                comBo.removeItem(comBo.findText(toremove))

            except Exception as err:
                print err

    def updateIFTVenale(self, item):
        '''print "******call of updateIFTVenale*****"'''
        val = Utils.getTableWidgetCellStrValue(self.ui.tableWidgetIFTSurface, item.row(), 1)
        '''print val'''
        item2 = QTableWidgetItem(str(val))
        self.ui.tableWidgetIFTv_venale.setItem( item.row(),1, item2)

    def updateIFPBVenale(self, item):
        val = Utils.getTableWidgetCellStrValue(self.ui.tableWidgetIFPBSurface, item.row(), 1)
        item2 = QTableWidgetItem(str(val))
        self.ui.tableWidgetIFPBv_venale.setItem( item.row(),1, item2)

    def initMasks(self):
        validatorNum = QRegExpValidator(globalvars.regexpNum)
        for i in range(1,7):
            for u in range(5):
                namevalift = "lineEditIFTVal" + str(i) + str(self.classeRanges[u])
                namedebift = "lineEditDebutIFTC" + str(i) + str(self.classeRanges[u])
                namefinift = "lineEditFinIFTC"  + str(i) + str(self.classeRanges[u])
                namevalifpb = "lineEditIFTVal" + str(i) + str(self.classeRanges[u]) + "_2"
                namedebifpb = "lineEditDebutIFPBC" + str(i) + str(self.classeRanges[u])
                namefinifpb = "lineEditFinIFPBC"  + str(i) + str(self.classeRanges[u])
                lineEditvalifpb = self.ui.tabWidget.findChildren(QtGui.QLineEdit, namevalifpb)
                lineEditdebifpb = self.ui.tabWidget.findChildren(QtGui.QLineEdit, namedebifpb)
                lineEditfinifpb = self.ui.tabWidget.findChildren(QtGui.QLineEdit, namefinifpb)
                lineEditvalift = self.ui.tabWidget.findChildren(QtGui.QLineEdit, namevalift)
                lineEditdebift = self.ui.tabWidget.findChildren(QtGui.QLineEdit, namedebift)
                lineEditfinift = self.ui.tabWidget.findChildren(QtGui.QLineEdit, namefinift)
                for lineEdit in lineEditvalift:
                    lineEdit.setValidator(validatorNum)
                for lineEdit in lineEditdebift:
                    lineEdit.setValidator(validatorNum)
                for lineEdit in lineEditfinift:
                    lineEdit.setValidator(validatorNum)
                for lineEdit in lineEditvalifpb:
                    lineEdit.setValidator(validatorNum)
                for lineEdit in lineEditdebifpb:
                    lineEdit.setValidator(validatorNum)
                for lineEdit in lineEditfinifpb:
                    lineEdit.setValidator(validatorNum)

