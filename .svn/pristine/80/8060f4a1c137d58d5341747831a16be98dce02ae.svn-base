CREATE TABLE public.avoirconjoint
(
   idconjoint_a bigint, 
   idconjoint_b bigint, 
   CONSTRAINT fk_personne_a FOREIGN KEY (idconjoint_a) REFERENCES public.personne (idpersonne) ON UPDATE NO ACTION ON DELETE NO ACTION, 
   CONSTRAINT fk_personne_b FOREIGN KEY (idconjoint_b) REFERENCES public.personne (idpersonne) ON UPDATE NO ACTION ON DELETE NO ACTION, 
   CONSTRAINT unik_personne_a UNIQUE (idconjoint_a), 
   CONSTRAINT unik_personne_b UNIQUE (idconjoint_b), 
   CONSTRAINT pk_avoirconjoint PRIMARY KEY (idconjoint_a, idconjoint_b)
) 
WITH (
  OIDS = FALSE
)
;
ALTER TABLE public.avoirconjoint
  OWNER TO postgres;
COMMENT ON TABLE public.avoirconjoint
  IS 'Table contenant l''id de la personne marie et celui de sa femme';
