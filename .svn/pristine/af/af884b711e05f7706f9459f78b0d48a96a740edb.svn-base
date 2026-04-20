ALTER TABLE public.impot_batiment
   ADD COLUMN codebatiment character varying(10);
   ALTER TABLE public.impot_batiment
  ADD CONSTRAINT fk_batiment FOREIGN KEY (codebatiment) REFERENCES public.batiment (codebatiment)
   ON UPDATE NO ACTION ON DELETE NO ACTION;
CREATE INDEX fki_batiment
  ON public.impot_batiment(codebatiment);
  ALTER TABLE public.impot_batiment
  ADD CONSTRAINT unik_impot_batiment UNIQUE (annee, codebatiment);

