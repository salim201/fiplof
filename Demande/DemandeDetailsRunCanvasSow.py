import os
import sys
import os
import os.path
import psycopg2
import qgis
from PyQt4 import QtCore, QtGui
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtCore import QFileInfo
import time
import datetime, globalvars
import datetime
from datetime import date
import qgis
import psycopg2
from qgis.core import *
from qgis.gui import *
import os
#from qgis.gui import QgisInterface
import psycopg2
import psycopg2.extras
from Utils import Utils
#import  processing

import sys

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

from DemandeDetails import Ui_DemandeDetailsForm

class DemandeDetailsRun(QtGui.QDialog):

  def __init__(self,parent):
    QtGui.QDialog.__init__(self)
    # Set up the user interface from Designer.

    self.parent = parent
    self.ui = Ui_DemandeDetailsForm()
    self.ui.setupUi(self)
    self.tabWigdets = self.ui.tabWidgetOppositionDemande
    self.tbDemande = self.ui.tableDemande
    self.tbOpposition = self.ui.tableOpposition
    self.ui.Rejeter.setVisible(False)

    #        self.dialog = dialog
    os.chdir(self.resolve(".."))
    dr = os.getcwd()
    self.CreationDemande = ""

    sys.path.append(os.path.dirname(dr))
    from Configuration import DbConfig
    #        from Configuration import DbConfig
    self.db_config = DbConfig.DbConfig()
    self.coddistrict = 0
    self.codecommune = 0
    self.idfokontany = 0
    self.iddemande = 0
    self.idopposition = 0
    self.connection = ""
    self.ddDate = 0
    #        self.setModal(True)
    #self.cvs = self.parent.MainWindow.canvas
    self.autoincrementkeydemande = 0
    self.opposition = []
    self.demandeurs = []
    self.filenamepreview = ""
    self.connection = self.parent.connection
    self.cursor = self.connection.cursor()
    self.utils = Utils(self.connection)
    self.idparcelle = self.parent.idparcelle

    #self.parent.currvalDemande = parent.currvalDemande
    #self.id_projet = self.parent.id_projet

    #connection = self.parent.connection
    self.setModal(True)

    self.setModal(True)

    self.parent = parent
    print self.parent
    self.coddistrict = 0
    self.codecommune = 0
    self.edition = self.parent.stateEdition
    self.geomid = self.parent.geomid
    self.canvas = self.parent.canvas
    self.tool = self.parent.tool

    self.connection = self.parent.connection
    #self.parent.currvalDemande = parent.currvalDemande
    #self.currvalDemande = self.parent.currvalDemande
    self.iddemandeForJournal = None
    self.iddemande = 0
    self.idopposition = 0
    self.gid = self.parent.idDemande
    print "gid= " + str(self.gid)
    print "self.edition in"
    print self.edition
    print "self.edition out"
    self.filenamepreview = ""
    try:
      self.parentDlg = self.parent.dlg
    except:
      pass
    self.dlg = ""
    self.ui.dateDemandeDateEdit.setDisplayFormat("dd/MM/yyyy")
    self.ui.dateDemandeDateEdit.setDate(QDate.currentDate())
    #        self.dateDemandeLineEdit.setInputMask(_fromUtf8(""))
    self.ui.dateDemandeDateEdit.setEnabled(True)
    self.ui.dateDemandeDateEdit.setCalendarPopup(True)

    self.ui.dateReconnaissanceDateEdit.setEnabled(True)
    self.ui.dateReconnaissanceDateEdit.setCalendarPopup(True)
    self.ui.dateReconnaissanceDateEdit.setDisplayFormat("dd/MM/yyyy")
    self.ui.dateReconnaissanceDateEdit.setDate(QDate.currentDate())

    #self.ui.dateReconnaissanceDateEdit.dateChanged.connect(self.evaluateDateReconnaissance)
    validator = QtGui.QDoubleValidator()
    self.ui.coutLineEdit.setValidator(validator)
    self.ui.regionLineEdit.setReadOnly(True)
    self.ui.districtLineEdit.setReadOnly(True)
    self.ui.numeroDemandeLineEdit.setReadOnly(False)
    self.ui.numeroDemandeLineEdit.setEnabled(True)
    self.loadConsistance(self.connection)
    self.EtatChampDemande = 0
    #self.ui.fokontanyComboBox.currentIndexChanged.connect(self.fillFokontany)
    #self.generateDemandeKey()
    #self.pushButton.clicked.connect(self.callDemandeur)
    # self.dateDeReconnaissanceLineEdit.mousePressEvent.connect(self.evaluateDateReconnaissance)
    #self.pushButton_2.clicked.connect(self.callOpposition)

    print "SELF.IDPARCELLE IN"
    print self.idparcelle
    print "SELF.IDPARCELLE OUT"

    #self.filenamepreview = self.preview()
    os.chdir(self.resolve(".."))
    dr = os.getcwd()
    sys.path.append(os.path.dirname(dr))
    self.init_canvas()

    #self.ui.label.setPixmap(QtGui.QPixmap(self.filenamepreview))
    self.utils = Utils(self.connection)
    self.initActions()
    self.FetchDemandeCF()

    #if self.ui.tabWidgetOppositionDemande.
    self.currentIndex = -1


  def initActions(self):

    import globalvars
    idcommune = globalvars.id_commune
    print "----------------globalvars.id_commune----------------"
    print globalvars.id_commune
    print "--------------------globalvars.id_commune-----------"
    cursor = self.connection.cursor()
    cursor.execute("SELECT *   FROM commune  WHERE idcommune=%s", [int(idcommune)])
    dm = cursor.fetchone()
    if (len(dm) >= 1):
      iddistrict = dm[1]
      cursor.execute("SELECT *   FROM district  WHERE iddistrict=%s", [int(iddistrict)])
      dm = cursor.fetchone()
      idregion = dm[1]

    cursor.execute("SELECT nomregion  FROM region  WHERE idregion=%s", [int(idregion)])
    dm = cursor.fetchone()
    if (len(dm) >= 1):
      region = dm[0]

    cursor.execute("SELECT *  FROM district  WHERE iddistrict=%s", [int(iddistrict)])
    dm = cursor.fetchone()
    if (len(dm) >= 1):
      coddistrict = dm[2]
      self.coddistrict = coddistrict

    cursor.execute("SELECT *  FROM commune  WHERE idcommune=%s", [int(idcommune)])
    dm = cursor.fetchone()
    if (len(dm) >= 1):
      codeCommune = dm[2]
      self.codecommune = codeCommune

    if self.edition == 2:
      self.ui.BtnCreate.clicked.connect(self.updateGeometrie)
      self.ui.districtLineEdit.setEnabled(False)
      self.ui.coutLineEdit.setReadOnly(True)
      self.ui.regionLineEdit.setReadOnly(True)
      self.ui.dateDemandeDateEdit.setReadOnly(True)
      self.ui.dateReconnaissanceDateEdit.setReadOnly(True)
      self.ui.numeroDemandeLineEdit.setReadOnly(True)
      self.ui.addBtn.setEnabled(False)
      self.ui.delBtn.setEnabled(False)
      self.ui.BtnCancel.setEnabled(False)
      self.ui.communeLineEdit.setReadOnly(True)
      self.ui.fokontanyComboBox.setDisabled(True)
      self.ui.BtnCreate.setText(QtGui.QApplication.translate("CreationDemande", "Modifier la Geometrie", None, QtGui.QApplication.UnicodeUTF8))
      self.setWindowTitle(QtGui.QApplication.translate("CreationDemande", "Modification de la geometrie", None, QtGui.QApplication.UnicodeUTF8))

    if self.edition == 1:
      self.ui.BtnCreate.clicked.connect(self.updateInfos)
      self.ui.addBtn.clicked.connect(self.loadForm)
      self.ui.delBtn.clicked.connect(self.removeRow)

      validator = QtGui.QDoubleValidator()
      self.ui.coutLineEdit.setValidator(validator)
      if self.EtatChampDemande == 0 :
          print " ne pas changer numero demande "
      else :
          self.ui.fokontanyComboBox.currentIndexChanged.connect(self.fillFokontany)
      self.ui.BtnCreate.setText(QtGui.QApplication.translate("CreationDemande", "Modifier les Informations", None,QtGui.QApplication.UnicodeUTF8))
      #self.ui.pushButton_5.setText(QtGui.QApplication.translate("CreationDemande", "Annuler", None, QtGui.QApplication.UnicodeUTF8))
      self.setWindowTitle(QtGui.QApplication.translate("CreationDemande", "Modification des Informations", None, QtGui.QApplication.UnicodeUTF8))
      self.EtatChampDemande = 1
    if self.edition == 0 :
      print "ffsd"
      print " self.edition == 0 "
      self.ui.BtnCreate.setEnabled(False)
      self.ui.BtnCancel.setEnabled(False)
      self.ui.addBtn.setEnabled(False)
      self.ui.delBtn.setEnabled(False)
      self.ui.numeroDemandeLineEdit.setEnabled(True)
      self.ui.numeroDemandeLineEdit.setReadOnly(True)
      self.ui.coutLineEdit.setReadOnly(True)
      self.ui.regionLineEdit.setReadOnly(True)
      self.ui.districtLineEdit.setReadOnly(True)
      self.ui.communeLineEdit.setEnabled(True)
      self.ui.communeLineEdit.setReadOnly(True)
      self.ui.dateReconnaissanceDateEdit.setReadOnly(True)
      self.ui.dateDemandeDateEdit.setReadOnly(True)

      self.setWindowTitle(QtGui.QApplication.translate("CreationDemande", "Consultation Demande", None, QtGui.QApplication.UnicodeUTF8))

  def FetchDemandeCF(self):
    cursor = self.connection.cursor()
    cursor = self.connection.cursor()
    print " FetchDemandeCF in "
    print self.gid
    print " FetchDemandeCF out"
    cursor.execute("SELECT *   FROM demande  WHERE gid=%s", [self.gid])
    res = cursor.fetchone()
    cursor.execute("SELECT *   FROM commune  WHERE idcommune=%s", [int(res[17])])
    commune = cursor.fetchone()
    if (len(res) >= 1):
      dateDemande = res[9].isoformat()
      year, month, day = res[9].isoformat().split("-")
      dateDemande = date(int(year), int(month), int(day))
      self.ui.dateDemandeDateEdit.setDate(dateDemande)

      dateReconnaissance = res[10].isoformat()
      year, month, day = res[10].isoformat().split("-")
      dateReconnaissance = date(int(year), int(month), int(day))
      self.ui.dateReconnaissanceDateEdit.setDate(dateReconnaissance)

      self.iddemandeForJournal = res[0]  # Recuperation de l'id de la table demande
      print "res[2]"
      print str(res[2])
      self.ui.numeroDemandeLineEdit.setText(str(res[2]))
      self.iddemande = int(res[0])
      self.ui.coutLineEdit.setText(str(res[19]))
      self.ui.regionLineEdit.setText(str(res[11]))
      self.ui.districtLineEdit.setText(str(res[12]))
      self.ui.communeLineEdit.setText(str(commune[3]))
      self.loadFokontany(int(commune[0]))
      self.loadConsistance(self.connection)
      self.loadOpposition(self.connection)
      self.loadDemandeur(self.connection)
      self.ui.numeroDemandeLineEdit.setReadOnly(True)
      self.ui.coutLineEdit.setEnabled(True)
      self.ui.regionLineEdit.setReadOnly(True)
      self.ui.districtLineEdit.setReadOnly(True)
      self.ui.communeLineEdit.setReadOnly(True)

      #self.ui.communeComboBox.setReadOnly(True)

  def add_values(self, data):
      columns = len(data)
      rowPosition = self.ui.tableOpposition.rowCount()
      self.ui.tableOpposition.setColumnCount(columns)
      self.ui.tableOpposition.insertRow(rowPosition)
      for i in range(len(data)):
          item = QtGui.QTableWidgetItem()
          print
          "at add_values range"
          print
          str(data[i])
          item.setText(_translate("", str(data[i]), None))
          print
          "at add_values range out"
          self.ui.tableOpposition.setItem(rowPosition, i, item)


  def add_value(self, data):
      columns = len(data)
      rowPosition = self.ui.tableDemande.rowCount()
      self.ui.tableDemande.setColumnCount(columns)
      self.ui.tableDemande.insertRow(rowPosition)
      for i in range(len(data)):
          item = QtGui.QTableWidgetItem()
          print
          "at add_values range"
          print
          str(data[i])
          item.setText(_translate("", str(data[i]), None))
          print
          "at add_values range out"
          self.ui.tableDemande.setItem(rowPosition, i, item)

  def loadDemandeur(self,connexion):
      cursor = connexion.cursor()
      cursor.execute("SELECT * from demandeur_d  as d "
                     " INNER JOIN avoir_dmd as avd on d.iddemandeur = avd.iddemandeur "
                     " where  avd.gid =%s", [int(self.gid)])
      dm = cursor.fetchall()
      self.demandeurs = []
      if (len(dm) >= 1 ):
          demandeTmp = []
          for d in dm :
              #demandeTmp.append(d[1])
              #demandeTmp.append(d[2])
              #self.demandeurs.append(demandeTmp)
              data = (str(d[1]), str(d[2]))
              self.add_value(data)

  def loadOpposition(self,connexion):
      cursor = connexion.cursor()
      cursor.execute("SELECT * from oppositions  where gid=%s", [int(self.gid)])
      dm = cursor.fetchall()
      self.data = []
      if (len(dm) >= 1):
          OppTemp = []
          for o in dm :
              # 2018 - 05 - 09
              year, month, day = o[1].isoformat().split("-")
              dateOpposition = day + "/" + month + "/" + year

              year, month, day = o[2].isoformat().split("-")
              dateDemande = day + "/" + month + "/" + year
              data = (str(o[4]), str(o[3]), dateOpposition, dateDemande)
              try:
                  self.add_values(data)
              except Exception as e:
                  print(e)

  def loadFokontany(self, idcommune):

    cursor = self.connection.cursor()
    cursor.execute("SELECT *  FROM fokontany  WHERE idcommune=%s", [int(idcommune)])
    dm = cursor.fetchall()
    size = len(dm)
    if (size >= 1):
      district = dm[0]
      self.ui.fokontanyComboBox.clear()
      for row in dm:
        lignefkt = row[3]
        self.ui.fokontanyComboBox.addItem(_fromUtf8(row[3]), row[0])
    else:
      self.ui.fokontanyComboBox.clear()

  def updateGeometrie(self):
    # Ecriture dans le journal
    from Projet.journalRunn import journal
    journal = journal(self.connection)
    journal.inserToJournal(globalvars.id_user, self.iddemandeForJournal, u"Demande",
                           u"Edition de la geometrie d'une demande")
    # fin ecritude dans le journal
    self.close()
    try:
        print "try"
        self.canvas.setMapTool(self.tool)
        self.parent.activateChangeOngeom.setEnabled(True)
      #self.parentDlg.close()

    except Exception as e:
      pass
      print(e)
    self.parent.close()

    # self.selectionButton.setDefaultAction(self.selectionButton.sender())
    # if self.ui.actionEditing_Node_Layers.isChecked() :
    #    self.canvas.setMapTool(self.parentool)
    #    self.ui.actionEnregistrer.setEnabled(True)
    # else:
    #   self.canvas.unsetMapTool(self.tool)
    #    self.ui.actionEnregistrer.setEnabled(False)
    # self.MainWindow.canvas.refresh()

  def updateInfos(self):
    from datetime import date
    date_format = "%d/%m/%Y"
    # a = datetime.strptime(self.dateDemandeLineEdit.text(), date_format)
    # b = datetime.strptime(self.dateDeReconnaissanceLineEdit.text(), date_format)

    a = self.ui.dateDemandeDateEdit.text()
    a = a.split("/")
    a = date(int(a[2]), int(a[1]), int(a[0]))

    b = self.ui.dateReconnaissanceDateEdit.text()
    b = b.split("/")
    b = date(int(b[2]), int(b[1]), int(b[0]))

    diffdate = b - a

    self.ddDate = diffdate.days

    if self.ddDate < 15:
      QMessageBox.critical(self.ui.dateReconnaissanceDateEdit, "Erreur",
                           "La date de reconnaissance doit etre  au moins 15 jours apres")
      self.ui.dateReconnaissanceDateEdit.setFocus(Qt.Qt.OtherFocusReason)
      return

    if self.ui.coutLineEdit.text() == "":
      QMessageBox.critical(self.ui.coutLineEdit, "Erreur", "Le cout ne doit pas etre vide")
      self.ui.coutLineEdit.setFocus(Qt.Qt.OtherFocusReason)
      return

    cursor = self.connection.cursor()
    numDmd = str(self.ui.numeroDemandeLineEdit.text())
    print " num demande in"
    print numDmd
    print " num demande out"
    self.numDemande = numDmd
    dateDemande = self.ui.dateDemandeDateEdit.text()
    dtDmande = dateDemande.split('/')

    dateReconnaissance = self.ui.dateReconnaissanceDateEdit.text()
    dtReconnaissance = dateReconnaissance.split('/')

    cout = float(self.ui.coutLineEdit.text())
    region = str(self.ui.regionLineEdit.text())
    district = str(self.ui.districtLineEdit.text())
    # commune = str(self.commune.text())
    fokontany = str(self.ui.fokontanyComboBox.currentText())
    consistance = str(self.ui.consistanceComboBox.currentText())

    cursor.execute("UPDATE demande SET cout=(%s), datedemande= (%s), numdemande=(%s) , datereconnaissance=(%s) , consistance=(%s)  WHERE gid = (%s)",
                   (cout, datetime.date(int(dtDmande[2]), int(dtDmande[1]), int(dtDmande[0])),numDmd,datetime.date(int(dtReconnaissance[2]), int(dtReconnaissance[1]), int(dtReconnaissance[0])),consistance, int(self.gid)))


    cursor.execute("UPDATE parcelle_d SET numdemande=(%s) WHERE gid = (%s)", (numDmd, self.gid))
    self.connection.commit()

    #Delete opposition before updating
    cursor.execute("delete  from  oppositions WHERE gid=%s", [int(self.gid)])
    self.connection.commit()

    rowCount = self.ui.tableDemande.rowCount()
    columnCount = self.ui.tableDemande.columnCount()
    rowCountOppo = self.ui.tableOpposition.rowCount()
    # traitement des oppositions
    i = 0
    OppositionTemp = []
    if (rowCountOppo) >= 1:
        while (i <= rowCountOppo):
            j = 0
            while (j <= 3):
                item = self.ui.tableOpposition.item(i, j)
                if item == None:
                    print
                    "None"
                else:
                    print
                    item.text()
                    OppositionTemp.append(item.text())

                j = j + 1
            if len(OppositionTemp) >= 1:
                self.opposition.append(OppositionTemp)
            OppositionTemp = []
            i = i + 1

    if len(self.opposition) >= 1:
        for o in self.opposition:
            dateOpposition = o[2]
            dateOpposition = dateOpposition.split('/')
            dateOpposition = datetime.date(int(dateOpposition[2]), int(dateOpposition[1]), int(dateOpposition[0]))

            dateDemande = o[3]
            dateDemande = dateDemande.split('/')
            dateDemande = datetime.date(int(dateDemande[2]), int(dateDemande[1]), int(dateDemande[0]))

            # dateReglement = o[7]
            etatOppositions = 0
            # dateReglement = dateReglement.split('/')
            # dateReglement = datetime.date(int(dateReglement[2]), int(dateReglement[1]), int(dateReglement[0]))

            exe = cursor.execute(
                "INSERT INTO oppositions (typeopposition,description,dateopposition,datedemande,iddemande,gid)"
                " VALUES (%s,%s,%s,%s,%s,%s)",
                (str(o[1]), str(o[0]), dateOpposition, dateDemande, int(self.iddemandeForJournal), self.idparcelle))
            self.connection.commit()
    i = j = 0

    #


    # Delete Demande before updating
    try:
        cursor.execute("SELECT *   FROM avoir_dmd  WHERE gid=%s",[int(self.gid)])
        dm = cursor.fetchall()
        if (len(dm))>= 1:
            for demandeur in dm :
                cursor.execute("delete  from avoir_dmd WHERE gid=%s", [int(self.gid)])
                cursor.execute("delete  from demandeur_d WHERE iddemandeur=%s", [int(demandeur[0])])
                self.connection.commit()
    except StandardError as e:
        print e

    i = 0
    demandeurs = []
    while (i <= rowCount):
        j = 0
        while (j <= 1):
            item = self.ui.tableDemande.item(i, j)
            if item == None:
                print "None"
            else:
                print item.text()
                demandeurs.append(item.text())

            j = j + 1
        if len(demandeurs) >= 1:
            self.demandeurs.append(demandeurs)
        demandeurs = []
        i = i + 1
    print " demandeurs in"
    print self.demandeurs
    print"self.demandeurs out"

    if len(self.demandeurs) >= 1:
        try:
            for d in self.demandeurs:
                exe = cursor.execute("INSERT INTO demandeur_d (nom,prenom) VALUES (%s,%s) RETURNING iddemandeur ",
                                     (str(d[0]), str(d[1])))
                self.connection.commit()
                iddemandeur = cursor.fetchone()
                if iddemandeur[0]:
                    exe = cursor.execute("INSERT INTO avoir_dmd (iddemandeur,iddemande,gid) VALUES (%s,%s,%s)",
                                         (int(iddemandeur[0]), int(self.iddemandeForJournal), self.idparcelle))
                    self.connection.commit()
        except StandardError as e:
            print e

    # Ecriture dans le journal
    from Projet.journalRunn import journal
    journal = journal(self.connection)
    journal.inserToJournal(globalvars.id_user, self.iddemandeForJournal, u"Demande",
                           u"Edition des informations d'une demande")
    # fin ecritude dans le journal
    # self.dialog.close()

    cLayer = self.parent.current_layer
    mc = self.parent.canvas
    #        mc = qgis.utils.iface.mapCanvas()
    for layer in mc.layers():
      if layer.type() == layer.VectorLayer:
        layer.removeSelection()

    mc.refresh()
    mc.refresh()
    mc.refresh()
    mc.refresh()
    mc.refresh()
    mc.refresh()
    self.parent.showAll()
    self.close()


  def cellSelected(self,row,column):
      self.selectedRow = row
  def removeRow(self):
      print " init remove out"

      self.currentIndex = int(self.ui.tabWidgetOppositionDemande.currentIndex())
      currentRWOpp = self.ui.tableOpposition.currentRow()
      currentRWODmd = self.ui.tableDemande.currentRow()

      rowCount = self.ui.tableDemande.rowCount()
      columnCount = self.ui.tableDemande.columnCount()

      if self.currentIndex == 0:
          if currentRWOpp == -1 :
              print " impossible"
              QMessageBox.critical(self.ui.tableOpposition, "Erreur", "Veuillez entrer au moins choisir une ligne")
              return
          else :
              self.ui.tableOpposition.removeRow(self.selectedRow)
      if self.currentIndex == 1:
          if currentRWODmd == -1 :
              print "dqsd"
              QMessageBox.critical(self.ui.tableDemande, "Erreur", "Veuillez entrer au moins choisir une ligne")
              return
          else :
              self.ui.tableDemande.removeRow(self.selectedRow)


  def loadForm(self):
      print " load form "
      print " btn clicked"
      self.currentIndex = int(self.ui.tabWidgetOppositionDemande.currentIndex())
      if self.currentIndex == 0:
          from OppositionFormRun import OppositionFormRun
          numDmd = str(self.ui.numeroDemandeLineEdit.text())
          self.numDemande = numDmd
          opp = OppositionFormRun(self)
          opp.show()
          result = opp.exec_()
      if self.currentIndex == 1:
          from DemandeursFormRun import DemandeursFormRun
          numDmd = str(self.ui.numeroDemandeLineEdit.text())
          self.numDemande = numDmd
          demandeurs = DemandeursFormRun(self)
          demandeurs.show()
          result = demandeurs.exec_()

  def tabSelected(self, arg=None):
      print "changed"
      print arg
      self.currentIndex = int(arg)

  def init_canvas(self):
      style = {
          u'outline_width': u'0.3',
          u'outline_color': u'244,0,0,255',
          u'offset_unit': u'MM',
          u'color': u'227,26,28,255',
          u'outline_style': u'solid',
          u'style': u'b_diagonal',
          u'joinstyle': u'bevel',
          u'outline_width_unit': u'MM',
          u'border_width_map_unit_scale': u'0,0',
          u'offset': u'0,0',
          u'offset_map_unit_scale': u'0,0'
      }
      self.cvs = QgsMapCanvas()
      self.idparcelle;
      self.ui.horizontalLayout_2.addWidget(self.canvas)
      self.cvs.show()
      uri = QgsDataSourceURI()
      uri.setConnection(
          self.db_config.db_host,
          self.db_config.db_port,
          self.db_config.db_name,
          self.db_config.db_user,
          self.db_config.db_pass
      )
      uri.setDataSource("public", "parcelle_d", "geom", "gid=%s" % (self.idparcelle,))
      uri.setKeyColumn("gid")
      layer = QgsVectorLayer(uri.uri(), "Demande", "postgres")
      if not layer.isValid():
        return
      crs = QgsCoordinateReferenceSystem(globalvars.EPSG_SCR, QgsCoordinateReferenceSystem.EpsgCrsId)
      layer.setCrs(crs)
      symbol_layer = QgsFillSymbolV2.createSimple(style)
      layer.rendererV2().setSymbol(symbol_layer)
      QgsMapLayerRegistry.instance().addMapLayer(layer)
      self.cvs.setLayerSet([QgsMapCanvasLayer(layer)])
      self.cvs.setExtent(layer.extent())
      self.cvs.refresh()

  def callDemandeur(self):
      from CreateDemandeurCertificat import CreateDemandeurCertificat
      Demandeur = CreateDemandeurCertificat(self)
      Demandeur.show()
      result = Demandeur.exec_()

  def callOpposition(self):

      from OppositionRunn import OppositionRunn
      print
      "call opposition "
      numDmd = str(self.ui.numeroDemandeLineEdit.text())
      self.numDemande = numDmd
      opp = OppositionRunn(self)
      print
      opp
      opp.show()
      result = opp.exec_()


  def resolve(self, name, basepath=None):
      if not basepath:
          basepath = os.path.dirname(os.path.realpath(__file__))
      return os.path.join(basepath, name)


  def evaluateDateReconnaissance(self):
      print "first test of all"
      from datetime import datetime
      from datetime import date
      date_format = "%d/%m/%Y"
      # a = datetime.strptime(self.dateDemandeLineEdit.text(), date_format)
      # b = datetime.strptime(self.dateDeReconnaissanceLineEdit.text(), date_format)

      a = self.ui.dateDemandeDateEdit.text()
      print "a"
      print a
      a = a.split("/")
      print a[2]
      print a[1]
      # a = date(int(a[2]),int(a[1]),int(a[0]))

      b = self.ui.dateReconnaissanceDateEdit.text()
      b = b.split("/")
      # b = date(int(b[2]),int(b[1]),int(b[0]))



      from datetime import datetime
      date_format = "%m/%d/%Y"
      a = datetime.strptime('' + str(a[1]) + '/' + str(a[0]) + '/' + str(a[2]) + '', date_format)
      b = datetime.strptime('' + str(b[1]) + '/' + str(b[0]) + '/' + str(b[2]) + '', date_format)
      delta = b - a
      diffdate = b - a
      self.ddDate = delta.days
      if self.ddDate < 15:
          QMessageBox.critical(self.ui.dateReconnaissanceDateEdit, "Erreur",
                               "La date de reconnaissance doit etre 15 jours apres")


          # self.dateDeReconnaissanceLineEdit.setText("")
          # self.dateDeReconnaissanceLineEdit.setReadOnly(True)

  def getFokontany(self, idfkt):
      print
      " get fokontany "

  def fillFokontany(self):
      self.idfokontany = self.utils.getComboValue(self.ui.fokontanyComboBox)
      self.generateDemandeKey()
  def generateDemandeKey(self):

      print "generate unique code demande key"
      self.lineEdit = self.coddistrict
      print self.coddistrict
      print self.codecommune
      connection = self.parent.connection
      cursor = connection.cursor()
      cursor.execute("SELECT *   FROM fokontany  WHERE idfokontany=%s",
                     [int(self.utils.getComboValue(self.ui.fokontanyComboBox))])
      dm = cursor.fetchone()
      print " dm FOKONTANY IN"
      print dm
      print " dm FOKONTANY OUT"

      chFkt = str(dm[2]).strip()
      chDistrict = str(self.coddistrict).strip()
      chCommune = str(self.codecommune).strip()
      # chfkt = str(idfkt.strip())
      self.ui.numeroDemandeLineEdit.setText(
          _fromUtf8(chDistrict + chCommune + "_" + chFkt) + "-F-" + str(self.gid))
      self.ui.numeroDemandeLineEdit.setReadOnly(True)

      #        self.lineEdit.setText(self.coddistrict)
  def loadConsistance(self, connexion):
      cursor = connexion.cursor()
      cursor.execute("SELECT *   FROM consistance")
      cs = cursor.fetchall()
      size = len(cs)
      if (size >= 1):
          consistance = cs[0]
          for row in cs:
              ligneconsistance = row[2]
              self.ui.consistanceComboBox.addItem(_fromUtf8(row[1]), row[0])

  def loadRegionDistrictCommune(self, connexion, idregion, iddistrict, idcommune):
      cursor = connexion.cursor()
      cursor.execute("SELECT nomregion  FROM region  WHERE idregion=%s", [int(idregion)])
      dm = cursor.fetchone()
      if (len(dm) >= 1):
          region = dm[0]
          self.ui.regionLineEdit.setText(_fromUtf8(region))
          self.ui.regionLineEdit.setReadOnly(True)

      cursor.execute("SELECT *  FROM district  WHERE iddistrict=%s", [int(iddistrict)])
      dm = cursor.fetchone()
      if (len(dm) >= 1):
          coddistrict = dm[2]
          district = dm[3]
          self.coddistrict = coddistrict

      self.ui.districtLineEdit.setText(_fromUtf8(district))
      cursor.execute("SELECT *  FROM commune  WHERE idcommune=%s", [int(idcommune)])
      dm = cursor.fetchone()
      if (len(dm) >= 1):
          libelleCommune = dm[3]
          codeCommune = dm[2]
          self.codecommune = codeCommune
          self.ui.communeLineEdit.setText(_fromUtf8(libelleCommune))
          self.ui.communeLineEdit.setReadOnly(True)

  def loadCommune(self, connexion, idcommune):
      cursor = connexion.cursor()
      cursor.execute("SELECT *  FROM fokontany  WHERE idcommune=%s", [int(idcommune)])
      dm = cursor.fetchall()
      size = len(dm)
      if (size >= 1):
          district = dm[0]
          self.ui.fokontanyComboBox.clear()
          for row in dm:
              lignefkt = row[3]
              self.ui.fokontanyComboBox.addItem(_fromUtf8(row[3]), row[0])
              print
              lignefkt
      else:
          self.ui.fokontanyComboBox.clear()

  def commitDemande(self):


      self.evaluateDateReconnaissance()
      self.idfokontany = self.utils.getComboValue(self.ui.fokontanyComboBox)
      print self.idfokontany
      #lendemandeurs = len(self.demandeurs)
      #lenoppositions = len(self.opposition)

      if self.ddDate < 15:
          self.ui.dateReconnaissanceDateEdit.setFocus(Qt.Qt.OtherFocusReason)
          return

      rowCount = self.ui.tableDemande.rowCount()
      columnCount = self.ui.tableDemande.columnCount()
      rowCountOppo = self.ui.tableOpposition.rowCount()

      if rowCount == 0:
          QMessageBox.critical(self.ui.addBtn, "Erreur","Veuillez au moins ajouter un demandeur")
          return
      if self.ui.coutLineEdit.text() == "":
          QMessageBox.critical(self.ui.coutLineEdit, "Erreur", "Le cout ne doit pas etre vide")
          self.ui.coutLineEdit.setFocus(Qt.Qt.OtherFocusReason)
          return

      connection = psycopg2.connect(host=self.db_config.db_host, port=self.db_config.db_port,
                                        database=self.db_config.db_name, user=self.db_config.db_user,
                                        password=self.db_config.db_pass)

      cursor = connection.cursor()
      numDmd = str(self.ui.numeroDemandeLineEdit.text())
      self.numDemande = numDmd

      dateDemande = self.ui.dateDemandeDateEdit.text()
      dtDmande = dateDemande.split('/')

      dateReconnaissance = self.ui.dateReconnaissanceDateEdit.text()
      dtReconnaissance = dateReconnaissance.split('/')

      cout = float(self.ui.coutLineEdit.text())
      region = str(self.ui.regionLineEdit.text())
      district = str(self.ui.districtLineEdit.text())
      commune = str(self.ui.communeLineEdit.text())
      fokontany = str(self.ui.fokontanyComboBox.currentText())
      idfkt = self.utils.getComboValue(self.ui.fokontanyComboBox)
      consistance = str(self.ui.consistanceComboBox.currentText())
      print consistance
      idcommune = globalvars.id_commune
      self.idfokontany = idfkt
      exe = cursor.execute(
              "INSERT INTO demande (numdemande,datedemande,datereconnaissance,gid,region,district,idcommune,idfokontany,cout,consistance,idprojet) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING iddemande ",
              (numDmd, datetime.date(int(dtDmande[2]), int(dtDmande[1]), int(dtDmande[0])),
               datetime.date(int(dtReconnaissance[2]), int(dtReconnaissance[1]), int(dtReconnaissance[0])),
               self.idparcelle, region, district, idcommune, idfkt, cout, consistance, int(self.id_projet)))
          #        slf = qgis.utils.iface.messageBar()

          #        cursor.execute("UPDATE parcelle_d SET numdemande=(%s) WHERE gid = (%s)", (numDmd,self.idparcelle))
          #        connection.commit()
          #        slf.pushMessage("enregistrement Parcelle avec succes", level=QgsMessageBar.SUCCESS)

      # update parcelle_d to add num grille here

      connection.commit()


          # traitement des demandeurs
      idDemandePourJournal = cursor.fetchone()

      #add demandeurs here

      i = 0

      print " init remove in"
      demandeurs = []
      while (i <= rowCount ) :
          j = 0
          while ( j <= 1 ):
              item = self.ui.tableDemande.item(i,j)
              if item == None :
                  print "None"
              else :
                  print item.text()
                  demandeurs.append(item.text())

              j = j + 1
          if len(demandeurs) >= 1 :
              self.demandeurs.append(demandeurs)
          demandeurs = []
          i = i + 1
      print " demandeurs in"
      print self.demandeurs
      print "self.demandeurs out"
      if len(self.demandeurs) >= 1 :
          for d in self.demandeurs:
              exe = cursor.execute("INSERT INTO demandeur_d (nom,prenom) VALUES (%s,%s) RETURNING iddemandeur ",
                                   (str(d[0]), str(d[1])))
              connection.commit()
              iddemandeur = cursor.fetchone()
              if iddemandeur[0]:
                  exe = cursor.execute("INSERT INTO avoir_dmd (iddemandeur,iddemande,gid) VALUES (%s,%s,%s)",
                                       (int(iddemandeur[0]), int(idDemandePourJournal[0]), self.idparcelle))
                  connection.commit()


      # traitement des oppositions

      i = 0
      OppositionTemp = []
      if (rowCountOppo) >= 1:
          while (i <= rowCountOppo ) :
              j = 0
              while ( j <= 3 ):
                  item = self.ui.tableOpposition.item(i,j)
                  if item == None :
                      print "None"
                  else :
                      print item.text()
                      OppositionTemp.append(item.text())

                  j = j + 1
              if len(OppositionTemp) >= 1 :
                  self.opposition.append(OppositionTemp)
              OppositionTemp = []
              i = i + 1
      print "self.opposition in"
      print self.opposition
      print "self.opposition out"
      if len(self.opposition) >= 1:
          for o in self.opposition:
              dateOpposition = o[2]
              dateOpposition = dateOpposition.split('/')
              dateOpposition = datetime.date(int(dateOpposition[2]), int(dateOpposition[1]), int(dateOpposition[0]))

              dateDemande = o[3]
              dateDemande = dateDemande.split('/')
              dateDemande = datetime.date(int(dateDemande[2]), int(dateDemande[1]), int(dateDemande[0]))

              #dateReglement = o[7]
              etatOppositions = 0
              #dateReglement = dateReglement.split('/')
              #dateReglement = datetime.date(int(dateReglement[2]), int(dateReglement[1]), int(dateReglement[0]))

              exe = cursor.execute(
                  "INSERT INTO oppositions (typeopposition,description,dateopposition,datedemande,iddemande,gid)"
                  " VALUES (%s,%s,%s,%s,%s,%s)",
                  (str(o[1]), str(o[0]), dateOpposition, dateDemande,int(idDemandePourJournal[0]), self.idparcelle))
              connection.commit()
      i = j = 0

      # Enregistrement de la consistance au niveau de la parcelle liee a la demande creee nampiko kely fa ilaiko any am certificat SALIM
      if self.ui.consistanceComboBox.currentIndex() == -1:
          cursor.execute("UPDATE parcelle_d SET numdemande=(%s) WHERE gid = (%s)", (numDmd, self.idparcelle))
      else:
          consistanceParcelle = str(self.ui.consistanceComboBox.currentText())
          cursor.execute("UPDATE parcelle_d SET numdemande=(%s),consistance = (%s) WHERE gid = (%s)",
                         (numDmd, consistanceParcelle, self.idparcelle))
      connection.commit()
          #        last_iddemande = cursor.fetchone()[0]
          #        canvas = QgsMapCanvas()

          # Ecriture dans le journal


      from Projet.journalRunn import journal
      journal = journal(connection)
      journal.inserToJournal(globalvars.id_user, idDemandePourJournal[0], u"Demande",u"Creation de demande de Certificat")
      # Fin ecriture dans journal
      cLayer = self.parent.current_layer
      mc = self.parent.MainWindow.canvas
      #        mc = qgis.utils.iface.mapCanvas()
      for layer in mc.layers():
          if layer.type() == layer.VectorLayer:
              layer.removeSelection()

      mc.refresh()
      mc.refresh()
      mc.refresh()
      mc.refresh()
      mc.refresh()
      mc.refresh()
          # self.dialog.close()
      cursor.execute("UPDATE parcelle_d SET grille = (%s) WHERE gid = (%s)",
                     (str(self.ui.numeroGrilleLineEdit.text()), self.idparcelle))
      connection.commit()
      self.parent.ui.actionValidate.setEnabled(True)
      self.close()



