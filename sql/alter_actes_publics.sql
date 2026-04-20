ALTER TABLE public.actepublic ALTER COLUMN numeroactepublic DROP NOT NULL;
ALTER TABLE public.actepublic ALTER COLUMN dateenregistrement DROP NOT NULL;
ALTER TABLE public.actepublic ALTER COLUMN nomofficierpublic DROP NOT NULL;
ALTER TABLE public.actepublic ALTER COLUMN valeurtransaction DROP NOT NULL;
ALTER TABLE public.actepublic ALTER COLUMN nombreoperation DROP NOT NULL;
ALTER TABLE public.actepublic ADD COLUMN idprojet integer;
ALTER TABLE public.actepublic ALTER COLUMN idprojet SET NOT NULL;
ALTER TABLE public.actepublic ALTER COLUMN idprojet SET DEFAULT 0;