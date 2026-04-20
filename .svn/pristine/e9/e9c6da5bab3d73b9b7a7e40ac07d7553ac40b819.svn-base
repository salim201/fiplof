ALTER TABLE public.parcelle_d
   ADD COLUMN idcontribuable bigint;
   
ALTER TABLE public.parcelle_d
  ADD CONSTRAINT fk_contribuable FOREIGN KEY (idcontribuable) REFERENCES public.contribuable (idcontribuable)
   ON UPDATE NO ACTION ON DELETE NO ACTION;
CREATE INDEX fki_contribuable
  ON public.parcelle_d(idcontribuable);