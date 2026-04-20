CREATE TABLE public.consistance_batiment
(
   id bigserial, 
   consistance character varying(80), 
   mombamombanytany character varying(80), 
   valeurariary integer, 
   valeur_location integer, 
   CONSTRAINT "pk_consistanceBat" PRIMARY KEY (id)
) 
WITH (
  OIDS = FALSE
)
;
COMMENT ON COLUMN public.consistance_batiment.id IS 'id ';

ALTER TABLE public.batiment DROP CONSTRAINT fk_batiment_consistance;

ALTER TABLE public.batiment
  ADD CONSTRAINT fk_consistance_batiment FOREIGN KEY (idconsistance) REFERENCES public.consistance_batiment (id)
   ON UPDATE NO ACTION ON DELETE NO ACTION;