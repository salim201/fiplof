@echo on

SET OSGEO4W_ROOT=C:\Program Files\QGIS Wien\apps\
SET PYTHONHOME=%OSGEO4W_ROOT%Python27
SET PATH=%OSGEO4W_ROOT%Python27\Scripts;C:\Program Files\QGIS Wien\bin;%OSGEO4W_ROOT%qgis-ltr\bin
SET PYTHONPATH=%OSGEO4W_ROOT%qgis-ltr\python
python plof.py