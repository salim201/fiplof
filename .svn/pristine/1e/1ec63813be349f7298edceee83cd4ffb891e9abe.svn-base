ALTER TABLE public.impot_parcelle
   ADD COLUMN idparcelle bigint;
  ALTER TABLE public.impot_parcelle
  ADD CONSTRAINT fk_parcelle_impot FOREIGN KEY (idparcelle) REFERENCES public.parcelle_d (gid)
   ON UPDATE NO ACTION ON DELETE NO ACTION;
CREATE INDEX fki_parcelle_impot
  ON public.impot_parcelle(idparcelle);
  ALTER TABLE public.impot_parcelle
  ADD CONSTRAINT unik_impot_parcelle UNIQUE (annee, idparcelle);
