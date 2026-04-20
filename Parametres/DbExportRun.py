#coding: utf8
from PyQt4 import QtGui, Qt, QtCore
from FormExport import Ui_Export
from .DbExportThread import DbExportThread
from os.path import expanduser
import os, sys
import psycopg2
import re
from Configuration import DbConfig
from plof import Plof
from ConfigParser import SafeConfigParser
import globalvars



class DbExportRun(Qt.QDialog):
    parent = None  # type: Plof

    def __init__(self, parent, exetype, empty = False, isImportData= False):
        Qt.QDialog.__init__(self)
        self.ui = Ui_Export()
        self.ui.setupUi(self)
        self.parent = parent
        self.connexion = self.parent.connection
        self.cursor = self.connexion.cursor()
        self.thread = None
        self.LOGIN = ''
        self.PASSWORD = ''
        self.FILESAVE = ''
        self.CURRENT_DB = ''
        self.CURRENT_USER = ''
        self.NOM_BASE = None
        self.isImportData = False
        self.output = []
        self.current_datebase()
        self.current_dbuser()
        self.ui.find.clicked.connect(self.upload_file)
        self.ui.launch.clicked.connect(self.launch)
        self.ui.cancel.clicked.connect(self.reject)
        self.db_config = DbConfig.DbConfig()
        self.empty = empty
        self.isImportData = isImportData
        validatorNomBase = Qt.QRegExpValidator(globalvars.regexpNomBase)
        self.ui.lineEditNomBase.setValidator(validatorNomBase)
        if self.empty:
            self.ui.filename.hide()
            self.ui.find.hide()
            self.ui.label.hide()
            self.ui.labelNomBase.setText(u"Nom de la base à créer")
            dirname = os.path.dirname(__file__)
            filename =os.path.join(dirname, "empty_db_fiplof.sql")
            print "*******************filename******************"
            print filename
            self.FILESAVE = str(filename)
            self.ui.filename.setText(str(filename))
        #self.ui.lineEditNomBase.textChanged.connect(self.toLowerField)
        if exetype == "pg_dump":
            self.setWindowTitle("Exporter BD")
            self.ui.labelNomBase.hide()
            self.ui.lineEditNomBase.hide()
            self.ui.checkBoxConnectDB.hide()
        else:
            self.setWindowTitle("Importer BD")
            self.ui.launch.setText("Lancer l'import")
            if self.empty:
                self.setWindowTitle(u"Création nouvelle base vide")
                self.ui.launch.setText(u"Créer la base")
            self.ui.labelNomBase.show()
            self.ui.lineEditNomBase.show()
            if not self.empty:
                self.ui.lineEditNomBase.setText(self.db_config.db_name)
            if isImportData:
                self.setWindowTitle(u"IMPORT DE DONNEES")
                self.ui.launch.setText("Lancer l'import")
                self.ui.labelNomBase.hide()
                self.ui.lineEditNomBase.hide()
                self.ui.lineEditNomBase.setText(self.db_config.db_name)


            self.ui.checkBoxConnectDB.show()
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
        if self.type == "pg_dump":
            #filename = QtGui.QFileDialog.getSaveFileName(self, 'Open File', expanduser("~"), '*.backup;;*.tar;;*.sql')
            filename = QtGui.QFileDialog.getSaveFileName(self, 'Open File', expanduser("~"), '*.sql')
        else:
            #filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', expanduser("~"), '*.backup;;*.tar;;*.sql')
            if not self.empty:
                if self.isImportData:
                    filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', expanduser("~"), '*.7z')
                else:
                    filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', expanduser("~"), '*.sql')
        self.FILESAVE = str(filename)
        self.ui.filename.setText(str(filename))

    def launch(self):
        if self.type != "pg_dump":
            if str(self.ui.lineEditNomBase.text()).strip() =='' or self.FILESAVE == '':
                QtGui.QMessageBox.critical(None, u"Erreur", u"Le nom de la base de données et le fichier sql sont obligatoires")
                return
            else:
                regex = r"é+|è+|à+|ç+|ù+|ô+|ê+|â+|@+|%+|\*+|\?+|\s+|:+|/+|\\+|\*+|\-+"
                x = re.compile(regex)
                if re.match(regex, str(self.ui.lineEditNomBase.text()).strip().lower()):
                    QtGui.QMessageBox.critical(None, u"Erreur", u"Le nom de la base de données ne doit ni comporter d'espace, ni de caractères spéciaux, ni d'accents!")
                    return
                else:
                    self.NOM_BASE = str(self.ui.lineEditNomBase.text()).strip()

                if self.empty:
                    texte = u"Voulez vous vraiment créer une base de données vide portant le nom " + self.NOM_BASE + " ?"
                    reply = Qt.QMessageBox.question(self, "Attention",texte,
                                                       Qt.QMessageBox.Yes | Qt.QMessageBox.No, Qt.QMessageBox.No)
                    if reply == Qt.QMessageBox.No:
                        return
                else:
                    texte = u"Voulez vous vraiment restaurer la base de données portant le nom " + self.NOM_BASE + u" ? Cette action sera irréversible."
                    reply = Qt.QMessageBox.question(self, "Attention", texte,
                                                    Qt.QMessageBox.Yes | Qt.QMessageBox.No, Qt.QMessageBox.No)
                    if reply == Qt.QMessageBox.No:
                        return

        self.ui.cancel.setEnabled(False)
        self.ui.launch.setEnabled(False)
        self.ui.find.setEnabled(False)
        self.ui.listWidget.clear()
        pgdump = self.get_pgdump_path()
        self.message_added("Recuperation de l'executable %s" % self.type)
        self.progress(30)
        self.thread = DbExportThread(pgdump=pgdump, filename=self.FILESAVE, nomBase=self.NOM_BASE, isImportData=self.isImportData )
        self.thread.messageAddedSignal.connect(self.message_added)
        self.thread.doneSignal.connect(self.export_done)
        self.message_added("Debut de l'export" if self.type == "pg_dump" else "Debut de l'import")
        self.progress(60)
        print ('launch ')
        self.thread.start()
        print ('fin launch thread')
        return

    def message_added(self, m):
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
            if self.ui.checkBoxConnectDB.isChecked():
                try:
                    self.editIniFile()
                except Exception as err:
                    print err
            self.close()
            self.parent.MainWindow.close()
        self.ui.cancel.setEnabled(True)
        self.ui.launch.setEnabled(True)
        self.ui.find.setEnabled(True)

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
        self.ui.lineEditNomBase.setText(self.ui.lineEditNomBase.text().toLower())

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
