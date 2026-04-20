CREATE TABLE public.personne
(
   idpersonne bigserial, 
   nompersonne character varying(100), 
   prenompersonne character varying(100), 
   sexepersonne character varying(25), 
   datenaissancepersonne date, 
   nevers smallint, 
   lieunaissancepersonne character varying(100), 
   numcipersonne character varying(20), 
   datecipersonne date, 
   lieucipersonne character varying(100), 
   numactenaissancepersonne character varying(50), 
   dateactenaissancepersonne date, 
   lieuactenaissancepersonne character varying(100), 
   adressepersonne character varying(100), 
   situationmatrimoniale smallint DEFAULT 0, 
   nompere character varying(150), 
   nommere character varying(150), 
   CONSTRAINT pk_personne PRIMARY KEY (idpersonne)
) 
WITH (
  OIDS = FALSE
)
;
ALTER TABLE public.personne
  OWNER TO postgres;
COMMENT ON COLUMN public.personne.situationmatrimoniale IS '0 => celibataire, 1 => marie, 2 => veuf';
COMMENT ON TABLE public.personne
  IS 'Table personne en generale, permettant de gerer les proprietaires, les demandeurs et les contribuables';
