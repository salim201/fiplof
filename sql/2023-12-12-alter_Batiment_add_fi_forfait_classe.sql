ALTER TABLE public.batiment
   ADD COLUMN fi_forfait character varying(20);
COMMENT ON COLUMN public.batiment.fi_forfait
  IS 'Valeur type calcul impôt:soit surface,soit classe, soit valeur_locative';
ALTER TABLE public.batiment
   ADD COLUMN idclasse bigint;
COMMENT ON COLUMN public.batiment.idclasse
  IS 'id classe batiment';