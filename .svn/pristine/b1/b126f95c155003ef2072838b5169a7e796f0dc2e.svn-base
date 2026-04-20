CREATE TABLE public.groupe_acces
(
   id bigserial,
   groupe_id integer,
   menu character varying(255),
   acces_c boolean,
   acces_r boolean,
   acces_u boolean,
   acces_d boolean,
   acces_p boolean,
   PRIMARY KEY (id),
   FOREIGN KEY (groupe_id) REFERENCES public.groupe (id) ON UPDATE CASCADE ON DELETE CASCADE
)
WITH (
  OIDS = FALSE
)
;

ALTER TABLE public.groupe_acces
  ADD UNIQUE (groupe_id, menu);
