-- Table: public.blob_history

-- DROP TABLE public.blob_history;

CREATE TABLE public.blob_history
(
  idpersonne bigint,
  idutilisateur bigint,
  old_file bytea,
  new_file bytea,
  old_file_type character varying(10),
  new_file_type character varying(10),
  nature character varying(128),
  datemodification date,
  old_file_name character varying(100),
  new_file_name character varying(100),
  CONSTRAINT fki_blob_history_pers FOREIGN KEY (idpersonne)
      REFERENCES public.personne (idpersonne) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT fki_blob_hitory_utilisateur FOREIGN KEY (idutilisateur)
      REFERENCES public.utilisateur (idutilisateur) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.blob_history
  OWNER TO postgres;

