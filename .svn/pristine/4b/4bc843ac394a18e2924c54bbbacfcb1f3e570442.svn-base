from usecases.ogrimporter.OgrImporter import OgrImporter
from osgeo import ogr as driver
from adapters.ogr.ParcelleDemandeMapper import ParcelleDemandeMapper

filename = r'C:\Users\Christophe\Downloads\PlofRepertoire\data\ANDRAINJATO EST\base\plof_data.gdb'
mapper = ParcelleDemandeMapper()
importer = OgrImporter(filename, driver, mapper)

statements = importer.getSqlStatementsFromOGR()
print(statements)
