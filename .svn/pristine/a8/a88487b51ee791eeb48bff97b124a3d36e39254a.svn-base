CREATE TABLE public.blob_voisin
(
   idpoint bigint, 
   idparcelle bigint, 
   voisin character varying(256), 
   signature_fic bytea, 
   signature_name character varying(128), 
   signature_ext character varying(10), 
   CONSTRAINT pk_blob_voisin PRIMARY KEY (idpoint, idparcelle, voisin)
) 
WITH (
  OIDS = FALSE
)
;