ALTER TABLE public.configuration
   ADD COLUMN date_dernier_maj timestamp without time zone;
ALTER TABLE public.configuration
   ADD COLUMN date_dernier_autobackup timestamp without time zone;
