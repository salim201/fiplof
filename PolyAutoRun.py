# coding: utf-8
from PyQt4 import QtCore, QtGui
from PyQt4 import QtGui, Qt
import datetime
import  globalvars

from PolygoneAutomatique import Ui_PolyAuto

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


class PolyAutoRun(Qt.QDialog):
    def __init__(self,parent):
        Qt.QDialog.__init__(self)
        self.ui = Ui_PolyAuto()
        self.parent = parent
        self.registry = self.parent.registry
        try :
            self.DemandeLayer = self.registry.mapLayersByName("Demandes Parcelle")[0]
            self.CFLayer = self.registry.mapLayersByName("Certificats")[0]
            self.FiscaliteLayer = self.registry.mapLayersByName("Fiscalite")[0]
        except Exception as e:
            print(e)

        #self.idxMode = self.parent.idxMode
        self.ui.setupUi(self)
        self.move(4,410)
        #self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.init_actions()

    def init_actions(self):
        self.ui.Apply.clicked.connect(self.saveOptionsSnap)

        if globalvars.Tolerance == 0 :
            self.ui.tolRanceSpinBox.setValue(int(0))
        else :
            self.ui.tolRanceSpinBox.setValue(int(globalvars.Tolerance))

        index = self.ui.modeComboBox.findText(str(globalvars.Mode), QtCore.Qt.MatchFixedString)
        print " self.ui.modeComboBox.findText(str(globalvars.Mode), QtCore.Qt.MatchFixedString)"
        print index

        self.ui.modeComboBox.setCurrentIndex(int(globalvars.Mode))
        self.ui.coucheCibleComboBox_2.setCurrentIndex(int(globalvars.CurrentLayer))
        if globalvars.checked == 1 :
            self.ui.activCheckBox.setChecked(True)
        else:
            self.ui.activCheckBox.setChecked(False)

        if globalvars.NotIntersecting == 1:
            self.ui.notIntersecting.setChecked(True)
        else:
            self.ui.notIntersecting.setChecked(False)

        #self.ui.modeComboBox.setVisible(False)
        #self.ui.modeLabel.setVisible(False)
        #if index >= 0:
        #    self.ui.modeComboBox.setCurrentIndex(index)
        #self.ui.pushButtonEditFisc.clicked.connect(self.fisc_edit)



    def refresh(self):
        if globalvars.Tolerance == 0 :
            self.ui.tolRanceSpinBox.setValue(int(0))
        else :
            self.ui.tolRanceSpinBox.setValue(int(globalvars.Tolerance))

        index = self.ui.modeComboBox.findText(str(globalvars.Mode), QtCore.Qt.MatchFixedString)
        print  "index"
        print index
        print "globalvars.Mode"
        print globalvars.Mode
        self.ui.modeComboBox.setCurrentIndex(int(globalvars.Mode))
        self.ui.coucheCibleComboBox_2.setCurrentIndex(int(globalvars.CurrentLayer))

        if globalvars.checked == 1 :
            self.ui.activCheckBox.setChecked(True)
        else:
            self.ui.activCheckBox.setChecked(False)


        if globalvars.NotIntersecting == 1 :
            self.ui.notIntersecting.setChecked(True)
        else:
            self.ui.notIntersecting.setChecked(False)

    def saveOptionsSnap(self):
        print "saveOptionsSnap"
        idxCoucheCible = self.ui.coucheCibleComboBox_2.currentIndex()
        idxMode = self.ui.modeComboBox.currentIndex()
        tolerance = self.ui.tolRanceSpinBox.text()
        idxUnits = self.ui.unitSComboBox.currentIndex()
        #self.parent.idxMode = idxMode

        print "idxCoucheCible"
        print idxCoucheCible

        globalvars.CurrentLayer = idxCoucheCible
        globalvars.Mode = idxMode
        globalvars.Tolerance = tolerance
        globalvars.Unit = idxUnits

        if (self.ui.notIntersecting.isChecked()):
            globalvars.NotIntersecting = 1

        print "tolerance"
        print tolerance

        print "IdxUnits"
        print idxUnits

        if self.ui.notIntersecting.isChecked() :
            globalvars.NotIntersecting  = 1
        else :
            globalvars.NotIntersecting = 0


        if (idxCoucheCible == 1):
            print "test"
            print idxCoucheCible


        self.refresh()
        self.close()


