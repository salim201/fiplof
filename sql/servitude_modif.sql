DROP SEQUENCE IF EXISTS public.servitude_id_seq CASCADE;
ALTER TABLE public.servitude
DROP COLUMN idservitude CASCADE;

ALTER TABLE public.servitude
   ADD COLUMN idservitude bigserial;
   
ALTER TABLE public.servitude
  ADD CONSTRAINT pk_servitude PRIMARY KEY (idservitude);

