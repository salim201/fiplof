ALTER TABLE public.parcelle_d ADD COLUMN idcertificat bigint;

ALTER TABLE public.parcelle_d
  ADD CONSTRAINT fk_certificat FOREIGN KEY (idcertificat)
      REFERENCES public.certificat (idcertificat) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE parcelle_d ADD COLUMN idhameau bigint;

ALTER TABLE public.parcelle_d
  ADD CONSTRAINT fk_hameau FOREIGN KEY (idhameau)
      REFERENCES public.hameau (idhameau) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;