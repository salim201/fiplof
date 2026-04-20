ALTER TABLE public.parcelle_d
   ADD COLUMN idclasse bigint;
ALTER TABLE public.parcelle_d
  ADD CONSTRAINT fk_parcelle_classe FOREIGN KEY (idclasse) REFERENCES public.classe (idclasse)
   ON UPDATE NO ACTION ON DELETE NO ACTION;
CREATE INDEX fki_parcelle_classe
  ON public.parcelle_d(idclasse);
