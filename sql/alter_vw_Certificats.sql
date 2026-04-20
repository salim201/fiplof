-- View: public.vw_certificat
DROP VIEW public.vw_certificat;

CREATE OR REPLACE VIEW public.vw_certificat AS 
 SELECT p.gid,
    p.geom,
    c.numerocertificat,
    c.idcommune
   FROM certificat c
     JOIN parcelle_d p ON p.idcertificat = c.idcertificat;

ALTER TABLE public.vw_certificat
  OWNER TO postgres;
