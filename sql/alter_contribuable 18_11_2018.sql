ALTER TABLE public.contribuable
   ADD COLUMN modecalcul smallint;
COMMENT ON COLUMN public.contribuable.modecalcul
  IS 'Valeur = 1 => calcul par surface
Valeur = 2 => calcul par consistance
Valeur = 3 => calcul par classe';
