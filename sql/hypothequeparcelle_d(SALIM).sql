CREATE TABLE public.hypothequeparcelle_d
(
   idhypotheque bigint, 
   idparcelle bigint, 
   CONSTRAINT pk_hypothequeparcelle_d PRIMARY KEY (idhypotheque, idparcelle), 
   CONSTRAINT fk_hypotheque FOREIGN KEY (idhypotheque) REFERENCES public.hypotheque (idhypotheque) ON UPDATE NO ACTION ON DELETE NO ACTION, 
   CONSTRAINT fk_parcelle FOREIGN KEY (idparcelle) REFERENCES public.parcelle_d (gid) ON UPDATE NO ACTION ON DELETE NO ACTION
) 
WITH (
  OIDS = FALSE
)
;
