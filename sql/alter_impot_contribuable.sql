ALTER TABLE public.impot_contribuable
   ADD COLUMN idpersonne bigint;
ALTER TABLE public.impot_contribuable
  ADD CONSTRAINT fk_personne FOREIGN KEY (idpersonne) REFERENCES public.personne (idpersonne)
   ON UPDATE NO ACTION ON DELETE NO ACTION;
CREATE INDEX fki_personne
  ON public.impot_contribuable(idpersonne);
  ALTER TABLE public.impot_contribuable
  ADD CONSTRAINT unik_impot_contribuable UNIQUE (annee, idpersonne);
