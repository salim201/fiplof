CREATE SEQUENCE projet_idprojet_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 2147483647
  START 1
  CACHE 1;
ALTER TABLE projet_idprojet_seq
  OWNER TO postgres;

CREATE TABLE projet
(
  idprojet integer NOT NULL DEFAULT nextval('projet_idprojet_seq'::regclass),
  date_lancement date,
  date_premier_import date,
  date_dernier_import date,
  langue character varying(2),
  nom character varying(128) NOT NULL,
  CONSTRAINT pk_projet_idprojet PRIMARY KEY (idprojet)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE projet
  OWNER TO postgres;


CREATE SEQUENCE projet_commune_idprojet_commune_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE projet_commune_idprojet_commune_seq
  OWNER TO postgres;

CREATE TABLE projet_commune
(
  idprojet_commune bigint NOT NULL DEFAULT nextval('projet_commune_idprojet_commune_seq'::regclass),
  idcommune bigint,
  idprojet integer,
  CONSTRAINT pk_projet_commune_idprojet_commune PRIMARY KEY (idprojet_commune),
  CONSTRAINT fk_commune_idcommune FOREIGN KEY (idcommune)
      REFERENCES commune (idcommune) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk_projet_idprojet FOREIGN KEY (idprojet)
      REFERENCES projet (idprojet) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT uq_projet_commune UNIQUE (idcommune, idprojet)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE projet_commune
  OWNER TO postgres;

ALTER TABLE projet_commune
  ADD COLUMN fond_image character varying(1024);
ALTER TABLE projet_commune
  ADD COLUMN couche_titres character varying(1024);
ALTER TABLE projet_commune
  ADD COLUMN couche_cadastres character varying(1024);
ALTER TABLE projet_commune
  ADD COLUMN couche_limites character varying(1024);