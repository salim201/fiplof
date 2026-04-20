CREATE TABLE public.occupant_titrefoncier
(
   idtitrefoncier bigint, 
   idoccupant bigint, 
   CONSTRAINT pk_occtitre PRIMARY KEY (idtitrefoncier, idoccupant), 
   CONSTRAINT fk_titre FOREIGN KEY (idtitrefoncier) REFERENCES titrefoncier (gid) ON UPDATE NO ACTION ON DELETE NO ACTION, 
   CONSTRAINT fk_occupant FOREIGN KEY (idoccupant) REFERENCES occupant (idoccupant) ON UPDATE NO ACTION ON DELETE NO ACTION
) 
WITH (
  OIDS = FALSE
)
;
ALTER TABLE public.occupant_titrefoncier
  OWNER TO postgres;
