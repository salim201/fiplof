-- Table: public.contribuableconsorts

-- DROP TABLE public.contribuableconsorts;

CREATE TABLE public.contribuableconsorts
(
  idcontribuable bigint NOT NULL,
  idconsort bigint NOT NULL,
  CONSTRAINT pk_contribuableconsorts PRIMARY KEY (idcontribuable, idconsort),
  CONSTRAINT fk_consorts FOREIGN KEY (idconsort)
      REFERENCES public.contribuable (idcontribuable) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT fk_contribuable FOREIGN KEY (idcontribuable)
      REFERENCES public.contribuable (idcontribuable) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.contribuableconsorts
  OWNER TO postgres;

-- Index: public.fki_consorts

-- DROP INDEX public.fki_consorts;

CREATE INDEX fki_consorts
  ON public.contribuableconsorts
  USING btree
  (idconsort);

