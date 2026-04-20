CREATE OR REPLACE VIEW public.vw_certificat AS 
 SELECT p.gid,
    p.geom,
    c.numerocertificat,
    c.idcommune,
    c.idcertificat
   FROM certificat c
     JOIN parcelle_d p ON p.idcertificat = c.idcertificat;

ALTER TABLE public.vw_certificat
  OWNER TO postgres;
  
 ALTER TABLE public.certificat
  ADD CONSTRAINT uk_numcertificat UNIQUE (numerocertificat) USING INDEX TABLESPACE pg_default;

ALTER TABLE public.demande ADD COLUMN datedecision date;

ALTER TABLE public.projetcouche ADD COLUMN plofpaps integer;
ALTER TABLE public.projetcouche ALTER COLUMN plofpaps SET DEFAULT 0;


ALTER TABLE public.avoir_demande ADD COLUMN csv_id character varying(32);
ALTER TABLE demande
   ADD COLUMN categorie character varying;
   ALTER TABLE public.personnemorale
   ADD COLUMN csv_id character varying(32);
ALTER TABLE public.commune
   ADD COLUMN csv_id character varying(32);
   ALTER TABLE public.demande ADD COLUMN csv_id character varying(32);
ALTER TABLE public.demande
   ADD COLUMN code_parcelle character varying(32);
   ALTER TABLE public.district
   ADD COLUMN csv_id character varying(32);
   ALTER TABLE public.fokontany
   ADD COLUMN csv_id character varying(32);
   
   ALTER TABLE public.hameau
   ADD COLUMN csv_id character varying(32);
   
   ALTER TABLE public.parcelle_d ADD COLUMN csv_id character varying(32);
   ALTER TABLE parcelle_d
   ADD COLUMN anomalie boolean;
   ALTER TABLE parcelle_d
   ADD COLUMN limitrophe boolean;
   ALTER TABLE personne ADD COLUMN csv_id character varying(32);
   ALTER TABLE public.personnemoraleparcelle
   ADD COLUMN iddemande bigint;
	ALTER TABLE public.personnemoraleparcelle
   ADD COLUMN csv_id character varying(32);
   ALTER TABLE public.region
   ADD COLUMN csv_id character varying(32);
   ALTER TABLE public.typepersonnemorale
   ADD COLUMN csv_id character varying(32);
   -- Table: type_anomalie

-- DROP TABLE type_anomalie;

CREATE TABLE type_anomalie
(
  id_type_anomalie bigserial NOT NULL,
  valeur character varying(32),
  csv_id character varying(32),
  CONSTRAINT pk_type_anomalie PRIMARY KEY (id_type_anomalie)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE type_anomalie
  OWNER TO postgres;
  
  CREATE TABLE anomalie
(
  idanomalie bigserial NOT NULL,
  id_type_anomalie bigint,
  description character varying(1024),
  resolu boolean,
  csv_iddemande character varying(32),
  date_anomalie date,
  csv_id character varying(32),
  csv_id_type_anomalie character varying(32),
  CONSTRAINT pk_anomalie PRIMARY KEY (idanomalie)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE anomalie
  OWNER TO postgres;
-- Sequence: iddemande_seq

-- DROP SEQUENCE iddemande_seq;

CREATE SEQUENCE iddemande_sans_geom_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 5241
  CACHE 1;
ALTER TABLE iddemande_seq
  OWNER TO postgres;

-- Table: demande

-- DROP TABLE demande;

CREATE TABLE demande_sans_geom
(
  iddemande integer NOT NULL DEFAULT nextval('iddemande_seq'::regclass),
  id integer,
  numdemande character varying(1000),
  nomdemandeur character varying(100),
  surface numeric,
  parcelle character varying(5),
  etat_cf integer,
  geom geometry,
  gid integer NOT NULL DEFAULT 0,
  datedemande date,
  datereconnaissance date,
  region character varying(250),
  district character varying(250),
  commune character varying(250),
  fokontany character varying(250),
  titre character(50),
  idfokontany integer,
  idcommune integer,
  idrejet integer,
  cout real,
  consistance character varying(250),
  idprojet integer,
  numdemandepaps character varying(250),
  datedecision date,
  csv_id character varying(32),
  code_parcelle character varying(32),
  CONSTRAINT demande_sans_geom_pkey PRIMARY KEY (iddemande)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE demande_sans_geom
   ADD COLUMN categorie character varying(32);
ALTER TABLE demande
  OWNER TO postgres;
  
  INSERT INTO spatial_ref_sys(srid,auth_name,auth_srid,srtext,proj4text)
VALUES(98751,'fiplof', 98751, 'PROJCS["laborde",GEOGCS["GCS_Tananarive_1925",DATUM["D_Tananarive_1925",SPHEROID["International_1924",6378388.0,297.0]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Hotine_Oblique_Mercator_Azimuth_Center"],PARAMETER["False_Easting",400000.0],PARAMETER["False_Northing",800000.0],PARAMETER["Scale_Factor",0.9995],PARAMETER["Azimuth",18.9],PARAMETER["Longitude_Of_Center",46.437229166666],PARAMETER["Latitude_Of_Center",-18.9],UNIT["Meter",1.0]]', '+proj=omerc +lat_0=-18.9 +lonc=44.10000000000001 +alpha=18.9 +k=0.9995000000000001 +x_0=400000 +y_0=800000 +gamma=18.9 +ellps=intl +towgs84=-189,-242,-91,0,0,0,0 +pm=paris +units=m +no_defs ');

 ALTER TABLE public.personne
  ADD CONSTRAINT uk_csv_pers UNIQUE (csv_id);
  
  ALTER TABLE public.region
  ADD CONSTRAINT uk_csv_reg UNIQUE (csv_id);
  
  ALTER TABLE public.district
  ADD CONSTRAINT uk_csv_dist UNIQUE (csv_id);
  
  ALTER TABLE public.commune
  ADD CONSTRAINT uk_csv_commu UNIQUE (csv_id);
  
  ALTER TABLE public.fokontany
  ADD CONSTRAINT uk_csv_foko UNIQUE (csv_id);
  
  ALTER TABLE public.hameau
  ADD CONSTRAINT uk_csv_hame UNIQUE (csv_id);
  
  ALTER TABLE public.parcelle_d
  ADD CONSTRAINT uk_csv_parcd UNIQUE (csv_id);
  
  ALTER TABLE public.demande
  ADD CONSTRAINT uk_csv_dema UNIQUE (csv_id);
  
  ALTER TABLE public.typepersonnemorale
  ADD CONSTRAINT uk_csv_typersonnemorale UNIQUE (csv_id);
  
  ALTER TABLE public.personnemorale
  ADD CONSTRAINT uk_csv_personnemorale UNIQUE (csv_id);
  
  ALTER TABLE public.type_anomalie
  ADD CONSTRAINT uk_csv_typeano UNIQUE (csv_id);
  
  ALTER TABLE public.anomalie
  ADD CONSTRAINT uk_csv_anomalie UNIQUE (csv_id);
  
  ALTER TABLE public.avoir_demande
  ADD CONSTRAINT uk_csv_avd UNIQUE (csv_id);
  
  ALTER TABLE public.personnemoraleparcelle
  ADD CONSTRAINT uk_csv_persmorparc UNIQUE (csv_id);
  ALTER TABLE public.demande_sans_geom
  ADD CONSTRAINT uk_csv_demande_sans UNIQUE (csv_id);
  
-- 28/05/2022

ALTER TABLE parcelle_d
   ADD COLUMN observation character varying(64);
   
ALTER TABLE parcelle_d
   ADD COLUMN code_parcelle_en_doublon character varying(64);
   
ALTER TABLE parcelle_d
   ADD COLUMN editer_en_cf boolean;
   
ALTER TABLE demande
   ADD COLUMN opposition boolean;
   
ALTER TABLE demande
   ADD COLUMN planche_plof character varying(32);
   
ALTER TABLE demande
   ADD COLUMN charges character varying(128);
   
ALTER TABLE demande_sans_geom
   ADD COLUMN opposition boolean;
   
ALTER TABLE demande_sans_geom
   ADD COLUMN planche_plof character varying(32);
   
ALTER TABLE demande_sans_geom
   ADD COLUMN charges character varying(128);