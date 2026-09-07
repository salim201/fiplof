import base64
import psycopg2
import psycopg2.extras


class BlobPersonne:

    def __init__(self):

        self.idblob = None
        self.idpersonne = None

        self.cin_recto = None
        self.cin_verso = None
        self.signature = None
        self.empreinte_d = None
        self.empreinte_g = None
        self.photo_demandeur = None

        self.cin_recto_name = None
        self.cin_recto_type = None

        self.cin_verso_name = None
        self.cin_verso_type = None

        self.signature_name = None
        self.signature_type = None

        self.empreinte_d_name = None
        self.empreinte_d_type = None

        self.empreinte_g_name = None
        self.empreinte_g_type = None

        self.photo_demandeur_type = None

        self.datemaj = None

    def map(self, row):

        self.idblob = row["idblob"]
        self.idpersonne = row["idpersonne"]

        self.cin_recto = row["cin_recto"]
        self.cin_verso = row["cin_verso"]
        self.signature = row["signature"]
        self.empreinte_d = row["empreinte_d"]
        self.empreinte_g = row["empreinte_g"]
        self.photo_demandeur = row["photo_demandeur"]

        self.cin_recto_name = row["cin_recto_name"]
        self.cin_recto_type = row["cin_recto_type"]

        self.cin_verso_name = row["cin_verso_name"]
        self.cin_verso_type = row["cin_verso_type"]

        self.signature_name = row["signature_name"]
        self.signature_type = row["signature_type"]

        self.empreinte_d_name = row["empreinte_d_name"]
        self.empreinte_d_type = row["empreinte_d_type"]

        self.empreinte_g_name = row["empreinte_g_name"]
        self.empreinte_g_type = row["empreinte_g_type"]

        self.photo_demandeur_type = row["photo_demandeur_type"]

        self.datemaj = row["datemaj"]

    @staticmethod
    def insertPhotos(connection, idpersonne, photos):

        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        )

        try:

            blob = BlobPersonne()
            blob.idpersonne = idpersonne

            # Parcours photos
            for photo in photos:

                type_photo = photo.get("type")
                base64_data = photo.get("base64")

                if not base64_data:
                    continue

                header, encoded = base64_data.split(",", 1)

                mime_type = header.split(";")[0].replace(
                    "data:",
                    ""
                )

                extension = mime_type.split("/")[-1].lower()

                if extension == "jpeg":
                    extension = "jpg"

                image_bytes = base64.b64decode(encoded)

                image_binary = psycopg2.Binary(image_bytes)

                # CIN RECTO
                if type_photo == "CNI_RECTO":

                    blob.cin_recto = image_binary
                    blob.cin_recto_type = extension
                    blob.cin_recto_name = "cin_recto.{}".format(extension)

                # CIN VERSO
                elif type_photo == "CNI_VERSO":

                    blob.cin_verso = image_binary
                    blob.cin_verso_type = extension
                    blob.cin_verso_name = "cin_verso.{}".format(extension)

                # PHOTO DEMANDEUR
                elif type_photo == "PHOTO_DEMANDEUR":

                    blob.photo_demandeur = image_binary
                    blob.photo_demandeur_type = extension

                # SIGNATURE
                elif type_photo == "SIGNATURE":

                    blob.signature = image_binary
                    blob.signature_type = extension
                    blob.signature_name = "signature.{}".format(extension)

                # EMPREINTE DROITE
                elif type_photo == "EMPREINTE_D":

                    blob.empreinte_d = image_binary
                    blob.empreinte_d_type = extension
                    blob.empreinte_d_name = "empreinte_d.{}".format(extension)

                # EMPREINTE GAUCHE
                elif type_photo == "EMPREINTE_G":

                    blob.empreinte_g = image_binary
                    blob.empreinte_g_type = extension
                    blob.empreinte_g_name = "empreinte_g.{}".format(extension)

            sql = """
                INSERT INTO blob_personne
                (
                    idpersonne,

                    cin_recto,
                    cin_verso,
                    signature,
                    empreinte_d,
                    empreinte_g,
                    photo_demandeur,

                    cin_recto_name,
                    cin_recto_type,

                    cin_verso_name,
                    cin_verso_type,

                    signature_name,
                    signature_type,

                    empreinte_d_name,
                    empreinte_d_type,

                    empreinte_g_name,
                    empreinte_g_type,

                    photo_demandeur_type

                )
                VALUES
                (
                    %s,

                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,

                    %s,
                    %s,

                    %s,
                    %s,

                    %s,
                    %s,

                    %s,
                    %s,

                    %s,
                    %s,

                    %s
                )
                RETURNING idblob
            """

            cursor.execute(sql, (

                blob.idpersonne,

                blob.cin_recto,
                blob.cin_verso,
                blob.signature,
                blob.empreinte_d,
                blob.empreinte_g,
                blob.photo_demandeur,

                blob.cin_recto_name,
                blob.cin_recto_type,

                blob.cin_verso_name,
                blob.cin_verso_type,

                blob.signature_name,
                blob.signature_type,

                blob.empreinte_d_name,
                blob.empreinte_d_type,

                blob.empreinte_g_name,
                blob.empreinte_g_type,

                blob.photo_demandeur_type

            ))

            idblob = cursor.fetchone()[0]

            connection.commit()

            return idblob

        except Exception as e:

            connection.rollback()
            print("Erreur insertPhotos :", e)

        finally:

            cursor.close()

        return None

    @staticmethod
    def findByPersonne(connection, idpersonne):

        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        )

        try:

            sql = """
                SELECT *
                FROM blob_personne
                WHERE idpersonne = %s
            """

            cursor.execute(sql, (idpersonne,))

            row = cursor.fetchone()

            if row is None:
                return None

            blob = BlobPersonne()
            blob.map(row)

            return blob

        except Exception as e:

            print(e)

        finally:

            cursor.close()

        return None