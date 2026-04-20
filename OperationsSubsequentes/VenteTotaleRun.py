# -*- coding: utf-8 -*-
import os
import sys
import os
import os.path
from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from .VenteTotal import Ui_Dialog
import globalvars
import psycopg2


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class VenteTotaleRun(QtGui.QDialog):
    def __init__(self,parent, indivision = False):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.parent = parent
        self.row = -1
        self.title = self.parent.title
        self.typeOp = self.parent.typeOp
        self.id_projet = self.parent.id_projet
        self.connection = self.parent.connection
        self.acte = self.parent.acte
        self.indivision = indivision

        self.details = self.parent.details
        self.CF = self.parent.numCf
        self.Parcelled = self.parent.idGeom
        self.idcertificat = self.parent.idCertificat
        self.proprioCF = []
        self.personne = []
        self.personneMorale = []
        self.idCF = 0
        self.idPersonne = 0
        self.setWindowTitle(self.title)
        self.typeOp = self.parent.typeOp
        self.idActe = self.parent.idActe

        self.vente = []

        #self.cur = self.parent.connection.cursor()
        self.ui.setupUi(self)
        self.ui.details.setVisible(True)
        self.ui.details.setVisible(True)
        self.ui.details.clicked.connect(self.showDetail)
        self.ui.details0.setVisible(False)
        #self.ui.detailsDecedee.setVisible(False)
        #self.ui.DetailHeritier.setVisible(False)

        from Certificat.GestionProprietaireRun import GestionProprietaireRun
        self.proprio = GestionProprietaireRun(self.connection)

        if self.indivision is True:
            self.proprio.ui.radioButtonPersMorale.hide()
        else:
            self.proprio.ui.radioButtonPersMorale.show()

        from Certificat.ListePersonnePqueRun import ListePersonnePqueRun
        self.pPhysiqueRun = ListePersonnePqueRun(self.connection)


        self.initActions()


    def showDetail(self):
        if self.idPersonne == 0 :
            QtGui.QMessageBox.information(self, u"Données ", u"Veuillez selectionner la personne detenteur")
        else :
            from PersonnePhysiqueRun import PersonnePhysiqueRun
            self.p = PersonnePhysiqueRun(self.connection,int(self.idPersonne))
            self.p.exec_()
    def initActions(self):

        print "ident"
        i = 0
        n = len(self.CF)

        cursor = self.connection.cursor()
        while (i < n) :
            #add numCF
            #self.proprioCF.append(self.CF[i])

            #add Type Personne
            cursor.execute("SELECT *  FROM certificat where numerocertificat =%s ", [str(self.CF[i])])
            rs = cursor.fetchone()

            idcf = rs[8]
            cursor.execute("SELECT *  FROM parcelle_d where idcertificat =%s ", [int(idcf)])
            row = cursor.fetchone()
            print  "RS cf"
            print rs

            #idCf = rs[1].split('-')
            idgeom = row[0]  # idparcelle

            cursor.execute("SELECT * from personne ph" 
                             " INNER  JOIN proprietaireparcelle phd ON  phd.idpersonne = ph.idpersonne "
                             " INNER  JOIN parcelle_d pc ON  phd.idparcelle = pc.gid "
                             " WHERE pc.gid = %s AND pc.idcertificat = %s",
                             [int(idgeom),int(rs[8])])
            rw = cursor.fetchall()

            cursor.execute("SELECT * from personnemorale pm"
                           " INNER  JOIN personnemoraleparcelle_d phd ON  phd.idpersonne = pm.idpersonnemorale "
                           " INNER  JOIN parcelle_d pc ON  phd.idparcelle = pc.gid "
                           " WHERE pc.gid = %s AND pc.idcertificat = %s",
                           [int(idgeom), int(rs[8])])
            rx = cursor.fetchall()
            print ("***************RX----------" + str(rx))
            if len(rw)  >= 1 :
                for  r in rw:
                    self.proprioCF.append(self.CF[i])
                    if(len(r) >= 1 ):
                        typePersonne = "Personne physique"
                        self.proprioCF.append(typePersonne)
                        self.proprioCF.append(r[1])
                        self.proprioCF.append(r[2])
                        self.proprioCF.append(rs[8])
                        self.proprioCF.append(r[0])
                        #self.addValueTable(self.proprioCF)
                        #self.proprioCF = []
            else:
                if len(rx) >= 1:
                    for b in rx:
                        self.proprioCF.append(self.CF[i])
                        print ("*****tompony morale****" + str(b))
                        if(len(b) >= 1):
                            typePersonne = "Personne morale"
                            self.proprioCF.append(typePersonne)
                            self.proprioCF.append(b[1])
                            self.proprioCF.append(b[3])
                            self.proprioCF.append(rs[8])
                            self.proprioCF.append(b[6])
                            #self.addValueTable(self.proprioCF)
                            #self.proprioCF = []


            i = i + 1
        print " self.proprioCF "
        print self.proprioCF
        self.addValueTable(self.proprioCF)
        self.ui.tableWidget.setSelectionBehavior(1)
        self.ui.tableWidget.cellClicked.connect(self.cellSelected)
        self.ui.tableWidget_2.cellClicked.connect(self.cellSelected1)
        self.ui.ajouter.clicked.connect(self.ajoutProprio)
        self.proprio.listePersonne.ui.btnSelectionner.clicked.connect(self.getIdPersonnePhysique)
        self.proprio.listePersonneMorale.ui.pushButton_5.clicked.connect(self.getIdPersonneMorale)
        self.ui.details.clicked.connect(self.detailsPersonne)
        self.ui.enlever.clicked.connect(self.deleteRow)
        self.ui.Enregistrer.clicked.connect(self.saveAll)
        #self.ui.decedee.clicked.connect(self.Decedee)


    def saveAll(self):
        print "save all"
        #add into operationsub table
        lance = int(1)
        cursor = self.connection.cursor()
        exe = cursor.execute("INSERT INTO operationsub (typeacte,idacte) VALUES (%s,%s) RETURNING id ",
                             (self.typeOp, self.idActe))
        self.connection.commit()
        id = cursor.fetchone()
        if len(id) >= 1 :
            QtGui.QMessageBox.information(self, u"Données ", u"Données sauvegardées")
            if self.typeOp == 1:
                if self.acte == 'public' :

                    exe = cursor.execute(
                        "UPDATE actepublic set lance = (%s) WHERE idactepublic = %s returning idactepublic",
                        (lance, int(self.idActe)))
                    self.connection.commit()


                if self.acte == 'privee' :

                    exe = cursor.execute(
                        "UPDATE acteprive set lance = (%s) WHERE idacteprive = %s returning idacteprive",
                        (lance, int(self.idActe)))
                    self.connection.commit()
        #update  propretaire CF
        #self.personne
        #self.CF
        idcf = 0
        n = len(self.CF)
        cursor = self.connection.cursor()
        i = 0
        m = len(self.personne)
        k = len(self.personneMorale)
        try :
            #representant = True
            while (i < n):
                # add Type Personne
                cursor.execute("SELECT *  FROM certificat where numerocertificat =%s ", [str(self.CF[i])])
                rs = cursor.fetchone()
                #idCf = rs[1].split('-')
                #idgeom = idCf[2]  #
                idcf = rs[8]
                cursor.execute("SELECT *  FROM parcelle_d where idcertificat =%s ", [int(idcf)])
                row = cursor.fetchone()
                idgeom = row[0]
                if self.indivision == False:
                    try:
                        cursor.execute("delete from proprietaireparcelle WHERE idparcelle=%s", [int(idgeom)])
                    except Exception as err:
                        print ("erreur suppression proprietaire dans vente totale")
                        print (err)
                    try:
                        cursor.execute("delete from personnemoraleparcelle_d WHERE idparcelle=%s", [int(idgeom)])
                    except Exception as err:
                        print ("erreur suppression personnemoraleparcelle_d dans vente totale")
                        print (err)
                j = 0
                if m > 0:
                    while (j < m):
                        if j == 0:
                            representant = True
                        else:
                            representant = False
                        #cursor.execute("delete from proprietaireparcelle_d WHERE idparcelle=%s", [int(idgeom)])
                        #self.connection.commit()
                        #cursor.execute("UPDATE proprietaireparcelle_d SET idpersonne=(%s) WHERE idparcelle = (%s)",(self.personne[j], idgeom))
                        if self.indivision == False:
                            try:
                                exe = cursor.execute("INSERT INTO proprietaireparcelle (idparcelle,idpersonne,representant)" \
                                                 " VALUES (%s,%s,%s) RETURNING idparcelle ", (idgeom,self.personne[j],representant))
                                self.connection.commit()
                            except StandardError as e:
                                print(e)
                                self.connection.rollback()

                            avdm = []

                            try:
                                exe = cursor.execute("SELECT * FROM avoir_demande WHERE idparcelle = %s ", (idgeom,))
                                avdm = cursor.fetchall()
                            except StandardError as e:
                                print(e)
                                self.connection.rollback()
                            if len(avdm) == 0:
                                try:
                                    exe = cursor.execute(
                                        "INSERT INTO avoir_demande (idparcelle,idpersonne, representant)" \
                                        " VALUES (%s,%s, %s) RETURNING idparcelle ",
                                        (idgeom, self.personne[j], representant))
                                    self.connection.commit()
                                except StandardError as e:
                                    print(e)
                                    self.connection.rollback()

                        else: #INDIVISION IS TRUE
                            try:
                                exe = cursor.execute("INSERT INTO proprietaireparcelle (idparcelle,idpersonne,representant)" \
                                                 " VALUES (%s,%s,%s) RETURNING idparcelle ", (idgeom, self.personne[j], False))
                                self.connection.commit()
                            except StandardError as e:
                                print(e)
                                self.connection.rollback()

                        j = j + 1
                        """   
                        try:
                            cursor.execute("UPDATE proprietaireparcelle SET idpersonne=(%s) , representant=(%s) WHERE idparcelle = (%s)",
                                   (self.proprio.listePersonne.idpersonne,representant, idgeom))
                            self.connection.commit()
                        except StandardError as e:
                            print(e)
                            self.connection.rollback()
                        """

                else:
                    if k > 0:
                        while j < k:
                            try:
                                exe = cursor.execute("INSERT INTO personnemoraleparcelle_d (idparcelle,idpersonne)" \
                                                     " VALUES (%s,%s) RETURNING idparcelle ",
                                                     (idgeom, self.personneMorale[j]))
                                self.connection.commit()
                            except Exception as err:
                                print("Erreur insertion proprio morale " + str(err))
                                self.connection.rollback()

                            j = j + 1
                i = i + 1

        except Exception as e:
            print(e)
        from Projet.journalRunn import journal
        journal = journal(self.connection)
        journal.inserToJournal(globalvars.id_user, idcf, u"Certificat",
                               u"Vente Total")
        self.close()
    def deleteRow(self):
        if self.row == -1:
            QtGui.QMessageBox.information(self, u"Données non séléctionnées",
                                          u"Veuillez au moins sélécionner une ligne")
            return
        else :
            self.ui.tableWidget_2.removeRow(self.row)
    def detailsPersonne(self):
        print 'selle'
        try:
            self.pPhysiqueRun.ouvrirPersonnePque()
            #result = self.pPhysiqueRun.personne.exec_()
        except StandardError as e:
            print e

    def getIdPersonneMorale(self):
        self.personneMorale.append(self.proprio.listePersonneMorale.idpersonne)
        print ("*****personnes morales***** " + str(self.proprio.listePersonneMorale.idpersonne))

        i = 0
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT p.idpersonnemorale, p.denomination, p.siege, tpm.type "
                       "FROM personnemorale p INNER JOIN typepersonnemorale tpm ON p.idtype = tpm.idtype "
                       "WHERE p.idpersonnemorale = %s", (self.proprio.listePersonneMorale.idpersonne,))
            results = cursor.fetchone()


            rowPosition = self.ui.tableWidget_2.rowCount()
            self.ui.tableWidget_2.insertRow(rowPosition)
            j = 1
            while j < len(results):
                self.ui.tableWidget_2.setItem(rowPosition, j - 1, QTableWidgetItem(unicode(results[j])))
                j = j + 1
            i = i + 1

        except Exception as err:
            print ("Erreur get id personne morale vente totale " + str(err))
            self.connection.rollback()

        # acursor.execute("SELECT p.idpersonne , p.nompersonne, p.prenompersonne"
        #                "FROM personnephysique p "
        #                "WHERE p.idpersonne = %s", (self.proprio.listePersonne.idpersonne,))

        self.proprio.listePersonneMorale.close()
        self.proprio.close()

    def getIdPersonnePhysique(self):
        print " XY in"

        print
        self.proprio.listePersonne.idpersonne
        self.personne.append(self.proprio.listePersonne.idpersonne)

        i = 0
        cursor = self.connection.cursor()

        cursor.execute("SELECT p.idpersonne, p.nompersonne, p.prenompersonne, p.numcipersonne "
                       "FROM personne p "
                       "WHERE p.idpersonne = %s", (self.proprio.listePersonne.idpersonne,))

        # acursor.execute("SELECT p.idpersonne , p.nompersonne, p.prenompersonne"
        #                "FROM personnephysique p "
        #                "WHERE p.idpersonne = %s", (self.proprio.listePersonne.idpersonne,))
        results = cursor.fetchone()
        rowPosition = self.ui.tableWidget_2.rowCount()
        self.ui.tableWidget_2.insertRow(rowPosition)
        j = 1
        while j < len(results):
            self.ui.tableWidget_2.setItem(rowPosition, j - 1, QTableWidgetItem(unicode(results[j])))
            j = j + 1
        i = i + 1
        self.proprio.listePersonne.close()
        self.proprio.close()


    def addValueTable(self,data,table = 0):
        columns = len(data)

        if (table == 0) :
            table = self.ui.tableWidget
        else :
            table = self.ui.tableWidget_2

        rowPosition = table.rowCount()
        #self.tbDemande.setColumnCount(columns)

        table.insertRow(rowPosition)
        for i in range(len(data)):
            item = QtGui.QTableWidgetItem()
            item.setText(_translate("", _fromUtf8(str(data[i])), None))
            table.setItem(rowPosition, i, item)

    def cellSelected1(self, row):
        # ID = self.gids[row]
        #ID = self.ui.tableWidget_2.item(row, 4).text()
        self.row = row

    def cellSelected(self, row):
        #ID = self.gids[row]
        ID = self.ui.tableWidget.item(row, 4).text()
        idPersonne = self.ui.tableWidget.item(row, 5).text()
        self.vente.append(self.ui.tableWidget.item(row,0).text())
        self.vente.append(self.ui.tableWidget.item(row, 1).text())
        self.vente.append(self.ui.tableWidget.item(row, 2).text())
        self.vente.append(self.ui.tableWidget.item(row, 3).text())
        self.vente.append(self.ui.tableWidget.item(row, 4).text())

        self.idCF = int(ID)
        self.idPersonne = int(self.ui.tableWidget.item(row, 5).text())
        self.pPhysiqueRun.idpersonne = int(self.ui.tableWidget.item(row, 5).text())

    def PersonneDetails(self):
        from Personnes.PersonnePhysiqueRun import PersonnePhysiqueRun
        GP = PersonnePhysiqueRun(self.parent)
        GP.exec_()

    def ajoutProprio(self):
        #from Certificat.GestionProprietaireRun import GestionProprietaireRun
        #GP = GestionProprietaireRun(self.connection)
        self.proprio.exec_()

    def enregistrer(self):
        print "enregistrer"
        if not self.check():
            return

        self.save()
        self.accept()


    def check(self):
        print "demande"


    def save(self):

        import time
        import datetime
        try:
            print "try in"
        except Exception as e:
            print e





