DROP VIEW IF EXISTS public.vw_shape_certificat;
CREATE OR REPLACE VIEW public.vw_shape_certificat AS 
 SELECT p.geom,
    c.numerocertificat,
    c.numerodemande,
    p.codeparcelle,
    pers.nompersonne AS nom_prop,
    pers.prenompersonne AS prenom_prop,
    pers.numcipersonne,
    pers.datecipersonne,
    pers.lieucipersonne,
    pers.numactenaissancepersonne,
    pers.dateactenaissancepersonne,
    pers.lieuactenaissancepersonne,
    p.surface,
    d.datedemande,
    d.datedecision,
    d.numdecision,
    d.debut_affichage,
    d.fin_affichage,
    d.datereconnaissance,
    COALESCE(d.region, ''::character varying) AS region,
    d.district,
    com.nomcommune,
    fkt.nomfokontany,
    COALESCE(h.nomhameau, ''::character varying) AS nomhameau,
    d.categorie,
    d.consistance
   FROM certificat c
     JOIN parcelle_d p ON p.idcertificat = c.idcertificat
     JOIN demande d ON d.gid = p.gid
     JOIN proprietaireparcelle pp ON p.gid = pp.idparcelle
     JOIN personne pers ON pp.idpersonne = pers.idpersonne
     JOIN commune com ON com.idcommune = d.idcommune
     LEFT JOIN fokontany fkt ON fkt.idfokontany = d.idfokontany
     LEFT JOIN hameau h ON h.idhameau = p.idhameau;

ALTER TABLE public.vw_shape_certificat
  OWNER TO postgres;
