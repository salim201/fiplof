CREATE TABLE public.titre
(
   gid bigserial, 
   titres character varying(25), 
   propriete character varying(100), 
   sur_plan double precision, 
   titre_r character varying(100), 
   parcelle character varying(50), 
   partie character varying(50), 
   feuille character varying(50), 
   geom public.geometry, 
   CONSTRAINT pk_titre PRIMARY KEY (gid)
) 
WITH (
  OIDS = FALSE
)
;
