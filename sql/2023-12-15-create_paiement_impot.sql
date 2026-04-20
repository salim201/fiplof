CREATE TABLE public.fi_paiement_impot
(
   id_paiement bigserial, 
   date date, 
   montant real, 
   numquittance character varying(50), 
   idpersonne bigint, 
   CONSTRAINT pk_paiement_impot PRIMARY KEY (id_paiement), 
   CONSTRAINT fk_personne FOREIGN KEY (idpersonne) REFERENCES public.personne (idpersonne) ON UPDATE NO ACTION ON DELETE NO ACTION
) 
WITH (
  OIDS = FALSE
)
;
ALTER TABLE public.fi_paiement_impot
  OWNER TO postgres;