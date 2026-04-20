ALTER TABLE public.proprietaireparcelle DROP COLUMN coproprietaireconsort;
ALTER TABLE public.proprietaireparcelle
  ADD CONSTRAINT fk_personne FOREIGN KEY (idpersonne) REFERENCES public.personne (idpersonne)
   ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE public.proprietaireparcelle
  ADD CONSTRAINT fk_parcelle FOREIGN KEY (idparcelle) REFERENCES public.parcelle_d (gid)
   ON UPDATE NO ACTION ON DELETE NO ACTION;
CREATE INDEX fki_parcelle
  ON public.proprietaireparcelle(idparcelle);
ALTER TABLE public.proprietaireparcelle DROP CONSTRAINT fk_proprietaireparcelle_personne;
ALTER TABLE public.proprietaireparcelle DROP CONSTRAINT fk_proprietaireparcelle_parcelle_d;
ALTER TABLE public.proprietaireparcelle
  ADD CONSTRAINT pk_proprietaire PRIMARY KEY (idpersonne, idparcelle);