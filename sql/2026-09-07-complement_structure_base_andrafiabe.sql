--
-- Complément de structure pour la base andrafiabe
--
-- Généré le : 2026-09-07
-- Source     : base_ambovombe.sql (dump PostgreSQL 17.9 / pg_dump 18.3)
-- Cible      : base_andrafiabe.sql (dump PostgreSQL 9.3.5 / pg_dump 9.3.5)
--
-- Objectif   : aligner la STRUCTURE (uniquement) de la base andrafiabe sur
--              celle de la base ambovombe. Aucune donnée n'est copiée.
--
-- Compatibilité : PostgreSQL 9.3
--   Adaptations apportées par rapport au dump source (PG 17) :
--     * jsonb          -> json          (jsonb n'existe qu'à partir de PG 9.4)
--     * gen_random_uuid() retiré        (fonction absente du noyau avant PG 13 ;
--                                        l'application fournit l'UUID)
--     * EXECUTE FUNCTION -> EXECUTE PROCEDURE (syntaxe des triggers avant PG 11)
--     * directives PG17 exclues (SET transaction_timeout, row_security, ...)
--
-- Ordre des opérations :
--   1. Colonnes manquantes        (avant contraintes / triggers qui en dépendent)
--   2. Nouvelles tables
--   3. Contraintes (PK, UNIQUE, FK)
--   4. Index
--   5. Fonctions
--   6. Triggers
--

SET client_encoding = 'UTF8';

BEGIN;

-- ============================================================================
-- 1. COLONNES MANQUANTES
-- ============================================================================

ALTER TABLE public.anomalie ADD COLUMN iddemande bigint;

ALTER TABLE public.date_synchro ADD COLUMN datemaj timestamp without time zone DEFAULT now();

ALTER TABLE public.demande ADD COLUMN num_guichet_foncier character varying(50);

ALTER TABLE public.personne ADD COLUMN cin_nom_prenom_key character varying(300);

ALTER TABLE public.personnemorale ADD COLUMN idrepresentant bigint;

-- ============================================================================
-- 2. NOUVELLES TABLES
-- ============================================================================

--
-- Table fiplof_raw_ingestion
--
CREATE TABLE public.fiplof_raw_ingestion (
    id bigint NOT NULL,
    version_schema character varying(20),
    source_systeme character varying(100),
    type_message character varying(50),
    payload text NOT NULL,
    statut character varying(30) DEFAULT 'RECEIVED'::character varying,
    erreur text,
    id_batch character varying(100),
    created_at timestamp without time zone DEFAULT now(),
    processed_at timestamp without time zone,
    commune character varying(100),
    valid_parcelle text,
    error_parcelle text,
    traitement_statut character varying(30),
    traitement_parcelle_valide text,
    traitement_parcelle_refuse text,
    inbound_dossier_id uuid
);

--
-- Table inbound_dossiers
-- Adaptée PG 9.3 : payload jsonb -> json ; DEFAULT gen_random_uuid() retiré
--
CREATE TABLE public.inbound_dossiers (
    id uuid NOT NULL,
    source_transfer_id character varying(100) NOT NULL,
    source_system character varying(20) DEFAULT 'topomanager'::character varying NOT NULL,
    payload json NOT NULL,
    internal_status character varying(30) DEFAULT 'queued'::character varying NOT NULL,
    callback_status character varying(20) DEFAULT 'pending'::character varying NOT NULL,
    callback_error text,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);

--
-- Table inbound_idempotency
-- Adaptée PG 9.3 : response_body jsonb -> json
--
CREATE TABLE public.inbound_idempotency (
    idempotency_key character varying(64) NOT NULL,
    response_code integer NOT NULL,
    response_body json NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);

--
-- Table retour_externe
--
CREATE TABLE public.retour_externe (
    id integer NOT NULL,
    code_parcelle character varying(100),
    numero character varying(100),
    type_numero character(1),
    statut_retour character varying(20),
    date_statut_retour timestamp without time zone,
    geom public.geometry,
    CONSTRAINT retour_externe_statut_retour_check CHECK (((statut_retour)::text = ANY ((ARRAY['RETURNED'::character varying, 'VIEWED'::character varying, ''::character varying])::text[]))),
    CONSTRAINT retour_externe_type_numero_check CHECK ((type_numero = ANY (ARRAY['F'::bpchar, 'K'::bpchar])))
);

--
-- Table securite_compte_api
--
CREATE TABLE public.securite_compte_api (
    id_compte integer NOT NULL,
    login character varying(100) NOT NULL,
    mot_de_passe_hash text NOT NULL,
    nom_systeme character varying(100),
    actif boolean DEFAULT true,
    access_token text,
    refresh_token text,
    access_token_expire_at timestamp without time zone,
    refresh_token_expire_at timestamp without time zone,
    derniere_connexion timestamp without time zone,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    statut character varying(30) DEFAULT 'EN_ATTENTE'::character varying,
    nom character varying(100) NOT NULL,
    CONSTRAINT chk_statut_compte CHECK (((statut)::text = ANY ((ARRAY['PENDING'::character varying, 'VALIDATED'::character varying, 'REJECTED'::character varying])::text[])))
);

-- ============================================================================
-- 3. CONTRAINTES (PK, UNIQUE, FK)
-- ============================================================================

-- Clés primaires des nouvelles tables
ALTER TABLE ONLY public.fiplof_raw_ingestion
    ADD CONSTRAINT fiplof_raw_ingestion_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.inbound_dossiers
    ADD CONSTRAINT inbound_dossiers_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.inbound_idempotency
    ADD CONSTRAINT inbound_idempotency_pkey PRIMARY KEY (idempotency_key);

ALTER TABLE ONLY public.retour_externe
    ADD CONSTRAINT retour_externe_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.securite_compte_api
    ADD CONSTRAINT securite_compte_api_pkey PRIMARY KEY (id_compte);

-- Clés uniques
ALTER TABLE ONLY public.inbound_dossiers
    ADD CONSTRAINT inbound_dossiers_source_transfer_id_key UNIQUE (source_transfer_id);

ALTER TABLE ONLY public.securite_compte_api
    ADD CONSTRAINT securite_compte_api_login_key UNIQUE (login);

-- Contrainte unique sur la nouvelle colonne personne.cin_nom_prenom_key
ALTER TABLE ONLY public.personne
    ADD CONSTRAINT uk_personne_identity UNIQUE (cin_nom_prenom_key);

-- Clé étrangère sur la nouvelle colonne personnemorale.idrepresentant
ALTER TABLE ONLY public.personnemorale
    ADD CONSTRAINT fk_morale_physique FOREIGN KEY (idrepresentant) REFERENCES public.personne(idpersonne);

-- ============================================================================
-- 4. INDEX
-- ============================================================================

CREATE INDEX fki_morale_physique ON public.personnemorale USING btree (idrepresentant);

CREATE INDEX idx_compte_login ON public.securite_compte_api USING btree (login);

CREATE INDEX idx_fiplof_raw_ingestion_created ON public.fiplof_raw_ingestion USING btree (created_at DESC);

CREATE INDEX idx_fiplof_raw_ingestion_id ON public.fiplof_raw_ingestion USING btree (id DESC);

CREATE INDEX idx_fiplof_raw_ingestion_statut ON public.fiplof_raw_ingestion USING btree (statut);

CREATE INDEX ix_fiplof_raw_ingestion_inbound_dossier_id ON public.fiplof_raw_ingestion USING btree (inbound_dossier_id);

-- ============================================================================
-- 5. FONCTIONS
-- ============================================================================

CREATE FUNCTION public.fn_retour_externe_certificat() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_geom geometry;
    v_code_parcelle varchar;
BEGIN

    -- récupérer geom + code parcelle via la demande liée
    SELECT p.geom, p.codeparcelle
    INTO v_geom, v_code_parcelle
    FROM public.parcelle_d p
    INNER JOIN public.demande d
        ON d.gid = p.gid
    WHERE d.numdemande = NEW.numerodemande;

    -- insertion retour_externe
    INSERT INTO public.retour_externe (
        code_parcelle,
        numero,
        type_numero,
        statut_retour,
        date_statut_retour,
        geom
    )
    VALUES (
        v_code_parcelle,
        NEW.numerocertificat,
        'K',
        '',
        NULL,
        v_geom
    );

    RETURN NEW;
END;
$$;

CREATE FUNCTION public.fn_retour_externe_demande() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_geom geometry;
    v_code_parcelle varchar;
BEGIN

    -- récupérer geom et code parcelle
    SELECT geom, codeparcelle
    INTO v_geom, v_code_parcelle
    FROM public.parcelle_d
    WHERE gid = NEW.gid;

    -- insertion dans retour_externe
    INSERT INTO public.retour_externe (
        code_parcelle,
        numero,
        type_numero,
        statut_retour,
        date_statut_retour,
        geom
    )
    VALUES (
        v_code_parcelle,
        NEW.numdemande,
        'F',
        '',
        NULL,
        v_geom
    );

    RETURN NEW;
END;
$$;

CREATE FUNCTION public.json_try_parse(p_text text) RETURNS json
    LANGUAGE plpgsql IMMUTABLE
    AS $$
                BEGIN
                    RETURN p_text::json;
                EXCEPTION WHEN OTHERS THEN
                    RETURN NULL;
                END;
                $$;

CREATE FUNCTION public.set_personne_identity_key() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.cin_nom_prenom_key :=
        UPPER(
            COALESCE(NEW.numcipersonne, '') || '_' ||
            COALESCE(NEW.nompersonne, '') || '_' ||
            COALESCE(NEW.prenompersonne, '')
        );

    RETURN NEW;
END;
$$;

CREATE FUNCTION public.update_updated_at() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
   NEW.updated_at = CURRENT_TIMESTAMP;
   RETURN NEW;
END;
$$;

-- ============================================================================
-- 6. TRIGGERS
-- Adaptés PG 9.3 : EXECUTE FUNCTION -> EXECUTE PROCEDURE
-- ============================================================================

CREATE TRIGGER trg_set_personne_identity_key
    BEFORE INSERT OR UPDATE ON public.personne
    FOR EACH ROW
    EXECUTE PROCEDURE public.set_personne_identity_key();

CREATE TRIGGER trg_update_compte_api
    BEFORE UPDATE ON public.securite_compte_api
    FOR EACH ROW
    EXECUTE PROCEDURE public.update_updated_at();

CREATE TRIGGER trg_retour_externe_demande
    AFTER INSERT ON public.demande
    FOR EACH ROW
    EXECUTE PROCEDURE public.fn_retour_externe_demande();

CREATE TRIGGER trg_retour_externe_certificat
    AFTER INSERT ON public.certificat
    FOR EACH ROW
    EXECUTE PROCEDURE public.fn_retour_externe_certificat();

COMMIT;