DROP VIEW vw_fiscalite;

CREATE OR REPLACE VIEW vw_fiscalite AS 
 SELECT p.gid,
    p.geom,
    p.numero
   FROM parcelle_d p
  WHERE p.estfiscalite = 1;

ALTER TABLE vw_fiscalite
  OWNER TO postgres;