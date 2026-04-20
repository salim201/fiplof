ALTER TABLE public.parcelle_d ADD COLUMN id_commune bigint;
COMMENT ON COLUMN public.parcelle_d.id_commune IS 'Cle etrangere commune';
ALTER TABLE public.parcelle_d
  ADD CONSTRAINT fk_idcommune FOREIGN KEY (id_commune) REFERENCES public.commune (idcommune)
   ON UPDATE NO ACTION ON DELETE NO ACTION;
CREATE INDEX fki_idcommune
  ON public.parcelle_d(id_commune);