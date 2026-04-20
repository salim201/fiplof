DROP SEQUENCE IF EXISTS utilisateur_id_seq CASCADE;

CREATE SEQUENCE utilisateur_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 2147483647
  START 1
  CACHE 1;
ALTER TABLE utilisateur_id_seq
  OWNER TO postgres;


DROP TABLE IF EXISTS utilisateur CASCADE;

CREATE TABLE utilisateur
(
  idutilisateur integer NOT NULL DEFAULT nextval('utilisateur_id_seq'::regclass),
  nomutilisateur character varying(100) NOT NULL,
  prenomutilisateur character varying(100),
  loginutilisateur character varying(50) NOT NULL,
  passwordutilisateur character varying(50) NOT NULL,
  typeutilisateur character varying(20),
  telephone character varying(20),
  adresse character varying(256),
  fonction character varying(128),
  CONSTRAINT pk_utilisateur PRIMARY KEY (idutilisateur)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE utilisateur
  OWNER TO postgres;