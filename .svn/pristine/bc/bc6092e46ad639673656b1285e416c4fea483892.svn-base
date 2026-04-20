CREATE SEQUENCE public.hameauidseq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE public.hameauidseq
  OWNER TO postgres;
ALTER TABLE public.hameau ALTER COLUMN idhameau SET DEFAULT nextval('hameauidseq'::regclass);