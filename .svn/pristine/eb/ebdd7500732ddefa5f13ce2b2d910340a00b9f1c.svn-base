CREATE TABLE public.avoir_demande
(
   idpersonne bigint, 
   iddemande bigint, 
   idparcelle bigint, 
   CONSTRAINT fk_personne FOREIGN KEY (idpersonne) REFERENCES public.personne (idpersonne) ON UPDATE NO ACTION ON DELETE NO ACTION, 
   CONSTRAINT fk_demande FOREIGN KEY (iddemande) REFERENCES public.demande (iddemande) ON UPDATE NO ACTION ON DELETE NO ACTION, 
   CONSTRAINT fk_parcelle_d FOREIGN KEY (idparcelle) REFERENCES public.parcelle_d (gid) ON UPDATE NO ACTION ON DELETE NO ACTION, 
   CONSTRAINT pk_avoir_demande PRIMARY KEY (idpersonne, iddemande)
) 
WITH (
  OIDS = FALSE
)
;
ALTER TABLE public.avoir_demande
  OWNER TO postgres;
COMMENT ON TABLE public.avoir_demande
  IS 'Table liant Personne, demande et parcelle_d';
