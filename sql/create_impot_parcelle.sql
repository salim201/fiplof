CREATE TABLE public.impot_parcelle
(
   id bigserial, 
   hetratany money, 
   annee smallint, 
   CONSTRAINT pk_impot_percelle PRIMARY KEY (id)
) 
WITH (
  OIDS = FALSE
)
;
ALTER TABLE public.impot_parcelle
  OWNER TO postgres;
