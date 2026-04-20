CREATE TABLE public.menage
(
    id_menage bigserial NOT NULL,
    code_menage character varying(125) NOT NULL,
    nombre_homme integer DEFAULT 0,
    nombre_femme integer DEFAULT 0,
    nombre_enfant integer DEFAULT 0,
    nombre_homme_actif integer DEFAULT 0,
    nombre_femme_active integer DEFAULT 0,
    possede_terre boolean DEFAULT False,
    acces_ressource boolean DEFAULT True
)
WITH (
    OIDS = FALSE
);

ALTER TABLE  public.menage
    OWNER to postgres;
	
ALTER TABLE public.menage
    ADD CONSTRAINT pk_menage PRIMARY KEY (id_menage);
	
ALTER TABLE public.menage
    ADD CONSTRAINT uk_code_menage UNIQUE (code_menage);
	
-- create table personne menage
	
CREATE TABLE public.personne_menage
(
    idpersonne bigint NOT NULL,
    id_menage bigint NOT NULL,
    est_chef boolean DEFAULT False
)
WITH (
    OIDS = FALSE
);

ALTER TABLE public.personne_menage
    OWNER to postgres;
	
ALTER TABLE public.personne_menage
    ADD CONSTRAINT pk_personne_menage PRIMARY KEY (idpersonne, id_menage);
	
ALTER TABLE public.personne_menage
    ADD CONSTRAINT fk_personne FOREIGN KEY (idpersonne)
    REFERENCES public.personne (idpersonne) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;
CREATE INDEX fki_fk_personne
    ON public.personne_menage(idpersonne);
	
ALTER TABLE public.personne_menage
    ADD CONSTRAINT fk_menage FOREIGN KEY (id_menage)
    REFERENCES public.menage (id_menage) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;
CREATE INDEX fki_fk_menage
    ON public.personne_menage(id_menage);