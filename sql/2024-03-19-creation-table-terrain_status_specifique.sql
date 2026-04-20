CREATE TABLE public.terain_status_specifique
(
   gid bigserial, 
   fn_fg character varying(100), 
   demandeur character varying(100), 
   sur_plan double precision, 
   obs character varying(100), 
   geom public.geometry, 
   CONSTRAINT pk_tss PRIMARY KEY (gid)
) 
WITH (
  OIDS = FALSE
)
;
