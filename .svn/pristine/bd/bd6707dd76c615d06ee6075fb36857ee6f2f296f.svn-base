-- View: vw_demande

DROP VIEW vw_demande;

CREATE OR REPLACE VIEW vw_demande AS 
 SELECT p.gid,
    p.geom,
    COALESCE(p.numdemande, p.codeparcelle) AS numdemande,
    d.idcommune
   FROM demande d
     RIGHT JOIN parcelle_d p ON p.gid = d.gid
  WHERE p.estfiscalite IS NULL OR p.estfiscalite = 0 OR p.conversion = 1;

ALTER TABLE vw_demande
  OWNER TO postgres;