# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
from api_config import getApiBaseUrl, setApiBaseUrl

class ConfigFIPLOFRun(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setWindowTitle(u"Configuration Service FIPLOF")
        self.setModal(True)
        self.resize(450, 150)
        self._buildUI()
        self._load()

    def _buildUI(self):
        layout = QtGui.QVBoxLayout(self)
        form = QtGui.QFormLayout()
        self.urlEdit = QtGui.QLineEdit()
        self.urlEdit.setPlaceholderText("http://localhost:8001")
        form.addRow("URL de base API :", self.urlEdit)
        layout.addLayout(form)
        layout.addStretch()
        btnLay = QtGui.QHBoxLayout()
        btnLay.addStretch()
        btnSave = QtGui.QPushButton(u"Enregistrer")
        btnSave.clicked.connect(self._save)
        btnCancel = QtGui.QPushButton(u"Annuler")
        btnCancel.clicked.connect(self.reject)
        btnLay.addWidget(btnSave)
        btnLay.addWidget(btnCancel)
        layout.addLayout(btnLay)

    def _load(self):
        self.urlEdit.setText(getApiBaseUrl())

    def _save(self):
        url = unicode(self.urlEdit.text()).strip()
        if not url:
            QtGui.QMessageBox.warning(self, u"Erreur", u"L'URL ne peut pas \u00eatre vide.")
            return
        setApiBaseUrl(url)
        QtGui.QMessageBox.information(self, u"Succ\u00e8s", u"URL sauvegard\u00e9e.")
        self.accept()
