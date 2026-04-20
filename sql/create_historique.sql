CREATE TABLE public.historique
(
   idhistorique bigserial, 
   typeoperation character varying(200), 
   dateoperation date, 
   CONSTRAINT pk_historique PRIMARY KEY (idhistorique)
) 
WITH (
  OIDS = FALSE
)
;
ALTER TABLE public.historique
  OWNER TO postgres;
ALTER TABLE historique
   ADD COLUMN idcertificat bigint;