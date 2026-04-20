ALTER TABLE public.parcelle_d DROP CONSTRAINT uk_code_parcelle;

ALTER TABLE public.parcelle_d
  ADD CONSTRAINT uk_code_parcelle UNIQUE(codeparcelle, id_commune);
