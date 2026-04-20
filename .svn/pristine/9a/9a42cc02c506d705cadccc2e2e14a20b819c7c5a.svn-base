DROP VIEW vw_fiscalite;

CREATE OR REPLACE VIEW public.vw_fiscalite AS
 SELECT p.gid,
    p.geom,
    p.codeparcelle as numero
   FROM parcelle_d p
  WHERE p.estfiscalite = 1;

ALTER TABLE public.vw_fiscalite
  OWNER TO postgres;
