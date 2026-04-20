CREATE OR REPLACE VIEW public.vw_titre AS 
 SELECT titre.gid,
    titre.titres,
    titre.propriete,
    titre.sur_plan,
    titre.titre_r,
    titre.parcelle,
    titre.partie,
    titre.feuille,
    titre.geom
   FROM titre;

ALTER TABLE public.vw_titre
  OWNER TO postgres;

  CREATE OR REPLACE VIEW public.vw_cadastre AS 
 SELECT cadastre.gid,
    cadastre.nom_section,
    cadastre.section,
    cadastre.parcelle,
    cadastre.nom_plan,
    cadastre.geom
   FROM cadastre;

ALTER TABLE public.vw_cadastre
  OWNER TO postgres;

CREATE OR REPLACE VIEW public.vw_demandefn AS 
 SELECT demandefn.gid,
    demandefn.fn_fg,
    demandefn.demandeur,
    demandefn.sur_plan,
    demandefn.geom
   FROM demandefn;

ALTER TABLE public.vw_demandefn
  OWNER TO postgres;