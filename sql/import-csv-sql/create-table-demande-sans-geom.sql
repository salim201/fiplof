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