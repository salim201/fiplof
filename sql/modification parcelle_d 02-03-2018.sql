ALTER TABLE public.parcelle_d ADD COLUMN srisraparcelle character varying(5);
ALTER TABLE public.parcelle_d ADD COLUMN codeparcelle character varying(10);
ALTER TABLE public.parcelle_d ADD COLUMN numcertificat character varying(20);
ALTER TABLE public.parcelle_d
   ADD COLUMN estfiscalite smallint;