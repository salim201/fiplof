ALTER TABLE public.parcelle_d
   ADD COLUMN fi_forfait character varying(15);
COMMENT ON COLUMN public.parcelle_d.fi_forfait
  IS 'Valeur type calcul impôt:soit surface,soit classe, soit valeur_venale';

