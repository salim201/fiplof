-- Column: public.personne.rcin_personne

-- ALTER TABLE public.personne DROP COLUMN rcin_personne;

ALTER TABLE public.personne
    ADD COLUMN rcin_personne character varying(256) COLLATE pg_catalog."default";