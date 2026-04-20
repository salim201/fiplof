#coding: utf8
from PyQt4 import QtGui, Qt, QtCore
from PyQt4.QtGui import *
from separation_bd import Ui_Dialog
from .SeparationBaseThread import SeparationBaseThread
from os.path import expanduser
import os, sys
import psycopg2
import re
from Configuration import DbConfig
from plof import Plof
from ConfigParser import SafeConfigParser
import globalvars



class SeparationBaseRun(Qt.QDialog):
    parent = None  # type: Plof

    def __init__(self, parent, exetype, empty = False):
        Qt.QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.parent = parent
        self.connexion = self.parent.connection
        self.cursor = self.connexion.cursor()
        self.thread = None
        print "CONSTRUCTEUR"
        self.LOGIN = ''
        self.PASSWORD = ''
        self.FILESAVE = ''
        self.CURRENT_DB = ''
        self.CURRENT_USER = ''
        self.NOM_BASE = []
        self.communes = []
        self.output = []
        self.current_datebase()
        self.current_dbuser()
        #self.ui.find.clicked.connect(self.upload_file)
        self.ui.launch.clicked.connect(self.launch)
        self.ui.cancel.clicked.connect(self.reject)
        self.db_config = DbConfig.DbConfig()
        self.empty = empty
        validatorNomBase = Qt.QRegExpValidator(globalvars.regexpNomBase)
        #self.ui.lineEditNomBase.setValidator(validatorNomBase)
        if self.empty:
            dirname = os.path.dirname(__file__)
            filename = dirname + "/empty_db_fiplof.sql"
            print "*******************filename******************"
            print filename
            self.FILESAVE = str(filename)

        self.generate_nom_base()

            #self.ui.filename.setText(str(filename))
        #self.ui.lineEditNomBase.textChanged.connect(self.toLowerField)

        self.type = exetype

    def get_pgdump_path(self):
        setting = None
        cursor = self.connexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT setting FROM pg_settings where name like 'data_directory'")
            row = cursor.fetchone()
            setting = row["setting"]
        except Exception as e:
            print(e)
        cursor.close()
        if setting is None:
            return None
        b = os.path.dirname(setting)
        return str(os.path.join(b, "bin\\%s.exe" % self.type))

    def upload_file(self):
        pass

    def generate_nom_base(self):
        communes = self.getAllCommunes()
        self.communes = communes
        dataToShow = []
        print "call of generate nom base"
        for com in communes:
            dt = []
            nom_commune = com[3]
            dt.append(nom_commune)
            nom_base = str(nom_commune).strip().replace(' ', '_').lower() + "_d_" +  str(com[11]).replace(' ', '_').replace('-', '_').lower()
            self.NOM_BASE.append(nom_base)
            dt.append(nom_base)
            dataToShow.append(dt)

        self.showInTable(dataToShow)

    def getAllCommunes(self):
        res = None
        try:
            cur = self.connexion.cursor()
            cur.execute('SELECT DISTINCT c.*, d.nomdistrict FROM commune c INNER JOIN district d ON c.iddistrict = d.iddistrict')
            res = cur.fetchall()
        except Exception as err:
            print err
            self.connexion.rollback()
        return res

    def launch(self):
        if self.type != "pg_dump":
            if self.FILESAVE == '':
                QtGui.QMessageBox.critical(None, u"Erreur", u"Le fichier permettant la création de la base vide n'a pas pu être chargé")
                return
            else:
                if self.empty:
                    texte = u"Voulez vous vraiment créer les base de données vide portant les nom " + str(self.NOM_BASE) + " ?"
                    reply = Qt.QMessageBox.question(self, "Attention",texte,
                                                       Qt.QMessageBox.Yes | Qt.QMessageBox.No, Qt.QMessageBox.No)
                    if reply == Qt.QMessageBox.No:
                        return

        self.ui.cancel.setEnabled(False)
        self.ui.launch.setEnabled(False)
        pgdump = self.get_pgdump_path()
        self.ui.listWidget.clear()
        self.message_added("Recuperation de l'executable %s" % self.type)
        self.progress(0)
        self.thread = SeparationBaseThread(pgdump=pgdump, filename=self.FILESAVE, nomBase=self.NOM_BASE, communes = self.communes, connexion = self.connexion)
        self.thread.messageAddedSignal.connect(self.message_added)
        self.thread.updateProgreesSignal.connect(self.progress)
        self.thread.doneSignal.connect(self.export_done)
        self.message_added("Debut de l'export" if self.type == "pg_dump" else "Debut de l'import")
        #self.progress(60)
        self.thread.start()
        return

    def message_added(self, m):
        pass
        step = QtGui.QListWidgetItem(m)
        step.setIcon(QtGui.QIcon(":/std/icone/accept.png"))
        self.ui.listWidget.addItem(step)
        self.ui.listWidget.scrollToBottom()

    def progress(self, p):
        self.ui.progressBar.setValue(p)

    def export_done(self):
        self.progress(100)
        QtGui.QMessageBox.information(
            self,
            "Termine",
            "L'export de la base est termine" if self.type == "pg_dump" else
            "L'import de la base est termine\nL'application va maintenant se fermer."
        )
        if self.type == "pg_restore":
            self.close()
            self.parent.MainWindow.close()
        self.ui.cancel.setEnabled(True)
        self.ui.launch.setEnabled(True)

    def current_datebase(self):
        self.cursor.execute("SELECT current_database()")
        dm = self.cursor.fetchone()
        size = len(dm)
        if size >= 1:
            self.CURRENT_DB = dm[0]
        else:
            print "FAILED loaded DB"

    def current_dbuser(self):
        self.cursor.execute("SELECT user")
        dm = self.cursor.fetchone()
        size = len(dm)
        if size >= 1:
            self.CURRENT_USER = dm[0]
            print self.CURRENT_USER
        else:
            print "FAILED loaded DB"

    def toLowerField(self):
        pass

    def editIniFile(self):
        self.parser = SafeConfigParser()
        self.parser.read(self.resolve("app.ini"))
        self.db_name = self.parser.get('database', 'name')
        self.parser.set('database', 'name', self.NOM_BASE)
        with open(self.resolve('app.ini'), 'wb') as configFile:
            self.parser.write(configFile)
        #QtGui.QMessageBox.information(self, 'informartion', u"Modification réussi! L'application doit s'arreter pour prendre en compte la modification.")
        self.close()
        sys.exit()

    def resolve(self, name, basepath=None):
        if not basepath:
            basepath = os.path.dirname(os.path.realpath(__file__))
            base = basepath.replace('Parametres', 'Configuration')
            print base
        return os.path.join(base, name)

    def showInTable(self, data):
        self.ui.tableWidget.setRowCount(0)
        i = 0
        while i < len(data):
            rowPosition = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(rowPosition)
            # self.idPersonnePhysiques.append(data[i][0])
            j = 0
            while j < len(data[i]):
                self.ui.tableWidget.setItem(rowPosition, j , QTableWidgetItem(unicode(data[i][j])))
                j = j + 1
            i = i + 1
