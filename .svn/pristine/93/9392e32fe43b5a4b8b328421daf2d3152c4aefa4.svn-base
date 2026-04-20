ALTER TABLE IF EXISTS public.district
    ADD CONSTRAINT fk_region FOREIGN KEY (idregion)
    REFERENCES public.region (idregion) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;
CREATE INDEX  fki_fk_region
    ON public.district(idregion);