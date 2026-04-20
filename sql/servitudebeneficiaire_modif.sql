DROP SEQUENCE IF EXISTS public.servitudebeneficiaire_idservitude_seq CASCADE;
ALTER TABLE public.servitudebeneficiaire
DROP COLUMN idservitude CASCADE;

ALTER TABLE public.servitudebeneficiaire
   ADD COLUMN idservitude bigint;
   
ALTER TABLE public.servitudebeneficiaire
  ADD CONSTRAINT fk_servitudebeneficiaire_serv FOREIGN KEY (idservitude) REFERENCES public.servitude (idservitude)
   ON UPDATE NO ACTION ON DELETE NO ACTION;
CREATE INDEX fki_servitudebeneficiaire_serv
  ON public.servitudebeneficiaire(idservitude);
   
ALTER TABLE public.servitudebeneficiaire
  ADD CONSTRAINT pk_servitudebeneficiaire PRIMARY KEY (idbeneficiaire, idservitude);


