ALTER TABLE public.demande DROP CONSTRAINT uk_codeparcelle;

ALTER TABLE public.demande
  ADD CONSTRAINT uk_codeparcelle UNIQUE(code_parcelle, idcommune);