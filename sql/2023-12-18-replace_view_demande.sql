-- View: public.vw_demande

DROP VIEW public.vw_demande;

CREATE OR REPLACE VIEW public.vw_demande AS 
 SELECT p.gid,
    p.geom,
    COALESCE(p.numdemande, p.codeparcelle) AS numdemande,
    d.idcommune
   FROM demande d
     RIGHT JOIN parcelle_d p ON p.gid = d.gid
  WHERE p.estfiscalite IS NULL OR p.estfiscalite = 0 OR p.numdemande IS NOT NULL OR p.conversion = 1;

ALTER TABLE public.vw_demande
  OWNER TO postgres;