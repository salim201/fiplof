# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from .AddLayerAdministration import Ui_Dialog
from models.ProjetCouche import ProjetCouche
from Utils import Utils
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class AddLayerAdministrationRun(QtGui.QDialog):
    """docstring for AddLayerRun"""
    def __init__(self, connection, idprojet_commune, couche_id=0):
        super(AddLayerAdministrationRun, self).__init__()
        self.connection, self.idprojet_commune = connection, idprojet_commune
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.selected_color, self.couche_id = None, 0
        self.init_actions()
        self.ordre = 0
        if couche_id:
            couche = ProjetCouche.find_by_id(self.connection, couche_id)
            if couche:
                idx = 0
                if couche.type_couche == 'R':
                    idx = 1
                self.selected_color = QtGui.QColor(couche.couleur_bg)
                self.couche_id = couche.id
                #self.ui.lineEditLibelle.setText(couche.libelle)
                self.ui.comboBox.setCurrentIndex(self.ui.comboBox.findText(str(couche.libelle)))
                self.ui.comboBoxType.setCurrentIndex(idx)
                self.ui.pushButtonCouleur.setIcon(Utils.create_icon(QtGui.QColor(couche.couleur_bg)))
                self.ui.lineEditFichier.setText(couche.fichier)
                self.ordre = couche.ordre
                self.ui.pushButtonEnregistrer.setText("Enregistrer les Modifications")

    def init_actions(self):
        self.ui.comboBoxType.currentIndexChanged.connect(self.comboboxtype_indexchanged)
        self.ui.pushButtonAnnuler.clicked.connect(self.reject)
        self.ui.pushButtonParcourir.clicked.connect(self.browse_file)
        self.ui.pushButtonCouleur.clicked.connect(self.choose_color)
        self.ui.pushButtonEnregistrer.clicked.connect(self.save)

    def comboboxtype_indexchanged(self):
        visible = self.ui.comboBoxType.currentIndex() == 0
        self.ui.label_3.setVisible(visible)
        self.ui.pushButtonCouleur.setVisible(visible)

    def browse_file(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, "Choisissez un fichier")
        if not filename:
            return
        self.ui.lineEditFichier.setText(filename)

    def choose_color(self):
        dialog = QtGui.QColorDialog()
        if dialog.exec_():
            self.selected_color = dialog.selectedColor()
            self.ui.pushButtonCouleur.setIcon(Utils.create_icon(self.selected_color))

    def save(self):
        type_couche = 'S'
        if self.ui.comboBoxType.currentIndex() == 1:
            type_couche = 'R'
            self.selected_color = QtGui.QColor('white')
        if self.ui.comboBox.currentText().isEmpty():
            self.ui.comboBox.setFocus()
            return
        if type_couche == 'S' and not self.selected_color:
            self.ui.pushButtonCouleur.setFocus()
            return
        if self.ui.lineEditFichier.text().isEmpty():
            self.ui.pushButtonParcourir.setFocus()
            return
        p = ProjetCouche()
        p.id = self.couche_id
        p.libelle = str(self.ui.comboBox.currentText())
        p.fichier = str(self.ui.lineEditFichier.text())
        #p.fichier = "F:/doc imprimé plofs/TANA.ecw"

        p.idprojet_commune = self.idprojet_commune
        p.type_couche = type_couche
        p.couleur_bg = str(self.selected_color.name())
        p.ordre = self.ordre
        if not p.id:
            p.ordre = ProjetCouche.max_ordre_by_projet_commune(self.connection, self.idprojet_commune) + 1
        p.save(self.connection)
        self.accept()
