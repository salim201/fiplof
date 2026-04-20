ALTER TABLE public.categorie
   ALTER COLUMN v_venale SET DEFAULT 0;
   ALTER TABLE public.categorie
   ALTER COLUMN u_surface TYPE character varying(10);
   ALTER TABLE public.categorie
   ALTER COLUMN u_venale TYPE character varying(10);
   ALTER TABLE public.categorie
   ALTER COLUMN taux SET DEFAULT 1;

