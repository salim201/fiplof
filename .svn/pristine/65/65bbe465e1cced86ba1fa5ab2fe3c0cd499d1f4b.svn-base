-- Table: public.proprietaireparcelle_d

-- DROP TABLE public.proprietaireparcelle_d;

CREATE TABLE public.proprietaireparcelle_d
(
  idparcelle bigint NOT NULL,
  idpersonne bigint NOT NULL,
  CONSTRAINT pk_proprio_parcelle PRIMARY KEY (idparcelle, idpersonne),
  CONSTRAINT fk_parcelle_d FOREIGN KEY (idparcelle)
      REFERENCES public.parcelle_d (gid) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT fk_personne FOREIGN KEY (idpersonne)
      REFERENCES public.personnephysique (idpersonne) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.proprietaireparcelle_d
  OWNER TO postgres;
