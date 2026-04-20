import os
import sys
import os
import os.path
import psycopg2, datetime
from PyQt4 import QtCore, QtGui
import globalvars
import qgis
from qgis.core import *


from ParametrageDateOCFM import Ui_Dialog

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
class DateOCFM(QtGui.QDialog):
  def __init__(self, connection):
    QtGui.QDialog.__init__(self)
    import sys
    reload(sys)
    self.connection = connection
    print("init constructeur")
    sys.setdefaultencoding('utf8')
    self.ui = Ui_Dialog()
    self.ui.setupUi(self)
    #self.initAction()
    self.substeps = []
    self.TabVoisins = []
    self.id_projet = int(globalvars.id_projet)
    self.idCommune = int(globalvars.id_commune)
    self.idRegion = 0
    self.idDistrict = 0
    self.codeGuichet = 0
    self.codeDistrict= 0
    self.nomDistrict = ""
    self.nomRegion  = ""
    self.NumDemande = ""
    # self.initSteps()
    # self.ui.pushButtonLancer.setEnabled(True)
    # self.ui.pushButtonAnnuler.setEnabled(True)
    # self.ui.pushButtonParcourir.setEnabled(True)
    # self.chargerTerritoire()

  def chargerTerritoire(self):
      cursor = self.connection.cursor()
      cursor.execute("SELECT *   FROM commune  WHERE idcommune=%s", [int(self.idCommune)])
      row = cursor.fetchone()
      print("Commune row")
      print(row)
      if row is None :
          QMessageBox.critical(self.ui.lineEdit, "Erreur", "Veuillez parametrer Commune-District-Region")
          return

      if (len(row) >= 1 and row is not  None):
          self.idDistrict = row[1]
          self.codeGuichet = row[9]
          cursor.execute("SELECT *   FROM district  WHERE iddistrict=%s", [int(self.idDistrict)])
          rw = cursor.fetchone()
          self.codeDistrict   = rw[2]
          self.nomDistrict = rw[3]

          self.idRegion = rw[1]

          cursor.execute("SELECT *   FROM region  WHERE idregion=%s", [int(self.idRegion)])
          rw2 = cursor.fetchone()
          self.nomRegion = rw2[3]

          print(" code  district ")
          print(self.codeDistrict)

          print(" code  guichet ")
          print(self.codeGuichet)

          #
          self.NumDemande =  _fromUtf8(str(self.codeDistrict) + "-" + str(self.codeGuichet)) + "-F-"


  def initSteps(self):
      self.ui.listWidgetSteps.clear()
      self.ui.listWidget.clear()
      del self.substeps[:]
      for i in [_fromUtf8("Import autres parametres initiaux : Consistance,Categorie"), _fromUtf8("Import Geometrie et des donnees alphanumeriques"), _fromUtf8(" Mise a jour table FIPLOF")]:
          step = QtGui.QListWidgetItem(i)
          step.setIcon(QtGui.QIcon(":/std/icone/time.png"))
          self.ui.listWidgetSteps.addItem(step)
          self.substeps.append([])

  def initAction(self):
      self.ui.pushButtonAnnuler.clicked.connect(self.accept)
      self.ui.pushButtonParcourir.clicked.connect(self.browseFile)
      self.ui.pushButtonLancer.clicked.connect(self.launch)
      #self.ui.listWidgetSteps.itemSelectionChanged.connect(self.refreshSubSteps)

  def browseFile(self):
      self.filename = QtGui.QFileDialog.getOpenFileName(self, "Choisissez un fichier","","Fichier de forme files(*.shp)")
      self.ui.lineEdit.setText(self.filename)
      self.ui.pushButtonLancer.setEnabled(True)

  def refreshSubSteps(self):
      items = self.ui.listWidgetSteps.selectedItems()
      self.ui.listWidget.clear()
      if len(items) == 0:
          return
      index = self.ui.listWidgetSteps.indexFromItem(items[0])
      self.ui.listWidget.clear()
      for item in self.substeps[index.row()]:
          listitem = QtGui.QListWidgetItem(item['text'])
          listitem.setIcon(QtGui.QIcon(":/std/icone/bullet_%s.png" % (item['icon'])))
          self.ui.listWidget.addItem(listitem)

  def launch(self):
      self.ui.progressBar.setValue(0)
      self.initSteps()
      id_projet = int(globalvars.id_projet)
      if self.filename == "":
          return
      self.ui.pushButtonLancer.setEnabled(False)
      self.ui.pushButtonAnnuler.setEnabled(False)
      self.ui.pushButtonParcourir.setEnabled(False)
      filename = _fromUtf8(self.filename)
      TabCodeParcelle = []

      layer = QgsVectorLayer(filename, "dataFromPLOFPapers", "ogr")
      features = layer.getFeatures()
      countFeatures = layer.featureCount()
      print("countFeatures")
      print(countFeatures)
      cursor = self.connection.cursor()
      i = 0
      try:
          for f in features:
              geometry = f.geometry()
              if geometry.wkbType() == QGis.WKBPolygon:
                  x = geometry.asPolygon()
              if geometry.wkbType() == QGis.WKBMultiPolygon:
                  x = geometry.asMultiPolygon()[0]

              attrs = f.attributes()
              size = len(attrs)
              print(attrs)


              try:
                  num = ""

                  codeParcelle = attrs[2].toPyObject()
                  print(codeParcelle)
                  print(" code parcelle--")

                  #NumDemande = self.NumDemande+" "+str(attrs[2].toPyObject())
                  print('Geometry.exportToWkt()')
                  print(str(geometry.exportToWkt()))
                  exe = cursor.execute(
                      "INSERT INTO parcelle_d (geom,surface ,codeparcelle,id_commune)VALUES (ST_GeomFromText(%s, "+str(globalvars.EPSG_SCR)+"),ST_Area(%s), %s, %s) returning gid,surface",
                      (str(geometry.exportToWkt()), str(geometry.exportToWkt()), str(codeParcelle),self.idCommune))
                  self.connection.commit()
                  print("AFTER commit")
                  dm = cursor.fetchone()
                  gid = dm[0]

                  p = (i + 1) * 100 / countFeatures
                  self.progress(p)

                  # #insert into table demande
                  # self.ui.numeroDemandeLineEdit.setText(
                  #     _fromUtf8(chDistrict + "-" + chCodeGuichet) + "-F-" + str(self.currentValDemande))
              except Exception as e:
                  TabCodeParcelle.append(codeParcelle)
                  self.connection.rollback()
                  print(e)

              #
              # try:
              #     cout = 5000
              #     categorie = attrs[23].toPyObject()
              #     fkt = attrs[11].toPyObject()
              #     cursor.execute("SELECT *  FROM fokontany  WHERE nomfokontany=%s", [str(fkt).strip()])
              #     row = cursor.fetchone()
              #
              #     if (row is not  None):
              #         idFokontany = row[0]
              #         exe = cursor.execute(
              #             "INSERT INTO demande (numdemande,gid,region,district,idcommune,cout,categorie,idprojet,consistance,idfokontany) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING iddemande ",
              #             (str(NumDemande),
              #              gid, str(self.nomRegion), str(self.nomDistrict), int(self.idCommune), cout, str(categorie), int(self.id_projet)
              #              ,str(consistance),int(idFokontany)))
              #         self.connection.commit()
              #         print('after commit demande')
              #         rowDemande = cursor.fetchone()
              # except Exception as e:
              #     print(e)
              #     self.connection.rollback()
              #
              # try:
              #     cursor.execute("UPDATE parcelle_d SET numdemande=(%s) WHERE gid = (%s)",
              #                        (str(NumDemande), gid))
              #     self.connection.commit()
              # except Exception as e:
              #     print(e)
              # try :
              #     pparam = attrs[24].toPyObject()
              #     Personnne = self.recupPersonne(pparam)
              #     if(Personnne is not  None) :
              #         exe = cursor.execute(
              #              "INSERT INTO avoir_demande (idpersonne,iddemande,idparcelle) VALUES (%s,%s,%s)",
              #              (int(Personnne[0]), int(rowDemande[0]), gid))
              #         self.connection.commit()
              #         print('after commit demande')
              # except Exception as e:
              #     print(e)
              #     self.connection.rollback()
              # try:
              #     print("TRAITER VOISIN")
              #
              # except Exception as e :
              #     print(e)
              #     self.connection.rollback()
      except Exception as e:
          print(e)
      print(' parcelle ayant des probleme de geometrie')
      print(TabCodeParcelle)



  # self.myThread = ImporterThread(filename=self.filename, connection=self.connection)
      # self.connect(self.myThread, SIGNAL("finished()"), self.termine)
      # self.connect(self.myThread, SIGNAL("alert(QString)"), self.alert)
      # self.connect(self.myThread, SIGNAL("clearSubstep(int)"), self.clearSubstep)
      # self.connect(self.myThread, SIGNAL("addSubStep(int, QString, QString)"), self.addSubStep)
      # self.connect(self.myThread, SIGNAL("progress(int)"), self.progress)
      # self.connect(self.myThread, SIGNAL("stepInit(int)"), self.stepInit)
      # self.connect(self.myThread, SIGNAL("stepDone(int)"), self.stepDone)
      # self.myThread.start()

  def recupPersonne(self,ppParam):
      cursor = self.connection.cursor()
      cursor.execute("SELECT *  FROM personne  WHERE pparams=%s", [str(ppParam)])
      row = cursor.fetchone()
      return row

  def termine(self):
      Utils.alert("Importation Terminee")
      self.ui.pushButtonLancer.setEnabled(True)
      self.ui.pushButtonAnnuler.setEnabled(True)
      self.ui.pushButtonParcourir.setEnabled(True)

  def alert(self, msg):
      Utils.alert(msg)

  def clearSubstep(self, step):
      del self.substeps[step][:]

  def progress(self, p):
      self.ui.progressBar.setValue(p)

  def addSubStep(self, index, text, icon):
      self.substeps[index].append({'text': text, 'icon': icon})

  def stepInit(self, step):
      self.ui.listWidgetSteps.item(step).setIcon(QtGui.QIcon(':/std/icone/time_go.png'))

  def stepDone(self, step):
      m = 0
      for item in self.substeps[step]:
          if item["icon"] == 'red':
              v = 2
          if item["icon"] == "orange":
              v = 1
          if item["icon"] == "green":
              v = 0
          m = v if m < v else m
      if m == 0:
          icon = ":/std/icone/accept.png"
      if m == 1:
          icon = ":/std/icone/warning.png"
      if m == 2:
          icon = ":/std/icone/error.png"
      self.ui.listWidgetSteps.item(step).setIcon(QtGui.QIcon(icon))




