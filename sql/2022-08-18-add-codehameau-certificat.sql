-- Column: public.certificat.code_hameau

-- ALTER TABLE IF EXISTS public.certificat DROP COLUMN IF EXISTS code_hameau;

ALTER TABLE IF EXISTS public.certificat
    ADD COLUMN code_hameau character varying(256) COLLATE pg_catalog."default";