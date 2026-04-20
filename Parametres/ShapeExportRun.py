from PyQt4 import QtGui, Qt
from FormExport import Ui_Export
from .ShapeExportThread import ShapeExportThread
from os.path import expanduser
import os
import psycopg2
from plof import Plof


class ShapeExportRun(Qt.QDialog):
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
        self.output = []
        self.current_datebase()
        self.current_dbuser()
        self.ui.find.clicked.connect(self.upload_file)
        self.ui.launch.clicked.connect(self.launch)
        self.ui.cancel.clicked.connect(self.reject)
        if exetype == "pgsql2shp":
            self.setWindowTitle("Exporter Shape Demande et Certificat")
            self.ui.launch.setText("Lancer l'export en shapefile")
            self.ui.labelNomBase.hide()
            self.ui.lineEditNomBase.hide()
            self.ui.checkBoxConnectDB.hide()
            self.ui.label.setText("Choisir un dossier")
        self.type = exetype

    def get_pgsql2shp_path(self):
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
        if self.type == "pgsql2shp":
            #filename = QtGui.QFileDialog.getSaveFileName(self, 'Open File', expanduser("~"), '*.backup;;*.tar;;*.sql')
            try:
                filename = QtGui.QFileDialog.getExistingDirectory(self, "Choisissez un dossier")
                print ('open folder')
            except Exception as err:
                print err
        else:
            #filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', expanduser("~"), '*.backup;;*.tar;;*.sql')
            filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', expanduser("~"), '*.shp')
        self.FILESAVE = str(filename)
        self.ui.filename.setText(str(filename))

    def launch(self):
        self.ui.cancel.setEnabled(False)
        self.ui.launch.setEnabled(False)
        self.ui.find.setEnabled(False)
        self.ui.listWidget.clear()
        pgsql2shp = self.get_pgsql2shp_path()
        self.message_added("Recuperation de l'executable %s" % self.type)
        self.progress(30)
        self.thread = ShapeExportThread(pgdump=pgsql2shp, filename=self.FILESAVE)
        self.thread.messageAddedSignal.connect(self.message_added)
        self.thread.doneSignal.connect(self.export_done)
        self.message_added("Debut de l'export" if self.type == "pg_dump" else "Debut de l'export")
        self.progress(60)
        try:
            self.thread.start()
        except Exception as err:
            print(err)
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
            "L'export des shapefiles est termine" if self.type == "pgsql2shp" else
            "L'import de la base est termine\nL'application va maintenant se fermer."
        )
        if self.type == "pg_restore":
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

