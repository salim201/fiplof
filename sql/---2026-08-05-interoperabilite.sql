ALTER TABLE personne DROP CONSTRAINT uk_cin;
ALTER TABLE personne
ADD COLUMN cin_nom_prenom_key varchar(300);
UPDATE personne
SET cin_nom_prenom_key =
UPPER(numcipersonne || '_' || nompersonne || '_' || prenompersonne);
ALTER TABLE personne
ADD CONSTRAINT uk_personne_identity UNIQUE (cin_nom_prenom_key);

CREATE OR REPLACE FUNCTION set_personne_identity_key()
RETURNS trigger AS $$
BEGIN
    NEW.cin_nom_prenom_key :=
        UPPER(
            COALESCE(NEW.numcipersonne, '') || '_' ||
            COALESCE(NEW.nompersonne, '') || '_' ||
            COALESCE(NEW.prenompersonne, '')
        );

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER trg_set_personne_identity_key
BEFORE INSERT OR UPDATE
ON personne
FOR EACH ROW
EXECUTE PROCEDURE set_personne_identity_key();



CREATE TABLE fiplof_raw_ingestion (
    id BIGSERIAL PRIMARY KEY,
    version_schema VARCHAR(20),
    source_systeme VARCHAR(100),
    type_message VARCHAR(50),
    payload TEXT NOT NULL,
    statut VARCHAR(30) DEFAULT 'RECEIVED',
    erreur TEXT,
	id_batch character varying(100),
    created_at TIMESTAMP DEFAULT NOW(),
    processed_at TIMESTAMP NULL
);


CREATE TABLE securite_compte_api (
    id_compte SERIAL PRIMARY KEY,

    login VARCHAR(100) NOT NULL UNIQUE,
    mot_de_passe_hash TEXT NOT NULL,

    nom_systeme VARCHAR(100),

    actif BOOLEAN DEFAULT TRUE,

    access_token TEXT,
    refresh_token TEXT,

    access_token_expire_at TIMESTAMP,
    refresh_token_expire_at TIMESTAMP,

    derniere_connexion TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = CURRENT_TIMESTAMP;
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_compte_api
BEFORE UPDATE ON securite_compte_api
FOR EACH ROW
EXECUTE PROCEDURE update_updated_at();
CREATE INDEX idx_compte_login
ON securite_compte_api(login);

ALTER TABLE public.securite_compte_api
ADD COLUMN statut VARCHAR(30) DEFAULT 'EN_ATTENTE';
ALTER TABLE public.securite_compte_api
ADD CONSTRAINT chk_statut_compte
CHECK (statut IN ('EN_ATTENTE', 'APPROUVE', 'REJETE'));


ALTER TABLE public.securite_compte_api
DROP CONSTRAINT IF EXISTS chk_statut_compte;

ALTER TABLE public.securite_compte_api
ADD CONSTRAINT chk_statut_compte
CHECK (
    statut IN ('PENDING', 'VALIDATED', 'REJECTED')
);


ALTER TABLE public.fiplof_raw_ingestion
ADD COLUMN commune character varying(100);
ALTER TABLE public.fiplof_raw_ingestion
ADD COLUMN valid_parcelle text,
ADD COLUMN error_parcelle text;
ALTER TABLE public.fiplof_raw_ingestion
ADD COLUMN traitement_statut character varying(30),
ADD COLUMN traitement_parcelle_valide text,
ADD COLUMN traitement_parcelle_refuse text;

ALTER TABLE securite_compte_api
ADD COLUMN nom character varying(100) NOT NULL;

CREATE TABLE public.retour_externe
(
    id SERIAL PRIMARY KEY,

    code_parcelle VARCHAR(100),

    numero VARCHAR(100),

    -- F = Fangatahana
    -- K = Karatany
    type_numero CHAR(1)
    CHECK (type_numero IN ('F', 'K')),

    -- RETURNED = accepté/retourné
    -- VIEWED = visualisé seulement
    -- '' = aucun statut
    statut_retour VARCHAR(20)
    CHECK (statut_retour IN ('RETURNED', 'VIEWED', '')),

    date_statut_retour TIMESTAMP
);

ALTER TABLE public.retour_externe
ADD COLUMN geom geometry;



CREATE OR REPLACE FUNCTION public.fn_retour_externe_demande()
RETURNS trigger AS
$$
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
$$
LANGUAGE plpgsql;
CREATE TRIGGER trg_retour_externe_demande
AFTER INSERT ON public.demande
FOR EACH ROW
EXECUTE PROCEDURE public.fn_retour_externe_demande();

CREATE OR REPLACE FUNCTION public.fn_retour_externe_certificat()
RETURNS trigger AS
$$
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
$$
LANGUAGE plpgsql;


CREATE TRIGGER trg_retour_externe_certificat
AFTER INSERT ON public.certificat
FOR EACH ROW
EXECUTE PROCEDURE public.fn_retour_externe_certificat();


VACUUM ANALYZE public.fiplof_raw_ingestion;
CREATE INDEX IF NOT EXISTS idx_fiplof_raw_ingestion_id
ON public.fiplof_raw_ingestion(id DESC);
CREATE INDEX IF NOT EXISTS idx_fiplof_raw_ingestion_created
ON public.fiplof_raw_ingestion(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_fiplof_raw_ingestion_statut
ON public.fiplof_raw_ingestion(statut);


CREATE TABLE inbound_dossiers (
    id                 VARCHAR(36) PRIMARY KEY, -- UUID côté Python
    source_transfer_id VARCHAR(100) NOT NULL UNIQUE,
    source_system      VARCHAR(20)  NOT NULL DEFAULT 'topomanager',

    -- JSON remplacé par TEXT
    payload            TEXT NOT NULL,

    internal_status    VARCHAR(30)  NOT NULL DEFAULT 'queued',
    callback_status    VARCHAR(20)  NOT NULL DEFAULT 'pending',
    callback_error     TEXT,

    created_at         TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at         TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);


CREATE TABLE inbound_idempotency (
    idempotency_key VARCHAR(64) PRIMARY KEY,
    response_code   INT NOT NULL,

    -- JSONB remplacé par TEXT
    response_body   TEXT NOT NULL,

    created_at      TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);