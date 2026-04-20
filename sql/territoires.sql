ALTER TABLE public.region
   ALTER COLUMN coderegion TYPE character varying(50);

ALTER TABLE public.region
   ALTER COLUMN nomregion TYPE character varying(50);

ALTER TABLE public.district
   ALTER COLUMN codedistrict TYPE character varying(10);

