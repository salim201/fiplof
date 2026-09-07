# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.extras
from datetime import datetime

class SecuriteCompteModel:
    def __init__(self):
        self.connection = None
        
    def setConnection(self, connection):
        self.connection = connection
        
    def getAllComptes(self, recherche=None):
        if not self.connection:
            return []
            
        comptes = []
        try:
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            
            query = """
                SELECT 
                    id_compte,
                    login,
                    nom,
                    nom_systeme,
                    actif,
                    statut,
                    derniere_connexion,
                    created_at,
                    updated_at
                FROM securite_compte_api
            """
            
            params = []
            if recherche:
                query += " WHERE login ILIKE %s OR nom ILIKE %s OR nom_systeme ILIKE %s"
                search_pattern = "%" + recherche + "%"
                params = [search_pattern, search_pattern, search_pattern]
                
            query += " ORDER BY id_compte DESC"
            
            cursor.execute(query, tuple(params) if params else None)
            results = cursor.fetchall()
            
            for row in results:
                compte = {
                    'id_compte': row['id_compte'],
                    'login': row['login'],
                    'nom': row['nom'],
                    'nom_systeme': row['nom_systeme'] or '',
                    'actif': row['actif'],
                    'statut': row['statut'],
                    'derniere_connexion': row['derniere_connexion'],
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at']
                }
                comptes.append(compte)
                
            cursor.close()
            
        except Exception as e:
            print("Erreur getAllComptes:", str(e))
            
        return comptes
    
    def getCompteById(self, id_compte):
        if not self.connection:
            return None
            
        try:
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            
            query = """
                SELECT 
                    id_compte,
                    login,
                    nom,
                    nom_systeme,
                    actif,
                    statut,
                    mot_de_passe_hash,
                    access_token,
                    refresh_token,
                    access_token_expire_at,
                    refresh_token_expire_at,
                    derniere_connexion,
                    created_at,
                    updated_at
                FROM securite_compte_api
                WHERE id_compte = %s
            """
            
            cursor.execute(query, (id_compte,))
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return {
                    'id_compte': row['id_compte'],
                    'login': row['login'],
                    'nom': row['nom'],
                    'nom_systeme': row['nom_systeme'] or '',
                    'actif': row['actif'],
                    'statut': row['statut'],
                    'mot_de_passe_hash': row['mot_de_passe_hash'],
                    'access_token': row['access_token'],
                    'refresh_token': row['refresh_token'],
                    'access_token_expire_at': row['access_token_expire_at'],
                    'refresh_token_expire_at': row['refresh_token_expire_at'],
                    'derniere_connexion': row['derniere_connexion'],
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at']
                }
                
        except Exception as e:
            print("Erreur getCompteById:", str(e))
            
        return None
    
    def updateStatut(self, id_compte, nouveau_statut):
        if not self.connection:
            return False
            
        valid_statuts = ['PENDING', 'VALIDATED', 'REJECTED']
        if nouveau_statut not in valid_statuts:
            print("Statut invalide:", nouveau_statut)
            return False
            
        try:
            cursor = self.connection.cursor()
            
            query = """
                UPDATE securite_compte_api
                SET statut = %s,
                    updated_at = %s
                WHERE id_compte = %s
            """
            
            cursor.execute(query, (nouveau_statut, datetime.now(), id_compte))
            self.connection.commit()
            cursor.close()
            
            return True
            
        except Exception as e:
            print("Erreur updateStatut:", str(e))
            self.connection.rollback()
            return False
    
    def updateActif(self, id_compte, actif):
        if not self.connection:
            return False
            
        try:
            cursor = self.connection.cursor()
            
            query = """
                UPDATE securite_compte_api
                SET actif = %s,
                    updated_at = %s
                WHERE id_compte = %s
            """
            
            cursor.execute(query, (actif, datetime.now(), id_compte))
            self.connection.commit()
            cursor.close()
            
            return True
            
        except Exception as e:
            print("Erreur updateActif:", str(e))
            self.connection.rollback()
            return False
    
    def updateCompte(self, id_compte, statut=None, actif=None):
        if not self.connection:
            return False
            
        try:
            cursor = self.connection.cursor()
            
            updates = []
            params = []
            
            if statut is not None:
                valid_statuts = ['PENDING', 'VALIDATED', 'REJECTED']
                if statut in valid_statuts:
                    updates.append("statut = %s")
                    params.append(statut)
                    
            if actif is not None:
                updates.append("actif = %s")
                params.append(actif)
                
            if not updates:
                return False
                
            updates.append("updated_at = %s")
            params.append(datetime.now())
            params.append(id_compte)
            
            query = """
                UPDATE securite_compte_api
                SET """ + ", ".join(updates) + """
                WHERE id_compte = %s
            """
            
            cursor.execute(query, tuple(params))
            self.connection.commit()
            cursor.close()
            
            return True
            
        except Exception as e:
            print("Erreur updateCompte:", str(e))
            self.connection.rollback()
            return False
    
    def deleteCompte(self, id_compte):
        if not self.connection:
            return False
            
        try:
            cursor = self.connection.cursor()
            
            query = "DELETE FROM securite_compte_api WHERE id_compte = %s"
            
            cursor.execute(query, (id_compte,))
            self.connection.commit()
            cursor.close()
            
            return True
            
        except Exception as e:
            print("Erreur deleteCompte:", str(e))
            self.connection.rollback()
            return False
    
    def createCompte(self, login, nom, nom_systeme, mot_de_passe_hash):
        if not self.connection:
            return None
            
        try:
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            
            query = """
                INSERT INTO securite_compte_api 
                (login, nom, nom_systeme, mot_de_passe_hash, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id_compte
            """
            
            now = datetime.now()
            cursor.execute(query, (login, nom, nom_systeme, mot_de_passe_hash, now, now))
            
            result = cursor.fetchone()
            self.connection.commit()
            cursor.close()
            
            return result['id_compte'] if result else None
            
        except Exception as e:
            print("Erreur createCompte:", str(e))
            self.connection.rollback()
            return None