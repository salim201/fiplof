ALTER TABLE public.batiment
  DROP CONSTRAINT fk_batiment_parcelle;
ALTER TABLE public.batiment
  ADD CONSTRAINT fk_batiment_parcelle FOREIGN KEY (idparcelle)
      REFERENCES public.parcelle_d (gid) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;