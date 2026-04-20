#coding: utf8
from PyQt4 import QtGui, Qt
from FormExport import Ui_Export
from .DbUpdateThread import DbUpdateThread
from os.path import expanduser
import os, sys
import psycopg2
import re
from Configuration import DbConfig
from plof import Plof
from ConfigParser import SafeConfigParser



class DbUpdateRun(Qt.QDialog):
    parent = None  # type: Plof

    def __init__(self, parent, exetype):
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
        self.output = []
        self.current_datebase()
        self.current_dbuser()
        self.ui.find.clicked.connect(self.upload_file)
        self.ui.launch.clicked.connect(self.launch)
        self.ui.cancel.clicked.connect(self.reject)
        self.db_config = DbConfig.DbConfig()
        #self.ui.lineEditNomBase.textChanged.connect(self.toLowerField)
        if exetype == "pg_dump":
            self.setWindowTitle("Exporter BD")
            self.ui.labelNomBase.hide()
            self.ui.lineEditNomBase.hide()
            self.ui.checkBoxConnectDB.hide()
        else:
            self.setWindowTitle(u"Mise à jour BD")
            self.ui.launch.setText(u"Lancer la mise à jour")
            self.ui.labelNomBase.show()
            self.ui.lineEditNomBase.show()
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

        self.ui.cancel.setEnabled(False)
        self.ui.launch.setEnabled(False)
        self.ui.find.setEnabled(False)
        self.ui.listWidget.clear()
        pgdump = self.get_pgdump_path()
        self.message_added("Recuperation de l'executable %s" % self.type)
        self.progress(30)
        self.thread = DbUpdateThread(pgdump=pgdump, filename=self.FILESAVE, nomBase=self.NOM_BASE)
        self.thread.messageAddedSignal.connect(self.message_added)
        self.thread.doneSignal.connect(self.export_done)
        self.message_added("Debut de l'export" if self.type == "pg_dump" else "Debut de l'import")
        self.progress(60)
        self.thread.start()
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
        self.ui.lineEditNomBase.setText(self.ui.lineEditNomBase.text())

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
