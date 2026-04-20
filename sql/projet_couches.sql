CREATE SEQUENCE projetcouche_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE projetcouche_id_seq
  OWNER TO plof;


CREATE TABLE projetcouche
(
  id bigint NOT NULL DEFAULT nextval('projetcouche_id_seq'::regclass),
  idprojet_commune bigint,
  libelle character varying(64),
  type_couche character(1),
  fichier character varying(1024),
  couleur_bg character varying(7),
  CONSTRAINT projetcouche_pkey PRIMARY KEY (id),
  CONSTRAINT projetcouche_idprojet_commune_fkey FOREIGN KEY (idprojet_commune)
      REFERENCES projet_commune (idprojet_commune) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE
)
WITH (
  OIDS=FALSE
);
ALTER TABLE projetcouche
  OWNER TO plof;