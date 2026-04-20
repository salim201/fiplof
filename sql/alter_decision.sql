ALTER TABLE public.decision ALTER COLUMN numerodecision DROP NOT NULL;
ALTER TABLE public.decision ADD COLUMN idprojet integer;
