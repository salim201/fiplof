CREATE TABLE public.impot_minimum
(
    id_impotminimum serial,
    type character varying(6) NOT NULL,
    valeur real,
    annee character varying,
    PRIMARY KEY (id_impotminimum)
)
WITH (
    OIDS = FALSE
);

ALTER TABLE public.impot_minimum
    OWNER to postgres;