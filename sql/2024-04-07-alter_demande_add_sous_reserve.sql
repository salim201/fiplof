ALTER TABLE public.demande
   ADD COLUMN sous_reserve boolean;
COMMENT ON COLUMN public.demande.sous_reserve
  IS 'Vrai si decision crl sous reserve';