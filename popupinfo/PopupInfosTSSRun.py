# coding: utf-8
from PyQt4 import QtCore, QtGui
from PyQt4 import QtGui, Qt
import datetime
from PopupInfosTSS import Ui_INFORMATIONS
from Utilisateur import AccesManager
import globalvars

# create the dialog for qgsPlof  Qt.QDialog
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


class PopupInfosTSSRun(Qt.QDialog):
    def __init__(self, parent):
        Qt.QDialog.__init__(self)
        self.parent = parent
        self.connection, self.canvas = self.parent.connection, self.parent.MainWindow.canvas
        self.newParcelleCF = True
        self.gid = self.parent.currentSelect
        self.ui = Ui_INFORMATIONS()
        self.ui.setupUi(self)
        self.ui.pushButtonAnnuler.setVisible(False)
        self.ui.pushButtonValider.setVisible(False)
        self.registry = None
        self.iddemande = self.numDemande = self.dateDemande = self.idparcelle = None
        self.MainWindow = self.parent.MainWindow
        self.currentGeomIdParcelle = self.gid
        self.idparcelle = self.gid
        self.currvalDemande = self.gid
        self.id_projet = parent.id_projet
        self.geometryeEdit = 0
        self.stateEdition = 1
        self.geomid = self.gid
        self.tool = parent.tool
        self.iface = parent.iface
        self.Mcs = self.MainWindow
        self.idDemande = self.gid
        self.getFeatureInfos()
        if globalvars.groupe_id != 1 and globalvars.groupe_id != 13:
            self.ui.pushButtonEditFisc.setEnabled(False)
        self.init_actions()

    def init_actions(self):
        self.ui.pushButtonEditFisc.clicked.connect(self.tss_edit)
        self.ui.pushButtonValider.clicked.connect(self.save_tss_edit)
        self.ui.pushButtonAnnuler.clicked.connect(self.stop_edit)

    def getFeatureInfos(self):
        connection = self.connection
        cursor = connection.cursor()
        cursor.execute(
            "SELECT fn_fg,demandeur,sur_plan,obs"
            " FROM terain_status_specifique  WHERE gid=%s ", [int(self.gid)])
        dm = cursor.fetchone()
        self.ui.fn_fg.setReadOnly(True)
        self.ui.demandeur.setReadOnly(True)
        self.ui.sur_plan.setReadOnly(True)
        self.ui.obs.setReadOnly(True)
        
        if len(dm) >= 1:
            if dm[0] is None: 
                self.ui.fn_fg.setText("")
            else:
                self.ui.fn_fg.setText(_fromUtf8(str(dm[0])))

            if dm[1] is None:
                self.ui.demandeur.setText("")
            else:
                self.ui.demandeur.setText(_fromUtf8(str(dm[1])))

            if dm[2] is None:    
                self.ui.sur_plan.setText("")
            else:
                self.ui.sur_plan.setText(_fromUtf8(str(dm[2])))

            if dm[3] is None:    
                self.ui.obs.setText("")
            else:
                self.ui.obs.setText(_fromUtf8(str(dm[3])))

        else:
            pass

    def tss_edit(self):
        self.ui.pushButtonEditFisc.setVisible(False)
        self.ui.pushButtonAnnuler.setVisible(True)
        self.ui.pushButtonValider.setVisible(True)
        self.ui.fn_fg.setReadOnly(False)
        self.ui.demandeur.setReadOnly(False)
        self.ui.sur_plan.setReadOnly(False)
        self.ui.obs.setReadOnly(False)

    def save_tss_edit(self):
        try:
            fn_fg = str(self.ui.fn_fg.text()).encode("utf-8")
            demandeur = str(self.ui.demandeur.text()).encode("utf-8")
            sur_plan = str(self.ui.sur_plan.text()).encode("utf-8")
            obs = str(self.ui.obs.text()).encode("utf-8")

            cursor = self.connection.cursor()
            exe = cursor.execute(
                "update terain_status_specifique set fn_fg =%s,demandeur = %s,sur_plan = %s,obs = %s"
                    "WHERE gid=%s ",
                (fn_fg,demandeur,sur_plan, obs,self.gid))
            
            self.connection.commit()
            QtGui.QMessageBox.information(
                    self,
                    "Edition TSS", _fromUtf8("Donnée insérer avec succès")
                )
            self.stop_edit()
        except Exception as err:
            print(err)
            self.connection.rollback()

    def stop_edit(self):
        self.ui.pushButtonEditFisc.setVisible(True)
        self.ui.pushButtonAnnuler.setVisible(False)
        self.ui.pushButtonValider.setVisible(False)
        self.ui.fn_fg.setReadOnly(True)
        self.ui.demandeur.setReadOnly(True)
        self.ui.sur_plan.setReadOnly(True)
        self.ui.obs.setReadOnly(True) 