-- Sequence: public.autrecharge_idcharge_seq

-- DROP SEQUENCE public.autrecharge_idcharge_seq;

CREATE SEQUENCE public.autrecharge_idcharge_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE public.autrecharge_idcharge_seq
  OWNER TO postgres;

  
-- Novaina type date ny date fa character iz tam farany teo, dia novaina koa ny type idcharge fa character iz teo

-- Table: public.autrecharge

-- DROP TABLE public.autrecharge;

-- Table: public.autrecharge

-- DROP TABLE public.autrecharge;

CREATE TABLE public.autrecharge
(
  type character(32),
  descriptioncharge character(32),
  dateinscriptionregistre date,
  idcharge bigint NOT NULL DEFAULT nextval('autrecharge_idcharge_seq'::regclass),
  CONSTRAINT pk_autrecharge PRIMARY KEY (idcharge)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.autrecharge
  OWNER TO postgres;

