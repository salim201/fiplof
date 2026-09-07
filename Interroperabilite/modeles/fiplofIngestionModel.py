# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.extras
import globalvars
from datetime import datetime
import json

class FiplofIngestionEntity:
    def __init__(self):
        self.id = None
        self.version_schema = ""
        self.source_systeme = ""
        self.type_message = ""
        self.payload = ""
        self.statut = "RECEIVED"
        self.erreur = ""
        self.id_batch = ""
        self.created_at = datetime.now()
        self.processed_at = None
        self.commune = ""
        self.valid_parcelle = ""
        self.error_parcelle = ""
        self.traitement_statut = ""
        self.traitement_parcelle_valide = ""
        self.traitement_parcelle_refuse = ""

class FiplofIngestionModel:
    def __init__(self):
        self.connection = None
        
    def setConnection(self, connection):
        """Définit la connexion à la base de données"""
        self.connection = connection

   

    
    def getDossierInPayload(self):
        """Récupère toutes les ingestions"""
        if not self.connection:
            return []
            
        allDossier = []
        try:
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            
            query = """
                SELECT *
                FROM fiplof_raw_ingestion
                WHERE statut IN ('DONE', 'PARTIAL_SUCCESS')
                AND (traitement_statut IS NULL OR traitement_statut != 'SUCCESS')
                ORDER BY created_at DESC;
            """
            
            cursor.execute(query)
            results = cursor.fetchall()
            
            for row in results:
                
                allDossier.append({
                    'id': row['id'],
                    'source_systeme': row['source_systeme'],
                    'statut': row['statut'],
                    'traitement_statut': row['traitement_statut'],
                    'valid_parcelle': row['valid_parcelle'],
                    'error_parcelle': row['error_parcelle'],
                    'created_at': row['created_at']
                })
            
                
            cursor.close()
            
        except Exception as e:
            print("Erreur lors de la récupération des ingestions:", str(e))
            
        return allDossier
           
    def getIngestionsWithoutPayload(self):
        """Récupère toutes les ingestions"""
        if not self.connection:
            return []
            
        ingestions = []
        try:
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            
            query = """
                SELECT *
                FROM fiplof_raw_ingestion
                WHERE statut IN ('DONE', 'PARTIAL_SUCCESS')
                AND (traitement_statut IS NULL OR traitement_statut != 'SUCCESS')
                ORDER BY created_at DESC;
            """
            
            
            cursor.execute(query)
            results = cursor.fetchall()
            
            for row in results:
                
                ingestions.append({
                    'id': row['id'],
                    'source_systeme': row['source_systeme'],
                    'statut': row['statut'],
                    'traitement_statut': row['traitement_statut'],
                    'valid_parcelle': row['valid_parcelle'],
                    'error_parcelle': row['error_parcelle'],
                    'created_at': row['created_at']
                })
            
                
            cursor.close()
            
        except Exception as e:
            print("Erreur lors de la récupération des ingestions:", str(e))
            
        return ingestions

    def getIngestionsWithPayload(self, ingestion_id=None):
        """Récupère les ingestions avec payload"""

        if not self.connection:
            return []

        ingestions = []

        try:

            cursor = self.connection.cursor(
                cursor_factory=psycopg2.extras.DictCursor
            )

            query = """
            SELECT *
            FROM fiplof_raw_ingestion
            """
            print("DEBUG ingestion_id : ++++++++++++")
            print(ingestion_id)
            params = []

            # Filtre par ID si fourni
            if ingestion_id:
                query += " WHERE id = %s "
                params.append(ingestion_id)

            query += " ORDER BY created_at DESC "

            cursor.execute(query, tuple(params))

            results = cursor.fetchall()

            for row in results:

                payload = row['payload']

                # Convertir JSON texte en dict Python
                try:
                    if isinstance(payload, basestring):
                        payload = json.loads(payload)
                except:
                    payload = {}

                ingestions.append({

                    'id': row['id'],

                    'version_schema': row['version_schema'],

                    'source_systeme': row['source_systeme'],

                    'type_message': row['type_message'],

                    'payload': payload,

                    'statut': row['statut'],

                    'erreur': row['erreur'],

                    'id_batch': row['id_batch'],

                    'created_at': row['created_at'],

                    'processed_at': row['processed_at'],

                    'commune': row['commune'],

                    'valid_parcelle': row['valid_parcelle'],

                    'error_parcelle': row['error_parcelle'],

                    'traitement_statut': row['traitement_statut'],

                    'traitement_parcelle_valide':
                        row['traitement_parcelle_valide'],

                    'traitement_parcelle_refuse':
                        row['traitement_parcelle_refuse']
                })

            cursor.close()

        except Exception as e:

            print(
                "Erreur lors de la récupération des ingestions:",
                str(e)
            )

        return ingestions

    @staticmethod
    def updateTraitementStatut(connection, id_ingestion,
                            traitement_statut,
                            traitement_parcelle_valide,
                            traitement_parcelle_refuse):

        cursor = connection.cursor()

        try:
            query = """
                UPDATE fiplof_raw_ingestion
                SET
                    traitement_statut = %s,
                    traitement_parcelle_valide = %s,
                    traitement_parcelle_refuse = %s
                WHERE id = %s
            """

            cursor.execute(query, (
                traitement_statut,
                traitement_parcelle_valide,
                traitement_parcelle_refuse,
                id_ingestion
            ))

            return cursor.rowcount > 0
        finally:
            cursor.close()
