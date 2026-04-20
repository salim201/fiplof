CREATE SEQUENCE public.actedj_gid_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1569
  CACHE 1;
ALTER TABLE public.actedj_gid_seq
  OWNER TO postgres;
  
CREATE TABLE public.actedejalance
(
  id bigint NOT NULL DEFAULT nextval('actedj_gid_seq'::regclass),
  idacte bigint,
  typeacte bigint
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.actedejalance
  OWNER TO postgres;


ALTER TABLE public.actedejalance
  ADD CONSTRAINT pk_actedejalance PRIMARY KEY(id);
  
--ALTER TABLE public.actedejalance ALTER COLUMN id SET NOT NULL;
--ALTER TABLE public.actedejalance ALTER COLUMN id SET DEFAULT nextval('actedj_gid_seq'::regclass);

