# coding: utf-8
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QDialog
from .UiTypePersonneMorale import Ui_Dialog
import psycopg2


class TypePersonneMoraleRun(QDialog):
    def __init__(self, connection, idtype=0):
        QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.connection, self.idtype = connection, idtype
        self.init_fields()
        self.init_actions()

    def init_actions(self):
        self.ui.pushButtonAnnuler.clicked.connect(self.reject)
        self.ui.pushButtonEnregistrer.clicked.connect(self.save)

    def init_fields(self):
        if not self.idtype:
            return
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT * FROM typepersonnemorale WHERE idtype = %s", (self.idtype, ))
            row = cursor.fetchone()
            self.ui.lineEditType.setText(row["type"])
            self.ui.lineEditKarazany.setText(row["karazana"])
        except Exception as e:
            print(e)
        cursor.close()

    def save(self):
        if self.ui.lineEditType.text() == "":
            self.ui.lineEditType.setFocus()
            return
        if self.ui.lineEditKarazany.text() == "":
            self.ui.lineEditKarazany.setFocus()
            return
        cursor = self.connection.cursor()
        a = unicode(self.ui.lineEditType.text()).encode('utf-8')
        b = unicode(self.ui.lineEditKarazany.text()).encode('utf-8')
        try:
            if self.idtype:
                cursor.execute("UPDATE typepersonnemorale SET type=%s, karazana=%s WHERE idtype=%s", (a, b, self.idtype))
            else:
                cursor.execute("INSERT INTO typepersonnemorale(type, karazana) VALUES(%s, %s)", (a, b))
            self.connection.commit()
        except Exception as e:
            print(e)
            self.connection.rollback()
        cursor.close()
        self.accept()