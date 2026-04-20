# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
import time
import datetime, globalvars
import datetime
from datetime import date
from .proprioMutation import Ui_Dialog


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


class proprioMutation(QtGui.QDialog):
    def __init__(self,parent):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.parent = parent
        self.details = self.parent.details
        self.id_projet = self.parent.id_projet
        self.connection = self.parent.connection
        self.idacte = self.parent.idActe
        self.CF = self.parent.numCf
        self.Parcelled = self.parent.idGeom
        self.idcertificat = self.parent.idCertificat
        self.typeOperation = 0
        self.proprioCF = []
        self.Mutation = []
        self.decedee = []
        self.personne = []
#       print self.parent.txt
        self.ui.setupUi(self)
        self.idCF = 0

        self.typeOp = self.parent.typeOp
        self.idActe = self.parent.idActe
        self.ui.details.setVisible(True)
        self.ui.details.clicked.connect(self.showDetail)
        self.ui.detailsDecedee.setVisible(False)
        self.ui.DetailHeritier.setVisible(False)
        #self.typeOperation ""
        from Certificat.GestionProprietaireRun import GestionProprietaireRun
        self.proprio = GestionProprietaireRun(self.connection)
        self.proprio.ui.radioButtonPersMorale.hide()
        self.initActions()

    def showDetail(self):

        if self.idCF == 0 :
            QtGui.QMessageBox.information(self, u"Données ", u"Veuillez selectionner la personne detenteur")
        else :
            from Personnes.PersonnePhysiqueRun import PersonnePhysiqueRun
            self.p = PersonnePhysiqueRun(self.connection,int(self.idCF))
            self.p.exec_()

    def detailsActes(self):
        if len(self.details) == 0 :
            print "do not nothing"
        else :
            print " SELF.DETAILS "
            print self.details
            details = self.details

            self.ui.lineEditNumActe.setText(details[1])
            dateActe = details[2].isoformat()
            year, month, day = details[2].isoformat().split("-")
            dateActe = date(int(year), int(month), int(day))
            self.ui.dateEditActe.setDate(dateActe)
            self.ui.lineEditNumActeNotoriete.setText(details[3])

            dateActeNotoriere = details[4].isoformat()
            year, month, day = details[4].isoformat().split("-")
            dateActeNotoriere = date(int(year), int(month), int(day))
            self.ui.dateEditActeNotoriete.setDate(dateActeNotoriere)


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
            item.setText(_translate("", str(data[i]), None))
            table.setItem(rowPosition, i, item)

    def addDemandeurs(self):
        self.nom = self.ui.nomLineEdit.text()
        self.prenom = self.ui.prenomLineEdit.text()
        cursor = self.connection.cursor()
        self.dtemp = []
        if ( (str(self.nom) != "") & (str(self.prenom) != "")) :
            print "dqdqs"
            self.dtemp.append(str(self.nom))
            self.dtemp.append(str(self.prenom))
            data = (self.nom, self.prenom)
            self.addValueTable(data)
        self.ui.nomLineEdit.setText("")
        self.ui.prenomLineEdit.setText("")
        self.close()

    def initActions(self):
        i = 0
        n = len(self.CF)
        cursor = self.connection.cursor()
        while (i < n) :
            #add numCF
            #self.proprioCF.append(self.CF[i])
            #add Type Personne
            cursor.execute("SELECT *  FROM certificat where numerocertificat =%s ", [str(self.CF[i])])
            rs = cursor.fetchone()
            print  "RS cf"
            print rs
            #idCf = rs[1].split('-')
            #idgeom = idCf[2]  # idparcelle

            idcf = rs[8]
            cursor.execute("SELECT *  FROM parcelle_d where idcertificat =%s ", [int(idcf)])
            row = cursor.fetchone()
            idgeom = row[0]  # idparcelle

            cursor.execute("SELECT * from personne ph" 
                             " INNER  JOIN proprietaireparcelle phd ON  phd.idpersonne = ph.idpersonne "
                             " INNER  JOIN parcelle_d pc ON  phd.idparcelle = pc.gid "
                             " WHERE pc.gid = %s AND pc.idcertificat = %s",
                             [int(idgeom),int(rs[8])])
            rw = cursor.fetchall()
            if rw is not None:
                for r in rw:
                    if(len(r) >= 1 ):
                        typePersonne = "Personne physique"
                        self.proprioCF.append(self.CF[i])
                        self.proprioCF.append(typePersonne)
                        self.proprioCF.append(r[1])
                        self.proprioCF.append(r[2])
                        self.proprioCF.append(r[0])
                        self.proprioCF.append(rs[8])

                    else :
                        typePersonne = "Personne Morale"

                    self.addValueTable(self.proprioCF)
                    print ('proprio CF')
                    print (self.proprioCF)
                    self.Mutation.append(self.proprioCF)
                    self.proprioCF = []

            i = i + 1
        print " self.proprioCF "
        print self.proprioCF
        self.addValueTable(self.proprioCF)
        self.ui.tableWidget.setSelectionBehavior(1)
        self.ui.tableWidget.cellClicked.connect(self.cellSelected)
        self.ui.AjouterHeritier.clicked.connect(self.ajouterHeritiers)
        self.ui.decedee.clicked.connect(self.Decedee)
        self.ui.Enregistrer.clicked.connect(self.saveAll)
        self.proprio.listePersonne.ui.btnSelectionner.clicked.connect(self.getIdPersonnePhysique)

    def getIdPersonnePhysique(self):
        print " XY in"
        from qgis.core import *
        from qgis.gui import *
        from PyQt4.QtGui import *
        from PyQt4.QtCore import *
        from qgis.gui import *
        print self.proprio.listePersonne.idpersonne
        self.personne.append(self.proprio.listePersonne.idpersonne)

        i = 0
        cursor = self.connection.cursor()
        cursor.execute("SELECT p.idpersonne, p.nompersonne, p.prenompersonne, p.numcipersonne,p.adressepersonne,p.sexepersonne "
                         "FROM personne p "
                         "WHERE p.idpersonne = %s", (self.proprio.listePersonne.idpersonne,))

        #acursor.execute("SELECT p.idpersonne , p.nompersonne, p.prenompersonne"
        #                "FROM personnephysique p "
        #                "WHERE p.idpersonne = %s", (self.proprio.listePersonne.idpersonne,))
        results = cursor.fetchone()
        rowPosition = self.ui.tableWidget_3.rowCount()
        self.ui.tableWidget_3.insertRow(rowPosition)

        j = 1
        while j < len(results):
            self.ui.tableWidget_3.setItem(rowPosition, j - 1, QTableWidgetItem(unicode(results[j])))
            j = j + 1
        i = i + 1
        self.proprio.listePersonne.close()
        self.proprio.close()

        print "XY out"

    def closeAndLoadPersonne(self):
        print "text"

    def cellSelected(self, row):
        #ID = self.gids[row]
        ID = self.ui.tableWidget.item(row, 4).text()
        self.decedee.append(self.ui.tableWidget.item(row,0).text())
        self.decedee.append(self.ui.tableWidget.item(row, 1).text())
        self.decedee.append(self.ui.tableWidget.item(row, 2).text())
        self.decedee.append(self.ui.tableWidget.item(row, 3).text())
        self.decedee.append(self.ui.tableWidget.item(row, 4).text())
        self.idCF = int(ID)

    def ajouterHeritiers(self):
        from Certificat.GestionProprietaireRun import GestionProprietaireRun
        GP = GestionProprietaireRun(self.connection)
        #from .GestionProprietaireRun import GestionProprietaireRun
        #self.proprio = GestionProprietaireRun(self.connection)
        self.proprio.exec_()

    def Decedee(self):
        from PyQt4 import QtCore, QtGui, Qt
        from PyQt4.QtCore import *
        from PyQt4.QtGui import *
#        from qgis.core import *
#        from qgis.gui import *
        if self.idCF == 0 :
            QtGui.QMessageBox.information(self, u"Données non séléctionnées",
                                          u"Veuillez au moins sélécionner une ligne")
            return
        else :
            print "self.IdActeDeces IN"
            reply = QMessageBox.question(self.ui.decedee, "Confirm", u"Voulez-vous ajouter cette personne dans la liste des personnes décédées?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                print "remove "
                self.addValueTable(self.decedee,1)
                self.decedee = []
            else :
                print " do not nothing"
    def enregistrer(self):
        print "enregistrer"
        if not self.check():
            return

        self.save()
        self.accept()

    def check(self):
        if self.ui.lineEditNumActe.text() == "":
            QtGui.QMessageBox.warning(self, "FIPLOF", "Veuillez remplir ce champ")
            self.ui.lineEditNumActe.setFocus(Qt.Qt.OtherFocusReason)
            return False
        if self.ui.dateEditActe.text() == "":
            QtGui.QMessageBox.warning(self, "FIPLOF", "Veuillez remplir ce champ")
            self.ui.dateEditActe.setFocus(Qt.Qt.OtherFocusReason)
            return False
        if self.ui.lineEditNumActeNotoriete.text() == "":
            QtGui.QMessageBox.warning(self, "FIPLOF", "Veuillez remplir ce champ")
            self.ui.lineEditNumActeNotoriete.setFocus(Qt.Qt.OtherFocusReason)
            return False
        if self.ui.dateEditActeNotoriete.text() == "":
            QtGui.QMessageBox.warning(self, "FIPLOF", "Veuillez remplir ce champ")
            self.ui.dateEditActeNotoriete.setFocus(Qt.Qt.OtherFocusReason)
            return False

        return True

    def saveAll(self):
        print "save all"
        self.typeOp = self.parent.typeOp
        lance = int(1)

        #add into operationsub table
        cursor = self.connection.cursor()
        exe = cursor.execute("INSERT INTO operationsub (typeacte,idacte) VALUES (%s,%s) RETURNING id ",
                             (self.typeOp, self.idActe))
        self.connection.commit()
        id = cursor.fetchone()
        if len(id) >= 1 :
            QtGui.QMessageBox.information(self, u"Données ", u"Données sauvegardées")
            cursor = self.connection.cursor()
            if self.typeOp  == 0 :
                exe = cursor.execute(
                    "UPDATE actedeces set lance = (%s) WHERE idactedeces = %s returning idactedeces",
                    (lance, int(self.idActe)))
                self.connection.commit()



        #update  propretaire CF
        #self.personne
        #self.CF
        n = len(self.CF)
        cursor = self.connection.cursor()
        i = j = 0

        m = len(self.personne)
        try :
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
                cursor.execute("delete from proprietaireparcelle WHERE idparcelle=%s", [int(idgeom)])
                #representant = True
                while (j < m):
                    if j == 0:
                        representant = True
                    else:
                        representant = False
                    #cursor.execute("delete from proprietaireparcelle_d WHERE idparcelle=%s", [int(idgeom)])
                    #self.connection.commit()
                    #cursor.execute("UPDATE proprietaireparcelle_d SET idpersonne=(%s) WHERE idparcelle = (%s)",(self.personne[j], idgeom))
                    try:
                        exe = cursor.execute("INSERT INTO proprietaireparcelle (idparcelle,idpersonne,representant)" \
                                         " VALUES (%s,%s,%s) RETURNING idparcelle ", (idgeom,self.personne[j],representant))
                        self.connection.commit()
                    except StandardError as e:
                        print(e)
                        self.connection.rollback()
                    j = j + 1
                i = i  + 1
            self.close()
        except Exception as e:
            print(e)
    def save(self):

        import time
        import datetime
        sql = "INSERT INTO actedeces" \
              "(numeroactedeces, dateactedeces,numeroactenotoriete,dateactenotoriete,idprojet) " \
              "values" \
              "(%s, %s, %s, %s, %s)"

        numActe = int(self.ui.lineEditNumActe.text())
        dateActe = self.ui.dateEditActe.text()
        dateActes = dateActe.split('/')
        dateActess = datetime.date(int(dateActes[2]), int(dateActes[1]), int(dateActes[0]))
        numActeNotoriete = int(self.ui.lineEditNumActeNotoriete.text())

        dateActeNote = self.ui.dateEditActeNotoriete.text()
        dateActeNotes = dateActeNote.split('/')
        dateActeNotess = datetime.date(int(dateActeNotes[2]), int(dateActeNotes[1]), int(dateActeNotes[0]))

        idprojet = int(self.id_projet)

        # params = (numActe, dateEnreg,nomOfficier,valeur,nombreOperation,idprojet)
        params = (numActe, dateActess, numActeNotoriete, dateActeNotess, idprojet)
        # if self.id:
        #    sql = "UPDATE hameau SET nomhameau=%s, codehameau=%s ,idfokontany=%s " \
        #          " WHERE idhameau=%s"
        #    params = params + (self.id,)
        cursor = self.connection.cursor()
        try:
            print
            "try in"
            cursor.execute(sql, params)
            print
            "try out"
            self.connection.commit()
            self.parent.showAll()
        except Exception as e:
            print
            e
            self.connection.rollback()
        cursor.close()

