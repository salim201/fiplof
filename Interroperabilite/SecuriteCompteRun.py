# -*- coding: utf-8 -*-
import sys
import os

from PyQt4 import Qt, QtGui, QtCore

try:
    from thread import get_ident
except ImportError:
    from threading import get_ident

from SecuriteCompte import Ui_SecuriteCompte
from modeles.securiteCompteModel import SecuriteCompteModel

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class SecuriteCompteRun(QtGui.QDialog):
    def __init__(self, connection):
        self.connection = connection
        self.model = SecuriteCompteModel()
        self.model.setConnection(connection)
        self.current_compte_id = None
        
        QtGui.QDialog.__init__(self)
        self.setModal(True)
        self.ui = Ui_SecuriteCompte()
        self.ui.setupUi(self)
        
        self.ui.tableWidget_comptes.setColumnHidden(0, True)
        font = self.ui.tableWidget_comptes.font()
        font.setPointSize(9)
        self.ui.tableWidget_comptes.setFont(font)

        self.ui.btn_Activer.setVisible(False)
        self.ui.btn_Desactiver.setVisible(False)
        self.ui.btn_ValiderStatut.setVisible(False)
        self.ui.btn_RejeterStatut.setVisible(False)
        self.ui.btn_Reinitialiser.setVisible(False)
        self.ui.tableWidget_comptes.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.ui.label_login.setText("Login :")
        font2 = self.ui.comboBox_statut.font()
        font2.setPointSize(7)
        self.ui.comboBox_statut.setFont(font2)
        
        self.initActions()
        self.loadComptes()
        
    def initActions(self):
        pass
        
    def _u(self, val):
        if val is None:
            return u''
        if isinstance(val, unicode):
            return val
        if isinstance(val, str):
            return val.decode('utf-8')
        return unicode(val)
        
    def loadComptes(self, recherche=None):
        try:
            comptes = self.model.getAllComptes(recherche)
            
            self.ui.tableWidget_comptes.setRowCount(0)
            
            for compte in comptes:
                rowPosition = self.ui.tableWidget_comptes.rowCount()
                self.ui.tableWidget_comptes.insertRow(rowPosition)
                
                self.ui.tableWidget_comptes.setItem(rowPosition, 0, QtGui.QTableWidgetItem(str(compte['id_compte'])))
                self.ui.tableWidget_comptes.setItem(rowPosition, 1, QtGui.QTableWidgetItem(self._u(compte['login'])))
                self.ui.tableWidget_comptes.setItem(rowPosition, 2, QtGui.QTableWidgetItem(self._u(compte['nom'])))
                self.ui.tableWidget_comptes.setItem(rowPosition, 3, QtGui.QTableWidgetItem(self._u(compte['nom_systeme'])))
                
                actif_item = QtGui.QTableWidgetItem()
                actif_item.setText("Oui" if compte['actif'] else "Non")
                actif_item.setData(QtCore.Qt.UserRole, compte['actif'])
                self.ui.tableWidget_comptes.setItem(rowPosition, 4, actif_item)
                
                statut_item = QtGui.QTableWidgetItem()
                statut_item.setText(compte['statut'] or 'PENDING')
                self.ui.tableWidget_comptes.setItem(rowPosition, 5, statut_item)
                
                der_connex = compte['derniere_connexion']
                der_connex_str = der_connex.strftime('%Y-%m-%d %H:%M') if der_connex else '-'
                self.ui.tableWidget_comptes.setItem(rowPosition, 6, QtGui.QTableWidgetItem(der_connex_str))
                
                created = compte['created_at']
                created_str = created.strftime('%Y-%m-%d %H:%M') if created else '-'
                self.ui.tableWidget_comptes.setItem(rowPosition, 7, QtGui.QTableWidgetItem(created_str))
                
                self.ui.tableWidget_comptes.setRowHeight(rowPosition, 30)
                
            self.ui.tableWidget_comptes.resizeColumnsToContents()
            self.ui.tableWidget_comptes.setColumnWidth(1, 150)
            self.ui.tableWidget_comptes.setColumnWidth(2, 150)
            self.ui.tableWidget_comptes.setColumnWidth(3, 150)
            self.ui.tableWidget_comptes.setColumnWidth(4, 80)
            self.ui.tableWidget_comptes.setColumnWidth(5, 120)
            
            self.showMessage("{} compte(s) charg\u00e9(s)".format(len(comptes)))
            
        except Exception as e:
            print("Erreur loadComptes:", str(e))
            self.showMessage("Erreur lors du chargement des comptes", error=True)
    
    def on_btn_rechercher_clicked(self):
        recherche = self.ui.lineEdit_recherche.text().strip()
        self.loadComptes(recherche if recherche else None)
        
    def on_btn_actualiser_clicked(self):
        self.ui.lineEdit_recherche.clear()
        self.loadComptes()
        self.clearForm()
        
    def on_tableWidget_comptes_itemSelectionChanged(self):
        selected_items = self.ui.tableWidget_comptes.selectedItems()
        
        if not selected_items:
            return
            
        row = selected_items[0].row()
        
        id_compte = int(self.ui.tableWidget_comptes.item(row, 0).text())
        login = self.ui.tableWidget_comptes.item(row, 1).text()
        actif_item = self.ui.tableWidget_comptes.item(row, 4)
        actif = actif_item.data(QtCore.Qt.UserRole).toBool() if actif_item else False
        statut_item = self.ui.tableWidget_comptes.item(row, 5)
        statut = statut_item.text() if statut_item else 'PENDING'
        
        self.current_compte_id = id_compte
        self.ui.label_id_valeur.setText(str(id_compte))
        self.ui.label_login_valeur.setText(login)
        self.ui.checkBox_actif.setChecked(actif)
        
        index = self.ui.comboBox_statut.findText(statut)
        if index >= 0:
            self.ui.comboBox_statut.setCurrentIndex(index)
            
        self.showMessage(u"Compte " + unicode(login) + u" s\u00e9lectionn\u00e9")
        
    def on_btn_enregistrer_clicked(self):
        if not self.current_compte_id:
            self.showMessage("Aucun compte sélectionné", error=True)
            return
            
        try:
            nouveau_statut = unicode(self.ui.comboBox_statut.currentText())
            actif = self.ui.checkBox_actif.isChecked()
            
            success = self.model.updateCompte(self.current_compte_id, statut=nouveau_statut, actif=actif)
            
            if success:
                self.showMessage(u"Compte mis \u00e0 jour avec succ\u00e8s")
                self.loadComptes()
            else:
                self.showMessage("Erreur lors de la mise à jour", error=True)
                
        except Exception as e:
            print("Erreur enregistrer:", str(e))
            self.showMessage("Erreur: " + str(e), error=True)
            
    def on_btn_Activer_clicked(self):
        if not self.current_compte_id:
            self.showMessage("Aucun compte sélectionné", error=True)
            return
            
        try:
            success = self.model.updateActif(self.current_compte_id, True)
            
            if success:
                self.ui.checkBox_actif.setChecked(True)
                self.showMessage(u"Compte activ\u00e9")
                self.loadComptes()
            else:
                self.showMessage("Erreur lors de l'activation", error=True)
                
        except Exception as e:
            print("Erreur activation:", str(e))
            self.showMessage("Erreur: " + str(e), error=True)
            
    def on_btn_Desactiver_clicked(self):
        if not self.current_compte_id:
            self.showMessage("Aucun compte sélectionné", error=True)
            return
            
        try:
            success = self.model.updateActif(self.current_compte_id, False)
            
            if success:
                self.ui.checkBox_actif.setChecked(False)
                self.showMessage(u"Compte désactivé")
                self.loadComptes()
            else:
                self.showMessage("Erreur lors de la désactivation", error=True)
                
        except Exception as e:
            print("Erreur désactivation:", str(e))
            self.showMessage("Erreur: " + str(e), error=True)
            
    def on_btn_ValiderStatut_clicked(self):
        if not self.current_compte_id:
            self.showMessage("Aucun compte sélectionné", error=True)
            return
            
        try:
            success = self.model.updateCompte(self.current_compte_id, statut='VALIDATED', actif=True)
            
            if success:
                index = self.ui.comboBox_statut.findText('VALIDATED')
                if index >= 0:
                    self.ui.comboBox_statut.setCurrentIndex(index)
                self.ui.checkBox_actif.setChecked(True)
                self.showMessage(u"Compte valid\u00e9 et activ\u00e9")
                self.loadComptes()
            else:
                self.showMessage("Erreur lors de la validation", error=True)
                
        except Exception as e:
            print("Erreur validation:", str(e))
            self.showMessage("Erreur: " + str(e), error=True)
            
    def on_btn_RejeterStatut_clicked(self):
        if not self.current_compte_id:
            self.showMessage("Aucun compte sélectionné", error=True)
            return
            
        try:
            success = self.model.updateStatut(self.current_compte_id, 'REJECTED')
            
            if success:
                index = self.ui.comboBox_statut.findText('REJECTED')
                if index >= 0:
                    self.ui.comboBox_statut.setCurrentIndex(index)
                self.showMessage("Statut défini à REJECTED")
                self.loadComptes()
            else:
                self.showMessage("Erreur lors du rejet", error=True)
                
        except Exception as e:
            print("Erreur rejet:", str(e))
            self.showMessage("Erreur: " + str(e), error=True)
            
    def on_btn_Reinitialiser_clicked(self):
        self.clearForm()
        self.showMessage("Formulaire réinitialisé")
        
    def clearForm(self):
        self.current_compte_id = None
        self.ui.label_id_valeur.setText("-")
        self.ui.label_login_valeur.setText("-")
        self.ui.checkBox_actif.setChecked(False)
        self.ui.comboBox_statut.setCurrentIndex(0)
        
    def showMessage(self, message, error=False):
        self.ui.label_message.setText(message)
        if error:
            self.ui.label_message.setStyleSheet("QLabel { color: #e74c3c; font-style: italic; }")
        else:
            self.ui.label_message.setStyleSheet("QLabel { color: #7f8c8d; font-style: italic; }")