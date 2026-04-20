CREATE TABLE public.contribuables_parcelle
(
   idpersonne bigint, 
   idparcelle bigint, 
   contribuable boolean, 
   CONSTRAINT pk_contr_parcelle PRIMARY KEY (idpersonne, idparcelle), 
   CONSTRAINT fk_personne FOREIGN KEY (idpersonne) REFERENCES public.personne (idpersonne) ON UPDATE NO ACTION ON DELETE NO ACTION, 
   CONSTRAINT fk_parcelle FOREIGN KEY (idparcelle) REFERENCES public.parcelle_d (gid) ON UPDATE NO ACTION ON DELETE NO ACTION
) 
WITH (
  OIDS = FALSE
)
;
ALTER TABLE public.contribuables_parcelle
  OWNER TO postgres;
