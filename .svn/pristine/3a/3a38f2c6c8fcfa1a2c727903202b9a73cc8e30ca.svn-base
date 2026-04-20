ALTER TABLE public.batiment
   ADD COLUMN idcategorie bigint;
ALTER TABLE public.batiment
  ADD CONSTRAINT fk_categorie FOREIGN KEY (idcategorie) REFERENCES public.categorie (idcategorie)
   ON UPDATE NO ACTION ON DELETE NO ACTION;
CREATE INDEX fki_categorie
  ON public.batiment(idcategorie);
