DROP SEQUENCE IF EXISTS public.hypotheque_id_seq CASCADE;
ALTER TABLE public.hypotheque
DROP COLUMN idhypotheque CASCADE;

ALTER TABLE public.hypotheque
   ADD COLUMN idhypotheque bigserial;
   
ALTER TABLE public.hypotheque
  ADD CONSTRAINT pk_hypotheque PRIMARY KEY (idhypotheque);