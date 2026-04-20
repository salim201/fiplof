-- Sequence: public.pointscardinaux_idpointscardinaux_seq

-- DROP SEQUENCE public.pointscardinaux_idpointscardinaux_seq;

CREATE SEQUENCE public.pointscardinaux_idpointscardinaux_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE public.pointscardinaux_idpointscardinaux_seq
  OWNER TO postgres;

-- Table: public.pointscardinaux

-- DROP TABLE public.pointscardinaux;

CREATE TABLE public.pointscardinaux
(
  idpointscardinaux integer NOT NULL DEFAULT nextval('pointscardinaux_idpointscardinaux_seq'::regclass),
  "position" character varying,
  fanondroana character varying,
  CONSTRAINT pk_pointscardinaux PRIMARY KEY (idpointscardinaux),
  CONSTRAINT ui_position UNIQUE ("position")
)
WITH (
  OIDS=FALSE
);

ALTER TABLE public.pointscardinaux
   ALTER COLUMN "position" SET NOT NULL;
   
ALTER TABLE public.pointscardinaux
  OWNER TO postgres;
