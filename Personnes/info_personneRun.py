#coding: utf8
from PyQt4.QtGui import *
from PyQt4 import QtGui
from PyQt4 import QtCore, Qt
from PyQt4.QtCore import *
import time, psycopg2, datetime, os, sys
from psycopg2.extensions import *
from .info_personne import Ui_Dialog
import globalvars
from Utilisateur import AccesManager
import psycopg2.extras
import tempfile
#sys.setrecursionlimit(1500)
import os

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class info_personneRun(QDialog):
    def __init__(self, connection, idpersonne):
        QDialog.__init__(self)
        self.setModal(True)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setModal(True)
        self.idpersonne = idpersonne
        self.connection = connection
        self.paths = []
        self.path_cin_recto_r = None
        self.path_cin_verso_r = None
        self.path_signature_r = None
        self.path_empreinte_d_r = None
        self.path_empreinte_g_r = None
        self.initActions()
        self.readByteA(self.idpersonne)
        self.ui.tabWidgetIdentite.setCurrentIndex(0)
        self.ui.tabWidgetIdentite.removeTab(3)
        self.ui.tabWidgetIdentite.removeTab(3)
        self.setWindowTitle(u"Preuves d'identités")

    def initActions(self):
        self.ui.toolButtonParcourirCinRecto.clicked.connect(self.browseFile)
        self.ui.toolButtonParcourirVerso.clicked.connect(self.browseFile)
        self.ui.toolButtonParcourirSignature.clicked.connect(self.browseFile)
        self.ui.toolButtonParcourirEmpreinteD.clicked.connect(self.browseFile)
        self.ui.toolButtonParcourirEmpreinteG.clicked.connect(self.browseFile)
        self.ui.pushButtonModifier.clicked.connect(self.readFileInput)
        self.ui.pushButtonFermer.clicked.connect(self.close)
        self.ui.pushButtonSupprimer.clicked.connect(self.deleteCol)

    def browseFile(self):
        self.senderName = self.sender().objectName()
        if str(self.senderName).strip() == "toolButtonParcourirCinRecto":
            try:
                self.path_cin_recto_r = QtGui.QFileDialog.getOpenFileName(self, "Choisir un fichier image", "",
                                                                  u"Fichiers image (*.jpeg;*.jpg; *.png)")
                self.ui.lineEditCinRecto.setText(self.path_cin_recto_r)
            except Exception as err:
                print (err)

        if str(self.senderName).strip() == "toolButtonParcourirVerso":
            try:
                self.path_cin_verso_r = QtGui.QFileDialog.getOpenFileName(self, "Choisir un fichier image", "",
                                                                  u"Fichiers image (*.jpeg;*.jpg; *.png)")
                self.ui.lineEditCinVerso.setText(self.path_cin_verso_r)
            except Exception as err:
                print (err)

        if str(self.senderName).strip() == "toolButtonParcourirSignature":
            try:
                self.path_signature_r = QtGui.QFileDialog.getOpenFileName(self, "Choisir un fichier image", "",
                                                                  u"Fichiers image (*.jpeg;*.jpg; *.png)")
                self.ui.lineEditCinSignature.setText(self.path_signature_r)
            except Exception as err:
                print (err)

        if str(self.senderName).strip() == "toolButtonParcourirEmpreinteD":
            try:
                self.path_empreinte_d_r = QtGui.QFileDialog.getOpenFileName(self, "Choisir un fichier image", "",
                                                                  u"Fichiers image (*.jpeg;*.jpg; *.png)")
                self.ui.lineEditEmpreinteD.setText(self.path_empreinte_d_r)
            except Exception as err:
                print (err)

        if str(self.senderName).strip() == "tollButtonParcourirEmpreinteG":
            try:
                self.path_empreinte_g_r = QtGui.QFileDialog.getOpenFileName(self, "Choisir un fichier image", "",
                                                                  u"Fichiers image (*.jpeg;*.jpg; *.png)")
                self.ui.lineEditEmpreinteG.setText(self.path_empreinte_g_r)
            except Exception as err:
                print (err)

    def readFileInput(self):
        #Lecture des data from database
        reply = QtGui.QMessageBox.question(self, "Attention", "Etes vous sure de vouloir modifier ces informations?",
                                           QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.No:
            return

        res = None
        cur = self.connection.cursor()
        try:
            cur.execute('SELECT * FROM blob_personne WHERE idpersonne = %s', (str(self.idpersonne),))
            res = cur.fetchone()
        except Exception as err:
            print err
            self.connection.rollback()
        cur.close()

        # Lecture signature
        nom_fic_signature = None
        ext_signature = None
        signature = ''
        if self.path_signature_r is not None and str(self.path_signature_r).strip() != '':
            signature = str(self.path_signature_r).decode('utf-8').strip()
            tab = signature.replace('\\', '/').split('.')
            ext_signature = tab[len(tab) - 1]
            tab_name_fic = tab[0].split('/')
            nom_fic_signature = tab_name_fic[len(tab_name_fic) - 1]
            # time.sleep(2)
            signat = signature.replace('\\', '/')
            signature = signat

        nom_fic_cin_recto = None
        ext_cin_recto = None
        cin_recto = ''
        if self.path_cin_recto_r is not None and str(self.path_cin_recto_r).strip() != '':
            cin_recto = str(self.path_cin_recto_r).decode('utf-8').strip()
            tab = cin_recto.replace('\\', '/').split('.')
            ext_cin_recto = tab[len(tab) - 1]
            tab_name_fic = tab[0].split('/')
            nom_fic_cin_recto = tab_name_fic[len(tab_name_fic) - 1]
            cin_rect = cin_recto.replace('\\', '/')
            cin_recto = cin_rect

        nom_fic_cin_verso = None
        cin_verso = ''
        ext_cin_verso = None
        if self.path_cin_verso_r is not None and str(self.path_cin_verso_r).strip() != '':
            cin_verso = str(self.path_cin_verso_r).decode('utf-8').strip()
            tab = cin_verso.replace('\\', '/').split('.')
            ext_cin_verso = tab[len(tab) - 1]
            tab_name_fic = tab[0].split('/')
            nom_fic_cin_verso = tab_name_fic[len(tab_name_fic) - 1]
            cin_vers = cin_verso.replace('\\', '/')
            cin_verso = cin_vers

        print cin_recto

        print cin_verso

        # Full path

        signature_path = str(self.path_signature_r).decode('utf-8')
        cin_recto_path = str(self.path_cin_recto_r).decode('utf-8')
        cin_verso_path = str(self.path_cin_verso_r).decode('utf-8')

        print "path defined"
        print cin_recto_path
        signature_file = None
        cin_recto_file = None
        cin_verso_file = None
        if signature != '' and os.path.isfile(signature_path):
            try:
                signature_file = open(signature_path, 'rb').read()
                print "fichier signature ouvert"
                self.saveToHistory(self.idpersonne,'signature',signature_file,ext_signature, nom_fic_signature)
            except Exception as err:
                print ("Erreur ouverture fichier signature" + err)
        else:
            if res is not None:
                signature_file = res[4]
                nom_fic_signature = res[11]
                ext_signature = res[12]

        if cin_recto != '' and os.path.isfile(cin_recto_path):
            try:
                cin_recto_file = open(cin_recto_path, 'rb').read()
                print "fichier cin_recto ouvert"
                self.saveToHistory(self.idpersonne, 'cin_recto', cin_recto_file, ext_cin_recto, nom_fic_cin_recto)
            except Exception as err:
                print ("Erreur ouverture fichier cin recto" + err)
        else:
            if res is not None:
                cin_recto_file = res[2]
                nom_fic_cin_recto = res[7]
                ext_cin_recto = res[8]

        if cin_verso != '' and os.path.isfile(cin_verso_path):
            try:
                cin_verso_file = open(cin_verso_path, 'rb').read()
                print "fichier cin_verso ouvert"
                self.saveToHistory(self.idpersonne, 'cin_verso', cin_verso_file, ext_cin_verso, nom_fic_cin_verso)
            except Exception as err:
                print ("Erreur ouverture fichier cin verso" + err)
        else:
            if res is not None:
                cin_verso_file = res[3]
                nom_fic_cin_verso = res[9]
                ext_cin_verso = res[10]

        if signature_file is not None or cin_recto_file is not None or cin_verso_file is not None:
            print "1 of all is not none"
            print str(self.idpersonne).strip()
            if self.exists("blob_personne", "idpersonne", str(self.idpersonne).strip()):
                print  "here is my test"
                try:
                    self.insertBlobFiles(idpersonne=self.idpersonne, cin_recto=cin_recto_file,
                                         cin_verso=cin_verso_file, signature=signature_file,
                                         edit_mode=1, ext_signature=ext_signature,
                                         ext_cin_recto=ext_cin_recto, ext_cin_verso=ext_cin_verso,
                                         nom_signature=nom_fic_signature,
                                         nom_cin_recto=nom_fic_cin_recto,
                                         nom_cin_verso=nom_fic_cin_verso)
                except Exception as err:
                    print(err)
            else:
                print  "here is my test 2"
                try:
                    self.insertBlobFiles(idpersonne=self.idpersonne, cin_recto=cin_recto_file, cin_verso=cin_verso_file,
                                         signature=signature_file, edit_mode=0, ext_signature=ext_signature,
                                         ext_cin_recto=ext_cin_recto, ext_cin_verso=ext_cin_verso,
                                         nom_signature=nom_fic_signature, nom_cin_recto=nom_fic_cin_recto,
                                         nom_cin_verso=nom_fic_cin_verso)
                except Exception as err:
                    print(err)
        self.readByteA(self.idpersonne)


    def readByteA(self, idpersonne):
        self.ui.graphicsViewCinRecto.hide()
        self.ui.graphicsViewCinVerso.hide()
        self.ui.graphicsViewSignature.hide()
        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cur.execute("SELECT * FROM blob_personne WHERE idpersonne = %s ",
                        (idpersonne,))
            res = cur.fetchall()
            print res
        except Exception as err:
            print (err)
            self.connection.rollback()

        path1 = None
        path2 = None
        path3 = None
        path4 = None
        path5 = None
        for colon in res:
            # name = colon[1]
            #Contenus
            file_cin_recto = colon['cin_recto']
            file_cin_verso = colon['cin_verso']
            file_signature = colon['signature']
            file_empreinte_d = colon['empreinte_d']
            file_empreinte_g = colon['empreinte_g']
            #print file_empreinte_d
            name_cin_recto = colon['cin_recto_name']
            name_cin_verso = colon['cin_verso_name']
            name_signature = colon['signature_name']
            name_empreinte_g = colon['empreinte_g_name']
            name_empreinte_d = colon['empreinte_d_name']
            #Extensions
            ext_cin_recto = colon['cin_recto_type']
            ext_cin_verso = colon['cin_verso_type']
            ext_signature = colon['signature_type']
            ext_empreinte_g = colon['empreinte_g_type']
            ext_empreinte_d = colon['empreinte_d_type']

            print("Stocker le fichier sur le disque \n")
            if file_cin_recto is not None:
                path1 = os.path.join(tempfile.gettempdir(), name_cin_recto + "." + ext_cin_recto)
            if file_cin_verso is not None:
                path2 = os.path.join(tempfile.gettempdir(), name_cin_verso + "." + ext_cin_verso)
            if file_signature is not None:
                path3 = os.path.join(tempfile.gettempdir(), name_signature + "." + ext_signature)
            if file_empreinte_d is not None:
                path4 = os.path.join(tempfile.gettempdir(), name_empreinte_d + "." + ext_empreinte_d)
            if file_empreinte_g is not None:
                path5 = os.path.join(tempfile.gettempdir(), name_empreinte_g + "." + ext_empreinte_g)
            print ("after path def")

        # Convertir les donnees binaires au format
        # approprie et les ecrire sur le disque dur
        if path1 is not None:
            try:
                with open(path1, 'wb') as myfile:
                    myfile.write(file_cin_recto)
                #print("Le fichier stockees dans: ", path1, "\n")
                self.ui.graphicsViewCinRecto.show()
                self.showInScene(path1,self.ui.graphicsViewCinRecto)
                self.paths.append(path1)
            except Exception as err:
                print (err)
        if path2 is not None:
            try:
                with open(path2, 'wb') as myfile:
                    myfile.write(file_cin_verso)
                #print("Le fichier stockees dans: ", path2, "\n")
                self.ui.graphicsViewCinVerso.show()
                self.showInScene(path2, self.ui.graphicsViewCinVerso)
                self.paths.append(path2)
            except Exception as err:
                print (err)
        if path3 is not None:
            try:
                with open(path3, 'wb') as myfile:
                    myfile.write(file_signature)
                #print("Le fichier stockees dans: ", path3, "\n")
                self.ui.graphicsViewSignature.show()
                self.showInScene(path3, self.ui.graphicsViewSignature, True)
                self.paths.append(path3)
            except Exception as err:
                print (err)
        if path4 is not None:
            with open(path4, 'wb') as myfile:
                myfile.write(file_empreinte_d)
            #print("Le fichier stockees dans: ", path4, "\n")
            self.showInScene(path4, self.ui.graphicsViewEmpreinteD, True)
            self.paths.append(path4)
        if path5 is not None:
            try:
                with open(path5, 'wb') as myfile:
                    myfile.write(file_empreinte_g)
                #print("Le fichier stockees dans: ", path5, "\n")
                self.showInScene(path5, self.ui.graphicsViewEmpreinteG, True)
                self.paths.append(path5)
            except Exception as err:
                print (err)

        # fermeture de la connexion à la base de données
        cur.close()

    def showInScene(self, path, graphics_view, isSignature = False):
        rez = QtCore.QSize(graphics_view.height(),graphics_view.width())
        pix = QPixmap(path)
        pix2 = pix.scaledToWidth(600)
        item = QGraphicsPixmapItem(pix2)
        scene = QGraphicsScene(self)
        scene.addItem(item)
        graphics_view.setScene(scene)

    def __del__(self):
        for path in self.paths:
            try:
                os.remove(path)
            except Exception as err:
                print err

    def insertBlobFiles(self, idpersonne, cin_recto = None, cin_verso = None, signature = None, empreinte_d = None, empreinte_g = None, edit_mode = 0, ext_signature = None, ext_cin_recto = None, ext_cin_verso = None, nom_signature = None, nom_cin_recto = None, nom_cin_verso = None):
        print "INSERT BLOB FILES"
        cur = self.connection.cursor()
        if edit_mode == 0:
            try:
                cur.execute('INSERT INTO blob_personne (idpersonne,cin_recto , cin_verso, signature, empreinte_d, empreinte_g, '
                            'signature_type, cin_recto_type, cin_verso_type, signature_name, cin_recto_name, cin_verso_name ) '
                            'VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s) ',
                            (idpersonne, psycopg2.Binary(cin_recto), psycopg2.Binary(cin_verso),psycopg2.Binary(signature),
                             psycopg2.Binary(empreinte_d), psycopg2.Binary(empreinte_g), ext_signature, ext_cin_recto, ext_cin_verso,
                             nom_signature, nom_cin_recto, nom_cin_verso))
                self.connection.commit()
                print "INSERTION REUISSI"
                self.etatInsertion = self.etatInsertion + "INSERTION SIGNATURE REUSSIE\n"
            except Exception as err:
                print err
                self.etatInsertion = self.etatInsertion + "ECHEC INSERTION SIGNATURE \n"
                self.erreur = self.erreur + "ERREUR SIGNATURE " + str(err) + "\n"
                self.connection.rollback()
        else:
            try:
                cur.execute(
                    'UPDATE blob_personne SET cin_recto = %s , cin_verso = %s, signature = %s, empreinte_d = %s, empreinte_g = %s, '
                    'signature_type = %s, cin_recto_type = %s, cin_verso_type = %s, signature_name = %s, cin_recto_name = %s, cin_verso_name = %s '
                    ' where idpersonne = %s',
                    ( psycopg2.Binary(cin_recto), psycopg2.Binary(cin_verso), psycopg2.Binary(signature),
                     psycopg2.Binary(empreinte_d), psycopg2.Binary(empreinte_g), ext_signature, ext_cin_recto,
                     ext_cin_verso,
                     nom_signature, nom_cin_recto, nom_cin_verso, idpersonne))
                self.connection.commit()
                print "MODIFICATION REUSSIE"
                self.etatInsertion = self.etatInsertion + "MODIFICATION SIGNATURE REUSSIE\n"
            except Exception as err:
                print err
                self.etatInsertion = self.etatInsertion + "ECHEC MODIFICATION SIGNATURE \n"
                self.erreur = self.erreur + "ERREUR SIGNATURE " + str(err) + "\n"
                self.connection.rollback()

    def exists(self, table, column, value):
        sql = "SELECT %s FROM %s WHERE %s=" % (column, table, column)
        cursor = self.connection.cursor()
        cursor.execute(sql + "%s", (value,))
        rows = cursor.fetchall()
        cursor.close()
        return len(rows) > 0

    def saveToHistory(self, idpersonne, nature, new_file, new_ext, new_name):
        print "call of save to history blob"
        #get blob file
        res = None
        old_file = None
        old_file_name = None
        old_file_ext = None

        cur = self.connection.cursor()
        try:
            cur.execute('SELECT * FROM blob_personne WHERE idpersonne = %s', (str(idpersonne),))
            res = cur.fetchone()
        except Exception as err:
            print err
            self.connection.rollback()

        cur.close()

        if res is not None:
            datejour = datetime.date.today()
            if nature == "cin_recto":
                old_file = res[2]
                old_file_name = res[7]
                old_file_ext = res[8]
            if nature == "cin_verso":
                old_file = res[3]
                old_file_name = res[9]
                old_file_ext = res[10]
            if nature == "signature":
                old_file = res[4]
                old_file_name = res[11]
                old_file_ext = res[12]

            curs = self.connection.cursor()
            try:
                curs.execute('INSERT INTO blob_history (idpersonne, idutilisateur, old_file, new_file, old_file_type, new_file_type, datemodification, old_file_name, new_file_name, nature) '
                             'VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s)', (str(idpersonne),str(globalvars.id_user), psycopg2.Binary(old_file), psycopg2.Binary(new_file), old_file_ext, new_ext,datejour, old_file_name,
                                                                                new_name, nature))
                self.connection.commit()
            except Exception as err:
                print err
                self.connection.rollback()

            curs.close()

    def deleteBlobData(self, idpersonne, nature):
        print "call of delete blod data"
        new_file = None
        new_ext = None
        new_name = None
        self.saveToHistory(idpersonne, nature, new_file, new_ext, new_name)
        curs = self.connection.cursor()
        if nature == 'cin_recto':
            try:
                curs.execute('UPDATE blob_personne SET cin_recto = NULL, cin_recto_name = NULL, cin_recto_type = NULL WHERE idpersonne = %s', (str(idpersonne),))
                self.connection.commit()
            except Exception as err:
                print err
                self.connection.rollback()

        if nature == 'cin_verso':
            try:
                curs.execute('UPDATE blob_personne SET cin_verso = NULL, cin_verso_name = NULL, cin_verso_type = NULL WHERE idpersonne = %s', (str(idpersonne),))
                self.connection.commit()
            except Exception as err:
                print err
                self.connection.rollback()

        if nature == 'signature':
            try:
                curs.execute('UPDATE blob_personne SET signature = NULL, signature_name = NULL, signature_type = NULL WHERE idpersonne = %s', (str(idpersonne),))
                self.connection.commit()
            except Exception as err:
                print err
                self.connection.rollback()

    def deleteCol(self):
        print "call of delete col"
        nature = ''
        texte_avertissement = ''
        if self.ui.tabWidgetIdentite.currentIndex() == 0:
            nature = 'cin_recto'
            texte_avertissement = u"Etes vous sure de vouloir supprimer le CIN recto de cet individu?"

        if self.ui.tabWidgetIdentite.currentIndex() == 1:
            nature = 'cin_verso'
            texte_avertissement = u"Etes vous sure de vouloir supprimer le CIN verso de cet individu?"

        if self.ui.tabWidgetIdentite.currentIndex() == 2:
            nature = 'signature'
            texte_avertissement = u"Etes vous sure de vouloir supprimer la signature de cet individu?"
        if nature != '':
            try:
                reply = QtGui.QMessageBox.question(self, "Attention", texte_avertissement,
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            except Exception as err:
                print err
            print "ato er"
            if reply == QtGui.QMessageBox.No:
                return
            self.deleteBlobData(self.idpersonne, nature)
            self.readByteA(self.idpersonne)