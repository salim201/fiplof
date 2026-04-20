ALTER TABLE public.anomalie
  ADD CONSTRAINT fk_type_anomalie FOREIGN KEY (id_type_anomalie) REFERENCES public.type_anomalie (id_type_anomalie)
   ON UPDATE NO ACTION ON DELETE NO ACTION;
CREATE INDEX fki_type_anomalie
  ON public.anomalie(id_type_anomalie);

CREATE TABLE public.demande_anomalie
(
  iddemande bigint NOT NULL,
  idanomalie bigint NOT NULL,
  CONSTRAINT pk_demande_anomalie PRIMARY KEY (iddemande, idanomalie)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.demande_anomalie
  OWNER TO postgres;

  ALTER TABLE public.demande_anomalie
  ADD CONSTRAINT fk_demande FOREIGN KEY (iddemande) REFERENCES public.demande (iddemande)
   ON UPDATE NO ACTION ON DELETE NO ACTION;
   
ALTER TABLE public.demande_anomalie
  ADD CONSTRAINT fk_anomalie FOREIGN KEY (idanomalie) REFERENCES public.anomalie (idanomalie)
   ON UPDATE NO ACTION ON DELETE NO ACTION;
CREATE INDEX fki_anomalie
  ON public.demande_anomalie(idanomalie);
