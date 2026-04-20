-- Table: public.groupe

-- DROP TABLE public.groupe;

CREATE TABLE public.groupe
(
  id serial,
  nom character varying(128),
  description text,
  CONSTRAINT groupe_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.groupe
  OWNER TO postgres;


INSERT INTO groupe(id, nom, description) VALUES(1, 'Admin', 'Administrateur de l''application');

ALTER TABLE public.utilisateur
  ADD COLUMN groupe_id integer;
ALTER TABLE public.utilisateur
  ADD FOREIGN KEY (groupe_id) REFERENCES public.groupe (id) ON UPDATE CASCADE ON DELETE CASCADE;


UPDATE utilisateur SET groupe_id = 1;