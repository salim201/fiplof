# coding: utf-8

# Form implementation generated from reading ui file 'CreaDemande.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!


import os
import sys
import os
import os.path
import psycopg2
import qgis
#from qgis.utils import iface
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
from qgis.gui import *
import time
import datetime
import globalvars
from PyQt4 import QtGui, Qt
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, Qt
from PyQt4 import QtCore, QtGui


from PyQt4 import QtGui, Qt
from PyQt4 import Qt, QtGui
import psycopg2
from psycopg2 import extras
from Utils import Utils
from PyQt4.QtCore import *




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

class Ui_CreationDemande(object):
    def __init__(self, parent):
        self.parent = parent
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
        self.cvs = self.parent.MainWindow.canvas
        self.autoincrementkeydemande = 0
        self.opposition = []

        self.demandeurs = []
        self.filenamepreview = ""
        self.connection = self.parent.connection
        self.utils = Utils(self.connection)
        self.idparcelle = self.parent.idparcelle

        self.parent.currvalDemande = parent.currvalDemande
        self.id_projet = self.parent.id_projet
        print self.parent.iddemande
        #self.fokontanyComboBox.currentIndexChanged.connect(self.fillFokontany)

    def callDemandeur(self):
        from CreateDemandeurCertificat import CreateDemandeurCertificat
        Demandeur = CreateDemandeurCertificat(self)
        Demandeur.show()
        result = Demandeur.exec_()

    def callOpposition(self):

        from OppositionRunn import OppositionRunn
        print "call opposition "
        numDmd = str(self.lineEditDemande.text())
        self.numDemande = numDmd
        opp = OppositionRunn(self)
        print opp
        opp.show()
        result = opp.exec_()



    def resolve(self, name, basepath=None):
        if not basepath:
            basepath = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(basepath, name)

    def showCalWid(self):
        self.calendar = QtGui.QCalendarWidget()
        print "test..."
        self.calendar.setMinimumDate(QtCore.QDate(1900, 1, 1))
        self.calendar.setMaximumDate(QtCore.QDate(3000, 1, 1))
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.updateDate)
        self.calendar.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.calendar.setStyleSheet('background: white; color: black')
        self.calendar.setGridVisible(True)
        pos = QtGui.QCursor.pos()
        self.calendar.setGeometry(pos.x(), pos.y(), 300, 200)
        self.calendar.show()

    def showCalWid2(self):
        self.calendar = QtGui.QCalendarWidget()
        self.calendar.setMinimumDate(QtCore.QDate(1900, 1, 1))
        self.calendar.setMaximumDate(QtCore.QDate(3000, 1, 1))
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.updateDate2)
        self.calendar.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.calendar.setStyleSheet('background: white; color: black')
        self.calendar.setGridVisible(True)
        pos = QtGui.QCursor.pos()
        self.calendar.setGeometry(pos.x(), pos.y(), 300, 200)
        self.calendar.show()

    def updateDate(self, *args):
        date = self.calendar.selectedDate()
        self.dateDemandeLineEdit.setReadOnly(False)
        self.dateDemandeLineEdit.setText("{}/{}/{}".format(date.day(), date.month(), date.year()))  # output: 20/9/2013
        #        getDate = self.calendar.selectedDate().
        #        self.lineEdit.setText(getDate)
        self.calendar.deleteLater()
        self.dateDemandeLineEdit.setReadOnly(True)



    def updateDate2(self, *args):
        date = self.calendar.selectedDate()
        self.dateDeReconnaissanceLineEdit.setReadOnly(False)
        from datetime import datetime
        date_format = "%d/%m/%Y"
        a = datetime.strptime(self.dateDemandeLineEdit.text(), date_format)


        self.dateDeReconnaissanceLineEdit.setText(
            "{}/{}/{}".format(date.day(), date.month(), date.year()))  # output: 20/9/2013

        b = datetime.strptime(self.dateDeReconnaissanceLineEdit.text(), date_format)
        delta = b - a
        diffdate =  delta.days  # that's it
        if diffdate < 15 :
            QMessageBox.critical(self.dateDeReconnaissanceLineEdit, "Erreur", "La date de reconnaissance doit etre 15 jours apres")
            self.dateDeReconnaissanceLineEdit.setText("")

        self.calendar.deleteLater()
        self.dateDeReconnaissanceLineEdit.setReadOnly(True)

    def evaluateDateReconnaissance(self):
        print "first test of all"
        from datetime import datetime
        from datetime import date
        date_format = "%d/%m/%Y"
        #a = datetime.strptime(self.dateDemandeLineEdit.text(), date_format)
        #b = datetime.strptime(self.dateDeReconnaissanceLineEdit.text(), date_format)

        a = self.dateDemandeLineEdit.text()
        print "a"
        print a
        a = a.split("/")
        print a[2]
        print a[1]
        #a = date(int(a[2]),int(a[1]),int(a[0]))

        b = self.dateDeReconnaissanceLineEdit.text()
        b = b.split("/")
        #b = date(int(b[2]),int(b[1]),int(b[0]))



        from datetime import datetime
        date_format = "%m/%d/%Y"
        a = datetime.strptime(''+str(a[1])+'/'+str(a[0])+'/'+str(a[2])+'', date_format)
        b = datetime.strptime(''+str(b[1])+'/'+str(b[0])+'/'+str(b[2])+'', date_format)
        delta = b - a
        diffdate = b - a
        self.ddDate = delta.days
        if self.ddDate < 30 :
            QMessageBox.critical(self.dateDeReconnaissanceLineEdit, "Erreur", u"La date de reconnaissance doit etre 30 jours après la décision")


            #self.dateDeReconnaissanceLineEdit.setText("")
        #self.dateDeReconnaissanceLineEdit.setReadOnly(True)




    def getFokontany(self,idfkt):
        print " get fokontany "


    def generateDemandeKey(self):
        print "generate unique code demande key"
        self.lineEdit = self.coddistrict
        print self.coddistrict
        print self.codecommune
        connection = self.parent.connection
        cursor = connection.cursor()
        cursor.execute("SELECT *   FROM fokontany  WHERE idfokontany=%s", [int(self.utils.getComboValue(self.fokontanyComboBox))])
        dm = cursor.fetchone()
        print " dm FOKONTANY IN"
        print dm
        print " dm FOKONTANY OUT"


        chFkt = str(dm[2]).strip()
        chDistrict = str(self.coddistrict).strip()
        chCommune = str(self.codecommune).strip()
        if self.codecommune < 10:
            chCommune = "0" + chCommune


        print " self.utils.getComboValue(self.fokontanyComboBox) in"
        print self.utils.getComboValue(self.fokontanyComboBox)
        print " self.utils.getComboValue(self.fokontanyComboBox) out"


        #chfkt = str(idfkt.strip())
        self.lineEditDemande.setText(_fromUtf8(chDistrict+chCommune+"_"+chFkt)+"-F-"+str(self.parent.currvalDemande))
        self.lineEditDemande.setReadOnly(True)

    #        self.lineEdit.setText(self.coddistrict)

    def setupUi(self, CreationDemande):
        CreationDemande.setObjectName(_fromUtf8("CreationDemande"))
        self.CreationDemande = CreationDemande
        connection = self.parent.connection
        self.CreationDemande.setModal(True)

#        connection = psycopg2.connect(host=self.db_config.db_host, port=self.db_config.db_port,database=self.db_config.db_name, user=self.db_config.db_user,password=self.db_config.db_pass)

        cursor = connection.cursor()
        self.formGroupBox_2 = QtGui.QGroupBox(CreationDemande)
        self.formGroupBox_2.setGeometry(QtCore.QRect(20, 220, 281, 141))
        self.formGroupBox_2.setObjectName(_fromUtf8("formGroupBox_2"))
        self.formLayout_2 = QtGui.QFormLayout(self.formGroupBox_2)
        self.lineEditRegion = QtGui.QLineEdit(self.formGroupBox_2)
#        self.communeComboBox = QtGui.QComboBox(self.formGroupBox_2)
        self.commune = QtGui.QLineEdit(self.formGroupBox_2)

        self.formGroupBox = QtGui.QGroupBox(CreationDemande)
        self.formGroupBox.setGeometry(QtCore.QRect(20, 10, 281, 144))
        self.formGroupBox.setObjectName(_fromUtf8("formGroupBox"))
        self.lineEditDemande = QtGui.QLineEdit(self.formGroupBox)

        self.filenamepreview = self.preview()
        os.chdir(self.resolve(".."))
        dr = os.getcwd()
        sys.path.append(os.path.dirname(dr))

        import globalvars

#        os.remove(filename)

        self.lineEditDemande.setReadOnly(True)
        #idregion = 484
        #iddistrict = 487
        #idcommune = 498

        #iddistrict = 5
        idcommune = globalvars.id_commune
        print "----------------globalvars.id_commune----------------"
        print globalvars.id_commune
        print "--------------------globalvars.id_commune-----------"


        cursor.execute("SELECT *   FROM commune  WHERE idcommune=%s", [int(idcommune)])
        dm = cursor.fetchone()
        if (len(dm) >= 1):
            iddistrict = dm[1]
            cursor.execute("SELECT *   FROM district  WHERE iddistrict=%s", [int(iddistrict)])
            dm = cursor.fetchone()
            idregion = dm[1]

 #               for row in dm:
 #                   lignecommune = row[3]
 #                   self.communeComboBox.addItem(_fromUtf8(row[3]), row[0])


        CreationDemande.resize(580, 437)



        self.label = QtGui.QLabel(self.formGroupBox)
        self.label.setGeometry(QtCore.QRect(8, 10, 85, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.dateDemandeLabel = QtGui.QLabel(self.formGroupBox)
        self.dateDemandeLabel.setGeometry(QtCore.QRect(8, 36, 70, 16))
        self.dateDemandeLabel.setObjectName(_fromUtf8("dateDemandeLabel"))

        self.dateDemandeLineEdit = QtGui.QDateEdit(self.formGroupBox)
        self.dateDemandeLineEdit.setGeometry(QtCore.QRect(129, 36, 129, 20))
        self.dateDemandeLineEdit.setDisplayFormat("dd/MM/yyyy")
        self.dateDemandeLineEdit.setDate(QDate.currentDate())
#        self.dateDemandeLineEdit.setInputMask(_fromUtf8(""))
        self.dateDemandeLineEdit.setEnabled(True)
        self.dateDemandeLineEdit.setCalendarPopup(True)
        self.dateDemandeLineEdit.setObjectName(_fromUtf8("dateDemandeLineEdit"))


        self.dateDeReconnaissanceLabel = QtGui.QLabel(self.formGroupBox)
        self.dateDeReconnaissanceLabel.setGeometry(QtCore.QRect(8, 62, 115, 16))
        self.dateDeReconnaissanceLabel.setObjectName(_fromUtf8("dateDeReconnaissanceLabel"))

        self.dateDeReconnaissanceLineEdit = QtGui.QDateEdit(self.formGroupBox)
        self.dateDeReconnaissanceLineEdit.setGeometry(QtCore.QRect(129, 62, 129, 20))
        self.dateDeReconnaissanceLineEdit.setObjectName(_fromUtf8("dateDeReconnaissanceLineEdit"))
        self.dateDeReconnaissanceLineEdit.setEnabled(True)
        self.dateDeReconnaissanceLineEdit.setCalendarPopup(True)
        self.dateDeReconnaissanceLineEdit.setDisplayFormat("dd/MM/yyyy")
        self.dateDeReconnaissanceLineEdit.setDate(QDate.currentDate())
        self.dateDeReconnaissanceLineEdit.dateChanged.connect(self.evaluateDateReconnaissance)
        #self.ui.dateDemandeLineEdit.dateChanged.connect(self.evaluateDateReconnaissance)
        #self.calendar.clicked.connect(self.updateDate2)
#        self.dateDemandeLineEdit.setObjectName(_fromUtf8("dateDemandeLineEdit"))

        self.dateDemandeLineEdit.setReadOnly(False)
        self.dateDeReconnaissanceLineEdit.setReadOnly(False)

        self.consistanceLabel = QtGui.QLabel(self.formGroupBox)
        self.consistanceLabel.setGeometry(QtCore.QRect(8, 88, 58, 16))
        self.consistanceLabel.setObjectName(_fromUtf8("consistanceLabel"))
        self.consistanceComboBox = QtGui.QComboBox(self.formGroupBox)
        self.consistanceComboBox.setGeometry(QtCore.QRect(129, 88, 131, 20))
        self.consistanceComboBox.setObjectName(_fromUtf8("consistanceComboBox"))



        self.coutLabel = QtGui.QLabel(self.formGroupBox)
        self.coutLabel.setGeometry(QtCore.QRect(8, 114, 23, 16))
        self.coutLabel.setObjectName(_fromUtf8("coutLabel"))
        self.coutLineEdit = QtGui.QLineEdit(self.formGroupBox)
        self.coutLineEdit.setGeometry(QtCore.QRect(129, 114, 129, 20))
        self.coutLineEdit.setObjectName(_fromUtf8("coutLineEdit"))

        #validations
        validator = QtGui.QDoubleValidator()
        self.coutLineEdit.setValidator(validator)
        #self.coutLineEdit.setInputMask('[0-9]')


        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("D:/EN COURS/PYTHON/DatePickerDialog.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.lineEditDemande.setGeometry(QtCore.QRect(130, 10, 131, 20))
        self.lineEditDemande.setObjectName(_fromUtf8("lineEditDemande"))
        self.horizontalGroupBox = QtGui.QGroupBox(CreationDemande)
        self.horizontalGroupBox.setGeometry(QtCore.QRect(20, 160, 281, 51))
        self.horizontalGroupBox.setObjectName(_fromUtf8("horizontalGroupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalGroupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton_2 = QtGui.QPushButton(self.horizontalGroupBox)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton = QtGui.QPushButton(self.horizontalGroupBox)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)

        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setContentsMargins(7, 9, 15, -1)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.regionLabel = QtGui.QLabel(self.formGroupBox_2)
        self.regionLabel.setObjectName(_fromUtf8("regionLabel"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.regionLabel)
        self.districtLabel = QtGui.QLabel(self.formGroupBox_2)
        self.districtLabel.setObjectName(_fromUtf8("districtLabel"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.districtLabel)
        self.communeLabel = QtGui.QLabel(self.formGroupBox_2)
        self.communeLabel.setObjectName(_fromUtf8("communeLabel"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.communeLabel)

#        self.communeComboBox.setObjectName(_fromUtf8("communeComboBox"))
        self.commune.setObjectName(_fromUtf8("commune"))
#        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.communeComboBox)
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.commune)
        self.fokontanyLabel = QtGui.QLabel(self.formGroupBox_2)
        self.fokontanyLabel.setObjectName(_fromUtf8("fokontanyLabel"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.fokontanyLabel)
        self.fokontanyComboBox = QtGui.QComboBox(self.formGroupBox_2)
        self.fokontanyComboBox.setObjectName(_fromUtf8("fokontanyComboBox"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.fokontanyComboBox)
        #self.pushButton_3 = QtGui.QPushButton(self.formGroupBox_2)
        #self.pushButton_3.setEnabled(False)
        #self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        #self.formLayout_2.setWidget(4, QtGui.QFormLayout.FieldRole, self.pushButton_3)

        self.lineEditRegion.setObjectName(_fromUtf8("lineEditRegion"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEditRegion)
        self.lineEditDistrict = QtGui.QLineEdit(self.formGroupBox_2)
        self.lineEditDistrict.setObjectName(_fromUtf8("lineEditDistrict"))
        self.lineEditRegion.setReadOnly(True)
        self.lineEditDistrict.setReadOnly(True)


        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEditDistrict)
        self.horizontalGroupBox_2 = QtGui.QGroupBox(CreationDemande)
        self.horizontalGroupBox_2.setGeometry(QtCore.QRect(20, 370, 281, 51))
        self.horizontalGroupBox_2.setObjectName(_fromUtf8("horizontalGroupBox_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalGroupBox_2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton_4 = QtGui.QPushButton(self.horizontalGroupBox_2)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.horizontalLayout_2.addWidget(self.pushButton_4)
        self.pushButton_5 = QtGui.QPushButton(self.horizontalGroupBox_2)
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.horizontalLayout_2.addWidget(self.pushButton_5)
        self.horizontalLayoutWidget = QtGui.QWidget(CreationDemande)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(310, 10, 261, 391))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))

        self.label_2 = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)


        self.loadCommune(connection,idcommune)
        self.loadRegionDistrictCommune(connection,idregion,iddistrict,idcommune)

        self.loadConsistance(connection)

#        self.pushButton_Cal1.clicked.connect(self.showCalWid)
#        self.pushButton_Cal2.clicked.connect(self.showCalWid2)
        self.fokontanyComboBox.currentIndexChanged.connect(self.fillFokontany)
        self.generateDemandeKey()
        self.pushButton.clicked.connect(self.callDemandeur)
        #self.dateDeReconnaissanceLineEdit.mousePressEvent.connect(self.evaluateDateReconnaissance)
        self.pushButton_2.clicked.connect(self.callOpposition)
        self.label_2.setPixmap(QtGui.QPixmap(self.filenamepreview))
        self.pushButton_4.clicked.connect(self.commitDemande)


#        self.dateDeReconnaissanceLineEdit.focusInEvent()


        self.retranslateUi(CreationDemande)
        QtCore.QMetaObject.connectSlotsByName(CreationDemande)

    def fillFokontany(self):
        self.idfokontany = self.utils.getComboValue(self.fokontanyComboBox)
        self.generateDemandeKey()

    def preview(self):
        sql = "SELECT ST_AsPNG(" \
              "ST_AsRaster(" \
              "ST_Buffer(geom, -10),200,200,ARRAY['8BUI', '8BUI', '8BUI'], ARRAY[118,154,118], ARRAY[0,0,0]" \
              ")) png " \
              "from parcelle_d WHERE gid=%s"
        connection = self.parent.connection
#        cursor = connection.cursor()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SET bytea_output TO escape")
        cursor.execute(sql, (self.idparcelle,))
        row = cursor.fetchone()
        filename = "preview.png"
        f = open(filename, "wb")
        f.write(row['png'])
        f.close()
        cursor.close()
        return filename

    def commitDemande(self):

        print " OPPOSITIONS IN"
        print self.opposition
        print len(self.opposition)
        print " OPPOSITIONS OUT"
        self.evaluateDateReconnaissance()
        self.idfokontany = self.utils.getComboValue(self.fokontanyComboBox)
        print self.idfokontany
        lendemandeurs = len(self.demandeurs)
        lenoppositions = len(self.opposition)


        if self.ddDate < 15 :
            self.dateDeReconnaissanceLineEdit.setFocus(Qt.Qt.OtherFocusReason)
            return
        if lendemandeurs == 0:
            QMessageBox.critical(self.pushButton, "Erreur",
                                 "Veuillez au moins ajouter un demandeur")
            return
        if self.coutLineEdit.text() == "":
            QMessageBox.critical(self.coutLineEdit, "Erreur","Le cout ne doit pas etre vide")
            self.coutLineEdit.setFocus(Qt.Qt.OtherFocusReason)
            return

        connection = psycopg2.connect(host=self.db_config.db_host, port=self.db_config.db_port,
                                      database=self.db_config.db_name, user=self.db_config.db_user,
                                      password=self.db_config.db_pass)

        cursor = connection.cursor()
        numDmd = str(self.lineEditDemande.text())
        self.numDemande = numDmd

        dateDemande = self.dateDemandeLineEdit.text()
        dtDmande = dateDemande.split('/')

        dateReconnaissance = self.dateDeReconnaissanceLineEdit.text()
        dtReconnaissance = dateReconnaissance.split('/')

        cout = float(self.coutLineEdit.text())
        region = str(self.lineEditRegion.text())
        district = str(self.lineEditDistrict.text())
        commune = str(self.commune.text())
        fokontany = str(self.fokontanyComboBox.currentText())
        idfkt= self.utils.getComboValue(self.fokontanyComboBox)
        consistance = str(self.consistanceComboBox.currentText())
        print consistance
        idcommune = globalvars.id_commune
        self.idfokontany = idfkt
        exe = cursor.execute("INSERT INTO demande (numdemande,datedemande,datereconnaissance,gid,region,district,idcommune,idfokontany,cout,consistance,idprojet) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING iddemande ",(numDmd, datetime.date(int(dtDmande[2]), int(dtDmande[1]), int(dtDmande[0])),
                                                                                                                                                                                            datetime.date(int(dtReconnaissance[2]), int(dtReconnaissance[1]), int(dtReconnaissance[0])),self.idparcelle, region, district, idcommune, idfkt,cout,consistance,int(self.id_projet)))
#        slf = qgis.utils.iface.messageBar()

#        cursor.execute("UPDATE parcelle_d SET numdemande=(%s) WHERE gid = (%s)", (numDmd,self.idparcelle))
#        connection.commit()
#        slf.pushMessage("enregistrement Parcelle avec succes", level=QgsMessageBar.SUCCESS)
        connection.commit()

        #traitement des demandeurs
        idDemandePourJournal  = cursor.fetchone()

        if lendemandeurs >= 1 :
            for d in self.demandeurs :
                exe = cursor.execute("INSERT INTO demandeur_d (nom,prenom) VALUES (%s,%s) RETURNING iddemandeur ",(str(d[0]),str(d[1])))
                connection.commit()
                iddemandeur = cursor.fetchone()
                if iddemandeur[0] :
                    exe = cursor.execute("INSERT INTO avoir_dmd (iddemandeur,iddemande,gid) VALUES (%s,%s,%s)",(int(iddemandeur[0]), int(idDemandePourJournal[0]),self.idparcelle))
                    connection.commit()

        if lenoppositions >= 1 :

            for o in self.opposition:
                dateOpposition = o[3]
                dateOpposition = dateOpposition.split('/')
                dateOpposition = datetime.date(int(dateOpposition[2]), int(dateOpposition[1]), int(dateOpposition[0]))

                dateDemande = o[4]
                dateDemande = dateDemande.split('/')
                dateDemande = datetime.date(int(dateDemande[2]), int(dateDemande[1]), int(dateDemande[0]))


                dateReglement = o[7]
                etatOppositions = 0
                dateReglement = dateReglement.split('/')
                dateReglement = datetime.date(int(dateReglement[2]), int(dateReglement[1]), int(dateReglement[0]))

                exe = cursor.execute("INSERT INTO oppositions (typeopposition,description,dateopposition,datedemande,naturereglement,descriptionreglement,"
                                     "datereglement,iddemande,gid)"
                                     " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                 (str(o[1]), str(o[2]),dateOpposition,dateDemande,str(o[5]),str(o[6]),dateReglement,int(idDemandePourJournal[0]),self.idparcelle))
                connection.commit()






        #traitement des oppositions
        #add demandeurs
        i = j = 0

        #Enregistrement de la consistance au niveau de la parcelle liee a la demande creee nampiko kely fa ilaiko any am certificat SALIM
        if self.consistanceComboBox.currentIndex() == -1:
            cursor.execute("UPDATE parcelle_d SET numdemande=(%s) WHERE gid = (%s)", (numDmd, self.idparcelle))
        else:
            consistanceParcelle = str(self.consistanceComboBox.currentText())
            cursor.execute("UPDATE parcelle_d SET numdemande=(%s),consistance = (%s) WHERE gid = (%s)",
                   (numDmd, consistanceParcelle, self.idparcelle))
        connection.commit()
#        last_iddemande = cursor.fetchone()[0]
#        canvas = QgsMapCanvas()

        #Ecriture dans le journal
        from Projet.journalRunn import journal
        journal = journal(connection)
        journal.inserToJournal(globalvars.id_user, idDemandePourJournal[0], u"Demande", u"Création de demande de Certificat")
        #Fin ecriture dans journal
        cLayer  = self.parent.current_layer
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
        #self.dialog.close()
        self.parent.ui.actionValidate.setEnabled(True)
        self.CreationDemande.close()


 #       self.parent.displayLayers()

        print cLayer

    def loadConsistance(self,connexion):
        cursor = connexion.cursor()
        cursor.execute("SELECT *   FROM consistance")
        cs = cursor.fetchall()
        size = len(cs)
        if (size >= 1):
            consistance = cs[0]
            for row in cs:
                ligneconsistance = row[2]
                self.consistanceComboBox.addItem(_fromUtf8(row[1]), row[0])
    def loadRegionDistrictCommune(self,connexion,idregion,iddistrict,idcommune):
        cursor = connexion.cursor()
        cursor.execute("SELECT nomregion  FROM region  WHERE idregion=%s", [int(idregion)])
        dm = cursor.fetchone()
        if (len(dm) >= 1):
            region = dm[0]
            self.lineEditRegion.setText(_fromUtf8(region))
            self.lineEditRegion.setReadOnly(True)

        cursor.execute("SELECT *  FROM district  WHERE iddistrict=%s", [int(iddistrict)])
        dm = cursor.fetchone()
        if (len(dm) >= 1):
            coddistrict = dm[2]
            district = dm[3]
            self.coddistrict = coddistrict

        self.lineEditDistrict.setText(_fromUtf8(district))
        cursor.execute("SELECT *  FROM commune  WHERE idcommune=%s", [int(idcommune)])
        dm = cursor.fetchone()
        if (len(dm) >= 1):
            libelleCommune = dm[3]
            codeCommune = dm[2]
            self.codecommune = codeCommune
            self.commune.setText(_fromUtf8(libelleCommune))
            self.commune.setReadOnly(True)

    def loadCommune(self,connexion,idcommune):
        cursor = connexion.cursor()
        cursor.execute("SELECT *  FROM fokontany  WHERE idcommune=%s", [int(idcommune)])
        dm = cursor.fetchall()
        size = len(dm)
        if(size >= 1) :
            district = dm[0]
            self.fokontanyComboBox.clear()
            for row in dm:
                lignefkt = row[3]
                self.fokontanyComboBox.addItem(_fromUtf8(row[3]),row[0])
                print lignefkt
        else :
            self.fokontanyComboBox.clear()

    def changeCommune(self,text):

        self.lineEditDemande.setReadOnly(False)
        idcommune = self.communeComboBox.itemData(text)
        self.communeComboBox.currentText()
        connection = psycopg2.connect(host=self.db_config.db_host, port=self.db_config.db_port,
                                      database=self.db_config.db_name, user=self.db_config.db_user,
                                      password=self.db_config.db_pass)
        cursor = connection.cursor()



        cursor.execute("SELECT *  FROM commune  WHERE idcommune=%s", [int(idcommune)])
        dm = cursor.fetchone()
        size = len(dm)
        if(size >= 1) :
            codecommune = dm[2]
            self.codecommune = codecommune

            print codecommune
#              for row in dm:
#                lignefkt = row[3]



        cursor.execute("SELECT *  FROM fokontany  WHERE idcommune=%s", [int(idcommune)])
        dm = cursor.fetchall()
        size = len(dm)
        if(size >= 1) :
            district = dm[0]
            self.fokontanyComboBox.clear()
            for row in dm:
                lignefkt = row[3]
                self.fokontanyComboBox.addItem(_fromUtf8(row[3]),row[0])
                print lignefkt
        else :
            self.fokontanyComboBox.clear()



        self.generateDemandeKey()
#        self.lineEditDemande.setText(_fromUtf8(str(self.codecommune)))
#        self.generateDemandeKey()

    def retranslateUi(self, CreationDemande):
        CreationDemande.setWindowTitle(_translate("CreationDemande", "Demande certificat", None))

        self.label.setText(_translate("CreationDemande", "Numero Demande", None))
        self.dateDemandeLabel.setText(_translate("CreationDemande", "Date demande", None))
        self.dateDeReconnaissanceLabel.setText(_translate("CreationDemande", "Date de reconnaissance", None))
        self.consistanceLabel.setText(_translate("CreationDemande", "Consistance", None))
        self.coutLabel.setText(_translate("CreationDemande", "Cout", None))
        self.pushButton_2.setText(_translate("CreationDemande", "Oppositions", None))
        self.pushButton.setText(_translate("CreationDemande", "Demandeurs", None))
        self.regionLabel.setText(_translate("CreationDemande", "Region", None))
        self.districtLabel.setText(_translate("CreationDemande", "District", None))
        self.communeLabel.setText(_translate("CreationDemande", "Commune", None))
        self.fokontanyLabel.setText(_translate("CreationDemande", "Fokontany", None))
        #self.pushButton_3.setText(_translate("CreationDemande", "Nouveau FKT", None))
        self.pushButton_4.setText(_translate("CreationDemande", "Creer demande", None))
        self.pushButton_5.setText(_translate("CreationDemande", "Annuler", None))

