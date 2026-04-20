ALTER TABLE public.personnemorale
   ADD COLUMN idrepresentant bigint;


ALTER TABLE public.personnemorale
  ADD CONSTRAINT fk_morale_physique FOREIGN KEY (idrepresentant) REFERENCES public.personne (idpersonne)
   ON UPDATE NO ACTION ON DELETE NO ACTION;
CREATE INDEX fki_morale_physique
  ON public.personnemorale(idrepresentant);