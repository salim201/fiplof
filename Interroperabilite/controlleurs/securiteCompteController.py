# -*- coding: utf-8 -*-

import sys
import os

from ..SecuriteCompteRun import SecuriteCompteRun
from ..modeles.securiteCompteModel import SecuriteCompteModel

class SecuriteCompteController:
    def __init__(self, connection):
        self.connection = connection
        self.model = SecuriteCompteModel()
        self.model.setConnection(connection)
        
    def showDialog(self):
        dialog = SecuriteCompteRun(self.connection)
        dialog.exec_()
        return dialog
        
    def getModel(self):
        return self.model