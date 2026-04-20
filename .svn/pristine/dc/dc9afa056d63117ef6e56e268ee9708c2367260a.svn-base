--SELECT ST_AsPNG(ST_AsRaster(ST_Buffer(geom, 10),200,200,ARRAY['8BUI', '8BUI', '8BUI'], ARRAY[118,154,118], ARRAY[0,0,0])) png from parcelle_d WHERE gid=1049
SELECT short_name FROM ST_GDALDrivers();
-- ALTER DATABASE db_plof_fi SET postgis.gdal_enabled_drivers TO 'GTiff PNG JPEG';
 --ALTER SYSTEM SET postgis.gdal_enabled_drivers TO 'GTiff PNG JPEG';
-- SELECT pg_reload_conf();