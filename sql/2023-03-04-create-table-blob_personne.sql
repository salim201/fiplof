CREATE TABLE public.blob_personne
(
   idblob bigserial, 
   idpersonne bigint, 
   cin_recto bytea, 
   cin_verso bytea, 
   signature bytea, 
   empreinte_d bytea, 
   empreinte_g bytea, 
   CONSTRAINT pk_blob_personne PRIMARY KEY (idblob), 
   CONSTRAINT fk_blob_personne FOREIGN KEY (idpersonne) REFERENCES personne (idpersonne) ON UPDATE NO ACTION ON DELETE NO ACTION
) 
WITH (
  OIDS = FALSE
)
;
ALTER TABLE public.blob_personne
  OWNER TO postgres;