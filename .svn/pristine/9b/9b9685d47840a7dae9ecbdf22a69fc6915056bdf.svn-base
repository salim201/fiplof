DROP SEQUENCE IF EXISTS public.servitudeparcellegrevees_idservitude_seq CASCADE;
ALTER TABLE public.servitudeparcellegrevees
DROP COLUMN idservitude CASCADE;

ALTER TABLE public.servitudeparcellegrevees
   ADD COLUMN idservitude bigint;
   
ALTER TABLE public.servitudeparcellegrevees
  ADD CONSTRAINT fk_servitudeparcellegrevees_serv FOREIGN KEY (idservitude) REFERENCES public.servitude (idservitude)
   ON UPDATE NO ACTION ON DELETE NO ACTION;
CREATE INDEX fki_servitudeparcellegrevees_serv
  ON public.servitudeparcellegrevees(idservitude);
   
ALTER TABLE public.servitudeparcellegrevees
  ADD CONSTRAINT pk_servitudeparcellegrevees PRIMARY KEY (idparcellegrevees, idservitude);


