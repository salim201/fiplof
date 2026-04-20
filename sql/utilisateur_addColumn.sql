ALTER TABLE public.utilisateur ADD COLUMN loginufiplof character varying(250);
ALTER TABLE public.utilisateur ADD COLUMN passwdfiplof character varying(250);



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
  loginufiplof character varying(250),
  passwdfiplof character varying(250),
  CONSTRAINT pk_utilisateur PRIMARY KEY (idutilisateur)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE utilisateur
  OWNER TO postgres;