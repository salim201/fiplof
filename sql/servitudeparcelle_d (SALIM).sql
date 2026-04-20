CREATE TABLE public.servitudeparcelle_d
(
   idservitude bigint, 
   idparcelle bigint, 
   CONSTRAINT pk_servitude_parcelle PRIMARY KEY (idservitude, idparcelle), 
   CONSTRAINT fk_servitude FOREIGN KEY (idservitude) REFERENCES public.servitude (idservitude) ON UPDATE NO ACTION ON DELETE NO ACTION, 
   CONSTRAINT fk_parcelle FOREIGN KEY (idparcelle) REFERENCES public.parcelle_d (gid) ON UPDATE NO ACTION ON DELETE NO ACTION
) 
WITH (
  OIDS = FALSE
)
;