# -*- coding: utf-8 -*-
"""
Point d'entrée pour tester le module SecuriteCompte
Usage: python test_securite.py
"""

import sys
import os

# Ajout du chemin du plugin
PLUGIN_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PLUGIN_DIR not in sys.path:
    sys.path.append(PLUGIN_DIR)

from PyQt4 import QtGui
import psycopg2

# Configuration de la connexion PostgreSQL
# Modifier ces paramètres selon votre environnement
DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'fiplof',
    'user': 'postgres',
    'password': 'postgres'
}


def main():
    app = QtGui.QApplication(sys.argv)
    
    try:
        # Connexion à la base de données
        print("Connexion à la base de données...")
        connection = psycopg2.connect(**DB_CONFIG)
        print("Connexion établie avec succès")
        
        # Import et lancement du module
        from SecuriteCompteRun import SecuriteCompteRun
        
        window = SecuriteCompteRun(connection)
        window.show()
        
        sys.exit(app.exec_())
        
    except psycopg2.OperationalError as e:
        print("Erreur de connexion à la base de données:")
        print(str(e))
        print("\nVeuillez modifier les paramètres de connexion dans ce fichier:")
        print(__file__)
        sys.exit(1)
    except Exception as e:
        print("Erreur:", str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()