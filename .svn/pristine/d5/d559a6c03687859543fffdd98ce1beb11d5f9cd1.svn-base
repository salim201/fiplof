CREATE TABLE public.autrechargesparcelle_d
(
   idcharge bigint, 
   idparcelle bigint, 
   CONSTRAINT pk_autrechargeparcelle_d PRIMARY KEY (idcharge, idparcelle), 
   CONSTRAINT fk_autrecharge FOREIGN KEY (idcharge) REFERENCES public.autrecharge (idcharge) ON UPDATE NO ACTION ON DELETE NO ACTION, 
   CONSTRAINT fk_parcelle FOREIGN KEY (idparcelle) REFERENCES public.parcelle_d (gid) ON UPDATE NO ACTION ON DELETE NO ACTION
) 
WITH (
  OIDS = FALSE
)
;
