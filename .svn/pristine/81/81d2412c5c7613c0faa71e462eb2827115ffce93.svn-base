from PyQt4 import QtGui, Qt
from .UiTransparence import Ui_Dialog


class Transparence(QtGui.QDialog):
    def __init__(self, layer):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.layer = layer
        self.init_actions()
        self.init_value()

    def init_actions(self):
        self.ui.checkBoxTransparence.stateChanged.connect(self.checkBoxTransparenceStateChanged)
        self.ui.horizontalSlider.valueChanged.connect(self.horizontalSliderValueChanged)
        self.ui.pushButtonCancel.clicked.connect(self.rollback)
        self.ui.pushButtonOK.clicked.connect(self.accept)

    def checkBoxTransparenceStateChanged(self, state):
        self.ui.horizontalSlider.setEnabled(state)
        if state == 0:
            self.ui.horizontalSlider.setValue(0)

    def horizontalSliderValueChanged(self, value):
        self.ui.label.setText(str(value) + "%")
        if self.layer.type() == 0:
            self.layer.setLayerTransparency(value)
        else:
            self.layer.renderer().setOpacity(float(100 - value)/100)
        self.layer.triggerRepaint()

    def init_value(self):
        p = 0
        if self.layer.type() == 0:
            self.old = self.layer.layerTransparency()
            p = self.layer.layerTransparency()
        else:
            self.old = self.layer.renderer ().opacity()
            p = 100 - self.layer.renderer().opacity() * 100
        self.ui.horizontalSlider.setValue(p)
        if p > 0:
            self.ui.checkBoxTransparence.setCheckState(Qt.Qt.Checked)

    def rollback(self):
        if self.layer.type() == 0:
            self.layer.setLayerTransparency(self.old)
        else:
            self.layer.renderer().setOpacity(self.old)
        self.layer.triggerRepaint()
        self.reject()
