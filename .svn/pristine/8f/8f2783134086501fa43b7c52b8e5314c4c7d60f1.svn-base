-- Sequence: public.z_certifiable_gid_seq

-- DROP SEQUENCE public.z_certifiable_gid_seq;

CREATE SEQUENCE public.z_certifiable_gid_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE public.z_certifiable_gid_seq
  OWNER TO postgres;

-- Table: public.z_certifiable

-- DROP TABLE public.z_certifiable;

CREATE TABLE public.z_certifiable
(
  gid integer NOT NULL DEFAULT nextval('z_certifiable_gid_seq'::regclass),
  id integer,
  crtfbl integer,
  geom geometry(Polygon,29702),
  CONSTRAINT z_certifiable_pkey PRIMARY KEY (gid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.z_certifiable
  OWNER TO postgres;

-- Index: public.z_certifiable_geom_idx

-- DROP INDEX public.z_certifiable_geom_idx;

CREATE INDEX z_certifiable_geom_idx
  ON public.z_certifiable
  USING gist
  (geom);

-- View: public.vw_z_certifiable

-- DROP VIEW public.vw_z_certifiable;

CREATE OR REPLACE VIEW public.vw_z_certifiable AS 
 SELECT z_certifiable.gid,
    z_certifiable.id,
    z_certifiable.crtfbl,
    z_certifiable.geom
   FROM z_certifiable;

ALTER TABLE public.vw_z_certifiable
  OWNER TO postgres;