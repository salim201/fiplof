CREATE TABLE public.impot_batiment
(
   id bigserial, 
   hetratrano money, 
   annee smallint, 
   CONSTRAINT pk_impot_batiment PRIMARY KEY (id)
) 
WITH (
  OIDS = FALSE
)
;
ALTER TABLE public.impot_batiment
  OWNER TO postgres;
