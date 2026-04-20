@echo on
SET PGPASSWORD=postgres
"C:/Program Files/PostgreSQL/9.6\bin/psql.exe" -U postgres < "C:\plofstandalone\trunk\Parametres/plof_schema.sql"
"C:/Program Files/PostgreSQL/9.6\bin\pg_restore.exe" --host localhost --port 5432 --username "postgres" --dbname "plof_vierge"  --verbose "C:/Users/Hope/Desktop/test.sql"
arning;

UPDATE pg_database SET datallowconn = 'false' WHERE datname = 'plof';

SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'plof';

DROP DATABASE IF EXISTS plof;
DROP USER IF EXISTS plof;
CREATE ROLE plof LOGIN PASSWORD 'plof';
--
-- TOC entry 4775 (class 1262 OID 93991)
-- Name: plof; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE plof WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'French_France.1252' LC_CTYPE = 'French_France.1252';

\c plof;

SET postgis.gdal_enabled_drivers = 'ENABLE_ALL';
CREATE EXTENSION IF NOT EXISTS postgis SCHEMA public;
-- CREATE EXTENSION IF NOT EXISTS postgis_topology SCHEMA topology;
CREATE EXTENSION IF NOT EXISTS pgrouting SCHEMA public;
CREATE EXTENSION IF NOT EXISTS plpgsql SCHEMA pg_catalog;