from subprocess import Popen
import os

OSGEO4W_ROOT = "C:\\Program Files (x86)\\QGIS Wien\\apps\\"
os.environ["PYTHONHOME"] = OSGEO4W_ROOT + r"Python27"
os.environ["PATH"] = OSGEO4W_ROOT + r"Python27\Scripts;C:\Program Files (x86)\QGIS Wien\bin" + ";" + OSGEO4W_ROOT + r"qgis-ltr\bin"
os.environ["PYTHONPATH"] = OSGEO4W_ROOT + "qgis-ltr\python"

p = Popen("python plof.py", shell=True)
