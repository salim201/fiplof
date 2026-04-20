from PyQt4 import QtCore, QtGui
from PyQt4 import QtGui, Qt
from CurrentLayer import Ui_Dialog
from MultipleLayersEditNodesButton import MultipleLayersEditNodesButton

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


class cLayerRun(Qt.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent.MainWindow)
        self.parent = parent
        self.connection = self.parent.connection
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.init_actions()

    def init_actions(self):
        self.ui.pushButtonCancel.clicked.connect(self.reject)
        self.ui.pushButtonOK.clicked.connect(self.accept)

    def updateLayer(self):
        print  "self.ui.choisirCoucheComboBox.currentIndex()"
        print  self.ui.choisirCoucheComboBox.currentIndex()

    def getFeatureInfos(self):
        connection = self.connection
        cursor = connection.cursor()
        cursor.execute(
            "SELECT pd.gid,pd.numdemande,d.datedemande,pd.surface,d.nomdemandeur,cf.numerocertificat,fkt.nomfokontany,hm.nomhameau"
            " FROM parcelle_d pd  "
            " LEFT JOIN demande d ON pd.gid = d.gid   "
            " LEFT JOIN certificat cf ON pd.idcertificat = cf.idcertificat  "
            " LEFT JOIN fokontany  fkt ON d.idfokontany = fkt.idfokontany "
            " LEFT JOIN hameau  hm     ON fkt.idfokontany = hm.idfokontany WHERE pd.gid=%s ", [int(self.gid)])
        dm = cursor.fetchone()
        if (len(dm) >= 1):
            self.ui.numDemandeCF.setText("NUMDEMANDE : " + str(dm[1]))
            self.ui.numDemandeCF.setReadOnly(True)

            numCF = str(dm[5]) if dm[5] != None else ""
            self.ui.infos1.setText("NUMCERTIFICAT : " + numCF)
            self.ui.infos1.setReadOnly(True)

            nomDemandeur = str(dm[4]) if dm[4] != None else ""
            self.ui.infos2.setText("DEMANDEUR : " + str(nomDemandeur))
            self.ui.infos2.setReadOnly(True)

            surface = str(dm[3]) if dm[3] != None else ""
            self.ui.infos3.setText("SURFACE : " + str(surface))
            self.ui.infos3.setReadOnly(True)

            fokontany = str(dm[6]) if dm[6] != None else ""
            self.ui.infos5.setText("FOKONTANY : " + str(fokontany))
            self.ui.infos5.setReadOnly(True)

            hameau = str(dm[7]) if dm[7] != None else ""
            self.ui.infos6.setText("HAMEAU : " + str(hameau))
            self.ui.infos6.setReadOnly(True)
