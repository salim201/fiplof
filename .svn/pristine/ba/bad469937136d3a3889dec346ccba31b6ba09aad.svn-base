-- View: public.vw_tss

-- DROP VIEW public.vw_tss;

CREATE OR REPLACE VIEW public.vw_tss AS 
 SELECT terain_status_specifique.gid,
    terain_status_specifique.fn_fg,
    terain_status_specifique.demandeur,
    terain_status_specifique.sur_plan,
    terain_status_specifique.obs,
    terain_status_specifique.geom
   FROM terain_status_specifique;

ALTER TABLE public.vw_tss
  OWNER TO postgres;