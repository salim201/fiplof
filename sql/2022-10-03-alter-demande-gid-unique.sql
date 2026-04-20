ALTER TABLE IF EXISTS public.demande
    ADD CONSTRAINT uk_gid UNIQUE (gid);

COMMENT ON CONSTRAINT uk_gid ON public.demande
    IS 'unique gid from parcelle_d';