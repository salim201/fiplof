CREATE TABLE public.occupant
(
   idoccupant bigserial, 
   nom character varying(400), 
   CONSTRAINT pk_occupant PRIMARY KEY (idoccupant)
) 
WITH (
  OIDS = FALSE
)
;
ALTER TABLE public.occupant
  OWNER TO postgres;
