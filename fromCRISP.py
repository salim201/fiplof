import psycopg2
import psycopg2.extras

#layer=QgsVectorLayer("D:\CRISP-IPSS-FIPLOF\Shape IPSS\Shape IPSS.shp","dataIPSS","ogr")
layer=QgsVectorLayer("D:\OPROD-FIPLOF\KT_15261.shp","dataIPSS","ogr")


#print (layer.fields().names())
features=layer.getFeatures()
dBName = "plof"

connection = psycopg2.connect(database=dBName, user='postgres', password ='postgres', host='localhost')
cursor = connection.cursor()
i = 0
try :
    for f in features:
        geometry = f.geometry()
        x = None
        strgeom = ""
        if geometry.wkbType() == QGis.WKBPolygon:
            x = geometry.asPolygon()
        if geometry.wkbType() == QGis.WKBMultiPolygon:
            x = geometry.asMultiPolygon()[0]
        print("GEOMETRY")
        x = x[0]
        print(x)
        sizearray = len(x)
        print("----------Dimension-------")
        print(sizearray)
        if (sizearray >= 1):
            z = x[0]
            for y in x:
                print "element "
                print y
                if x[0] == y:
                    if i == 0:
                        strgeom += str(y[0]) + " " + str(y[1])
                    else:
                        strgeom += ", " + str(y[0]) + " " + str(y[1])
                else:
                    strgeom += ", " + str(y[0]) + " " + str(y[1])
                i = i + 1
            wkt = "POLYGON((" + strgeom + "))"
            print("as WKT")
            print(geometry.exportToWkt())
            print "STR GEOM"
            print strgeom
            try:
                num = ""
                id_commune = 3
                exe = cursor.execute(
                    "INSERT INTO parcelle_d (numero,geom,surface ,id_commune)VALUES (%s, ST_GeomFromText(%s, 29702),ST_Area(%s), %s) returning gid,surface",
                    (num, geometry.exportToWkt(), geometry.exportToWkt(), id_commune))
                connection.commit()
                print("AFTER commit")
            except Exception as e:
                print(e)
                

        attrs = f.attributes()
        size = len(attrs)
#        print("----Size---")
        while(i < size ) :
            print(i)
            #print("---Afficher elements -at--"+str(i))
            #print(attrs[i])
            i = i + 1
        #break
#        print(size)
#        print (attrs)
    
except Exception as e:
    print(e)

#def traiterCategorieConsistance
#def traiterGeom() :
#def traiterVoisin():
    
    
data_list = []
#for field in layer.fields():
#    field_name = field.name()
#    field_type = field.typeName()
#
#    data = field_name, field_type
#    data_list.append(data)
#    print(data_list)
