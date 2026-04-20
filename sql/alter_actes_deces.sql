ALTER TABLE public.actedeces ALTER COLUMN numeroactedeces DROP NOT NULL;
ALTER TABLE public.actedeces ALTER COLUMN dateactedeces DROP NOT NULL;
ALTER TABLE public.actedeces ALTER COLUMN numeroactenotoriete DROP NOT NULL;
ALTER TABLE public.actedeces ALTER COLUMN dateactenotoriete DROP NOT NULL;
ALTER TABLE public.actedeces ADD COLUMN idprojet integer;