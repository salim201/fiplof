import psycopg2
import psycopg2.extras
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class ProjetCouche:
    def __init__(self):
        self.id, self.idprojet_commune, self.libelle, self.type_couche,\
            self.fichier, self.couleur_bg, self.ordre = "0", "0", "", "", "", "", 0
        self.show_label, self.font, self.font_size, self.font_size_map_unit = False, "", 0, False
        self.font_color = ""
        self.show_stroke, self.stroke_width, self.stroke_color = False, 0, ""
        self.label_name = ""
        self.remplissage = 0
        self.plofpaps = 0
        self.certifiable = 0

    def map(self, res):
        self.id, self.idprojet_commune, self.libelle, self.type_couche,\
            self.fichier, self.couleur_bg, self.ordre = res["id"],\
            res["idprojet_commune"], res["libelle"], res["type_couche"],\
            res["fichier"], res["couleur_bg"], res["ordre"]
        self.show_label, self.font, self.font_size = res["show_label"], res["font"], res["font_size"]
        self.font_size_map_unit = res["font_size_map_unit"]
        self.font_color = res["font_color"]
        self.show_stroke, self.stroke_width, self.stroke_color = res["show_stroke"], res["stroke_width"], res["stroke_color"]
        self.label_name = res["label_name"]
        self.remplissage = res["remplissage"]
        self.plofpaps = res["plofpaps"]
        self.certifiable = res["certifiable"]

    def insert(self, connection):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute(
                "INSERT INTO projetcouche("
                "idprojet_commune, libelle, type_couche, fichier, couleur_bg, ordre, "
                "show_label, font, font_size, font_size_map_unit, font_color, "
                "show_stroke, stroke_width, stroke_color, label_name,remplissage,plofpaps,certifiable"
                ") "
                "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (
                    self.idprojet_commune
                    , self.libelle
                    , self.type_couche
                    , self.fichier
                    , self.couleur_bg
                    , self.ordre
                    , self.show_label
                    , self.font
                    , self.font_size
                    , self.font_size_map_unit
                    , self.font_color
                    , self.show_stroke
                    , self.stroke_width
                    , self.stroke_color
                    , self.label_name
                    , self.remplissage
                    , self.plofpaps
                    , self.certifiable
                )
            )
            connection.commit()
        except Exception as e:
            print(e)
            cursor.close()
            connection.rollback()

    def update(self, connection):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        #cursor = connection.cursor()
        print("----font_size---")
        print(self.font_size)
        print(self.font_size)
        try:
            cursor.execute(
                "UPDATE projetcouche SET libelle=(%s), type_couche=(%s), fichier=(%s), couleur_bg=(%s), ordre=(%s)"
                ", show_label = (%s), font=(%s), font_size=(%s), font_size_map_unit=(%s), font_color=(%s)"
                ", show_stroke=(%s), stroke_width=(%s), stroke_color=(%s), label_name=(%s) , remplissage=(%s) , plofpaps=(%s), certifiable=(%s) "
                " WHERE id=(%s)",
                (self.libelle
                 , self.type_couche
                 , self.fichier
                 , self.couleur_bg
                 , self.ordre
                 , self.show_label
                 , self.font
                 , self.font_size
                 , self.font_size_map_unit
                 , self.font_color
                 , self.show_stroke
                 , self.stroke_width
                 , self.stroke_color
                 , self.label_name
                 , self.remplissage
                 , self.plofpaps
                 , self.certifiable
                 , self.id
                 )
            )
            connection.commit()
        except Exception as e:
            print(e)
            print("---EXCEPTION TO UPDATE")
            cursor.close()
            connection.rollback()

    def save(self, connection):
        print("---self.id---")
        print(self.id)
        if self.id:
            print('Update projet')
            self.update(connection)
        else:
            self.insert(connection)

    @staticmethod
    def find_by_projet_commune(connection, idprojet_commune):
        results = []
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute(
                "SELECT * FROM projetcouche WHERE idprojet_commune = %s"
                " ORDER BY ordre, id", (idprojet_commune,)
            )
            rows = cursor.fetchall()
            for r in rows:
                d = ProjetCouche()
                d.map(r)
                results.append(d)
        except Exception as e:
            print(e)
        cursor.close()
        return results

    @staticmethod
    def find_by_id(connection, couche_id):
        # :returns: ProjetCouche
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT * FROM projetcouche WHERE id = %s", (couche_id,))
            row = cursor.fetchone()
            d = ProjetCouche()
            d.map(row)
            cursor.close()
            return d
        except Exception as e:
            print(e)
        return None

    @staticmethod
    def delete_by_id(connection, couche_id):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("DELETE FROM projetcouche WHERE id = %s", (couche_id,))
            cursor.close()
            connection.commit()
        except Exception as e:
            print(e)
            connection.rollback()


    @staticmethod
    def max_ordre_by_projet_commune(connection, idprojet_commune):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute(
                "SELECT coalesce(max(ordre), 0) mo FROM projetcouche"
                " WHERE idprojet_commune = %s", (idprojet_commune,)
            )
            row = cursor.fetchone()
            cursor.close()
            print(row)
            return row["mo"]
        except Exception as e:
            print(e)
        return 0

    @staticmethod
    def reorder(connection, idcouches):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        mapped = map((lambda x: '(' + str(x) + ', 1)'), idcouches)
        reduced = reduce((lambda x, y: x + ',' + y), mapped)
        print(reduced)
        s = """
        WITH BARE AS (
            SELECT * FROM (
                VALUES %s
            ) AS T(id, c)
        ),
        ORDERED AS (
            SELECT id, sum(c)over (order by c asc rows between unbounded preceding and current row) as ordre FROM BARE
        )
        UPDATE projetcouche SET ordre = ORDERED.ordre
        FROM ORDERED WHERE ORDERED.id = projetcouche.id
        """
        sql = s % (reduced)
        try:
            cursor.execute(sql)
            connection.commit()
        except Exception as e:
            print(e)
            connection.rollback()
        cursor.close()
