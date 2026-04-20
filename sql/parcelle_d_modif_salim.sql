ALTER TABLE public.parcelle_d
   ADD COLUMN idcharge bigint;
ALTER TABLE public.parcelle_d
   ADD COLUMN idhypotheque bigint;
ALTER TABLE public.parcelle_d
   ADD COLUMN idservitude bigint;

ALTER TABLE public.parcelle_d
  ADD CONSTRAINT fk_charge FOREIGN KEY (idcharge) REFERENCES public.autrecharge (idcharge)
   ON UPDATE NO ACTION ON DELETE NO ACTION;
CREATE INDEX fki_charge
  ON public.parcelle_d(idcharge);

ALTER TABLE public.parcelle_d
  ADD CONSTRAINT fk_hypotheque FOREIGN KEY (idhypotheque) REFERENCES public.hypotheque (idhypotheque)
   ON UPDATE NO ACTION ON DELETE NO ACTION;
CREATE INDEX fki_hypotheque
  ON public.parcelle_d(idhypotheque);
  
ALTER TABLE public.parcelle_d
  ADD CONSTRAINT fk_servitude FOREIGN KEY (idservitude) REFERENCES public.servitude (idservitude)
   ON UPDATE NO ACTION ON DELETE NO ACTION;
CREATE INDEX fki_servitude
  ON public.parcelle_d(idservitude);

