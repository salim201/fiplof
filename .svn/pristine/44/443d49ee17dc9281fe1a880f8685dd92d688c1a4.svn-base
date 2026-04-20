-- 2022-05-12
CREATE OR REPLACE VIEW public.vw_certificat AS 
 SELECT p.gid,
    p.geom,
    c.numerocertificat,
    c.idcommune,
    c.idcertificat
   FROM certificat c
     JOIN parcelle_d p ON p.idcertificat = c.idcertificat;

ALTER TABLE public.vw_certificat
  OWNER TO postgres;
  
-- 2022-05-13
ALTER TABLE public.certificat
  ADD CONSTRAINT uk_numcertificat UNIQUE (numerocertificat) USING INDEX TABLESPACE pg_default;
  
-- 2022-05-14
ALTER TABLE public.demande ADD COLUMN datedecision date;


ALTER TABLE public.commune
   ADD COLUMN csv_id character varying(32);  
ALTER TABLE public.district
   ADD COLUMN csv_id character varying(32);   
ALTER TABLE public.fokontany
   ADD COLUMN csv_id character varying(32);  
ALTER TABLE public.hameau
   ADD COLUMN csv_id character varying(32);   
ALTER TABLE public.personne
   ADD COLUMN csv_id character varying(32);
ALTER TABLE public.region
   ADD COLUMN csv_id character varying(32);   
-- 2022-05-20
ALTER TABLE public.personnemorale
   ADD COLUMN csv_id character varying(32);
   
ALTER TABLE public.typepersonnemorale
   ADD COLUMN csv_id character varying(32);
   
-- 2022-05-23

ALTER TABLE public.avoir_demande ADD COLUMN csv_id character varying(32);

ALTER TABLE public.demande ADD COLUMN csv_id character varying(32);

ALTER TABLE public.demande
   ADD COLUMN code_parcelle character varying(32);
   
ALTER TABLE public.parcelle_d ADD COLUMN csv_id character varying(32);

ALTER TABLE public.personnemoraleparcelle
   ADD COLUMN iddemande bigint;
ALTER TABLE public.personnemoraleparcelle
   ADD COLUMN csv_id character varying(32);
   
-- 2022-05-24
ALTER TABLE public.projetcouche ADD COLUMN plofpaps integer;
ALTER TABLE public.projetcouche ALTER COLUMN plofpaps SET DEFAULT 0;

-- 2022-05-26
CREATE OR REPLACE VIEW public.vw_certificat AS 
 SELECT p.gid,
    p.geom,
    c.numerocertificat,
    c.idcommune,
    c.idcertificat
   FROM certificat c
     JOIN parcelle_d p ON p.idcertificat = c.idcertificat;

ALTER TABLE public.vw_certificat
  OWNER TO postgres;
  
 ALTER TABLE public.certificat
  ADD CONSTRAINT uk_numcertificat UNIQUE (numerocertificat) USING INDEX TABLESPACE pg_default;

ALTER TABLE public.demande ADD COLUMN datedecision date;

ALTER TABLE public.projetcouche ADD COLUMN plofpaps integer;
ALTER TABLE public.projetcouche ALTER COLUMN plofpaps SET DEFAULT 0;


ALTER TABLE public.avoir_demande ADD COLUMN csv_id character varying(32);
ALTER TABLE demande
   ADD COLUMN categorie character varying;
   ALTER TABLE public.personnemorale
   ADD COLUMN csv_id character varying(32);
ALTER TABLE public.commune
   ADD COLUMN csv_id character varying(32);
   ALTER TABLE public.demande ADD COLUMN csv_id character varying(32);
ALTER TABLE public.demande
   ADD COLUMN code_parcelle character varying(32);
   ALTER TABLE public.district
   ADD COLUMN csv_id character varying(32);
   ALTER TABLE public.fokontany
   ADD COLUMN csv_id character varying(32);
   
   ALTER TABLE public.hameau
   ADD COLUMN csv_id character varying(32);
   
   ALTER TABLE public.parcelle_d ADD COLUMN csv_id character varying(32);
   ALTER TABLE parcelle_d
   ADD COLUMN anomalie boolean;
   ALTER TABLE parcelle_d
   ADD COLUMN limitrophe boolean;
   ALTER TABLE personne ADD COLUMN csv_id character varying(32);
   ALTER TABLE public.personnemoraleparcelle
   ADD COLUMN iddemande bigint;
	ALTER TABLE public.personnemoraleparcelle
   ADD COLUMN csv_id character varying(32);
   ALTER TABLE public.region
   ADD COLUMN csv_id character varying(32);
   ALTER TABLE public.typepersonnemorale
   ADD COLUMN csv_id character varying(32);
   -- Table: type_anomalie

-- DROP TABLE type_anomalie;

CREATE TABLE type_anomalie
(
  id_type_anomalie bigserial NOT NULL,
  valeur character varying(32),
  csv_id character varying(32),
  CONSTRAINT pk_type_anomalie PRIMARY KEY (id_type_anomalie)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE type_anomalie
  OWNER TO postgres;
  
  CREATE TABLE anomalie
(
  idanomalie bigserial NOT NULL,
  id_type_anomalie bigint,
  description character varying(1024),
  resolu boolean,
  csv_iddemande character varying(32),
  date_anomalie date,
  csv_id character varying(32),
  csv_id_type_anomalie character varying(32),
  CONSTRAINT pk_anomalie PRIMARY KEY (idanomalie)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE anomalie
  OWNER TO postgres;
-- Sequence: iddemande_seq

-- DROP SEQUENCE iddemande_seq;

CREATE SEQUENCE iddemande_sans_geom_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 5241
  CACHE 1;
ALTER TABLE iddemande_seq
  OWNER TO postgres;

-- Table: demande

-- DROP TABLE demande;

CREATE TABLE demande_sans_geom
(
  iddemande integer NOT NULL DEFAULT nextval('iddemande_seq'::regclass),
  id integer,
  numdemande character varying(1000),
  nomdemandeur character varying(100),
  surface numeric,
  parcelle character varying(5),
  etat_cf integer,
  geom geometry,
  gid integer NOT NULL DEFAULT 0,
  datedemande date,
  datereconnaissance date,
  region character varying(250),
  district character varying(250),
  commune character varying(250),
  fokontany character varying(250),
  titre character(50),
  idfokontany integer,
  idcommune integer,
  idrejet integer,
  cout real,
  consistance character varying(250),
  idprojet integer,
  numdemandepaps character varying(250),
  datedecision date,
  csv_id character varying(32),
  code_parcelle character varying(32),
  CONSTRAINT demande_sans_geom_pkey PRIMARY KEY (iddemande)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE demande_sans_geom
   ADD COLUMN categorie character varying(32);
ALTER TABLE demande
  OWNER TO postgres;
  
  INSERT INTO spatial_ref_sys(srid,auth_name,auth_srid,srtext,proj4text)
VALUES(98751,'fiplof', 98751, 'PROJCS["laborde",GEOGCS["GCS_Tananarive_1925",DATUM["D_Tananarive_1925",SPHEROID["International_1924",6378388.0,297.0]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Hotine_Oblique_Mercator_Azimuth_Center"],PARAMETER["False_Easting",400000.0],PARAMETER["False_Northing",800000.0],PARAMETER["Scale_Factor",0.9995],PARAMETER["Azimuth",18.9],PARAMETER["Longitude_Of_Center",46.437229166666],PARAMETER["Latitude_Of_Center",-18.9],UNIT["Meter",1.0]]', '+proj=omerc +lat_0=-18.9 +lonc=44.10000000000001 +alpha=18.9 +k=0.9995000000000001 +x_0=400000 +y_0=800000 +gamma=18.9 +ellps=intl +towgs84=-189,-242,-91,0,0,0,0 +pm=paris +units=m +no_defs ');

 ALTER TABLE public.personne
  ADD CONSTRAINT uk_csv_pers UNIQUE (csv_id);
  
  ALTER TABLE public.region
  ADD CONSTRAINT uk_csv_reg UNIQUE (csv_id);
  
  ALTER TABLE public.district
  ADD CONSTRAINT uk_csv_dist UNIQUE (csv_id);
  
  ALTER TABLE public.commune
  ADD CONSTRAINT uk_csv_commu UNIQUE (csv_id);
  
  ALTER TABLE public.fokontany
  ADD CONSTRAINT uk_csv_foko UNIQUE (csv_id);
  
  ALTER TABLE public.hameau
  ADD CONSTRAINT uk_csv_hame UNIQUE (csv_id);
  
  ALTER TABLE public.parcelle_d
  ADD CONSTRAINT uk_csv_parcd UNIQUE (csv_id);
  
  ALTER TABLE public.demande
  ADD CONSTRAINT uk_csv_dema UNIQUE (csv_id);
  
  ALTER TABLE public.typepersonnemorale
  ADD CONSTRAINT uk_csv_typersonnemorale UNIQUE (csv_id);
  
  ALTER TABLE public.personnemorale
  ADD CONSTRAINT uk_csv_personnemorale UNIQUE (csv_id);
  
  ALTER TABLE public.type_anomalie
  ADD CONSTRAINT uk_csv_typeano UNIQUE (csv_id);
  
  ALTER TABLE public.anomalie
  ADD CONSTRAINT uk_csv_anomalie UNIQUE (csv_id);
  
  ALTER TABLE public.avoir_demande
  ADD CONSTRAINT uk_csv_avd UNIQUE (csv_id);
  
  ALTER TABLE public.personnemoraleparcelle
  ADD CONSTRAINT uk_csv_persmorparc UNIQUE (csv_id);
  ALTER TABLE public.demande_sans_geom
  ADD CONSTRAINT uk_csv_demande_sans UNIQUE (csv_id);
  

ALTER TABLE parcelle_d
   ADD COLUMN observation character varying(64);
   
ALTER TABLE parcelle_d
   ADD COLUMN code_parcelle_en_doublon character varying(64);
   
ALTER TABLE parcelle_d
   ADD COLUMN editer_en_cf boolean;
   
ALTER TABLE demande
   ADD COLUMN opposition boolean;
   
ALTER TABLE demande
   ADD COLUMN planche_plof character varying(32);
   
ALTER TABLE demande
   ADD COLUMN charges character varying(128);
   
ALTER TABLE demande_sans_geom
   ADD COLUMN opposition boolean;
   
ALTER TABLE demande_sans_geom
   ADD COLUMN planche_plof character varying(32);
   
ALTER TABLE demande_sans_geom
   ADD COLUMN charges character varying(128);
   
-- 2022-07-03
ALTER TABLE public.personne
    ADD COLUMN rcin_personne character varying(256) COLLATE pg_catalog."default";

ALTER TABLE public.personnemorale
    ADD COLUMN rcin_pm character varying(256);
ALTER TABLE public.personnemorale
    ADD COLUMN mandataire character varying(256);
ALTER TABLE public.personnemorale
    ADD COLUMN type_declarant character varying(256);
	
-- 2022-07-07
ALTER TABLE public.demande ADD COLUMN numdecision character varying(50);

-- 2022-08-03

ALTER TABLE parcelle_d
  ADD CONSTRAINT geometry_valid_check CHECK (st_isvalid(geom));
  
-- 2022-08-05
ALTER TABLE demande
  ADD CONSTRAINT uk_demande UNIQUE(numdemande);
  
 -- 2022-08-17
 ALTER TABLE public.certificat
   ADD COLUMN idhameau bigint;
   
ALTER TABLE public.limitesparcelle
   ALTER COLUMN description TYPE character varying(1024);
   
ALTER TABLE public.consistance
   ALTER COLUMN libelleconsistance TYPE character varying(1024);
ALTER TABLE public.consistance
   ALTER COLUMN parcelleoubatiment TYPE character(1024);
   
-- 2022-08-18
ALTER TABLE public.certificat
    ADD COLUMN code_hameau character varying(256) COLLATE pg_catalog."default";
	
ALTER TABLE public.demande
    ALTER COLUMN consistance TYPE character varying(1024) COLLATE pg_catalog."default";

ALTER TABLE public.demande
    ALTER COLUMN nomdemandeur TYPE character varying(1024) COLLATE pg_catalog."default";
	
ALTER TABLE public.hameau
   ALTER COLUMN codehameau TYPE character varying(64);
   
-- 2022-08-23
ALTER TABLE personne ADD ogr_id character varying (32);

-- 2022-10-03
ALTER TABLE IF EXISTS public.demande
    ADD CONSTRAINT uk_gid UNIQUE (gid);

COMMENT ON CONSTRAINT uk_gid ON public.demande
    IS 'unique gid from parcelle_d';
	
-- 2022-10-25
ALTER TABLE public.demande
    ALTER COLUMN nomdemandeur TYPE character varying(1024) COLLATE pg_catalog."default";
	
ALTER TABLE public.parcelle_d
    ALTER COLUMN nomdemandeur TYPE character varying(1024) COLLATE pg_catalog."default";
	
-- 2022-11-13
ALTER TABLE public.demande
    ADD COLUMN  debut_affichage date;


ALTER TABLE public.demande
    ADD COLUMN  fin_affichage date;
	
-- 2022-11-16
ALTER TABLE IF EXISTS public.parcelle_d
    ADD CONSTRAINT uk_code_parcelle UNIQUE (codeparcelle);
	
-- 2022-12-17

-- 2022-12-18
ALTER TABLE public.personne
    ADD COLUMN handicap boolean DEFAULT False;

ALTER TABLE public.personne
    ADD COLUMN niveau_education text;

ALTER TABLE public.personne
    ADD COLUMN possede_emploi boolean DEFAULT True;

ALTER TABLE public.personne
    ADD COLUMN migrant boolean DEFAULT False;

ALTER TABLE public.personne
    ADD COLUMN date_arrivee date;
	
	
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
	
-- 2023-01-03
ALTER TABLE public.district
    ADD CONSTRAINT fk_region FOREIGN KEY (idregion)
    REFERENCES public.region (idregion) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;
CREATE INDEX  fki_fk_region
    ON public.district(idregion);
	
-- 2023-02-07
ALTER TABLE public.demande
   ADD COLUMN numero_demande_lrsys character varying(128);
   
-- 2023-02-25
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

-- 2023-03-01
ALTER TABLE public.fokontany
  ADD CONSTRAINT uk_code_fkt_idcom UNIQUE (codefokontany, idcommune);
  
ALTER TABLE public.hameau
  ADD CONSTRAINT uk_codeham_idfkt UNIQUE (codehameau, idfokontany);
  
-- 2023-03-02
   
ALTER TABLE avoir_demande DROP CONSTRAINT pk_avoir_demande;

ALTER TABLE avoir_demande
  ADD CONSTRAINT pk_avoir_demande PRIMARY KEY(idpersonne, idparcelle);
  
ALTER TABLE avoir_demande
   ALTER COLUMN iddemande DROP NOT NULL;
   
ALTER TABLE parcelle_d
   ADD COLUMN categorie character varying(128);
ALTER TABLE parcelle_d
   ALTER COLUMN consistance TYPE character varying(128);
   
ALTER TABLE parcelle_d
   ALTER COLUMN region TYPE character varying(128);
   
ALTER TABLE parcelle_d
   ALTER COLUMN commune TYPE character varying(128);
   
ALTER TABLE parcelle_d
   ALTER COLUMN fkt TYPE character varying(128);


-- 2023-03-03
ALTER TABLE demande
  ADD CONSTRAINT uk_codeparcelle UNIQUE (code_parcelle);
  
-- 2023-03-04
ALTER TABLE personne DROP COLUMN IF EXISTS cin_recto;
ALTER TABLE personne DROP COLUMN IF EXISTS cin_verso;
ALTER TABLE personne DROP COLUMN IF EXISTS signature;
ALTER TABLE personne DROP COLUMN IF EXISTS empreinte_d;
ALTER TABLE personne DROP COLUMN IF EXISTS empreinte_g;

CREATE TABLE public.blob_personne
(
   idblob bigserial, 
   idpersonne bigint, 
   cin_recto bytea, 
   cin_verso bytea, 
   signature bytea, 
   empreinte_d bytea, 
   empreinte_g bytea, 
   CONSTRAINT pk_blob_personne PRIMARY KEY (idblob), 
   CONSTRAINT fk_blob_personne FOREIGN KEY (idpersonne) REFERENCES personne (idpersonne) ON UPDATE NO ACTION ON DELETE NO ACTION
) 
WITH (
  OIDS = FALSE
)
;
ALTER TABLE public.blob_personne
  OWNER TO postgres;
  
-- 2023-03-05
DROP VIEW vw_demande;

CREATE OR REPLACE VIEW vw_demande AS 
 SELECT p.gid,
    p.geom,
    COALESCE(p.numdemande, p.codeparcelle) AS numdemande,
    d.idcommune
   FROM demande d
     RIGHT JOIN parcelle_d p ON p.gid = d.gid
  WHERE p.estfiscalite IS NULL OR p.estfiscalite = 0 OR p.conversion = 1;

ALTER TABLE vw_demande
  OWNER TO postgres;
  
ALTER TABLE blob_personne
  ADD CONSTRAINT uk_idpersonne UNIQUE (idpersonne);
  
ALTER TABLE parcelle_d
   ALTER COLUMN ref_import TYPE character varying(64);
   
-- 2023-03-19
ALTER TABLE blob_personne
  ADD COLUMN cin_recto_name character varying(128);
ALTER TABLE blob_personne
  ADD COLUMN cin_recto_type character varying(10);
ALTER TABLE blob_personne
  ADD COLUMN cin_verso_name character varying(128);
ALTER TABLE blob_personne
  ADD COLUMN cin_verso_type character varying(10);
ALTER TABLE blob_personne
  ADD COLUMN signature_name character varying(128);
ALTER TABLE blob_personne
  ADD COLUMN signature_type character varying(10);
ALTER TABLE blob_personne
  ADD COLUMN empreinte_d_name character varying(128);
ALTER TABLE blob_personne
  ADD COLUMN empreinte_d_type character varying(10);
ALTER TABLE blob_personne
  ADD COLUMN empreinte_g_name character varying(128);
ALTER TABLE blob_personne
  ADD COLUMN empreinte_g_type character varying(10);
  
-- 2023-03-21
ALTER TABLE blob_personne
  ADD COLUMN photo_demandeur BYTEA;
ALTER TABLE blob_personne
  ADD COLUMN photo_demandeur_type character varying(10);
  

CREATE TABLE type_document(
   id_type SERIAL,
   libelle_type CHARACTER VARYING(128) ,
   PRIMARY KEY(id_type)
);


CREATE TABLE document(
   id_document BIGSERIAL,
   photo_document BYTEA,
   extension_document CHARACTER VARYING(10) ,
   num_page INTEGER,
   observation TEXT,
   id_type SMALLINT,
   iddemande BIGINT,
   PRIMARY KEY(id_document),
   FOREIGN KEY(id_type) REFERENCES type_document(id_type),
   FOREIGN KEY(iddemande) REFERENCES demande(iddemande)
);

-- 2023-03-22
ALTER TABLE parcelle_d
   ALTER COLUMN district TYPE character varying(128);
   
-- 2023-06-15
ALTER TABLE public.demande
   ADD COLUMN lieudit character varying(256);
ALTER TABLE public.demande
   ADD COLUMN collecteur_demande character varying(512);
   
ALTER TABLE public.demande_crl ADD COLUMN titulaire boolean;

INSERT INTO role_crl (id_role, libelle_role) VALUES (4, 'Ray aman-dReny 1');
INSERT INTO role_crl (id_role, libelle_role) VALUES (5, 'Ray aman-dReny 2');
INSERT INTO role_crl (id_role, libelle_role) VALUES (6, 'Ray aman-dReny 3');
INSERT INTO role_crl (id_role, libelle_role) VALUES (3, 'Ny Solotenan ny Fokontany');
INSERT INTO role_crl (id_role, libelle_role) VALUES (2, 'Ny Solotenan ny Kaominina');
INSERT INTO role_crl (id_role, libelle_role) VALUES (7, 'Ny Mpiasan ny Birao Ifoton ny Fananan-tany');

-- 2023-06-19
ALTER TABLE public.demande
   ADD COLUMN duree_occupation smallint;
   
ALTER TABLE public.demande
   ADD COLUMN origine text;
   
ALTER TABLE public.personne
   ADD COLUMN conjoint character varying(256);
   
-- 2023-06-20
CREATE TABLE public.blob_voisin
(
   idpoint bigint, 
   idparcelle bigint, 
   voisin character varying(256), 
   signature_fic bytea, 
   signature_name character varying(128), 
   signature_ext character varying(10), 
   CONSTRAINT pk_blob_voisin PRIMARY KEY (idpoint, idparcelle, voisin)
) 
WITH (
  OIDS = FALSE
)
;

-- 2023-06-21
ALTER TABLE public.autrecharge
   ADD COLUMN idparcelle bigint;
   
ALTER TABLE public.demande
   ADD COLUMN avis_crl boolean;

-- 2023-07-01
ALTER TABLE public.demande
   ADD COLUMN texte_crl text;
   
ALTER TABLE public.demande_crl
   ADD COLUMN president boolean DEFAULT FALSE;
   
-- 2023-07-03
ALTER TABLE public.demande DROP CONSTRAINT uk_codeparcelle;

ALTER TABLE public.demande
  ADD CONSTRAINT uk_codeparcelle UNIQUE(code_parcelle, idcommune);
  
ALTER TABLE public.parcelle_d DROP CONSTRAINT uk_code_parcelle;

ALTER TABLE public.parcelle_d
  ADD CONSTRAINT uk_code_parcelle UNIQUE(codeparcelle, id_commune);
  
-- 2023-07-04
ALTER TABLE public.parcelle_d DROP CONSTRAINT IF EXISTS uk_geom;

-- 2023-07-22
DROP VIEW IF EXISTS public.vw_shape_certificat;
CREATE OR REPLACE VIEW public.vw_shape_certificat AS 
 SELECT p.geom,
    c.numerocertificat,
    c.numerodemande,
    p.codeparcelle,
    pers.nompersonne AS nom_prop,
    pers.prenompersonne AS prenom_prop,
    pers.numcipersonne,
    pers.datecipersonne,
    pers.lieucipersonne,
    pers.numactenaissancepersonne,
    pers.dateactenaissancepersonne,
    pers.lieuactenaissancepersonne,
    p.surface,
    d.datedemande,
    d.datedecision,
    d.numdecision,
    d.debut_affichage,
    d.fin_affichage,
    d.datereconnaissance,
    COALESCE(d.region, ''::character varying) AS region,
    d.district,
    com.nomcommune,
    fkt.nomfokontany,
    COALESCE(h.nomhameau, ''::character varying) AS nomhameau,
    d.categorie,
    d.consistance
   FROM certificat c
     JOIN parcelle_d p ON p.idcertificat = c.idcertificat
     JOIN demande d ON d.gid = p.gid
     JOIN proprietaireparcelle pp ON p.gid = pp.idparcelle
     JOIN personne pers ON pp.idpersonne = pers.idpersonne
     JOIN commune com ON com.idcommune = d.idcommune
     LEFT JOIN fokontany fkt ON fkt.idfokontany = d.idfokontany
     LEFT JOIN hameau h ON h.idhameau = p.idhameau;

ALTER TABLE public.vw_shape_certificat
  OWNER TO postgres;
  
DROP  VIEW IF EXISTS public.vw_shape_demande;

CREATE OR REPLACE VIEW public.vw_shape_demande AS 
 WITH q1 AS (
         SELECT demande_1.iddemande,
            string_agg((((((((((((((((((((((((((((((concat(p_1.nompersonne, ' ', COALESCE(p_1.prenompersonne, ''::character varying)) || '<FIELD>'::text) || p_1.sexepersonne::text) || '<FIELD>'::text) || COALESCE(p_1.datenaissancepersonne, '1000-01-01'::date)) || '<FIELD>'::text) || COALESCE(p_1.nevers::integer, 0)) || '<FIELD>'::text) || COALESCE(p_1.numcipersonne, ''::character varying)::text) || '<FIELD>'::text) || COALESCE(p_1.numactenaissancepersonne, ''::character varying)::text) || '<FIELD>'::text) || COALESCE(p_1.datecipersonne, '1000-01-01'::date)) || '<FIELD>'::text) || COALESCE(p_1.lieucipersonne, ''::character varying)::text) || '<FIELD>'::text) || COALESCE(p_1.dateactenaissancepersonne, '1000-01-01'::date)) || '<FIELD>'::text) || COALESCE(p_1.lieuactenaissancepersonne, ''::character varying)::text) || '<FIELD>'::text) || COALESCE(p_1.adressepersonne, ''::character varying)::text) || '<FIELD>'::text) || COALESCE(p_1.nompere, ''::character varying)::text) || '<FIELD>'::text) || COALESCE(p_1.nommere, ''::character varying)::text) || '<FIELD>'::text) || COALESCE(p_1.conjoint, ''::character varying)::text) || '<FIELD>'::text) || p_1.idpersonne) || '<FIELD>'::text) || COALESCE(a.representant, false), '<ROW>'::text) AS demandeurs
           FROM demande demande_1
             LEFT JOIN avoir_demande a ON a.iddemande = demande_1.iddemande
             LEFT JOIN personne p_1 ON p_1.idpersonne = a.idpersonne
          GROUP BY demande_1.iddemande
        )
 SELECT p.geom,
    COALESCE(demande.code_parcelle, ''::character varying) AS c_parcelle,
    demande.numdemande,
    demande.datedemande,
    p.surface,
    COALESCE(demande.region) AS "coalesce",
    demande.district,
    com.nomcommune,
    fkt.nomfokontany,
    COALESCE(demande.lieudit, ''::character varying) AS lieudit,
    demande.categorie,
    demande.consistance,
    q1.demandeurs,
    COALESCE(h.codehameau, ''::character varying) AS codehameau,
    COALESCE(h.nomhameau, ''::character varying) AS nomhameau
   FROM demande
     JOIN q1 ON q1.iddemande = demande.iddemande
     JOIN parcelle_d p ON p.gid = demande.gid
     JOIN commune com ON com.idcommune = demande.idcommune
     LEFT JOIN fokontany fkt ON fkt.idfokontany = demande.idfokontany
     LEFT JOIN hameau h ON h.idhameau = p.idhameau
  WHERE demande.numdemande IS NOT NULL;
  
  
ALTER TABLE public.vw_shape_demande
  OWNER TO postgres;
  
-- 2022-09-03
ALTER TABLE public.autrecharge
   ALTER COLUMN descriptioncharge TYPE text;
   
-- 2023-09-11
UPDATE public.consistance SET libelleconsistance = parcelleoubatiment WHERE TRIM(parcelleoubatiment) = 'TANIMBARY' OR TRIM(parcelleoubatiment) = 'ALA' OR TRIM(parcelleoubatiment) = 'TANIMBOLY';