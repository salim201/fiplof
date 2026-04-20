-- Table: public.path_personne

-- DROP TABLE public.path_personne;

CREATE TABLE public.path_personne
(
  idpersonne bigint NOT NULL,
  cin_recto character varying(2048),
  cin_verso character varying(2048),
  signature character varying(2048),
  CONSTRAINT pk_path PRIMARY KEY (idpersonne)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.path_personne
  OWNER TO postgres;

ALTER TABLE public.limitesparcelle ADD COLUMN path_file character varying(2048);