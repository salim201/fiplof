DROP VIEW public.vw_demande;

CREATE OR REPLACE VIEW public.vw_demande AS
 SELECT p.gid,
    p.geom,
    p.numdemande,
    d.idcommune
   FROM demande d
     RIGHT JOIN parcelle_d p ON p.gid = d.gid
   WHERE p.estfiscalite is null or p.estfiscalite = 0 or conversion = 1;

ALTER TABLE public.vw_demande
  OWNER TO postgres;
