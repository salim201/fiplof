# -*- coding: utf-8 -*-
class DateSynchro:
    def table_name(self):
        return "date_syncho"

    def key_name(self):
        return "id_synchro"

    def key_value(self):
        return self.id_synchro

    def fields(self):
        return ("date_synchro",)

    def values(self):
        return (self.date_synchro,)

    def __init__(self, connection):
        self.connection = connection  # Connexion à la base de données
        self.id_synchro = 0
        self.date_synchro = None

    def map(self, res):
        self.id_synchro = res["id_synchro"]
        self.date_synchro = res["date_synchro"]

    def insert(self):
        print(self.date_synchro)
        try:
            import datetime
            if self.date_synchro is None:
                self.date_synchro = datetime.datetime.now()
            print(self.date_synchro)
            print(datetime.datetime.now())
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO date_synchro (date_synchro) VALUES (%s)", (self.date_synchro,))

            self.connection.commit()

            self.id_synchro = cursor.lastrowid
            return True
        except Exception as e:
            print("Erreur lors de l'insertion date_synchro:", e)
            self.connection.rollback()  # En cas d'erreur, on annule la transaction
            return False

    def update(self):
        try:
            if self.date_synchro is None:
                import datetime
                self.date_synchro = datetime.datetime.now()
            cursor = self.connection.cursor()

            cursor.execute("UPDATE date_syncho SET date_synchro = ? WHERE id_syncho = ?",
                           (self.date_synchro, self.id_synchro))

            self.connection.commit()

        except Exception as e:
            # En cas d'erreur, on annule la transaction et on affiche un message d'erreur
            print("Erreur lors de la mise à jour:", e)
            self.connection.rollback()  # Annuler la transaction si une erreur se produit
            return False  # Retourne False pour indiquer que l'opération a échoué

        return True  # Retourne True pour indiquer que l'opération a réussi


