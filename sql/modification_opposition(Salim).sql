ALTER TABLE public.oppositions DROP COLUMN "etatOpposition";
ALTER TABLE public.oppositions ADD COLUMN "etatopposition" integer;
ALTER TABLE public.oppositions ALTER COLUMN "etatopposition" SET DEFAULT 0;