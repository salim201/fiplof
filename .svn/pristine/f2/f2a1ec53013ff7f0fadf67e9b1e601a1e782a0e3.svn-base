-- Table: public.limitesparcelle

-- DROP TABLE public.limitesparcelle;

CREATE TABLE public.limitesparcelle
(
  idpointscardinaux integer NOT NULL,
  idparcelle bigint NOT NULL,
  description character varying,
  CONSTRAINT pk_cardinal_parcelle PRIMARY KEY (idpointscardinaux, idparcelle),
  CONSTRAINT fk_parcelle FOREIGN KEY (idparcelle)
      REFERENCES public.parcelle_d (gid) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT fk_pointscardinaux FOREIGN KEY (idpointscardinaux)
      REFERENCES public.pointscardinaux (idpointscardinaux) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.limitesparcelle
  OWNER TO postgres;
