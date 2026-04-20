# -*- coding: utf-8 -*-
import psycopg2
import psycopg2.extras

class ConnectRemoteModel:

    def __init__(self):
        print  "eto "
        self.curRemote=None
        self.connectRemote=None

    @staticmethod
    def connectToRemote(self,paramConnection):
        try:
            self.connectRemote = psycopg2.connect(
                user=paramConnection[2],
                password=paramConnection[3],
                host=paramConnection[0],
                port=paramConnection[1],
                database=paramConnection[4]
            )
            return self.connectRemote
        except (Exception, psycopg2.Error) as error:
            print ("Erreur lors de la connexion à PostgreSQL", error)
            return False
