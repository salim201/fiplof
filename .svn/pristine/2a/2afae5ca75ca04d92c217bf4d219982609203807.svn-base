ALTER TABLE public.parcelle_d
    ADD COLUMN inventaire boolean;

ALTER TABLE public.parcelle_d
    ADD COLUMN sujet_demande boolean;

ALTER TABLE public.parcelle_d
    ADD COLUMN date_inventaire date;

ALTER TABLE public.parcelle_d
    ADD COLUMN user_import_inv BIGINT;

ALTER TABLE public.parcelle_d
    ADD COLUMN date_import_inv date;

ALTER TABLE public.parcelle_d
    ADD COLUMN ref_import character varying(64);

--path vers image PVRL
ALTER TABLE public.demande
    ADD COLUMN pvrl character varying(250);

ALTER TABLE public.demande
    ADD COLUMN cqe boolean;

ALTER TABLE public.demande
    ADD COLUMN date_cqe date;

--Responsable cqe
ALTER TABLE public.demande
    ADD COLUMN resp_cqe character varying(250);

ALTER TABLE public.demande
    ADD COLUMN user_cqe BIGINT;

-- path vers image CIN
ALTER TABLE public.personne
    ADD COLUMN cin_recto character varying(250);

ALTER TABLE public.personne
    ADD COLUMN cin_verso character varying(250);

-- path signature
ALTER TABLE public.personne
    ADD COLUMN signature character varying(250);

-- path empreintes
ALTER TABLE public.personne
    ADD COLUMN empreinte_d character varying(250);

ALTER TABLE public.personne
    ADD COLUMN empreinte_g character varying(250);
	
CREATE TABLE public.role_crl
(
    id_role serial,
    libelle_role character varying(100),
    PRIMARY KEY (id_role)
)
WITH (
    OIDS = FALSE
);

ALTER TABLE public.role_crl
    OWNER to postgres;
	

CREATE TABLE public.demande_crl
(
    idpersonne bigint NOT NULL,
    iddemande bigint NOT NULL,
    id_role smallint NOT NULL,
    -- coché pour membres RL lors de la RL
    rl boolean,
    -- coché pour membre RL à l'affichage
    affiche boolean,
    CONSTRAINT demande_crl_pkey PRIMARY KEY (idpersonne, iddemande, id_role),
    CONSTRAINT demande_crl_id_role_fkey FOREIGN KEY (id_role)
        REFERENCES public.role_crl (id_role) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT demande_crl_iddemande_fkey FOREIGN KEY (iddemande)
        REFERENCES public.demande (iddemande) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT demande_crl_idpersonne_fkey FOREIGN KEY (idpersonne)
        REFERENCES public.personne (idpersonne) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.demande_crl
    OWNER to postgres;
	
	
	
	
	