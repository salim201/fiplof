CREATE TABLE public.acces
(
   id bigserial,
   nom character varying(64),
   libelle character varying(128),
   PRIMARY KEY (id),
   UNIQUE (nom)
)
WITH (
  OIDS = FALSE
)
;

INSERT INTO public.acces(nom, libelle)
   VALUES
   ('DEMANDE/CREATE', 'Creation Demande'),
   ('DEMANDE/READ', 'Consultation Demande'),
   ('DEMANDE/EDIT_INFO', 'Edition des informations des demandes'),
   ('DEMANDE/EDIT_GEO', 'Edition des geometries des demandes');


DROP TABLE public.groupe_acces CASCADE;

CREATE TABLE public.groupe_acces
(
   id bigserial,
   groupe_id bigint,
   acces_id bigint,
   autorise boolean,
   PRIMARY KEY (id),
   FOREIGN KEY (groupe_id) REFERENCES public.groupe (id) ON UPDATE CASCADE ON DELETE CASCADE,
   FOREIGN KEY (acces_id) REFERENCES public.acces (id) ON UPDATE CASCADE ON DELETE CASCADE
)
WITH (
  OIDS = FALSE
)
;
