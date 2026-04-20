ALTER TABLE public.blob_personne DROP CONSTRAINT fk_blob_personne;
ALTER TABLE public.blob_history DROP CONSTRAINT fki_blob_history_pers;
ALTER TABLE public.blob_history DROP CONSTRAINT fki_blob_hitory_utilisateur;