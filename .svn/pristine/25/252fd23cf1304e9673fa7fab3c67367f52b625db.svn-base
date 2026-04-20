--
-- PostgreSQL database dump
--

-- Dumped from database version 9.3.5
-- Dumped by pg_dump version 9.3.5
-- Started on 2024-12-04 10:47:53

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 6 (class 2615 OID 1682064)
-- Name: tiger; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA tiger;


ALTER SCHEMA tiger OWNER TO postgres;

--
-- TOC entry 7 (class 2615 OID 1682065)
-- Name: tiger_data; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA tiger_data;


ALTER SCHEMA tiger_data OWNER TO postgres;

--
-- TOC entry 8 (class 2615 OID 1682066)
-- Name: topology; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA topology;


ALTER SCHEMA topology OWNER TO postgres;

--
-- TOC entry 378 (class 3079 OID 11750)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 5047 (class 0 OID 0)
-- Dependencies: 378
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- TOC entry 383 (class 3079 OID 1682067)
-- Name: address_standardizer; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS address_standardizer WITH SCHEMA public;


--
-- TOC entry 5048 (class 0 OID 0)
-- Dependencies: 383
-- Name: EXTENSION address_standardizer; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION address_standardizer IS 'Used to parse an address into constituent elements. Generally used to support geocoding address normalization step.';


--
-- TOC entry 382 (class 3079 OID 1682074)
-- Name: fuzzystrmatch; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS fuzzystrmatch WITH SCHEMA public;


--
-- TOC entry 5049 (class 0 OID 0)
-- Dependencies: 382
-- Name: EXTENSION fuzzystrmatch; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION fuzzystrmatch IS 'determine similarities and distance between strings';


--
-- TOC entry 381 (class 3079 OID 1682089)
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- TOC entry 5050 (class 0 OID 0)
-- Dependencies: 381
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';


--
-- TOC entry 380 (class 3079 OID 1683454)
-- Name: pgrouting; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS pgrouting WITH SCHEMA public;


--
-- TOC entry 5051 (class 0 OID 0)
-- Dependencies: 380
-- Name: EXTENSION pgrouting; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgrouting IS 'pgRouting Extension';


--
-- TOC entry 379 (class 3079 OID 1683608)
-- Name: postgis_topology; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS postgis_topology WITH SCHEMA topology;


--
-- TOC entry 5052 (class 0 OID 0)
-- Dependencies: 379
-- Name: EXTENSION postgis_topology; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis_topology IS 'PostGIS topology spatial types and functions';


SET search_path = public, pg_catalog;

--
-- TOC entry 1736 (class 1255 OID 1686219)
-- Name: update_datemaj(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION update_datemaj() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.datemaj = CURRENT_TIMESTAMP;  -- Définit la valeur de datemaj à l'heure actuelle lors d'une mise à jour
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.update_datemaj() OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 199 (class 1259 OID 1683747)
-- Name: acces; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE acces (
    id bigint NOT NULL,
    nom character varying(64),
    libelle character varying(128),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.acces OWNER TO postgres;

--
-- TOC entry 200 (class 1259 OID 1683750)
-- Name: acces_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE acces_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.acces_id_seq OWNER TO postgres;

--
-- TOC entry 5053 (class 0 OID 0)
-- Dependencies: 200
-- Name: acces_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE acces_id_seq OWNED BY acces.id;


--
-- TOC entry 201 (class 1259 OID 1683752)
-- Name: actedeces; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE actedeces (
    idactedeces bigint NOT NULL,
    numeroactedeces character(32),
    dateactedeces date,
    numeroactenotoriete character(32),
    dateactenotoriete date,
    idprojet integer,
    lance integer DEFAULT 0,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.actedeces OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 1683756)
-- Name: actedeces_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE actedeces_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.actedeces_id_seq OWNER TO postgres;

--
-- TOC entry 5054 (class 0 OID 0)
-- Dependencies: 202
-- Name: actedeces_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE actedeces_id_seq OWNED BY actedeces.idactedeces;


--
-- TOC entry 203 (class 1259 OID 1683758)
-- Name: actedecessubsequente; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE actedecessubsequente (
    idactedeces bigint NOT NULL,
    idoperationsubsequente bigint NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.actedecessubsequente OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 1683761)
-- Name: actedj_gid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE actedj_gid_seq
    START WITH 1569
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.actedj_gid_seq OWNER TO postgres;

--
-- TOC entry 205 (class 1259 OID 1683763)
-- Name: actedejalance; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE actedejalance (
    id bigint DEFAULT nextval('actedj_gid_seq'::regclass) NOT NULL,
    idacte bigint,
    typeacte bigint,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.actedejalance OWNER TO postgres;

--
-- TOC entry 206 (class 1259 OID 1683767)
-- Name: acteprive; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE acteprive (
    idacteprive bigint NOT NULL,
    numeroacteprive character(32),
    dateenregistrement date,
    datelegalisationsignature date,
    nombreoperation bigint,
    valeurtransaction real,
    idprojet integer,
    lance integer DEFAULT 0,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.acteprive OWNER TO postgres;

--
-- TOC entry 207 (class 1259 OID 1683771)
-- Name: acteprive_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE acteprive_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.acteprive_id_seq OWNER TO postgres;

--
-- TOC entry 5055 (class 0 OID 0)
-- Dependencies: 207
-- Name: acteprive_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE acteprive_id_seq OWNED BY acteprive.idacteprive;


--
-- TOC entry 208 (class 1259 OID 1683773)
-- Name: acteprivesubsequente; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE acteprivesubsequente (
    idacteprive bigint NOT NULL,
    idoperationsubsequente bigint NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.acteprivesubsequente OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 1683776)
-- Name: actepublic; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE actepublic (
    idactepublic bigint NOT NULL,
    dateenregistrement date,
    nomofficierpublic text,
    nombreoperation bigint,
    idprojet integer DEFAULT 0 NOT NULL,
    numeroactepublic integer,
    valeurtransaction real,
    lance bigint DEFAULT 0,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.actepublic OWNER TO postgres;

--
-- TOC entry 210 (class 1259 OID 1683784)
-- Name: actepublic_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE actepublic_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.actepublic_id_seq OWNER TO postgres;

--
-- TOC entry 5056 (class 0 OID 0)
-- Dependencies: 210
-- Name: actepublic_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE actepublic_id_seq OWNED BY actepublic.idactepublic;


--
-- TOC entry 211 (class 1259 OID 1683786)
-- Name: actepublicsubsequente; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE actepublicsubsequente (
    idactepublic bigint NOT NULL,
    idoperationsubsequente bigint NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.actepublicsubsequente OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 1683789)
-- Name: aireastatutspecifique; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE aireastatutspecifique (
    originecontour text,
    nom character(120),
    type character(120),
    shape_length double precision,
    shape_area double precision,
    idaireastatutspecifique bigint NOT NULL,
    geom geometry,
    observation character varying(300),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.aireastatutspecifique OWNER TO postgres;

--
-- TOC entry 213 (class 1259 OID 1683795)
-- Name: aireastatutspecifique_idaireastatutspecifique_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE aireastatutspecifique_idaireastatutspecifique_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.aireastatutspecifique_idaireastatutspecifique_seq OWNER TO postgres;

--
-- TOC entry 5057 (class 0 OID 0)
-- Dependencies: 213
-- Name: aireastatutspecifique_idaireastatutspecifique_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE aireastatutspecifique_idaireastatutspecifique_seq OWNED BY aireastatutspecifique.idaireastatutspecifique;


--
-- TOC entry 214 (class 1259 OID 1683797)
-- Name: anomalie; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE anomalie (
    idanomalie bigint NOT NULL,
    id_type_anomalie bigint,
    description character varying(1024),
    resolu boolean,
    csv_iddemande character varying(32),
    date_anomalie date,
    csv_id character varying(32),
    csv_id_type_anomalie character varying(32),
    datemaj timestamp without time zone DEFAULT now(),
    uuid_lr_sys character varying(90),
    iddemande bigint
);


ALTER TABLE public.anomalie OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 1683803)
-- Name: anomalie_idanomalie_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE anomalie_idanomalie_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.anomalie_idanomalie_seq OWNER TO postgres;

--
-- TOC entry 5058 (class 0 OID 0)
-- Dependencies: 215
-- Name: anomalie_idanomalie_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE anomalie_idanomalie_seq OWNED BY anomalie.idanomalie;


--
-- TOC entry 216 (class 1259 OID 1683805)
-- Name: autrecharge; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE autrecharge (
    type character(32),
    descriptioncharge text,
    dateinscriptionregistre date,
    idcharge bigint NOT NULL,
    idparcelle bigint,
    datemaj timestamp without time zone DEFAULT now(),
    uuid_lr_sys character varying(90)
);


ALTER TABLE public.autrecharge OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 1683811)
-- Name: autrecharge_idcharge_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE autrecharge_idcharge_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.autrecharge_idcharge_seq OWNER TO postgres;

--
-- TOC entry 5059 (class 0 OID 0)
-- Dependencies: 217
-- Name: autrecharge_idcharge_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE autrecharge_idcharge_seq OWNED BY autrecharge.idcharge;


--
-- TOC entry 218 (class 1259 OID 1683813)
-- Name: autrechargesparcelle_d; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE autrechargesparcelle_d (
    idcharge bigint NOT NULL,
    idparcelle bigint NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.autrechargesparcelle_d OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 1683816)
-- Name: avoir_demande; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE avoir_demande (
    idpersonne bigint NOT NULL,
    iddemande bigint,
    idparcelle bigint NOT NULL,
    representant boolean,
    csv_id character varying(32),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.avoir_demande OWNER TO postgres;

--
-- TOC entry 5060 (class 0 OID 0)
-- Dependencies: 219
-- Name: TABLE avoir_demande; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE avoir_demande IS 'Table liant Personne, demande et parcelle_d';


--
-- TOC entry 220 (class 1259 OID 1683819)
-- Name: avoir_dmd; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE avoir_dmd (
    iddemandeur integer NOT NULL,
    iddemande integer NOT NULL,
    gid integer,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.avoir_dmd OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 1683822)
-- Name: avoirconjoint; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE avoirconjoint (
    idconjoint_a bigint NOT NULL,
    idconjoint_b bigint NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.avoirconjoint OWNER TO postgres;

--
-- TOC entry 5061 (class 0 OID 0)
-- Dependencies: 221
-- Name: TABLE avoirconjoint; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE avoirconjoint IS 'Table contenant l''id de la personne marie et celui de sa femme';


--
-- TOC entry 222 (class 1259 OID 1683825)
-- Name: batiment; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE batiment (
    codebatiment character varying(10) NOT NULL,
    idparcelle bigint,
    idconsistance bigint,
    surfacebatiment real,
    nbpiecebatiment integer,
    locationbatiment boolean,
    idcategorie bigint,
    fi_forfait character varying(20),
    idclasse bigint,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.batiment OWNER TO postgres;

--
-- TOC entry 5062 (class 0 OID 0)
-- Dependencies: 222
-- Name: COLUMN batiment.fi_forfait; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN batiment.fi_forfait IS 'Valeur type calcul impôt:soit surface,soit classe, soit valeur_locative';


--
-- TOC entry 5063 (class 0 OID 0)
-- Dependencies: 222
-- Name: COLUMN batiment.idclasse; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN batiment.idclasse IS 'id classe batiment';


--
-- TOC entry 223 (class 1259 OID 1683828)
-- Name: beneficiaire; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE beneficiaire (
    idbeneficiaire bigint NOT NULL,
    libellebeneficiaire text,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.beneficiaire OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 1683834)
-- Name: beneficiaire_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE beneficiaire_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.beneficiaire_id_seq OWNER TO postgres;

--
-- TOC entry 5064 (class 0 OID 0)
-- Dependencies: 224
-- Name: beneficiaire_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE beneficiaire_id_seq OWNED BY beneficiaire.idbeneficiaire;


--
-- TOC entry 225 (class 1259 OID 1683836)
-- Name: blob_history; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE blob_history (
    idpersonne bigint,
    idutilisateur bigint,
    old_file bytea,
    new_file bytea,
    old_file_type character varying(10),
    new_file_type character varying(10),
    nature character varying(128),
    datemodification date,
    old_file_name character varying(100),
    new_file_name character varying(100),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.blob_history OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 1683842)
-- Name: blob_personne; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE blob_personne (
    idblob bigint NOT NULL,
    idpersonne bigint,
    cin_recto bytea,
    cin_verso bytea,
    signature bytea,
    empreinte_d bytea,
    empreinte_g bytea,
    cin_recto_name character varying(128),
    cin_recto_type character varying(10),
    cin_verso_name character varying(128),
    cin_verso_type character varying(10),
    signature_name character varying(128),
    signature_type character varying(10),
    empreinte_d_name character varying(128),
    empreinte_d_type character varying(10),
    empreinte_g_name character varying(128),
    empreinte_g_type character varying(10),
    photo_demandeur bytea,
    photo_demandeur_type character varying(10),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.blob_personne OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 1683848)
-- Name: blob_personne_idblob_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE blob_personne_idblob_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.blob_personne_idblob_seq OWNER TO postgres;

--
-- TOC entry 5065 (class 0 OID 0)
-- Dependencies: 227
-- Name: blob_personne_idblob_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE blob_personne_idblob_seq OWNED BY blob_personne.idblob;


--
-- TOC entry 228 (class 1259 OID 1683850)
-- Name: blob_voisin; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE blob_voisin (
    idpoint bigint NOT NULL,
    idparcelle bigint NOT NULL,
    voisin character varying(256) NOT NULL,
    signature_fic bytea,
    signature_name character varying(128),
    signature_ext character varying(10),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.blob_voisin OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 1683856)
-- Name: cadastre; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE cadastre (
    gid bigint NOT NULL,
    nom_section character varying(100),
    section character varying(10),
    parcelle character varying(10),
    nom_plan character varying(50),
    geom geometry,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.cadastre OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 1683862)
-- Name: cadastre_gid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE cadastre_gid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cadastre_gid_seq OWNER TO postgres;

--
-- TOC entry 5066 (class 0 OID 0)
-- Dependencies: 230
-- Name: cadastre_gid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE cadastre_gid_seq OWNED BY cadastre.gid;


--
-- TOC entry 231 (class 1259 OID 1683864)
-- Name: categorie; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE categorie (
    idcategorie bigint NOT NULL,
    libellecategorie character(32) NOT NULL,
    typeimposition character(32) NOT NULL,
    v_surface integer DEFAULT 0 NOT NULL,
    valeur_location_ha integer DEFAULT 0 NOT NULL,
    u_surface character varying(10),
    v_venale integer DEFAULT 0,
    u_venale character varying(10),
    taux real DEFAULT 1,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.categorie OWNER TO postgres;

--
-- TOC entry 5067 (class 0 OID 0)
-- Dependencies: 231
-- Name: COLUMN categorie.v_surface; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN categorie.v_surface IS 'valeur par surface';


--
-- TOC entry 5068 (class 0 OID 0)
-- Dependencies: 231
-- Name: COLUMN categorie.u_surface; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN categorie.u_surface IS 'unité surface';


--
-- TOC entry 5069 (class 0 OID 0)
-- Dependencies: 231
-- Name: COLUMN categorie.v_venale; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN categorie.v_venale IS 'valeur venale';


--
-- TOC entry 5070 (class 0 OID 0)
-- Dependencies: 231
-- Name: COLUMN categorie.taux; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN categorie.taux IS 'taux d''imposition par valeur venale';


--
-- TOC entry 232 (class 1259 OID 1683871)
-- Name: categorie_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE categorie_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.categorie_id_seq OWNER TO postgres;

--
-- TOC entry 5071 (class 0 OID 0)
-- Dependencies: 232
-- Name: categorie_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE categorie_id_seq OWNED BY categorie.idcategorie;


--
-- TOC entry 233 (class 1259 OID 1683873)
-- Name: categorieforfaitaire; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE categorieforfaitaire (
    idcategorie bigint NOT NULL,
    idforfaitaire bigint NOT NULL,
    descripiton text,
    valeurariary money,
    valeurlocationbatiment money,
    iftifpb character varying(5),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.categorieforfaitaire OWNER TO postgres;

--
-- TOC entry 234 (class 1259 OID 1683879)
-- Name: certificat; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE certificat (
    numerocertificat character(50),
    numerodemande character(50),
    datereconnaissance date,
    typecertificat character(50),
    datecreation date,
    dateedition date,
    datedelivrance date,
    memo text,
    idcertificat bigint NOT NULL,
    idfokontany bigint,
    idprojet bigint,
    isprint integer DEFAULT 0,
    idcommune bigint,
    idhameau bigint,
    code_hameau character varying(256),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.certificat OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 1683886)
-- Name: certificat_idcertificat_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE certificat_idcertificat_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.certificat_idcertificat_seq OWNER TO postgres;

--
-- TOC entry 5072 (class 0 OID 0)
-- Dependencies: 235
-- Name: certificat_idcertificat_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE certificat_idcertificat_seq OWNED BY certificat.idcertificat;


--
-- TOC entry 236 (class 1259 OID 1683888)
-- Name: classe; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE classe (
    idclasse bigint NOT NULL,
    libelleclasse character(32) NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.classe OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 1683891)
-- Name: classe_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE classe_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.classe_id_seq OWNER TO postgres;

--
-- TOC entry 5073 (class 0 OID 0)
-- Dependencies: 237
-- Name: classe_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE classe_id_seq OWNED BY classe.idclasse;


--
-- TOC entry 238 (class 1259 OID 1683893)
-- Name: classecategorieforfaitaire; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE classecategorieforfaitaire (
    idcategorie bigint NOT NULL,
    idclasse bigint NOT NULL,
    iftifpb character(5),
    valeurariary integer,
    debut integer,
    fin integer,
    unite character varying(10),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.classecategorieforfaitaire OWNER TO postgres;

--
-- TOC entry 5074 (class 0 OID 0)
-- Dependencies: 238
-- Name: COLUMN classecategorieforfaitaire.unite; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN classecategorieforfaitaire.unite IS 'unité classe forfaitaire';


--
-- TOC entry 239 (class 1259 OID 1683896)
-- Name: commune; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE commune (
    idcommune bigint NOT NULL,
    iddistrict bigint,
    codecommune character varying(10) NOT NULL,
    nomcommune character varying(50) NOT NULL,
    shapelength double precision,
    shapearea double precision,
    cptcertificat bigint DEFAULT 1,
    cptimport bigint DEFAULT 1,
    cptdemande bigint DEFAULT 1 NOT NULL,
    codeg integer,
    csv_id character varying(32),
    maire character varying(250),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.commune OWNER TO postgres;

--
-- TOC entry 240 (class 1259 OID 1683902)
-- Name: commune_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE commune_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.commune_id_seq OWNER TO postgres;

--
-- TOC entry 5075 (class 0 OID 0)
-- Dependencies: 240
-- Name: commune_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE commune_id_seq OWNED BY commune.idcommune;


--
-- TOC entry 241 (class 1259 OID 1683904)
-- Name: consistance; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE consistance (
    idconsistance bigint NOT NULL,
    libelleconsistance character varying(1024) NOT NULL,
    parcelleoubatiment character(1024) NOT NULL,
    valeurariary integer,
    valeurariary_ifpb integer,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.consistance OWNER TO postgres;

--
-- TOC entry 242 (class 1259 OID 1683910)
-- Name: consistance_batiment; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE consistance_batiment (
    id bigint NOT NULL,
    consistance character varying(80),
    mombamombanytany character varying(80),
    valeurariary integer DEFAULT 0,
    valeur_location integer DEFAULT 0,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.consistance_batiment OWNER TO postgres;

--
-- TOC entry 5076 (class 0 OID 0)
-- Dependencies: 242
-- Name: COLUMN consistance_batiment.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN consistance_batiment.id IS 'id ';


--
-- TOC entry 243 (class 1259 OID 1683915)
-- Name: consistance_batiment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE consistance_batiment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.consistance_batiment_id_seq OWNER TO postgres;

--
-- TOC entry 5077 (class 0 OID 0)
-- Dependencies: 243
-- Name: consistance_batiment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE consistance_batiment_id_seq OWNED BY consistance_batiment.id;


--
-- TOC entry 244 (class 1259 OID 1683917)
-- Name: consistance_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE consistance_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.consistance_id_seq OWNER TO postgres;

--
-- TOC entry 5078 (class 0 OID 0)
-- Dependencies: 244
-- Name: consistance_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE consistance_id_seq OWNED BY consistance.idconsistance;


--
-- TOC entry 245 (class 1259 OID 1683919)
-- Name: consistanceforfaitaire; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE consistanceforfaitaire (
    idconsistance bigint NOT NULL,
    idforfaitaire bigint NOT NULL,
    prix money,
    prixaveclocation money,
    iftifpb character(5),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.consistanceforfaitaire OWNER TO postgres;

--
-- TOC entry 246 (class 1259 OID 1683922)
-- Name: contribuable_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE contribuable_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.contribuable_id_seq OWNER TO postgres;

--
-- TOC entry 247 (class 1259 OID 1683924)
-- Name: contribuable; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE contribuable (
    idcontribuable integer DEFAULT nextval('contribuable_id_seq'::regclass) NOT NULL,
    nom character varying(250),
    datenaissance date,
    lieu character varying(250),
    cin character varying(250),
    hetratany real,
    hetratrano real,
    idfkt integer,
    datereglement date,
    prenom character varying(80),
    adresse character varying(100),
    datecin date,
    numactenaissance character varying(50),
    dateactenaissance date,
    lieuactenaissance character varying(80),
    sexe character varying(50),
    idcontribuableconsorts bigint,
    lieucin character varying(80),
    etatpaiement smallint,
    montantpayee money DEFAULT 0,
    nevers smallint,
    modecalcul smallint,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.contribuable OWNER TO postgres;

--
-- TOC entry 5079 (class 0 OID 0)
-- Dependencies: 247
-- Name: COLUMN contribuable.modecalcul; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN contribuable.modecalcul IS 'Valeur = 1 => calcul par surface
Valeur = 2 => calcul par consistance
Valeur = 3 => calcul par classe';


--
-- TOC entry 248 (class 1259 OID 1683932)
-- Name: contribuableconsorts; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE contribuableconsorts (
    idcontribuable bigint NOT NULL,
    idconsort bigint NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.contribuableconsorts OWNER TO postgres;

--
-- TOC entry 249 (class 1259 OID 1683935)
-- Name: contribuables_parcelle; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE contribuables_parcelle (
    idpersonne bigint NOT NULL,
    idparcelle bigint NOT NULL,
    contribuable boolean,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.contribuables_parcelle OWNER TO postgres;

--
-- TOC entry 250 (class 1259 OID 1683938)
-- Name: crd_gid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE crd_gid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.crd_gid_seq OWNER TO postgres;

--
-- TOC entry 377 (class 1259 OID 1686333)
-- Name: date_synchro; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE date_synchro (
    id_synchro integer NOT NULL,
    date_synchro timestamp without time zone DEFAULT now(),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.date_synchro OWNER TO postgres;

--
-- TOC entry 376 (class 1259 OID 1686331)
-- Name: date_synchro_id_synchro_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE date_synchro_id_synchro_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.date_synchro_id_synchro_seq OWNER TO postgres;

--
-- TOC entry 5080 (class 0 OID 0)
-- Dependencies: 376
-- Name: date_synchro_id_synchro_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE date_synchro_id_synchro_seq OWNED BY date_synchro.id_synchro;


--
-- TOC entry 251 (class 1259 OID 1683946)
-- Name: decisionsubsequente; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE decisionsubsequente (
    idoperationsubsequente bigint NOT NULL,
    iddecision bigint NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.decisionsubsequente OWNER TO postgres;

--
-- TOC entry 252 (class 1259 OID 1683949)
-- Name: demande; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE demande (
    iddemande integer NOT NULL,
    id integer,
    numdemande character varying(1000),
    nomdemandeur character varying(1024),
    surface numeric,
    parcelle character varying(5),
    etat_cf integer,
    geom geometry,
    gid integer DEFAULT 0 NOT NULL,
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
    consistance character varying(1024),
    idprojet integer,
    numdemandepaps character varying(250),
    datedecision date,
    csv_id character varying(32),
    code_parcelle character varying(32),
    categorie character varying,
    opposition boolean,
    planche_plof character varying(32),
    charges character varying(128),
    numdecision character varying(50),
    debut_affichage date,
    fin_affichage date,
    numero_demande_lrsys character varying(128),
    pvrl character varying(250),
    cqe boolean,
    date_cqe date,
    resp_cqe character varying(250),
    user_cqe bigint,
    lieudit character varying(256),
    collecteur_demande character varying(512),
    duree_occupation smallint,
    origine text,
    avis_crl boolean,
    texte_crl text,
    sous_reserve boolean,
    datemaj timestamp without time zone DEFAULT now(),
    num_guichet_foncier character varying(50),
    uuid_dossier_lr character varying(90)
);


ALTER TABLE public.demande OWNER TO postgres;

--
-- TOC entry 5081 (class 0 OID 0)
-- Dependencies: 252
-- Name: COLUMN demande.sous_reserve; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN demande.sous_reserve IS 'Vrai si decision crl sous reserve';


--
-- TOC entry 253 (class 1259 OID 1683956)
-- Name: demande_anomalie; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE demande_anomalie (
    iddemande bigint NOT NULL,
    idanomalie bigint NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.demande_anomalie OWNER TO postgres;

--
-- TOC entry 254 (class 1259 OID 1683959)
-- Name: demande_crl; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE demande_crl (
    idpersonne bigint NOT NULL,
    iddemande bigint NOT NULL,
    id_role smallint NOT NULL,
    rl boolean,
    affiche boolean,
    titulaire boolean,
    president boolean DEFAULT false,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.demande_crl OWNER TO postgres;

--
-- TOC entry 255 (class 1259 OID 1683963)
-- Name: iddemande_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE iddemande_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.iddemande_seq OWNER TO postgres;

--
-- TOC entry 5082 (class 0 OID 0)
-- Dependencies: 255
-- Name: iddemande_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE iddemande_seq OWNED BY demande.iddemande;


--
-- TOC entry 256 (class 1259 OID 1683965)
-- Name: demande_sans_geom; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE demande_sans_geom (
    iddemande integer DEFAULT nextval('iddemande_seq'::regclass) NOT NULL,
    id integer,
    numdemande character varying(1000),
    nomdemandeur character varying(100),
    surface numeric,
    parcelle character varying(5),
    etat_cf integer,
    geom geometry,
    gid integer DEFAULT 0 NOT NULL,
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
    categorie character varying(32),
    opposition boolean,
    planche_plof character varying(32),
    charges character varying(128),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.demande_sans_geom OWNER TO postgres;

--
-- TOC entry 257 (class 1259 OID 1683981)
-- Name: demandefn; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE demandefn (
    gid bigint NOT NULL,
    fn_fg character varying(25),
    demandeur character varying(100),
    sur_plan double precision,
    geom geometry,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.demandefn OWNER TO postgres;

--
-- TOC entry 258 (class 1259 OID 1683987)
-- Name: demandefn_gid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE demandefn_gid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.demandefn_gid_seq OWNER TO postgres;

--
-- TOC entry 5083 (class 0 OID 0)
-- Dependencies: 258
-- Name: demandefn_gid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE demandefn_gid_seq OWNED BY demandefn.gid;


--
-- TOC entry 259 (class 1259 OID 1683997)
-- Name: district; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE district (
    iddistrict bigint NOT NULL,
    idregion bigint,
    codedistrict character varying(10),
    nomdistrict character varying(50),
    shapelength double precision,
    shapearea double precision,
    csv_id character varying(32),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.district OWNER TO postgres;

--
-- TOC entry 260 (class 1259 OID 1684000)
-- Name: district_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE district_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.district_id_seq OWNER TO postgres;

--
-- TOC entry 5084 (class 0 OID 0)
-- Dependencies: 260
-- Name: district_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE district_id_seq OWNED BY district.iddistrict;


--
-- TOC entry 261 (class 1259 OID 1684002)
-- Name: document; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE document (
    id_document bigint NOT NULL,
    photo_document bytea,
    extension_document character varying(10),
    num_page integer,
    observation text,
    id_type smallint,
    iddemande bigint,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.document OWNER TO postgres;

--
-- TOC entry 262 (class 1259 OID 1684008)
-- Name: document_id_document_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE document_id_document_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.document_id_document_seq OWNER TO postgres;

--
-- TOC entry 5085 (class 0 OID 0)
-- Dependencies: 262
-- Name: document_id_document_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE document_id_document_seq OWNED BY document.id_document;


--
-- TOC entry 263 (class 1259 OID 1684018)
-- Name: fi_paiement_impot; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE fi_paiement_impot (
    id_paiement bigint NOT NULL,
    date date,
    montant real,
    numquittance character varying(50),
    idpersonne bigint,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.fi_paiement_impot OWNER TO postgres;

--
-- TOC entry 264 (class 1259 OID 1684021)
-- Name: fi_paiement_impot_id_paiement_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE fi_paiement_impot_id_paiement_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fi_paiement_impot_id_paiement_seq OWNER TO postgres;

--
-- TOC entry 5086 (class 0 OID 0)
-- Dependencies: 264
-- Name: fi_paiement_impot_id_paiement_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE fi_paiement_impot_id_paiement_seq OWNED BY fi_paiement_impot.id_paiement;


--
-- TOC entry 265 (class 1259 OID 1684023)
-- Name: fokontany; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE fokontany (
    idfokontany bigint NOT NULL,
    idcommune bigint,
    codefokontany text NOT NULL,
    nomfokontany character varying(50) NOT NULL,
    shapelength double precision,
    shapearea double precision,
    csv_id character varying(32),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.fokontany OWNER TO postgres;

--
-- TOC entry 266 (class 1259 OID 1684029)
-- Name: fokontany_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE fokontany_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fokontany_id_seq OWNER TO postgres;

--
-- TOC entry 5087 (class 0 OID 0)
-- Dependencies: 266
-- Name: fokontany_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE fokontany_id_seq OWNED BY fokontany.idfokontany;


--
-- TOC entry 267 (class 1259 OID 1684031)
-- Name: groupe; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE groupe (
    id integer NOT NULL,
    nom character varying(128),
    description text,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.groupe OWNER TO postgres;

--
-- TOC entry 268 (class 1259 OID 1684037)
-- Name: groupe_acces; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE groupe_acces (
    id bigint NOT NULL,
    groupe_id bigint,
    acces_id bigint,
    autorise boolean,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.groupe_acces OWNER TO postgres;

--
-- TOC entry 269 (class 1259 OID 1684040)
-- Name: groupe_acces_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE groupe_acces_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.groupe_acces_id_seq OWNER TO postgres;

--
-- TOC entry 5088 (class 0 OID 0)
-- Dependencies: 269
-- Name: groupe_acces_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE groupe_acces_id_seq OWNED BY groupe_acces.id;


--
-- TOC entry 270 (class 1259 OID 1684042)
-- Name: groupe_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE groupe_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.groupe_id_seq OWNER TO postgres;

--
-- TOC entry 5089 (class 0 OID 0)
-- Dependencies: 270
-- Name: groupe_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE groupe_id_seq OWNED BY groupe.id;


--
-- TOC entry 271 (class 1259 OID 1684044)
-- Name: hameau; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE hameau (
    idhameau bigint NOT NULL,
    idfokontany bigint,
    codehameau character varying(64) NOT NULL,
    nomhameau character varying(50) NOT NULL,
    shapelength double precision,
    shapearea double precision,
    csv_id character varying(32),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.hameau OWNER TO postgres;

--
-- TOC entry 272 (class 1259 OID 1684047)
-- Name: hameau_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE hameau_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.hameau_id_seq OWNER TO postgres;

--
-- TOC entry 5090 (class 0 OID 0)
-- Dependencies: 272
-- Name: hameau_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE hameau_id_seq OWNED BY hameau.idhameau;


--
-- TOC entry 273 (class 1259 OID 1684049)
-- Name: historique; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE historique (
    idhistorique bigint NOT NULL,
    typeoperation character varying(200),
    dateoperation date,
    idcertificat bigint,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.historique OWNER TO postgres;

--
-- TOC entry 274 (class 1259 OID 1684052)
-- Name: historique_idhistorique_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE historique_idhistorique_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.historique_idhistorique_seq OWNER TO postgres;

--
-- TOC entry 5091 (class 0 OID 0)
-- Dependencies: 274
-- Name: historique_idhistorique_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE historique_idhistorique_seq OWNED BY historique.idhistorique;


--
-- TOC entry 275 (class 1259 OID 1684054)
-- Name: hypotheque; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE hypotheque (
    dateinscriptionregistre date,
    duree bigint,
    valeur money,
    creancier character(50),
    descriptionhypotheque text,
    dateradiation date,
    idhypotheque bigint NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.hypotheque OWNER TO postgres;

--
-- TOC entry 276 (class 1259 OID 1684060)
-- Name: hypotheque_idhypotheque_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE hypotheque_idhypotheque_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.hypotheque_idhypotheque_seq OWNER TO postgres;

--
-- TOC entry 5092 (class 0 OID 0)
-- Dependencies: 276
-- Name: hypotheque_idhypotheque_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE hypotheque_idhypotheque_seq OWNED BY hypotheque.idhypotheque;


--
-- TOC entry 277 (class 1259 OID 1684062)
-- Name: hypothequeparcelle_d; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE hypothequeparcelle_d (
    idhypotheque bigint NOT NULL,
    idparcelle bigint NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.hypothequeparcelle_d OWNER TO postgres;

--
-- TOC entry 278 (class 1259 OID 1684065)
-- Name: iddemande_sans_geom_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE iddemande_sans_geom_seq
    START WITH 5241
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.iddemande_sans_geom_seq OWNER TO postgres;

--
-- TOC entry 279 (class 1259 OID 1684067)
-- Name: idprojet_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE idprojet_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.idprojet_seq OWNER TO postgres;

--
-- TOC entry 280 (class 1259 OID 1684069)
-- Name: impot; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE impot (
    idimpot bigint NOT NULL,
    numquittanceimpot bigint NOT NULL,
    anneeimpot bigint NOT NULL,
    dateimpot date NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.impot OWNER TO postgres;

--
-- TOC entry 281 (class 1259 OID 1684072)
-- Name: impot_batiment; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE impot_batiment (
    id bigint NOT NULL,
    hetratrano money,
    annee smallint,
    codebatiment character varying(10),
    montant_paye money,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.impot_batiment OWNER TO postgres;

--
-- TOC entry 282 (class 1259 OID 1684075)
-- Name: impot_batiment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE impot_batiment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.impot_batiment_id_seq OWNER TO postgres;

--
-- TOC entry 5093 (class 0 OID 0)
-- Dependencies: 282
-- Name: impot_batiment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE impot_batiment_id_seq OWNED BY impot_batiment.id;


--
-- TOC entry 283 (class 1259 OID 1684077)
-- Name: impot_contribuable; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE impot_contribuable (
    id bigint NOT NULL,
    hetratrano money,
    hetratany money,
    etatpaiement smallint,
    annee smallint,
    datereglement date,
    montantpaye money,
    idpersonne bigint,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.impot_contribuable OWNER TO postgres;

--
-- TOC entry 284 (class 1259 OID 1684080)
-- Name: impot_contribuable_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE impot_contribuable_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.impot_contribuable_id_seq OWNER TO postgres;

--
-- TOC entry 5094 (class 0 OID 0)
-- Dependencies: 284
-- Name: impot_contribuable_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE impot_contribuable_id_seq OWNED BY impot_contribuable.id;


--
-- TOC entry 285 (class 1259 OID 1684082)
-- Name: impot_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE impot_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.impot_id_seq OWNER TO postgres;

--
-- TOC entry 5095 (class 0 OID 0)
-- Dependencies: 285
-- Name: impot_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE impot_id_seq OWNED BY impot.idimpot;


--
-- TOC entry 286 (class 1259 OID 1684084)
-- Name: impot_minimum; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE impot_minimum (
    id_impotminimum integer NOT NULL,
    type character varying(6) NOT NULL,
    valeur real,
    annee character varying,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.impot_minimum OWNER TO postgres;

--
-- TOC entry 287 (class 1259 OID 1684090)
-- Name: impot_minimum_id_impotminimum_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE impot_minimum_id_impotminimum_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.impot_minimum_id_impotminimum_seq OWNER TO postgres;

--
-- TOC entry 5096 (class 0 OID 0)
-- Dependencies: 287
-- Name: impot_minimum_id_impotminimum_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE impot_minimum_id_impotminimum_seq OWNED BY impot_minimum.id_impotminimum;


--
-- TOC entry 288 (class 1259 OID 1684092)
-- Name: impot_parcelle; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE impot_parcelle (
    id bigint NOT NULL,
    hetratany money,
    annee smallint,
    idparcelle bigint,
    montant_paye money,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.impot_parcelle OWNER TO postgres;

--
-- TOC entry 289 (class 1259 OID 1684095)
-- Name: impot_parcelle_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE impot_parcelle_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.impot_parcelle_id_seq OWNER TO postgres;

--
-- TOC entry 5097 (class 0 OID 0)
-- Dependencies: 289
-- Name: impot_parcelle_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE impot_parcelle_id_seq OWNED BY impot_parcelle.id;


--
-- TOC entry 290 (class 1259 OID 1684097)
-- Name: impotparcelle; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE impotparcelle (
    idparcelle bigint NOT NULL,
    idimpot bigint NOT NULL,
    etatpaiement smallint,
    montantpayee money,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.impotparcelle OWNER TO postgres;

--
-- TOC entry 291 (class 1259 OID 1684100)
-- Name: journal; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE journal (
    id bigint NOT NULL,
    idutilisateur bigint,
    idobjetcible bigint,
    typeobjectcible character varying(100),
    description character varying(150),
    dateaction date,
    heureaction time without time zone,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.journal OWNER TO postgres;

--
-- TOC entry 292 (class 1259 OID 1684103)
-- Name: journal_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE journal_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.journal_id_seq OWNER TO postgres;

--
-- TOC entry 5098 (class 0 OID 0)
-- Dependencies: 292
-- Name: journal_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE journal_id_seq OWNED BY journal.id;


--
-- TOC entry 293 (class 1259 OID 1684105)
-- Name: limcomm_gid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE limcomm_gid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.limcomm_gid_seq OWNER TO postgres;

--
-- TOC entry 294 (class 1259 OID 1684107)
-- Name: limcommanjozorobe_gid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE limcommanjozorobe_gid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.limcommanjozorobe_gid_seq OWNER TO postgres;

--
-- TOC entry 295 (class 1259 OID 1684109)
-- Name: limitesparcelle; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE limitesparcelle (
    idpointscardinaux integer NOT NULL,
    idparcelle bigint NOT NULL,
    description character varying(1024),
    path_file character varying(2048),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.limitesparcelle OWNER TO postgres;

--
-- TOC entry 296 (class 1259 OID 1684123)
-- Name: menage; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE menage (
    id_menage bigint NOT NULL,
    code_menage character varying(125) NOT NULL,
    nombre_homme integer DEFAULT 0,
    nombre_femme integer DEFAULT 0,
    nombre_enfant integer DEFAULT 0,
    nombre_homme_actif integer DEFAULT 0,
    nombre_femme_active integer DEFAULT 0,
    possede_terre boolean DEFAULT false,
    acces_ressource boolean DEFAULT true,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.menage OWNER TO postgres;

--
-- TOC entry 297 (class 1259 OID 1684133)
-- Name: menage_id_menage_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE menage_id_menage_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.menage_id_menage_seq OWNER TO postgres;

--
-- TOC entry 5099 (class 0 OID 0)
-- Dependencies: 297
-- Name: menage_id_menage_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE menage_id_menage_seq OWNED BY menage.id_menage;


--
-- TOC entry 298 (class 1259 OID 1684135)
-- Name: migration_history; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE migration_history (
    filename character varying(128),
    migration_date timestamp without time zone,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.migration_history OWNER TO postgres;

--
-- TOC entry 299 (class 1259 OID 1684146)
-- Name: operationsub_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE operationsub_id_seq
    START WITH 18845
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.operationsub_id_seq OWNER TO postgres;

--
-- TOC entry 300 (class 1259 OID 1684148)
-- Name: operationsub; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE operationsub (
    id bigint DEFAULT nextval('operationsub_id_seq'::regclass) NOT NULL,
    typeacte bigint,
    idacte bigint,
    idcf character varying(250),
    datedepot date,
    dateinscription date,
    cout real,
    cout2 real,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.operationsub OWNER TO postgres;

--
-- TOC entry 301 (class 1259 OID 1684152)
-- Name: operationsubsequente; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE operationsubsequente (
    idoperationsubsequente bigint NOT NULL,
    idparcelle bigint,
    typeoperationsubsequente character(120) NOT NULL,
    datedepotdemande date NOT NULL,
    dateinscriptionregistre date NOT NULL,
    cout1 money NOT NULL,
    cout2 money,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.operationsubsequente OWNER TO postgres;

--
-- TOC entry 302 (class 1259 OID 1684155)
-- Name: operationsubsequente_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE operationsubsequente_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.operationsubsequente_id_seq OWNER TO postgres;

--
-- TOC entry 5100 (class 0 OID 0)
-- Dependencies: 302
-- Name: operationsubsequente_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE operationsubsequente_id_seq OWNED BY operationsubsequente.idoperationsubsequente;


--
-- TOC entry 303 (class 1259 OID 1684157)
-- Name: oppositions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE oppositions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.oppositions_id_seq OWNER TO postgres;

--
-- TOC entry 304 (class 1259 OID 1684159)
-- Name: oppositions; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE oppositions (
    idopposition integer DEFAULT nextval('oppositions_id_seq'::regclass) NOT NULL,
    dateopposition date,
    datedemande date,
    typeopposition character varying(250),
    description character varying(250),
    datereglement date,
    naturereglement character varying(250),
    descriptionreglement character varying(250),
    iddemande integer NOT NULL,
    gid integer,
    etatopposition integer DEFAULT 0,
    datemaj timestamp without time zone DEFAULT now(),
    uuid_lr_sys character varying(90)
);


ALTER TABLE public.oppositions OWNER TO postgres;

--
-- TOC entry 305 (class 1259 OID 1684167)
-- Name: param_layer_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE param_layer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.param_layer_id_seq OWNER TO postgres;

--
-- TOC entry 306 (class 1259 OID 1684169)
-- Name: param_layer; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE param_layer (
    id integer DEFAULT nextval('param_layer_id_seq'::regclass) NOT NULL,
    label_font character varying(64),
    label_size smallint,
    label_color character varying(7),
    stroke_size smallint,
    stroke_color character varying(7),
    layer_index smallint,
    font_size_map_units boolean,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.param_layer OWNER TO postgres;

--
-- TOC entry 307 (class 1259 OID 1684179)
-- Name: parcelle_d; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE parcelle_d (
    gid integer NOT NULL,
    numero character varying(30),
    geom geometry,
    numdemande character varying(1000),
    nomdemandeur character varying(1024),
    surface numeric(20,1),
    titre character varying(20),
    partie numeric(10,1),
    parcelle character varying(20),
    etat numeric(10,1),
    datecreation date,
    datereconnaissance date,
    cout double precision,
    region character varying(128),
    district character varying(128),
    commune character varying(128),
    fkt character varying(128),
    consistance character varying(128),
    feuille character(50),
    idcertificat bigint,
    idhameau bigint,
    idcharge bigint,
    idhypotheque bigint,
    idservitude bigint,
    idcategorie bigint,
    srisraparcelle character varying(5),
    codeparcelle character varying(50),
    numcertificat character varying(20),
    estfiscalite smallint DEFAULT 0,
    idcontribuable bigint,
    grille character varying(100),
    has_data boolean,
    numerodmdpaps character varying(250),
    conversion smallint,
    etatparcelle_d smallint,
    id_consistance bigint,
    idclasse bigint,
    id_commune bigint,
    csv_id character varying(32),
    anomalie boolean,
    limitrophe boolean,
    observation character varying(64),
    code_parcelle_en_doublon character varying(64),
    editer_en_cf boolean,
    inventaire boolean,
    sujet_demande boolean,
    date_inventaire date,
    user_import_inv bigint,
    date_import_inv date,
    ref_import character varying(64),
    categorie character varying(128),
    fi_forfait character varying(15),
    datemaj timestamp without time zone DEFAULT now(),
    uuid_dossier_lr character varying(90),
    CONSTRAINT geometry_valid_check CHECK (st_isvalid(geom))
);


ALTER TABLE public.parcelle_d OWNER TO postgres;

--
-- TOC entry 5101 (class 0 OID 0)
-- Dependencies: 307
-- Name: COLUMN parcelle_d.conversion; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN parcelle_d.conversion IS 'Valeur = 1 equivalent parcelle convertie en demande
Valeur = 2 equivalent parcelle convertie en Certficat';


--
-- TOC entry 5102 (class 0 OID 0)
-- Dependencies: 307
-- Name: COLUMN parcelle_d.etatparcelle_d; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN parcelle_d.etatparcelle_d IS '0 aucun
1 titre
2 cadastre
3 certificat
';


--
-- TOC entry 5103 (class 0 OID 0)
-- Dependencies: 307
-- Name: COLUMN parcelle_d.id_consistance; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN parcelle_d.id_consistance IS 'Clé etrangère vers consistance';


--
-- TOC entry 5104 (class 0 OID 0)
-- Dependencies: 307
-- Name: COLUMN parcelle_d.id_commune; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN parcelle_d.id_commune IS 'Cle etrangere commune';


--
-- TOC entry 5105 (class 0 OID 0)
-- Dependencies: 307
-- Name: COLUMN parcelle_d.fi_forfait; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN parcelle_d.fi_forfait IS 'Valeur type calcul impôt:soit surface,soit classe, soit valeur_venale';


--
-- TOC entry 308 (class 1259 OID 1684187)
-- Name: parcelle_d_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE parcelle_d_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.parcelle_d_id_seq OWNER TO postgres;

--
-- TOC entry 5106 (class 0 OID 0)
-- Dependencies: 308
-- Name: parcelle_d_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE parcelle_d_id_seq OWNED BY parcelle_d.gid;


--
-- TOC entry 309 (class 1259 OID 1684207)
-- Name: parcellegrevees; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE parcellegrevees (
    idparcellegrevees bigint NOT NULL,
    libelleparcellegrevees text,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.parcellegrevees OWNER TO postgres;

--
-- TOC entry 310 (class 1259 OID 1684213)
-- Name: parcellegrevees_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE parcellegrevees_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.parcellegrevees_id_seq OWNER TO postgres;

--
-- TOC entry 5107 (class 0 OID 0)
-- Dependencies: 310
-- Name: parcellegrevees_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE parcellegrevees_id_seq OWNED BY parcellegrevees.idparcellegrevees;


--
-- TOC entry 372 (class 1259 OID 1685387)
-- Name: path_personne; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE path_personne (
    idpersonne bigint NOT NULL,
    cin_recto character varying(2048),
    cin_verso character varying(2048),
    signature character varying(2048),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.path_personne OWNER TO postgres;

--
-- TOC entry 311 (class 1259 OID 1684223)
-- Name: personne; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE personne (
    idpersonne bigint NOT NULL,
    nompersonne character varying(100),
    prenompersonne character varying(100),
    sexepersonne character varying(25),
    datenaissancepersonne date,
    nevers smallint,
    lieunaissancepersonne character varying(100),
    numcipersonne character varying(20),
    datecipersonne date,
    lieucipersonne character varying(100),
    numactenaissancepersonne character varying(50),
    dateactenaissancepersonne date,
    lieuactenaissancepersonne character varying(100),
    adressepersonne character varying(100),
    situationmatrimoniale smallint DEFAULT 0,
    nompere character varying(150),
    nommere character varying(150),
    csv_id character varying(32),
    rcin_personne character varying(256),
    ogr_id character varying(32),
    handicap boolean DEFAULT false,
    niveau_education text,
    possede_emploi boolean DEFAULT true,
    migrant boolean DEFAULT false,
    date_arrivee date,
    conjoint character varying(256),
    datemaj timestamp without time zone DEFAULT now(),
    uuid_dossier_lr character varying(90)
);


ALTER TABLE public.personne OWNER TO postgres;

--
-- TOC entry 5108 (class 0 OID 0)
-- Dependencies: 311
-- Name: TABLE personne; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE personne IS 'Table personne en generale, permettant de gerer les proprietaires, les demandeurs et les contribuables';


--
-- TOC entry 5109 (class 0 OID 0)
-- Dependencies: 311
-- Name: COLUMN personne.situationmatrimoniale; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN personne.situationmatrimoniale IS '0 => celibataire, 1 => marie, 2 => veuf';


--
-- TOC entry 312 (class 1259 OID 1684233)
-- Name: personne_idpersonne_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE personne_idpersonne_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.personne_idpersonne_seq OWNER TO postgres;

--
-- TOC entry 5110 (class 0 OID 0)
-- Dependencies: 312
-- Name: personne_idpersonne_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE personne_idpersonne_seq OWNED BY personne.idpersonne;


--
-- TOC entry 313 (class 1259 OID 1684235)
-- Name: personne_menage; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE personne_menage (
    idpersonne bigint NOT NULL,
    id_menage bigint NOT NULL,
    est_chef boolean DEFAULT false,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.personne_menage OWNER TO postgres;

--
-- TOC entry 314 (class 1259 OID 1684239)
-- Name: personnemorale; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE personnemorale (
    numeroproprietaire character(50),
    denomination text NOT NULL,
    datecreation date,
    siege text,
    observation text,
    idtype bigint,
    idpersonnemorale bigint NOT NULL,
    csv_id character varying(32),
    rcin_pm character varying(256),
    mandataire character varying(256),
    type_declarant character varying(256),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.personnemorale OWNER TO postgres;

--
-- TOC entry 315 (class 1259 OID 1684245)
-- Name: personnemorale_idpersonnemorale_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE personnemorale_idpersonnemorale_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.personnemorale_idpersonnemorale_seq OWNER TO postgres;

--
-- TOC entry 5111 (class 0 OID 0)
-- Dependencies: 315
-- Name: personnemorale_idpersonnemorale_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE personnemorale_idpersonnemorale_seq OWNED BY personnemorale.idpersonnemorale;


--
-- TOC entry 316 (class 1259 OID 1684247)
-- Name: personnemoraleparcelle; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE personnemoraleparcelle (
    idparcelle bigint NOT NULL,
    idpersonnemorale character(32) NOT NULL,
    idpersonne bigint NOT NULL,
    representant boolean,
    iddemande bigint,
    csv_id character varying(32),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.personnemoraleparcelle OWNER TO postgres;

--
-- TOC entry 317 (class 1259 OID 1684250)
-- Name: personnemoraleparcelle_d; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE personnemoraleparcelle_d (
    idpersonne bigint NOT NULL,
    idparcelle bigint NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.personnemoraleparcelle_d OWNER TO postgres;

--
-- TOC entry 318 (class 1259 OID 1684261)
-- Name: pointscardinaux; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE pointscardinaux (
    idpointscardinaux integer NOT NULL,
    "position" character varying NOT NULL,
    fanondroana character varying,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.pointscardinaux OWNER TO postgres;

--
-- TOC entry 319 (class 1259 OID 1684267)
-- Name: pointscardinaux_idpointscardinaux_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE pointscardinaux_idpointscardinaux_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pointscardinaux_idpointscardinaux_seq OWNER TO postgres;

--
-- TOC entry 5112 (class 0 OID 0)
-- Dependencies: 319
-- Name: pointscardinaux_idpointscardinaux_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE pointscardinaux_idpointscardinaux_seq OWNED BY pointscardinaux.idpointscardinaux;


--
-- TOC entry 320 (class 1259 OID 1684269)
-- Name: projet_idprojet_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE projet_idprojet_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE public.projet_idprojet_seq OWNER TO postgres;

--
-- TOC entry 321 (class 1259 OID 1684271)
-- Name: projet; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE projet (
    idprojet integer DEFAULT nextval('projet_idprojet_seq'::regclass) NOT NULL,
    date_lancement date,
    date_premier_import date,
    date_dernier_import date,
    langue character varying(2),
    nom character varying(128) NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.projet OWNER TO postgres;

--
-- TOC entry 322 (class 1259 OID 1684275)
-- Name: projet_commune_idprojet_commune_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE projet_commune_idprojet_commune_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.projet_commune_idprojet_commune_seq OWNER TO postgres;

--
-- TOC entry 323 (class 1259 OID 1684277)
-- Name: projet_commune; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE projet_commune (
    idprojet_commune bigint DEFAULT nextval('projet_commune_idprojet_commune_seq'::regclass) NOT NULL,
    idcommune bigint,
    idprojet integer,
    fond_image character varying(1024),
    couche_titres character varying(1024),
    couche_cadastres character varying(1024),
    couche_limites character varying(1024),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.projet_commune OWNER TO postgres;

--
-- TOC entry 324 (class 1259 OID 1684284)
-- Name: projet_plof; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE projet_plof (
    idprojet integer DEFAULT nextval('idprojet_seq'::regclass) NOT NULL,
    "codeRegion" integer,
    "codeDistrict" integer,
    "codeCommune" integer,
    "Region" character varying(250),
    "District" character varying(250),
    "Commune" character varying(250),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.projet_plof OWNER TO postgres;

--
-- TOC entry 325 (class 1259 OID 1684291)
-- Name: projetcouche_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE projetcouche_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.projetcouche_id_seq OWNER TO postgres;

--
-- TOC entry 326 (class 1259 OID 1684293)
-- Name: projetcouche; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE projetcouche (
    id bigint DEFAULT nextval('projetcouche_id_seq'::regclass) NOT NULL,
    idprojet_commune bigint,
    libelle character varying(64),
    type_couche character(1),
    fichier character varying(1024),
    couleur_bg character varying(7),
    ordre integer DEFAULT 0 NOT NULL,
    label_name character varying(64),
    show_label boolean,
    font character varying(64),
    font_size smallint,
    font_size_map_unit boolean,
    font_color character varying(7),
    show_stroke boolean,
    stroke_width smallint,
    stroke_color character varying(7),
    remplissage integer DEFAULT 0,
    plofpaps integer DEFAULT 0,
    certifiable smallint DEFAULT 0,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.projetcouche OWNER TO postgres;

--
-- TOC entry 327 (class 1259 OID 1684311)
-- Name: proprietaireparcelle; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE proprietaireparcelle (
    idpersonne bigint NOT NULL,
    idparcelle bigint NOT NULL,
    representant boolean,
    contribuable boolean,
    estcoproprietaire boolean,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.proprietaireparcelle OWNER TO postgres;

--
-- TOC entry 5113 (class 0 OID 0)
-- Dependencies: 327
-- Name: COLUMN proprietaireparcelle.contribuable; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN proprietaireparcelle.contribuable IS 'differencier les proprios contribuable et les non contribuable';


--
-- TOC entry 328 (class 1259 OID 1684317)
-- Name: region; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE region (
    idregion bigint NOT NULL,
    coderegion character varying(50),
    nomregion character varying(50),
    shapelength double precision,
    shapearea double precision,
    csv_id character varying(32),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.region OWNER TO postgres;

--
-- TOC entry 329 (class 1259 OID 1684320)
-- Name: region_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE region_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.region_id_seq OWNER TO postgres;

--
-- TOC entry 5114 (class 0 OID 0)
-- Dependencies: 329
-- Name: region_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE region_id_seq OWNED BY region.idregion;


--
-- TOC entry 330 (class 1259 OID 1684322)
-- Name: rejet_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE rejet_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rejet_id_seq OWNER TO postgres;

--
-- TOC entry 331 (class 1259 OID 1684324)
-- Name: rejet; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE rejet (
    idrejet integer DEFAULT nextval('rejet_id_seq'::regclass) NOT NULL,
    typerejet character varying(250),
    daterejet date,
    motifrejet character varying(250),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.rejet OWNER TO postgres;

--
-- TOC entry 332 (class 1259 OID 1684331)
-- Name: role_crl; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE role_crl (
    id_role integer NOT NULL,
    libelle_role character varying(100),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.role_crl OWNER TO postgres;

--
-- TOC entry 333 (class 1259 OID 1684334)
-- Name: role_crl_id_role_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE role_crl_id_role_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.role_crl_id_role_seq OWNER TO postgres;

--
-- TOC entry 5115 (class 0 OID 0)
-- Dependencies: 333
-- Name: role_crl_id_role_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE role_crl_id_role_seq OWNED BY role_crl.id_role;


--
-- TOC entry 334 (class 1259 OID 1684336)
-- Name: servitude; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE servitude (
    numeroservitude bigint,
    dateinscription date NOT NULL,
    origine character(50) NOT NULL,
    descriptionservitude text,
    datelevee date,
    radie smallint,
    shape_length double precision,
    shape_area double precision,
    idservitude bigint NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.servitude OWNER TO postgres;

--
-- TOC entry 335 (class 1259 OID 1684342)
-- Name: servitude_idservitude_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE servitude_idservitude_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.servitude_idservitude_seq OWNER TO postgres;

--
-- TOC entry 5116 (class 0 OID 0)
-- Dependencies: 335
-- Name: servitude_idservitude_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE servitude_idservitude_seq OWNED BY servitude.idservitude;


--
-- TOC entry 336 (class 1259 OID 1684344)
-- Name: servitudebeneficiaire; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE servitudebeneficiaire (
    idbeneficiaire bigint NOT NULL,
    idservitude bigint NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.servitudebeneficiaire OWNER TO postgres;

--
-- TOC entry 337 (class 1259 OID 1684347)
-- Name: servitudeparcelle_d; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE servitudeparcelle_d (
    idservitude bigint NOT NULL,
    idparcelle bigint NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.servitudeparcelle_d OWNER TO postgres;

--
-- TOC entry 338 (class 1259 OID 1684350)
-- Name: servitudeparcellegrevees; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE servitudeparcellegrevees (
    idparcellegrevees bigint NOT NULL,
    idservitude bigint NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.servitudeparcellegrevees OWNER TO postgres;

--
-- TOC entry 339 (class 1259 OID 1684353)
-- Name: servitudeparcellegrevees_idservitude_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE servitudeparcellegrevees_idservitude_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.servitudeparcellegrevees_idservitude_seq OWNER TO postgres;

--
-- TOC entry 5117 (class 0 OID 0)
-- Dependencies: 339
-- Name: servitudeparcellegrevees_idservitude_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE servitudeparcellegrevees_idservitude_seq OWNED BY servitudeparcellegrevees.idservitude;


--
-- TOC entry 340 (class 1259 OID 1684355)
-- Name: terain_status_specifique; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE terain_status_specifique (
    gid bigint NOT NULL,
    fn_fg character varying(100),
    demandeur character varying(100),
    sur_plan double precision,
    obs character varying(100),
    geom geometry,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.terain_status_specifique OWNER TO postgres;

--
-- TOC entry 341 (class 1259 OID 1684361)
-- Name: terain_status_specifique_gid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE terain_status_specifique_gid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.terain_status_specifique_gid_seq OWNER TO postgres;

--
-- TOC entry 5118 (class 0 OID 0)
-- Dependencies: 341
-- Name: terain_status_specifique_gid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE terain_status_specifique_gid_seq OWNED BY terain_status_specifique.gid;


--
-- TOC entry 342 (class 1259 OID 1684363)
-- Name: titre; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE titre (
    gid bigint NOT NULL,
    titres character varying(25),
    propriete character varying(100),
    sur_plan double precision,
    titre_r character varying(100),
    parcelle character varying(50),
    partie character varying(50),
    feuille character varying(50),
    geom geometry,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.titre OWNER TO postgres;

--
-- TOC entry 343 (class 1259 OID 1684369)
-- Name: titre arivonimamo i eugenie_gid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "titre arivonimamo i eugenie_gid_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."titre arivonimamo i eugenie_gid_seq" OWNER TO postgres;

--
-- TOC entry 344 (class 1259 OID 1684371)
-- Name: titre_gid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE titre_gid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.titre_gid_seq OWNER TO postgres;

--
-- TOC entry 5119 (class 0 OID 0)
-- Dependencies: 344
-- Name: titre_gid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE titre_gid_seq OWNED BY titre.gid;


--
-- TOC entry 345 (class 1259 OID 1684373)
-- Name: titrefoncier; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE titrefoncier (
    numerotitre character(50),
    datetitre date,
    contenance bigint,
    cheminplanindividuel character(50),
    originecontour text,
    typetitre character(50),
    acteurpublic smallint,
    nompropriete character(120),
    consistance character(120),
    shape_length double precision,
    shape_area double precision,
    geom geometry,
    gid bigint NOT NULL,
    observation character varying(400),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.titrefoncier OWNER TO postgres;

--
-- TOC entry 346 (class 1259 OID 1684379)
-- Name: titrefoncier_gid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE titrefoncier_gid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.titrefoncier_gid_seq OWNER TO postgres;

--
-- TOC entry 5120 (class 0 OID 0)
-- Dependencies: 346
-- Name: titrefoncier_gid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE titrefoncier_gid_seq OWNED BY titrefoncier.gid;


--
-- TOC entry 347 (class 1259 OID 1684381)
-- Name: type_anomalie; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE type_anomalie (
    id_type_anomalie bigint NOT NULL,
    valeur character varying(32),
    csv_id character varying(32),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.type_anomalie OWNER TO postgres;

--
-- TOC entry 348 (class 1259 OID 1684384)
-- Name: type_anomalie_id_type_anomalie_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE type_anomalie_id_type_anomalie_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.type_anomalie_id_type_anomalie_seq OWNER TO postgres;

--
-- TOC entry 5121 (class 0 OID 0)
-- Dependencies: 348
-- Name: type_anomalie_id_type_anomalie_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE type_anomalie_id_type_anomalie_seq OWNED BY type_anomalie.id_type_anomalie;


--
-- TOC entry 349 (class 1259 OID 1684386)
-- Name: type_document; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE type_document (
    id_type integer NOT NULL,
    libelle_type character varying(128),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.type_document OWNER TO postgres;

--
-- TOC entry 350 (class 1259 OID 1684389)
-- Name: type_document_id_type_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE type_document_id_type_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.type_document_id_type_seq OWNER TO postgres;

--
-- TOC entry 5122 (class 0 OID 0)
-- Dependencies: 350
-- Name: type_document_id_type_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE type_document_id_type_seq OWNED BY type_document.id_type;


--
-- TOC entry 351 (class 1259 OID 1684391)
-- Name: typeforfaitaire; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE typeforfaitaire (
    idforfaitaire bigint NOT NULL,
    libelleforfaitaire character varying(50) NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.typeforfaitaire OWNER TO postgres;

--
-- TOC entry 352 (class 1259 OID 1684394)
-- Name: typeforfaitaire_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE typeforfaitaire_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.typeforfaitaire_id_seq OWNER TO postgres;

--
-- TOC entry 5123 (class 0 OID 0)
-- Dependencies: 352
-- Name: typeforfaitaire_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE typeforfaitaire_id_seq OWNED BY typeforfaitaire.idforfaitaire;


--
-- TOC entry 353 (class 1259 OID 1684396)
-- Name: typeoperationsubsequente_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE typeoperationsubsequente_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.typeoperationsubsequente_id_seq OWNER TO postgres;

--
-- TOC entry 354 (class 1259 OID 1684398)
-- Name: typeoperationsubsequente; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE typeoperationsubsequente (
    idtype integer DEFAULT nextval('typeoperationsubsequente_id_seq'::regclass) NOT NULL,
    libelleoperation character varying(250),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.typeoperationsubsequente OWNER TO postgres;

--
-- TOC entry 355 (class 1259 OID 1684402)
-- Name: typepersonnemorale; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE typepersonnemorale (
    idtype bigint NOT NULL,
    type character varying(50),
    karazana character varying(50),
    csv_id character varying(32),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.typepersonnemorale OWNER TO postgres;

--
-- TOC entry 356 (class 1259 OID 1684405)
-- Name: typepersonnemorale_idtype_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE typepersonnemorale_idtype_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.typepersonnemorale_idtype_seq OWNER TO postgres;

--
-- TOC entry 5124 (class 0 OID 0)
-- Dependencies: 356
-- Name: typepersonnemorale_idtype_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE typepersonnemorale_idtype_seq OWNED BY typepersonnemorale.idtype;


--
-- TOC entry 357 (class 1259 OID 1684407)
-- Name: utilisateur_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE utilisateur_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE public.utilisateur_id_seq OWNER TO postgres;

--
-- TOC entry 358 (class 1259 OID 1684409)
-- Name: utilisateur; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE utilisateur (
    idutilisateur integer DEFAULT nextval('utilisateur_id_seq'::regclass) NOT NULL,
    nomutilisateur character varying(100) NOT NULL,
    prenomutilisateur character varying(100),
    loginutilisateur character varying(50) NOT NULL,
    passwordutilisateur character varying(50) NOT NULL,
    typeutilisateur character varying(20),
    telephone character varying(20),
    adresse character varying(256),
    fonction character varying(128),
    loginufiplof character varying(250),
    passwdfiplof character varying(250),
    groupe_id integer,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.utilisateur OWNER TO postgres;

--
-- TOC entry 359 (class 1259 OID 1684416)
-- Name: voisinparcelle_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE voisinparcelle_id_seq
    START WITH 10
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE public.voisinparcelle_id_seq OWNER TO postgres;

--
-- TOC entry 360 (class 1259 OID 1684418)
-- Name: voisinparcelle; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE voisinparcelle (
    idvp bigint DEFAULT nextval('voisinparcelle_id_seq'::regclass) NOT NULL,
    idvoisin bigint NOT NULL,
    idpacelle bigint NOT NULL,
    iddemande bigint NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.voisinparcelle OWNER TO postgres;

--
-- TOC entry 361 (class 1259 OID 1684422)
-- Name: voisins_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE voisins_id_seq
    START WITH 10
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE public.voisins_id_seq OWNER TO postgres;

--
-- TOC entry 362 (class 1259 OID 1684424)
-- Name: voisins; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE voisins (
    idvoisin bigint DEFAULT nextval('voisins_id_seq'::regclass) NOT NULL,
    nom character varying(250),
    prenom character varying(250),
    adresse character varying(250),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.voisins OWNER TO postgres;

--
-- TOC entry 363 (class 1259 OID 1684431)
-- Name: vw_cadastre; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW vw_cadastre AS
 SELECT cadastre.gid,
    cadastre.nom_section,
    cadastre.section,
    cadastre.parcelle,
    cadastre.nom_plan,
    cadastre.geom
   FROM cadastre;


ALTER TABLE public.vw_cadastre OWNER TO postgres;

--
-- TOC entry 364 (class 1259 OID 1684435)
-- Name: vw_certificat; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW vw_certificat AS
 SELECT p.gid,
    p.geom,
    c.numerocertificat,
    c.idcommune,
    c.idcertificat
   FROM (certificat c
     JOIN parcelle_d p ON ((p.idcertificat = c.idcertificat)));


ALTER TABLE public.vw_certificat OWNER TO postgres;

--
-- TOC entry 365 (class 1259 OID 1684440)
-- Name: vw_demande; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW vw_demande AS
 SELECT p.gid,
    p.geom,
    COALESCE(p.numdemande, p.codeparcelle) AS numdemande,
    d.idcommune
   FROM (demande d
     RIGHT JOIN parcelle_d p ON ((p.gid = d.gid)))
  WHERE ((((p.estfiscalite IS NULL) OR (p.estfiscalite = 0)) OR (p.numdemande IS NOT NULL)) OR (p.conversion = 1));


ALTER TABLE public.vw_demande OWNER TO postgres;

--
-- TOC entry 366 (class 1259 OID 1684445)
-- Name: vw_demandefn; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW vw_demandefn AS
 SELECT demandefn.gid,
    demandefn.fn_fg,
    demandefn.demandeur,
    demandefn.sur_plan,
    demandefn.geom
   FROM demandefn;


ALTER TABLE public.vw_demandefn OWNER TO postgres;

--
-- TOC entry 367 (class 1259 OID 1684449)
-- Name: vw_fiscalite; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW vw_fiscalite AS
 SELECT p.gid,
    p.geom,
    p.codeparcelle AS numero
   FROM parcelle_d p
  WHERE (p.estfiscalite = 1);


ALTER TABLE public.vw_fiscalite OWNER TO postgres;

--
-- TOC entry 368 (class 1259 OID 1684453)
-- Name: vw_shape_certificat; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW vw_shape_certificat AS
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
   FROM (((((((certificat c
     JOIN parcelle_d p ON ((p.idcertificat = c.idcertificat)))
     JOIN demande d ON ((d.gid = p.gid)))
     JOIN proprietaireparcelle pp ON ((p.gid = pp.idparcelle)))
     JOIN personne pers ON ((pp.idpersonne = pers.idpersonne)))
     JOIN commune com ON ((com.idcommune = d.idcommune)))
     LEFT JOIN fokontany fkt ON ((fkt.idfokontany = d.idfokontany)))
     LEFT JOIN hameau h ON ((h.idhameau = p.idhameau)));


ALTER TABLE public.vw_shape_certificat OWNER TO postgres;

--
-- TOC entry 369 (class 1259 OID 1684458)
-- Name: vw_shape_demande; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW vw_shape_demande AS
 WITH q1 AS (
         SELECT demande_1.iddemande,
            string_agg(((((((((((((((((((((((((((((((concat(p_1.nompersonne, ' ', COALESCE(p_1.prenompersonne, ''::character varying)) || '<FIELD>'::text) || (p_1.sexepersonne)::text) || '<FIELD>'::text) || COALESCE(p_1.datenaissancepersonne, '1000-01-01'::date)) || '<FIELD>'::text) || COALESCE((p_1.nevers)::integer, 0)) || '<FIELD>'::text) || (COALESCE(p_1.numcipersonne, ''::character varying))::text) || '<FIELD>'::text) || (COALESCE(p_1.numactenaissancepersonne, ''::character varying))::text) || '<FIELD>'::text) || COALESCE(p_1.datecipersonne, '1000-01-01'::date)) || '<FIELD>'::text) || (COALESCE(p_1.lieucipersonne, ''::character varying))::text) || '<FIELD>'::text) || COALESCE(p_1.dateactenaissancepersonne, '1000-01-01'::date)) || '<FIELD>'::text) || (COALESCE(p_1.lieuactenaissancepersonne, ''::character varying))::text) || '<FIELD>'::text) || (COALESCE(p_1.adressepersonne, ''::character varying))::text) || '<FIELD>'::text) || (COALESCE(p_1.nompere, ''::character varying))::text) || '<FIELD>'::text) || (COALESCE(p_1.nommere, ''::character varying))::text) || '<FIELD>'::text) || (COALESCE(p_1.conjoint, ''::character varying))::text) || '<FIELD>'::text) || p_1.idpersonne) || '<FIELD>'::text) || COALESCE(a.representant, false)), '<ROW>'::text) AS demandeurs
           FROM ((demande demande_1
             LEFT JOIN avoir_demande a ON ((a.iddemande = demande_1.iddemande)))
             LEFT JOIN personne p_1 ON ((p_1.idpersonne = a.idpersonne)))
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
   FROM (((((demande
     JOIN q1 ON ((q1.iddemande = demande.iddemande)))
     JOIN parcelle_d p ON ((p.gid = demande.gid)))
     JOIN commune com ON ((com.idcommune = demande.idcommune)))
     LEFT JOIN fokontany fkt ON ((fkt.idfokontany = demande.idfokontany)))
     LEFT JOIN hameau h ON ((h.idhameau = p.idhameau)))
  WHERE (demande.numdemande IS NOT NULL);


ALTER TABLE public.vw_shape_demande OWNER TO postgres;

--
-- TOC entry 370 (class 1259 OID 1684463)
-- Name: vw_titre; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW vw_titre AS
 SELECT titre.gid,
    titre.titres,
    titre.propriete,
    titre.sur_plan,
    titre.titre_r,
    titre.parcelle,
    titre.partie,
    titre.feuille,
    titre.geom
   FROM titre;


ALTER TABLE public.vw_titre OWNER TO postgres;

--
-- TOC entry 371 (class 1259 OID 1684467)
-- Name: vw_tss; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW vw_tss AS
 SELECT terain_status_specifique.gid,
    terain_status_specifique.fn_fg,
    terain_status_specifique.demandeur,
    terain_status_specifique.sur_plan,
    terain_status_specifique.obs,
    terain_status_specifique.geom
   FROM terain_status_specifique;


ALTER TABLE public.vw_tss OWNER TO postgres;

--
-- TOC entry 373 (class 1259 OID 1685396)
-- Name: z_certifiable_gid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE z_certifiable_gid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.z_certifiable_gid_seq OWNER TO postgres;

--
-- TOC entry 374 (class 1259 OID 1685398)
-- Name: z_certifiable; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE z_certifiable (
    gid integer DEFAULT nextval('z_certifiable_gid_seq'::regclass) NOT NULL,
    id integer,
    crtfbl integer,
    geom geometry(Polygon,29702),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.z_certifiable OWNER TO postgres;

--
-- TOC entry 375 (class 1259 OID 1685408)
-- Name: vw_z_certifiable; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW vw_z_certifiable AS
 SELECT z_certifiable.gid,
    z_certifiable.id,
    z_certifiable.crtfbl,
    z_certifiable.geom
   FROM z_certifiable;


ALTER TABLE public.vw_z_certifiable OWNER TO postgres;

--
-- TOC entry 4045 (class 2604 OID 1684471)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY acces ALTER COLUMN id SET DEFAULT nextval('acces_id_seq'::regclass);


--
-- TOC entry 4048 (class 2604 OID 1684472)
-- Name: idactedeces; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY actedeces ALTER COLUMN idactedeces SET DEFAULT nextval('actedeces_id_seq'::regclass);


--
-- TOC entry 4054 (class 2604 OID 1684473)
-- Name: idacteprive; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY acteprive ALTER COLUMN idacteprive SET DEFAULT nextval('acteprive_id_seq'::regclass);


--
-- TOC entry 4059 (class 2604 OID 1684474)
-- Name: idactepublic; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY actepublic ALTER COLUMN idactepublic SET DEFAULT nextval('actepublic_id_seq'::regclass);


--
-- TOC entry 4062 (class 2604 OID 1684475)
-- Name: idaireastatutspecifique; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY aireastatutspecifique ALTER COLUMN idaireastatutspecifique SET DEFAULT nextval('aireastatutspecifique_idaireastatutspecifique_seq'::regclass);


--
-- TOC entry 4064 (class 2604 OID 1684476)
-- Name: idanomalie; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY anomalie ALTER COLUMN idanomalie SET DEFAULT nextval('anomalie_idanomalie_seq'::regclass);


--
-- TOC entry 4066 (class 2604 OID 1684477)
-- Name: idcharge; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY autrecharge ALTER COLUMN idcharge SET DEFAULT nextval('autrecharge_idcharge_seq'::regclass);


--
-- TOC entry 4073 (class 2604 OID 1684478)
-- Name: idbeneficiaire; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY beneficiaire ALTER COLUMN idbeneficiaire SET DEFAULT nextval('beneficiaire_id_seq'::regclass);


--
-- TOC entry 4076 (class 2604 OID 1684479)
-- Name: idblob; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY blob_personne ALTER COLUMN idblob SET DEFAULT nextval('blob_personne_idblob_seq'::regclass);


--
-- TOC entry 4079 (class 2604 OID 1684480)
-- Name: gid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY cadastre ALTER COLUMN gid SET DEFAULT nextval('cadastre_gid_seq'::regclass);


--
-- TOC entry 4085 (class 2604 OID 1684481)
-- Name: idcategorie; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY categorie ALTER COLUMN idcategorie SET DEFAULT nextval('categorie_id_seq'::regclass);


--
-- TOC entry 4089 (class 2604 OID 1684482)
-- Name: idcertificat; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY certificat ALTER COLUMN idcertificat SET DEFAULT nextval('certificat_idcertificat_seq'::regclass);


--
-- TOC entry 4091 (class 2604 OID 1684483)
-- Name: idclasse; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY classe ALTER COLUMN idclasse SET DEFAULT nextval('classe_id_seq'::regclass);


--
-- TOC entry 4097 (class 2604 OID 1684484)
-- Name: idcommune; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY commune ALTER COLUMN idcommune SET DEFAULT nextval('commune_id_seq'::regclass);


--
-- TOC entry 4099 (class 2604 OID 1684485)
-- Name: idconsistance; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY consistance ALTER COLUMN idconsistance SET DEFAULT nextval('consistance_id_seq'::regclass);


--
-- TOC entry 4103 (class 2604 OID 1684486)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY consistance_batiment ALTER COLUMN id SET DEFAULT nextval('consistance_batiment_id_seq'::regclass);


--
-- TOC entry 4245 (class 2604 OID 1686336)
-- Name: id_synchro; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY date_synchro ALTER COLUMN id_synchro SET DEFAULT nextval('date_synchro_id_synchro_seq'::regclass);


--
-- TOC entry 4113 (class 2604 OID 1684488)
-- Name: iddemande; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY demande ALTER COLUMN iddemande SET DEFAULT nextval('iddemande_seq'::regclass);


--
-- TOC entry 4121 (class 2604 OID 1684490)
-- Name: gid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY demandefn ALTER COLUMN gid SET DEFAULT nextval('demandefn_gid_seq'::regclass);


--
-- TOC entry 4123 (class 2604 OID 1684492)
-- Name: iddistrict; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY district ALTER COLUMN iddistrict SET DEFAULT nextval('district_id_seq'::regclass);


--
-- TOC entry 4125 (class 2604 OID 1684493)
-- Name: id_document; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY document ALTER COLUMN id_document SET DEFAULT nextval('document_id_document_seq'::regclass);


--
-- TOC entry 4127 (class 2604 OID 1684495)
-- Name: id_paiement; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY fi_paiement_impot ALTER COLUMN id_paiement SET DEFAULT nextval('fi_paiement_impot_id_paiement_seq'::regclass);


--
-- TOC entry 4129 (class 2604 OID 1684496)
-- Name: idfokontany; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY fokontany ALTER COLUMN idfokontany SET DEFAULT nextval('fokontany_id_seq'::regclass);


--
-- TOC entry 4131 (class 2604 OID 1684497)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY groupe ALTER COLUMN id SET DEFAULT nextval('groupe_id_seq'::regclass);


--
-- TOC entry 4133 (class 2604 OID 1684498)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY groupe_acces ALTER COLUMN id SET DEFAULT nextval('groupe_acces_id_seq'::regclass);


--
-- TOC entry 4135 (class 2604 OID 1684499)
-- Name: idhameau; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY hameau ALTER COLUMN idhameau SET DEFAULT nextval('hameau_id_seq'::regclass);


--
-- TOC entry 4137 (class 2604 OID 1684500)
-- Name: idhistorique; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY historique ALTER COLUMN idhistorique SET DEFAULT nextval('historique_idhistorique_seq'::regclass);


--
-- TOC entry 4139 (class 2604 OID 1684501)
-- Name: idhypotheque; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY hypotheque ALTER COLUMN idhypotheque SET DEFAULT nextval('hypotheque_idhypotheque_seq'::regclass);


--
-- TOC entry 4142 (class 2604 OID 1684502)
-- Name: idimpot; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY impot ALTER COLUMN idimpot SET DEFAULT nextval('impot_id_seq'::regclass);


--
-- TOC entry 4144 (class 2604 OID 1684503)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY impot_batiment ALTER COLUMN id SET DEFAULT nextval('impot_batiment_id_seq'::regclass);


--
-- TOC entry 4146 (class 2604 OID 1684504)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY impot_contribuable ALTER COLUMN id SET DEFAULT nextval('impot_contribuable_id_seq'::regclass);


--
-- TOC entry 4148 (class 2604 OID 1684505)
-- Name: id_impotminimum; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY impot_minimum ALTER COLUMN id_impotminimum SET DEFAULT nextval('impot_minimum_id_impotminimum_seq'::regclass);


--
-- TOC entry 4150 (class 2604 OID 1684506)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY impot_parcelle ALTER COLUMN id SET DEFAULT nextval('impot_parcelle_id_seq'::regclass);


--
-- TOC entry 4153 (class 2604 OID 1684507)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY journal ALTER COLUMN id SET DEFAULT nextval('journal_id_seq'::regclass);


--
-- TOC entry 4163 (class 2604 OID 1684509)
-- Name: id_menage; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY menage ALTER COLUMN id_menage SET DEFAULT nextval('menage_id_menage_seq'::regclass);


--
-- TOC entry 4168 (class 2604 OID 1684511)
-- Name: idoperationsubsequente; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY operationsubsequente ALTER COLUMN idoperationsubsequente SET DEFAULT nextval('operationsubsequente_id_seq'::regclass);


--
-- TOC entry 4176 (class 2604 OID 1684513)
-- Name: gid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY parcelle_d ALTER COLUMN gid SET DEFAULT nextval('parcelle_d_id_seq'::regclass);


--
-- TOC entry 4179 (class 2604 OID 1684516)
-- Name: idparcellegrevees; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY parcellegrevees ALTER COLUMN idparcellegrevees SET DEFAULT nextval('parcellegrevees_id_seq'::regclass);


--
-- TOC entry 4185 (class 2604 OID 1684518)
-- Name: idpersonne; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY personne ALTER COLUMN idpersonne SET DEFAULT nextval('personne_idpersonne_seq'::regclass);


--
-- TOC entry 4189 (class 2604 OID 1684519)
-- Name: idpersonnemorale; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY personnemorale ALTER COLUMN idpersonnemorale SET DEFAULT nextval('personnemorale_idpersonnemorale_seq'::regclass);


--
-- TOC entry 4193 (class 2604 OID 1684521)
-- Name: idpointscardinaux; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY pointscardinaux ALTER COLUMN idpointscardinaux SET DEFAULT nextval('pointscardinaux_idpointscardinaux_seq'::regclass);


--
-- TOC entry 4208 (class 2604 OID 1684523)
-- Name: idregion; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY region ALTER COLUMN idregion SET DEFAULT nextval('region_id_seq'::regclass);


--
-- TOC entry 4212 (class 2604 OID 1684524)
-- Name: id_role; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY role_crl ALTER COLUMN id_role SET DEFAULT nextval('role_crl_id_role_seq'::regclass);


--
-- TOC entry 4214 (class 2604 OID 1684525)
-- Name: idservitude; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY servitude ALTER COLUMN idservitude SET DEFAULT nextval('servitude_idservitude_seq'::regclass);


--
-- TOC entry 4218 (class 2604 OID 1684526)
-- Name: idservitude; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY servitudeparcellegrevees ALTER COLUMN idservitude SET DEFAULT nextval('servitudeparcellegrevees_idservitude_seq'::regclass);


--
-- TOC entry 4220 (class 2604 OID 1684527)
-- Name: gid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY terain_status_specifique ALTER COLUMN gid SET DEFAULT nextval('terain_status_specifique_gid_seq'::regclass);


--
-- TOC entry 4222 (class 2604 OID 1684528)
-- Name: gid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY titre ALTER COLUMN gid SET DEFAULT nextval('titre_gid_seq'::regclass);


--
-- TOC entry 4224 (class 2604 OID 1684529)
-- Name: gid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY titrefoncier ALTER COLUMN gid SET DEFAULT nextval('titrefoncier_gid_seq'::regclass);


--
-- TOC entry 4226 (class 2604 OID 1684530)
-- Name: id_type_anomalie; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY type_anomalie ALTER COLUMN id_type_anomalie SET DEFAULT nextval('type_anomalie_id_type_anomalie_seq'::regclass);


--
-- TOC entry 4228 (class 2604 OID 1684531)
-- Name: id_type; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY type_document ALTER COLUMN id_type SET DEFAULT nextval('type_document_id_type_seq'::regclass);


--
-- TOC entry 4230 (class 2604 OID 1684532)
-- Name: idforfaitaire; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY typeforfaitaire ALTER COLUMN idforfaitaire SET DEFAULT nextval('typeforfaitaire_id_seq'::regclass);


--
-- TOC entry 4234 (class 2604 OID 1684533)
-- Name: idtype; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY typepersonnemorale ALTER COLUMN idtype SET DEFAULT nextval('typepersonnemorale_idtype_seq'::regclass);


--
-- TOC entry 4871 (class 0 OID 1683747)
-- Dependencies: 199
-- Data for Name: acces; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY acces (id, nom, libelle, datemaj) FROM stdin;
1	DEMANDE/CREATE	Creation Demande	2024-12-03 09:01:48.101
2	DEMANDE/READ	Consultation Demande	2024-12-03 09:01:48.101
3	DEMANDE/EDIT_INFO	Edition des informations des demandes	2024-12-03 09:01:48.101
4	DEMANDE/EDIT_GEO	Edition des geometries des demandes	2024-12-03 09:01:48.101
5	CERTIFICAT/CREATE	Creation Certificat	2024-12-03 09:01:48.101
6	CERTIFICAT/READ	Consultation Certificat	2024-12-03 09:01:48.101
7	CERTIFICAT/EDIT_INFO	Edition des informations des certificats	2024-12-03 09:01:48.101
8	CERTIFICAT/EDIT_GEO	Edition des geometries des certificats	2024-12-03 09:01:48.101
9	PERSONNE_PHYSIQUE/CREATE	Creation Personne Physique	2024-12-03 09:01:48.101
10	PERSONNE_PHYSIQUE/READ	Consultation Personne Physique	2024-12-03 09:01:48.101
11	PERSONNE_PHYSIQUE/EDIT	Edition Personne Physique	2024-12-03 09:01:48.101
12	PERSONNE_MORALE/CREATE	Creation Personne Morale	2024-12-03 09:01:48.101
13	PERSONNE_MORALE/READ	Consultation Personne Morale	2024-12-03 09:01:48.101
14	PERSONNE_MORALE/EDIT	Edition Personne Morale	2024-12-03 09:01:48.101
15	PERSONNE_MORALE_TYPE/CREATE	Creation Type de Personnes Morales	2024-12-03 09:01:48.101
16	PERSONNE_MORALE_TYPE/READ	Consultation Type de Personnes Morales	2024-12-03 09:01:48.101
17	PERSONNE_MORALE_TYPE/EDIT	Edition Type de Personnes Morales	2024-12-03 09:01:48.101
18	PERSONNE_MORALE_TYPE/DELETE	Supression Type de Personnes Morales	2024-12-03 09:01:48.101
19	KARATANY/PRINT	Impression Karatany	2024-12-03 09:01:48.101
21	CERTIFICAT/ATTESTATION	Attestation Certificat	2024-12-03 09:01:48.101
23	CERTIFICAT/ANNULATION	Annulation Certificat	2024-12-03 09:01:48.101
24	OPERATIONS_SUBSEQUENTES	Operations Subsequentes	2024-12-03 09:01:48.101
25	IMPOT_FONCIER/CREATE	Saisie des Donnees	2024-12-03 09:01:48.101
26	IMPOT_FONCIER/CALCUL	Calcul Impots	2024-12-03 09:01:48.101
27	IMPOT_FONCIER/PARAMETRES	Parametres	2024-12-03 09:01:48.101
28	IMPOT_FONCIER/REGISTRE	Registre des Demandes	2024-12-03 09:01:48.101
29	IMPOT_FONCIER/BENEFICIAIRES	Liste des Beneficiaires	2024-12-03 09:01:48.101
30	IMPOT_FONCIER/AFFICHAGE	Affichage	2024-12-03 09:01:48.101
33	FICHIER/LOAD_PTS_XLS	Charger des points depuis xls	2024-12-03 09:01:48.101
34	FICHIER/LEVE_GPS	Leve parcelle GPS	2024-12-03 09:01:48.101
35	DEMANDE/LISTIN_IMPORT	Import Listing	2024-12-03 09:01:48.101
36	DEMANDE/DATE_ATTRIB	Attribution des dates	2024-12-03 09:01:48.101
37	DEMANDE/OPPOSITION	Signaler Opposition	2024-12-03 09:01:48.101
38	RECONNAISSANCE_LOCALE/EXPORT_RL	Export données pour RL	2024-12-03 09:01:48.101
39	RECONNAISSANCE_LOCALE/IMPORT_RL	Import données après RL	2024-12-03 09:01:48.101
40	CERTIFICAT/TRANSFO_GROUPEE	Transformation groupée	2024-12-03 09:01:48.101
41	CERTIFICAT/ANNULLE	Annulation certificat	2024-12-03 09:01:48.101
42	IMPOT_FONCIER/AUTRES	Autres_Liste des beneficiaires	2024-12-03 09:01:48.101
43	IMPORT_EXPORT/EXPORT_SHAPE	Export shapefile	2024-12-03 09:01:48.101
45	PROJET/ANCIENNE_DONNEES	Anciennes données	2024-12-03 09:01:48.101
46	PROJET/DONNEES_TERRAIN	Données Terrains	2024-12-03 09:01:48.101
47	PROJET/NEW	Nouveau projet	2024-12-03 09:01:48.101
48	PROJET/LIST	Liste des projets	2024-12-03 09:01:48.101
49	PROJET/PARAMS	Paramètres projet	2024-12-03 09:01:48.101
50	PARAMETRES/HAMEAU	Hameau	2024-12-03 09:01:48.101
51	PARAMETRES/CATEGORIE	Categorie	2024-12-03 09:01:48.101
52	PARAMETRES/CONSISTANCE_BAT	Consistance batiment	2024-12-03 09:01:48.101
53	PARAMETRES/TERRITOIRE	Territoires	2024-12-03 09:01:48.101
54	PARAMETRES/CONTENANCE_MAX	Contenance maximale	2024-12-03 09:01:48.101
55	PARAMETRES/BDD	Base de données	2024-12-03 09:01:48.101
56	PARAMETRES/COMPTEUR	Compteur	2024-12-03 09:01:48.101
57	PARAMETRES/BD_VIDE	Créer une base de données vide	2024-12-03 09:01:48.101
58	PARAMETRES/BD_SPLIT	Séparer la base en base de données par commune	2024-12-03 09:01:48.101
59	ETATS/AFFICHAGE	Affichage collectif	2024-12-03 09:01:48.101
60	ETATS/FANAPAHANA	Decision	2024-12-03 09:01:48.101
61	ETATS/ATTESTATION	Attestation	2024-12-03 09:01:48.101
62	ETATS/RP	Registre Parcellaire	2024-12-03 09:01:48.101
63	ETATS/PAGE_OP	Page Operations subsequentes	2024-12-03 09:01:48.101
64	ETATS/RDD	Registre de demande	2024-12-03 09:01:48.101
65	ETATS/AVIS_IMPOSITION	Avis imposition	2024-12-03 09:01:48.101
66	ETATS/CERTIFICAT_AFFICHAGE	Certificat affichage	2024-12-03 09:01:48.101
67	ETATS/LISTING_DEMANDE	Listing Demande	2024-12-03 09:01:48.101
68	ETATS/PVRL	PVRL	2024-12-03 09:01:48.101
69	ETATS/NOMBRE_CF	Nombre de demande et CF	2024-12-03 09:01:48.101
70	ETATS/STATISTIQUES	Statistique	2024-12-03 09:01:48.101
71	INVENTAIRE/IMPORT_DATA	Import Données inventaire	2024-12-03 09:01:48.101
72	INVENTAIRE/FILTRE	Filtre inventaire	2024-12-03 09:01:48.101
73	PLOF/IMPORT_SHAPE	Import Shape PLOF	2024-12-03 09:01:48.101
74	PLOF/IMPORT_DXF	Import Fichier DXF	2024-12-03 09:01:48.101
75	DEMANDE/CREATE_NO_GEOM	Creation Demande sans géometrie	2024-12-03 09:01:48.101
76	IMPORT_EXPORT/IMPORT	Restauration BD	2024-12-03 09:01:48.101
77	IMPORT_EXPORT/EXPORT	Sauvegarde BD	2024-12-03 09:01:48.101
78	TOOL_EDIT/EDIT_GEOM	Edition géometrie sur carte	2024-12-03 09:01:48.101
79	TOOL_EDIT/DEL_GEOM	Supprimer géometrie sur carte	2024-12-03 09:01:48.101
80	BTN/RASTER	Bouton Raster (table des matières)	2024-12-03 09:01:48.101
81	BTN/VECTEUR	Bouton Vecteur (table des matières)	2024-12-03 09:01:48.101
82	BTN/SUPPR	Bouton Supprimer (table des matières)	2024-12-03 09:01:48.101
83	TOOL_EDIT/PARAM_ACCROCHAGE	Paramètres accrochages	2024-12-03 09:01:48.101
84	PROJET_UTILISATEUR/GERER_GROUPE	Gestion des groupes	2024-12-03 09:01:48.101
86	IMPORT_EXPORT/IMPORT_PLOF	Import Plof repertoire	2024-12-03 09:01:48.101
\.


--
-- TOC entry 5125 (class 0 OID 0)
-- Dependencies: 200
-- Name: acces_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('acces_id_seq', 86, true);


--
-- TOC entry 4873 (class 0 OID 1683752)
-- Dependencies: 201
-- Data for Name: actedeces; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY actedeces (idactedeces, numeroactedeces, dateactedeces, numeroactenotoriete, dateactenotoriete, idprojet, lance, datemaj) FROM stdin;
\.


--
-- TOC entry 5126 (class 0 OID 0)
-- Dependencies: 202
-- Name: actedeces_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('actedeces_id_seq', 1, false);


--
-- TOC entry 4875 (class 0 OID 1683758)
-- Dependencies: 203
-- Data for Name: actedecessubsequente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY actedecessubsequente (idactedeces, idoperationsubsequente, datemaj) FROM stdin;
\.


--
-- TOC entry 4877 (class 0 OID 1683763)
-- Dependencies: 205
-- Data for Name: actedejalance; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY actedejalance (id, idacte, typeacte, datemaj) FROM stdin;
\.


--
-- TOC entry 5127 (class 0 OID 0)
-- Dependencies: 204
-- Name: actedj_gid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('actedj_gid_seq', 1569, false);


--
-- TOC entry 4878 (class 0 OID 1683767)
-- Dependencies: 206
-- Data for Name: acteprive; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY acteprive (idacteprive, numeroacteprive, dateenregistrement, datelegalisationsignature, nombreoperation, valeurtransaction, idprojet, lance, datemaj) FROM stdin;
\.


--
-- TOC entry 5128 (class 0 OID 0)
-- Dependencies: 207
-- Name: acteprive_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('acteprive_id_seq', 1, false);


--
-- TOC entry 4880 (class 0 OID 1683773)
-- Dependencies: 208
-- Data for Name: acteprivesubsequente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY acteprivesubsequente (idacteprive, idoperationsubsequente, datemaj) FROM stdin;
\.


--
-- TOC entry 4881 (class 0 OID 1683776)
-- Dependencies: 209
-- Data for Name: actepublic; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY actepublic (idactepublic, dateenregistrement, nomofficierpublic, nombreoperation, idprojet, numeroactepublic, valeurtransaction, lance, datemaj) FROM stdin;
\.


--
-- TOC entry 5129 (class 0 OID 0)
-- Dependencies: 210
-- Name: actepublic_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('actepublic_id_seq', 1, false);


--
-- TOC entry 4883 (class 0 OID 1683786)
-- Dependencies: 211
-- Data for Name: actepublicsubsequente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY actepublicsubsequente (idactepublic, idoperationsubsequente, datemaj) FROM stdin;
\.


--
-- TOC entry 4884 (class 0 OID 1683789)
-- Dependencies: 212
-- Data for Name: aireastatutspecifique; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY aireastatutspecifique (originecontour, nom, type, shape_length, shape_area, idaireastatutspecifique, geom, observation, datemaj) FROM stdin;
\.


--
-- TOC entry 5130 (class 0 OID 0)
-- Dependencies: 213
-- Name: aireastatutspecifique_idaireastatutspecifique_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('aireastatutspecifique_idaireastatutspecifique_seq', 3, true);


--
-- TOC entry 4886 (class 0 OID 1683797)
-- Dependencies: 214
-- Data for Name: anomalie; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY anomalie (idanomalie, id_type_anomalie, description, resolu, csv_iddemande, date_anomalie, csv_id, csv_id_type_anomalie, datemaj, uuid_lr_sys, iddemande) FROM stdin;
\.


--
-- TOC entry 5131 (class 0 OID 0)
-- Dependencies: 215
-- Name: anomalie_idanomalie_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('anomalie_idanomalie_seq', 1, false);


--
-- TOC entry 4888 (class 0 OID 1683805)
-- Dependencies: 216
-- Data for Name: autrecharge; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY autrecharge (type, descriptioncharge, dateinscriptionregistre, idcharge, idparcelle, datemaj, uuid_lr_sys) FROM stdin;
\.


--
-- TOC entry 5132 (class 0 OID 0)
-- Dependencies: 217
-- Name: autrecharge_idcharge_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('autrecharge_idcharge_seq', 16, true);


--
-- TOC entry 4890 (class 0 OID 1683813)
-- Dependencies: 218
-- Data for Name: autrechargesparcelle_d; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY autrechargesparcelle_d (idcharge, idparcelle, datemaj) FROM stdin;
\.


--
-- TOC entry 4891 (class 0 OID 1683816)
-- Dependencies: 219
-- Data for Name: avoir_demande; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY avoir_demande (idpersonne, iddemande, idparcelle, representant, csv_id, datemaj) FROM stdin;
\.


--
-- TOC entry 4892 (class 0 OID 1683819)
-- Dependencies: 220
-- Data for Name: avoir_dmd; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY avoir_dmd (iddemandeur, iddemande, gid, datemaj) FROM stdin;
\.


--
-- TOC entry 4893 (class 0 OID 1683822)
-- Dependencies: 221
-- Data for Name: avoirconjoint; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY avoirconjoint (idconjoint_a, idconjoint_b, datemaj) FROM stdin;
\.


--
-- TOC entry 4894 (class 0 OID 1683825)
-- Dependencies: 222
-- Data for Name: batiment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY batiment (codebatiment, idparcelle, idconsistance, surfacebatiment, nbpiecebatiment, locationbatiment, idcategorie, fi_forfait, idclasse, datemaj) FROM stdin;
\.


--
-- TOC entry 4895 (class 0 OID 1683828)
-- Dependencies: 223
-- Data for Name: beneficiaire; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY beneficiaire (idbeneficiaire, libellebeneficiaire, datemaj) FROM stdin;
\.


--
-- TOC entry 5133 (class 0 OID 0)
-- Dependencies: 224
-- Name: beneficiaire_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('beneficiaire_id_seq', 1, false);


--
-- TOC entry 4897 (class 0 OID 1683836)
-- Dependencies: 225
-- Data for Name: blob_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY blob_history (idpersonne, idutilisateur, old_file, new_file, old_file_type, new_file_type, nature, datemodification, old_file_name, new_file_name, datemaj) FROM stdin;
\.


--
-- TOC entry 4898 (class 0 OID 1683842)
-- Dependencies: 226
-- Data for Name: blob_personne; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY blob_personne (idblob, idpersonne, cin_recto, cin_verso, signature, empreinte_d, empreinte_g, cin_recto_name, cin_recto_type, cin_verso_name, cin_verso_type, signature_name, signature_type, empreinte_d_name, empreinte_d_type, empreinte_g_name, empreinte_g_type, photo_demandeur, photo_demandeur_type, datemaj) FROM stdin;
\.


--
-- TOC entry 5134 (class 0 OID 0)
-- Dependencies: 227
-- Name: blob_personne_idblob_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('blob_personne_idblob_seq', 1, false);


--
-- TOC entry 4900 (class 0 OID 1683850)
-- Dependencies: 228
-- Data for Name: blob_voisin; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY blob_voisin (idpoint, idparcelle, voisin, signature_fic, signature_name, signature_ext, datemaj) FROM stdin;
\.


--
-- TOC entry 4901 (class 0 OID 1683856)
-- Dependencies: 229
-- Data for Name: cadastre; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY cadastre (gid, nom_section, section, parcelle, nom_plan, geom, datemaj) FROM stdin;
\.


--
-- TOC entry 5135 (class 0 OID 0)
-- Dependencies: 230
-- Name: cadastre_gid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('cadastre_gid_seq', 1, false);


--
-- TOC entry 4903 (class 0 OID 1683864)
-- Dependencies: 231
-- Data for Name: categorie; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY categorie (idcategorie, libellecategorie, typeimposition, v_surface, valeur_location_ha, u_surface, v_venale, u_venale, taux, datemaj) FROM stdin;
\.


--
-- TOC entry 5136 (class 0 OID 0)
-- Dependencies: 232
-- Name: categorie_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('categorie_id_seq', 1, false);


--
-- TOC entry 4905 (class 0 OID 1683873)
-- Dependencies: 233
-- Data for Name: categorieforfaitaire; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY categorieforfaitaire (idcategorie, idforfaitaire, descripiton, valeurariary, valeurlocationbatiment, iftifpb, datemaj) FROM stdin;
\.


--
-- TOC entry 4906 (class 0 OID 1683879)
-- Dependencies: 234
-- Data for Name: certificat; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY certificat (numerocertificat, numerodemande, datereconnaissance, typecertificat, datecreation, dateedition, datedelivrance, memo, idcertificat, idfokontany, idprojet, isprint, idcommune, idhameau, code_hameau, datemaj) FROM stdin;
\.


--
-- TOC entry 5137 (class 0 OID 0)
-- Dependencies: 235
-- Name: certificat_idcertificat_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('certificat_idcertificat_seq', 1, false);


--
-- TOC entry 4908 (class 0 OID 1683888)
-- Dependencies: 236
-- Data for Name: classe; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY classe (idclasse, libelleclasse, datemaj) FROM stdin;
1	Classe A                        	2024-12-03 09:01:48.101
2	Classe B                        	2024-12-03 09:01:48.101
3	Classe C                        	2024-12-03 09:01:48.101
4	Classe D                        	2024-12-03 09:01:48.101
5	Classe E                        	2024-12-03 09:01:48.101
\.


--
-- TOC entry 5138 (class 0 OID 0)
-- Dependencies: 237
-- Name: classe_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('classe_id_seq', 1, false);


--
-- TOC entry 4910 (class 0 OID 1683893)
-- Dependencies: 238
-- Data for Name: classecategorieforfaitaire; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY classecategorieforfaitaire (idcategorie, idclasse, iftifpb, valeurariary, debut, fin, unite, datemaj) FROM stdin;
\.


--
-- TOC entry 4911 (class 0 OID 1683896)
-- Dependencies: 239
-- Data for Name: commune; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY commune (idcommune, iddistrict, codecommune, nomcommune, shapelength, shapearea, cptcertificat, cptimport, cptdemande, codeg, csv_id, maire, datemaj) FROM stdin;
\.


--
-- TOC entry 5139 (class 0 OID 0)
-- Dependencies: 240
-- Name: commune_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('commune_id_seq', 1, false);


--
-- TOC entry 4913 (class 0 OID 1683904)
-- Dependencies: 241
-- Data for Name: consistance; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY consistance (idconsistance, libelleconsistance, parcelleoubatiment, valeurariary, valeurariary_ifpb, datemaj) FROM stdin;
8	ALA	ALA                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             	0	0	2024-12-03 09:01:48.101
9	TANIMBOLY	TANIMBOLY                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       	0	0	2024-12-03 09:01:48.101
7	TANIMBARY	TANIMBARY                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       	0	0	2024-12-03 09:01:48.101
\.


--
-- TOC entry 4914 (class 0 OID 1683910)
-- Dependencies: 242
-- Data for Name: consistance_batiment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY consistance_batiment (id, consistance, mombamombanytany, valeurariary, valeur_location, datemaj) FROM stdin;
1	Tafo bozaka	Tafo bozaka	0	0	2024-12-03 09:01:48.101
2	Tafo fanitso	Tafo fanitso	0	0	2024-12-03 09:01:48.101
\.


--
-- TOC entry 5140 (class 0 OID 0)
-- Dependencies: 243
-- Name: consistance_batiment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('consistance_batiment_id_seq', 2, true);


--
-- TOC entry 5141 (class 0 OID 0)
-- Dependencies: 244
-- Name: consistance_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('consistance_id_seq', 9, true);


--
-- TOC entry 4917 (class 0 OID 1683919)
-- Dependencies: 245
-- Data for Name: consistanceforfaitaire; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY consistanceforfaitaire (idconsistance, idforfaitaire, prix, prixaveclocation, iftifpb, datemaj) FROM stdin;
\.


--
-- TOC entry 4919 (class 0 OID 1683924)
-- Dependencies: 247
-- Data for Name: contribuable; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY contribuable (idcontribuable, nom, datenaissance, lieu, cin, hetratany, hetratrano, idfkt, datereglement, prenom, adresse, datecin, numactenaissance, dateactenaissance, lieuactenaissance, sexe, idcontribuableconsorts, lieucin, etatpaiement, montantpayee, nevers, modecalcul, datemaj) FROM stdin;
\.


--
-- TOC entry 5142 (class 0 OID 0)
-- Dependencies: 246
-- Name: contribuable_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('contribuable_id_seq', 12, true);


--
-- TOC entry 4920 (class 0 OID 1683932)
-- Dependencies: 248
-- Data for Name: contribuableconsorts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY contribuableconsorts (idcontribuable, idconsort, datemaj) FROM stdin;
\.


--
-- TOC entry 4921 (class 0 OID 1683935)
-- Dependencies: 249
-- Data for Name: contribuables_parcelle; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY contribuables_parcelle (idpersonne, idparcelle, contribuable, datemaj) FROM stdin;
\.


--
-- TOC entry 5143 (class 0 OID 0)
-- Dependencies: 250
-- Name: crd_gid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('crd_gid_seq', 1569, true);


--
-- TOC entry 5039 (class 0 OID 1686333)
-- Dependencies: 377
-- Data for Name: date_synchro; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY date_synchro (id_synchro, date_synchro, datemaj) FROM stdin;
\.


--
-- TOC entry 5144 (class 0 OID 0)
-- Dependencies: 376
-- Name: date_synchro_id_synchro_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('date_synchro_id_synchro_seq', 1, false);


--
-- TOC entry 4923 (class 0 OID 1683946)
-- Dependencies: 251
-- Data for Name: decisionsubsequente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY decisionsubsequente (idoperationsubsequente, iddecision, datemaj) FROM stdin;
\.


--
-- TOC entry 4924 (class 0 OID 1683949)
-- Dependencies: 252
-- Data for Name: demande; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY demande (iddemande, id, numdemande, nomdemandeur, surface, parcelle, etat_cf, geom, gid, datedemande, datereconnaissance, region, district, commune, fokontany, titre, idfokontany, idcommune, idrejet, cout, consistance, idprojet, numdemandepaps, datedecision, csv_id, code_parcelle, categorie, opposition, planche_plof, charges, numdecision, debut_affichage, fin_affichage, numero_demande_lrsys, pvrl, cqe, date_cqe, resp_cqe, user_cqe, lieudit, collecteur_demande, duree_occupation, origine, avis_crl, texte_crl, sous_reserve, datemaj, num_guichet_foncier, uuid_dossier_lr) FROM stdin;
\.


--
-- TOC entry 4925 (class 0 OID 1683956)
-- Dependencies: 253
-- Data for Name: demande_anomalie; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY demande_anomalie (iddemande, idanomalie, datemaj) FROM stdin;
\.


--
-- TOC entry 4926 (class 0 OID 1683959)
-- Dependencies: 254
-- Data for Name: demande_crl; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY demande_crl (idpersonne, iddemande, id_role, rl, affiche, titulaire, president, datemaj) FROM stdin;
\.


--
-- TOC entry 4928 (class 0 OID 1683965)
-- Dependencies: 256
-- Data for Name: demande_sans_geom; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY demande_sans_geom (iddemande, id, numdemande, nomdemandeur, surface, parcelle, etat_cf, geom, gid, datedemande, datereconnaissance, region, district, commune, fokontany, titre, idfokontany, idcommune, idrejet, cout, consistance, idprojet, numdemandepaps, datedecision, csv_id, code_parcelle, categorie, opposition, planche_plof, charges, datemaj) FROM stdin;
\.


--
-- TOC entry 4929 (class 0 OID 1683981)
-- Dependencies: 257
-- Data for Name: demandefn; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY demandefn (gid, fn_fg, demandeur, sur_plan, geom, datemaj) FROM stdin;
\.


--
-- TOC entry 5145 (class 0 OID 0)
-- Dependencies: 258
-- Name: demandefn_gid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('demandefn_gid_seq', 1, false);


--
-- TOC entry 4931 (class 0 OID 1683997)
-- Dependencies: 259
-- Data for Name: district; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY district (iddistrict, idregion, codedistrict, nomdistrict, shapelength, shapearea, csv_id, datemaj) FROM stdin;
\.


--
-- TOC entry 5146 (class 0 OID 0)
-- Dependencies: 260
-- Name: district_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('district_id_seq', 1, false);


--
-- TOC entry 4933 (class 0 OID 1684002)
-- Dependencies: 261
-- Data for Name: document; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY document (id_document, photo_document, extension_document, num_page, observation, id_type, iddemande, datemaj) FROM stdin;
\.


--
-- TOC entry 5147 (class 0 OID 0)
-- Dependencies: 262
-- Name: document_id_document_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('document_id_document_seq', 1, false);


--
-- TOC entry 4935 (class 0 OID 1684018)
-- Dependencies: 263
-- Data for Name: fi_paiement_impot; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY fi_paiement_impot (id_paiement, date, montant, numquittance, idpersonne, datemaj) FROM stdin;
\.


--
-- TOC entry 5148 (class 0 OID 0)
-- Dependencies: 264
-- Name: fi_paiement_impot_id_paiement_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('fi_paiement_impot_id_paiement_seq', 1, false);


--
-- TOC entry 4937 (class 0 OID 1684023)
-- Dependencies: 265
-- Data for Name: fokontany; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY fokontany (idfokontany, idcommune, codefokontany, nomfokontany, shapelength, shapearea, csv_id, datemaj) FROM stdin;
\.


--
-- TOC entry 5149 (class 0 OID 0)
-- Dependencies: 266
-- Name: fokontany_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('fokontany_id_seq', 1, false);


--
-- TOC entry 4939 (class 0 OID 1684031)
-- Dependencies: 267
-- Data for Name: groupe; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY groupe (id, nom, description, datemaj) FROM stdin;
1	Admin	Administrateur de l'application	2024-12-03 09:01:48.101
5	Responsable Commune	 Responsable des communes	2024-12-03 09:01:48.101
10	Guichet Foncier	 Agent Guichet Foncier	2024-12-03 09:01:48.101
11	Assistants Techniques	Assistants Techniques 	2024-12-03 09:01:48.101
12	Formateur	 Formateur	2024-12-03 09:01:48.101
13	Guichet Unique (TOPO)	 TOPO pour mise à jour PLOF	2024-12-03 09:01:48.101
14	Disposition Transitoire	 Disposition Transitoire	2024-12-03 09:01:48.101
\.


--
-- TOC entry 4940 (class 0 OID 1684037)
-- Dependencies: 268
-- Data for Name: groupe_acces; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY groupe_acces (id, groupe_id, acces_id, autorise, datemaj) FROM stdin;
188	10	3	t	2024-12-03 09:01:48.101
189	10	4	t	2024-12-03 09:01:48.101
22	5	2	t	2024-12-03 09:01:48.101
23	5	3	f	2024-12-03 09:01:48.101
24	5	4	f	2024-12-03 09:01:48.101
135	5	35	f	2024-12-03 09:01:48.101
136	5	36	f	2024-12-03 09:01:48.101
137	5	37	f	2024-12-03 09:01:48.101
144	5	75	f	2024-12-03 09:01:48.101
30	5	6	t	2024-12-03 09:01:48.101
31	5	7	f	2024-12-03 09:01:48.101
32	5	8	f	2024-12-03 09:01:48.101
124	5	21	t	2024-12-03 09:01:48.101
125	5	23	f	2024-12-03 09:01:48.101
138	5	40	f	2024-12-03 09:01:48.101
139	5	41	f	2024-12-03 09:01:48.101
33	5	9	f	2024-12-03 09:01:48.101
34	5	10	f	2024-12-03 09:01:48.101
35	5	11	f	2024-12-03 09:01:48.101
36	5	12	f	2024-12-03 09:01:48.101
37	5	13	f	2024-12-03 09:01:48.101
38	5	14	f	2024-12-03 09:01:48.101
53	5	15	f	2024-12-03 09:01:48.101
54	5	16	f	2024-12-03 09:01:48.101
55	5	17	f	2024-12-03 09:01:48.101
56	5	18	f	2024-12-03 09:01:48.101
57	5	19	f	2024-12-03 09:01:48.101
126	5	24	f	2024-12-03 09:01:48.101
127	5	25	f	2024-12-03 09:01:48.101
128	5	26	f	2024-12-03 09:01:48.101
129	5	27	f	2024-12-03 09:01:48.101
130	5	28	f	2024-12-03 09:01:48.101
131	5	29	t	2024-12-03 09:01:48.101
132	5	30	f	2024-12-03 09:01:48.101
145	5	42	f	2024-12-03 09:01:48.101
141	5	34	f	2024-12-03 09:01:48.101
142	5	38	f	2024-12-03 09:01:48.101
143	5	39	f	2024-12-03 09:01:48.101
146	5	43	t	2024-12-03 09:01:48.101
190	10	35	t	2024-12-03 09:01:48.101
191	10	36	t	2024-12-03 09:01:48.101
192	10	37	t	2024-12-03 09:01:48.101
193	10	75	t	2024-12-03 09:01:48.101
194	10	5	t	2024-12-03 09:01:48.101
195	10	6	t	2024-12-03 09:01:48.101
198	10	21	t	2024-12-03 09:01:48.101
199	10	23	f	2024-12-03 09:01:48.101
200	10	40	t	2024-12-03 09:01:48.101
201	10	41	f	2024-12-03 09:01:48.101
202	10	9	t	2024-12-03 09:01:48.101
203	10	10	t	2024-12-03 09:01:48.101
204	10	11	t	2024-12-03 09:01:48.101
205	10	12	t	2024-12-03 09:01:48.101
206	10	13	t	2024-12-03 09:01:48.101
207	10	14	t	2024-12-03 09:01:48.101
208	10	15	t	2024-12-03 09:01:48.101
209	10	16	t	2024-12-03 09:01:48.101
210	10	17	t	2024-12-03 09:01:48.101
211	10	18	t	2024-12-03 09:01:48.101
213	10	24	t	2024-12-03 09:01:48.101
214	10	25	t	2024-12-03 09:01:48.101
215	10	26	t	2024-12-03 09:01:48.101
216	10	27	t	2024-12-03 09:01:48.101
217	10	28	t	2024-12-03 09:01:48.101
218	10	29	t	2024-12-03 09:01:48.101
219	10	30	t	2024-12-03 09:01:48.101
220	10	42	t	2024-12-03 09:01:48.101
221	10	33	t	2024-12-03 09:01:48.101
222	10	34	t	2024-12-03 09:01:48.101
223	10	38	t	2024-12-03 09:01:48.101
224	10	39	t	2024-12-03 09:01:48.101
225	10	43	t	2024-12-03 09:01:48.101
226	10	76	t	2024-12-03 09:01:48.101
228	10	45	f	2024-12-03 09:01:48.101
229	10	46	f	2024-12-03 09:01:48.101
230	10	47	t	2024-12-03 09:01:48.101
231	10	48	t	2024-12-03 09:01:48.101
232	10	49	t	2024-12-03 09:01:48.101
233	10	50	t	2024-12-03 09:01:48.101
234	10	51	t	2024-12-03 09:01:48.101
235	10	52	t	2024-12-03 09:01:48.101
236	10	53	t	2024-12-03 09:01:48.101
237	10	54	f	2024-12-03 09:01:48.101
238	10	55	t	2024-12-03 09:01:48.101
239	10	56	t	2024-12-03 09:01:48.101
21	5	1	f	2024-12-03 09:01:48.101
29	5	5	f	2024-12-03 09:01:48.101
140	5	33	f	2024-12-03 09:01:48.101
147	5	76	f	2024-12-03 09:01:48.101
148	5	77	f	2024-12-03 09:01:48.101
149	5	45	f	2024-12-03 09:01:48.101
151	5	47	f	2024-12-03 09:01:48.101
152	5	48	f	2024-12-03 09:01:48.101
153	5	49	f	2024-12-03 09:01:48.101
154	5	50	f	2024-12-03 09:01:48.101
155	5	51	f	2024-12-03 09:01:48.101
156	5	52	f	2024-12-03 09:01:48.101
157	5	53	f	2024-12-03 09:01:48.101
158	5	54	f	2024-12-03 09:01:48.101
159	5	55	f	2024-12-03 09:01:48.101
160	5	56	f	2024-12-03 09:01:48.101
161	5	57	f	2024-12-03 09:01:48.101
162	5	58	f	2024-12-03 09:01:48.101
163	5	59	f	2024-12-03 09:01:48.101
164	5	60	f	2024-12-03 09:01:48.101
166	5	62	f	2024-12-03 09:01:48.101
167	5	63	f	2024-12-03 09:01:48.101
168	5	64	f	2024-12-03 09:01:48.101
169	5	65	t	2024-12-03 09:01:48.101
170	5	66	f	2024-12-03 09:01:48.101
171	5	67	f	2024-12-03 09:01:48.101
172	5	68	f	2024-12-03 09:01:48.101
173	5	69	t	2024-12-03 09:01:48.101
174	5	70	f	2024-12-03 09:01:48.101
175	5	71	f	2024-12-03 09:01:48.101
176	5	72	f	2024-12-03 09:01:48.101
177	5	73	f	2024-12-03 09:01:48.101
178	5	74	f	2024-12-03 09:01:48.101
179	5	78	f	2024-12-03 09:01:48.101
181	5	83	f	2024-12-03 09:01:48.101
182	5	80	f	2024-12-03 09:01:48.101
183	5	81	f	2024-12-03 09:01:48.101
184	5	82	f	2024-12-03 09:01:48.101
185	5	84	f	2024-12-03 09:01:48.101
187	10	2	t	2024-12-03 09:01:48.101
242	10	59	t	2024-12-03 09:01:48.101
243	10	60	t	2024-12-03 09:01:48.101
244	10	61	t	2024-12-03 09:01:48.101
245	10	62	t	2024-12-03 09:01:48.101
246	10	63	t	2024-12-03 09:01:48.101
247	10	64	t	2024-12-03 09:01:48.101
248	10	65	t	2024-12-03 09:01:48.101
249	10	66	t	2024-12-03 09:01:48.101
250	10	67	t	2024-12-03 09:01:48.101
251	10	68	t	2024-12-03 09:01:48.101
252	10	69	t	2024-12-03 09:01:48.101
253	10	70	f	2024-12-03 09:01:48.101
254	10	71	f	2024-12-03 09:01:48.101
255	10	72	f	2024-12-03 09:01:48.101
256	10	73	f	2024-12-03 09:01:48.101
257	10	74	f	2024-12-03 09:01:48.101
258	10	78	f	2024-12-03 09:01:48.101
259	10	79	f	2024-12-03 09:01:48.101
260	10	83	f	2024-12-03 09:01:48.101
261	10	80	f	2024-12-03 09:01:48.101
262	10	81	f	2024-12-03 09:01:48.101
263	10	82	f	2024-12-03 09:01:48.101
264	10	84	t	2024-12-03 09:01:48.101
265	11	1	t	2024-12-03 09:01:48.101
266	11	2	t	2024-12-03 09:01:48.101
267	11	3	t	2024-12-03 09:01:48.101
268	11	4	t	2024-12-03 09:01:48.101
269	11	35	t	2024-12-03 09:01:48.101
270	11	36	t	2024-12-03 09:01:48.101
271	11	37	t	2024-12-03 09:01:48.101
272	11	75	t	2024-12-03 09:01:48.101
273	11	5	t	2024-12-03 09:01:48.101
274	11	6	t	2024-12-03 09:01:48.101
275	11	7	t	2024-12-03 09:01:48.101
276	11	8	t	2024-12-03 09:01:48.101
277	11	21	t	2024-12-03 09:01:48.101
278	11	23	f	2024-12-03 09:01:48.101
279	11	40	t	2024-12-03 09:01:48.101
280	11	41	f	2024-12-03 09:01:48.101
281	11	9	t	2024-12-03 09:01:48.101
282	11	10	t	2024-12-03 09:01:48.101
283	11	11	t	2024-12-03 09:01:48.101
284	11	12	t	2024-12-03 09:01:48.101
285	11	13	t	2024-12-03 09:01:48.101
286	11	14	t	2024-12-03 09:01:48.101
287	11	15	t	2024-12-03 09:01:48.101
288	11	16	t	2024-12-03 09:01:48.101
289	11	17	t	2024-12-03 09:01:48.101
290	11	18	t	2024-12-03 09:01:48.101
291	11	19	t	2024-12-03 09:01:48.101
292	11	24	f	2024-12-03 09:01:48.101
293	11	25	f	2024-12-03 09:01:48.101
294	11	26	f	2024-12-03 09:01:48.101
295	11	27	f	2024-12-03 09:01:48.101
296	11	28	f	2024-12-03 09:01:48.101
297	11	29	f	2024-12-03 09:01:48.101
298	11	30	f	2024-12-03 09:01:48.101
299	11	42	f	2024-12-03 09:01:48.101
300	11	33	t	2024-12-03 09:01:48.101
301	11	34	t	2024-12-03 09:01:48.101
302	11	38	t	2024-12-03 09:01:48.101
303	11	39	t	2024-12-03 09:01:48.101
304	11	43	t	2024-12-03 09:01:48.101
305	11	76	t	2024-12-03 09:01:48.101
306	11	77	t	2024-12-03 09:01:48.101
307	11	45	t	2024-12-03 09:01:48.101
308	11	46	t	2024-12-03 09:01:48.101
309	11	47	t	2024-12-03 09:01:48.101
310	11	48	t	2024-12-03 09:01:48.101
311	11	49	t	2024-12-03 09:01:48.101
312	11	50	t	2024-12-03 09:01:48.101
313	11	51	t	2024-12-03 09:01:48.101
314	11	52	f	2024-12-03 09:01:48.101
315	11	53	t	2024-12-03 09:01:48.101
316	11	54	f	2024-12-03 09:01:48.101
317	11	55	t	2024-12-03 09:01:48.101
318	11	56	t	2024-12-03 09:01:48.101
319	11	57	t	2024-12-03 09:01:48.101
320	11	58	t	2024-12-03 09:01:48.101
321	11	59	t	2024-12-03 09:01:48.101
322	11	60	t	2024-12-03 09:01:48.101
323	11	61	t	2024-12-03 09:01:48.101
324	11	62	t	2024-12-03 09:01:48.101
325	11	63	t	2024-12-03 09:01:48.101
326	11	64	t	2024-12-03 09:01:48.101
327	11	65	t	2024-12-03 09:01:48.101
328	11	66	t	2024-12-03 09:01:48.101
329	11	67	t	2024-12-03 09:01:48.101
330	11	68	t	2024-12-03 09:01:48.101
331	11	69	t	2024-12-03 09:01:48.101
332	11	70	f	2024-12-03 09:01:48.101
333	11	71	t	2024-12-03 09:01:48.101
334	11	72	t	2024-12-03 09:01:48.101
335	11	73	t	2024-12-03 09:01:48.101
336	11	74	f	2024-12-03 09:01:48.101
337	11	78	t	2024-12-03 09:01:48.101
338	11	79	t	2024-12-03 09:01:48.101
339	11	83	f	2024-12-03 09:01:48.101
340	11	80	t	2024-12-03 09:01:48.101
341	11	81	t	2024-12-03 09:01:48.101
342	11	82	t	2024-12-03 09:01:48.101
343	11	84	f	2024-12-03 09:01:48.101
345	12	2	t	2024-12-03 09:01:48.101
346	12	3	t	2024-12-03 09:01:48.101
212	10	19	t	2024-12-03 09:01:48.101
227	10	77	t	2024-12-03 09:01:48.101
241	10	58	f	2024-12-03 09:01:48.101
347	12	4	t	2024-12-03 09:01:48.101
348	12	35	t	2024-12-03 09:01:48.101
349	12	36	t	2024-12-03 09:01:48.101
350	12	37	t	2024-12-03 09:01:48.101
351	12	75	t	2024-12-03 09:01:48.101
352	12	5	t	2024-12-03 09:01:48.101
353	12	6	t	2024-12-03 09:01:48.101
354	12	7	t	2024-12-03 09:01:48.101
355	12	8	t	2024-12-03 09:01:48.101
356	12	21	t	2024-12-03 09:01:48.101
357	12	23	f	2024-12-03 09:01:48.101
358	12	40	t	2024-12-03 09:01:48.101
360	12	9	t	2024-12-03 09:01:48.101
361	12	10	t	2024-12-03 09:01:48.101
362	12	11	t	2024-12-03 09:01:48.101
363	12	12	t	2024-12-03 09:01:48.101
364	12	13	t	2024-12-03 09:01:48.101
344	12	1	t	2024-12-03 09:01:48.101
197	10	8	f	2024-12-03 09:01:48.101
368	12	17	t	2024-12-03 09:01:48.101
369	12	18	t	2024-12-03 09:01:48.101
370	12	19	t	2024-12-03 09:01:48.101
371	12	24	t	2024-12-03 09:01:48.101
372	12	25	t	2024-12-03 09:01:48.101
373	12	26	t	2024-12-03 09:01:48.101
427	13	35	f	2024-12-03 09:01:48.101
428	13	36	f	2024-12-03 09:01:48.101
429	13	37	f	2024-12-03 09:01:48.101
430	13	75	f	2024-12-03 09:01:48.101
431	13	5	f	2024-12-03 09:01:48.101
432	13	6	t	2024-12-03 09:01:48.101
433	13	7	f	2024-12-03 09:01:48.101
434	13	8	f	2024-12-03 09:01:48.101
435	13	21	f	2024-12-03 09:01:48.101
436	13	23	f	2024-12-03 09:01:48.101
437	13	40	f	2024-12-03 09:01:48.101
438	13	41	f	2024-12-03 09:01:48.101
439	13	9	f	2024-12-03 09:01:48.101
440	13	10	f	2024-12-03 09:01:48.101
442	13	12	f	2024-12-03 09:01:48.101
443	13	13	f	2024-12-03 09:01:48.101
444	13	14	f	2024-12-03 09:01:48.101
445	13	15	f	2024-12-03 09:01:48.101
446	13	16	f	2024-12-03 09:01:48.101
447	13	17	f	2024-12-03 09:01:48.101
448	13	18	f	2024-12-03 09:01:48.101
449	13	19	f	2024-12-03 09:01:48.101
450	13	24	f	2024-12-03 09:01:48.101
451	13	25	f	2024-12-03 09:01:48.101
452	13	26	f	2024-12-03 09:01:48.101
453	13	27	f	2024-12-03 09:01:48.101
454	13	28	f	2024-12-03 09:01:48.101
455	13	29	f	2024-12-03 09:01:48.101
457	13	42	f	2024-12-03 09:01:48.101
458	13	33	f	2024-12-03 09:01:48.101
459	13	34	f	2024-12-03 09:01:48.101
460	13	38	f	2024-12-03 09:01:48.101
461	13	39	f	2024-12-03 09:01:48.101
462	13	43	t	2024-12-03 09:01:48.101
463	13	76	f	2024-12-03 09:01:48.101
464	13	77	t	2024-12-03 09:01:48.101
465	13	45	f	2024-12-03 09:01:48.101
466	13	46	f	2024-12-03 09:01:48.101
467	13	47	f	2024-12-03 09:01:48.101
468	13	48	t	2024-12-03 09:01:48.101
469	13	49	f	2024-12-03 09:01:48.101
470	13	50	f	2024-12-03 09:01:48.101
472	13	52	f	2024-12-03 09:01:48.101
473	13	53	f	2024-12-03 09:01:48.101
474	13	54	f	2024-12-03 09:01:48.101
475	13	55	t	2024-12-03 09:01:48.101
476	13	56	f	2024-12-03 09:01:48.101
477	13	57	f	2024-12-03 09:01:48.101
478	13	58	f	2024-12-03 09:01:48.101
479	13	59	f	2024-12-03 09:01:48.101
480	13	60	f	2024-12-03 09:01:48.101
481	13	61	f	2024-12-03 09:01:48.101
482	13	62	f	2024-12-03 09:01:48.101
483	13	63	f	2024-12-03 09:01:48.101
484	13	64	f	2024-12-03 09:01:48.101
485	13	65	f	2024-12-03 09:01:48.101
487	13	67	f	2024-12-03 09:01:48.101
488	13	68	f	2024-12-03 09:01:48.101
489	13	69	t	2024-12-03 09:01:48.101
490	13	70	t	2024-12-03 09:01:48.101
491	13	71	f	2024-12-03 09:01:48.101
492	13	72	f	2024-12-03 09:01:48.101
493	13	73	t	2024-12-03 09:01:48.101
494	13	74	t	2024-12-03 09:01:48.101
495	13	78	f	2024-12-03 09:01:48.101
496	13	79	f	2024-12-03 09:01:48.101
497	13	83	f	2024-12-03 09:01:48.101
498	13	80	t	2024-12-03 09:01:48.101
499	13	81	t	2024-12-03 09:01:48.101
500	13	82	t	2024-12-03 09:01:48.101
367	12	16	t	2024-12-03 09:01:48.101
374	12	27	t	2024-12-03 09:01:48.101
375	12	28	t	2024-12-03 09:01:48.101
376	12	29	t	2024-12-03 09:01:48.101
377	12	30	t	2024-12-03 09:01:48.101
378	12	42	t	2024-12-03 09:01:48.101
379	12	33	t	2024-12-03 09:01:48.101
380	12	34	t	2024-12-03 09:01:48.101
381	12	38	t	2024-12-03 09:01:48.101
382	12	39	t	2024-12-03 09:01:48.101
383	12	43	t	2024-12-03 09:01:48.101
384	12	76	t	2024-12-03 09:01:48.101
385	12	77	t	2024-12-03 09:01:48.101
387	12	46	t	2024-12-03 09:01:48.101
388	12	47	t	2024-12-03 09:01:48.101
389	12	48	t	2024-12-03 09:01:48.101
390	12	49	t	2024-12-03 09:01:48.101
391	12	50	t	2024-12-03 09:01:48.101
392	12	51	t	2024-12-03 09:01:48.101
393	12	52	t	2024-12-03 09:01:48.101
394	12	53	t	2024-12-03 09:01:48.101
395	12	54	t	2024-12-03 09:01:48.101
396	12	55	t	2024-12-03 09:01:48.101
397	12	56	t	2024-12-03 09:01:48.101
398	12	57	t	2024-12-03 09:01:48.101
399	12	58	t	2024-12-03 09:01:48.101
400	12	59	t	2024-12-03 09:01:48.101
402	12	61	t	2024-12-03 09:01:48.101
403	12	62	t	2024-12-03 09:01:48.101
404	12	63	t	2024-12-03 09:01:48.101
405	12	64	t	2024-12-03 09:01:48.101
406	12	65	t	2024-12-03 09:01:48.101
407	12	66	t	2024-12-03 09:01:48.101
408	12	67	t	2024-12-03 09:01:48.101
409	12	68	t	2024-12-03 09:01:48.101
410	12	69	t	2024-12-03 09:01:48.101
411	12	70	t	2024-12-03 09:01:48.101
412	12	71	t	2024-12-03 09:01:48.101
413	12	72	t	2024-12-03 09:01:48.101
414	12	73	t	2024-12-03 09:01:48.101
415	12	74	t	2024-12-03 09:01:48.101
417	12	79	t	2024-12-03 09:01:48.101
418	12	83	f	2024-12-03 09:01:48.101
419	12	80	t	2024-12-03 09:01:48.101
420	12	81	t	2024-12-03 09:01:48.101
421	12	82	t	2024-12-03 09:01:48.101
422	12	84	f	2024-12-03 09:01:48.101
424	13	2	t	2024-12-03 09:01:48.101
366	12	15	t	2024-12-03 09:01:48.101
425	13	3	f	2024-12-03 09:01:48.101
544	14	45	t	2024-12-03 09:01:48.101
502	14	1	t	2024-12-03 09:01:48.101
503	14	2	t	2024-12-03 09:01:48.101
504	14	3	t	2024-12-03 09:01:48.101
505	14	4	t	2024-12-03 09:01:48.101
506	14	35	t	2024-12-03 09:01:48.101
507	14	36	t	2024-12-03 09:01:48.101
508	14	37	t	2024-12-03 09:01:48.101
523	14	14	t	2024-12-03 09:01:48.101
524	14	15	t	2024-12-03 09:01:48.101
525	14	16	t	2024-12-03 09:01:48.101
526	14	17	t	2024-12-03 09:01:48.101
527	14	18	t	2024-12-03 09:01:48.101
528	14	19	t	2024-12-03 09:01:48.101
530	14	25	f	2024-12-03 09:01:48.101
531	14	26	f	2024-12-03 09:01:48.101
532	14	27	f	2024-12-03 09:01:48.101
533	14	28	f	2024-12-03 09:01:48.101
534	14	29	f	2024-12-03 09:01:48.101
535	14	30	f	2024-12-03 09:01:48.101
536	14	42	f	2024-12-03 09:01:48.101
537	14	33	t	2024-12-03 09:01:48.101
538	14	34	t	2024-12-03 09:01:48.101
539	14	38	t	2024-12-03 09:01:48.101
540	14	39	t	2024-12-03 09:01:48.101
541	14	43	t	2024-12-03 09:01:48.101
542	14	76	t	2024-12-03 09:01:48.101
543	14	77	t	2024-12-03 09:01:48.101
545	14	46	t	2024-12-03 09:01:48.101
546	14	47	t	2024-12-03 09:01:48.101
547	14	48	t	2024-12-03 09:01:48.101
548	14	49	t	2024-12-03 09:01:48.101
549	14	50	t	2024-12-03 09:01:48.101
550	14	51	t	2024-12-03 09:01:48.101
551	14	52	f	2024-12-03 09:01:48.101
552	14	53	t	2024-12-03 09:01:48.101
553	14	54	f	2024-12-03 09:01:48.101
554	14	55	t	2024-12-03 09:01:48.101
555	14	56	t	2024-12-03 09:01:48.101
556	14	57	t	2024-12-03 09:01:48.101
557	14	58	f	2024-12-03 09:01:48.101
558	14	59	t	2024-12-03 09:01:48.101
559	14	60	t	2024-12-03 09:01:48.101
560	14	61	t	2024-12-03 09:01:48.101
561	14	62	t	2024-12-03 09:01:48.101
562	14	63	t	2024-12-03 09:01:48.101
563	14	64	t	2024-12-03 09:01:48.101
564	14	65	f	2024-12-03 09:01:48.101
565	14	66	t	2024-12-03 09:01:48.101
566	14	67	t	2024-12-03 09:01:48.101
567	14	68	t	2024-12-03 09:01:48.101
568	14	69	t	2024-12-03 09:01:48.101
569	14	70	t	2024-12-03 09:01:48.101
570	14	71	t	2024-12-03 09:01:48.101
571	14	72	t	2024-12-03 09:01:48.101
572	14	73	t	2024-12-03 09:01:48.101
573	14	74	t	2024-12-03 09:01:48.101
574	14	78	t	2024-12-03 09:01:48.101
575	14	79	t	2024-12-03 09:01:48.101
576	14	83	t	2024-12-03 09:01:48.101
577	14	80	t	2024-12-03 09:01:48.101
578	14	81	t	2024-12-03 09:01:48.101
579	14	82	t	2024-12-03 09:01:48.101
580	14	84	f	2024-12-03 09:01:48.101
150	5	46	f	2024-12-03 09:01:48.101
165	5	61	f	2024-12-03 09:01:48.101
180	5	79	f	2024-12-03 09:01:48.101
186	10	1	t	2024-12-03 09:01:48.101
240	10	57	t	2024-12-03 09:01:48.101
509	14	75	t	2024-12-03 09:01:48.101
510	14	5	t	2024-12-03 09:01:48.101
511	14	6	t	2024-12-03 09:01:48.101
512	14	7	t	2024-12-03 09:01:48.101
513	14	8	t	2024-12-03 09:01:48.101
359	12	41	f	2024-12-03 09:01:48.101
365	12	14	t	2024-12-03 09:01:48.101
386	12	45	t	2024-12-03 09:01:48.101
401	12	60	t	2024-12-03 09:01:48.101
416	12	78	t	2024-12-03 09:01:48.101
423	13	1	f	2024-12-03 09:01:48.101
426	13	4	f	2024-12-03 09:01:48.101
441	13	11	f	2024-12-03 09:01:48.101
456	13	30	f	2024-12-03 09:01:48.101
471	13	51	f	2024-12-03 09:01:48.101
486	13	66	f	2024-12-03 09:01:48.101
501	13	84	f	2024-12-03 09:01:48.101
514	14	21	t	2024-12-03 09:01:48.101
515	14	23	f	2024-12-03 09:01:48.101
516	14	40	t	2024-12-03 09:01:48.101
517	14	41	f	2024-12-03 09:01:48.101
518	14	9	t	2024-12-03 09:01:48.101
519	14	10	t	2024-12-03 09:01:48.101
520	14	11	t	2024-12-03 09:01:48.101
521	14	12	t	2024-12-03 09:01:48.101
522	14	13	t	2024-12-03 09:01:48.101
529	14	24	t	2024-12-03 09:01:48.101
581	14	86	t	2024-12-03 09:01:48.101
196	10	7	t	2024-12-03 09:01:48.101
\.


--
-- TOC entry 5150 (class 0 OID 0)
-- Dependencies: 269
-- Name: groupe_acces_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('groupe_acces_id_seq', 581, true);


--
-- TOC entry 5151 (class 0 OID 0)
-- Dependencies: 270
-- Name: groupe_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('groupe_id_seq', 14, true);


--
-- TOC entry 4943 (class 0 OID 1684044)
-- Dependencies: 271
-- Data for Name: hameau; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY hameau (idhameau, idfokontany, codehameau, nomhameau, shapelength, shapearea, csv_id, datemaj) FROM stdin;
\.


--
-- TOC entry 5152 (class 0 OID 0)
-- Dependencies: 272
-- Name: hameau_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('hameau_id_seq', 1, false);


--
-- TOC entry 4945 (class 0 OID 1684049)
-- Dependencies: 273
-- Data for Name: historique; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY historique (idhistorique, typeoperation, dateoperation, idcertificat, datemaj) FROM stdin;
\.


--
-- TOC entry 5153 (class 0 OID 0)
-- Dependencies: 274
-- Name: historique_idhistorique_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('historique_idhistorique_seq', 45, true);


--
-- TOC entry 4947 (class 0 OID 1684054)
-- Dependencies: 275
-- Data for Name: hypotheque; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY hypotheque (dateinscriptionregistre, duree, valeur, creancier, descriptionhypotheque, dateradiation, idhypotheque, datemaj) FROM stdin;
\.


--
-- TOC entry 5154 (class 0 OID 0)
-- Dependencies: 276
-- Name: hypotheque_idhypotheque_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('hypotheque_idhypotheque_seq', 6, true);


--
-- TOC entry 4949 (class 0 OID 1684062)
-- Dependencies: 277
-- Data for Name: hypothequeparcelle_d; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY hypothequeparcelle_d (idhypotheque, idparcelle, datemaj) FROM stdin;
\.


--
-- TOC entry 5155 (class 0 OID 0)
-- Dependencies: 278
-- Name: iddemande_sans_geom_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('iddemande_sans_geom_seq', 5241, false);


--
-- TOC entry 5156 (class 0 OID 0)
-- Dependencies: 255
-- Name: iddemande_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('iddemande_seq', 1, false);


--
-- TOC entry 5157 (class 0 OID 0)
-- Dependencies: 279
-- Name: idprojet_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('idprojet_seq', 1, false);


--
-- TOC entry 4952 (class 0 OID 1684069)
-- Dependencies: 280
-- Data for Name: impot; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY impot (idimpot, numquittanceimpot, anneeimpot, dateimpot, datemaj) FROM stdin;
\.


--
-- TOC entry 4953 (class 0 OID 1684072)
-- Dependencies: 281
-- Data for Name: impot_batiment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY impot_batiment (id, hetratrano, annee, codebatiment, montant_paye, datemaj) FROM stdin;
\.


--
-- TOC entry 5158 (class 0 OID 0)
-- Dependencies: 282
-- Name: impot_batiment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('impot_batiment_id_seq', 1, false);


--
-- TOC entry 4955 (class 0 OID 1684077)
-- Dependencies: 283
-- Data for Name: impot_contribuable; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY impot_contribuable (id, hetratrano, hetratany, etatpaiement, annee, datereglement, montantpaye, idpersonne, datemaj) FROM stdin;
\.


--
-- TOC entry 5159 (class 0 OID 0)
-- Dependencies: 284
-- Name: impot_contribuable_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('impot_contribuable_id_seq', 1, false);


--
-- TOC entry 5160 (class 0 OID 0)
-- Dependencies: 285
-- Name: impot_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('impot_id_seq', 1, false);


--
-- TOC entry 4958 (class 0 OID 1684084)
-- Dependencies: 286
-- Data for Name: impot_minimum; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY impot_minimum (id_impotminimum, type, valeur, annee, datemaj) FROM stdin;
\.


--
-- TOC entry 5161 (class 0 OID 0)
-- Dependencies: 287
-- Name: impot_minimum_id_impotminimum_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('impot_minimum_id_impotminimum_seq', 1, false);


--
-- TOC entry 4960 (class 0 OID 1684092)
-- Dependencies: 288
-- Data for Name: impot_parcelle; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY impot_parcelle (id, hetratany, annee, idparcelle, montant_paye, datemaj) FROM stdin;
\.


--
-- TOC entry 5162 (class 0 OID 0)
-- Dependencies: 289
-- Name: impot_parcelle_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('impot_parcelle_id_seq', 1, false);


--
-- TOC entry 4962 (class 0 OID 1684097)
-- Dependencies: 290
-- Data for Name: impotparcelle; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY impotparcelle (idparcelle, idimpot, etatpaiement, montantpayee, datemaj) FROM stdin;
\.


--
-- TOC entry 4963 (class 0 OID 1684100)
-- Dependencies: 291
-- Data for Name: journal; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY journal (id, idutilisateur, idobjetcible, typeobjectcible, description, dateaction, heureaction, datemaj) FROM stdin;
\.


--
-- TOC entry 5163 (class 0 OID 0)
-- Dependencies: 292
-- Name: journal_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('journal_id_seq', 524, true);


--
-- TOC entry 5164 (class 0 OID 0)
-- Dependencies: 293
-- Name: limcomm_gid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('limcomm_gid_seq', 1, true);


--
-- TOC entry 5165 (class 0 OID 0)
-- Dependencies: 294
-- Name: limcommanjozorobe_gid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('limcommanjozorobe_gid_seq', 18, true);


--
-- TOC entry 4967 (class 0 OID 1684109)
-- Dependencies: 295
-- Data for Name: limitesparcelle; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY limitesparcelle (idpointscardinaux, idparcelle, description, path_file, datemaj) FROM stdin;
\.


--
-- TOC entry 4968 (class 0 OID 1684123)
-- Dependencies: 296
-- Data for Name: menage; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY menage (id_menage, code_menage, nombre_homme, nombre_femme, nombre_enfant, nombre_homme_actif, nombre_femme_active, possede_terre, acces_ressource, datemaj) FROM stdin;
\.


--
-- TOC entry 5166 (class 0 OID 0)
-- Dependencies: 297
-- Name: menage_id_menage_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('menage_id_menage_seq', 1, false);


--
-- TOC entry 4970 (class 0 OID 1684135)
-- Dependencies: 298
-- Data for Name: migration_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY migration_history (filename, migration_date, datemaj) FROM stdin;
sql/2024-11-19-DROPTABLEIFEXISTS.sql	2024-12-03 09:01:49.382	2024-12-03 09:01:49.382
\.


--
-- TOC entry 4972 (class 0 OID 1684148)
-- Dependencies: 300
-- Data for Name: operationsub; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY operationsub (id, typeacte, idacte, idcf, datedepot, dateinscription, cout, cout2, datemaj) FROM stdin;
18846	0	1	\N	\N	\N	\N	\N	2024-12-03 09:01:48.101
18847	0	2	\N	\N	\N	\N	\N	2024-12-03 09:01:48.101
18848	3	3	\N	\N	\N	\N	\N	2024-12-03 09:01:48.101
18849	0	1	\N	\N	\N	\N	\N	2024-12-03 09:01:48.101
18850	3	1	\N	\N	\N	\N	\N	2024-12-03 09:01:48.101
\.


--
-- TOC entry 5167 (class 0 OID 0)
-- Dependencies: 299
-- Name: operationsub_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('operationsub_id_seq', 18850, true);


--
-- TOC entry 4973 (class 0 OID 1684152)
-- Dependencies: 301
-- Data for Name: operationsubsequente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY operationsubsequente (idoperationsubsequente, idparcelle, typeoperationsubsequente, datedepotdemande, dateinscriptionregistre, cout1, cout2, datemaj) FROM stdin;
\.


--
-- TOC entry 5168 (class 0 OID 0)
-- Dependencies: 302
-- Name: operationsubsequente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('operationsubsequente_id_seq', 1, false);


--
-- TOC entry 4976 (class 0 OID 1684159)
-- Dependencies: 304
-- Data for Name: oppositions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY oppositions (idopposition, dateopposition, datedemande, typeopposition, description, datereglement, naturereglement, descriptionreglement, iddemande, gid, etatopposition, datemaj, uuid_lr_sys) FROM stdin;
\.


--
-- TOC entry 5169 (class 0 OID 0)
-- Dependencies: 303
-- Name: oppositions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('oppositions_id_seq', 1, false);


--
-- TOC entry 4978 (class 0 OID 1684169)
-- Dependencies: 306
-- Data for Name: param_layer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY param_layer (id, label_font, label_size, label_color, stroke_size, stroke_color, layer_index, font_size_map_units, datemaj) FROM stdin;
9	MS Shell Dlg 2	12	#ffff7f	1	#000000	2	f	2024-12-03 09:01:48.101
11	Arial Black	14	#ffffff	1	#55007f	3	f	2024-12-03 09:01:48.101
10	Arial Black	12	#ffffff	2	#55007f	5	f	2024-12-03 09:01:48.101
12	Arial Black	15	#ffffff	1	#55aa00	4	f	2024-12-03 09:01:48.101
7	MS Shell Dlg 2	12	#ff0000	1	#000000	0	t	2024-12-03 09:01:48.101
8	Verdana	8	#ffff7f	1	#000000	1	t	2024-12-03 09:01:48.101
\.


--
-- TOC entry 5170 (class 0 OID 0)
-- Dependencies: 305
-- Name: param_layer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('param_layer_id_seq', 12, true);


--
-- TOC entry 4979 (class 0 OID 1684179)
-- Dependencies: 307
-- Data for Name: parcelle_d; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY parcelle_d (gid, numero, geom, numdemande, nomdemandeur, surface, titre, partie, parcelle, etat, datecreation, datereconnaissance, cout, region, district, commune, fkt, consistance, feuille, idcertificat, idhameau, idcharge, idhypotheque, idservitude, idcategorie, srisraparcelle, codeparcelle, numcertificat, estfiscalite, idcontribuable, grille, has_data, numerodmdpaps, conversion, etatparcelle_d, id_consistance, idclasse, id_commune, csv_id, anomalie, limitrophe, observation, code_parcelle_en_doublon, editer_en_cf, inventaire, sujet_demande, date_inventaire, user_import_inv, date_import_inv, ref_import, categorie, fi_forfait, datemaj, uuid_dossier_lr) FROM stdin;
\.


--
-- TOC entry 5171 (class 0 OID 0)
-- Dependencies: 308
-- Name: parcelle_d_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('parcelle_d_id_seq', 1, false);


--
-- TOC entry 4981 (class 0 OID 1684207)
-- Dependencies: 309
-- Data for Name: parcellegrevees; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY parcellegrevees (idparcellegrevees, libelleparcellegrevees, datemaj) FROM stdin;
\.


--
-- TOC entry 5172 (class 0 OID 0)
-- Dependencies: 310
-- Name: parcellegrevees_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('parcellegrevees_id_seq', 1, false);


--
-- TOC entry 5035 (class 0 OID 1685387)
-- Dependencies: 372
-- Data for Name: path_personne; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY path_personne (idpersonne, cin_recto, cin_verso, signature, datemaj) FROM stdin;
\.


--
-- TOC entry 4983 (class 0 OID 1684223)
-- Dependencies: 311
-- Data for Name: personne; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY personne (idpersonne, nompersonne, prenompersonne, sexepersonne, datenaissancepersonne, nevers, lieunaissancepersonne, numcipersonne, datecipersonne, lieucipersonne, numactenaissancepersonne, dateactenaissancepersonne, lieuactenaissancepersonne, adressepersonne, situationmatrimoniale, nompere, nommere, csv_id, rcin_personne, ogr_id, handicap, niveau_education, possede_emploi, migrant, date_arrivee, conjoint, datemaj, uuid_dossier_lr) FROM stdin;
\.


--
-- TOC entry 5173 (class 0 OID 0)
-- Dependencies: 312
-- Name: personne_idpersonne_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('personne_idpersonne_seq', 1, false);


--
-- TOC entry 4985 (class 0 OID 1684235)
-- Dependencies: 313
-- Data for Name: personne_menage; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY personne_menage (idpersonne, id_menage, est_chef, datemaj) FROM stdin;
\.


--
-- TOC entry 4986 (class 0 OID 1684239)
-- Dependencies: 314
-- Data for Name: personnemorale; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY personnemorale (numeroproprietaire, denomination, datecreation, siege, observation, idtype, idpersonnemorale, csv_id, rcin_pm, mandataire, type_declarant, datemaj) FROM stdin;
\.


--
-- TOC entry 5174 (class 0 OID 0)
-- Dependencies: 315
-- Name: personnemorale_idpersonnemorale_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('personnemorale_idpersonnemorale_seq', 16, true);


--
-- TOC entry 4988 (class 0 OID 1684247)
-- Dependencies: 316
-- Data for Name: personnemoraleparcelle; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY personnemoraleparcelle (idparcelle, idpersonnemorale, idpersonne, representant, iddemande, csv_id, datemaj) FROM stdin;
\.


--
-- TOC entry 4989 (class 0 OID 1684250)
-- Dependencies: 317
-- Data for Name: personnemoraleparcelle_d; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY personnemoraleparcelle_d (idpersonne, idparcelle, datemaj) FROM stdin;
\.


--
-- TOC entry 4990 (class 0 OID 1684261)
-- Dependencies: 318
-- Data for Name: pointscardinaux; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY pointscardinaux (idpointscardinaux, "position", fanondroana, datemaj) FROM stdin;
4	Nord	Avaratra	2024-12-03 09:01:48.101
5	Sud	Atsimo	2024-12-03 09:01:48.101
6	Est	Atsinanana	2024-12-03 09:01:48.101
11	Ouest	Andrefana	2024-12-03 09:01:48.101
\.


--
-- TOC entry 5175 (class 0 OID 0)
-- Dependencies: 319
-- Name: pointscardinaux_idpointscardinaux_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('pointscardinaux_idpointscardinaux_seq', 14, true);


--
-- TOC entry 4993 (class 0 OID 1684271)
-- Dependencies: 321
-- Data for Name: projet; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY projet (idprojet, date_lancement, date_premier_import, date_dernier_import, langue, nom, datemaj) FROM stdin;
\.


--
-- TOC entry 4995 (class 0 OID 1684277)
-- Dependencies: 323
-- Data for Name: projet_commune; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY projet_commune (idprojet_commune, idcommune, idprojet, fond_image, couche_titres, couche_cadastres, couche_limites, datemaj) FROM stdin;
\.


--
-- TOC entry 5176 (class 0 OID 0)
-- Dependencies: 322
-- Name: projet_commune_idprojet_commune_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('projet_commune_idprojet_commune_seq', 48, true);


--
-- TOC entry 5177 (class 0 OID 0)
-- Dependencies: 320
-- Name: projet_idprojet_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('projet_idprojet_seq', 1, false);


--
-- TOC entry 4996 (class 0 OID 1684284)
-- Dependencies: 324
-- Data for Name: projet_plof; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY projet_plof (idprojet, "codeRegion", "codeDistrict", "codeCommune", "Region", "District", "Commune", datemaj) FROM stdin;
\.


--
-- TOC entry 4998 (class 0 OID 1684293)
-- Dependencies: 326
-- Data for Name: projetcouche; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY projetcouche (id, idprojet_commune, libelle, type_couche, fichier, couleur_bg, ordre, label_name, show_label, font, font_size, font_size_map_unit, font_color, show_stroke, stroke_width, stroke_color, remplissage, plofpaps, certifiable, datemaj) FROM stdin;
\.


--
-- TOC entry 5178 (class 0 OID 0)
-- Dependencies: 325
-- Name: projetcouche_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('projetcouche_id_seq', 1, false);


--
-- TOC entry 4999 (class 0 OID 1684311)
-- Dependencies: 327
-- Data for Name: proprietaireparcelle; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY proprietaireparcelle (idpersonne, idparcelle, representant, contribuable, estcoproprietaire, datemaj) FROM stdin;
\.


--
-- TOC entry 5000 (class 0 OID 1684317)
-- Dependencies: 328
-- Data for Name: region; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY region (idregion, coderegion, nomregion, shapelength, shapearea, csv_id, datemaj) FROM stdin;
\.


--
-- TOC entry 5179 (class 0 OID 0)
-- Dependencies: 329
-- Name: region_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('region_id_seq', 1, false);


--
-- TOC entry 5003 (class 0 OID 1684324)
-- Dependencies: 331
-- Data for Name: rejet; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY rejet (idrejet, typerejet, daterejet, motifrejet, datemaj) FROM stdin;
\.


--
-- TOC entry 5180 (class 0 OID 0)
-- Dependencies: 330
-- Name: rejet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('rejet_id_seq', 1, false);


--
-- TOC entry 5004 (class 0 OID 1684331)
-- Dependencies: 332
-- Data for Name: role_crl; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY role_crl (id_role, libelle_role, datemaj) FROM stdin;
4	Ray aman-dReny 1	2024-12-03 09:01:48.101
5	Ray aman-dReny 2	2024-12-03 09:01:48.101
6	Ray aman-dReny 3	2024-12-03 09:01:48.101
3	Ny Solotenan ny Fokontany	2024-12-03 09:01:48.101
2	Ny Solotenan ny Kaominina	2024-12-03 09:01:48.101
7	Ny Mpiasan ny Birao Ifoton ny Fananan-tany	2024-12-03 09:01:48.101
\.


--
-- TOC entry 5181 (class 0 OID 0)
-- Dependencies: 333
-- Name: role_crl_id_role_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('role_crl_id_role_seq', 1, false);


--
-- TOC entry 5006 (class 0 OID 1684336)
-- Dependencies: 334
-- Data for Name: servitude; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY servitude (numeroservitude, dateinscription, origine, descriptionservitude, datelevee, radie, shape_length, shape_area, idservitude, datemaj) FROM stdin;
\.


--
-- TOC entry 5182 (class 0 OID 0)
-- Dependencies: 335
-- Name: servitude_idservitude_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('servitude_idservitude_seq', 19, true);


--
-- TOC entry 5008 (class 0 OID 1684344)
-- Dependencies: 336
-- Data for Name: servitudebeneficiaire; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY servitudebeneficiaire (idbeneficiaire, idservitude, datemaj) FROM stdin;
\.


--
-- TOC entry 5009 (class 0 OID 1684347)
-- Dependencies: 337
-- Data for Name: servitudeparcelle_d; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY servitudeparcelle_d (idservitude, idparcelle, datemaj) FROM stdin;
\.


--
-- TOC entry 5010 (class 0 OID 1684350)
-- Dependencies: 338
-- Data for Name: servitudeparcellegrevees; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY servitudeparcellegrevees (idparcellegrevees, idservitude, datemaj) FROM stdin;
\.


--
-- TOC entry 5183 (class 0 OID 0)
-- Dependencies: 339
-- Name: servitudeparcellegrevees_idservitude_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('servitudeparcellegrevees_idservitude_seq', 1, false);


--
-- TOC entry 4039 (class 0 OID 1682378)
-- Dependencies: 175
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text, datemaj) FROM stdin;
98751	fiplof	98751	PROJCS["laborde",GEOGCS["GCS_Tananarive_1925",DATUM["D_Tananarive_1925",SPHEROID["International_1924",6378388.0,297.0]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Hotine_Oblique_Mercator_Azimuth_Center"],PARAMETER["False_Easting",400000.0],PARAMETER["False_Northing",800000.0],PARAMETER["Scale_Factor",0.9995],PARAMETER["Azimuth",18.9],PARAMETER["Longitude_Of_Center",46.437229166666],PARAMETER["Latitude_Of_Center",-18.9],UNIT["Meter",1.0]]	+proj=omerc +lat_0=-18.9 +lonc=44.10000000000001 +alpha=18.9 +k=0.9995000000000001 +x_0=400000 +y_0=800000 +gamma=18.9 +ellps=intl +towgs84=-189,-242,-91,0,0,0,0 +pm=paris +units=m +no_defs 	2024-12-03 09:01:48.101
\.


--
-- TOC entry 5012 (class 0 OID 1684355)
-- Dependencies: 340
-- Data for Name: terain_status_specifique; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY terain_status_specifique (gid, fn_fg, demandeur, sur_plan, obs, geom, datemaj) FROM stdin;
\.


--
-- TOC entry 5184 (class 0 OID 0)
-- Dependencies: 341
-- Name: terain_status_specifique_gid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('terain_status_specifique_gid_seq', 1, false);


--
-- TOC entry 5014 (class 0 OID 1684363)
-- Dependencies: 342
-- Data for Name: titre; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY titre (gid, titres, propriete, sur_plan, titre_r, parcelle, partie, feuille, geom, datemaj) FROM stdin;
\.


--
-- TOC entry 5185 (class 0 OID 0)
-- Dependencies: 343
-- Name: titre arivonimamo i eugenie_gid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"titre arivonimamo i eugenie_gid_seq"', 333, true);


--
-- TOC entry 5186 (class 0 OID 0)
-- Dependencies: 344
-- Name: titre_gid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('titre_gid_seq', 1, false);


--
-- TOC entry 5017 (class 0 OID 1684373)
-- Dependencies: 345
-- Data for Name: titrefoncier; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY titrefoncier (numerotitre, datetitre, contenance, cheminplanindividuel, originecontour, typetitre, acteurpublic, nompropriete, consistance, shape_length, shape_area, geom, gid, observation, datemaj) FROM stdin;
\.


--
-- TOC entry 5187 (class 0 OID 0)
-- Dependencies: 346
-- Name: titrefoncier_gid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('titrefoncier_gid_seq', 12, true);


--
-- TOC entry 5019 (class 0 OID 1684381)
-- Dependencies: 347
-- Data for Name: type_anomalie; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY type_anomalie (id_type_anomalie, valeur, csv_id, datemaj) FROM stdin;
\.


--
-- TOC entry 5188 (class 0 OID 0)
-- Dependencies: 348
-- Name: type_anomalie_id_type_anomalie_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('type_anomalie_id_type_anomalie_seq', 1, false);


--
-- TOC entry 5021 (class 0 OID 1684386)
-- Dependencies: 349
-- Data for Name: type_document; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY type_document (id_type, libelle_type, datemaj) FROM stdin;
\.


--
-- TOC entry 5189 (class 0 OID 0)
-- Dependencies: 350
-- Name: type_document_id_type_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('type_document_id_type_seq', 1, false);


--
-- TOC entry 5023 (class 0 OID 1684391)
-- Dependencies: 351
-- Data for Name: typeforfaitaire; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY typeforfaitaire (idforfaitaire, libelleforfaitaire, datemaj) FROM stdin;
\.


--
-- TOC entry 5190 (class 0 OID 0)
-- Dependencies: 352
-- Name: typeforfaitaire_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('typeforfaitaire_id_seq', 1, false);


--
-- TOC entry 5026 (class 0 OID 1684398)
-- Dependencies: 354
-- Data for Name: typeoperationsubsequente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY typeoperationsubsequente (idtype, libelleoperation, datemaj) FROM stdin;
1	Mutation par décès	2024-12-03 09:01:48.101
2	Vente total	2024-12-03 09:01:48.101
3	Vente partielle avec distraction de parcelle	2024-12-03 09:01:48.101
4	Vente partielle en restant dans l'indivision	2024-12-03 09:01:48.101
5	Donation total d'un certificat	2024-12-03 09:01:48.101
6	Donation partielle avec distraction 	2024-12-03 09:01:48.101
7	Donation partielle en restant dans l'indivision	2024-12-03 09:01:48.101
8	Echange total de deux certificats	2024-12-03 09:01:48.101
9	Fusion des certificats	2024-12-03 09:01:48.101
\.


--
-- TOC entry 5191 (class 0 OID 0)
-- Dependencies: 353
-- Name: typeoperationsubsequente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('typeoperationsubsequente_id_seq', 11, true);


--
-- TOC entry 5027 (class 0 OID 1684402)
-- Dependencies: 355
-- Data for Name: typepersonnemorale; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY typepersonnemorale (idtype, type, karazana, csv_id, datemaj) FROM stdin;
1	Société	Orinasa	\N	2024-12-03 09:01:48.101
2	ONG	ONG	\N	2024-12-03 09:01:48.101
3	Association	Fikambanana	\N	2024-12-03 09:01:48.101
\.


--
-- TOC entry 5192 (class 0 OID 0)
-- Dependencies: 356
-- Name: typepersonnemorale_idtype_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('typepersonnemorale_idtype_seq', 3, true);


--
-- TOC entry 5030 (class 0 OID 1684409)
-- Dependencies: 358
-- Data for Name: utilisateur; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY utilisateur (idutilisateur, nomutilisateur, prenomutilisateur, loginutilisateur, passwordutilisateur, typeutilisateur, telephone, adresse, fonction, loginufiplof, passwdfiplof, groupe_id, datemaj) FROM stdin;
8	Responsable	Commune	respcom	0308BD47138299D52D9A197C3D2178DD	\N	034			\N	\N	5	2024-12-03 09:01:48.101
10	Assistant	Technique	ats	34EE78AE5EDC56DC1DC00BB844C5D62A	\N	034			\N	\N	11	2024-12-03 09:01:48.101
11	Formateur		formation	06048D2F2D2CA345A721B4FD25B91A92	\N	034			\N	\N	12	2024-12-03 09:01:48.101
12	Agent	Topo	topo	1D6EA1F692424E806963838CF9E37E37	\N	034			\N	\N	13	2024-12-03 09:01:48.101
13	Disposition	Transitoire	dt	13D94D956F809706C5245ABD927A0E15	\N	034			\N	\N	14	2024-12-03 09:01:48.101
14	Agent	Guichet Foncier	agf	A3856373041BB18DD4A9943A55B4D654	\N	034			\N	\N	10	2024-12-03 09:01:48.101
1	Administrateur	Fiplof	admin	EC40092C49C76E8EA3A8AA7F7FA9B0EB	\N	034			maire	maire	1	2024-12-03 09:01:48.101
\.


--
-- TOC entry 5193 (class 0 OID 0)
-- Dependencies: 357
-- Name: utilisateur_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('utilisateur_id_seq', 15, true);


--
-- TOC entry 5032 (class 0 OID 1684418)
-- Dependencies: 360
-- Data for Name: voisinparcelle; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY voisinparcelle (idvp, idvoisin, idpacelle, iddemande, datemaj) FROM stdin;
10	10	2	2	2024-12-03 09:01:48.101
11	11	2	2	2024-12-03 09:01:48.101
\.


--
-- TOC entry 5194 (class 0 OID 0)
-- Dependencies: 359
-- Name: voisinparcelle_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('voisinparcelle_id_seq', 11, true);


--
-- TOC entry 5034 (class 0 OID 1684424)
-- Dependencies: 362
-- Data for Name: voisins; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY voisins (idvoisin, nom, prenom, adresse, datemaj) FROM stdin;
10	V01	\N	Adresse	2024-12-03 09:01:48.101
11	V02	\N	Adresse 2	2024-12-03 09:01:48.101
\.


--
-- TOC entry 5195 (class 0 OID 0)
-- Dependencies: 361
-- Name: voisins_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('voisins_id_seq', 11, true);


--
-- TOC entry 5037 (class 0 OID 1685398)
-- Dependencies: 374
-- Data for Name: z_certifiable; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY z_certifiable (gid, id, crtfbl, geom, datemaj) FROM stdin;
\.


--
-- TOC entry 5196 (class 0 OID 0)
-- Dependencies: 373
-- Name: z_certifiable_gid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('z_certifiable_gid_seq', 1, false);


SET search_path = topology, pg_catalog;

--
-- TOC entry 4038 (class 0 OID 1683624)
-- Dependencies: 195
-- Data for Name: layer; Type: TABLE DATA; Schema: topology; Owner: postgres
--

COPY layer (topology_id, layer_id, schema_name, table_name, feature_column, feature_type, level, child_id) FROM stdin;
\.


--
-- TOC entry 4037 (class 0 OID 1683611)
-- Dependencies: 194
-- Data for Name: topology; Type: TABLE DATA; Schema: topology; Owner: postgres
--

COPY topology (id, name, srid, "precision", hasz) FROM stdin;
\.


SET search_path = public, pg_catalog;

--
-- TOC entry 4249 (class 2606 OID 1684544)
-- Name: acces_nom_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY acces
    ADD CONSTRAINT acces_nom_key UNIQUE (nom);


--
-- TOC entry 4251 (class 2606 OID 1684546)
-- Name: acces_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY acces
    ADD CONSTRAINT acces_pkey PRIMARY KEY (id);


--
-- TOC entry 4564 (class 2606 OID 1686339)
-- Name: date_synchro_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY date_synchro
    ADD CONSTRAINT date_synchro_pkey PRIMARY KEY (id_synchro);


--
-- TOC entry 4371 (class 2606 OID 1684550)
-- Name: demande_crl_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY demande_crl
    ADD CONSTRAINT demande_crl_pkey PRIMARY KEY (idpersonne, iddemande, id_role);


--
-- TOC entry 4357 (class 2606 OID 1684552)
-- Name: demande_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY demande
    ADD CONSTRAINT demande_pkey PRIMARY KEY (iddemande);


--
-- TOC entry 4373 (class 2606 OID 1684554)
-- Name: demande_sans_geom_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY demande_sans_geom
    ADD CONSTRAINT demande_sans_geom_pkey PRIMARY KEY (iddemande);


--
-- TOC entry 4385 (class 2606 OID 1684558)
-- Name: document_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY document
    ADD CONSTRAINT document_pkey PRIMARY KEY (id_document);


--
-- TOC entry 4398 (class 2606 OID 1684560)
-- Name: groupe_acces_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY groupe_acces
    ADD CONSTRAINT groupe_acces_pkey PRIMARY KEY (id);


--
-- TOC entry 4396 (class 2606 OID 1684562)
-- Name: groupe_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY groupe
    ADD CONSTRAINT groupe_pkey PRIMARY KEY (id);


--
-- TOC entry 4425 (class 2606 OID 1684564)
-- Name: impot_minimum_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY impot_minimum
    ADD CONSTRAINT impot_minimum_pkey PRIMARY KEY (id_impotminimum);


--
-- TOC entry 4444 (class 2606 OID 1684566)
-- Name: operationsub_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY operationsub
    ADD CONSTRAINT operationsub_pkey PRIMARY KEY (id);


--
-- TOC entry 4452 (class 2606 OID 1684568)
-- Name: param_layer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY param_layer
    ADD CONSTRAINT param_layer_pkey PRIMARY KEY (id);


--
-- TOC entry 4462 (class 2606 OID 1684570)
-- Name: parcelle_d_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY parcelle_d
    ADD CONSTRAINT parcelle_d_pkey PRIMARY KEY (gid);


--
-- TOC entry 4253 (class 2606 OID 1684572)
-- Name: pk_actedeces; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY actedeces
    ADD CONSTRAINT pk_actedeces PRIMARY KEY (idactedeces);


--
-- TOC entry 4257 (class 2606 OID 1684574)
-- Name: pk_actedecessubsequente; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY actedecessubsequente
    ADD CONSTRAINT pk_actedecessubsequente PRIMARY KEY (idactedeces, idoperationsubsequente);


--
-- TOC entry 4259 (class 2606 OID 1684576)
-- Name: pk_actedejalance; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY actedejalance
    ADD CONSTRAINT pk_actedejalance PRIMARY KEY (id);


--
-- TOC entry 4261 (class 2606 OID 1684578)
-- Name: pk_acteprive; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY acteprive
    ADD CONSTRAINT pk_acteprive PRIMARY KEY (idacteprive);


--
-- TOC entry 4265 (class 2606 OID 1684580)
-- Name: pk_acteprivesubsequente; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY acteprivesubsequente
    ADD CONSTRAINT pk_acteprivesubsequente PRIMARY KEY (idacteprive, idoperationsubsequente);


--
-- TOC entry 4267 (class 2606 OID 1684582)
-- Name: pk_actepublic; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY actepublic
    ADD CONSTRAINT pk_actepublic PRIMARY KEY (idactepublic);


--
-- TOC entry 4271 (class 2606 OID 1684584)
-- Name: pk_actepublicsubsequente; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY actepublicsubsequente
    ADD CONSTRAINT pk_actepublicsubsequente PRIMARY KEY (idactepublic, idoperationsubsequente);


--
-- TOC entry 4273 (class 2606 OID 1684586)
-- Name: pk_aire; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY aireastatutspecifique
    ADD CONSTRAINT pk_aire PRIMARY KEY (idaireastatutspecifique);


--
-- TOC entry 4276 (class 2606 OID 1684588)
-- Name: pk_anomalie; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY anomalie
    ADD CONSTRAINT pk_anomalie PRIMARY KEY (idanomalie);


--
-- TOC entry 4280 (class 2606 OID 1684590)
-- Name: pk_autrecharge; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY autrecharge
    ADD CONSTRAINT pk_autrecharge PRIMARY KEY (idcharge);


--
-- TOC entry 4282 (class 2606 OID 1684592)
-- Name: pk_autrechargeparcelle_d; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY autrechargesparcelle_d
    ADD CONSTRAINT pk_autrechargeparcelle_d PRIMARY KEY (idcharge, idparcelle);


--
-- TOC entry 4284 (class 2606 OID 1684594)
-- Name: pk_avoir_demande; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY avoir_demande
    ADD CONSTRAINT pk_avoir_demande PRIMARY KEY (idpersonne, idparcelle);


--
-- TOC entry 4290 (class 2606 OID 1684596)
-- Name: pk_avoir_dmd; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY avoir_dmd
    ADD CONSTRAINT pk_avoir_dmd PRIMARY KEY (iddemande, iddemandeur);


--
-- TOC entry 4292 (class 2606 OID 1684598)
-- Name: pk_avoirconjoint; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY avoirconjoint
    ADD CONSTRAINT pk_avoirconjoint PRIMARY KEY (idconjoint_a, idconjoint_b);


--
-- TOC entry 4301 (class 2606 OID 1684600)
-- Name: pk_batiment; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY batiment
    ADD CONSTRAINT pk_batiment PRIMARY KEY (codebatiment);


--
-- TOC entry 4303 (class 2606 OID 1684602)
-- Name: pk_beneficiaire; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY beneficiaire
    ADD CONSTRAINT pk_beneficiaire PRIMARY KEY (idbeneficiaire);


--
-- TOC entry 4305 (class 2606 OID 1684604)
-- Name: pk_blob_personne; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY blob_personne
    ADD CONSTRAINT pk_blob_personne PRIMARY KEY (idblob);


--
-- TOC entry 4309 (class 2606 OID 1684606)
-- Name: pk_blob_voisin; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY blob_voisin
    ADD CONSTRAINT pk_blob_voisin PRIMARY KEY (idpoint, idparcelle, voisin);


--
-- TOC entry 4311 (class 2606 OID 1684608)
-- Name: pk_cadastre; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY cadastre
    ADD CONSTRAINT pk_cadastre PRIMARY KEY (gid);


--
-- TOC entry 4438 (class 2606 OID 1684610)
-- Name: pk_cardinal_parcelle; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY limitesparcelle
    ADD CONSTRAINT pk_cardinal_parcelle PRIMARY KEY (idpointscardinaux, idparcelle);


--
-- TOC entry 4313 (class 2606 OID 1684612)
-- Name: pk_categorie; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY categorie
    ADD CONSTRAINT pk_categorie PRIMARY KEY (idcategorie);


--
-- TOC entry 4317 (class 2606 OID 1684614)
-- Name: pk_categorieforfaitaire; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY categorieforfaitaire
    ADD CONSTRAINT pk_categorieforfaitaire PRIMARY KEY (idcategorie, idforfaitaire);


--
-- TOC entry 4320 (class 2606 OID 1684616)
-- Name: pk_certificat; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY certificat
    ADD CONSTRAINT pk_certificat PRIMARY KEY (idcertificat);


--
-- TOC entry 4324 (class 2606 OID 1684618)
-- Name: pk_classe; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY classe
    ADD CONSTRAINT pk_classe PRIMARY KEY (idclasse);


--
-- TOC entry 4328 (class 2606 OID 1684620)
-- Name: pk_classecategorieforfaitaire; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY classecategorieforfaitaire
    ADD CONSTRAINT pk_classecategorieforfaitaire PRIMARY KEY (idcategorie, idclasse);


--
-- TOC entry 4331 (class 2606 OID 1684622)
-- Name: pk_commune; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY commune
    ADD CONSTRAINT pk_commune PRIMARY KEY (idcommune);


--
-- TOC entry 4335 (class 2606 OID 1684624)
-- Name: pk_consistance; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY consistance
    ADD CONSTRAINT pk_consistance PRIMARY KEY (idconsistance);


--
-- TOC entry 4337 (class 2606 OID 1684626)
-- Name: pk_consistanceBat; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY consistance_batiment
    ADD CONSTRAINT "pk_consistanceBat" PRIMARY KEY (id);


--
-- TOC entry 4341 (class 2606 OID 1684628)
-- Name: pk_consistanceforfaitaire; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY consistanceforfaitaire
    ADD CONSTRAINT pk_consistanceforfaitaire PRIMARY KEY (idconsistance, idforfaitaire);


--
-- TOC entry 4351 (class 2606 OID 1684630)
-- Name: pk_contr_parcelle; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY contribuables_parcelle
    ADD CONSTRAINT pk_contr_parcelle PRIMARY KEY (idpersonne, idparcelle);


--
-- TOC entry 4344 (class 2606 OID 1684632)
-- Name: pk_contribuable; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY contribuable
    ADD CONSTRAINT pk_contribuable PRIMARY KEY (idcontribuable);


--
-- TOC entry 4349 (class 2606 OID 1684634)
-- Name: pk_contribuableconsorts; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY contribuableconsorts
    ADD CONSTRAINT pk_contribuableconsorts PRIMARY KEY (idcontribuable, idconsort);


--
-- TOC entry 4355 (class 2606 OID 1684638)
-- Name: pk_decisionsubsequente; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY decisionsubsequente
    ADD CONSTRAINT pk_decisionsubsequente PRIMARY KEY (idoperationsubsequente, iddecision);


--
-- TOC entry 4369 (class 2606 OID 1684640)
-- Name: pk_demande_anomalie; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY demande_anomalie
    ADD CONSTRAINT pk_demande_anomalie PRIMARY KEY (iddemande, idanomalie);


--
-- TOC entry 4377 (class 2606 OID 1684644)
-- Name: pk_demandefn; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY demandefn
    ADD CONSTRAINT pk_demandefn PRIMARY KEY (gid);


--
-- TOC entry 4381 (class 2606 OID 1684646)
-- Name: pk_district; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY district
    ADD CONSTRAINT pk_district PRIMARY KEY (iddistrict);


--
-- TOC entry 4390 (class 2606 OID 1684650)
-- Name: pk_fokontany; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY fokontany
    ADD CONSTRAINT pk_fokontany PRIMARY KEY (idfokontany);


--
-- TOC entry 4401 (class 2606 OID 1684652)
-- Name: pk_hameau; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY hameau
    ADD CONSTRAINT pk_hameau PRIMARY KEY (idhameau);


--
-- TOC entry 4407 (class 2606 OID 1684654)
-- Name: pk_historique; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY historique
    ADD CONSTRAINT pk_historique PRIMARY KEY (idhistorique);


--
-- TOC entry 4409 (class 2606 OID 1684656)
-- Name: pk_hypotheque; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY hypotheque
    ADD CONSTRAINT pk_hypotheque PRIMARY KEY (idhypotheque);


--
-- TOC entry 4411 (class 2606 OID 1684658)
-- Name: pk_hypothequeparcelle_d; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY hypothequeparcelle_d
    ADD CONSTRAINT pk_hypothequeparcelle_d PRIMARY KEY (idhypotheque, idparcelle);


--
-- TOC entry 4413 (class 2606 OID 1684660)
-- Name: pk_impot; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY impot
    ADD CONSTRAINT pk_impot PRIMARY KEY (idimpot);


--
-- TOC entry 4416 (class 2606 OID 1684662)
-- Name: pk_impot_batiment; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY impot_batiment
    ADD CONSTRAINT pk_impot_batiment PRIMARY KEY (id);


--
-- TOC entry 4421 (class 2606 OID 1684664)
-- Name: pk_impot_contribuable; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY impot_contribuable
    ADD CONSTRAINT pk_impot_contribuable PRIMARY KEY (id);


--
-- TOC entry 4428 (class 2606 OID 1684666)
-- Name: pk_impot_percelle; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY impot_parcelle
    ADD CONSTRAINT pk_impot_percelle PRIMARY KEY (id);


--
-- TOC entry 4434 (class 2606 OID 1684668)
-- Name: pk_impotparcelle; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY impotparcelle
    ADD CONSTRAINT pk_impotparcelle PRIMARY KEY (idparcelle, idimpot);


--
-- TOC entry 4436 (class 2606 OID 1684670)
-- Name: pk_journal; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY journal
    ADD CONSTRAINT pk_journal PRIMARY KEY (id);


--
-- TOC entry 4440 (class 2606 OID 1684674)
-- Name: pk_menage; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY menage
    ADD CONSTRAINT pk_menage PRIMARY KEY (id_menage);


--
-- TOC entry 4447 (class 2606 OID 1684680)
-- Name: pk_operationsubsequente; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY operationsubsequente
    ADD CONSTRAINT pk_operationsubsequente PRIMARY KEY (idoperationsubsequente);


--
-- TOC entry 4450 (class 2606 OID 1684682)
-- Name: pk_oppositions; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY oppositions
    ADD CONSTRAINT pk_oppositions PRIMARY KEY (idopposition);


--
-- TOC entry 4387 (class 2606 OID 1684684)
-- Name: pk_paiement_impot; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY fi_paiement_impot
    ADD CONSTRAINT pk_paiement_impot PRIMARY KEY (id_paiement);


--
-- TOC entry 4470 (class 2606 OID 1684692)
-- Name: pk_parcellegrevees; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY parcellegrevees
    ADD CONSTRAINT pk_parcellegrevees PRIMARY KEY (idparcellegrevees);


--
-- TOC entry 4559 (class 2606 OID 1685394)
-- Name: pk_path; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY path_personne
    ADD CONSTRAINT pk_path PRIMARY KEY (idpersonne);


--
-- TOC entry 4482 (class 2606 OID 1684696)
-- Name: pk_persmorale; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY personnemorale
    ADD CONSTRAINT pk_persmorale PRIMARY KEY (idpersonnemorale);


--
-- TOC entry 4472 (class 2606 OID 1684698)
-- Name: pk_personne; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY personne
    ADD CONSTRAINT pk_personne PRIMARY KEY (idpersonne);


--
-- TOC entry 4480 (class 2606 OID 1684700)
-- Name: pk_personne_menage; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY personne_menage
    ADD CONSTRAINT pk_personne_menage PRIMARY KEY (idpersonne, id_menage);


--
-- TOC entry 4489 (class 2606 OID 1684702)
-- Name: pk_personnemoraleparcelle; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY personnemoraleparcelle
    ADD CONSTRAINT pk_personnemoraleparcelle PRIMARY KEY (idparcelle, idpersonnemorale, idpersonne);


--
-- TOC entry 4493 (class 2606 OID 1684704)
-- Name: pk_personnemoraleparcelle_d; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY personnemoraleparcelle_d
    ADD CONSTRAINT pk_personnemoraleparcelle_d PRIMARY KEY (idpersonne, idparcelle);


--
-- TOC entry 4495 (class 2606 OID 1684708)
-- Name: pk_pointscardinaux; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY pointscardinaux
    ADD CONSTRAINT pk_pointscardinaux PRIMARY KEY (idpointscardinaux);


--
-- TOC entry 4501 (class 2606 OID 1684710)
-- Name: pk_projet_commune_idprojet_commune; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY projet_commune
    ADD CONSTRAINT pk_projet_commune_idprojet_commune PRIMARY KEY (idprojet_commune);


--
-- TOC entry 4499 (class 2606 OID 1684712)
-- Name: pk_projet_idprojet; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY projet
    ADD CONSTRAINT pk_projet_idprojet PRIMARY KEY (idprojet);


--
-- TOC entry 4511 (class 2606 OID 1684716)
-- Name: pk_proprietaire; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY proprietaireparcelle
    ADD CONSTRAINT pk_proprietaire PRIMARY KEY (idpersonne, idparcelle);


--
-- TOC entry 4513 (class 2606 OID 1684720)
-- Name: pk_region; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY region
    ADD CONSTRAINT pk_region PRIMARY KEY (idregion);


--
-- TOC entry 4517 (class 2606 OID 1684722)
-- Name: pk_rejet; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY rejet
    ADD CONSTRAINT pk_rejet PRIMARY KEY (idrejet);


--
-- TOC entry 4521 (class 2606 OID 1684724)
-- Name: pk_servitude; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY servitude
    ADD CONSTRAINT pk_servitude PRIMARY KEY (idservitude);


--
-- TOC entry 4527 (class 2606 OID 1684726)
-- Name: pk_servitude_parcelle; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY servitudeparcelle_d
    ADD CONSTRAINT pk_servitude_parcelle PRIMARY KEY (idservitude, idparcelle);


--
-- TOC entry 4525 (class 2606 OID 1684728)
-- Name: pk_servitudebeneficiaire; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY servitudebeneficiaire
    ADD CONSTRAINT pk_servitudebeneficiaire PRIMARY KEY (idbeneficiaire, idservitude);


--
-- TOC entry 4531 (class 2606 OID 1684730)
-- Name: pk_servitudeparcellegrevees; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY servitudeparcellegrevees
    ADD CONSTRAINT pk_servitudeparcellegrevees PRIMARY KEY (idparcellegrevees, idservitude);


--
-- TOC entry 4535 (class 2606 OID 1684732)
-- Name: pk_titre; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY titre
    ADD CONSTRAINT pk_titre PRIMARY KEY (gid);


--
-- TOC entry 4537 (class 2606 OID 1684734)
-- Name: pk_titrefoncier; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY titrefoncier
    ADD CONSTRAINT pk_titrefoncier PRIMARY KEY (gid);


--
-- TOC entry 4533 (class 2606 OID 1684736)
-- Name: pk_tss; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY terain_status_specifique
    ADD CONSTRAINT pk_tss PRIMARY KEY (gid);


--
-- TOC entry 4539 (class 2606 OID 1684738)
-- Name: pk_type_anomalie; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY type_anomalie
    ADD CONSTRAINT pk_type_anomalie PRIMARY KEY (id_type_anomalie);


--
-- TOC entry 4545 (class 2606 OID 1684740)
-- Name: pk_typeforfaitaire; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY typeforfaitaire
    ADD CONSTRAINT pk_typeforfaitaire PRIMARY KEY (idforfaitaire);


--
-- TOC entry 4547 (class 2606 OID 1684742)
-- Name: pk_typeoperationsubsequente; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY typeoperationsubsequente
    ADD CONSTRAINT pk_typeoperationsubsequente PRIMARY KEY (idtype);


--
-- TOC entry 4549 (class 2606 OID 1684744)
-- Name: pk_typepersonnemorale; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY typepersonnemorale
    ADD CONSTRAINT pk_typepersonnemorale PRIMARY KEY (idtype);


--
-- TOC entry 4553 (class 2606 OID 1684746)
-- Name: pk_utilisateur; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY utilisateur
    ADD CONSTRAINT pk_utilisateur PRIMARY KEY (idutilisateur);


--
-- TOC entry 4555 (class 2606 OID 1684748)
-- Name: pk_voisinparcelle; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY voisinparcelle
    ADD CONSTRAINT pk_voisinparcelle PRIMARY KEY (idvp);


--
-- TOC entry 4557 (class 2606 OID 1684750)
-- Name: pk_voisins; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY voisins
    ADD CONSTRAINT pk_voisins PRIMARY KEY (idvoisin);


--
-- TOC entry 4505 (class 2606 OID 1684752)
-- Name: projet_plof_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY projet_plof
    ADD CONSTRAINT projet_plof_pkey PRIMARY KEY (idprojet);


--
-- TOC entry 4507 (class 2606 OID 1684754)
-- Name: projetcouche_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY projetcouche
    ADD CONSTRAINT projetcouche_pkey PRIMARY KEY (id);


--
-- TOC entry 4519 (class 2606 OID 1684756)
-- Name: role_crl_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY role_crl
    ADD CONSTRAINT role_crl_pkey PRIMARY KEY (id_role);


--
-- TOC entry 4543 (class 2606 OID 1684758)
-- Name: type_document_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY type_document
    ADD CONSTRAINT type_document_pkey PRIMARY KEY (id_type);


--
-- TOC entry 4497 (class 2606 OID 1684760)
-- Name: ui_position; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY pointscardinaux
    ADD CONSTRAINT ui_position UNIQUE ("position");


--
-- TOC entry 4474 (class 2606 OID 1684762)
-- Name: uk_cin; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY personne
    ADD CONSTRAINT uk_cin UNIQUE (numcipersonne);


--
-- TOC entry 5197 (class 0 OID 0)
-- Dependencies: 4474
-- Name: CONSTRAINT uk_cin ON personne; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON CONSTRAINT uk_cin ON personne IS 'cle unique cin';


--
-- TOC entry 4392 (class 2606 OID 1684764)
-- Name: uk_code_fkt_idcom; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY fokontany
    ADD CONSTRAINT uk_code_fkt_idcom UNIQUE (codefokontany, idcommune);


--
-- TOC entry 4442 (class 2606 OID 1684766)
-- Name: uk_code_menage; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY menage
    ADD CONSTRAINT uk_code_menage UNIQUE (code_menage);


--
-- TOC entry 4464 (class 2606 OID 1684768)
-- Name: uk_code_parcelle; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY parcelle_d
    ADD CONSTRAINT uk_code_parcelle UNIQUE (codeparcelle, id_commune);


--
-- TOC entry 4403 (class 2606 OID 1684770)
-- Name: uk_codeham_idfkt; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY hameau
    ADD CONSTRAINT uk_codeham_idfkt UNIQUE (codehameau, idfokontany);


--
-- TOC entry 4360 (class 2606 OID 1684772)
-- Name: uk_codeparcelle; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY demande
    ADD CONSTRAINT uk_codeparcelle UNIQUE (code_parcelle, idcommune);


--
-- TOC entry 4278 (class 2606 OID 1684774)
-- Name: uk_csv_anomalie; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY anomalie
    ADD CONSTRAINT uk_csv_anomalie UNIQUE (csv_id);


--
-- TOC entry 4286 (class 2606 OID 1684776)
-- Name: uk_csv_avd; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY avoir_demande
    ADD CONSTRAINT uk_csv_avd UNIQUE (csv_id);


--
-- TOC entry 4333 (class 2606 OID 1684778)
-- Name: uk_csv_commu; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY commune
    ADD CONSTRAINT uk_csv_commu UNIQUE (csv_id);


--
-- TOC entry 4362 (class 2606 OID 1684780)
-- Name: uk_csv_dema; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY demande
    ADD CONSTRAINT uk_csv_dema UNIQUE (csv_id);


--
-- TOC entry 4375 (class 2606 OID 1684782)
-- Name: uk_csv_demande_sans; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY demande_sans_geom
    ADD CONSTRAINT uk_csv_demande_sans UNIQUE (csv_id);


--
-- TOC entry 4383 (class 2606 OID 1684784)
-- Name: uk_csv_dist; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY district
    ADD CONSTRAINT uk_csv_dist UNIQUE (csv_id);


--
-- TOC entry 4394 (class 2606 OID 1684786)
-- Name: uk_csv_foko; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY fokontany
    ADD CONSTRAINT uk_csv_foko UNIQUE (csv_id);


--
-- TOC entry 4405 (class 2606 OID 1684788)
-- Name: uk_csv_hame; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY hameau
    ADD CONSTRAINT uk_csv_hame UNIQUE (csv_id);


--
-- TOC entry 4466 (class 2606 OID 1684790)
-- Name: uk_csv_parcd; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY parcelle_d
    ADD CONSTRAINT uk_csv_parcd UNIQUE (csv_id);


--
-- TOC entry 4476 (class 2606 OID 1684792)
-- Name: uk_csv_pers; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY personne
    ADD CONSTRAINT uk_csv_pers UNIQUE (csv_id);


--
-- TOC entry 4491 (class 2606 OID 1684794)
-- Name: uk_csv_persmorparc; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY personnemoraleparcelle
    ADD CONSTRAINT uk_csv_persmorparc UNIQUE (csv_id);


--
-- TOC entry 4484 (class 2606 OID 1684796)
-- Name: uk_csv_personnemorale; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY personnemorale
    ADD CONSTRAINT uk_csv_personnemorale UNIQUE (csv_id);


--
-- TOC entry 4515 (class 2606 OID 1684798)
-- Name: uk_csv_reg; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY region
    ADD CONSTRAINT uk_csv_reg UNIQUE (csv_id);


--
-- TOC entry 4541 (class 2606 OID 1684800)
-- Name: uk_csv_typeano; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY type_anomalie
    ADD CONSTRAINT uk_csv_typeano UNIQUE (csv_id);


--
-- TOC entry 4551 (class 2606 OID 1684802)
-- Name: uk_csv_typersonnemorale; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY typepersonnemorale
    ADD CONSTRAINT uk_csv_typersonnemorale UNIQUE (csv_id);


--
-- TOC entry 4364 (class 2606 OID 1684804)
-- Name: uk_demande; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY demande
    ADD CONSTRAINT uk_demande UNIQUE (numdemande);


--
-- TOC entry 4366 (class 2606 OID 1684806)
-- Name: uk_gid; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY demande
    ADD CONSTRAINT uk_gid UNIQUE (gid);


--
-- TOC entry 5198 (class 0 OID 0)
-- Dependencies: 4366
-- Name: CONSTRAINT uk_gid ON demande; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON CONSTRAINT uk_gid ON demande IS 'unique gid from parcelle_d';


--
-- TOC entry 4307 (class 2606 OID 1684808)
-- Name: uk_idpersonne; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY blob_personne
    ADD CONSTRAINT uk_idpersonne UNIQUE (idpersonne);


--
-- TOC entry 4322 (class 2606 OID 1684810)
-- Name: uk_numcertificat; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY certificat
    ADD CONSTRAINT uk_numcertificat UNIQUE (numerocertificat);


--
-- TOC entry 4346 (class 2606 OID 1684812)
-- Name: unik_cin_contribuable; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY contribuable
    ADD CONSTRAINT unik_cin_contribuable UNIQUE (cin);


--
-- TOC entry 4418 (class 2606 OID 1684816)
-- Name: unik_impot_batiment; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY impot_batiment
    ADD CONSTRAINT unik_impot_batiment UNIQUE (annee, codebatiment);


--
-- TOC entry 4423 (class 2606 OID 1684818)
-- Name: unik_impot_contribuable; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY impot_contribuable
    ADD CONSTRAINT unik_impot_contribuable UNIQUE (annee, idpersonne);


--
-- TOC entry 4430 (class 2606 OID 1684820)
-- Name: unik_impot_parcelle; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY impot_parcelle
    ADD CONSTRAINT unik_impot_parcelle UNIQUE (annee, idparcelle);


--
-- TOC entry 4294 (class 2606 OID 1684822)
-- Name: unik_personne_a; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY avoirconjoint
    ADD CONSTRAINT unik_personne_a UNIQUE (idconjoint_a);


--
-- TOC entry 4296 (class 2606 OID 1684824)
-- Name: unik_personne_b; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY avoirconjoint
    ADD CONSTRAINT unik_personne_b UNIQUE (idconjoint_b);


--
-- TOC entry 4468 (class 2606 OID 1684826)
-- Name: unique_certificat; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY parcelle_d
    ADD CONSTRAINT unique_certificat UNIQUE (idcertificat);


--
-- TOC entry 4503 (class 2606 OID 1684828)
-- Name: uq_projet_commune; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY projet_commune
    ADD CONSTRAINT uq_projet_commune UNIQUE (idcommune, idprojet);


--
-- TOC entry 4562 (class 2606 OID 1685406)
-- Name: z_certifiable_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY z_certifiable
    ADD CONSTRAINT z_certifiable_pkey PRIMARY KEY (gid);


--
-- TOC entry 4367 (class 1259 OID 1684829)
-- Name: fki_anomalie; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_anomalie ON demande_anomalie USING btree (idanomalie);


--
-- TOC entry 4287 (class 1259 OID 1684830)
-- Name: fki_avoir_dmd_iddemande; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_avoir_dmd_iddemande ON avoir_dmd USING btree (iddemande);


--
-- TOC entry 4288 (class 1259 OID 1684831)
-- Name: fki_avoir_dmd_iddemandeur; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_avoir_dmd_iddemandeur ON avoir_dmd USING btree (iddemandeur);


--
-- TOC entry 4414 (class 1259 OID 1684832)
-- Name: fki_batiment; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_batiment ON impot_batiment USING btree (codebatiment);


--
-- TOC entry 4297 (class 1259 OID 1684833)
-- Name: fki_categorie; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_categorie ON batiment USING btree (idcategorie);


--
-- TOC entry 4453 (class 1259 OID 1684834)
-- Name: fki_certificat; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_certificat ON parcelle_d USING btree (idcertificat);


--
-- TOC entry 4454 (class 1259 OID 1684835)
-- Name: fki_charge; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_charge ON parcelle_d USING btree (idcharge);


--
-- TOC entry 4455 (class 1259 OID 1684836)
-- Name: fki_consistance; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_consistance ON parcelle_d USING btree (id_consistance);


--
-- TOC entry 4342 (class 1259 OID 1684837)
-- Name: fki_consort; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_consort ON contribuable USING btree (idcontribuableconsorts);


--
-- TOC entry 4347 (class 1259 OID 1684838)
-- Name: fki_consorts; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_consorts ON contribuableconsorts USING btree (idconsort);


--
-- TOC entry 4456 (class 1259 OID 1684839)
-- Name: fki_contribuable; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_contribuable ON parcelle_d USING btree (idcontribuable);


--
-- TOC entry 4448 (class 1259 OID 1684840)
-- Name: fki_demande; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_demande ON oppositions USING btree (iddemande);


--
-- TOC entry 4477 (class 1259 OID 1684841)
-- Name: fki_fk_menage; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_fk_menage ON personne_menage USING btree (id_menage);


--
-- TOC entry 4478 (class 1259 OID 1684842)
-- Name: fki_fk_personne; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_fk_personne ON personne_menage USING btree (idpersonne);


--
-- TOC entry 4378 (class 1259 OID 1684843)
-- Name: fki_fk_region; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_fk_region ON district USING btree (idregion);


--
-- TOC entry 4318 (class 1259 OID 1684844)
-- Name: fki_fokontany; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_fokontany ON certificat USING btree (idfokontany);


--
-- TOC entry 4457 (class 1259 OID 1684845)
-- Name: fki_hypotheque; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_hypotheque ON parcelle_d USING btree (idhypotheque);


--
-- TOC entry 4458 (class 1259 OID 1684846)
-- Name: fki_idcommune; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_idcommune ON parcelle_d USING btree (id_commune);


--
-- TOC entry 4508 (class 1259 OID 1684847)
-- Name: fki_parcelle; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_parcelle ON proprietaireparcelle USING btree (idparcelle);


--
-- TOC entry 4459 (class 1259 OID 1684848)
-- Name: fki_parcelle_classe; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_parcelle_classe ON parcelle_d USING btree (idclasse);


--
-- TOC entry 4426 (class 1259 OID 1684849)
-- Name: fki_parcelle_impot; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_parcelle_impot ON impot_parcelle USING btree (idparcelle);


--
-- TOC entry 4419 (class 1259 OID 1684850)
-- Name: fki_personne; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_personne ON impot_contribuable USING btree (idpersonne);


--
-- TOC entry 4460 (class 1259 OID 1684851)
-- Name: fki_servitude; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_servitude ON parcelle_d USING btree (idservitude);


--
-- TOC entry 4522 (class 1259 OID 1684852)
-- Name: fki_servitudebeneficiaire_serv; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_servitudebeneficiaire_serv ON servitudebeneficiaire USING btree (idservitude);


--
-- TOC entry 4528 (class 1259 OID 1684853)
-- Name: fki_servitudeparcellegrevees_serv; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_servitudeparcellegrevees_serv ON servitudeparcellegrevees USING btree (idservitude);


--
-- TOC entry 4274 (class 1259 OID 1684854)
-- Name: fki_type_anomalie; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_type_anomalie ON anomalie USING btree (id_type_anomalie);


--
-- TOC entry 4254 (class 1259 OID 1684855)
-- Name: i_fk_actedecessubsequente_acte; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_actedecessubsequente_acte ON actedecessubsequente USING btree (idactedeces);


--
-- TOC entry 4255 (class 1259 OID 1684856)
-- Name: i_fk_actedecessubsequente_oper; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_actedecessubsequente_oper ON actedecessubsequente USING btree (idoperationsubsequente);


--
-- TOC entry 4262 (class 1259 OID 1684857)
-- Name: i_fk_acteprivesubsequente_acte; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_acteprivesubsequente_acte ON acteprivesubsequente USING btree (idacteprive);


--
-- TOC entry 4263 (class 1259 OID 1684858)
-- Name: i_fk_acteprivesubsequente_oper; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_acteprivesubsequente_oper ON acteprivesubsequente USING btree (idoperationsubsequente);


--
-- TOC entry 4268 (class 1259 OID 1684859)
-- Name: i_fk_actepublicsubsequente_act; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_actepublicsubsequente_act ON actepublicsubsequente USING btree (idactepublic);


--
-- TOC entry 4269 (class 1259 OID 1684860)
-- Name: i_fk_actepublicsubsequente_ope; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_actepublicsubsequente_ope ON actepublicsubsequente USING btree (idoperationsubsequente);


--
-- TOC entry 4298 (class 1259 OID 1684861)
-- Name: i_fk_batiment_consistance; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_batiment_consistance ON batiment USING btree (idconsistance);


--
-- TOC entry 4299 (class 1259 OID 1684862)
-- Name: i_fk_batiment_parcelle; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_batiment_parcelle ON batiment USING btree (idparcelle);


--
-- TOC entry 4314 (class 1259 OID 1684863)
-- Name: i_fk_categorieforfaitaire_cate; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_categorieforfaitaire_cate ON categorieforfaitaire USING btree (idcategorie);


--
-- TOC entry 4315 (class 1259 OID 1684864)
-- Name: i_fk_categorieforfaitaire_type; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_categorieforfaitaire_type ON categorieforfaitaire USING btree (idforfaitaire);


--
-- TOC entry 4325 (class 1259 OID 1684865)
-- Name: i_fk_classecategorieforfaitai1; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_classecategorieforfaitai1 ON classecategorieforfaitaire USING btree (idclasse);


--
-- TOC entry 4326 (class 1259 OID 1684866)
-- Name: i_fk_classecategorieforfaitair; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_classecategorieforfaitair ON classecategorieforfaitaire USING btree (idcategorie);


--
-- TOC entry 4329 (class 1259 OID 1684867)
-- Name: i_fk_commune_district; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_commune_district ON commune USING btree (iddistrict);


--
-- TOC entry 4338 (class 1259 OID 1684868)
-- Name: i_fk_consistanceforfaitaire_co; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_consistanceforfaitaire_co ON consistanceforfaitaire USING btree (idconsistance);


--
-- TOC entry 4339 (class 1259 OID 1684869)
-- Name: i_fk_consistanceforfaitaire_ty; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_consistanceforfaitaire_ty ON consistanceforfaitaire USING btree (idforfaitaire);


--
-- TOC entry 4352 (class 1259 OID 1684870)
-- Name: i_fk_decisionsubsequente_decis; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_decisionsubsequente_decis ON decisionsubsequente USING btree (iddecision);


--
-- TOC entry 4353 (class 1259 OID 1684871)
-- Name: i_fk_decisionsubsequente_opera; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_decisionsubsequente_opera ON decisionsubsequente USING btree (idoperationsubsequente);


--
-- TOC entry 4358 (class 1259 OID 1684872)
-- Name: i_fk_demande_parcelle_d; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_demande_parcelle_d ON demande USING btree (gid);


--
-- TOC entry 4379 (class 1259 OID 1684873)
-- Name: i_fk_district_region; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_district_region ON district USING btree (idregion);


--
-- TOC entry 4388 (class 1259 OID 1684874)
-- Name: i_fk_fokontany_commune; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_fokontany_commune ON fokontany USING btree (idcommune);


--
-- TOC entry 4399 (class 1259 OID 1684875)
-- Name: i_fk_hameau_fokontany; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_hameau_fokontany ON hameau USING btree (idfokontany);


--
-- TOC entry 4431 (class 1259 OID 1684876)
-- Name: i_fk_impotparcelle_impot; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_impotparcelle_impot ON impotparcelle USING btree (idimpot);


--
-- TOC entry 4432 (class 1259 OID 1684877)
-- Name: i_fk_impotparcelle_parcelle; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_impotparcelle_parcelle ON impotparcelle USING btree (idparcelle);


--
-- TOC entry 4445 (class 1259 OID 1684878)
-- Name: i_fk_operationsubsequente_parc; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_operationsubsequente_parc ON operationsubsequente USING btree (idparcelle);


--
-- TOC entry 4485 (class 1259 OID 1684886)
-- Name: i_fk_personnemoraleparcelle_p1; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_personnemoraleparcelle_p1 ON personnemoraleparcelle USING btree (idpersonne);


--
-- TOC entry 4486 (class 1259 OID 1684887)
-- Name: i_fk_personnemoraleparcelle_pa; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_personnemoraleparcelle_pa ON personnemoraleparcelle USING btree (idparcelle);


--
-- TOC entry 4487 (class 1259 OID 1684888)
-- Name: i_fk_personnemoraleparcelle_pe; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_personnemoraleparcelle_pe ON personnemoraleparcelle USING btree (idpersonnemorale);


--
-- TOC entry 4509 (class 1259 OID 1684889)
-- Name: i_fk_proprietaireparcelle_pers; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_proprietaireparcelle_pers ON proprietaireparcelle USING btree (idpersonne);


--
-- TOC entry 4523 (class 1259 OID 1684890)
-- Name: i_fk_servitudebeneficiaire_ben; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_servitudebeneficiaire_ben ON servitudebeneficiaire USING btree (idbeneficiaire);


--
-- TOC entry 4529 (class 1259 OID 1684891)
-- Name: i_fk_servitudeparcellegrevees1; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_servitudeparcellegrevees1 ON servitudeparcellegrevees USING btree (idparcellegrevees);


--
-- TOC entry 4560 (class 1259 OID 1685407)
-- Name: z_certifiable_geom_idx; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX z_certifiable_geom_idx ON z_certifiable USING gist (geom);


--
-- TOC entry 4651 (class 2620 OID 1686239)
-- Name: update_acces_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_acces_datemaj BEFORE UPDATE ON acces FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4652 (class 2620 OID 1686314)
-- Name: update_actedeces_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_actedeces_datemaj BEFORE UPDATE ON actedeces FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4653 (class 2620 OID 1686316)
-- Name: update_actedecessubsequente_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_actedecessubsequente_datemaj BEFORE UPDATE ON actedecessubsequente FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4654 (class 2620 OID 1686220)
-- Name: update_actedejalance_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_actedejalance_datemaj BEFORE UPDATE ON actedejalance FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4655 (class 2620 OID 1686237)
-- Name: update_acteprive_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_acteprive_datemaj BEFORE UPDATE ON acteprive FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4656 (class 2620 OID 1686318)
-- Name: update_acteprivesubsequente_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_acteprivesubsequente_datemaj BEFORE UPDATE ON acteprivesubsequente FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4657 (class 2620 OID 1686238)
-- Name: update_actepublic_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_actepublic_datemaj BEFORE UPDATE ON actepublic FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4658 (class 2620 OID 1686236)
-- Name: update_actepublicsubsequente_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_actepublicsubsequente_datemaj BEFORE UPDATE ON actepublicsubsequente FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4659 (class 2620 OID 1686221)
-- Name: update_aireastatutspecifique_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_aireastatutspecifique_datemaj BEFORE UPDATE ON aireastatutspecifique FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4660 (class 2620 OID 1686235)
-- Name: update_anomalie_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_anomalie_datemaj BEFORE UPDATE ON anomalie FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4661 (class 2620 OID 1686242)
-- Name: update_autrecharge_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_autrecharge_datemaj BEFORE UPDATE ON autrecharge FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4662 (class 2620 OID 1686243)
-- Name: update_autrechargesparcelle_d_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_autrechargesparcelle_d_datemaj BEFORE UPDATE ON autrechargesparcelle_d FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4663 (class 2620 OID 1686234)
-- Name: update_avoir_demande_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_avoir_demande_datemaj BEFORE UPDATE ON avoir_demande FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4664 (class 2620 OID 1686240)
-- Name: update_avoir_dmd_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_avoir_dmd_datemaj BEFORE UPDATE ON avoir_dmd FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4665 (class 2620 OID 1686244)
-- Name: update_avoirconjoint_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_avoirconjoint_datemaj BEFORE UPDATE ON avoirconjoint FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4666 (class 2620 OID 1686233)
-- Name: update_batiment_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_batiment_datemaj BEFORE UPDATE ON batiment FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4667 (class 2620 OID 1686241)
-- Name: update_beneficiaire_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_beneficiaire_datemaj BEFORE UPDATE ON beneficiaire FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4668 (class 2620 OID 1686257)
-- Name: update_blob_history_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_blob_history_datemaj BEFORE UPDATE ON blob_history FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4669 (class 2620 OID 1686322)
-- Name: update_blob_personne_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_blob_personne_datemaj BEFORE UPDATE ON blob_personne FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4670 (class 2620 OID 1686222)
-- Name: update_blob_voisin_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_blob_voisin_datemaj BEFORE UPDATE ON blob_voisin FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4671 (class 2620 OID 1686223)
-- Name: update_cadastre_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_cadastre_datemaj BEFORE UPDATE ON cadastre FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4672 (class 2620 OID 1686251)
-- Name: update_categorie_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_categorie_datemaj BEFORE UPDATE ON categorie FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4673 (class 2620 OID 1686324)
-- Name: update_categorieforfaitaire_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_categorieforfaitaire_datemaj BEFORE UPDATE ON categorieforfaitaire FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4674 (class 2620 OID 1686254)
-- Name: update_certificat_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_certificat_datemaj BEFORE UPDATE ON certificat FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4675 (class 2620 OID 1686245)
-- Name: update_classe_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_classe_datemaj BEFORE UPDATE ON classe FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4676 (class 2620 OID 1686325)
-- Name: update_classecategorieforfaitaire_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_classecategorieforfaitaire_datemaj BEFORE UPDATE ON classecategorieforfaitaire FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4677 (class 2620 OID 1686250)
-- Name: update_commune_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_commune_datemaj BEFORE UPDATE ON commune FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4679 (class 2620 OID 1686246)
-- Name: update_consistance_batiment_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_consistance_batiment_datemaj BEFORE UPDATE ON consistance_batiment FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4678 (class 2620 OID 1686248)
-- Name: update_consistance_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_consistance_datemaj BEFORE UPDATE ON consistance FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4680 (class 2620 OID 1686249)
-- Name: update_consistanceforfaitaire_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_consistanceforfaitaire_datemaj BEFORE UPDATE ON consistanceforfaitaire FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4681 (class 2620 OID 1686247)
-- Name: update_contribuable_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_contribuable_datemaj BEFORE UPDATE ON contribuable FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4682 (class 2620 OID 1686255)
-- Name: update_contribuableconsorts_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_contribuableconsorts_datemaj BEFORE UPDATE ON contribuableconsorts FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4683 (class 2620 OID 1686256)
-- Name: update_contribuables_parcelle_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_contribuables_parcelle_datemaj BEFORE UPDATE ON contribuables_parcelle FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4684 (class 2620 OID 1686253)
-- Name: update_decisionsubsequente_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_decisionsubsequente_datemaj BEFORE UPDATE ON decisionsubsequente FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4686 (class 2620 OID 1686328)
-- Name: update_demande_anomalie_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_demande_anomalie_datemaj BEFORE UPDATE ON demande_anomalie FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4687 (class 2620 OID 1686311)
-- Name: update_demande_crl_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_demande_crl_datemaj BEFORE UPDATE ON demande_crl FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4685 (class 2620 OID 1686266)
-- Name: update_demande_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_demande_datemaj BEFORE UPDATE ON demande FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4688 (class 2620 OID 1686224)
-- Name: update_demande_sans_geom_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_demande_sans_geom_datemaj BEFORE UPDATE ON demande_sans_geom FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4689 (class 2620 OID 1686258)
-- Name: update_demandefn_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_demandefn_datemaj BEFORE UPDATE ON demandefn FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4690 (class 2620 OID 1686267)
-- Name: update_district_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_district_datemaj BEFORE UPDATE ON district FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4691 (class 2620 OID 1686313)
-- Name: update_document_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_document_datemaj BEFORE UPDATE ON document FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4692 (class 2620 OID 1686261)
-- Name: update_fi_paiement_impot_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_fi_paiement_impot_datemaj BEFORE UPDATE ON fi_paiement_impot FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4693 (class 2620 OID 1686265)
-- Name: update_fokontany_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_fokontany_datemaj BEFORE UPDATE ON fokontany FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4695 (class 2620 OID 1686268)
-- Name: update_groupe_acces_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_groupe_acces_datemaj BEFORE UPDATE ON groupe_acces FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4694 (class 2620 OID 1686259)
-- Name: update_groupe_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_groupe_datemaj BEFORE UPDATE ON groupe FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4696 (class 2620 OID 1686264)
-- Name: update_hameau_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_hameau_datemaj BEFORE UPDATE ON hameau FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4697 (class 2620 OID 1686262)
-- Name: update_historique_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_historique_datemaj BEFORE UPDATE ON historique FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4698 (class 2620 OID 1686277)
-- Name: update_hypotheque_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_hypotheque_datemaj BEFORE UPDATE ON hypotheque FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4699 (class 2620 OID 1686317)
-- Name: update_hypothequeparcelle_d_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_hypothequeparcelle_d_datemaj BEFORE UPDATE ON hypothequeparcelle_d FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4701 (class 2620 OID 1686275)
-- Name: update_impot_batiment_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_impot_batiment_datemaj BEFORE UPDATE ON impot_batiment FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4702 (class 2620 OID 1686282)
-- Name: update_impot_contribuable_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_impot_contribuable_datemaj BEFORE UPDATE ON impot_contribuable FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4700 (class 2620 OID 1686276)
-- Name: update_impot_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_impot_datemaj BEFORE UPDATE ON impot FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4703 (class 2620 OID 1686226)
-- Name: update_impot_minimum_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_impot_minimum_datemaj BEFORE UPDATE ON impot_minimum FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4704 (class 2620 OID 1686272)
-- Name: update_impot_parcelle_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_impot_parcelle_datemaj BEFORE UPDATE ON impot_parcelle FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4705 (class 2620 OID 1686309)
-- Name: update_impotparcelle_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_impotparcelle_datemaj BEFORE UPDATE ON impotparcelle FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4706 (class 2620 OID 1686278)
-- Name: update_journal_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_journal_datemaj BEFORE UPDATE ON journal FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4707 (class 2620 OID 1686227)
-- Name: update_limitesparcelle_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_limitesparcelle_datemaj BEFORE UPDATE ON limitesparcelle FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4708 (class 2620 OID 1686279)
-- Name: update_menage_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_menage_datemaj BEFORE UPDATE ON menage FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4709 (class 2620 OID 1686270)
-- Name: update_migration_history_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_migration_history_datemaj BEFORE UPDATE ON migration_history FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4710 (class 2620 OID 1686271)
-- Name: update_operationsub_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_operationsub_datemaj BEFORE UPDATE ON operationsub FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4711 (class 2620 OID 1686315)
-- Name: update_operationsubsequente_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_operationsubsequente_datemaj BEFORE UPDATE ON operationsubsequente FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4712 (class 2620 OID 1686281)
-- Name: update_oppositions_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_oppositions_datemaj BEFORE UPDATE ON oppositions FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4713 (class 2620 OID 1686273)
-- Name: update_param_layer_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_param_layer_datemaj BEFORE UPDATE ON param_layer FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4714 (class 2620 OID 1686291)
-- Name: update_parcelle_d_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_parcelle_d_datemaj BEFORE UPDATE ON parcelle_d FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4715 (class 2620 OID 1686290)
-- Name: update_parcellegrevees_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_parcellegrevees_datemaj BEFORE UPDATE ON parcellegrevees FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4745 (class 2620 OID 1686329)
-- Name: update_path_personne_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_path_personne_datemaj BEFORE UPDATE ON path_personne FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4716 (class 2620 OID 1686323)
-- Name: update_personne_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_personne_datemaj BEFORE UPDATE ON personne FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4717 (class 2620 OID 1686287)
-- Name: update_personne_menage_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_personne_menage_datemaj BEFORE UPDATE ON personne_menage FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4718 (class 2620 OID 1686283)
-- Name: update_personnemorale_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_personnemorale_datemaj BEFORE UPDATE ON personnemorale FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4720 (class 2620 OID 1686319)
-- Name: update_personnemoraleparcelle_d_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_personnemoraleparcelle_d_datemaj BEFORE UPDATE ON personnemoraleparcelle_d FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4719 (class 2620 OID 1686310)
-- Name: update_personnemoraleparcelle_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_personnemoraleparcelle_datemaj BEFORE UPDATE ON personnemoraleparcelle FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4721 (class 2620 OID 1686286)
-- Name: update_pointscardinaux_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_pointscardinaux_datemaj BEFORE UPDATE ON pointscardinaux FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4723 (class 2620 OID 1686326)
-- Name: update_projet_commune_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_projet_commune_datemaj BEFORE UPDATE ON projet_commune FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4722 (class 2620 OID 1686288)
-- Name: update_projet_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_projet_datemaj BEFORE UPDATE ON projet FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4724 (class 2620 OID 1686230)
-- Name: update_projet_plof_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_projet_plof_datemaj BEFORE UPDATE ON projet_plof FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4725 (class 2620 OID 1686231)
-- Name: update_projetcouche_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_projetcouche_datemaj BEFORE UPDATE ON projetcouche FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4726 (class 2620 OID 1686300)
-- Name: update_proprietaireparcelle_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_proprietaireparcelle_datemaj BEFORE UPDATE ON proprietaireparcelle FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4727 (class 2620 OID 1686299)
-- Name: update_region_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_region_datemaj BEFORE UPDATE ON region FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4728 (class 2620 OID 1686293)
-- Name: update_rejet_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_rejet_datemaj BEFORE UPDATE ON rejet FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4729 (class 2620 OID 1686308)
-- Name: update_role_crl_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_role_crl_datemaj BEFORE UPDATE ON role_crl FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4730 (class 2620 OID 1686298)
-- Name: update_servitude_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_servitude_datemaj BEFORE UPDATE ON servitude FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4731 (class 2620 OID 1686321)
-- Name: update_servitudebeneficiaire_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_servitudebeneficiaire_datemaj BEFORE UPDATE ON servitudebeneficiaire FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4732 (class 2620 OID 1686320)
-- Name: update_servitudeparcelle_d_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_servitudeparcelle_d_datemaj BEFORE UPDATE ON servitudeparcelle_d FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4733 (class 2620 OID 1686302)
-- Name: update_servitudeparcellegrevees_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_servitudeparcellegrevees_datemaj BEFORE UPDATE ON servitudeparcellegrevees FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4734 (class 2620 OID 1686294)
-- Name: update_terain_status_specifique_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_terain_status_specifique_datemaj BEFORE UPDATE ON terain_status_specifique FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4735 (class 2620 OID 1686295)
-- Name: update_titre_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_titre_datemaj BEFORE UPDATE ON titre FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4736 (class 2620 OID 1686297)
-- Name: update_titrefoncier_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_titrefoncier_datemaj BEFORE UPDATE ON titrefoncier FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4737 (class 2620 OID 1686296)
-- Name: update_type_anomalie_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_type_anomalie_datemaj BEFORE UPDATE ON type_anomalie FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4738 (class 2620 OID 1686312)
-- Name: update_type_document_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_type_document_datemaj BEFORE UPDATE ON type_document FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4739 (class 2620 OID 1686327)
-- Name: update_typeforfaitaire_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_typeforfaitaire_datemaj BEFORE UPDATE ON typeforfaitaire FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4740 (class 2620 OID 1686303)
-- Name: update_typeoperationsubsequente_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_typeoperationsubsequente_datemaj BEFORE UPDATE ON typeoperationsubsequente FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4741 (class 2620 OID 1686306)
-- Name: update_typepersonnemorale_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_typepersonnemorale_datemaj BEFORE UPDATE ON typepersonnemorale FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4742 (class 2620 OID 1686307)
-- Name: update_utilisateur_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_utilisateur_datemaj BEFORE UPDATE ON utilisateur FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4743 (class 2620 OID 1686304)
-- Name: update_voisinparcelle_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_voisinparcelle_datemaj BEFORE UPDATE ON voisinparcelle FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4744 (class 2620 OID 1686305)
-- Name: update_voisins_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_voisins_datemaj BEFORE UPDATE ON voisins FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4746 (class 2620 OID 1686330)
-- Name: update_z_certifiable_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_z_certifiable_datemaj BEFORE UPDATE ON z_certifiable FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4603 (class 2606 OID 1684892)
-- Name: demande_crl_id_role_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY demande_crl
    ADD CONSTRAINT demande_crl_id_role_fkey FOREIGN KEY (id_role) REFERENCES role_crl(id_role);


--
-- TOC entry 4604 (class 2606 OID 1684897)
-- Name: demande_crl_iddemande_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY demande_crl
    ADD CONSTRAINT demande_crl_iddemande_fkey FOREIGN KEY (iddemande) REFERENCES demande(iddemande);


--
-- TOC entry 4605 (class 2606 OID 1684902)
-- Name: demande_crl_idpersonne_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY demande_crl
    ADD CONSTRAINT demande_crl_idpersonne_fkey FOREIGN KEY (idpersonne) REFERENCES personne(idpersonne);


--
-- TOC entry 4607 (class 2606 OID 1684907)
-- Name: document_id_type_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY document
    ADD CONSTRAINT document_id_type_fkey FOREIGN KEY (id_type) REFERENCES type_document(id_type);


--
-- TOC entry 4608 (class 2606 OID 1684912)
-- Name: document_iddemande_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY document
    ADD CONSTRAINT document_iddemande_fkey FOREIGN KEY (iddemande) REFERENCES demande(iddemande);


--
-- TOC entry 4565 (class 2606 OID 1684917)
-- Name: fk_actedecessubsequente_actedece; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY actedecessubsequente
    ADD CONSTRAINT fk_actedecessubsequente_actedece FOREIGN KEY (idactedeces) REFERENCES actedeces(idactedeces);


--
-- TOC entry 4566 (class 2606 OID 1684922)
-- Name: fk_actedecessubsequente_operatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY actedecessubsequente
    ADD CONSTRAINT fk_actedecessubsequente_operatio FOREIGN KEY (idoperationsubsequente) REFERENCES operationsubsequente(idoperationsubsequente);


--
-- TOC entry 4567 (class 2606 OID 1684927)
-- Name: fk_acteprivesubsequente_actepriv; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY acteprivesubsequente
    ADD CONSTRAINT fk_acteprivesubsequente_actepriv FOREIGN KEY (idacteprive) REFERENCES acteprive(idacteprive);


--
-- TOC entry 4568 (class 2606 OID 1684932)
-- Name: fk_acteprivesubsequente_operatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY acteprivesubsequente
    ADD CONSTRAINT fk_acteprivesubsequente_operatio FOREIGN KEY (idoperationsubsequente) REFERENCES operationsubsequente(idoperationsubsequente);


--
-- TOC entry 4569 (class 2606 OID 1684937)
-- Name: fk_actepublicsubsequente_actepub; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY actepublicsubsequente
    ADD CONSTRAINT fk_actepublicsubsequente_actepub FOREIGN KEY (idactepublic) REFERENCES actepublic(idactepublic);


--
-- TOC entry 4570 (class 2606 OID 1684942)
-- Name: fk_actepublicsubsequente_operati; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY actepublicsubsequente
    ADD CONSTRAINT fk_actepublicsubsequente_operati FOREIGN KEY (idoperationsubsequente) REFERENCES operationsubsequente(idoperationsubsequente);


--
-- TOC entry 4601 (class 2606 OID 1684947)
-- Name: fk_anomalie; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY demande_anomalie
    ADD CONSTRAINT fk_anomalie FOREIGN KEY (idanomalie) REFERENCES anomalie(idanomalie);


--
-- TOC entry 4572 (class 2606 OID 1684952)
-- Name: fk_autrecharge; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY autrechargesparcelle_d
    ADD CONSTRAINT fk_autrecharge FOREIGN KEY (idcharge) REFERENCES autrecharge(idcharge);


--
-- TOC entry 4577 (class 2606 OID 1684957)
-- Name: fk_avoir_dmd_demande; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY avoir_dmd
    ADD CONSTRAINT fk_avoir_dmd_demande FOREIGN KEY (iddemande) REFERENCES demande(iddemande);


--
-- TOC entry 4616 (class 2606 OID 1684967)
-- Name: fk_batiment; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY impot_batiment
    ADD CONSTRAINT fk_batiment FOREIGN KEY (codebatiment) REFERENCES batiment(codebatiment);


--
-- TOC entry 4580 (class 2606 OID 1684972)
-- Name: fk_batiment_parcelle; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY batiment
    ADD CONSTRAINT fk_batiment_parcelle FOREIGN KEY (idparcelle) REFERENCES parcelle_d(gid);


--
-- TOC entry 4585 (class 2606 OID 1684977)
-- Name: fk_blob_personne; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY blob_personne
    ADD CONSTRAINT fk_blob_personne FOREIGN KEY (idpersonne) REFERENCES personne(idpersonne);


--
-- TOC entry 4581 (class 2606 OID 1684982)
-- Name: fk_categorie; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY batiment
    ADD CONSTRAINT fk_categorie FOREIGN KEY (idcategorie) REFERENCES categorie(idcategorie);


--
-- TOC entry 4586 (class 2606 OID 1684987)
-- Name: fk_categorieforfaitaire_categori; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY categorieforfaitaire
    ADD CONSTRAINT fk_categorieforfaitaire_categori FOREIGN KEY (idcategorie) REFERENCES categorie(idcategorie);


--
-- TOC entry 4587 (class 2606 OID 1684992)
-- Name: fk_categorieforfaitaire_typeforf; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY categorieforfaitaire
    ADD CONSTRAINT fk_categorieforfaitaire_typeforf FOREIGN KEY (idforfaitaire) REFERENCES typeforfaitaire(idforfaitaire);


--
-- TOC entry 4625 (class 2606 OID 1684997)
-- Name: fk_certificat; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY parcelle_d
    ADD CONSTRAINT fk_certificat FOREIGN KEY (idcertificat) REFERENCES certificat(idcertificat);


--
-- TOC entry 4626 (class 2606 OID 1685002)
-- Name: fk_charge; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY parcelle_d
    ADD CONSTRAINT fk_charge FOREIGN KEY (idcharge) REFERENCES autrecharge(idcharge);


--
-- TOC entry 4589 (class 2606 OID 1685007)
-- Name: fk_classecategorieforfaitaire_ca; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY classecategorieforfaitaire
    ADD CONSTRAINT fk_classecategorieforfaitaire_ca FOREIGN KEY (idcategorie) REFERENCES categorie(idcategorie);


--
-- TOC entry 4590 (class 2606 OID 1685012)
-- Name: fk_classecategorieforfaitaire_cl; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY classecategorieforfaitaire
    ADD CONSTRAINT fk_classecategorieforfaitaire_cl FOREIGN KEY (idclasse) REFERENCES classe(idclasse);


--
-- TOC entry 4591 (class 2606 OID 1685017)
-- Name: fk_commune_district; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY commune
    ADD CONSTRAINT fk_commune_district FOREIGN KEY (iddistrict) REFERENCES district(iddistrict);


--
-- TOC entry 4639 (class 2606 OID 1685022)
-- Name: fk_commune_idcommune; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY projet_commune
    ADD CONSTRAINT fk_commune_idcommune FOREIGN KEY (idcommune) REFERENCES commune(idcommune) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4627 (class 2606 OID 1685027)
-- Name: fk_consistance; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY parcelle_d
    ADD CONSTRAINT fk_consistance FOREIGN KEY (id_consistance) REFERENCES consistance(idconsistance);


--
-- TOC entry 4582 (class 2606 OID 1685032)
-- Name: fk_consistance_batiment; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY batiment
    ADD CONSTRAINT fk_consistance_batiment FOREIGN KEY (idconsistance) REFERENCES consistance_batiment(id);


--
-- TOC entry 4592 (class 2606 OID 1685037)
-- Name: fk_consistanceforfaitaire_consis; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY consistanceforfaitaire
    ADD CONSTRAINT fk_consistanceforfaitaire_consis FOREIGN KEY (idconsistance) REFERENCES consistance(idconsistance);


--
-- TOC entry 4593 (class 2606 OID 1685042)
-- Name: fk_consistanceforfaitaire_typefo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY consistanceforfaitaire
    ADD CONSTRAINT fk_consistanceforfaitaire_typefo FOREIGN KEY (idforfaitaire) REFERENCES typeforfaitaire(idforfaitaire);


--
-- TOC entry 4594 (class 2606 OID 1685047)
-- Name: fk_consort; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY contribuable
    ADD CONSTRAINT fk_consort FOREIGN KEY (idcontribuableconsorts) REFERENCES contribuable(idcontribuable);


--
-- TOC entry 4595 (class 2606 OID 1685052)
-- Name: fk_consorts; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY contribuableconsorts
    ADD CONSTRAINT fk_consorts FOREIGN KEY (idconsort) REFERENCES contribuable(idcontribuable);


--
-- TOC entry 4596 (class 2606 OID 1685057)
-- Name: fk_contribuable; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY contribuableconsorts
    ADD CONSTRAINT fk_contribuable FOREIGN KEY (idcontribuable) REFERENCES contribuable(idcontribuable);


--
-- TOC entry 4628 (class 2606 OID 1685062)
-- Name: fk_contribuable; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY parcelle_d
    ADD CONSTRAINT fk_contribuable FOREIGN KEY (idcontribuable) REFERENCES contribuable(idcontribuable);


--
-- TOC entry 4599 (class 2606 OID 1685072)
-- Name: fk_decisionsubsequente_operation; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY decisionsubsequente
    ADD CONSTRAINT fk_decisionsubsequente_operation FOREIGN KEY (idoperationsubsequente) REFERENCES operationsubsequente(idoperationsubsequente);


--
-- TOC entry 4574 (class 2606 OID 1685077)
-- Name: fk_demande; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY avoir_demande
    ADD CONSTRAINT fk_demande FOREIGN KEY (iddemande) REFERENCES demande(iddemande);


--
-- TOC entry 4602 (class 2606 OID 1685082)
-- Name: fk_demande; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY demande_anomalie
    ADD CONSTRAINT fk_demande FOREIGN KEY (iddemande) REFERENCES demande(iddemande);


--
-- TOC entry 4600 (class 2606 OID 1685087)
-- Name: fk_demandecertificat_parcelle; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY demande
    ADD CONSTRAINT fk_demandecertificat_parcelle FOREIGN KEY (gid) REFERENCES parcelle_d(gid);


--
-- TOC entry 4588 (class 2606 OID 1685092)
-- Name: fk_fokontany; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY certificat
    ADD CONSTRAINT fk_fokontany FOREIGN KEY (idfokontany) REFERENCES fokontany(idfokontany);


--
-- TOC entry 4610 (class 2606 OID 1685097)
-- Name: fk_fokontany_commune; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY fokontany
    ADD CONSTRAINT fk_fokontany_commune FOREIGN KEY (idcommune) REFERENCES commune(idcommune);


--
-- TOC entry 4613 (class 2606 OID 1685102)
-- Name: fk_hameau_fokontany; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY hameau
    ADD CONSTRAINT fk_hameau_fokontany FOREIGN KEY (idfokontany) REFERENCES fokontany(idfokontany);


--
-- TOC entry 4629 (class 2606 OID 1685112)
-- Name: fk_hypotheque; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY parcelle_d
    ADD CONSTRAINT fk_hypotheque FOREIGN KEY (idhypotheque) REFERENCES hypotheque(idhypotheque);


--
-- TOC entry 4614 (class 2606 OID 1685117)
-- Name: fk_hypotheque; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY hypothequeparcelle_d
    ADD CONSTRAINT fk_hypotheque FOREIGN KEY (idhypotheque) REFERENCES hypotheque(idhypotheque);


--
-- TOC entry 4630 (class 2606 OID 1685122)
-- Name: fk_idcommune; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY parcelle_d
    ADD CONSTRAINT fk_idcommune FOREIGN KEY (id_commune) REFERENCES commune(idcommune);


--
-- TOC entry 4619 (class 2606 OID 1685127)
-- Name: fk_impotparcelle_impot; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY impotparcelle
    ADD CONSTRAINT fk_impotparcelle_impot FOREIGN KEY (idimpot) REFERENCES impot(idimpot);


--
-- TOC entry 4620 (class 2606 OID 1685132)
-- Name: fk_impotparcelle_parcelle; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY impotparcelle
    ADD CONSTRAINT fk_impotparcelle_parcelle FOREIGN KEY (idparcelle) REFERENCES parcelle_d(gid);


--
-- TOC entry 4621 (class 2606 OID 1685137)
-- Name: fk_journal_utilisateur; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY journal
    ADD CONSTRAINT fk_journal_utilisateur FOREIGN KEY (idutilisateur) REFERENCES utilisateur(idutilisateur);


--
-- TOC entry 4634 (class 2606 OID 1685142)
-- Name: fk_menage; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY personne_menage
    ADD CONSTRAINT fk_menage FOREIGN KEY (id_menage) REFERENCES menage(id_menage) NOT VALID;


--
-- TOC entry 4624 (class 2606 OID 1685157)
-- Name: fk_oppositions_demande; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY oppositions
    ADD CONSTRAINT fk_oppositions_demande FOREIGN KEY (iddemande) REFERENCES demande(iddemande);


--
-- TOC entry 4622 (class 2606 OID 1685162)
-- Name: fk_parcelle; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY limitesparcelle
    ADD CONSTRAINT fk_parcelle FOREIGN KEY (idparcelle) REFERENCES parcelle_d(gid);


--
-- TOC entry 4646 (class 2606 OID 1685167)
-- Name: fk_parcelle; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY servitudeparcelle_d
    ADD CONSTRAINT fk_parcelle FOREIGN KEY (idparcelle) REFERENCES parcelle_d(gid);


--
-- TOC entry 4615 (class 2606 OID 1685172)
-- Name: fk_parcelle; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY hypothequeparcelle_d
    ADD CONSTRAINT fk_parcelle FOREIGN KEY (idparcelle) REFERENCES parcelle_d(gid);


--
-- TOC entry 4573 (class 2606 OID 1685177)
-- Name: fk_parcelle; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY autrechargesparcelle_d
    ADD CONSTRAINT fk_parcelle FOREIGN KEY (idparcelle) REFERENCES parcelle_d(gid);


--
-- TOC entry 4642 (class 2606 OID 1685182)
-- Name: fk_parcelle; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY proprietaireparcelle
    ADD CONSTRAINT fk_parcelle FOREIGN KEY (idparcelle) REFERENCES parcelle_d(gid);


--
-- TOC entry 4597 (class 2606 OID 1685187)
-- Name: fk_parcelle; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY contribuables_parcelle
    ADD CONSTRAINT fk_parcelle FOREIGN KEY (idparcelle) REFERENCES parcelle_d(gid);


--
-- TOC entry 4631 (class 2606 OID 1685197)
-- Name: fk_parcelle_classe; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY parcelle_d
    ADD CONSTRAINT fk_parcelle_classe FOREIGN KEY (idclasse) REFERENCES classe(idclasse);


--
-- TOC entry 4637 (class 2606 OID 1685212)
-- Name: fk_parcelle_d; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY personnemoraleparcelle_d
    ADD CONSTRAINT fk_parcelle_d FOREIGN KEY (idparcelle) REFERENCES parcelle_d(gid);


--
-- TOC entry 4575 (class 2606 OID 1685217)
-- Name: fk_parcelle_d; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY avoir_demande
    ADD CONSTRAINT fk_parcelle_d FOREIGN KEY (idparcelle) REFERENCES parcelle_d(gid);


--
-- TOC entry 4632 (class 2606 OID 1685222)
-- Name: fk_parcelle_d_categorie; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY parcelle_d
    ADD CONSTRAINT fk_parcelle_d_categorie FOREIGN KEY (idcategorie) REFERENCES categorie(idcategorie);


--
-- TOC entry 4618 (class 2606 OID 1685232)
-- Name: fk_parcelle_impot; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY impot_parcelle
    ADD CONSTRAINT fk_parcelle_impot FOREIGN KEY (idparcelle) REFERENCES parcelle_d(gid);


--
-- TOC entry 4638 (class 2606 OID 1685237)
-- Name: fk_persmorale; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY personnemoraleparcelle_d
    ADD CONSTRAINT fk_persmorale FOREIGN KEY (idpersonne) REFERENCES personnemorale(idpersonnemorale);


--
-- TOC entry 4576 (class 2606 OID 1685247)
-- Name: fk_personne; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY avoir_demande
    ADD CONSTRAINT fk_personne FOREIGN KEY (idpersonne) REFERENCES personne(idpersonne);


--
-- TOC entry 4643 (class 2606 OID 1685252)
-- Name: fk_personne; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY proprietaireparcelle
    ADD CONSTRAINT fk_personne FOREIGN KEY (idpersonne) REFERENCES personne(idpersonne);


--
-- TOC entry 4598 (class 2606 OID 1685257)
-- Name: fk_personne; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY contribuables_parcelle
    ADD CONSTRAINT fk_personne FOREIGN KEY (idpersonne) REFERENCES personne(idpersonne);


--
-- TOC entry 4617 (class 2606 OID 1685262)
-- Name: fk_personne; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY impot_contribuable
    ADD CONSTRAINT fk_personne FOREIGN KEY (idpersonne) REFERENCES personne(idpersonne);


--
-- TOC entry 4635 (class 2606 OID 1685267)
-- Name: fk_personne; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY personne_menage
    ADD CONSTRAINT fk_personne FOREIGN KEY (idpersonne) REFERENCES personne(idpersonne) NOT VALID;


--
-- TOC entry 4609 (class 2606 OID 1685272)
-- Name: fk_personne; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY fi_paiement_impot
    ADD CONSTRAINT fk_personne FOREIGN KEY (idpersonne) REFERENCES personne(idpersonne);


--
-- TOC entry 4578 (class 2606 OID 1685277)
-- Name: fk_personne_a; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY avoirconjoint
    ADD CONSTRAINT fk_personne_a FOREIGN KEY (idconjoint_a) REFERENCES personne(idpersonne);


--
-- TOC entry 4579 (class 2606 OID 1685282)
-- Name: fk_personne_b; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY avoirconjoint
    ADD CONSTRAINT fk_personne_b FOREIGN KEY (idconjoint_b) REFERENCES personne(idpersonne);


--
-- TOC entry 4623 (class 2606 OID 1685297)
-- Name: fk_pointscardinaux; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY limitesparcelle
    ADD CONSTRAINT fk_pointscardinaux FOREIGN KEY (idpointscardinaux) REFERENCES pointscardinaux(idpointscardinaux);


--
-- TOC entry 4640 (class 2606 OID 1685302)
-- Name: fk_projet_idprojet; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY projet_commune
    ADD CONSTRAINT fk_projet_idprojet FOREIGN KEY (idprojet) REFERENCES projet(idprojet) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4606 (class 2606 OID 1685307)
-- Name: fk_region; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY district
    ADD CONSTRAINT fk_region FOREIGN KEY (idregion) REFERENCES region(idregion) NOT VALID;


--
-- TOC entry 4633 (class 2606 OID 1685312)
-- Name: fk_servitude; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY parcelle_d
    ADD CONSTRAINT fk_servitude FOREIGN KEY (idservitude) REFERENCES servitude(idservitude);


--
-- TOC entry 4647 (class 2606 OID 1685317)
-- Name: fk_servitude; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY servitudeparcelle_d
    ADD CONSTRAINT fk_servitude FOREIGN KEY (idservitude) REFERENCES servitude(idservitude);


--
-- TOC entry 4644 (class 2606 OID 1685322)
-- Name: fk_servitudebeneficiaire_benefic; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY servitudebeneficiaire
    ADD CONSTRAINT fk_servitudebeneficiaire_benefic FOREIGN KEY (idbeneficiaire) REFERENCES beneficiaire(idbeneficiaire);


--
-- TOC entry 4645 (class 2606 OID 1685327)
-- Name: fk_servitudebeneficiaire_serv; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY servitudebeneficiaire
    ADD CONSTRAINT fk_servitudebeneficiaire_serv FOREIGN KEY (idservitude) REFERENCES servitude(idservitude);


--
-- TOC entry 4648 (class 2606 OID 1685332)
-- Name: fk_servitudeparcellegrevees_parc; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY servitudeparcellegrevees
    ADD CONSTRAINT fk_servitudeparcellegrevees_parc FOREIGN KEY (idparcellegrevees) REFERENCES parcellegrevees(idparcellegrevees);


--
-- TOC entry 4649 (class 2606 OID 1685337)
-- Name: fk_servitudeparcellegrevees_serv; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY servitudeparcellegrevees
    ADD CONSTRAINT fk_servitudeparcellegrevees_serv FOREIGN KEY (idservitude) REFERENCES servitude(idservitude);


--
-- TOC entry 4636 (class 2606 OID 1685347)
-- Name: fk_type; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY personnemorale
    ADD CONSTRAINT fk_type FOREIGN KEY (idtype) REFERENCES typepersonnemorale(idtype);


--
-- TOC entry 4571 (class 2606 OID 1685352)
-- Name: fk_type_anomalie; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY anomalie
    ADD CONSTRAINT fk_type_anomalie FOREIGN KEY (id_type_anomalie) REFERENCES type_anomalie(id_type_anomalie);


--
-- TOC entry 4584 (class 2606 OID 1685357)
-- Name: fki_blob_history_pers; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY blob_history
    ADD CONSTRAINT fki_blob_history_pers FOREIGN KEY (idpersonne) REFERENCES personne(idpersonne);


--
-- TOC entry 4583 (class 2606 OID 1685362)
-- Name: fki_blob_hitory_utilisateur; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY blob_history
    ADD CONSTRAINT fki_blob_hitory_utilisateur FOREIGN KEY (idutilisateur) REFERENCES utilisateur(idutilisateur);


--
-- TOC entry 4611 (class 2606 OID 1685367)
-- Name: groupe_acces_acces_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY groupe_acces
    ADD CONSTRAINT groupe_acces_acces_id_fkey FOREIGN KEY (acces_id) REFERENCES acces(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4612 (class 2606 OID 1685372)
-- Name: groupe_acces_groupe_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY groupe_acces
    ADD CONSTRAINT groupe_acces_groupe_id_fkey FOREIGN KEY (groupe_id) REFERENCES groupe(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4641 (class 2606 OID 1685377)
-- Name: projetcouche_idprojet_commune_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY projetcouche
    ADD CONSTRAINT projetcouche_idprojet_commune_fkey FOREIGN KEY (idprojet_commune) REFERENCES projet_commune(idprojet_commune) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4650 (class 2606 OID 1685382)
-- Name: utilisateur_groupe_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY utilisateur
    ADD CONSTRAINT utilisateur_groupe_id_fkey FOREIGN KEY (groupe_id) REFERENCES groupe(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 5046 (class 0 OID 0)
-- Dependencies: 9
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2024-12-04 10:47:54

--
-- PostgreSQL database dump complete
--

