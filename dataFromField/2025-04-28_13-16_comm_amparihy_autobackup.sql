--
-- PostgreSQL database dump
--

-- Dumped from database version 9.3.5
-- Dumped by pg_dump version 9.3.5
-- Started on 2025-04-28 13:16:31

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 6 (class 2615 OID 1514430)
-- Name: tiger; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA tiger;


ALTER SCHEMA tiger OWNER TO postgres;

--
-- TOC entry 7 (class 2615 OID 1514431)
-- Name: tiger_data; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA tiger_data;


ALTER SCHEMA tiger_data OWNER TO postgres;

--
-- TOC entry 8 (class 2615 OID 1514432)
-- Name: topology; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA topology;


ALTER SCHEMA topology OWNER TO postgres;

--
-- TOC entry 380 (class 3079 OID 11750)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 5157 (class 0 OID 0)
-- Dependencies: 380
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- TOC entry 385 (class 3079 OID 1514433)
-- Name: address_standardizer; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS address_standardizer WITH SCHEMA public;


--
-- TOC entry 5158 (class 0 OID 0)
-- Dependencies: 385
-- Name: EXTENSION address_standardizer; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION address_standardizer IS 'Used to parse an address into constituent elements. Generally used to support geocoding address normalization step.';


--
-- TOC entry 384 (class 3079 OID 1514440)
-- Name: fuzzystrmatch; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS fuzzystrmatch WITH SCHEMA public;


--
-- TOC entry 5159 (class 0 OID 0)
-- Dependencies: 384
-- Name: EXTENSION fuzzystrmatch; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION fuzzystrmatch IS 'determine similarities and distance between strings';


--
-- TOC entry 383 (class 3079 OID 1514455)
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- TOC entry 5160 (class 0 OID 0)
-- Dependencies: 383
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';


--
-- TOC entry 382 (class 3079 OID 1515820)
-- Name: pgrouting; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS pgrouting WITH SCHEMA public;


--
-- TOC entry 5161 (class 0 OID 0)
-- Dependencies: 382
-- Name: EXTENSION pgrouting; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgrouting IS 'pgRouting Extension';


--
-- TOC entry 381 (class 3079 OID 1515974)
-- Name: postgis_topology; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS postgis_topology WITH SCHEMA topology;


--
-- TOC entry 5162 (class 0 OID 0)
-- Dependencies: 381
-- Name: EXTENSION postgis_topology; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis_topology IS 'PostGIS topology spatial types and functions';


SET search_path = public, pg_catalog;

--
-- TOC entry 1738 (class 1255 OID 1516113)
-- Name: renamecolumn(character varying, character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION renamecolumn(tablename character varying, columnname character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$
declare
 
begin
	IF EXISTS(SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = tableName AND COLUMN_NAME = columnName)
	THEN
		ALTER TABLE tableName RENAME columnName TO v_surface;
	END IF;
end;
 
$$;


ALTER FUNCTION public.renamecolumn(tablename character varying, columnname character varying) OWNER TO postgres;

--
-- TOC entry 1740 (class 1255 OID 2257403)
-- Name: update_date_dernier_maj(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION update_date_dernier_maj() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Mettre à jour la colonne date_dernier_maj dans la table configuration
    UPDATE configuration
    SET date_dernier_maj = CURRENT_TIMESTAMP
    WHERE id_configuration=(SELECT MIN(id_configuration) FROM configuration);  -- Assure-toi de cibler la bonne ligne (ici, par exemple, la ligne avec id = 1)
    
    -- Retourner la ligne affectée pour le trigger
    RETURN NULL;
END;
$$;


ALTER FUNCTION public.update_date_dernier_maj() OWNER TO postgres;

--
-- TOC entry 1739 (class 1255 OID 1529480)
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
-- TOC entry 199 (class 1259 OID 1516114)
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
-- TOC entry 200 (class 1259 OID 1516117)
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
-- TOC entry 5163 (class 0 OID 0)
-- Dependencies: 200
-- Name: acces_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE acces_id_seq OWNED BY acces.id;


--
-- TOC entry 201 (class 1259 OID 1516119)
-- Name: actedeces; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE actedeces (
    idactedeces bigint NOT NULL,
    numeroactedeces character varying(64),
    dateactedeces date,
    numeroactenotoriete character varying(64),
    dateactenotoriete date,
    idprojet integer,
    lance integer DEFAULT 0,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.actedeces OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 1516123)
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
-- TOC entry 5164 (class 0 OID 0)
-- Dependencies: 202
-- Name: actedeces_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE actedeces_id_seq OWNED BY actedeces.idactedeces;


--
-- TOC entry 203 (class 1259 OID 1516125)
-- Name: actedecessubsequente; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE actedecessubsequente (
    idactedeces bigint NOT NULL,
    idoperationsubsequente bigint NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.actedecessubsequente OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 1516128)
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
-- TOC entry 205 (class 1259 OID 1516130)
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
-- TOC entry 206 (class 1259 OID 1516134)
-- Name: acteprive; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE acteprive (
    idacteprive bigint NOT NULL,
    numeroacteprive character varying(64),
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
-- TOC entry 207 (class 1259 OID 1516138)
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
-- TOC entry 5165 (class 0 OID 0)
-- Dependencies: 207
-- Name: acteprive_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE acteprive_id_seq OWNED BY acteprive.idacteprive;


--
-- TOC entry 208 (class 1259 OID 1516140)
-- Name: acteprivesubsequente; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE acteprivesubsequente (
    idacteprive bigint NOT NULL,
    idoperationsubsequente bigint NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.acteprivesubsequente OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 1516143)
-- Name: actepublic; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE actepublic (
    idactepublic bigint NOT NULL,
    dateenregistrement date,
    nomofficierpublic text,
    nombreoperation bigint,
    idprojet integer DEFAULT 0 NOT NULL,
    numeroactepublic character varying(64),
    valeurtransaction real,
    lance bigint DEFAULT 0,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.actepublic OWNER TO postgres;

--
-- TOC entry 210 (class 1259 OID 1516151)
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
-- TOC entry 5166 (class 0 OID 0)
-- Dependencies: 210
-- Name: actepublic_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE actepublic_id_seq OWNED BY actepublic.idactepublic;


--
-- TOC entry 211 (class 1259 OID 1516153)
-- Name: actepublicsubsequente; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE actepublicsubsequente (
    idactepublic bigint NOT NULL,
    idoperationsubsequente bigint NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.actepublicsubsequente OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 1516156)
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
-- TOC entry 213 (class 1259 OID 1516162)
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
-- TOC entry 5167 (class 0 OID 0)
-- Dependencies: 213
-- Name: aireastatutspecifique_idaireastatutspecifique_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE aireastatutspecifique_idaireastatutspecifique_seq OWNED BY aireastatutspecifique.idaireastatutspecifique;


--
-- TOC entry 214 (class 1259 OID 1516164)
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
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.anomalie OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 1516170)
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
-- TOC entry 5168 (class 0 OID 0)
-- Dependencies: 215
-- Name: anomalie_idanomalie_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE anomalie_idanomalie_seq OWNED BY anomalie.idanomalie;


--
-- TOC entry 216 (class 1259 OID 1516172)
-- Name: autrecharge; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE autrecharge (
    type character(32),
    descriptioncharge text,
    dateinscriptionregistre date,
    idcharge bigint NOT NULL,
    idparcelle bigint,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.autrecharge OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 1516178)
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
-- TOC entry 5169 (class 0 OID 0)
-- Dependencies: 217
-- Name: autrecharge_idcharge_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE autrecharge_idcharge_seq OWNED BY autrecharge.idcharge;


--
-- TOC entry 218 (class 1259 OID 1516180)
-- Name: autrechargesparcelle_d; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE autrechargesparcelle_d (
    idcharge bigint NOT NULL,
    idparcelle bigint NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.autrechargesparcelle_d OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 1516183)
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
-- TOC entry 5170 (class 0 OID 0)
-- Dependencies: 219
-- Name: TABLE avoir_demande; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE avoir_demande IS 'Table liant Personne, demande et parcelle_d';


--
-- TOC entry 220 (class 1259 OID 1516186)
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
-- TOC entry 221 (class 1259 OID 1516189)
-- Name: avoirconjoint; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE avoirconjoint (
    idconjoint_a bigint NOT NULL,
    idconjoint_b bigint NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.avoirconjoint OWNER TO postgres;

--
-- TOC entry 5171 (class 0 OID 0)
-- Dependencies: 221
-- Name: TABLE avoirconjoint; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE avoirconjoint IS 'Table contenant l''id de la personne marie et celui de sa femme';


--
-- TOC entry 222 (class 1259 OID 1516192)
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
-- TOC entry 5172 (class 0 OID 0)
-- Dependencies: 222
-- Name: COLUMN batiment.fi_forfait; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN batiment.fi_forfait IS 'Valeur type calcul impôt:soit surface,soit classe, soit valeur_locative';


--
-- TOC entry 5173 (class 0 OID 0)
-- Dependencies: 222
-- Name: COLUMN batiment.idclasse; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN batiment.idclasse IS 'id classe batiment';


--
-- TOC entry 223 (class 1259 OID 1516195)
-- Name: beneficiaire; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE beneficiaire (
    idbeneficiaire bigint NOT NULL,
    libellebeneficiaire text,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.beneficiaire OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 1516201)
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
-- TOC entry 5174 (class 0 OID 0)
-- Dependencies: 224
-- Name: beneficiaire_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE beneficiaire_id_seq OWNED BY beneficiaire.idbeneficiaire;


--
-- TOC entry 225 (class 1259 OID 1516203)
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
-- TOC entry 226 (class 1259 OID 1516209)
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
-- TOC entry 227 (class 1259 OID 1516215)
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
-- TOC entry 5175 (class 0 OID 0)
-- Dependencies: 227
-- Name: blob_personne_idblob_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE blob_personne_idblob_seq OWNED BY blob_personne.idblob;


--
-- TOC entry 228 (class 1259 OID 1516217)
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
-- TOC entry 229 (class 1259 OID 1516223)
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
-- TOC entry 230 (class 1259 OID 1516229)
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
-- TOC entry 5176 (class 0 OID 0)
-- Dependencies: 230
-- Name: cadastre_gid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE cadastre_gid_seq OWNED BY cadastre.gid;


--
-- TOC entry 231 (class 1259 OID 1516231)
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
-- TOC entry 5177 (class 0 OID 0)
-- Dependencies: 231
-- Name: COLUMN categorie.v_surface; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN categorie.v_surface IS 'valeur par surface';


--
-- TOC entry 5178 (class 0 OID 0)
-- Dependencies: 231
-- Name: COLUMN categorie.u_surface; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN categorie.u_surface IS 'unité surface';


--
-- TOC entry 5179 (class 0 OID 0)
-- Dependencies: 231
-- Name: COLUMN categorie.v_venale; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN categorie.v_venale IS 'valeur venale';


--
-- TOC entry 5180 (class 0 OID 0)
-- Dependencies: 231
-- Name: COLUMN categorie.taux; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN categorie.taux IS 'taux d''imposition par valeur venale';


--
-- TOC entry 232 (class 1259 OID 1516238)
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
-- TOC entry 5181 (class 0 OID 0)
-- Dependencies: 232
-- Name: categorie_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE categorie_id_seq OWNED BY categorie.idcategorie;


--
-- TOC entry 233 (class 1259 OID 1516240)
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
-- TOC entry 234 (class 1259 OID 1516246)
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
-- TOC entry 235 (class 1259 OID 1516253)
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
-- TOC entry 5182 (class 0 OID 0)
-- Dependencies: 235
-- Name: certificat_idcertificat_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE certificat_idcertificat_seq OWNED BY certificat.idcertificat;


--
-- TOC entry 236 (class 1259 OID 1516255)
-- Name: classe; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE classe (
    idclasse bigint NOT NULL,
    libelleclasse character(32) NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.classe OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 1516258)
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
-- TOC entry 5183 (class 0 OID 0)
-- Dependencies: 237
-- Name: classe_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE classe_id_seq OWNED BY classe.idclasse;


--
-- TOC entry 238 (class 1259 OID 1516260)
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
-- TOC entry 5184 (class 0 OID 0)
-- Dependencies: 238
-- Name: COLUMN classecategorieforfaitaire.unite; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN classecategorieforfaitaire.unite IS 'unité classe forfaitaire';


--
-- TOC entry 239 (class 1259 OID 1516263)
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
-- TOC entry 240 (class 1259 OID 1516269)
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
-- TOC entry 5185 (class 0 OID 0)
-- Dependencies: 240
-- Name: commune_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE commune_id_seq OWNED BY commune.idcommune;


--
-- TOC entry 379 (class 1259 OID 2120344)
-- Name: configuration; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE configuration (
    id_configuration bigint NOT NULL,
    host_remote character varying(128),
    port_remote character varying(128),
    user_remote character varying(128),
    password_remote text,
    dbname_remote character varying(128),
    host_backup character varying(128),
    port_backup character varying(128),
    user_backup character varying(128),
    password_backup text,
    dbname_backup character varying(128),
    auto_save_path text,
    has_z_certifiable boolean DEFAULT false NOT NULL,
    online_interco boolean DEFAULT false NOT NULL,
    date_dernier_maj timestamp without time zone,
    date_dernier_autobackup timestamp without time zone
);


ALTER TABLE public.configuration OWNER TO postgres;

--
-- TOC entry 378 (class 1259 OID 2120342)
-- Name: configuration_id_configuration_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE configuration_id_configuration_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.configuration_id_configuration_seq OWNER TO postgres;

--
-- TOC entry 5186 (class 0 OID 0)
-- Dependencies: 378
-- Name: configuration_id_configuration_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE configuration_id_configuration_seq OWNED BY configuration.id_configuration;


--
-- TOC entry 241 (class 1259 OID 1516271)
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
-- TOC entry 242 (class 1259 OID 1516277)
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
-- TOC entry 5187 (class 0 OID 0)
-- Dependencies: 242
-- Name: COLUMN consistance_batiment.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN consistance_batiment.id IS 'id ';


--
-- TOC entry 243 (class 1259 OID 1516282)
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
-- TOC entry 5188 (class 0 OID 0)
-- Dependencies: 243
-- Name: consistance_batiment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE consistance_batiment_id_seq OWNED BY consistance_batiment.id;


--
-- TOC entry 244 (class 1259 OID 1516284)
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
-- TOC entry 5189 (class 0 OID 0)
-- Dependencies: 244
-- Name: consistance_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE consistance_id_seq OWNED BY consistance.idconsistance;


--
-- TOC entry 245 (class 1259 OID 1516286)
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
-- TOC entry 246 (class 1259 OID 1516289)
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
-- TOC entry 247 (class 1259 OID 1516291)
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
-- TOC entry 5190 (class 0 OID 0)
-- Dependencies: 247
-- Name: COLUMN contribuable.modecalcul; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN contribuable.modecalcul IS 'Valeur = 1 => calcul par surface
Valeur = 2 => calcul par consistance
Valeur = 3 => calcul par classe';


--
-- TOC entry 248 (class 1259 OID 1516299)
-- Name: contribuableconsorts; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE contribuableconsorts (
    idcontribuable bigint NOT NULL,
    idconsort bigint NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.contribuableconsorts OWNER TO postgres;

--
-- TOC entry 249 (class 1259 OID 1516302)
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
-- TOC entry 250 (class 1259 OID 1516305)
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
-- TOC entry 377 (class 1259 OID 1529594)
-- Name: date_synchro; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE date_synchro (
    id_synchro integer NOT NULL,
    date_synchro timestamp without time zone DEFAULT now(),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.date_synchro OWNER TO postgres;

--
-- TOC entry 376 (class 1259 OID 1529592)
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
-- TOC entry 5191 (class 0 OID 0)
-- Dependencies: 376
-- Name: date_synchro_id_synchro_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE date_synchro_id_synchro_seq OWNED BY date_synchro.id_synchro;


--
-- TOC entry 251 (class 1259 OID 1516313)
-- Name: decisionsubsequente; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE decisionsubsequente (
    idoperationsubsequente bigint NOT NULL,
    iddecision bigint NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.decisionsubsequente OWNER TO postgres;

--
-- TOC entry 252 (class 1259 OID 1516316)
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
    num_guichet_foncier character varying(50)
);


ALTER TABLE public.demande OWNER TO postgres;

--
-- TOC entry 5192 (class 0 OID 0)
-- Dependencies: 252
-- Name: COLUMN demande.sous_reserve; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN demande.sous_reserve IS 'Vrai si decision crl sous reserve';


--
-- TOC entry 253 (class 1259 OID 1516323)
-- Name: demande_anomalie; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE demande_anomalie (
    iddemande bigint NOT NULL,
    idanomalie bigint NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.demande_anomalie OWNER TO postgres;

--
-- TOC entry 254 (class 1259 OID 1516326)
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
-- TOC entry 255 (class 1259 OID 1516330)
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
-- TOC entry 5193 (class 0 OID 0)
-- Dependencies: 255
-- Name: iddemande_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE iddemande_seq OWNED BY demande.iddemande;


--
-- TOC entry 256 (class 1259 OID 1516332)
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
-- TOC entry 257 (class 1259 OID 1516348)
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
-- TOC entry 258 (class 1259 OID 1516354)
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
-- TOC entry 5194 (class 0 OID 0)
-- Dependencies: 258
-- Name: demandefn_gid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE demandefn_gid_seq OWNED BY demandefn.gid;


--
-- TOC entry 259 (class 1259 OID 1516364)
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
-- TOC entry 260 (class 1259 OID 1516367)
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
-- TOC entry 5195 (class 0 OID 0)
-- Dependencies: 260
-- Name: district_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE district_id_seq OWNED BY district.iddistrict;


--
-- TOC entry 261 (class 1259 OID 1516369)
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
-- TOC entry 262 (class 1259 OID 1516375)
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
-- TOC entry 5196 (class 0 OID 0)
-- Dependencies: 262
-- Name: document_id_document_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE document_id_document_seq OWNED BY document.id_document;


--
-- TOC entry 263 (class 1259 OID 1516385)
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
-- TOC entry 264 (class 1259 OID 1516388)
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
-- TOC entry 5197 (class 0 OID 0)
-- Dependencies: 264
-- Name: fi_paiement_impot_id_paiement_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE fi_paiement_impot_id_paiement_seq OWNED BY fi_paiement_impot.id_paiement;


--
-- TOC entry 265 (class 1259 OID 1516390)
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
-- TOC entry 266 (class 1259 OID 1516396)
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
-- TOC entry 5198 (class 0 OID 0)
-- Dependencies: 266
-- Name: fokontany_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE fokontany_id_seq OWNED BY fokontany.idfokontany;


--
-- TOC entry 267 (class 1259 OID 1516398)
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
-- TOC entry 268 (class 1259 OID 1516404)
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
-- TOC entry 269 (class 1259 OID 1516407)
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
-- TOC entry 5199 (class 0 OID 0)
-- Dependencies: 269
-- Name: groupe_acces_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE groupe_acces_id_seq OWNED BY groupe_acces.id;


--
-- TOC entry 270 (class 1259 OID 1516409)
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
-- TOC entry 5200 (class 0 OID 0)
-- Dependencies: 270
-- Name: groupe_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE groupe_id_seq OWNED BY groupe.id;


--
-- TOC entry 271 (class 1259 OID 1516411)
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
-- TOC entry 272 (class 1259 OID 1516414)
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
-- TOC entry 5201 (class 0 OID 0)
-- Dependencies: 272
-- Name: hameau_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE hameau_id_seq OWNED BY hameau.idhameau;


--
-- TOC entry 273 (class 1259 OID 1516416)
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
-- TOC entry 274 (class 1259 OID 1516419)
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
-- TOC entry 5202 (class 0 OID 0)
-- Dependencies: 274
-- Name: historique_idhistorique_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE historique_idhistorique_seq OWNED BY historique.idhistorique;


--
-- TOC entry 275 (class 1259 OID 1516421)
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
-- TOC entry 276 (class 1259 OID 1516427)
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
-- TOC entry 5203 (class 0 OID 0)
-- Dependencies: 276
-- Name: hypotheque_idhypotheque_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE hypotheque_idhypotheque_seq OWNED BY hypotheque.idhypotheque;


--
-- TOC entry 277 (class 1259 OID 1516429)
-- Name: hypothequeparcelle_d; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE hypothequeparcelle_d (
    idhypotheque bigint NOT NULL,
    idparcelle bigint NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.hypothequeparcelle_d OWNER TO postgres;

--
-- TOC entry 278 (class 1259 OID 1516432)
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
-- TOC entry 279 (class 1259 OID 1516434)
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
-- TOC entry 280 (class 1259 OID 1516436)
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
-- TOC entry 281 (class 1259 OID 1516439)
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
-- TOC entry 282 (class 1259 OID 1516442)
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
-- TOC entry 5204 (class 0 OID 0)
-- Dependencies: 282
-- Name: impot_batiment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE impot_batiment_id_seq OWNED BY impot_batiment.id;


--
-- TOC entry 283 (class 1259 OID 1516444)
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
-- TOC entry 284 (class 1259 OID 1516447)
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
-- TOC entry 5205 (class 0 OID 0)
-- Dependencies: 284
-- Name: impot_contribuable_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE impot_contribuable_id_seq OWNED BY impot_contribuable.id;


--
-- TOC entry 285 (class 1259 OID 1516449)
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
-- TOC entry 5206 (class 0 OID 0)
-- Dependencies: 285
-- Name: impot_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE impot_id_seq OWNED BY impot.idimpot;


--
-- TOC entry 286 (class 1259 OID 1516451)
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
-- TOC entry 287 (class 1259 OID 1516457)
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
-- TOC entry 5207 (class 0 OID 0)
-- Dependencies: 287
-- Name: impot_minimum_id_impotminimum_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE impot_minimum_id_impotminimum_seq OWNED BY impot_minimum.id_impotminimum;


--
-- TOC entry 288 (class 1259 OID 1516459)
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
-- TOC entry 289 (class 1259 OID 1516462)
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
-- TOC entry 5208 (class 0 OID 0)
-- Dependencies: 289
-- Name: impot_parcelle_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE impot_parcelle_id_seq OWNED BY impot_parcelle.id;


--
-- TOC entry 290 (class 1259 OID 1516464)
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
-- TOC entry 291 (class 1259 OID 1516467)
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
-- TOC entry 292 (class 1259 OID 1516470)
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
-- TOC entry 5209 (class 0 OID 0)
-- Dependencies: 292
-- Name: journal_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE journal_id_seq OWNED BY journal.id;


--
-- TOC entry 293 (class 1259 OID 1516472)
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
-- TOC entry 294 (class 1259 OID 1516474)
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
-- TOC entry 295 (class 1259 OID 1516476)
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
-- TOC entry 296 (class 1259 OID 1516490)
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
-- TOC entry 297 (class 1259 OID 1516500)
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
-- TOC entry 5210 (class 0 OID 0)
-- Dependencies: 297
-- Name: menage_id_menage_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE menage_id_menage_seq OWNED BY menage.id_menage;


--
-- TOC entry 298 (class 1259 OID 1516502)
-- Name: migration_history; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE migration_history (
    filename character varying(128),
    migration_date timestamp without time zone,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.migration_history OWNER TO postgres;

--
-- TOC entry 299 (class 1259 OID 1516513)
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
-- TOC entry 300 (class 1259 OID 1516515)
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
-- TOC entry 301 (class 1259 OID 1516519)
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
-- TOC entry 302 (class 1259 OID 1516522)
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
-- TOC entry 5211 (class 0 OID 0)
-- Dependencies: 302
-- Name: operationsubsequente_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE operationsubsequente_id_seq OWNED BY operationsubsequente.idoperationsubsequente;


--
-- TOC entry 303 (class 1259 OID 1516524)
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
-- TOC entry 304 (class 1259 OID 1516526)
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
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.oppositions OWNER TO postgres;

--
-- TOC entry 305 (class 1259 OID 1516534)
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
-- TOC entry 306 (class 1259 OID 1516536)
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
-- TOC entry 307 (class 1259 OID 1516546)
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
    CONSTRAINT geometry_valid_check CHECK (st_isvalid(geom))
);


ALTER TABLE public.parcelle_d OWNER TO postgres;

--
-- TOC entry 5212 (class 0 OID 0)
-- Dependencies: 307
-- Name: COLUMN parcelle_d.conversion; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN parcelle_d.conversion IS 'Valeur = 1 equivalent parcelle convertie en demande
Valeur = 2 equivalent parcelle convertie en Certficat';


--
-- TOC entry 5213 (class 0 OID 0)
-- Dependencies: 307
-- Name: COLUMN parcelle_d.etatparcelle_d; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN parcelle_d.etatparcelle_d IS '0 aucun
1 titre
2 cadastre
3 certificat
';


--
-- TOC entry 5214 (class 0 OID 0)
-- Dependencies: 307
-- Name: COLUMN parcelle_d.id_consistance; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN parcelle_d.id_consistance IS 'Clé etrangère vers consistance';


--
-- TOC entry 5215 (class 0 OID 0)
-- Dependencies: 307
-- Name: COLUMN parcelle_d.id_commune; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN parcelle_d.id_commune IS 'Cle etrangere commune';


--
-- TOC entry 5216 (class 0 OID 0)
-- Dependencies: 307
-- Name: COLUMN parcelle_d.fi_forfait; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN parcelle_d.fi_forfait IS 'Valeur type calcul impôt:soit surface,soit classe, soit valeur_venale';


--
-- TOC entry 308 (class 1259 OID 1516554)
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
-- TOC entry 5217 (class 0 OID 0)
-- Dependencies: 308
-- Name: parcelle_d_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE parcelle_d_id_seq OWNED BY parcelle_d.gid;


--
-- TOC entry 309 (class 1259 OID 1516574)
-- Name: parcellegrevees; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE parcellegrevees (
    idparcellegrevees bigint NOT NULL,
    libelleparcellegrevees text,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.parcellegrevees OWNER TO postgres;

--
-- TOC entry 310 (class 1259 OID 1516580)
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
-- TOC entry 5218 (class 0 OID 0)
-- Dependencies: 310
-- Name: parcellegrevees_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE parcellegrevees_id_seq OWNED BY parcellegrevees.idparcellegrevees;


--
-- TOC entry 311 (class 1259 OID 1516582)
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
-- TOC entry 312 (class 1259 OID 1516596)
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
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.personne OWNER TO postgres;

--
-- TOC entry 5219 (class 0 OID 0)
-- Dependencies: 312
-- Name: TABLE personne; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE personne IS 'Table personne en generale, permettant de gerer les proprietaires, les demandeurs et les contribuables';


--
-- TOC entry 5220 (class 0 OID 0)
-- Dependencies: 312
-- Name: COLUMN personne.situationmatrimoniale; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN personne.situationmatrimoniale IS '0 => celibataire, 1 => marie, 2 => veuf';


--
-- TOC entry 313 (class 1259 OID 1516606)
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
-- TOC entry 5221 (class 0 OID 0)
-- Dependencies: 313
-- Name: personne_idpersonne_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE personne_idpersonne_seq OWNED BY personne.idpersonne;


--
-- TOC entry 314 (class 1259 OID 1516608)
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
-- TOC entry 315 (class 1259 OID 1516612)
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
-- TOC entry 316 (class 1259 OID 1516618)
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
-- TOC entry 5222 (class 0 OID 0)
-- Dependencies: 316
-- Name: personnemorale_idpersonnemorale_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE personnemorale_idpersonnemorale_seq OWNED BY personnemorale.idpersonnemorale;


--
-- TOC entry 317 (class 1259 OID 1516620)
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
-- TOC entry 318 (class 1259 OID 1516623)
-- Name: personnemoraleparcelle_d; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE personnemoraleparcelle_d (
    idpersonne bigint NOT NULL,
    idparcelle bigint NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.personnemoraleparcelle_d OWNER TO postgres;

--
-- TOC entry 319 (class 1259 OID 1516634)
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
-- TOC entry 320 (class 1259 OID 1516640)
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
-- TOC entry 5223 (class 0 OID 0)
-- Dependencies: 320
-- Name: pointscardinaux_idpointscardinaux_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE pointscardinaux_idpointscardinaux_seq OWNED BY pointscardinaux.idpointscardinaux;


--
-- TOC entry 321 (class 1259 OID 1516642)
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
-- TOC entry 322 (class 1259 OID 1516644)
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
-- TOC entry 323 (class 1259 OID 1516648)
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
-- TOC entry 324 (class 1259 OID 1516650)
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
-- TOC entry 325 (class 1259 OID 1516657)
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
-- TOC entry 326 (class 1259 OID 1516664)
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
-- TOC entry 327 (class 1259 OID 1516666)
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
-- TOC entry 328 (class 1259 OID 1516685)
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
-- TOC entry 5224 (class 0 OID 0)
-- Dependencies: 328
-- Name: COLUMN proprietaireparcelle.contribuable; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN proprietaireparcelle.contribuable IS 'differencier les proprios contribuable et les non contribuable';


--
-- TOC entry 329 (class 1259 OID 1516691)
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
-- TOC entry 330 (class 1259 OID 1516694)
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
-- TOC entry 5225 (class 0 OID 0)
-- Dependencies: 330
-- Name: region_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE region_id_seq OWNED BY region.idregion;


--
-- TOC entry 331 (class 1259 OID 1516696)
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
-- TOC entry 332 (class 1259 OID 1516698)
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
-- TOC entry 333 (class 1259 OID 1516705)
-- Name: role_crl; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE role_crl (
    id_role integer NOT NULL,
    libelle_role character varying(100),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.role_crl OWNER TO postgres;

--
-- TOC entry 334 (class 1259 OID 1516708)
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
-- TOC entry 5226 (class 0 OID 0)
-- Dependencies: 334
-- Name: role_crl_id_role_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE role_crl_id_role_seq OWNED BY role_crl.id_role;


--
-- TOC entry 335 (class 1259 OID 1516710)
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
-- TOC entry 336 (class 1259 OID 1516716)
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
-- TOC entry 5227 (class 0 OID 0)
-- Dependencies: 336
-- Name: servitude_idservitude_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE servitude_idservitude_seq OWNED BY servitude.idservitude;


--
-- TOC entry 337 (class 1259 OID 1516718)
-- Name: servitudebeneficiaire; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE servitudebeneficiaire (
    idbeneficiaire bigint NOT NULL,
    idservitude bigint NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.servitudebeneficiaire OWNER TO postgres;

--
-- TOC entry 338 (class 1259 OID 1516721)
-- Name: servitudeparcelle_d; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE servitudeparcelle_d (
    idservitude bigint NOT NULL,
    idparcelle bigint NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.servitudeparcelle_d OWNER TO postgres;

--
-- TOC entry 339 (class 1259 OID 1516724)
-- Name: servitudeparcellegrevees; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE servitudeparcellegrevees (
    idparcellegrevees bigint NOT NULL,
    idservitude bigint NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.servitudeparcellegrevees OWNER TO postgres;

--
-- TOC entry 340 (class 1259 OID 1516727)
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
-- TOC entry 5228 (class 0 OID 0)
-- Dependencies: 340
-- Name: servitudeparcellegrevees_idservitude_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE servitudeparcellegrevees_idservitude_seq OWNED BY servitudeparcellegrevees.idservitude;


--
-- TOC entry 341 (class 1259 OID 1516729)
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
-- TOC entry 342 (class 1259 OID 1516735)
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
-- TOC entry 5229 (class 0 OID 0)
-- Dependencies: 342
-- Name: terain_status_specifique_gid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE terain_status_specifique_gid_seq OWNED BY terain_status_specifique.gid;


--
-- TOC entry 343 (class 1259 OID 1516737)
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
-- TOC entry 344 (class 1259 OID 1516743)
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
-- TOC entry 345 (class 1259 OID 1516745)
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
-- TOC entry 5230 (class 0 OID 0)
-- Dependencies: 345
-- Name: titre_gid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE titre_gid_seq OWNED BY titre.gid;


--
-- TOC entry 346 (class 1259 OID 1516747)
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
-- TOC entry 347 (class 1259 OID 1516753)
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
-- TOC entry 5231 (class 0 OID 0)
-- Dependencies: 347
-- Name: titrefoncier_gid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE titrefoncier_gid_seq OWNED BY titrefoncier.gid;


--
-- TOC entry 348 (class 1259 OID 1516755)
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
-- TOC entry 349 (class 1259 OID 1516758)
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
-- TOC entry 5232 (class 0 OID 0)
-- Dependencies: 349
-- Name: type_anomalie_id_type_anomalie_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE type_anomalie_id_type_anomalie_seq OWNED BY type_anomalie.id_type_anomalie;


--
-- TOC entry 350 (class 1259 OID 1516760)
-- Name: type_document; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE type_document (
    id_type integer NOT NULL,
    libelle_type character varying(128),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.type_document OWNER TO postgres;

--
-- TOC entry 351 (class 1259 OID 1516763)
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
-- TOC entry 5233 (class 0 OID 0)
-- Dependencies: 351
-- Name: type_document_id_type_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE type_document_id_type_seq OWNED BY type_document.id_type;


--
-- TOC entry 352 (class 1259 OID 1516765)
-- Name: typeforfaitaire; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE typeforfaitaire (
    idforfaitaire bigint NOT NULL,
    libelleforfaitaire character varying(50) NOT NULL,
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.typeforfaitaire OWNER TO postgres;

--
-- TOC entry 353 (class 1259 OID 1516768)
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
-- TOC entry 5234 (class 0 OID 0)
-- Dependencies: 353
-- Name: typeforfaitaire_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE typeforfaitaire_id_seq OWNED BY typeforfaitaire.idforfaitaire;


--
-- TOC entry 354 (class 1259 OID 1516770)
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
-- TOC entry 355 (class 1259 OID 1516772)
-- Name: typeoperationsubsequente; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE typeoperationsubsequente (
    idtype integer DEFAULT nextval('typeoperationsubsequente_id_seq'::regclass) NOT NULL,
    libelleoperation character varying(250),
    datemaj timestamp without time zone DEFAULT now()
);


ALTER TABLE public.typeoperationsubsequente OWNER TO postgres;

--
-- TOC entry 356 (class 1259 OID 1516776)
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
-- TOC entry 357 (class 1259 OID 1516779)
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
-- TOC entry 5235 (class 0 OID 0)
-- Dependencies: 357
-- Name: typepersonnemorale_idtype_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE typepersonnemorale_idtype_seq OWNED BY typepersonnemorale.idtype;


--
-- TOC entry 358 (class 1259 OID 1516781)
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
-- TOC entry 359 (class 1259 OID 1516783)
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
-- TOC entry 360 (class 1259 OID 1516790)
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
-- TOC entry 361 (class 1259 OID 1516792)
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
-- TOC entry 362 (class 1259 OID 1516796)
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
-- TOC entry 363 (class 1259 OID 1516798)
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
-- TOC entry 364 (class 1259 OID 1516805)
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
-- TOC entry 365 (class 1259 OID 1516809)
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
-- TOC entry 366 (class 1259 OID 1516814)
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
-- TOC entry 367 (class 1259 OID 1516819)
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
-- TOC entry 368 (class 1259 OID 1516823)
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
-- TOC entry 369 (class 1259 OID 1516827)
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
-- TOC entry 370 (class 1259 OID 1516832)
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
-- TOC entry 371 (class 1259 OID 1516837)
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
-- TOC entry 372 (class 1259 OID 1516841)
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
-- TOC entry 373 (class 1259 OID 1516845)
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
-- TOC entry 374 (class 1259 OID 1516847)
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
-- TOC entry 375 (class 1259 OID 1516854)
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
-- TOC entry 4054 (class 2604 OID 1516858)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY acces ALTER COLUMN id SET DEFAULT nextval('acces_id_seq'::regclass);


--
-- TOC entry 4057 (class 2604 OID 1516859)
-- Name: idactedeces; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY actedeces ALTER COLUMN idactedeces SET DEFAULT nextval('actedeces_id_seq'::regclass);


--
-- TOC entry 4063 (class 2604 OID 1516860)
-- Name: idacteprive; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY acteprive ALTER COLUMN idacteprive SET DEFAULT nextval('acteprive_id_seq'::regclass);


--
-- TOC entry 4068 (class 2604 OID 1516861)
-- Name: idactepublic; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY actepublic ALTER COLUMN idactepublic SET DEFAULT nextval('actepublic_id_seq'::regclass);


--
-- TOC entry 4071 (class 2604 OID 1516862)
-- Name: idaireastatutspecifique; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY aireastatutspecifique ALTER COLUMN idaireastatutspecifique SET DEFAULT nextval('aireastatutspecifique_idaireastatutspecifique_seq'::regclass);


--
-- TOC entry 4073 (class 2604 OID 1516863)
-- Name: idanomalie; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY anomalie ALTER COLUMN idanomalie SET DEFAULT nextval('anomalie_idanomalie_seq'::regclass);


--
-- TOC entry 4075 (class 2604 OID 1516864)
-- Name: idcharge; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY autrecharge ALTER COLUMN idcharge SET DEFAULT nextval('autrecharge_idcharge_seq'::regclass);


--
-- TOC entry 4082 (class 2604 OID 1516865)
-- Name: idbeneficiaire; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY beneficiaire ALTER COLUMN idbeneficiaire SET DEFAULT nextval('beneficiaire_id_seq'::regclass);


--
-- TOC entry 4085 (class 2604 OID 1516866)
-- Name: idblob; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY blob_personne ALTER COLUMN idblob SET DEFAULT nextval('blob_personne_idblob_seq'::regclass);


--
-- TOC entry 4088 (class 2604 OID 1516867)
-- Name: gid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY cadastre ALTER COLUMN gid SET DEFAULT nextval('cadastre_gid_seq'::regclass);


--
-- TOC entry 4094 (class 2604 OID 1516868)
-- Name: idcategorie; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY categorie ALTER COLUMN idcategorie SET DEFAULT nextval('categorie_id_seq'::regclass);


--
-- TOC entry 4098 (class 2604 OID 1516869)
-- Name: idcertificat; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY certificat ALTER COLUMN idcertificat SET DEFAULT nextval('certificat_idcertificat_seq'::regclass);


--
-- TOC entry 4100 (class 2604 OID 1516870)
-- Name: idclasse; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY classe ALTER COLUMN idclasse SET DEFAULT nextval('classe_id_seq'::regclass);


--
-- TOC entry 4106 (class 2604 OID 1516871)
-- Name: idcommune; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY commune ALTER COLUMN idcommune SET DEFAULT nextval('commune_id_seq'::regclass);


--
-- TOC entry 4257 (class 2604 OID 2120347)
-- Name: id_configuration; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY configuration ALTER COLUMN id_configuration SET DEFAULT nextval('configuration_id_configuration_seq'::regclass);


--
-- TOC entry 4108 (class 2604 OID 1516872)
-- Name: idconsistance; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY consistance ALTER COLUMN idconsistance SET DEFAULT nextval('consistance_id_seq'::regclass);


--
-- TOC entry 4112 (class 2604 OID 1516873)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY consistance_batiment ALTER COLUMN id SET DEFAULT nextval('consistance_batiment_id_seq'::regclass);


--
-- TOC entry 4254 (class 2604 OID 1529597)
-- Name: id_synchro; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY date_synchro ALTER COLUMN id_synchro SET DEFAULT nextval('date_synchro_id_synchro_seq'::regclass);


--
-- TOC entry 4122 (class 2604 OID 1516875)
-- Name: iddemande; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY demande ALTER COLUMN iddemande SET DEFAULT nextval('iddemande_seq'::regclass);


--
-- TOC entry 4130 (class 2604 OID 1516877)
-- Name: gid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY demandefn ALTER COLUMN gid SET DEFAULT nextval('demandefn_gid_seq'::regclass);


--
-- TOC entry 4132 (class 2604 OID 1516879)
-- Name: iddistrict; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY district ALTER COLUMN iddistrict SET DEFAULT nextval('district_id_seq'::regclass);


--
-- TOC entry 4134 (class 2604 OID 1516880)
-- Name: id_document; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY document ALTER COLUMN id_document SET DEFAULT nextval('document_id_document_seq'::regclass);


--
-- TOC entry 4136 (class 2604 OID 1516882)
-- Name: id_paiement; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY fi_paiement_impot ALTER COLUMN id_paiement SET DEFAULT nextval('fi_paiement_impot_id_paiement_seq'::regclass);


--
-- TOC entry 4138 (class 2604 OID 1516883)
-- Name: idfokontany; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY fokontany ALTER COLUMN idfokontany SET DEFAULT nextval('fokontany_id_seq'::regclass);


--
-- TOC entry 4140 (class 2604 OID 1516884)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY groupe ALTER COLUMN id SET DEFAULT nextval('groupe_id_seq'::regclass);


--
-- TOC entry 4142 (class 2604 OID 1516885)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY groupe_acces ALTER COLUMN id SET DEFAULT nextval('groupe_acces_id_seq'::regclass);


--
-- TOC entry 4144 (class 2604 OID 1516886)
-- Name: idhameau; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY hameau ALTER COLUMN idhameau SET DEFAULT nextval('hameau_id_seq'::regclass);


--
-- TOC entry 4146 (class 2604 OID 1516887)
-- Name: idhistorique; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY historique ALTER COLUMN idhistorique SET DEFAULT nextval('historique_idhistorique_seq'::regclass);


--
-- TOC entry 4148 (class 2604 OID 1516888)
-- Name: idhypotheque; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY hypotheque ALTER COLUMN idhypotheque SET DEFAULT nextval('hypotheque_idhypotheque_seq'::regclass);


--
-- TOC entry 4151 (class 2604 OID 1516889)
-- Name: idimpot; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY impot ALTER COLUMN idimpot SET DEFAULT nextval('impot_id_seq'::regclass);


--
-- TOC entry 4153 (class 2604 OID 1516890)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY impot_batiment ALTER COLUMN id SET DEFAULT nextval('impot_batiment_id_seq'::regclass);


--
-- TOC entry 4155 (class 2604 OID 1516891)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY impot_contribuable ALTER COLUMN id SET DEFAULT nextval('impot_contribuable_id_seq'::regclass);


--
-- TOC entry 4157 (class 2604 OID 1516892)
-- Name: id_impotminimum; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY impot_minimum ALTER COLUMN id_impotminimum SET DEFAULT nextval('impot_minimum_id_impotminimum_seq'::regclass);


--
-- TOC entry 4159 (class 2604 OID 1516893)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY impot_parcelle ALTER COLUMN id SET DEFAULT nextval('impot_parcelle_id_seq'::regclass);


--
-- TOC entry 4162 (class 2604 OID 1516894)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY journal ALTER COLUMN id SET DEFAULT nextval('journal_id_seq'::regclass);


--
-- TOC entry 4172 (class 2604 OID 1516896)
-- Name: id_menage; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY menage ALTER COLUMN id_menage SET DEFAULT nextval('menage_id_menage_seq'::regclass);


--
-- TOC entry 4177 (class 2604 OID 1516898)
-- Name: idoperationsubsequente; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY operationsubsequente ALTER COLUMN idoperationsubsequente SET DEFAULT nextval('operationsubsequente_id_seq'::regclass);


--
-- TOC entry 4185 (class 2604 OID 1516900)
-- Name: gid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY parcelle_d ALTER COLUMN gid SET DEFAULT nextval('parcelle_d_id_seq'::regclass);


--
-- TOC entry 4188 (class 2604 OID 1516903)
-- Name: idparcellegrevees; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY parcellegrevees ALTER COLUMN idparcellegrevees SET DEFAULT nextval('parcellegrevees_id_seq'::regclass);


--
-- TOC entry 4195 (class 2604 OID 1516905)
-- Name: idpersonne; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY personne ALTER COLUMN idpersonne SET DEFAULT nextval('personne_idpersonne_seq'::regclass);


--
-- TOC entry 4199 (class 2604 OID 1516906)
-- Name: idpersonnemorale; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY personnemorale ALTER COLUMN idpersonnemorale SET DEFAULT nextval('personnemorale_idpersonnemorale_seq'::regclass);


--
-- TOC entry 4203 (class 2604 OID 1516908)
-- Name: idpointscardinaux; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY pointscardinaux ALTER COLUMN idpointscardinaux SET DEFAULT nextval('pointscardinaux_idpointscardinaux_seq'::regclass);


--
-- TOC entry 4218 (class 2604 OID 1516910)
-- Name: idregion; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY region ALTER COLUMN idregion SET DEFAULT nextval('region_id_seq'::regclass);


--
-- TOC entry 4222 (class 2604 OID 1516911)
-- Name: id_role; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY role_crl ALTER COLUMN id_role SET DEFAULT nextval('role_crl_id_role_seq'::regclass);


--
-- TOC entry 4224 (class 2604 OID 1516912)
-- Name: idservitude; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY servitude ALTER COLUMN idservitude SET DEFAULT nextval('servitude_idservitude_seq'::regclass);


--
-- TOC entry 4228 (class 2604 OID 1516913)
-- Name: idservitude; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY servitudeparcellegrevees ALTER COLUMN idservitude SET DEFAULT nextval('servitudeparcellegrevees_idservitude_seq'::regclass);


--
-- TOC entry 4230 (class 2604 OID 1516914)
-- Name: gid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY terain_status_specifique ALTER COLUMN gid SET DEFAULT nextval('terain_status_specifique_gid_seq'::regclass);


--
-- TOC entry 4232 (class 2604 OID 1516915)
-- Name: gid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY titre ALTER COLUMN gid SET DEFAULT nextval('titre_gid_seq'::regclass);


--
-- TOC entry 4234 (class 2604 OID 1516916)
-- Name: gid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY titrefoncier ALTER COLUMN gid SET DEFAULT nextval('titrefoncier_gid_seq'::regclass);


--
-- TOC entry 4236 (class 2604 OID 1516917)
-- Name: id_type_anomalie; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY type_anomalie ALTER COLUMN id_type_anomalie SET DEFAULT nextval('type_anomalie_id_type_anomalie_seq'::regclass);


--
-- TOC entry 4238 (class 2604 OID 1516918)
-- Name: id_type; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY type_document ALTER COLUMN id_type SET DEFAULT nextval('type_document_id_type_seq'::regclass);


--
-- TOC entry 4240 (class 2604 OID 1516919)
-- Name: idforfaitaire; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY typeforfaitaire ALTER COLUMN idforfaitaire SET DEFAULT nextval('typeforfaitaire_id_seq'::regclass);


--
-- TOC entry 4244 (class 2604 OID 1516920)
-- Name: idtype; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY typepersonnemorale ALTER COLUMN idtype SET DEFAULT nextval('typepersonnemorale_idtype_seq'::regclass);


--
-- TOC entry 4979 (class 0 OID 1516114)
-- Dependencies: 199
-- Data for Name: acces; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY acces (id, nom, libelle, datemaj) FROM stdin;
1	DEMANDE/CREATE	Creation Demande	2024-11-14 14:30:40.86
2	DEMANDE/READ	Consultation Demande	2024-11-14 14:30:40.86
3	DEMANDE/EDIT_INFO	Edition des informations des demandes	2024-11-14 14:30:40.86
4	DEMANDE/EDIT_GEO	Edition des geometries des demandes	2024-11-14 14:30:40.86
5	CERTIFICAT/CREATE	Creation Certificat	2024-11-14 14:30:40.86
6	CERTIFICAT/READ	Consultation Certificat	2024-11-14 14:30:40.86
7	CERTIFICAT/EDIT_INFO	Edition des informations des certificats	2024-11-14 14:30:40.86
8	CERTIFICAT/EDIT_GEO	Edition des geometries des certificats	2024-11-14 14:30:40.86
9	PERSONNE_PHYSIQUE/CREATE	Creation Personne Physique	2024-11-14 14:30:40.86
10	PERSONNE_PHYSIQUE/READ	Consultation Personne Physique	2024-11-14 14:30:40.86
11	PERSONNE_PHYSIQUE/EDIT	Edition Personne Physique	2024-11-14 14:30:40.86
12	PERSONNE_MORALE/CREATE	Creation Personne Morale	2024-11-14 14:30:40.86
13	PERSONNE_MORALE/READ	Consultation Personne Morale	2024-11-14 14:30:40.86
14	PERSONNE_MORALE/EDIT	Edition Personne Morale	2024-11-14 14:30:40.86
15	PERSONNE_MORALE_TYPE/CREATE	Creation Type de Personnes Morales	2024-11-14 14:30:40.86
16	PERSONNE_MORALE_TYPE/READ	Consultation Type de Personnes Morales	2024-11-14 14:30:40.86
17	PERSONNE_MORALE_TYPE/EDIT	Edition Type de Personnes Morales	2024-11-14 14:30:40.86
18	PERSONNE_MORALE_TYPE/DELETE	Supression Type de Personnes Morales	2024-11-14 14:30:40.86
19	KARATANY/PRINT	Impression Karatany	2024-11-14 14:30:40.86
21	CERTIFICAT/ATTESTATION	Attestation Certificat	2024-11-14 14:30:40.86
23	CERTIFICAT/ANNULATION	Annulation Certificat	2024-11-14 14:30:40.86
24	OPERATIONS_SUBSEQUENTES	Operations Subsequentes	2024-11-14 14:30:40.86
25	IMPOT_FONCIER/CREATE	Saisie des Donnees	2024-11-14 14:30:40.86
26	IMPOT_FONCIER/CALCUL	Calcul Impots	2024-11-14 14:30:40.86
27	IMPOT_FONCIER/PARAMETRES	Parametres	2024-11-14 14:30:40.86
28	IMPOT_FONCIER/REGISTRE	Registre des Demandes	2024-11-14 14:30:40.86
29	IMPOT_FONCIER/BENEFICIAIRES	Liste des Beneficiaires	2024-11-14 14:30:40.86
30	IMPOT_FONCIER/AFFICHAGE	Affichage	2024-11-14 14:30:40.86
33	FICHIER/LOAD_PTS_XLS	Charger des points depuis xls	2024-11-14 14:30:40.86
34	FICHIER/LEVE_GPS	Leve parcelle GPS	2024-11-14 14:30:40.86
35	DEMANDE/LISTIN_IMPORT	Import Listing	2024-11-14 14:30:40.86
36	DEMANDE/DATE_ATTRIB	Attribution des dates	2024-11-14 14:30:40.86
37	DEMANDE/OPPOSITION	Signaler Opposition	2024-11-14 14:30:40.86
38	RECONNAISSANCE_LOCALE/EXPORT_RL	Export données pour RL	2024-11-14 14:30:40.86
39	RECONNAISSANCE_LOCALE/IMPORT_RL	Import données après RL	2024-11-14 14:30:40.86
40	CERTIFICAT/TRANSFO_GROUPEE	Transformation groupée	2024-11-14 14:30:40.86
41	CERTIFICAT/ANNULLE	Annulation certificat	2024-11-14 14:30:40.86
42	IMPOT_FONCIER/AUTRES	Autres_Liste des beneficiaires	2024-11-14 14:30:40.86
43	IMPORT_EXPORT/EXPORT_SHAPE	Export shapefile	2024-11-14 14:30:40.86
45	PROJET/ANCIENNE_DONNEES	Anciennes données	2024-11-14 14:30:40.86
46	PROJET/DONNEES_TERRAIN	Données Terrains	2024-11-14 14:30:40.86
47	PROJET/NEW	Nouveau projet	2024-11-14 14:30:40.86
48	PROJET/LIST	Liste des projets	2024-11-14 14:30:40.86
49	PROJET/PARAMS	Paramètres projet	2024-11-14 14:30:40.86
50	PARAMETRES/HAMEAU	Hameau	2024-11-14 14:30:40.86
51	PARAMETRES/CATEGORIE	Categorie	2024-11-14 14:30:40.86
52	PARAMETRES/CONSISTANCE_BAT	Consistance batiment	2024-11-14 14:30:40.86
53	PARAMETRES/TERRITOIRE	Territoires	2024-11-14 14:30:40.86
54	PARAMETRES/CONTENANCE_MAX	Contenance maximale	2024-11-14 14:30:40.86
55	PARAMETRES/BDD	Base de données	2024-11-14 14:30:40.86
56	PARAMETRES/COMPTEUR	Compteur	2024-11-14 14:30:40.86
57	PARAMETRES/BD_VIDE	Créer une base de données vide	2024-11-14 14:30:40.86
58	PARAMETRES/BD_SPLIT	Séparer la base en base de données par commune	2024-11-14 14:30:40.86
59	ETATS/AFFICHAGE	Affichage collectif	2024-11-14 14:30:40.86
60	ETATS/FANAPAHANA	Decision	2024-11-14 14:30:40.86
61	ETATS/ATTESTATION	Attestation	2024-11-14 14:30:40.86
62	ETATS/RP	Registre Parcellaire	2024-11-14 14:30:40.86
63	ETATS/PAGE_OP	Page Operations subsequentes	2024-11-14 14:30:40.86
64	ETATS/RDD	Registre de demande	2024-11-14 14:30:40.86
65	ETATS/AVIS_IMPOSITION	Avis imposition	2024-11-14 14:30:40.86
66	ETATS/CERTIFICAT_AFFICHAGE	Certificat affichage	2024-11-14 14:30:40.86
67	ETATS/LISTING_DEMANDE	Listing Demande	2024-11-14 14:30:40.86
68	ETATS/PVRL	PVRL	2024-11-14 14:30:40.86
69	ETATS/NOMBRE_CF	Nombre de demande et CF	2024-11-14 14:30:40.86
70	ETATS/STATISTIQUES	Statistique	2024-11-14 14:30:40.86
71	INVENTAIRE/IMPORT_DATA	Import Données inventaire	2024-11-14 14:30:40.86
72	INVENTAIRE/FILTRE	Filtre inventaire	2024-11-14 14:30:40.86
73	PLOF/IMPORT_SHAPE	Import Shape PLOF	2024-11-14 14:30:40.86
74	PLOF/IMPORT_DXF	Import Fichier DXF	2024-11-14 14:30:40.86
75	DEMANDE/CREATE_NO_GEOM	Creation Demande sans géometrie	2024-11-14 14:30:40.86
76	IMPORT_EXPORT/IMPORT	Restauration BD	2024-11-14 14:30:40.86
77	IMPORT_EXPORT/EXPORT	Sauvegarde BD	2024-11-14 14:30:40.86
78	TOOL_EDIT/EDIT_GEOM	Edition géometrie sur carte	2024-11-14 14:30:40.86
79	TOOL_EDIT/DEL_GEOM	Supprimer géometrie sur carte	2024-11-14 14:30:40.86
80	BTN/RASTER	Bouton Raster (table des matières)	2024-11-14 14:30:40.86
81	BTN/VECTEUR	Bouton Vecteur (table des matières)	2024-11-14 14:30:40.86
82	BTN/SUPPR	Bouton Supprimer (table des matières)	2024-11-14 14:30:40.86
83	TOOL_EDIT/PARAM_ACCROCHAGE	Paramètres accrochages	2024-11-14 14:30:40.86
84	PROJET_UTILISATEUR/GERER_GROUPE	Gestion des groupes	2024-11-14 14:30:40.86
86	IMPORT_EXPORT/IMPORT_PLOF	Import Plof repertoire	2024-11-14 14:30:40.86
\.


--
-- TOC entry 5236 (class 0 OID 0)
-- Dependencies: 200
-- Name: acces_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('acces_id_seq', 86, true);


--
-- TOC entry 4981 (class 0 OID 1516119)
-- Dependencies: 201
-- Data for Name: actedeces; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY actedeces (idactedeces, numeroactedeces, dateactedeces, numeroactenotoriete, dateactenotoriete, idprojet, lance, datemaj) FROM stdin;
\.


--
-- TOC entry 5237 (class 0 OID 0)
-- Dependencies: 202
-- Name: actedeces_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('actedeces_id_seq', 1, false);


--
-- TOC entry 4983 (class 0 OID 1516125)
-- Dependencies: 203
-- Data for Name: actedecessubsequente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY actedecessubsequente (idactedeces, idoperationsubsequente, datemaj) FROM stdin;
\.


--
-- TOC entry 4985 (class 0 OID 1516130)
-- Dependencies: 205
-- Data for Name: actedejalance; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY actedejalance (id, idacte, typeacte, datemaj) FROM stdin;
\.


--
-- TOC entry 5238 (class 0 OID 0)
-- Dependencies: 204
-- Name: actedj_gid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('actedj_gid_seq', 1569, false);


--
-- TOC entry 4986 (class 0 OID 1516134)
-- Dependencies: 206
-- Data for Name: acteprive; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY acteprive (idacteprive, numeroacteprive, dateenregistrement, datelegalisationsignature, nombreoperation, valeurtransaction, idprojet, lance, datemaj) FROM stdin;
\.


--
-- TOC entry 5239 (class 0 OID 0)
-- Dependencies: 207
-- Name: acteprive_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('acteprive_id_seq', 1, false);


--
-- TOC entry 4988 (class 0 OID 1516140)
-- Dependencies: 208
-- Data for Name: acteprivesubsequente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY acteprivesubsequente (idacteprive, idoperationsubsequente, datemaj) FROM stdin;
\.


--
-- TOC entry 4989 (class 0 OID 1516143)
-- Dependencies: 209
-- Data for Name: actepublic; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY actepublic (idactepublic, dateenregistrement, nomofficierpublic, nombreoperation, idprojet, numeroactepublic, valeurtransaction, lance, datemaj) FROM stdin;
\.


--
-- TOC entry 5240 (class 0 OID 0)
-- Dependencies: 210
-- Name: actepublic_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('actepublic_id_seq', 1, false);


--
-- TOC entry 4991 (class 0 OID 1516153)
-- Dependencies: 211
-- Data for Name: actepublicsubsequente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY actepublicsubsequente (idactepublic, idoperationsubsequente, datemaj) FROM stdin;
\.


--
-- TOC entry 4992 (class 0 OID 1516156)
-- Dependencies: 212
-- Data for Name: aireastatutspecifique; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY aireastatutspecifique (originecontour, nom, type, shape_length, shape_area, idaireastatutspecifique, geom, observation, datemaj) FROM stdin;
\.


--
-- TOC entry 5241 (class 0 OID 0)
-- Dependencies: 213
-- Name: aireastatutspecifique_idaireastatutspecifique_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('aireastatutspecifique_idaireastatutspecifique_seq', 3, true);


--
-- TOC entry 4994 (class 0 OID 1516164)
-- Dependencies: 214
-- Data for Name: anomalie; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY anomalie (idanomalie, id_type_anomalie, description, resolu, csv_iddemande, date_anomalie, csv_id, csv_id_type_anomalie, datemaj) FROM stdin;
\.


--
-- TOC entry 5242 (class 0 OID 0)
-- Dependencies: 215
-- Name: anomalie_idanomalie_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('anomalie_idanomalie_seq', 1, false);


--
-- TOC entry 4996 (class 0 OID 1516172)
-- Dependencies: 216
-- Data for Name: autrecharge; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY autrecharge (type, descriptioncharge, dateinscriptionregistre, idcharge, idparcelle, datemaj) FROM stdin;
\.


--
-- TOC entry 5243 (class 0 OID 0)
-- Dependencies: 217
-- Name: autrecharge_idcharge_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('autrecharge_idcharge_seq', 16, true);


--
-- TOC entry 4998 (class 0 OID 1516180)
-- Dependencies: 218
-- Data for Name: autrechargesparcelle_d; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY autrechargesparcelle_d (idcharge, idparcelle, datemaj) FROM stdin;
\.


--
-- TOC entry 4999 (class 0 OID 1516183)
-- Dependencies: 219
-- Data for Name: avoir_demande; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY avoir_demande (idpersonne, iddemande, idparcelle, representant, csv_id, datemaj) FROM stdin;
\.


--
-- TOC entry 5000 (class 0 OID 1516186)
-- Dependencies: 220
-- Data for Name: avoir_dmd; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY avoir_dmd (iddemandeur, iddemande, gid, datemaj) FROM stdin;
\.


--
-- TOC entry 5001 (class 0 OID 1516189)
-- Dependencies: 221
-- Data for Name: avoirconjoint; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY avoirconjoint (idconjoint_a, idconjoint_b, datemaj) FROM stdin;
\.


--
-- TOC entry 5002 (class 0 OID 1516192)
-- Dependencies: 222
-- Data for Name: batiment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY batiment (codebatiment, idparcelle, idconsistance, surfacebatiment, nbpiecebatiment, locationbatiment, idcategorie, fi_forfait, idclasse, datemaj) FROM stdin;
\.


--
-- TOC entry 5003 (class 0 OID 1516195)
-- Dependencies: 223
-- Data for Name: beneficiaire; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY beneficiaire (idbeneficiaire, libellebeneficiaire, datemaj) FROM stdin;
\.


--
-- TOC entry 5244 (class 0 OID 0)
-- Dependencies: 224
-- Name: beneficiaire_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('beneficiaire_id_seq', 1, false);


--
-- TOC entry 5005 (class 0 OID 1516203)
-- Dependencies: 225
-- Data for Name: blob_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY blob_history (idpersonne, idutilisateur, old_file, new_file, old_file_type, new_file_type, nature, datemodification, old_file_name, new_file_name, datemaj) FROM stdin;
\.


--
-- TOC entry 5006 (class 0 OID 1516209)
-- Dependencies: 226
-- Data for Name: blob_personne; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY blob_personne (idblob, idpersonne, cin_recto, cin_verso, signature, empreinte_d, empreinte_g, cin_recto_name, cin_recto_type, cin_verso_name, cin_verso_type, signature_name, signature_type, empreinte_d_name, empreinte_d_type, empreinte_g_name, empreinte_g_type, photo_demandeur, photo_demandeur_type, datemaj) FROM stdin;
\.


--
-- TOC entry 5245 (class 0 OID 0)
-- Dependencies: 227
-- Name: blob_personne_idblob_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('blob_personne_idblob_seq', 8, true);


--
-- TOC entry 5008 (class 0 OID 1516217)
-- Dependencies: 228
-- Data for Name: blob_voisin; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY blob_voisin (idpoint, idparcelle, voisin, signature_fic, signature_name, signature_ext, datemaj) FROM stdin;
\.


--
-- TOC entry 5009 (class 0 OID 1516223)
-- Dependencies: 229
-- Data for Name: cadastre; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY cadastre (gid, nom_section, section, parcelle, nom_plan, geom, datemaj) FROM stdin;
61	AMBATO	BH	54	\N	010300002006740000010000000500000001AC905E2DD3FFBFC4C28F87F81CE93F5ED5B1F0E321F8BF46DC134FE650E83FB7A4D8B77B0DF8BF74DE170102D9D53F2455887737DEFFBF7CDD76C058F9DB3F01AC905E2DD3FFBFC4C28F87F81CE93F	2024-11-14 14:30:40.86
62	AMBATO	HG	42	\N	01030000200674000001000000050000001B0966101EB7F1BFF443A732B246E83FF89F7A0B9566E5BF0F2090DD40CCE73F5CAA0D9918ADE6BFF0BC2F0204B2D33FBB02859E22EAF1BF0033088FDB67D63F1B0966101EB7F1BFF443A732B246E83F	2024-11-14 14:30:40.86
63	ANKAZO	FR	1A1	2E	01030000200674000001000000050000000D58EBC84D4D02C0A081A23C714ACA3F2BFB4958C1C3FBBF609F5D15A0F6A5BF304ECD15396A00C0AC8BF4D34A67D7BF6ED4F40EDBE502C0C89993CEB75AC9BF0D58EBC84D4D02C0A081A23C714ACA3F	2024-11-14 14:30:40.86
64	\N	DE	14F	\N	01030000200674000001000000050000006C3F61B341D8F4BF80A09BDD1657AA3FBC20C99988E0ECBF4043E003FC7CB63F5CD226875AB6EBBFB0FB7BE5361AB8BF0862646C7068F4BFD870D0078C5EC5BF6C3F61B341D8F4BF80A09BDD1657AA3F	2024-11-14 14:30:40.86
65	\N	ER	3R3	34R	010300002006740000010000000500000078C6EA54272007C006593EBD4938F03F252558DFE2C603C0E835CE445215E53FB10BF1C6844006C0B89A90273909D43F56CD5FCD83A708C098239603B101E13F78C6EA54272007C006593EBD4938F03F	2024-11-14 14:30:40.86
66	REF	\N	3R4	4R3	01030000200674000001000000050000003D734093B0050DC0F0705E974D06DB3F86F4B0D69A3C09C040B3D9D391C1A0BF826556A2F7F609C0208688C9F15AB6BF9CC1E2A5DE2F0EC04052F9CAE82CA93F3D734093B0050DC0F0705E974D06DB3F	2024-11-14 14:30:40.86
67	ER4	Z4T	\N	Z4G	01030000200674000001000000040000002853CE497A5AE53F66C4DB5438800140600BE75048CCED3FF38FE6802D73FC3F021C34993ECF883F631AF364E8B3FA3F2853CE497A5AE53F66C4DB5438800140	2024-11-14 14:30:40.86
68	432F	FZE4	Z4RZ	\N	0103000020067400000100000005000000000F9A362283BDBF29D37F2977FCF23FB00E1A7C413CD93FA8D2126AAE69E73F40725511C62EBBBF401084437EC8D53F4030426DF15AD5BFD8F96373C5FEE73F000F9A362283BDBF29D37F2977FCF23F	2024-11-14 14:30:40.86
69	sdgz	zrgz	zrg	zrz	0103000020067400000100000005000000D63A04E7F7BF03C0483EF7C3C137FB3FD12F11CB51D3FFBF90DAD1974F8DF83FBB4B438DF19B01C0A0982AB8D09AF13FF97DAADFF3A505C052A86A454D83F43FD63A04E7F7BF03C0483EF7C3C137FB3F	2024-11-14 14:30:40.86
\.


--
-- TOC entry 5246 (class 0 OID 0)
-- Dependencies: 230
-- Name: cadastre_gid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('cadastre_gid_seq', 69, true);


--
-- TOC entry 5011 (class 0 OID 1516231)
-- Dependencies: 231
-- Data for Name: categorie; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY categorie (idcategorie, libellecategorie, typeimposition, v_surface, valeur_location_ha, u_surface, v_venale, u_venale, taux, datemaj) FROM stdin;
\.


--
-- TOC entry 5247 (class 0 OID 0)
-- Dependencies: 232
-- Name: categorie_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('categorie_id_seq', 1, false);


--
-- TOC entry 5013 (class 0 OID 1516240)
-- Dependencies: 233
-- Data for Name: categorieforfaitaire; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY categorieforfaitaire (idcategorie, idforfaitaire, descripiton, valeurariary, valeurlocationbatiment, iftifpb, datemaj) FROM stdin;
\.


--
-- TOC entry 5014 (class 0 OID 1516246)
-- Dependencies: 234
-- Data for Name: certificat; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY certificat (numerocertificat, numerodemande, datereconnaissance, typecertificat, datecreation, dateedition, datedelivrance, memo, idcertificat, idfokontany, idprojet, isprint, idcommune, idhameau, code_hameau, datemaj) FROM stdin;
409-05-KT-3                                       	409-05-F-138                                      	2024-03-13	Certificat foncier                                	2024-04-28	\N	\N	\N	3	1	1	0	1	\N	\N	2024-11-14 14:30:40.86
409-05-KT-4                                       	409-05-F-139                                      	2023-04-20	Certificat foncier                                	2023-06-05	\N	\N	\N	4	1	1	0	1	\N	\N	2024-11-14 14:30:40.86
409-05-KT-5                                       	409-05-F-140                                      	2023-03-02	Certificat foncier                                	2023-04-17	\N	\N	\N	5	1	1	0	1	\N	\N	2024-11-14 14:30:40.86
409-05-KT-6                                       	409-05-F-141                                      	2023-03-02	Certificat foncier                                	2023-04-17	\N	\N	\N	6	1	1	0	1	\N	\N	2024-11-14 14:30:40.86
409-05-KT-7                                       	409-05-F-142                                      	2023-03-01	Certificat foncier                                	2023-04-16	\N	\N	\N	7	1	1	0	1	\N	\N	2024-11-14 14:30:40.86
409-05-KT-8                                       	409-05-F-143                                      	2023-04-11	Certificat foncier                                	2023-05-27	\N	\N	\N	8	1	1	0	1	\N	\N	2024-11-14 14:30:40.86
409-05-KT-9                                       	409-05-F-144                                      	2023-03-16	Certificat foncier                                	2023-05-01	\N	\N	\N	9	1	1	0	1	\N	\N	2024-11-14 14:30:40.86
409-05-KT-10                                      	409-05-F-145                                      	2023-03-17	Certificat foncier                                	2023-05-02	\N	\N	\N	10	1	1	0	1	\N	\N	2024-11-14 14:30:40.86
409-05-KT-11                                      	409-05-F-146                                      	2023-03-24	Certificat foncier                                	2023-05-09	\N	\N	\N	11	1	1	0	1	\N	\N	2024-11-14 14:30:40.86
409-05-KT-2                                       	409-05-F-8                                        	2023-06-14	Certificat Foncier                                	2000-01-01	\N	\N	\N	2	1	1	0	1	\N	\N	2024-11-14 14:30:40.86
409-05-KT-12                                      	409-05-F-147                                      	2021-12-22	Certificat foncier                                	2022-02-06	\N	\N	\N	12	1	1	0	1	\N	\N	2024-11-14 14:30:40.86
409-05-KT-13                                      	409-05-F-148                                      	2023-12-13	Certificat foncier                                	2024-01-28	\N	\N	\N	13	1	1	1	1	\N	\N	2024-11-14 14:30:40.86
409-05-KT-1                                       	409-05-F-3                                        	2023-05-20	Certificat foncier                                	2023-07-05	\N	\N	\N	1	1	1	1	1	\N	\N	2024-11-14 14:30:40.86
\.


--
-- TOC entry 5248 (class 0 OID 0)
-- Dependencies: 235
-- Name: certificat_idcertificat_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('certificat_idcertificat_seq', 13, true);


--
-- TOC entry 5016 (class 0 OID 1516255)
-- Dependencies: 236
-- Data for Name: classe; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY classe (idclasse, libelleclasse, datemaj) FROM stdin;
1	Classe A                        	2024-11-14 14:30:40.86
2	Classe B                        	2024-11-14 14:30:40.86
3	Classe C                        	2024-11-14 14:30:40.86
4	Classe D                        	2024-11-14 14:30:40.86
5	Classe E                        	2024-11-14 14:30:40.86
\.


--
-- TOC entry 5249 (class 0 OID 0)
-- Dependencies: 237
-- Name: classe_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('classe_id_seq', 1, false);


--
-- TOC entry 5018 (class 0 OID 1516260)
-- Dependencies: 238
-- Data for Name: classecategorieforfaitaire; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY classecategorieforfaitaire (idcategorie, idclasse, iftifpb, valeurariary, debut, fin, unite, datemaj) FROM stdin;
\.


--
-- TOC entry 5019 (class 0 OID 1516263)
-- Dependencies: 239
-- Data for Name: commune; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY commune (idcommune, iddistrict, codecommune, nomcommune, shapelength, shapearea, cptcertificat, cptimport, cptdemande, codeg, csv_id, maire, datemaj) FROM stdin;
1	1	05	AMPARIHY	\N	\N	14	1	149	5	\N	\N	2024-11-14 14:30:40.86
\.


--
-- TOC entry 5250 (class 0 OID 0)
-- Dependencies: 240
-- Name: commune_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('commune_id_seq', 1, true);


--
-- TOC entry 5149 (class 0 OID 2120344)
-- Dependencies: 379
-- Data for Name: configuration; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY configuration (id_configuration, host_remote, port_remote, user_remote, password_remote, dbname_remote, host_backup, port_backup, user_backup, password_backup, dbname_backup, auto_save_path, has_z_certifiable, online_interco, date_dernier_maj, date_dernier_autobackup) FROM stdin;
1	192.168.10.2	5432	user	\N	base	192.168.10.25	5432	user	\N	base	C:\\fiplof_interco\\dataFromField	f	t	2025-04-28 13:10:10.652	\N
\.


--
-- TOC entry 5251 (class 0 OID 0)
-- Dependencies: 378
-- Name: configuration_id_configuration_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('configuration_id_configuration_seq', 1, true);


--
-- TOC entry 5021 (class 0 OID 1516271)
-- Dependencies: 241
-- Data for Name: consistance; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY consistance (idconsistance, libelleconsistance, parcelleoubatiment, valeurariary, valeurariary_ifpb, datemaj) FROM stdin;
10	KORIMPA	KORIMPA                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         	\N	\N	2024-11-14 14:30:40.86
11	TANIMBARY SY TANIMBOY	TANIMBARY SY TANIMBOY                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           	\N	\N	2024-11-14 14:30:40.86
12	TANIMBOLY SY TANIMBARY	TANIMBOLY SY TANIMBARY                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          	\N	\N	2024-11-14 14:30:40.86
13	TANIMNOLY	TANIMNOLY                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       	\N	\N	2024-11-14 14:30:40.86
14	TANIMBARY SY TANIMBOLY	TANIMBARY SY TANIMBOLY                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          	\N	\N	2024-11-14 14:30:40.86
8	ALA	ALA                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             	0	0	2024-11-14 14:30:40.86
9	TANIMBOLY	TANIMBOLY                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       	0	0	2024-11-14 14:30:40.86
7	TANIMBARY	TANIMBARY                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       	0	0	2024-11-14 14:30:40.86
\.


--
-- TOC entry 5022 (class 0 OID 1516277)
-- Dependencies: 242
-- Data for Name: consistance_batiment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY consistance_batiment (id, consistance, mombamombanytany, valeurariary, valeur_location, datemaj) FROM stdin;
1	Tafo bozaka	Tafo bozaka	0	0	2024-11-14 14:30:40.86
2	Tafo fanitso	Tafo fanitso	0	0	2024-11-14 14:30:40.86
\.


--
-- TOC entry 5252 (class 0 OID 0)
-- Dependencies: 243
-- Name: consistance_batiment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('consistance_batiment_id_seq', 2, true);


--
-- TOC entry 5253 (class 0 OID 0)
-- Dependencies: 244
-- Name: consistance_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('consistance_id_seq', 14, true);


--
-- TOC entry 5025 (class 0 OID 1516286)
-- Dependencies: 245
-- Data for Name: consistanceforfaitaire; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY consistanceforfaitaire (idconsistance, idforfaitaire, prix, prixaveclocation, iftifpb, datemaj) FROM stdin;
\.


--
-- TOC entry 5027 (class 0 OID 1516291)
-- Dependencies: 247
-- Data for Name: contribuable; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY contribuable (idcontribuable, nom, datenaissance, lieu, cin, hetratany, hetratrano, idfkt, datereglement, prenom, adresse, datecin, numactenaissance, dateactenaissance, lieuactenaissance, sexe, idcontribuableconsorts, lieucin, etatpaiement, montantpayee, nevers, modecalcul, datemaj) FROM stdin;
\.


--
-- TOC entry 5254 (class 0 OID 0)
-- Dependencies: 246
-- Name: contribuable_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('contribuable_id_seq', 12, true);


--
-- TOC entry 5028 (class 0 OID 1516299)
-- Dependencies: 248
-- Data for Name: contribuableconsorts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY contribuableconsorts (idcontribuable, idconsort, datemaj) FROM stdin;
\.


--
-- TOC entry 5029 (class 0 OID 1516302)
-- Dependencies: 249
-- Data for Name: contribuables_parcelle; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY contribuables_parcelle (idpersonne, idparcelle, contribuable, datemaj) FROM stdin;
\.


--
-- TOC entry 5255 (class 0 OID 0)
-- Dependencies: 250
-- Name: crd_gid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('crd_gid_seq', 1569, true);


--
-- TOC entry 5147 (class 0 OID 1529594)
-- Dependencies: 377
-- Data for Name: date_synchro; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY date_synchro (id_synchro, date_synchro, datemaj) FROM stdin;
\.


--
-- TOC entry 5256 (class 0 OID 0)
-- Dependencies: 376
-- Name: date_synchro_id_synchro_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('date_synchro_id_synchro_seq', 1, false);


--
-- TOC entry 5031 (class 0 OID 1516313)
-- Dependencies: 251
-- Data for Name: decisionsubsequente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY decisionsubsequente (idoperationsubsequente, iddecision, datemaj) FROM stdin;
\.


--
-- TOC entry 5032 (class 0 OID 1516316)
-- Dependencies: 252
-- Data for Name: demande; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY demande (iddemande, id, numdemande, nomdemandeur, surface, parcelle, etat_cf, geom, gid, datedemande, datereconnaissance, region, district, commune, fokontany, titre, idfokontany, idcommune, idrejet, cout, consistance, idprojet, numdemandepaps, datedecision, csv_id, code_parcelle, categorie, opposition, planche_plof, charges, numdecision, debut_affichage, fin_affichage, numero_demande_lrsys, pvrl, cqe, date_cqe, resp_cqe, user_cqe, lieudit, collecteur_demande, duree_occupation, origine, avis_crl, texte_crl, sous_reserve, datemaj, num_guichet_foncier) FROM stdin;
\.


--
-- TOC entry 5033 (class 0 OID 1516323)
-- Dependencies: 253
-- Data for Name: demande_anomalie; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY demande_anomalie (iddemande, idanomalie, datemaj) FROM stdin;
\.


--
-- TOC entry 5034 (class 0 OID 1516326)
-- Dependencies: 254
-- Data for Name: demande_crl; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY demande_crl (idpersonne, iddemande, id_role, rl, affiche, titulaire, president, datemaj) FROM stdin;
\.


--
-- TOC entry 5036 (class 0 OID 1516332)
-- Dependencies: 256
-- Data for Name: demande_sans_geom; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY demande_sans_geom (iddemande, id, numdemande, nomdemandeur, surface, parcelle, etat_cf, geom, gid, datedemande, datereconnaissance, region, district, commune, fokontany, titre, idfokontany, idcommune, idrejet, cout, consistance, idprojet, numdemandepaps, datedecision, csv_id, code_parcelle, categorie, opposition, planche_plof, charges, datemaj) FROM stdin;
\.


--
-- TOC entry 5037 (class 0 OID 1516348)
-- Dependencies: 257
-- Data for Name: demandefn; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY demandefn (gid, fn_fg, demandeur, sur_plan, geom, datemaj) FROM stdin;
58	23ZE	ZERZ	34	010300002006740000010000000600000000D23738E05908C0EECB24D83B08084000D23738E05908C0EECB24D83B080840005BBADAAA93A5BF04762CBA3A16E83FF8D0C9E216E106C0B0D945E5F2A820C0495D82E2B82E18C0BC6A57CC762FEB3F00D23738E05908C0EECB24D83B080840	2024-11-14 14:30:40.86
59	EZR	AETF	35	01030000200674000001000000050000007E6444545D172CC020189962D85C0D4091402BFC2D2924C00433B2494790F83F865400660F9128C0C8D8D1DD2434FEBFB0D8DBF8E30230C02074F102EC03DF3F7E6444545D172CC020189962D85C0D40	2024-11-14 14:30:40.86
\.


--
-- TOC entry 5257 (class 0 OID 0)
-- Dependencies: 258
-- Name: demandefn_gid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('demandefn_gid_seq', 59, true);


--
-- TOC entry 5039 (class 0 OID 1516364)
-- Dependencies: 259
-- Data for Name: district; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY district (iddistrict, idregion, codedistrict, nomdistrict, shapelength, shapearea, csv_id, datemaj) FROM stdin;
1	1	409	PORT BERGE	\N	\N	\N	2024-11-14 14:30:40.86
\.


--
-- TOC entry 5258 (class 0 OID 0)
-- Dependencies: 260
-- Name: district_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('district_id_seq', 1, true);


--
-- TOC entry 5041 (class 0 OID 1516369)
-- Dependencies: 261
-- Data for Name: document; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY document (id_document, photo_document, extension_document, num_page, observation, id_type, iddemande, datemaj) FROM stdin;
\.


--
-- TOC entry 5259 (class 0 OID 0)
-- Dependencies: 262
-- Name: document_id_document_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('document_id_document_seq', 1, false);


--
-- TOC entry 5043 (class 0 OID 1516385)
-- Dependencies: 263
-- Data for Name: fi_paiement_impot; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY fi_paiement_impot (id_paiement, date, montant, numquittance, idpersonne, datemaj) FROM stdin;
\.


--
-- TOC entry 5260 (class 0 OID 0)
-- Dependencies: 264
-- Name: fi_paiement_impot_id_paiement_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('fi_paiement_impot_id_paiement_seq', 1, false);


--
-- TOC entry 5045 (class 0 OID 1516390)
-- Dependencies: 265
-- Data for Name: fokontany; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY fokontany (idfokontany, idcommune, codefokontany, nomfokontany, shapelength, shapearea, csv_id, datemaj) FROM stdin;
1	1	1	AMBODIMANGA II	\N	\N	\N	2024-11-14 14:30:40.86
\.


--
-- TOC entry 5261 (class 0 OID 0)
-- Dependencies: 266
-- Name: fokontany_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('fokontany_id_seq', 1, true);


--
-- TOC entry 5047 (class 0 OID 1516398)
-- Dependencies: 267
-- Data for Name: groupe; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY groupe (id, nom, description, datemaj) FROM stdin;
1	Admin	Administrateur de l'application	2024-11-14 14:30:40.86
5	Responsable Commune	 Responsable des communes	2024-11-14 14:30:40.86
10	Guichet Foncier	 Agent Guichet Foncier	2024-11-14 14:30:40.86
11	Assistants Techniques	Assistants Techniques 	2024-11-14 14:30:40.86
12	Formateur	 Formateur	2024-11-14 14:30:40.86
13	Guichet Unique (TOPO)	 TOPO pour mise à jour PLOF	2024-11-14 14:30:40.86
14	Disposition Transitoire	 Disposition Transitoire	2024-11-14 14:30:40.86
\.


--
-- TOC entry 5048 (class 0 OID 1516404)
-- Dependencies: 268
-- Data for Name: groupe_acces; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY groupe_acces (id, groupe_id, acces_id, autorise, datemaj) FROM stdin;
188	10	3	t	2024-11-14 14:30:40.86
189	10	4	t	2024-11-14 14:30:40.86
22	5	2	t	2024-11-14 14:30:40.86
23	5	3	f	2024-11-14 14:30:40.86
24	5	4	f	2024-11-14 14:30:40.86
135	5	35	f	2024-11-14 14:30:40.86
136	5	36	f	2024-11-14 14:30:40.86
137	5	37	f	2024-11-14 14:30:40.86
144	5	75	f	2024-11-14 14:30:40.86
30	5	6	t	2024-11-14 14:30:40.86
31	5	7	f	2024-11-14 14:30:40.86
32	5	8	f	2024-11-14 14:30:40.86
124	5	21	t	2024-11-14 14:30:40.86
125	5	23	f	2024-11-14 14:30:40.86
138	5	40	f	2024-11-14 14:30:40.86
139	5	41	f	2024-11-14 14:30:40.86
33	5	9	f	2024-11-14 14:30:40.86
34	5	10	f	2024-11-14 14:30:40.86
35	5	11	f	2024-11-14 14:30:40.86
36	5	12	f	2024-11-14 14:30:40.86
37	5	13	f	2024-11-14 14:30:40.86
38	5	14	f	2024-11-14 14:30:40.86
53	5	15	f	2024-11-14 14:30:40.86
54	5	16	f	2024-11-14 14:30:40.86
55	5	17	f	2024-11-14 14:30:40.86
56	5	18	f	2024-11-14 14:30:40.86
57	5	19	f	2024-11-14 14:30:40.86
126	5	24	f	2024-11-14 14:30:40.86
127	5	25	f	2024-11-14 14:30:40.86
128	5	26	f	2024-11-14 14:30:40.86
129	5	27	f	2024-11-14 14:30:40.86
130	5	28	f	2024-11-14 14:30:40.86
131	5	29	t	2024-11-14 14:30:40.86
132	5	30	f	2024-11-14 14:30:40.86
145	5	42	f	2024-11-14 14:30:40.86
141	5	34	f	2024-11-14 14:30:40.86
142	5	38	f	2024-11-14 14:30:40.86
143	5	39	f	2024-11-14 14:30:40.86
146	5	43	t	2024-11-14 14:30:40.86
190	10	35	t	2024-11-14 14:30:40.86
191	10	36	t	2024-11-14 14:30:40.86
192	10	37	t	2024-11-14 14:30:40.86
193	10	75	t	2024-11-14 14:30:40.86
194	10	5	t	2024-11-14 14:30:40.86
195	10	6	t	2024-11-14 14:30:40.86
198	10	21	t	2024-11-14 14:30:40.86
199	10	23	f	2024-11-14 14:30:40.86
200	10	40	t	2024-11-14 14:30:40.86
201	10	41	f	2024-11-14 14:30:40.86
202	10	9	t	2024-11-14 14:30:40.86
203	10	10	t	2024-11-14 14:30:40.86
204	10	11	t	2024-11-14 14:30:40.86
205	10	12	t	2024-11-14 14:30:40.86
206	10	13	t	2024-11-14 14:30:40.86
207	10	14	t	2024-11-14 14:30:40.86
208	10	15	t	2024-11-14 14:30:40.86
209	10	16	t	2024-11-14 14:30:40.86
210	10	17	t	2024-11-14 14:30:40.86
211	10	18	t	2024-11-14 14:30:40.86
213	10	24	t	2024-11-14 14:30:40.86
214	10	25	t	2024-11-14 14:30:40.86
215	10	26	t	2024-11-14 14:30:40.86
216	10	27	t	2024-11-14 14:30:40.86
217	10	28	t	2024-11-14 14:30:40.86
218	10	29	t	2024-11-14 14:30:40.86
219	10	30	t	2024-11-14 14:30:40.86
220	10	42	t	2024-11-14 14:30:40.86
221	10	33	t	2024-11-14 14:30:40.86
222	10	34	t	2024-11-14 14:30:40.86
223	10	38	t	2024-11-14 14:30:40.86
224	10	39	t	2024-11-14 14:30:40.86
225	10	43	t	2024-11-14 14:30:40.86
226	10	76	t	2024-11-14 14:30:40.86
228	10	45	f	2024-11-14 14:30:40.86
229	10	46	f	2024-11-14 14:30:40.86
230	10	47	t	2024-11-14 14:30:40.86
231	10	48	t	2024-11-14 14:30:40.86
232	10	49	t	2024-11-14 14:30:40.86
233	10	50	t	2024-11-14 14:30:40.86
234	10	51	t	2024-11-14 14:30:40.86
235	10	52	t	2024-11-14 14:30:40.86
236	10	53	t	2024-11-14 14:30:40.86
237	10	54	f	2024-11-14 14:30:40.86
238	10	55	t	2024-11-14 14:30:40.86
239	10	56	t	2024-11-14 14:30:40.86
21	5	1	f	2024-11-14 14:30:40.86
29	5	5	f	2024-11-14 14:30:40.86
140	5	33	f	2024-11-14 14:30:40.86
147	5	76	f	2024-11-14 14:30:40.86
148	5	77	f	2024-11-14 14:30:40.86
149	5	45	f	2024-11-14 14:30:40.86
151	5	47	f	2024-11-14 14:30:40.86
152	5	48	f	2024-11-14 14:30:40.86
153	5	49	f	2024-11-14 14:30:40.86
154	5	50	f	2024-11-14 14:30:40.86
155	5	51	f	2024-11-14 14:30:40.86
156	5	52	f	2024-11-14 14:30:40.86
157	5	53	f	2024-11-14 14:30:40.86
158	5	54	f	2024-11-14 14:30:40.86
159	5	55	f	2024-11-14 14:30:40.86
160	5	56	f	2024-11-14 14:30:40.86
161	5	57	f	2024-11-14 14:30:40.86
162	5	58	f	2024-11-14 14:30:40.86
163	5	59	f	2024-11-14 14:30:40.86
164	5	60	f	2024-11-14 14:30:40.86
166	5	62	f	2024-11-14 14:30:40.86
167	5	63	f	2024-11-14 14:30:40.86
168	5	64	f	2024-11-14 14:30:40.86
169	5	65	t	2024-11-14 14:30:40.86
170	5	66	f	2024-11-14 14:30:40.86
171	5	67	f	2024-11-14 14:30:40.86
172	5	68	f	2024-11-14 14:30:40.86
173	5	69	t	2024-11-14 14:30:40.86
174	5	70	f	2024-11-14 14:30:40.86
175	5	71	f	2024-11-14 14:30:40.86
176	5	72	f	2024-11-14 14:30:40.86
177	5	73	f	2024-11-14 14:30:40.86
178	5	74	f	2024-11-14 14:30:40.86
179	5	78	f	2024-11-14 14:30:40.86
181	5	83	f	2024-11-14 14:30:40.86
182	5	80	f	2024-11-14 14:30:40.86
183	5	81	f	2024-11-14 14:30:40.86
184	5	82	f	2024-11-14 14:30:40.86
185	5	84	f	2024-11-14 14:30:40.86
187	10	2	t	2024-11-14 14:30:40.86
242	10	59	t	2024-11-14 14:30:40.86
243	10	60	t	2024-11-14 14:30:40.86
244	10	61	t	2024-11-14 14:30:40.86
245	10	62	t	2024-11-14 14:30:40.86
246	10	63	t	2024-11-14 14:30:40.86
247	10	64	t	2024-11-14 14:30:40.86
248	10	65	t	2024-11-14 14:30:40.86
249	10	66	t	2024-11-14 14:30:40.86
250	10	67	t	2024-11-14 14:30:40.86
251	10	68	t	2024-11-14 14:30:40.86
252	10	69	t	2024-11-14 14:30:40.86
253	10	70	f	2024-11-14 14:30:40.86
254	10	71	f	2024-11-14 14:30:40.86
255	10	72	f	2024-11-14 14:30:40.86
256	10	73	f	2024-11-14 14:30:40.86
257	10	74	f	2024-11-14 14:30:40.86
258	10	78	f	2024-11-14 14:30:40.86
259	10	79	f	2024-11-14 14:30:40.86
260	10	83	f	2024-11-14 14:30:40.86
261	10	80	f	2024-11-14 14:30:40.86
262	10	81	f	2024-11-14 14:30:40.86
263	10	82	f	2024-11-14 14:30:40.86
264	10	84	t	2024-11-14 14:30:40.86
265	11	1	t	2024-11-14 14:30:40.86
266	11	2	t	2024-11-14 14:30:40.86
267	11	3	t	2024-11-14 14:30:40.86
268	11	4	t	2024-11-14 14:30:40.86
269	11	35	t	2024-11-14 14:30:40.86
270	11	36	t	2024-11-14 14:30:40.86
271	11	37	t	2024-11-14 14:30:40.86
272	11	75	t	2024-11-14 14:30:40.86
273	11	5	t	2024-11-14 14:30:40.86
274	11	6	t	2024-11-14 14:30:40.86
275	11	7	t	2024-11-14 14:30:40.86
276	11	8	t	2024-11-14 14:30:40.86
277	11	21	t	2024-11-14 14:30:40.86
278	11	23	f	2024-11-14 14:30:40.86
279	11	40	t	2024-11-14 14:30:40.86
280	11	41	f	2024-11-14 14:30:40.86
281	11	9	t	2024-11-14 14:30:40.86
282	11	10	t	2024-11-14 14:30:40.86
283	11	11	t	2024-11-14 14:30:40.86
284	11	12	t	2024-11-14 14:30:40.86
285	11	13	t	2024-11-14 14:30:40.86
286	11	14	t	2024-11-14 14:30:40.86
287	11	15	t	2024-11-14 14:30:40.86
288	11	16	t	2024-11-14 14:30:40.86
289	11	17	t	2024-11-14 14:30:40.86
290	11	18	t	2024-11-14 14:30:40.86
291	11	19	t	2024-11-14 14:30:40.86
292	11	24	f	2024-11-14 14:30:40.86
293	11	25	f	2024-11-14 14:30:40.86
294	11	26	f	2024-11-14 14:30:40.86
295	11	27	f	2024-11-14 14:30:40.86
296	11	28	f	2024-11-14 14:30:40.86
297	11	29	f	2024-11-14 14:30:40.86
298	11	30	f	2024-11-14 14:30:40.86
299	11	42	f	2024-11-14 14:30:40.86
300	11	33	t	2024-11-14 14:30:40.86
301	11	34	t	2024-11-14 14:30:40.86
302	11	38	t	2024-11-14 14:30:40.86
303	11	39	t	2024-11-14 14:30:40.86
304	11	43	t	2024-11-14 14:30:40.86
305	11	76	t	2024-11-14 14:30:40.86
306	11	77	t	2024-11-14 14:30:40.86
307	11	45	t	2024-11-14 14:30:40.86
308	11	46	t	2024-11-14 14:30:40.86
309	11	47	t	2024-11-14 14:30:40.86
310	11	48	t	2024-11-14 14:30:40.86
311	11	49	t	2024-11-14 14:30:40.86
312	11	50	t	2024-11-14 14:30:40.86
313	11	51	t	2024-11-14 14:30:40.86
314	11	52	f	2024-11-14 14:30:40.86
315	11	53	t	2024-11-14 14:30:40.86
316	11	54	f	2024-11-14 14:30:40.86
317	11	55	t	2024-11-14 14:30:40.86
318	11	56	t	2024-11-14 14:30:40.86
319	11	57	t	2024-11-14 14:30:40.86
320	11	58	t	2024-11-14 14:30:40.86
321	11	59	t	2024-11-14 14:30:40.86
322	11	60	t	2024-11-14 14:30:40.86
323	11	61	t	2024-11-14 14:30:40.86
324	11	62	t	2024-11-14 14:30:40.86
325	11	63	t	2024-11-14 14:30:40.86
326	11	64	t	2024-11-14 14:30:40.86
327	11	65	t	2024-11-14 14:30:40.86
328	11	66	t	2024-11-14 14:30:40.86
329	11	67	t	2024-11-14 14:30:40.86
330	11	68	t	2024-11-14 14:30:40.86
331	11	69	t	2024-11-14 14:30:40.86
332	11	70	f	2024-11-14 14:30:40.86
333	11	71	t	2024-11-14 14:30:40.86
334	11	72	t	2024-11-14 14:30:40.86
335	11	73	t	2024-11-14 14:30:40.86
336	11	74	f	2024-11-14 14:30:40.86
337	11	78	t	2024-11-14 14:30:40.86
338	11	79	t	2024-11-14 14:30:40.86
339	11	83	f	2024-11-14 14:30:40.86
340	11	80	t	2024-11-14 14:30:40.86
341	11	81	t	2024-11-14 14:30:40.86
342	11	82	t	2024-11-14 14:30:40.86
343	11	84	f	2024-11-14 14:30:40.86
345	12	2	t	2024-11-14 14:30:40.86
346	12	3	t	2024-11-14 14:30:40.86
212	10	19	t	2024-11-14 14:30:40.86
227	10	77	t	2024-11-14 14:30:40.86
241	10	58	f	2024-11-14 14:30:40.86
347	12	4	t	2024-11-14 14:30:40.86
348	12	35	t	2024-11-14 14:30:40.86
349	12	36	t	2024-11-14 14:30:40.86
350	12	37	t	2024-11-14 14:30:40.86
351	12	75	t	2024-11-14 14:30:40.86
352	12	5	t	2024-11-14 14:30:40.86
353	12	6	t	2024-11-14 14:30:40.86
354	12	7	t	2024-11-14 14:30:40.86
355	12	8	t	2024-11-14 14:30:40.86
356	12	21	t	2024-11-14 14:30:40.86
357	12	23	f	2024-11-14 14:30:40.86
358	12	40	t	2024-11-14 14:30:40.86
360	12	9	t	2024-11-14 14:30:40.86
361	12	10	t	2024-11-14 14:30:40.86
362	12	11	t	2024-11-14 14:30:40.86
363	12	12	t	2024-11-14 14:30:40.86
364	12	13	t	2024-11-14 14:30:40.86
344	12	1	t	2024-11-14 14:30:40.86
197	10	8	f	2024-11-14 14:30:40.86
368	12	17	t	2024-11-14 14:30:40.86
369	12	18	t	2024-11-14 14:30:40.86
370	12	19	t	2024-11-14 14:30:40.86
371	12	24	t	2024-11-14 14:30:40.86
372	12	25	t	2024-11-14 14:30:40.86
373	12	26	t	2024-11-14 14:30:40.86
427	13	35	f	2024-11-14 14:30:40.86
428	13	36	f	2024-11-14 14:30:40.86
429	13	37	f	2024-11-14 14:30:40.86
430	13	75	f	2024-11-14 14:30:40.86
431	13	5	f	2024-11-14 14:30:40.86
432	13	6	t	2024-11-14 14:30:40.86
433	13	7	f	2024-11-14 14:30:40.86
434	13	8	f	2024-11-14 14:30:40.86
435	13	21	f	2024-11-14 14:30:40.86
436	13	23	f	2024-11-14 14:30:40.86
437	13	40	f	2024-11-14 14:30:40.86
438	13	41	f	2024-11-14 14:30:40.86
439	13	9	f	2024-11-14 14:30:40.86
440	13	10	f	2024-11-14 14:30:40.86
442	13	12	f	2024-11-14 14:30:40.86
443	13	13	f	2024-11-14 14:30:40.86
444	13	14	f	2024-11-14 14:30:40.86
445	13	15	f	2024-11-14 14:30:40.86
446	13	16	f	2024-11-14 14:30:40.86
447	13	17	f	2024-11-14 14:30:40.86
448	13	18	f	2024-11-14 14:30:40.86
449	13	19	f	2024-11-14 14:30:40.86
450	13	24	f	2024-11-14 14:30:40.86
451	13	25	f	2024-11-14 14:30:40.86
452	13	26	f	2024-11-14 14:30:40.86
453	13	27	f	2024-11-14 14:30:40.86
454	13	28	f	2024-11-14 14:30:40.86
455	13	29	f	2024-11-14 14:30:40.86
457	13	42	f	2024-11-14 14:30:40.86
458	13	33	f	2024-11-14 14:30:40.86
459	13	34	f	2024-11-14 14:30:40.86
460	13	38	f	2024-11-14 14:30:40.86
461	13	39	f	2024-11-14 14:30:40.86
462	13	43	t	2024-11-14 14:30:40.86
464	13	77	t	2024-11-14 14:30:40.86
465	13	45	f	2024-11-14 14:30:40.86
466	13	46	f	2024-11-14 14:30:40.86
467	13	47	f	2024-11-14 14:30:40.86
468	13	48	t	2024-11-14 14:30:40.86
469	13	49	f	2024-11-14 14:30:40.86
470	13	50	f	2024-11-14 14:30:40.86
472	13	52	f	2024-11-14 14:30:40.86
473	13	53	f	2024-11-14 14:30:40.86
474	13	54	f	2024-11-14 14:30:40.86
475	13	55	t	2024-11-14 14:30:40.86
476	13	56	f	2024-11-14 14:30:40.86
477	13	57	f	2024-11-14 14:30:40.86
478	13	58	f	2024-11-14 14:30:40.86
479	13	59	f	2024-11-14 14:30:40.86
480	13	60	f	2024-11-14 14:30:40.86
481	13	61	f	2024-11-14 14:30:40.86
482	13	62	f	2024-11-14 14:30:40.86
483	13	63	f	2024-11-14 14:30:40.86
484	13	64	f	2024-11-14 14:30:40.86
485	13	65	f	2024-11-14 14:30:40.86
487	13	67	f	2024-11-14 14:30:40.86
488	13	68	f	2024-11-14 14:30:40.86
489	13	69	t	2024-11-14 14:30:40.86
490	13	70	t	2024-11-14 14:30:40.86
491	13	71	f	2024-11-14 14:30:40.86
492	13	72	f	2024-11-14 14:30:40.86
493	13	73	t	2024-11-14 14:30:40.86
494	13	74	t	2024-11-14 14:30:40.86
495	13	78	f	2024-11-14 14:30:40.86
496	13	79	f	2024-11-14 14:30:40.86
497	13	83	f	2024-11-14 14:30:40.86
498	13	80	t	2024-11-14 14:30:40.86
499	13	81	t	2024-11-14 14:30:40.86
500	13	82	t	2024-11-14 14:30:40.86
367	12	16	t	2024-11-14 14:30:40.86
374	12	27	t	2024-11-14 14:30:40.86
375	12	28	t	2024-11-14 14:30:40.86
376	12	29	t	2024-11-14 14:30:40.86
377	12	30	t	2024-11-14 14:30:40.86
378	12	42	t	2024-11-14 14:30:40.86
379	12	33	t	2024-11-14 14:30:40.86
380	12	34	t	2024-11-14 14:30:40.86
381	12	38	t	2024-11-14 14:30:40.86
382	12	39	t	2024-11-14 14:30:40.86
383	12	43	t	2024-11-14 14:30:40.86
384	12	76	t	2024-11-14 14:30:40.86
385	12	77	t	2024-11-14 14:30:40.86
387	12	46	t	2024-11-14 14:30:40.86
388	12	47	t	2024-11-14 14:30:40.86
389	12	48	t	2024-11-14 14:30:40.86
390	12	49	t	2024-11-14 14:30:40.86
391	12	50	t	2024-11-14 14:30:40.86
392	12	51	t	2024-11-14 14:30:40.86
393	12	52	t	2024-11-14 14:30:40.86
394	12	53	t	2024-11-14 14:30:40.86
395	12	54	t	2024-11-14 14:30:40.86
396	12	55	t	2024-11-14 14:30:40.86
397	12	56	t	2024-11-14 14:30:40.86
398	12	57	t	2024-11-14 14:30:40.86
399	12	58	t	2024-11-14 14:30:40.86
400	12	59	t	2024-11-14 14:30:40.86
402	12	61	t	2024-11-14 14:30:40.86
403	12	62	t	2024-11-14 14:30:40.86
404	12	63	t	2024-11-14 14:30:40.86
405	12	64	t	2024-11-14 14:30:40.86
406	12	65	t	2024-11-14 14:30:40.86
407	12	66	t	2024-11-14 14:30:40.86
408	12	67	t	2024-11-14 14:30:40.86
409	12	68	t	2024-11-14 14:30:40.86
410	12	69	t	2024-11-14 14:30:40.86
411	12	70	t	2024-11-14 14:30:40.86
412	12	71	t	2024-11-14 14:30:40.86
413	12	72	t	2024-11-14 14:30:40.86
414	12	73	t	2024-11-14 14:30:40.86
415	12	74	t	2024-11-14 14:30:40.86
417	12	79	t	2024-11-14 14:30:40.86
418	12	83	f	2024-11-14 14:30:40.86
419	12	80	t	2024-11-14 14:30:40.86
420	12	81	t	2024-11-14 14:30:40.86
421	12	82	t	2024-11-14 14:30:40.86
422	12	84	f	2024-11-14 14:30:40.86
424	13	2	t	2024-11-14 14:30:40.86
366	12	15	t	2024-11-14 14:30:40.86
425	13	3	f	2024-11-14 14:30:40.86
544	14	45	t	2024-11-14 14:30:40.86
502	14	1	t	2024-11-14 14:30:40.86
503	14	2	t	2024-11-14 14:30:40.86
504	14	3	t	2024-11-14 14:30:40.86
505	14	4	t	2024-11-14 14:30:40.86
506	14	35	t	2024-11-14 14:30:40.86
507	14	36	t	2024-11-14 14:30:40.86
508	14	37	t	2024-11-14 14:30:40.86
523	14	14	t	2024-11-14 14:30:40.86
524	14	15	t	2024-11-14 14:30:40.86
525	14	16	t	2024-11-14 14:30:40.86
526	14	17	t	2024-11-14 14:30:40.86
527	14	18	t	2024-11-14 14:30:40.86
528	14	19	t	2024-11-14 14:30:40.86
530	14	25	f	2024-11-14 14:30:40.86
531	14	26	f	2024-11-14 14:30:40.86
532	14	27	f	2024-11-14 14:30:40.86
533	14	28	f	2024-11-14 14:30:40.86
534	14	29	f	2024-11-14 14:30:40.86
535	14	30	f	2024-11-14 14:30:40.86
536	14	42	f	2024-11-14 14:30:40.86
537	14	33	t	2024-11-14 14:30:40.86
538	14	34	t	2024-11-14 14:30:40.86
539	14	38	t	2024-11-14 14:30:40.86
540	14	39	t	2024-11-14 14:30:40.86
541	14	43	t	2024-11-14 14:30:40.86
542	14	76	t	2024-11-14 14:30:40.86
543	14	77	t	2024-11-14 14:30:40.86
545	14	46	t	2024-11-14 14:30:40.86
546	14	47	t	2024-11-14 14:30:40.86
547	14	48	t	2024-11-14 14:30:40.86
548	14	49	t	2024-11-14 14:30:40.86
549	14	50	t	2024-11-14 14:30:40.86
550	14	51	t	2024-11-14 14:30:40.86
551	14	52	f	2024-11-14 14:30:40.86
552	14	53	t	2024-11-14 14:30:40.86
553	14	54	f	2024-11-14 14:30:40.86
554	14	55	t	2024-11-14 14:30:40.86
555	14	56	t	2024-11-14 14:30:40.86
556	14	57	t	2024-11-14 14:30:40.86
557	14	58	f	2024-11-14 14:30:40.86
558	14	59	t	2024-11-14 14:30:40.86
559	14	60	t	2024-11-14 14:30:40.86
560	14	61	t	2024-11-14 14:30:40.86
561	14	62	t	2024-11-14 14:30:40.86
562	14	63	t	2024-11-14 14:30:40.86
563	14	64	t	2024-11-14 14:30:40.86
564	14	65	f	2024-11-14 14:30:40.86
565	14	66	t	2024-11-14 14:30:40.86
566	14	67	t	2024-11-14 14:30:40.86
567	14	68	t	2024-11-14 14:30:40.86
568	14	69	t	2024-11-14 14:30:40.86
569	14	70	t	2024-11-14 14:30:40.86
570	14	71	t	2024-11-14 14:30:40.86
571	14	72	t	2024-11-14 14:30:40.86
572	14	73	t	2024-11-14 14:30:40.86
573	14	74	t	2024-11-14 14:30:40.86
574	14	78	t	2024-11-14 14:30:40.86
575	14	79	t	2024-11-14 14:30:40.86
576	14	83	t	2024-11-14 14:30:40.86
577	14	80	t	2024-11-14 14:30:40.86
578	14	81	t	2024-11-14 14:30:40.86
579	14	82	t	2024-11-14 14:30:40.86
580	14	84	f	2024-11-14 14:30:40.86
150	5	46	f	2024-11-14 14:30:40.86
165	5	61	f	2024-11-14 14:30:40.86
180	5	79	f	2024-11-14 14:30:40.86
186	10	1	t	2024-11-14 14:30:40.86
240	10	57	t	2024-11-14 14:30:40.86
509	14	75	t	2024-11-14 14:30:40.86
510	14	5	t	2024-11-14 14:30:40.86
511	14	6	t	2024-11-14 14:30:40.86
512	14	7	t	2024-11-14 14:30:40.86
513	14	8	t	2024-11-14 14:30:40.86
359	12	41	f	2024-11-14 14:30:40.86
365	12	14	t	2024-11-14 14:30:40.86
386	12	45	t	2024-11-14 14:30:40.86
401	12	60	t	2024-11-14 14:30:40.86
416	12	78	t	2024-11-14 14:30:40.86
423	13	1	f	2024-11-14 14:30:40.86
426	13	4	f	2024-11-14 14:30:40.86
441	13	11	f	2024-11-14 14:30:40.86
456	13	30	f	2024-11-14 14:30:40.86
471	13	51	f	2024-11-14 14:30:40.86
486	13	66	f	2024-11-14 14:30:40.86
501	13	84	f	2024-11-14 14:30:40.86
514	14	21	t	2024-11-14 14:30:40.86
515	14	23	f	2024-11-14 14:30:40.86
516	14	40	t	2024-11-14 14:30:40.86
517	14	41	f	2024-11-14 14:30:40.86
518	14	9	t	2024-11-14 14:30:40.86
519	14	10	t	2024-11-14 14:30:40.86
520	14	11	t	2024-11-14 14:30:40.86
521	14	12	t	2024-11-14 14:30:40.86
522	14	13	t	2024-11-14 14:30:40.86
529	14	24	t	2024-11-14 14:30:40.86
581	14	86	t	2024-11-14 14:30:40.86
196	10	7	t	2024-11-14 14:30:40.86
463	13	76	t	2025-04-28 13:10:09.308
\.


--
-- TOC entry 5262 (class 0 OID 0)
-- Dependencies: 269
-- Name: groupe_acces_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('groupe_acces_id_seq', 581, true);


--
-- TOC entry 5263 (class 0 OID 0)
-- Dependencies: 270
-- Name: groupe_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('groupe_id_seq', 14, true);


--
-- TOC entry 5051 (class 0 OID 1516411)
-- Dependencies: 271
-- Data for Name: hameau; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY hameau (idhameau, idfokontany, codehameau, nomhameau, shapelength, shapearea, csv_id, datemaj) FROM stdin;
1	1	A	ANDILAMBE	\N	\N	\N	2024-11-14 14:30:40.86
\.


--
-- TOC entry 5264 (class 0 OID 0)
-- Dependencies: 272
-- Name: hameau_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('hameau_id_seq', 1, true);


--
-- TOC entry 5053 (class 0 OID 1516416)
-- Dependencies: 273
-- Data for Name: historique; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY historique (idhistorique, typeoperation, dateoperation, idcertificat, datemaj) FROM stdin;
\.


--
-- TOC entry 5265 (class 0 OID 0)
-- Dependencies: 274
-- Name: historique_idhistorique_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('historique_idhistorique_seq', 58, true);


--
-- TOC entry 5055 (class 0 OID 1516421)
-- Dependencies: 275
-- Data for Name: hypotheque; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY hypotheque (dateinscriptionregistre, duree, valeur, creancier, descriptionhypotheque, dateradiation, idhypotheque, datemaj) FROM stdin;
\.


--
-- TOC entry 5266 (class 0 OID 0)
-- Dependencies: 276
-- Name: hypotheque_idhypotheque_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('hypotheque_idhypotheque_seq', 6, true);


--
-- TOC entry 5057 (class 0 OID 1516429)
-- Dependencies: 277
-- Data for Name: hypothequeparcelle_d; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY hypothequeparcelle_d (idhypotheque, idparcelle, datemaj) FROM stdin;
\.


--
-- TOC entry 5267 (class 0 OID 0)
-- Dependencies: 278
-- Name: iddemande_sans_geom_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('iddemande_sans_geom_seq', 5241, false);


--
-- TOC entry 5268 (class 0 OID 0)
-- Dependencies: 255
-- Name: iddemande_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('iddemande_seq', 282, true);


--
-- TOC entry 5269 (class 0 OID 0)
-- Dependencies: 279
-- Name: idprojet_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('idprojet_seq', 1, false);


--
-- TOC entry 5060 (class 0 OID 1516436)
-- Dependencies: 280
-- Data for Name: impot; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY impot (idimpot, numquittanceimpot, anneeimpot, dateimpot, datemaj) FROM stdin;
\.


--
-- TOC entry 5061 (class 0 OID 1516439)
-- Dependencies: 281
-- Data for Name: impot_batiment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY impot_batiment (id, hetratrano, annee, codebatiment, montant_paye, datemaj) FROM stdin;
\.


--
-- TOC entry 5270 (class 0 OID 0)
-- Dependencies: 282
-- Name: impot_batiment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('impot_batiment_id_seq', 1, false);


--
-- TOC entry 5063 (class 0 OID 1516444)
-- Dependencies: 283
-- Data for Name: impot_contribuable; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY impot_contribuable (id, hetratrano, hetratany, etatpaiement, annee, datereglement, montantpaye, idpersonne, datemaj) FROM stdin;
\.


--
-- TOC entry 5271 (class 0 OID 0)
-- Dependencies: 284
-- Name: impot_contribuable_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('impot_contribuable_id_seq', 1, false);


--
-- TOC entry 5272 (class 0 OID 0)
-- Dependencies: 285
-- Name: impot_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('impot_id_seq', 1, false);


--
-- TOC entry 5066 (class 0 OID 1516451)
-- Dependencies: 286
-- Data for Name: impot_minimum; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY impot_minimum (id_impotminimum, type, valeur, annee, datemaj) FROM stdin;
\.


--
-- TOC entry 5273 (class 0 OID 0)
-- Dependencies: 287
-- Name: impot_minimum_id_impotminimum_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('impot_minimum_id_impotminimum_seq', 1, false);


--
-- TOC entry 5068 (class 0 OID 1516459)
-- Dependencies: 288
-- Data for Name: impot_parcelle; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY impot_parcelle (id, hetratany, annee, idparcelle, montant_paye, datemaj) FROM stdin;
\.


--
-- TOC entry 5274 (class 0 OID 0)
-- Dependencies: 289
-- Name: impot_parcelle_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('impot_parcelle_id_seq', 1, false);


--
-- TOC entry 5070 (class 0 OID 1516464)
-- Dependencies: 290
-- Data for Name: impotparcelle; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY impotparcelle (idparcelle, idimpot, etatpaiement, montantpayee, datemaj) FROM stdin;
\.


--
-- TOC entry 5071 (class 0 OID 1516467)
-- Dependencies: 291
-- Data for Name: journal; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY journal (id, idutilisateur, idobjetcible, typeobjectcible, description, dateaction, heureaction, datemaj) FROM stdin;
525	1	1	Certificat	Création de certificat foncier	2024-03-11	11:22:04.31	2024-11-14 14:30:40.86
526	1	1	Certificat	Impression de certificat foncier	2024-03-11	11:23:46.268	2024-11-14 14:30:40.86
527	1	2	Certificat	Création de certificat foncier	2024-03-11	13:41:52.576	2024-11-14 14:30:40.86
528	1	2	Certificat	Impression de certificat foncier	2024-03-11	13:42:19.107	2024-11-14 14:30:40.86
529	1	1	Certificat	Impression de certificat foncier	2024-03-13	16:17:12.156	2024-11-14 14:30:40.86
530	1	272	Demande	Creation de demande de Certificat	2024-03-13	16:21:32.612	2024-11-14 14:30:40.86
531	1	3	Certificat	Création de certificat foncier	2024-03-13	16:21:56.815	2024-11-14 14:30:40.86
532	1	3	Certificat	Impression de certificat foncier	2024-03-13	16:22:39.135	2024-11-14 14:30:40.86
533	1	273	Demande	Creation de demande de Certificat	2024-03-13	16:24:55.445	2024-11-14 14:30:40.86
534	1	4	Certificat	Création de certificat foncier	2024-03-13	16:26:46.007	2024-11-14 14:30:40.86
535	1	4	Certificat	Impression de certificat foncier	2024-03-13	16:27:28.483	2024-11-14 14:30:40.86
536	1	274	Demande	Creation de demande de Certificat	2024-03-14	08:32:39.148	2024-11-14 14:30:40.86
537	1	5	Certificat	Création de certificat foncier	2024-03-14	08:33:19.857	2024-11-14 14:30:40.86
538	1	275	Demande	Creation de demande de Certificat	2024-03-14	08:34:30.842	2024-11-14 14:30:40.86
539	1	6	Certificat	Création de certificat foncier	2024-03-14	08:34:48.244	2024-11-14 14:30:40.86
540	1	276	Demande	Creation de demande de Certificat	2024-03-14	08:36:50.345	2024-11-14 14:30:40.86
541	1	7	Certificat	Création de certificat foncier	2024-03-14	08:37:03.191	2024-11-14 14:30:40.86
542	1	277	Demande	Creation de demande de Certificat	2024-03-14	08:38:12.488	2024-11-14 14:30:40.86
543	1	8	Certificat	Création de certificat foncier	2024-03-14	08:38:41.644	2024-11-14 14:30:40.86
544	1	278	Demande	Creation de demande de Certificat	2024-03-14	08:39:41.502	2024-11-14 14:30:40.86
545	1	9	Certificat	Création de certificat foncier	2024-03-14	08:40:00.255	2024-11-14 14:30:40.86
546	1	279	Demande	Creation de demande de Certificat	2024-03-14	08:41:50.054	2024-11-14 14:30:40.86
547	1	10	Certificat	Création de certificat foncier	2024-03-14	08:42:04.486	2024-11-14 14:30:40.86
548	1	280	Demande	Creation de demande de Certificat	2024-03-14	08:43:21.002	2024-11-14 14:30:40.86
549	1	11	Certificat	Création de certificat foncier	2024-03-14	08:43:33.643	2024-11-14 14:30:40.86
550	1	1	Certificat	Impression de certificat foncier	2024-03-14	09:19:32.331	2024-11-14 14:30:40.86
551	1	2	Certificat	Impression de certificat foncier	2024-03-14	09:27:55.755	2024-11-14 14:30:40.86
552	1	7	Certificat	Impression de certificat foncier	2024-03-14	09:28:22.819	2024-11-14 14:30:40.86
553	1	10	Certificat	Impression de certificat foncier	2024-03-14	09:28:56.324	2024-11-14 14:30:40.86
554	1	10	Certificat	Impression de certificat foncier	2024-03-14	10:43:21.543	2024-11-14 14:30:40.86
555	14	2	Certificat	Modifiaction des informations d'un certificat foncier	2024-11-13	06:34:14.614	2024-11-14 14:30:40.86
556	14	13	Demande	Edition de la geometrie d'une demande	2024-11-13	06:36:05.527	2024-11-14 14:30:40.86
557	1	281	Demande	Creation de demande de Certificat	2024-11-13	07:01:34.33	2024-11-14 14:30:40.86
558	1	12	Certificat	Création de certificat foncier	2024-11-13	07:02:14.987	2024-11-14 14:30:40.86
559	1	282	Demande	Creation de demande de Certificat	2024-11-13	07:04:56.524	2024-11-14 14:30:40.86
560	1	13	Certificat	Création de certificat foncier	2024-11-13	07:05:24.383	2024-11-14 14:30:40.86
561	1	13	Certificat	Impression de certificat foncier	2024-11-13	07:05:54.035	2024-11-14 14:30:40.86
562	1	1	Certificat	Impression de certificat foncier	2024-11-13	07:06:22.173	2024-11-14 14:30:40.86
\.


--
-- TOC entry 5275 (class 0 OID 0)
-- Dependencies: 292
-- Name: journal_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('journal_id_seq', 562, true);


--
-- TOC entry 5276 (class 0 OID 0)
-- Dependencies: 293
-- Name: limcomm_gid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('limcomm_gid_seq', 1, true);


--
-- TOC entry 5277 (class 0 OID 0)
-- Dependencies: 294
-- Name: limcommanjozorobe_gid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('limcommanjozorobe_gid_seq', 18, true);


--
-- TOC entry 5075 (class 0 OID 1516476)
-- Dependencies: 295
-- Data for Name: limitesparcelle; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY limitesparcelle (idpointscardinaux, idparcelle, description, path_file, datemaj) FROM stdin;
\.


--
-- TOC entry 5076 (class 0 OID 1516490)
-- Dependencies: 296
-- Data for Name: menage; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY menage (id_menage, code_menage, nombre_homme, nombre_femme, nombre_enfant, nombre_homme_actif, nombre_femme_active, possede_terre, acces_ressource, datemaj) FROM stdin;
\.


--
-- TOC entry 5278 (class 0 OID 0)
-- Dependencies: 297
-- Name: menage_id_menage_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('menage_id_menage_seq', 1, false);


--
-- TOC entry 5078 (class 0 OID 1516502)
-- Dependencies: 298
-- Data for Name: migration_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY migration_history (filename, migration_date, datemaj) FROM stdin;
sql/2025-04-08-create_trigger_for_configuration.sql	2025-04-28 13:10:10.625	2025-04-28 13:10:10.625
\.


--
-- TOC entry 5080 (class 0 OID 1516515)
-- Dependencies: 300
-- Data for Name: operationsub; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY operationsub (id, typeacte, idacte, idcf, datedepot, dateinscription, cout, cout2, datemaj) FROM stdin;
\.


--
-- TOC entry 5279 (class 0 OID 0)
-- Dependencies: 299
-- Name: operationsub_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('operationsub_id_seq', 18850, true);


--
-- TOC entry 5081 (class 0 OID 1516519)
-- Dependencies: 301
-- Data for Name: operationsubsequente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY operationsubsequente (idoperationsubsequente, idparcelle, typeoperationsubsequente, datedepotdemande, dateinscriptionregistre, cout1, cout2, datemaj) FROM stdin;
\.


--
-- TOC entry 5280 (class 0 OID 0)
-- Dependencies: 302
-- Name: operationsubsequente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('operationsubsequente_id_seq', 1, false);


--
-- TOC entry 5084 (class 0 OID 1516526)
-- Dependencies: 304
-- Data for Name: oppositions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY oppositions (idopposition, dateopposition, datedemande, typeopposition, description, datereglement, naturereglement, descriptionreglement, iddemande, gid, etatopposition, datemaj) FROM stdin;
\.


--
-- TOC entry 5281 (class 0 OID 0)
-- Dependencies: 303
-- Name: oppositions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('oppositions_id_seq', 1, false);


--
-- TOC entry 5086 (class 0 OID 1516536)
-- Dependencies: 306
-- Data for Name: param_layer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY param_layer (id, label_font, label_size, label_color, stroke_size, stroke_color, layer_index, font_size_map_units, datemaj) FROM stdin;
9	MS Shell Dlg 2	12	#ffff7f	1	#000000	2	f	2024-11-14 14:30:40.86
10	Arial Black	12	#ffffff	2	#55007f	5	f	2024-11-14 14:30:40.86
12	Arial Black	15	#ffffff	1	#55aa00	4	f	2024-11-14 14:30:40.86
7	MS Shell Dlg 2	12	#ff0000	1	#000000	0	t	2024-11-14 14:30:40.86
8	Verdana	8	#ffff7f	1	#000000	1	t	2024-11-14 14:30:40.86
11	Arial Black	14	#aaff7f	1	#55007f	3	f	2024-11-14 14:30:40.86
\.


--
-- TOC entry 5282 (class 0 OID 0)
-- Dependencies: 305
-- Name: param_layer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('param_layer_id_seq', 12, true);


--
-- TOC entry 5087 (class 0 OID 1516546)
-- Dependencies: 307
-- Data for Name: parcelle_d; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY parcelle_d (gid, numero, geom, numdemande, nomdemandeur, surface, titre, partie, parcelle, etat, datecreation, datereconnaissance, cout, region, district, commune, fkt, consistance, feuille, idcertificat, idhameau, idcharge, idhypotheque, idservitude, idcategorie, srisraparcelle, codeparcelle, numcertificat, estfiscalite, idcontribuable, grille, has_data, numerodmdpaps, conversion, etatparcelle_d, id_consistance, idclasse, id_commune, csv_id, anomalie, limitrophe, observation, code_parcelle_en_doublon, editer_en_cf, inventaire, sujet_demande, date_inventaire, user_import_inv, date_import_inv, ref_import, categorie, fi_forfait, datemaj) FROM stdin;
\.


--
-- TOC entry 5283 (class 0 OID 0)
-- Dependencies: 308
-- Name: parcelle_d_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('parcelle_d_id_seq', 157, true);


--
-- TOC entry 5089 (class 0 OID 1516574)
-- Dependencies: 309
-- Data for Name: parcellegrevees; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY parcellegrevees (idparcellegrevees, libelleparcellegrevees, datemaj) FROM stdin;
\.


--
-- TOC entry 5284 (class 0 OID 0)
-- Dependencies: 310
-- Name: parcellegrevees_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('parcellegrevees_id_seq', 1, false);


--
-- TOC entry 5091 (class 0 OID 1516582)
-- Dependencies: 311
-- Data for Name: path_personne; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY path_personne (idpersonne, cin_recto, cin_verso, signature, datemaj) FROM stdin;
\.


--
-- TOC entry 5092 (class 0 OID 1516596)
-- Dependencies: 312
-- Data for Name: personne; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY personne (idpersonne, nompersonne, prenompersonne, sexepersonne, datenaissancepersonne, nevers, lieunaissancepersonne, numcipersonne, datecipersonne, lieucipersonne, numactenaissancepersonne, dateactenaissancepersonne, lieuactenaissancepersonne, adressepersonne, situationmatrimoniale, nompere, nommere, csv_id, rcin_personne, ogr_id, handicap, niveau_education, possede_emploi, migrant, date_arrivee, conjoint, datemaj) FROM stdin;
1	LAURENT		masculin	\N	1968	\N	409011013934	2000-06-30	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
8	TOMBOHASINA		masculin	\N	1971	\N	409301010188	1987-08-28	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
32	VELOMANANA		masculin	\N	1960	\N	409301007179	1980-08-27	PORT BERGE	\N	\N	\N	AMPILIFANDRANO	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
9	MALEMIZARA	 EDMOND	masculin	\N	1970	\N	409031000155	1991-03-01	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
11	ALIMADY		masculin	\N	1965	\N	409301010214	1987-09-25	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
13	NOMENDRAZANA	 ORALY	masculin	\N	1990	\N	409051004932	2011-07-12	PORT BERGE	\N	\N	\N	ANTSIRAKA	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
46	RASOALAHY		masculin	\N	1999	\N	423051017152	2018-01-30	MAMPIKONY	\N	\N	\N	ANTSARONALAHELY	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
19	ERNEST	 JEAN JACQUIC	masculin	1968-11-18	\N	\N	409301010576	1988-07-21	PORT BERGE	\N	\N	\N	ANTSIRAKA	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
15	TOMBOLAZA		masculin	\N	1973	\N	409091001935	1997-10-13	PORT BERGE	\N	\N	\N	TSARASAOTRA	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
14	RABEMANANA		masculin	1968-02-17	\N	\N	409301010118	1987-07-28	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
23	RABE	 PHILLIPE	masculin	1969-03-10	\N	\N	409031000020	1990-08-30	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
24	JOSE	 THOMAS	masculin	\N	1990	\N	409081001221	2012-10-24	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
18	TATANANA		masculin	\N	1940	\N	409301003650	1967-11-08	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
26	RATSARAZANDRY	 FLORIETTE	feminin	\N	1987	\N	409082000197	2006-11-16	AMPARIHY	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
27	MARIAMO		feminin	\N	1973	\N	409032000225	1991-10-28	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
2	TODIRAZANA		masculin	\N	1960	\N	409301011037	1986-10-25	PORT BERGE	\N	\N	\N	TSARASAOTRA	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
29	RAZAFINDRAVOLA	 VICTORINE	feminin	1984-04-13	\N	\N	409082000542	2009-12-28	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
30	RABESOA	 GILBERT	masculin	1991-11-19	\N	\N	409051004907	2011-06-01	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
45	VELOMASY	 FRANCOIS MITERAND	masculin	\N	1992	\N	409011027762	2012-05-03	PORT BERGE	\N	\N	\N	ANTSARONALAHELY	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
33	RAMANANTSOA	 JULES	masculin	1971-02-25	\N	\N	409301000081	1990-10-15	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
37	RANDRIAMAROMANANA	 FLODEMIN	masculin	1983-04-16	\N	\N	409051003584	2007-08-17	PORT BERGE	\N	\N	\N	BESISIKA	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
47	RASOLOFO	 ROLLAND	masculin	\N	1982	\N	409081000766	2010-06-08	AMPARIHY	\N	\N	\N	BEPAPANGO	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
39	RAZAFINDRASOA	 SERAPHINE	feminin	1968-10-07	\N	\N	409032000188	1991-01-03	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
48	SIDIMANANA		masculin	\N	1984	\N	409081000924	2010-06-08	AMPARIHY	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
49	MONY	 ELISTINE	feminin	\N	1982	\N	409082000769	2010-06-08	PORT BERGE	\N	\N	\N	ANTSARONALAHELY	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
53	JEAN	 ORTTANCE	feminin	1971-08-27	\N	\N	409092001058	1997-08-05	PORT BERGE	\N	\N	\N	AMBOMALAZA	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
51	ZARANY		feminin	\N	1985	\N	409082000761	2010-06-08	PORT BERGE	\N	\N	\N	ANTSARONALAHELY	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
4	ZAZETY		feminin	\N	1961	\N	409092001411	1997-10-13	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
57	RABEMANAMPY		masculin	1979-04-22	\N	\N	409091001923	1997-10-13	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
59	RAZISY		masculin	1961-03-17	\N	\N	401991040335	1981-05-16	MAJUNGA	\N	\N	\N	AMBALAVOLA	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
40	ROLLAND		masculin	\N	1995	\N	409081001773	2013-09-03	AMPARIHY	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
31	ZAMANIVARY		masculin	\N	1962	\N	409301008405	1982-08-10	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
3	RAHANTAMALALA	 ARISOA BENEDICTE	feminin	1982-05-31	\N	\N	409092002053	2002-12-17	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
5	RABEMANANJARA		masculin	\N	1967	\N	409301010186	1987-08-29	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
7	RABEMANAHY		masculin	1973-08-24	\N	\N	409051001195	1997-11-25	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
10	RASOAZAFY		feminin	1978-12-02	\N	\N	409092001509	1997-10-13	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
12	RAFAFINDRASANGA	 JEAN FREDERIC	masculin	\N	1977	\N	409011013468	1999-11-02	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
21	MANANJARA	 PASCAL	masculin	\N	1963	\N	409091000307	1992-08-25	PORT BERGE	\N	\N	\N	TSARASAOTRA	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
16	RAZAFIMIANTA	 ANTOINETTE	feminin	1990-06-21	\N	\N	409082001053	2010-11-12	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
20	EDMOND		masculin	1966-03-03	\N	\N	409301010191	1987-08-28	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
22	REGIS	 RABE GASTON	masculin	\N	1973	\N	409091000778	1994-02-24	PORT BERGE	\N	\N	\N	ANTSARONALAHELY	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
25	ZAME	 BERNE	masculin	1966-10-23	\N	\N	409301010196	1987-08-31	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
28	RAVELOMANANA		masculin	1967-04-06	\N	\N	409301010193	1987-08-28	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
36	RANDRIAMAHEFA	 VICTOR	masculin	1973-01-18	\N	\N	409091001404	1997-10-13	PORT BERGE	\N	\N	\N	AMBOANGISOA	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
60	MARIANE		feminin	\N	1968	\N	409032000201	1991-06-21	PORT BERGE	\N	\N	\N	TSARABAJA	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
38	RAZANATSARA	 VICTORINE	feminin	1965-01-25	\N	\N	409012000040	1990-04-05	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
34	LOUIS		masculin	1975-01-11	\N	\N	409011006882	1995-03-05	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
41	RASOAZANDRY	 MARTINE	feminin	1965-08-25	\N	\N	409302010575	1988-07-20	PORT BERGE	\N	\N	\N	ANTSIRAKA	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
42	RATSARAZANDRY	 FLORIANNE	feminin	1987-05-23	\N	\N	409082002706	2017-12-26	AMPARIHY	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
43	RENE		masculin	\N	1968	\N	409301010354	1988-03-21	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
35	RABEFALY	 AIME	masculin	1989-03-19	\N	\N	409051003923	2010-03-04	TSARAHASINA	\N	\N	\N	TSARAHASINA	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
52	LIETTE		feminin	\N	1985	\N	409082001513	2013-03-12	AMPARIHY	\N	\N	\N	ANTSARONALAHELY	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
54	DIRISY	 RAZAFINDRIASA	masculin	\N	1977	\N	409091001867	2010-02-22	PORT BERGE	\N	\N	\N	MAHASALAMA	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
50	MARINAZY		feminin	1975-11-05	\N	\N	409092002169	2003-10-16	PORT BERGE	\N	\N	\N	ANTSARONALAHELY	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
55	BEMILEFA	 MODESTE	masculin	\N	1983	\N	409091002262	2003-10-25	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
56	MARILISY		feminin	\N	1964	\N	409092001441	1997-10-13	PORT BERGE	\N	\N	\N	AMBOANGISOA	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
58	DAMASOA		feminin	1952-02-19	\N	\N	409302006235	1975-04-01	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
6	BERTHINE		feminin	\N	1989	\N	409422004562	1979-07-23	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
61	RANDRIAMALAZA	 EMMANUEL	masculin	\N	1980	\N	409091002645	1999-11-25	AMPARIHY	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
62	RABEMANANA	 JAQUES	masculin	1970-12-17	\N	\N	409031000136	1991-01-18	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
63	KRISY		feminin	1953-05-06	\N	\N	409032001603	1997-11-20	PORT BERGE	\N	\N	\N	MANARIMAIVALOKA	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
44	RASOLO		masculin	1974-12-15	\N	\N	409091000780	1994-02-24	PORT BERGE	\N	\N	\N	ANTSARONALAHELY	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
65	RASOAMALALA	 SOAZETTE	feminin	\N	1999	\N	409082002371	2017-12-20	PORT BERGE	\N	\N	\N	AMPARIHY	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
64	ANGELINE		feminin	\N	1971	\N	409092001900	1997-10-13	PORT BERGE	\N	\N	\N	ANTSARONALAHELY	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
17	RAZAFINDRAFARA	 BLANDINE	feminin	1988-09-12	\N	\N	409012027181	2011-11-02	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
66	ZARIZY		feminin	1975-04-19	\N	\N	409092001943	1997-10-13	PORT BERGE	\N	\N	\N		0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
67	NDRENARIVO	 TOLODRAZANA	masculin	1990-01-15	\N	\N	409011023540	2008-01-16	PORT BERGE	\N	\N	\N	TSARASAOTRA	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
68	JAOHASINA	 CHRYSOSTOME	masculin	1982-05-04	\N	\N	409091002502	2005-04-05	PORT BERGE	\N	\N	\N	AMBODIMANGA II	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
69	NIRILAHY		masculin	1961-04-06	\N	\N	409301007915	1981-02-19	PORT BERGE	\N	\N	\N	ANKORAOVAKA	0	\N	\N	\N	\N	\N	f	\N	t	f	\N	\N	2024-11-14 14:30:40.86
\.


--
-- TOC entry 5285 (class 0 OID 0)
-- Dependencies: 313
-- Name: personne_idpersonne_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('personne_idpersonne_seq', 69, true);


--
-- TOC entry 5094 (class 0 OID 1516608)
-- Dependencies: 314
-- Data for Name: personne_menage; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY personne_menage (idpersonne, id_menage, est_chef, datemaj) FROM stdin;
\.


--
-- TOC entry 5095 (class 0 OID 1516612)
-- Dependencies: 315
-- Data for Name: personnemorale; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY personnemorale (numeroproprietaire, denomination, datecreation, siege, observation, idtype, idpersonnemorale, csv_id, rcin_pm, mandataire, type_declarant, datemaj) FROM stdin;
\.


--
-- TOC entry 5286 (class 0 OID 0)
-- Dependencies: 316
-- Name: personnemorale_idpersonnemorale_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('personnemorale_idpersonnemorale_seq', 16, true);


--
-- TOC entry 5097 (class 0 OID 1516620)
-- Dependencies: 317
-- Data for Name: personnemoraleparcelle; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY personnemoraleparcelle (idparcelle, idpersonnemorale, idpersonne, representant, iddemande, csv_id, datemaj) FROM stdin;
\.


--
-- TOC entry 5098 (class 0 OID 1516623)
-- Dependencies: 318
-- Data for Name: personnemoraleparcelle_d; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY personnemoraleparcelle_d (idpersonne, idparcelle, datemaj) FROM stdin;
\.


--
-- TOC entry 5099 (class 0 OID 1516634)
-- Dependencies: 319
-- Data for Name: pointscardinaux; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY pointscardinaux (idpointscardinaux, "position", fanondroana, datemaj) FROM stdin;
4	Nord	Avaratra	2024-11-14 14:30:40.86
5	Sud	Atsimo	2024-11-14 14:30:40.86
6	Est	Atsinanana	2024-11-14 14:30:40.86
11	Ouest	Andrefana	2024-11-14 14:30:40.86
\.


--
-- TOC entry 5287 (class 0 OID 0)
-- Dependencies: 320
-- Name: pointscardinaux_idpointscardinaux_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('pointscardinaux_idpointscardinaux_seq', 14, true);


--
-- TOC entry 5102 (class 0 OID 1516644)
-- Dependencies: 322
-- Data for Name: projet; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY projet (idprojet, date_lancement, date_premier_import, date_dernier_import, langue, nom, datemaj) FROM stdin;
1	2023-10-09	2023-10-09	2023-10-09	MG	AMPARIHY	2024-11-14 14:30:40.86
\.


--
-- TOC entry 5104 (class 0 OID 1516650)
-- Dependencies: 324
-- Data for Name: projet_commune; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY projet_commune (idprojet_commune, idcommune, idprojet, fond_image, couche_titres, couche_cadastres, couche_limites, datemaj) FROM stdin;
49	1	1	\N	\N	\N	\N	2024-11-14 14:30:40.86
\.


--
-- TOC entry 5288 (class 0 OID 0)
-- Dependencies: 323
-- Name: projet_commune_idprojet_commune_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('projet_commune_idprojet_commune_seq', 49, true);


--
-- TOC entry 5289 (class 0 OID 0)
-- Dependencies: 321
-- Name: projet_idprojet_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('projet_idprojet_seq', 1, true);


--
-- TOC entry 5105 (class 0 OID 1516657)
-- Dependencies: 325
-- Data for Name: projet_plof; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY projet_plof (idprojet, "codeRegion", "codeDistrict", "codeCommune", "Region", "District", "Commune", datemaj) FROM stdin;
\.


--
-- TOC entry 5107 (class 0 OID 1516666)
-- Dependencies: 327
-- Data for Name: projetcouche; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY projetcouche (id, idprojet_commune, libelle, type_couche, fichier, couleur_bg, ordre, label_name, show_label, font, font_size, font_size_map_unit, font_color, show_stroke, stroke_width, stroke_color, remplissage, plofpaps, certifiable, datemaj) FROM stdin;
\.


--
-- TOC entry 5290 (class 0 OID 0)
-- Dependencies: 326
-- Name: projetcouche_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('projetcouche_id_seq', 1, false);


--
-- TOC entry 5108 (class 0 OID 1516685)
-- Dependencies: 328
-- Data for Name: proprietaireparcelle; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY proprietaireparcelle (idpersonne, idparcelle, representant, contribuable, estcoproprietaire, datemaj) FROM stdin;
\.


--
-- TOC entry 5109 (class 0 OID 1516691)
-- Dependencies: 329
-- Data for Name: region; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY region (idregion, coderegion, nomregion, shapelength, shapearea, csv_id, datemaj) FROM stdin;
1	190	SOFIA	\N	\N	\N	2024-11-14 14:30:40.86
\.


--
-- TOC entry 5291 (class 0 OID 0)
-- Dependencies: 330
-- Name: region_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('region_id_seq', 1, true);


--
-- TOC entry 5112 (class 0 OID 1516698)
-- Dependencies: 332
-- Data for Name: rejet; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY rejet (idrejet, typerejet, daterejet, motifrejet, datemaj) FROM stdin;
\.


--
-- TOC entry 5292 (class 0 OID 0)
-- Dependencies: 331
-- Name: rejet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('rejet_id_seq', 1, false);


--
-- TOC entry 5113 (class 0 OID 1516705)
-- Dependencies: 333
-- Data for Name: role_crl; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY role_crl (id_role, libelle_role, datemaj) FROM stdin;
4	Ray aman-dReny 1	2024-11-14 14:30:40.86
5	Ray aman-dReny 2	2024-11-14 14:30:40.86
6	Ray aman-dReny 3	2024-11-14 14:30:40.86
3	Ny Solotenan ny Fokontany	2024-11-14 14:30:40.86
2	Ny Solotenan ny Kaominina	2024-11-14 14:30:40.86
7	Ny Mpiasan ny Birao Ifoton ny Fananan-tany	2024-11-14 14:30:40.86
\.


--
-- TOC entry 5293 (class 0 OID 0)
-- Dependencies: 334
-- Name: role_crl_id_role_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('role_crl_id_role_seq', 1, false);


--
-- TOC entry 5115 (class 0 OID 1516710)
-- Dependencies: 335
-- Data for Name: servitude; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY servitude (numeroservitude, dateinscription, origine, descriptionservitude, datelevee, radie, shape_length, shape_area, idservitude, datemaj) FROM stdin;
\.


--
-- TOC entry 5294 (class 0 OID 0)
-- Dependencies: 336
-- Name: servitude_idservitude_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('servitude_idservitude_seq', 19, true);


--
-- TOC entry 5117 (class 0 OID 1516718)
-- Dependencies: 337
-- Data for Name: servitudebeneficiaire; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY servitudebeneficiaire (idbeneficiaire, idservitude, datemaj) FROM stdin;
\.


--
-- TOC entry 5118 (class 0 OID 1516721)
-- Dependencies: 338
-- Data for Name: servitudeparcelle_d; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY servitudeparcelle_d (idservitude, idparcelle, datemaj) FROM stdin;
\.


--
-- TOC entry 5119 (class 0 OID 1516724)
-- Dependencies: 339
-- Data for Name: servitudeparcellegrevees; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY servitudeparcellegrevees (idparcellegrevees, idservitude, datemaj) FROM stdin;
\.


--
-- TOC entry 5295 (class 0 OID 0)
-- Dependencies: 340
-- Name: servitudeparcellegrevees_idservitude_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('servitudeparcellegrevees_idservitude_seq', 1, false);


--
-- TOC entry 4048 (class 0 OID 1514744)
-- Dependencies: 175
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text, datemaj) FROM stdin;
98751	fiplof	98751	PROJCS["laborde",GEOGCS["GCS_Tananarive_1925",DATUM["D_Tananarive_1925",SPHEROID["International_1924",6378388.0,297.0]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Hotine_Oblique_Mercator_Azimuth_Center"],PARAMETER["False_Easting",400000.0],PARAMETER["False_Northing",800000.0],PARAMETER["Scale_Factor",0.9995],PARAMETER["Azimuth",18.9],PARAMETER["Longitude_Of_Center",46.437229166666],PARAMETER["Latitude_Of_Center",-18.9],UNIT["Meter",1.0]]	+proj=omerc +lat_0=-18.9 +lonc=44.10000000000001 +alpha=18.9 +k=0.9995000000000001 +x_0=400000 +y_0=800000 +gamma=18.9 +ellps=intl +towgs84=-189,-242,-91,0,0,0,0 +pm=paris +units=m +no_defs 	2024-11-14 14:30:40.86
\.


--
-- TOC entry 5121 (class 0 OID 1516729)
-- Dependencies: 341
-- Data for Name: terain_status_specifique; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY terain_status_specifique (gid, fn_fg, demandeur, sur_plan, obs, geom, datemaj) FROM stdin;
\.


--
-- TOC entry 5296 (class 0 OID 0)
-- Dependencies: 342
-- Name: terain_status_specifique_gid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('terain_status_specifique_gid_seq', 1, false);


--
-- TOC entry 5123 (class 0 OID 1516737)
-- Dependencies: 343
-- Data for Name: titre; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY titre (gid, titres, propriete, sur_plan, titre_r, parcelle, partie, feuille, geom, datemaj) FROM stdin;
192	A	A	1	A	A	\N	A	0103000020067400000100000005000000BC9C107D160EF2406CB0DEC8CD79204188633DD7DF75F440537A2509693F204178C7D6355D37F3409A8AD0BA49122041AC68EEF1EAA3F140AD25AD1A7C2F2041BC9C107D160EF2406CB0DEC8CD792041	2024-11-14 14:30:40.86
193	\N	\N	\N	TN32189H	\N	\N	\N	01030000200674000001000000140000002E5DC4022E721E41B84999F66323294118D85E715A721E4174D5C94838232941E0740B09AE721E416016EC9E1F2329413EAD913B1B731E41D239FAF85623294160EEA6D18B731E411C570C0443232941846A499A2C741E4124F9E12214232941FE50B4E757741E4194F99E18FB2229419EDF861565741E413A1F11B5F7222941923B446996741E41F2042CCFA5222941745A87E491741E41804AA958902229419207AD4978741E415694B2F66F222941320D81A858741E41D2BE49F852222941C6B3D2D48E731E41A8F480157E222941341F797FB7731E414CAC58A19822294154D37D876F721E4110386A59DD222941D886BEB35C721E4116428E8DF02229416685CD5CA2721E41A6091353142329414EC920C54E721E412E706E1535232941221164711D721E4190C5E59E5C2329412E5DC4022E721E41B84999F663232941	2024-12-09 15:06:39.58
194	\N	\N	\N	TN32081H	\N	\N	\N	010300002006740000010000000600000002E5DBC0CA571E41D0AD83DA552129419A72D50047581E41F6FD092C37212941408D3C5D32581E41E0B94F7C1F2129410A288BD203581E41842849D02B2129413A3DC4D9B0571E419AE94BA14121294102E5DBC0CA571E41D0AD83DA55212941	2024-12-09 15:07:47.898
195	\N	\N	\N	TN1413H	5	\N	\N	010300002006740000010000007A000000E0EDF7DE623E1E41285B56FF161E2941D28E70BD833D1E418C2114569E1B294152AA119B633E1E41506F3D8E521B294122AF60B8353E1E41F88B302F311B2941729C9B9D0A3E1E410ED579FE031B294118A6132BD73D1E41A2005156C31A294126014F10AC3D1E419E176AA4791A29412CD8187E6D3D1E4184CE94670A1A29411A405463423D1E41823DC73BBD1929410696EC872D3D1E4142025076AA192941002783E9F53C1E4178EA5E2862192941187F6DEED53C1E41CE98A0E6121929415C912CC0983C1E41CC359B60CD182941C8B2EC915B3C1E41DEBB95A24118294196C5D4D3183C1E41D8446A37DE172941402B08E0113C1E411AE5C2F0AE172941E20C1892C93B1E41329E34307C17294164E197A9983B1E41120BA81043172941FA5E98A9983B1E4106A9DC99221729418A07C73E953B1E41721AC977F4162941347351FE8A3B1E41E8A32B96D0162941F4A5A7915E3B1E4104E9AEBEA0162941F851AE28843B1E4190DEFD5D91162941E22472ABC13B1E41B2CE592BCD162941809BD36CE03B1E4128A1B5F808172941CABDA4D7E33B1E41DE5811C644172941DA639058F83B1E419CE380126C17294138630C30283C1E41728387A991172941CE5AE431513C1E41F811BCD5B317294194EC2BDD5E3C1E41BA952B22DB17294106003174843C1E4184CBE9B0351829412C157EB6B73C1E416E2D1E809A182941C489B779FF3C1E414A8945C4F61829415AD15A4F063D1E41E62FFDBB2B19294148A78E7B283D1E4168C20353511929419C2C9AA9733D1E41A61CC2E1AB192941F44F8BC1AD3D1E414C8A5F66121A29417AA71A18C93D1E41EC68F653531A2941E4C2C384F53D1E414AAF864DB11A29410E715972363E1E41DCC6C110F91A2941164E0976883E1E41BAF36589421B29417ECF652C8C3F1E41C8CD6DDAE21A2941AEABF2A5D7401E4106216D953A1D29416089F98282411E41701BE432021D29410CB3F9C807421E41702575E6DA1C29414454DFF87B421E4152625BD0C91C2941F8A74EE8E5421E4112B920B0C41C29417EB4E5D526431E41E2BE9DE4B11C2941D89D273094431E41D2ACC5E2881C294196BCB1350F441E418C9D1B765C1C29419253ABE46E441E410C9DB9B43D1C2941560D0755ED441E4188E808542E1C29415EA562C56B451E41164E657E271C2941EA27768ADC451E41CC9686881B1C2941CEC7B7E449461E4146BD3152051C2941E8DE7C6787461E41A6B07366ED1B2941BC9166D0AB421E4192388570061A29410EB57FD061461E41204BC44A86192941D470876787461E41626D41DC30192941D436EA28A6461E419A38B18515192941A4E24CEAC4461E416618C50401192941E48B8116E7461E41BA05ABEEEF182941DA2CCAC1F4461E4122B6482DD1182941E4A126ECED461E410E43AB4BAD182941AE3F8316E7461E413AB197297F182941043035D4B3461E417613FA475B182941784BFB106C461E415A0FCC0F1C18294146B90F9057461E41767521A3EF1729413C88FC106C461E41DC171B0CCA172941C62E45BC79461E41EEC24F95A917294156B6F028A6461E419C2450F266172941FE0054EAC4461E4186888B6F29172941E6676869B0461E41CEF349B8FE162941F601916787461E4182F30EF5B61629417663CDE449461E4168DA6A7C6D162941806E9AB827461E41709871CD0D16294148EDE26335461E41BE621C97F7152941F67559A43F461E41441A8C40DC15294154C26D232B461E41DE99EE5EB81529411C517C0BF1451E41906A3D5B66152941249D3460E3451E414200DB99471529414A233BF708461E41E614A07942152941ACD212F931461E4198DC57717715294190B4A7E672461E416E934A2CF415294114F5E8FA5A461E41A6D9ACED12162941EA91E8FA5A461E41D626D48E2C1629412EB5D91295461E417094711393162941AC6B55EAC4461E412A6DFB75CB162941AC1A2DECED461E41DC34B36D00172941F09C4602FF461E4132D0C68F2E172941D8886D00D6461E41461F36DC5517294108CD6569B0461E41C8FCB84AAB17294182395ED28A461E41C6BBC578F6172941DEEBA57D98461E41E625283A15182941EEFACBC1F4461E414E4D919259182941F4A1FFED16471E41D003771F8B182941A2DCA2C31D471E418AB40082C31829417ADAFDED16471E418867C50401192941464F9B2CF8461E410A6EA4FA0C19294106F95F69B0461E41BA8A6F712D192941283917BEA2461E410EF4DEBD541929417E69CE1295461E41E66720757F192941062AEE63EB491E41D2517965101929411820E19E554B1E4152D6FC5F701A2941C2628851074C1E417CB91D532C1B2941705547C9294D1E4190A1EA83C71A294160C45E02904C1E41F682393AF01929415EB37DD21B4C1E4150B5B6E2D21829419C3B3C78AE4B1E41A86F95D8DE1829413AFDE21B2E491E411298B73E1616294100F2F13116481E41F884F591EE142941F2EA8867D1421E41028FA5B2CD122941A865641EEB381E4152B01A5AE41629414A77388000391E4156655D98C5192941C676DF83F3391E410C87FDF1A51C2941AC8F57B6DC3A1E41B46D6550921F29418E97A63E953B1E417875DCED591F2941B0B9AD61C53C1E41A0654069F31E29411C1917BA093D1E411E363AD2CD1E2941BEBF732A883D1E41D0C7C4EE801E29414E4FFE2F033E1E4110612176371E2941E0EDF7DE623E1E41285B56FF161E2941	2024-12-09 15:07:47.898
196	\N	\N	\N	TN1413H	1	\N	\N	01030000200674000001000000290000007A28EEFF003C1E418480F131591F2941F40A6D8B153B1E4194000A54A41F29417AAE26072C3A1E41B05EE6ACE91F2941B8F6C58A27391E41ACDE19D418202941C606B73B70381E4150CD7C703C2029415C8181A62E381E41686FBB723B202941D064C73645371E41F44D629B4F20294132190950D5361E41C67E62105D20294110BCF3C9AC361E41FE0237B166202941B2A32A6322371E41E8BC76369020294150B5949285371E411A0FCA0CCA20294114A41466AA371E4154712408F4202941A82A30A35C381E4146574CCC292129411A2F0CDCA0381E41CCFCD74C5721294104D1CF772B3C1E41BE82CF5CDD21294180D4221B7B3D1E41E88DFA79B32229415677BC308C401E41DA61E69395222941A05665FCC0401E4180F369FA2E22294108C81DACB1401E41E20FD9A2E6212941489BD93DA8401E4170E19D7663212941D876A623C9401E414EE055DB222129416E1EE53478401E41B87DDAB4EF202941BCABF4B10C401E41D468022CB71F29418ADDBB8831401E41E6251C73431F2941C883CB45C8401E412E6D8BD5971E2941C6A5D57E39401E41621692FEAC1E29414CBD406A07401E41D87EA79B801E29415E86571B9A401E41E6BE69BA481E2941D4D215020A411E41C48D69453B1E294122386D7BE7401E41CE5B6FA9C31D294104F22C7460401E4176553D92C41D2941949904E371401E4154BB5F36981D29411A545C1F34401E416E47AC55AF1D2941CC485A21E13F1E41EE3F313CCC1D29419A98A3B37E3F1E419E81D105EC1D2941A6FF902CE83E1E41B4CDF865161E2941AABCE0A86C3E1E4152576AF63B1E29414EB20B8E003E1E4198C227096F1E29418AFD03249C3D1E41BEAD328BB11E2941B4351A56F03C1E411AE1A898FF1E29417A28EEFF003C1E418480F131591F2941	2024-12-09 15:07:47.912
197	\N	\N	\N	TN5216H	5	\N	\N	0103000020067400000100000022000000F07D48FC6C441E413844BAE7E3212941009EB67FB0441E41C2B04A1EDE212941B81105B9E0441E4118975AC3E7212941745D012D5C451E41A4D49A7AEF21294168A76D6ADD451E417867E395EC2129411CBF3AEF3B461E419C73DB31F7212941805E27BEAD461E41E0BD6304FC212941260A76F7DD461E41B60FDC31F7212941AC96D5F8F8461E41FECE0403E12129419C11D6F8F8461E41DCBB1D2FC12129412E2217D3E1461E414667A624A721294136D6279BCC461E419E7D365BA1212941C80D8B058B461E4180C4A88D4A21294146A7246EAC461E41FA6517A5172129411E594F5C4D451E41BA0647DAF6202941DA0CAE8049451E41364B2C6854212941CE6963F67E441E410485CA2077212941F811B947B8431E41D08B09D87E2129410CC1FA4482431E415491C92077212941F6C963E515421E417E4D394984212941D83C2DC2F0411E416C9C44FF80222941884FAACFCE431E416051CC1E9C2229417C8E08AE08441E41B06454F1A02229412802377A44441E41E8FB8C679422294182BFE6FA51441E41424965B98B222941722D471F4E441E41B6E37581762229415CEC666961441E410E8D6E4062222941682F676961441E410C0E1FE450222941DEECB7E853441E415AAD5FBE39222941AE8C387A44441E4182F47F2B2E222941F22EC9B03E441E4172D4804E0F222941EABCB90B35441E41D45349FBFC21294124D559E738441E41CEBB997AEF212941F07D48FC6C441E413844BAE7E3212941	2024-12-09 15:07:47.915
198	\N	\N	\N	TN1413H	2	\N	\N	010300002006740000010000002E00000034CA63E515421E418C4D3949842129412AC1FA4482431E417C91C920772129412E12B947B8431E41E88B09D87E212941EC6963F67E441E412C85CA2077212941000DAE8049451E41364B2C6854212941F8584F5C4D451E41AA0647DAF620294104B74FAE60451E41F85244A8F820294180A7246EAC461E41166617A517212941047104E3AE461E41F6EEC3C7132129419CCFC39A4A471E41123A4FCF1E20294168019E382E481E4190A791CCE81F294134BF5D3B64481E41B66104FF911F2941BC89AD9775481E41F401E5B47E1F29419C2CF2943F481E4190B7B233B31E2941ACA0756CF2471E4184C17C26631E294144A398D9E6471E41CCDEC1AFB11D29412C74F593C3461E41BA26D14E911C2941C88F62AE63471E41A8252D9B1C1C2941FEA4AE7EF0471E4160034E08111C29414A8542416F471E414EC00D51091C2941C6AE4713B6461E417AA1A4C8171C294186D6EB9D1F461E41DAA43B40261C2941D01094D7EE441E41B04931B94F1C2941BC09D83D5C441E41A82C5003631C29416C387A8203441E413615C70D7D1C2941BC433D5780431E41241ACD2BB01C29417A28BF2E33431E41BE238C51C71C294158DDE104CB421E4170217B89DC1C2941F0D9244857421E4112F7099DF51C29415E75088AC8411E41A463904C191D29415C079B2966411E41A874AF962C1D2941666E8DEDFF401E41A2FA0534521D2941CEE51E6ABC401E41FCC4D4FE721D29411444BD22DF401E4162B2CB779C1D2941546D9A4C47411E41247404EE8F1D2941509848AA73411E4166958B9DB31D29418CEE333323421E4130165DAE961D2941344E10806C421E41127AB205FA1D2941AC4883F8D7411E4108560FC1521E2941B8AC80617B411E4104C9E4D2B11F2941E84B1224FA401E41002D189A3F2029418C9515EA6F411E414811658DD12029410C1F4E709B411E41FEAE7C08F2202941BCE33303D5411E41C428658336212941B0253670FE411E410C6940E96721294134CA63E515421E418C4D394984212941	2024-12-09 15:07:47.915
199	\N	\N	\N	TN1413H	3	\N	\N	010300002006740000010000001100000082CE964D014E1E4118137EF6B11A294158E809A38B4D1E4194036D2EC71A2941B69AECC11B4D1E41AA86DBD4EB1A29417C529FCEAD4C1E41942FC2A80B1B2941D04FA25A324C1E414892E833331B294124348456E14B1E41865EE710521B2941C624A5E6B64B1E41B4A5065B651B2941CC7056D0674B1E41206A8CE7A71B29411A14173C414B1E41745873BBC71B2941564798F0124B1E41C2E38260D11B2941348A3B589B4A1E41C0041AD8DF1B2941D8F1AD8A444A1E416277598FE71B29411EA4FBC3744A1E41E6E8875B231C2941984AEFAAEF491E4108FD1ED3311C2941187F847A3E4D1E4122FA0D7FC21C294118E33A1FA94E1E41AA2311C5841C294182CE964D014E1E4118137EF6B11A2941	2024-12-09 15:07:47.915
200	\N	\N	\N	TN5216H	8	\N	\N	01030000200674000001000000040000008CB5D49B654E1E418405C0F37B1A2941F68D4CDA62501E410EC1A62FC3182941C82338EE1A4F1E413278E1313B1829418CB5D49B654E1E418405C0F37B1A2941	2024-12-09 15:07:47.915
201	\N	\N	\N	TN1413H	4	\N	\N	01030000200674000001000000050000003A301A2BB43E1E4120C4B0A90A1D29413CF03A90693F1E41DCF3D503D91D2941A03230176E401E41948B6A5C811D294158CCA94D8F3F1E41645278A9E01C29413A301A2BB43E1E4120C4B0A90A1D2941	2024-12-09 15:07:47.915
202	\N	\N	\N	TN5216H	2	\N	\N	010300002006740000010000001D0000005A96F942C42F1E41C691BF7A5C232941107A20EC18311E41B8FC217F482329415EB608B17F311E41C6F4B5A831232941164F2301DA341E41E0E65E18DB2129418C5C96630D351E413CD8A11716222941EECAF916C4351E419C47A155112229418628F49DE1341E414A1D08F953212941BCA8E8726E351E41E67FDBB0A8202941B4ECAA7B46351E415459DBB0A82029413C3FC53AE9341E4114DD79ACBC2029410C47DFF98B341E4144651DB0E3202941261C32A843341E41BCE625FE04212941AE2FC0C919341E41F6AB945825212941DEA04B67E6331E41B40F6C434E212941AC29990D8B331E41F282799982212941442244720D331E410E94852DB221294190D1820079321E41DCE62831D92129418254CE2214321E416463C72CED212941B8E3FC0103321E4114FB2FBDF5212941F2F325D9DE311E4144946DB41D222941748FEF6DD3311E41B6983D132A2229416A4471FB79311E4120FA75023F222941CAB7B71502311E41BEF1E1D855222941F88043B3CE301E4154EA4CED6722294150BAF5A36D301E418041C495A9222941A81474AD0A301E4160CC71A9F62229411248CEE7DE2F1E4136C5166F22232941B44030AECF2F1E41F86284073E2329415A96F942C42F1E41C691BF7A5C232941	2024-12-09 15:07:47.93
203	\N	\N	\N	TN5216H	1	\N	\N	0103000020067400000100000015000000D4054DF17B2F1E417A578AD1552329413682004BD72F1E41CC7BD1EBDD222941D8E612E719301E410E63F6BAA6222941C09260F67A301E41B200B4BB6B22294196F1A8FDC8301E41409076C4432229415C05390C65311E414CD2A09B1F222941ACB3AFF2A1311E410A700362102229416ACEE8E1B6311E418E8BC9B0F62129412232EEE9C9311E41CA7E29F3DD2129416294295DE8311E4144408D7BD3212941262279F052321E41DA56BC5AC221294122E66339C3321E414AA41C9DA9212941140AAC4011331E4174D07CDF902129415082C0605D331E416047A93A76212941BCCC6DB2A5331E419E1D385C4C212941E477200C01341E4138C1C0B30A21294126246E1B62341E41C05E7EB4CF2029414A7A685410321E416C7CDF67862129417CDF955973301E41B4A4D2955B21294140C457F98E2F1E414EF0BF24DA212941D4054DF17B2F1E417A578AD155232941	2024-12-09 15:07:47.932
204	\N	\N	\N	TN5276H	4	\N	\N	010300002006740000010000003000000080D4221B7B3D1E41E88DFA79B32229411CBC8193673E1E41DE71708949232941AC1382AEC23B1E4108E6F14617242941F446308AEB3A1E41BE1937019D232941181D67B5D03A1E41BA733F3B022429410C3F399DFC3A1E411ED16B6D0E242941D859A727373B1E4142424B41F7232941A4034CDD563B1E41405A759A572429414A42DE521C3B1E415821759A57242941162AE8652D3B1E41303B95D38A2429418C5F0207413C1E41408D488283242941843183D1D53C1E412063D82BB9242941DCF1E62EC73C1E419C9B67D5EE242941BCEC256AC73E1E415C08B54D4A2529415C8DA54E943F1E417429CB736C252941E448F2B9D33F1E410CAAED854B25294110C9C4A1FF3F1E415EA1C1533F2529418CE26A571F401E41AA5EF98B402529415058D8E159401E415682730F5425294148EFD6FB91401E41BC3D952E4F252941E29F5B92B6401E41AA477F154925294188F10148D6401E41BA941BAB3B252941E01B228109411E41046F962133252941D2494EB315411E417C19CE5934252941D4B5DD5C4B411E41E85711982A252941D29C6B20B9411E41A409C44623252941D0695F27E0411E41B46C33B72525294106BFC29E09421E41DEE628A41425294146845E4118421E4170CC3FB0FE2429411EECCDB11A421E41D63A4BB6F3242941600505F737421E41D0E6AF13E52429419AE8B5BF68421E4152FC99FADE24294128025C7588421E4156B9D132E02429410CA9166B02431E4108DEFF4AB42429411C7197A06D421E417219898614242941D4CEA39946421E412E22251C0724294194DFFDE326421E417ED0F8E9FA2329419E17BD8BF8411E41B49AD8B0C723294134CA30C88A411E4186FA3EE76423294140C6E45C4B411E41E84CA344562329411E9212751F411E41546A55F34E232941D87EDC15CA401E41EA075F137C232941183F955CE23F1E41202E11B558232941D8E4692AD63F1E41249E129B202329414424260618401E4152D4F261ED222941B4170E1466401E4136D3B016DB2229415677BC308C401E41DA61E6939522294180D4221B7B3D1E41E88DFA79B3222941	2024-12-09 15:07:47.932
244	\N	\N	\N	TN7550H	2	2	\N	01030000200674000001000000090000007077E35A488D1E418EA535FD4F2429410A1C9BA5E38D1E4164990B883624294194D094A9618E1E4102E6906424242941EC258163598E1E41941E6C40FD23294196AEBA78188E1E415ABA496F07242941507B74E0D98D1E41BA0CE6401124294114CB725A3A8D1E41B8D3F82A3724294168E640E4228D1E413CCB7ABE3C2429417077E35A488D1E418EA535FD4F242941	2024-12-09 15:07:48.035
205	\N	\N	\N	TN5216H	6	\N	\N	0103000020067400000100000023000000A4CE964D014E1E4112137EF6B11A2941EEE23A1FA94E1E41B62311C5841C2941667F847A3E4D1E4126FA0D7FC21C2941784AEFAAEF491E4124FD1ED3311C2941C684CDDFB1491E41B2A3EAAE311C294184BA87B56A491E419AE6DE4E6D1C29412CF29A187A491E4116006373191D294110EA5090A0491E41DE50E8F43E1D29410E5EF80363491E416E6C118C941D29413E4FF45FC3481E41AC6C34F3071E2941E2810FC504491E41127642F76B1E2941D079DC43DA491E417CC7D27BDC1E2941608EA062EB4A1E4110A510D2A11E2941562194A5AD4B1E411604C147961E2941A488B10AEF4B1E4156D27F1E681E29415EE838A58A4D1E4120026FBC711E2941ECD53EEDC94E1E4168DF46251C1E2941DC109678EE4E1E411442C52F391D2941CA7F312F734F1E413490384F681D29414840503854501E41DE50E3947A1D294176F3CBC551531E419AD9628D8C1D2941CE7CBE6A5C531E41EC407C65581D2941985032A653531E41B885F022EF1C294148624764AA521E4192293864A21B2941A8479D4C48521E41B8CF7DEB621B294138FE9CA8A8511E4196567E48DC1A294106A9EF32B4511E41AA9BD55F431A2941CEBD481C6B511E41F4E39336151A2941D421B066FF501E41E44D6B710F1A2941A06C4678CB501E41BC499336151A2941FCF8935E37501E41601521E9351A2941FA82BDDD2F4F1E41309E1489711A294136239D77D54E1E4172BAF8F57F1A2941C2B87C117B4E1E414AED7045911A2941A4CE964D014E1E4112137EF6B11A2941	2024-12-09 15:07:47.932
206	\N	\N	\N	TN5216H	7	\N	\N	0103000020067400000100000017000000E80591F5AB541E414C50EFB3851C2941A616927F12551E41F08ECFAA871C2941EE44255B11551E4130C69F97691C2941F6FF01A52B551E41F80828DD351C29413E86F3953B551E41AAF3BC1CFF1B2941CE38819E2B551E41AE383B79DA1B29415CAF30DB11551E41B2DAE486AA1B2941DC6E3143EB541E416C8F711C5C1B29411C724622E4541E410C9039B23E1B2941244A1328EA541E4158EB8C31061B29412EC6E444E0541E410C7F0381D61A294170120E50D2541E410ED3B81AC31A29414046A257A8541E414EFB9B2A751A29415C65875063541E41600056D0061A294114232B7152541E41AC8E2980C8192941545ABD7295531E41A4183E88BD19294170F151A905541E41040B71DAE11A294146F4AF71D8531E4104F25BA4941B294194745E0236541E4110D32EE4C01B29417C3E49D59B541E41E680BC0EF21B29412A263F9BB0541E41AE4A365D201C2941B6D32EF9AD541E41D016E3322A1C2941E80591F5AB541E414C50EFB3851C2941	2024-12-09 15:07:47.944
207	\N	\N	\N	TN493H	3	\N	\N	0103000020067400000100000012000000806B77CB0D5A1E4148D7FD82C71C29414805D6B449581E41106CC4B7E21B29418470A7853A551E41E4AA3F25C11B294146087E1458551E4118026EA32D1C2941C084537260551E41421D57CE891C2941CC6EA9FA2A551E41AE49C556881C294170F80B4B2E551E41D4724461AB1C2941BCFC57D303551E412AE6C7059D1D2941C0A7BDE21A551E41FEA5D5F6BA1D294142FC892F3B551E414E2457D0D21D2941469DB59E75551E41545AD54CE21D294180C13D53CC551E411C3EB6F8EF1D2941C4096DC41D561E41C80CBB46F71D29418C2857D396561E41068AC72D021E2941C88773C409571E413A4D3AD3C51D2941BE8566B1F8571E413CA01464641D2941BEF4BD1191591E410C75A07F051D2941806B77CB0D5A1E4148D7FD82C71C2941	2024-12-09 15:07:47.951
208	\N	\N	\N	TN493H	4	\N	\N	010300002006740000010000000A0000007A0C4168AE5B1E41DCA853FC92182941CEF3CE7FE95A1E41920FF493841829413E42777AA85A1E4186545A8B99182941B68659B72D5A1E415A90A05EAF182941FAFD039A2C591E413E4A2DBCDD182941260AC95F09581E412EAEFE5DF518294148C4DAAD34581E41340D1C6A53192941E83721BEEB571E4190F32AB05E19294158FD871036581E415621C89CD01929417A0C4168AE5B1E41DCA853FC92182941	2024-12-09 15:07:47.951
209	\N	\N	\N	TN493H	5	\N	\N	010300002006740000010000000F0000008244D2D4AA5A1E414A5F3D9491182941709E3AEF66591E41E4D727B8B91729416A9462DA1F591E4198FA9BB1CC172941E48F01E6A4581E41383C9344E2172941FCF4BEE128581E417450717EA817294186CE25C3C4561E41C6299E9DBD182941B465674317571E416CB4973BE91829417AE0ABD45C571E4170D95E62F9182941B437E18F00581E41D038E89EED182941B4936E6A27581E41F05B751BEB1829410072731B93581E41407D46D5E218294144F7A96409591E411AE4762FD8182941404816D932591E4174811376D118294102307D7B285A1E41624EF36CA71829418244D2D4AA5A1E414A5F3D9491182941	2024-12-09 15:07:47.951
210	\N	\N	\N	TN493H	6	\N	\N	0103000020067400000100000010000000AEE9E16315581E4164AB740995172941C0A9B986B2581E41E82C5E438817294138EBF18F24591E41BC6105668E17294100E4273E96581E41A690665127172941B4A74F2D89581E4178B1E6F32C1729417C888D4739581E41666FABD301172941C6943C8901581E41767446BE171729414403F70294571E410A577591E01629418E3B946C40571E41601B35CB121729410AF7EBA2E3561E4184897629E51629415A14C18839561E41383B78832B17294104BF3B2784561E41F8530FB451172941BA4A74C026571E4186C9F2EB87172941E2AA31B58B571E4126E9C21713182941AC6E05DC12581E41E8569B99A9172941AEE9E16315581E4164AB740995172941	2024-12-09 15:07:47.96
211	\N	\N	\N	TN493H	8	\N	\N	0103000020067400000100000005000000587C4C8288561E4106301F5EAF16294110D49878D0561E4146880E98DE16294118BCD21C20571E4172942F51BC162941684943DED5561E416E77CDFC90162941587C4C8288561E4106301F5EAF162941	2024-12-09 15:07:47.96
212	\N	\N	\N	TN5276H	3	\N	\N	010300002006740000010000000C000000F446308AEB3A1E41BE1937019D23294190FF21F26D391E41DA2C5878B722294110E81F2A243C1E4178E05548DC212941DE2E0CDCA0381E41BEFCD74C572129419448122765381E4148682DE465212941A0FB517F93381E4184311F12E121294110DEBC09CE381E41621E04549F2229410C79DE0E91381E4176008704FC22294130AD153A76381E41C4F436DA48232941C85EC31CDF381E41E2E6552DB423294180113808D3391E4146A5DD9C84232941F446308AEB3A1E41BE1937019D232941	2024-12-09 15:07:47.96
213	\N	\N	\N	TN4778H	16	\N	\N	01030000200674000001000000060000009C88F11DC9681E411E2E723A271129414422AABCF9681E41D2B44EE121112941A8C3070C12691E419CA0F0F5C6102941729F42FCF0681E4170183D3BC6102941A0F04541C4681E4162D63ED7081129419C88F11DC9681E411E2E723A27112941	2024-12-09 15:07:47.96
214	\N	\N	\N	TN4778H	15	\N	\N	0103000020067400000100000005000000E40C1296B8681E4146FE0CC459102941D86B24E8BE681E41265E96957A102941EE5C1332FB681E417E1121648110294114B1D015FF681E4184560F0F61102941E40C1296B8681E4146FE0CC459102941	2024-12-09 15:07:47.96
215	\N	\N	\N	TN6128H	2	2	\N	010300002006740000010000000C00000046E49CC2FD691E4140934F5DCD0E294176B859781F6A1E41F8ABCD340F0E29416422DFF7AF691E41A6E809CF010E29410CF2F15787691E41B85293C8FE0D29412086CA2509691E41B89DB22CE90D294188F4761EB0681E41C411F5B5C20D2941CE17DD3956681E4120D6BD77940D29410E8BC03130681E41027E5F043D0E29413648B39FEC681E414AC0FECFE00E29412084EEC464691E41E0279279C90E29414AACB511BC691E418E02C924D50E294146E49CC2FD691E4140934F5DCD0E2941	2024-12-09 15:07:47.96
216	\N	\N	\N	TN4778H	14	\N	\N	010300002006740000010000000B000000D417DD3956681E412CD6BD77940D29416CF4761EB0681E41C411F5B5C20D29412E86CA2509691E41CC9DB22CE90D294168F2F15787691E410A5393C8FE0D2941D422DFF7AF691E4194E809CF010E29416CA4294CAD691E419294D067FC0D2941EC8E0FD182691E415EDBA99AA20D2941AAF1AEC23A691E41D0A136D72C0D2941180C564A25681E41B84430BA470D294160EDD7AA63681E41D6DE308C930D2941D417DD3956681E412CD6BD77940D2941	2024-12-09 15:07:47.96
217	\N	\N	\N	TN6128H	3	2	\N	0103000020067400000100000013000000E28949EF8B621E41C0537CBBF00C29412672D0DF81621E413A71357FFA0C294144AE552E7A621E414CF12D26050D29413825D5C57A621E41685768230D0D29410408CF0E83621E4136435A42210D29412ECD464D8E621E41B2530A0B380D294120E2AD37B1621E41B454B6BE540D2941500B894BE5621E415ECBE7C0690D2941549BDAFB26631E41D6D11650820D29419229374959631E41FE1F8F8E8D0D2941AE7C8B6C97631E4102CB0A11940D294146916822C9631E419048C8E9970D2941C0E04ED3ED631E413E4A0A40950D2941BED4B41B13641E41B6FE8EBD8E0D29414C23365511641E41AAE411998A0D294112A3C740FA631E413ED0CE9A330D2941286AD16AEE631E411274D3A9D10C2941C032278274631E413C7B206EBE0C2941E28949EF8B621E41C0537CBBF00C2941	2024-12-09 15:07:47.96
218	\N	\N	\N	TN6128H	1	2	\N	010300002006740000010000001B000000E2E1557E2D631E41C45F0FF78C0D2941B0CEC0212D631E41AAEFE4A28C0D2941E296B79F44621E41243544E5F60D294192783A627C621E41A4067A22240E29415CD234D1F0631E41FEFFBA2B430E29416633CA2885641E41A0A198A8EE0E2941AA7FAD0524651E41BCCAC9C69C0F29417EC78FE2C2651E412811213A8E10294148735E5208661E415826594FB8102941C459D9B44C661E41F24262AFAB10294178B2523F94661E419EAB346673102941285564558F651E416CE2D56D120F2941AECC43D5C1651E4172FC5B7A530E29419AD9D4A7E6651E41126210CD450E2941AC1D35EDD7651E417AB281D21D0E2941549728DDEA651E41087B4FD9EB0D2941B86FEC1A4E651E412627BF72C50D2941D47BE48186641E4148682A46680D2941E247FC2E64641E41A29EDD527A0D29419852130B43641E41222894A3870D2941BE99B00619641E416C480B11940D2941FAE9CBF7F1631E41769BC718990D294170A16751CA631E41CE4EC3039F0D294154C27FFEA7631E4112E0052B9B0D29416224A5BB72631E417A20C718990D2941DC4CB88257631E4122238AA8940D2941E2E1557E2D631E41C45F0FF78C0D2941	2024-12-09 15:07:47.975
219	\N	\N	\N	TN6128H	4	2	\N	010300002006740000010000000700000034C8E3D0275F1E41582F46E58E0A2941E809EABA2E621E410C6BB8D0150A29411639505AF9631E41803D100C020A294106DD67ED72641E4150060F254F0929417C3B82AF87631E4118B96C5D3C092941D4AD7A50FD5E1E41B48E6EA87809294134C8E3D0275F1E41582F46E58E0A2941	2024-12-09 15:07:47.975
220	\N	\N	\N	TN4778H	13	\N	\N	0103000020067400000100000021000000166D4BF670611E41B0F11A32D90B2941065FA9B871611E418056223EBE0B29418EEBDA4676611E419048E7FBA80B2941DC33AAB871611E4124D0A432870B2941541803216A611E41E6DDDFF9740B29419ACC2F5566611E412EC844C85A0B2941DCB303216A611E415C5682BC4C0B2941308B35AF6E611E41D00EF61D240B294106814EF670611E41ECEAFF560D0B2941DAFF3A0977611E41188FF8CF000B2941309D22C274611E4108C9A9A0F10A2941048BF13370611E41963B8CFFE60A2941602FCF385D611E41FA15718BE00A2941B471C02A44611E41F2E9B506DF0A2941640F995A01611E41FCF7412AE00A2941826ABB5FC5601E4144E51723E80A2941AC75B1ABB4601E41F036BFBAEF0A2941841E7BC3A7601E41F88BC641FC0A2941B6AA3F066B601E41569E3212160B2941AAE8A1A74C601E4126458141250B29412EAFEB7C53601E41BC86B2CF290B294100DCD70A81601E414CD988C8310B294160443069C8601E410A80904F3E0B2941F4E53E77E1601E41DA48C40A470B294120634D85FA601E414C4C8943590B29416439B95514611E41FEB15503780B29419C4996D528611E416AD75024970B29417C3E874237611E41DA0BE7FBA80B29415EF490F647611E418ACC1AB7B10B294174EFCB385D611E41702F07CAB70B294190436E765C611E414EDF3A85C00B29419A575A8962611E411EA989B4CF0B2941166D4BF670611E41B0F11A32D90B2941	2024-12-09 15:07:47.975
221	\N	\N	\N	TN6127H	2	\N	\N	010300002006740000010000000C00000040B66FB4934E1E410E61997EA01129417E21B424124F1E41E48743E76E1129418064752CE04E1E4178BE2E183A112941500DE09C7C4E1E418CFDBCD517112941D27353AF694E1E417A929C0023112941A47BC67C1F4E1E41C26B46AE28112941646C3D7DEA4D1E419A0180371F112941686D8AB7024E1E41D6379D1E36112941C87F2B4D264E1E41D65ACA8359112941F219C28E414E1E416AAF4A2675112941D27237DD544E1E417E65C0748811294140B66FB4934E1E410E61997EA0112941	2024-12-09 15:07:47.975
222	\N	\N	\N	TN6127H	1	\N	\N	010300002006740000010000000E0000008A992DD0CD4C1E414E96D57FE311294136830E5E234D1E41C84046A4F21129411CFA63D61C4E1E4136166734B0112941A4F49A2CFE4D1E41740E06497611294108913A86FB4D1E417AF0A28D711129413CF81612964D1E41AEE5E54C5D112941780FE4A9924D1E41EE87E8615F1129414477401D804D1E41969F932D781129419EA1B762824D1E41FCC23DDB7D1129419251882D944D1E41CE9AEA9D851129414CF92A756F4D1E41B408AEFF8C112941E08E7B9D654D1E41142F506E8C11294102D86ADA214D1E41D2B16F6AA51129418A992DD0CD4C1E414E96D57FE3112941	2024-12-09 15:07:47.975
223	\N	\N	\N	TN5925H	2	5	\N	010300002006740000010000000E000000461C8412D7411E4142C5AF689E2229418C2DB77775421E41AC7A0801A7222941048D629B7B421E4122E323BAFB222941E242A5E4C5421E41C0230E94F9222941E6277BF6C8421E41BE605720162329412CCB7FB2D7421E41BE1C1A6A1E232941CE57B576F9421E41A2443090202329419C478C88FC421E41AA2E230BF8222941427FB269EE421E41C4508B5EF0222941CA0AB6C7F5421E4184C50752A3222941FCD9DFB66E421E41E2B7196B9A2229412414C75B21421E418CCCE9118B2229416AFC8005CC411E4146C510A280222941461C8412D7411E4142C5AF689E222941	2024-12-09 15:07:47.975
224	\N	\N	\N	TN5925H	3	5	\N	0103000020067400000100000007000000705CAEEE1A411E418A97D4FBD321294140489333CE411E416A49B96ABF2129411405E70FC8411E41C0EDB0A1A52129414457393DBE411E4194C042E39A212941182DC9F86B411E4174EF9CD9AA212941ECC4DA3A1F411E41ACBB77A7BC212941705CAEEE1A411E418A97D4FBD3212941	2024-12-09 15:07:47.975
225	\N	\N	\N	TN5925H	4	5	\N	01030000200674000001000000050000008CC4716063411E416E27E3307C21294130C0CAA76F411E41D20B2A5F91212941F2C8DCE8A6411E4144D1FBB485212941CE0C2E6799411E415A15A00F722129418CC4716063411E416E27E3307C212941	2024-12-09 15:07:47.975
226	\N	\N	\N	TN5925H	5	5	\N	01030000200674000001000000080000004EC6534907411E41AE007D3B8B2129418C419A9F5C411E4150B24DE27B21294136B8C0804E411E4176E7C5F063212941446A7FE58B411E4144D56CA957212941F0A078CB75411E413E717A06402129416E17FA52F7401E41983E568355212941948C503CFC401E41B884B535742129414EC6534907411E41AE007D3B8B212941	2024-12-09 15:07:47.991
227	\N	\N	\N	TN5925H	6	5	\N	0103000020067400000100000007000000D87ACB68FE411E412A0240E167212941A6E33303D5411E41C8286583362129415C3B9258AF411E413452106E36212941A64367BBAE411E41AED5E72E3D212941E28CC30FC6411E4194DB092B6421294194389D2ED4411E411E1BA43573212941D87ACB68FE411E412A0240E167212941	2024-12-09 15:07:47.991
228	\N	\N	\N	TN5925H	7	5	\N	010300002006740000010000000A000000C81E4E709B411E410AAF7C08F2202941849515EA6F411E415211658DD1202941747E4A2F55411E4178AF8524C12029417EAE766E41411E41384B5569C9202941B4E95542E3401E410CFAB981C520294188D285FDDA401E4150CB299CE0202941E018F2E7EC401E418A07CC2FF9202941B0EB266BF2401E415CBC9FF00C212941EE2EF0647A411E41FE5CCD7BFB202941C81E4E709B411E410AAF7C08F2202941	2024-12-09 15:07:47.991
245	\N	\N	\N	TN7550H	6	2	\N	0103000020067400000100000008000000EC4F076353891E41582176C8DD2329419EFEEAFD408A1E41BA56845DC023294136EDE3D4418B1E413C3E1A3A87232941FE857EA8E18A1E419C8680EECF2229413088F0388E891E41E096F8A3DE222941E8030C5D39891E41BC3D09EC252329417A206FD634891E4100C67CB382232941EC4F076353891E41582176C8DD232941	2024-12-09 15:07:48.035
229	\N	\N	\N	TN5925H	1	5	\N	010300002006740000010000001A000000D64FB96897411E4186D2E34C10262941D4E2D6FD46421E41D4A11B881A2629417E32A8974D421E41B0B62FBD05262941584E952E98421E411ACDA0E5F52529415EAB7CD677421E41CA8E1042B02529418A7A733531421E4152E3D72DB8252941FC2FDBAF22421E41E630E70BA4252941F8A4181B1A421E419A040E9D8C2529419A1C69E20E421E415E8A975167252941966EFB6BFA411E416E8738B93E25294178BB1776F6411E418884671F38252941F2181A28D2411E4150E02006422529414EA99DACBF411E41DEA78BFE442529413418348DAA411E41B853175843252941E2C2B71198411E41807533623F25294180D5444484411E41ACEFD1173B252941521CBF1A73411E41C0C5F27836252941725639F161411E41DE1BFC2635252941D236B81E50411E41DCF0ED21372529415E59615B38411E4170994A153C25294190ADF73B23411E41F2EA245D41252941627E470318411E419892FA4D472529418CC6C37E2A411E41A6F0C6904E2529416E7ACA7A4D411E41CE1DF0C65A2529416A13A66776411E41F8F11E209C252941D64FB96897411E4186D2E34C10262941	2024-12-09 15:07:47.991
230	\N	\N	\N	TN15615H	\N	\N	\N	010300002006740000010000000A00000038701E651E361E419E3AC2E60518294196CD7C0BE6361E41047EFFF7BD172941CCE631D268371E4180DD643EDF1729419C83A80E9D371E41BEE3143A841729416CDAAA3DDF371E416680E66620172941BC03AC2545381E41A296DB1EAC162941C4E6BA018C361E41664EC5EAC31629413CC4249DED331E41C2C2ECD4C71629419E4D498333351E41D492E84F8017294138701E651E361E419E3AC2E605182941	2024-12-09 15:07:47.991
231	\N	\N	\N	TN15777H	\N	\N	\N	0103000020067400000100000008000000DC9D98C05F341E41FAC6AC3ABE1A2941AE2B0B0F65351E4154C3AD3ABE1A29415A95C0D6F8351E4172E2D6A5971929415823DE05DD341E411C6ED75A321929412E189FDDD0331E4184B23301FA192941364152C2D5331E4114269F98511A2941F8C5E9117F341E41E43226106A1A2941DC9D98C05F341E41FAC6AC3ABE1A2941	2024-12-09 15:07:47.991
232	\N	\N	\N	TN9730H	\N	\N	\N	01030000200674000003000000430000007CEAD03596301E4170FEECCD351E29411A99AA60A8301E4140E65E7F141E29411AE704F9E8301E412ACDF705E11D29416CE90C4B78311E41AE71BA2F861D29418C26BCDF23321E412899F74F271D2941561F97E592321E41A04C93A4DE1C294104923315A7321E418202C85ABF1C2941BE407C23AD321E4160748D2DAC1C29414C3E67FD9C321E41027F4F57511C2941E643ED06A1321E411458A814351C29419650489FE1321E4150B39C26D01B294112836AD8F9321E41467003C5A61B29413E9276EB01331E4118BC533D6D1B29410C61E6CEF5321E41DC217DE0451B29414A833579D1321E4132E833F7E21A294164133679D1321E413226209FBD1A294130E24C9FE1321E41E00A795CA11A2941129AF4E1FD321E4150CAC6067D1A2941549FD48342331E410484547A411A294140B09FDAD3331E41E4629F7BD5192941825D815775341E41A85535595A1929413606C02DD0341E41FCBB2FE22719294190130FB308351E4178334E72F8182941FA68C2082D351E419CCFF4D9B71829411845162A3B351E4136AF1BAFA51829414EA8EAB877351E4170F2B1678718294166AD1269C2351E41041124196618294192ED3FB5E2351E41B66CF7CC45182941C28355071E361E41523AC2E605182941C060802533351E410293E84F8017294168D75B3FED331E41B0C2ECD4C716294188148AF6C0311E415A8B15433217294190327430752E1E41D86DC9F75718294108280D843C281E41224060A0511A2941484563BBC8251E41A0321AF14C1B29410661ACEBFB271E41CADD790D321C29414814EF7710291E41EE8F41F84F1B294128E4FA6575291E4122F02804551B29414CB3C1064D291E41E817FAC4A61B2941D69A38CDE62A1E412CC3DA66EB1B2941409A12A3F32C1E4196EF2ED23F1B294154AE4AD2B92E1E41E6D7823D941A2941F6E210BA61301E4156A54C7CF41B2941C0F01DB3852F1E412C1123B4781C2941E6F478950C2F1E4188393AF2B91B29419629B2493A2D1E41E6062843DC1B2941100425EEA62C1E411867FBD1181C2941AAEB1517B02F1E41C0D16165301D29419C9F56D3262F1E4118D3A109761D2941C8650CED392C1E41B24668C27E1C2941843762E9A42C1E41E864FBD1181C2941D421493D3D2A1E415EFD5320131D2941DAE04EB46F2A1E418E5D463F201D2941BA6765B5DC2A1E41DE22F994441D2941E02A1AE65D2B1E4158F35C8AD31C2941647995232A2D1E413E18AB1C7E1D29414276D5DFA02C1E416ED8CC30F31D294116F32EBFB12E1E41A2FAB156DC1E29419AF4645D612F1E41366FA3BF2F1E294192E680FAA32F1E418CA826FB481E2941BEF6FBA659301E41007D6A6D791E29419A30CBA47F2F1E416645DA06271F2941467CA4AAEE2F1E41BCD84F614D1F2941129137A257301E41825C5D67E31E2941CE34700180301E41B8903EFCB51E2941DAD13E198A301E410240A59A8C1E29417CEAD03596301E4170FEECCD351E2941080000002E73A4E592321E41744BAB816B192941941A38E8BA311E41C867651CAD1929412024DB44BA311E41A6A43C45AD1929414CC875085C311E41CE5519655F19294128E476E3B8311E41A4EAD32444192941E0205B4676311E4134E8BFCC1E1929410A3FC668F1311E41E8675685001929412E73A4E592321E41744BAB816B192941080000006032FB6ACB321E411856A75F3E1729414E7D727BAB331E4184A303EB0C172941CE39037314341E412294A85F3E172941300F0EF28F351E41C42C0A4A0E182941E453ECC336341E411CD3F950EA182941849090BE22331E41AE629050D51829410606FE06A1321E416A9825DADE1729416032FB6ACB321E411856A75F3E172941	2024-12-09 15:07:47.991
233	\N	\N	\N	TN6715H	\N	2	\N	010300002006740000010000001A000000F85B5D6FBE611E41B69269F1FC232941E4C15033CC621E41E66632540C2429417E197C7876631E419EE2E18F29242941C064C75688641E417440852619242941D002572AD1641E41DC4E66B01A2429418AC3059781651E41A28341F2242429416EC2A73B9B651E416641B8893C2429412C3CE0020A661E416ADCF0262D2429413EAC77090B661E418CD1F003C4232941C8A26BA39A661E41E0014F5FAA2329419220536769661E41FE6ADE0F8A23294166FD0D02E2651E41D62FCB37A423294134FB7D4AED651E41BE6F03E3BE2329419465A3EC8E651E41F0014E66BF232941D21413359A651E41E2563B95EE2329414462836151651E41B08D472CF22329412897FAEA3E651E4194F453B5CB2329410A7A150B1C651E41E8FC72014C232941A0B56379DD641E4144314DF66E2229411E48DCF4A0641E41067EF5B1EC212941C0B01EF801641E41981A5FDC7E222941304974DA5D631E41C4FF83C4F2222941AAA8025AAA621E415E616AB23F23294100C90114D8611E414238F97E732329415435961AD9611E416CBA1E60D2232941F85B5D6FBE611E41B69269F1FC232941	2024-12-09 15:07:48.007
234	\N	\N	\N	\N	\N	\N	\N	010300002006740000010000000F0000005C4E102171631E412A684F7517252941AC34D61E8C631E419A9C2E571B25294196015E7DB8631E41727EA66C2B2529418650AB90CD631E41783FBDD1322529416C9E6B47F3631E41706E1E823B252941A02E771E10641E41762DA5C23F252941587EF74229641E41A0E75A773E2529419C0194133F641E41C61569CD3C252941428F9FA129641E418870DB271B252941087E29610F641E41CA5A006FE42429414082B220F5631E41B48FCC88EA24294146B7AAE6E1631E418CFDB44EED242941C6333D8AC6631E418041FF99EE24294130E59C1CA7631E41E8CC73E7EA2429415C4E102171631E412A684F7517252941	2024-12-09 15:07:48.012
235	\N	\N	\N	TN15216H	\N	\N	\N	010300002006740000010000000A000000FCA5C9E2CF661E41766AE4635E2329415CD74EC0A1661E4180D2AD7E23232941AA19AA31EA651E4144CC8EBDFB222941EAC048C296651E41D8569D15B42229415C026BF18C651E412235596788222941DA44304E44651E41DC0EDCB5922229419418716DA8651E4106854F1D1D232941C806BE26B7651E412E1CDDC649232941944912CF52661E4154B1EC1478232941FCA5C9E2CF661E41766AE4635E232941	2024-12-09 15:07:48.012
236	\N	\N	\N	TN9026H	2	\N	\N	01030000200674000001000000330000005807B41148491E41F29F06651616294160103CE58A491E41BAC35DAD0B162941489B79A2A6491E4160F26FDFF61529410CED84B3C5491E41CCD6A792DF1529411483A8ADE5491E417AB9F564BF152941329077F0034A1E41844B7E6A9615294164D0EA114D4A1E412AD836D47D15294192462ECF854A1E41FA6DC25963152941B2881F1DA94A1E411455859C47152941C03C9CF0B14A1E411EBB25D42615294168008A97894A1E41CEB49D00E4142941C8B234946F4A1E418C3E17EBB8142941F8C0D95F534A1E41D8AF667579142941F22C51333F4A1E41E0884D1C34142941BA02C8062B4A1E41BE067FD91514294166C2BBAD1F4A1E41DC4CB2EFC81329417EAA4D33224A1E411E0FB4489A132941D847ED11304A1E412A8A901658132941E8CE47953A4A1E4138677BE9251329413EA394492C4A1E41EAD7C32C0B132941C0470D76E9491E418E5A9B21E9122941AA57E91C6A491E41C89DB12CB4122941E4028A5449491E41CCDE2700A01229415E03A75F31491E41D83F86A183122941AE2F048106491E41B6F8EA7418122941BC369006EC481E41EC1FE2F4EC11294134BF29E5DC481E415450EE26BB112941E89B178CB4481E4158487B0572112941063EB9CC80481E41C07A9D3A141129417A51965EDE431E419681B13728122941F207DF1B34441E41FA8A233234122941A4736A96C2441E4110EB148057122941B0CDFEC210451E4110AE7A48951229415A7865E41F451E414C2D34D9B91229412439799619451E41023E23CE0B132941E470C3AF15451E41447254853E1329416460461613451E41F0A2A7506013294110DCD65E3A451E4168826A3290132941448E2ECE6C451E412A204E27A81329419474888B19461E41941C4A4EC813294106C06941B6461E4104217D79E5132941983DAE3213471E4154A52F6A1D1429412097FF96D1471E41845E22DF7D1429410288F38B40481E4116C27DCEBE1429416CD983BB78481E4132A125B0DF1429413887D7CED2481E41BCEFF96F3315294198A0DCCEEF481E41C03225FB6315294182B8870609491E41B4C28AC3A1152941C03A945F14491E411E5EC3A7DD15294186BC3F972D491E411E005054001629415807B41148491E41F29F066516162941	2024-12-09 15:07:48.012
237	\N	\N	\N	TN9026H	1	\N	\N	010300002006740000010000004F000000582D2200D3361E41421E8D63E61D294128A5B9B868381E412A3490EBBC1D29414477DF83F3391E416E97723FA71C29413E77388000391E41A875D2E5C6192941A865641EEB381E4152B01A5AE4162941F2EA8867D1421E41028FA5B2CD12294100F2F13116481E41F884F591EE1429413AFDE21B2E491E411298B73E161629417C7E22321B491E41FAFB2A92F31529414E9CE76C09491E414C49CDC1DC1529410C08325EF6481E416E1A724AC41529414E00B658EC481E41ECA8A166AA152941347E25A3EB481E4186AB176A94152941AEDD5B20E3481E414A1B760B78152941984E63D9CD481E4162EC5709511529416052FFB093481E41E69AF4081F1529418674364755481E41FCF46D75E3142941BEBA59E4EA471E4154EBAD14A0142941DA37CEC958471E41F293396B521429414888C18917471E41FC61CFB1351429412882962EE5461E4114A1C81115142941A03BAA71C6461E414A699B2701142941665DDE868C461E41DAFFD583EA132941D268A2823E461E41D2010AD9D9132941B6C48B52CC451E41226D1092C4132941E6EF8FD470451E419C30705BB0132941A274FB2447451E41144BC325A7132941E0CD3FBE2C451E4198871D049A132941B8C5391E0C451E4172E99BE876132941C4835839FD441E41709CB8DB5F132941067E41D7F6441E4130EEC7753D1329418E9B6342F8441E4134919561201329414C967BA4FE441E415C39634D03132941FC4F97AA07451E41EC719231DA122941968D729B03451E419C51E59ABA1229413407E98101451E4174EDBF43AA1229419E38E99EED441E41DE1962578F122941A88C951FCF441E41B0A5948476122941DA726AC49C441E41B8C383DB5A122941DCC1AECC33441E41D0727E634212294166A23242F3431E41A4A101C0371229412A6C0A37D1431E412ED3DF5436122941AADEDEDB9E431E417426927538122941DC89D86D12431E4188483DDD4F1229411E06D2FF85421E41E4154FAE7312294116BE18582D421E4120BB1DA994122941DC700E68FC411E415C977128B312294104BFE8C5B4411E413ACCC13EF71229415AFAEB2E8F411E41447ADCF00D132941D68883B644411E41544FB5F429132941829E5E2DC7401E41AC2AC7C54D1329410033510650401E41743EAD2275132941F42165F019401E415E5CC60087132941703BC09BAD3F1E4176011373B71329419E109B12303F1E419690F0EEEB132941D06683FB873E1E41DAE38DE42D14294180AFC6EA543E1E412CC701A745142941466D4DE2B83D1E4190FEEA537D142941567EA84C563D1E412650FBFC981429414A9B9E75EF3C1E41BA544D54AF142941106065C1B13C1E4160922430C3142941BE720AD4063C1E4192C2721EFF1429417CD72E4C4B3B1E418E2613DF40152941E8E05005A73A1E41562B73787A152941AC950A9C573A1E4106FA6C8390152941A0B1AB51CD391E4144A05FE6B61529418EE739DD56391E413AFDB3B8E115294190293D4631391E41D893E4A4F615294154BC31DB0C391E41F22C22EA0A16294186E5EB2FED381E411C5AC2202B1629418407FCF1D2381E4104E53C8363162941521DF551B2381E41486FE8EA7A162941942A9A3273381E411A05039D91162941BC03AC2545381E41A296DB1EAC1629416CDAAA3DDF371E416680E666201729419C83A80E9D371E41BEE3143A84172941CCE631D268371E4180DD643EDF172941A28003FA64371E419471844074182941582D2200D3361E41421E8D63E61D2941	2024-12-09 15:07:48.012
238	\N	\N	\N	RN2065H	17	2	\N	0103000020067400000100000009000000BC29E5D40B8C1E41B6416CC3642429415C0931FF7A8C1E417460DCE8392429413C69874FDC8B1E41E499D08EA4232941C070C69FCA8B1E41FAC57F41A9232941CE24ED6FAB8B1E415AD39FDFAE232941B8D08D97888B1E417A7A7291BA2329410621F8A7678B1E41FA8AFD28C32329414094B1BBAF8B1E417A2352B9FB232941BC29E5D40B8C1E41B6416CC364242941	2024-12-09 15:07:48.023
239	\N	\N	\N	RN2065H	16	1	\N	010300002006740000010000000D0000009ED8781D618B1E41CE5D4268A223294172859F6C618B1E4142E9D256A22329417AA51F9B5D8B1E417E543191B22329415056F651698B1E41FC5A1315B0232941823D3B5E7D8B1E41423E887DA72329417A9E01398E8B1E41A0E75744A0232941902CA586A18B1E41003283519B23294118FAACC8B38B1E416E444687992329419480667CC68B1E4156D6E3B197232941588442B8D48B1E4142CA379A9A2329419216474DBB8B1E4128393D3A842329412AF5B671618B1E415625D11EA22329419ED8781D618B1E41CE5D4268A2232941	2024-12-09 15:07:48.024
240	\N	\N	\N	TN7550H	5	2	\N	0103000020067400000100000005000000E41A5F395B8B1E41A682603151202941804D896D0D8C1E4130F6AD776020294120F982204A8C1E41FA19B36DAF1F2941B01155DDC08B1E41FC93C4A9A31F2941E41A5F395B8B1E41A682603151202941	2024-12-09 15:07:48.024
241	\N	\N	\N	TN7550H	7	2	\N	010300002006740000010000001B0000007AA51F9B5D8B1E417E543191B223294172859F6C618B1E4142E9D256A22329419ED8781D618B1E41CE5D4268A2232941B02D0264508A1E41B433A07BDE232941F87A58A4A2891E41D6EAAD70F4232941F433A12A56891E41FEFDC81AFE232941A6B730B155891E4160EF365408242941A8331B196A891E4128B4663C0E2429412E5E5D0F78891E415A4185210F2429411CFC786A95891E419C78385F0B2429417C10F495BE891E41B689DA99022429415850EE81F7891E41CE762230FA232941341958AA1B8A1E4178CD3F0AF823294130EAC1D23F8A1E4154587ABEF32329413A6F5F04738A1E410C8ECF36E7232941F654D503908A1E41DCAC9E43DE232941F0380262B28A1E41F8EA9A22D523294168ED1AEEC78A1E41B6756469CF23294158A4DC5DE78A1E41B06C6B3ACF232941922F0490FD8A1E41389BD5D6D0232941DA03C069068B1E4108D72F7BD0232941923043C7138B1E41F4D2A6CCD0232941AE4DB4C7218B1E41AEBF9CA9CC2329419C2780992C8B1E410EAB9AC0C323294164C9A8253D8B1E416C68FDCBBB23294130150C9B5D8B1E41C0798491B22329417AA51F9B5D8B1E417E543191B2232941	2024-12-09 15:07:48.024
242	\N	\N	\N	TN7550H	4	2	\N	010300002006740000010000000B00000084DA350C92951E41ECDDF6B25C20294138A40899B7951E415ADFABEB2D20294114E194DB4F951E4190945CBC15202941EC1D1293FA941E41ECDB5E0F47202941160ABABFBE941E41C0F844E274202941B8F5C8F24D951E418E1938C1AF20294140E6DD307C951E415C2663A2932029412445656875951E41A6095C11862029417C78A1663D951E41D45343F96B2029418410F56767951E4112CB970F4E20294184DA350C92951E41ECDDF6B25C202941	2024-12-09 15:07:48.024
243	\N	\N	\N	TN7550H	3	2	\N	010300002006740000010000001900000038F3DEDA54921E41B85D25CA282329414C332FF375921E4178B0F1055C232941F2D5C5968B921E41C490872A91232941809842397E921E412EB61AFC9423294130EAE73BD2921E418C79F343D5232941223868B0D6921E4110E45A8B07242941D24B6A99DF921E411C5289680A2429417CDE9225F0921E4134417F450624294118CF7054FA921E414E80228B002429413276AEFA63931E416CE41A5105242941CAC4315871931E41D6AF060BFD232941EA829AEE53931E4190A63A2AF12329417434E32859931E41184B81C4E62329415A747ACC6E931E41E4C19F2DF3232941CADB6273ED931E41AABB4EABA9232941001FEEA0CD931E411A54E112852329412861721393931E4176E63DCD8A23294150E2E61162931E41A22184587F232941443CA29B25931E41585BFA3F572329411A3D3499D8921E417EC7BDD7662329411049A92AB4921E41A6EF4FDC392329411C5AA997A7921E41D68703F9322329418A9F2A0CAC921E41FE7F92F8242329411A5D34C587921E4150A3BEEC1E23294138F3DEDA54921E41B85D25CA28232941	2024-12-09 15:07:48.033
246	\N	\N	\N	TN7550H	1	2	\N	01030000200674000001000000180000004A4835EFAD891E4128D6535FCB242941707D6020538A1E41AE0E80D1D724294176E0528B708A1E410670689EEB2429413890F47D588B1E416EDDF2DFB52429415C4C10A81D8B1E415EED93546C2429414865FD24898B1E4176DCC1C05E24294124760219558B1E4154264DFC0E2429410670383A488B1E41641BA4F104242941DCDBB9B5348B1E4186571EA406242941484A19602B8B1E412AC3BA27FE232941C2E293122D8B1E4192CBDA0FEB23294194A0158E198B1E41982B5C8BD7232941BE6DF6B3FC8A1E417A716726D4232941AA2EBCD1D48A1E4166232A4DD32329418269E56BB58A1E410037BD1ED72329415C3B0A34848A1E418E3B6BF8E523294178C342984C8A1E411C2AB2BFF623294184CAA00A318A1E411AA02656FA232941A236EC75078A1E416A9F632FFB2329418A52691FE2891E412024AE8C01242941C0CECA56A4891E414CA0B1140C242941FAD0FB538C891E4146E6712C102429412E2BDBD167891E41E8DA28B0132429414A4835EFAD891E4128D6535FCB242941	2024-12-09 15:07:48.039
247	\N	\N	\N	TN33878H	1	\N	\N	010300002006740000010000000A0000004E65B1AB6C7F1E41442ACB7AC61D2941FA1005BD977E1E41BA5830F8B61C29418041E613287F1E419C164321971C2941A09557C95B7E1E41D451DD49DB1B2941223B6977D47D1E418C4F886BE91B294152D3B9004E7D1E41A6C2F1996B1C294104EE5DF3DC7C1E41A00FABE4631C2941C60A90BD7E7C1E4100E2CBF8B31C294114FF149B267D1E418ED532A2A71D29414E65B1AB6C7F1E41442ACB7AC61D2941	2024-12-09 15:07:48.039
248	\N	\N	\N	TN33877H	1	\N	\N	0103000020067400000100000009000000965021C15A801E419A8952E4571C29418041E613287F1E419C164321971C2941FA1005BD977E1E41BA5830F8B61C29414E65B1AB6C7F1E41442ACB7AC61D2941940F2BFA707F1E415668D8B7C61D2941D670AB12D0801E41AAEB4952D01D2941880B1D467F811E41EC0BAA62E21D2941EC7ECC8FDA801E41ACFBF83D311D2941965021C15A801E419A8952E4571C2941	2024-12-09 15:07:48.039
249	\N	\N	\N	TN33876H	1	\N	\N	0103000020067400000100000016000000E67F2E1FED4A1E41C2707DC2AC212941E0F914DE4D4C1E41AA71540D72212941B0E62D6C9A4D1E413EFA72973B212941F414CA95CF4D1E41BA30065550212941F41B641EE44D1E41029B2B234F212941780DD79BDE4D1E4100810C7A122129413A883B49DB4D1E4164937DE5ED202941C01B0723C64D1E41DED0FE60C4202941CCBEC7B4D64D1E4144D1A879BB2029419A5DA14EC94D1E41DC3E0C666E202941CA8D6B571C4E1E414C0995616B202941203A5260144E1E410ACB04DF28202941563913F1EE4D1E418665839D2D20294128A26C8D9F4D1E41B8784A2EED1F29413A7EDC17344D1E419EEC6977851F2941EC5D3B94FE4B1E411892D44FAA1F2941E89D42BFF84B1E41766205C9CA1F2941E60F8477384B1E41A6E320E8E41F294120E13FA96B4A1E41A87560B50720294116223B34894A1E41EC1BFD4A73202941FAE5BC7E9E4A1E41482A5DB4DA202941E67F2E1FED4A1E41C2707DC2AC212941	2024-12-09 15:07:48.039
250	\N	\N	\N	TN16391H	\N	\N	\N	0103000020067400000100000006000000A6D3A7B0906E1E41CAF6D8C4A41E2941A6100E5E836E1E41829C15368A1E2941E0031A27056E1E41E04048DA931E2941D010FDBA066E1E41580CFE65A71E2941604FA4AC4C6E1E41765134A4AA1E2941A6D3A7B0906E1E41CAF6D8C4A41E2941	2024-12-09 15:07:48.039
251	\N	\N	\N	TN6582H	1	\N	\N	01030000200674000001000000070000004C549B69D96A1E4130EF0D79111229415047B262BC6A1E41C8CFC72DF611294110286C17A16A1E413E6DF675FC112941DAF0544AA66A1E418CA153A4061229418E11C90F916A1E4142AF53680B122941FE276C17A16A1E41867582FC1F1229414C549B69D96A1E4130EF0D7911122941	2024-12-09 15:07:48.039
252	\N	\N	\N	TN6582H	2	\N	\N	0103000020067400000100000005000000F4AE95794D6D1E41D0D548B678122941142070CEBB6D1E41BAF15FFB691229414EEA867B906D1E416248405F31122941D6664FE2236D1E415097BC1F42122941F4AE95794D6D1E41D0D548B678122941	2024-12-09 15:07:48.039
253	\N	\N	\N	TN6582H	3	\N	\N	0103000020067400000100000008000000E8599FE6586D1E41E8B70DB508112941C453B6413E6D1E41C0251906F6102941E8C36FA5FB6C1E4176C20D480C1129416E099EF3E26C1E417A948D32FC10294118BB6EB79E6C1E41D2D60D6E13112941BEA4295AE06C1E411C198EA92A112941EE2D8751086D1E41B45402F71E112941E8599FE6586D1E41E8B70DB508112941	2024-12-09 15:07:48.039
254	\N	\N	\N	TN6582H	4	\N	\N	010300002006740000010000001C0000003C88D9183D721E414C32AB7C071129419E5046F24C721E4164B0F81500112941049B5E40A8721E41BC64BED9F5102941381B48C9ED721E41FE0EA753F01029413C832130FF721E414CCE4DA0EC102941A4B4304EE2721E4138774559B81029418A1002A4D9721E41D2E1D85EBA1029414C856667B6721E413EC33D42BD102941E0D5275F7E721E412408D81E6E102941BE3D378D74721E41BEA363856B102941066308D358721E41F6788A906F102941C620CAEA46721E411CFC99466F1029418C15BA8C17721E41A8662D4C71102941B821F86416721E41B0BBC878811029416652F0C511721E41C84D9ADE8B102941FC708BE20E721E41FEF1C88894102941EE644D0A10721E41FC839AEE9E1029415083E8260D721E41DE861EC6AA1029413AA8A2AF09721E41720CB253B610294124D99A1005721E417E155597C110294196282E8EFD711E41C83C93F7C9102941168A1E50F4711E4192C22685D5102941E0AED8D8F0711E4138F6A2BDDC102941AECD73F5ED711E41248255B7E71029419ACD73F5ED711E416C268461F010294110BB16B1EF711E415AB2365BFB102941A071A29FF6711E4198D3554F041129413C88D9183D721E414C32AB7C07112941	2024-12-09 15:07:48.054
255	\N	\N	\N	TN2579H	1	\N	\N	0103000020067400000100000007000000E0599FE6586D1E41F2B70DB508112941EC2D8751086D1E41CE5402F71E112941C0A4295AE06C1E412E198EA92A112941EAA6FB10126D1E4102B53C59301129415EBDCDED4A6D1E4106CE99FF3011294170E170B95F6D1E418AEB30DD22112941E0599FE6586D1E41F2B70DB508112941	2024-12-09 15:07:48.057
256	\N	\N	\N	TN12411H	2	\N	\N	010300002006740000010000001A000000608FA0FE3D871E419ABF4120E3262941209239782D871E4154631D07E92629412428738013871E417EF4241CF02629415081C7F5F7861E41D660848DF9262941AAA80813E5861E416C90FE6B012729419CDDB4E4CB861E41DAB20D960F272941B695FD16C0861E418E3141D917272941A2C409A17B861E41D6A61036622729410670E71E76861E41D474FDDD6A272941342697D77A861E41E0F8993E78272941D07AB95980861E41E808D59687272941A0FE55BA8D861E41F0C9568A96272941909A2F0A9F861E4106C254F3A1272941DA7B27AECC861E41E4E9CC3AB527294168A2ABFA62871E41A288762EDC272941EA8843E6BB871E41C649F821EB272941B01A4BFBC2871E413649C1F7C42729419C1A4BFBC2871E4134EC65B4A4272941409E2AE6AC871E4114F205C58B27294186B69EC892871E41741FE7F25F2729416AB6A23181871E4178A3CC0D4627294110CCC85260871E41B4816BF30D272941ACA13A456D871E41EA0BC8DDF9262941880E0E045A871E41C09C75B7F5262941DAACC0BF49871E41DCF481EFE8262941608FA0FE3D871E419ABF4120E3262941	2024-12-09 15:07:48.059
257	\N	\N	\N	TN12411H	1	\N	\N	0103000020067400000100000015000000FE25CEE956871E41A2F72BD2E12729419E1474A1BB861E411490FE53B72729410263F6DB95861E4148C7BD10A7272941CE5DD00584861E4168E193799A2729417C2B433C73861E410CAF06B089272941BCEB4ABE68861E41A2E3B28170272941960B47FD6D861E41F01A723E60272941D882F21A9B861E41E266E18D31272941D2C7106FB7861E41A63EAC8D11272941421FC04DDF861E41A6198A78FA262941985773ED01871E4154CA135BED2629415AC9F8341D871E414CC70070E42629413668E56F37871E410C988691DC262941D244E262F6861E411826014AC1262941FC32881A5B861E413CA2DE5ACD262941E2FAD47A38861E410CC2DA99D22629417C96BAE716861E41F4978691DC26294158DF164CDF851E41AAD334E26D2729417A8D8D43C9851E4180C4AA259E27294100D35C1BDB861E413EF81FB514282941FE25CEE956871E41A2F72BD2E1272941	2024-12-09 15:07:48.059
258	\N	\N	\N	TN14832H	2	\N	\N	010300002006740000010000001900000004874D8259711E41796E18340B2129414BB068FA03721E4106C17AAA3B21294176313E9CD7721E415DA8674D75212941C7A075A665731E41624A2504A221294191C183A22B741E412721966AEF212941EBDDDB729A741E4179B247C7252229412E366EC95D751E4186BA3B2AF021294103EEA5F76B761E4165BF409ABD21294116D02CBC5F761E41DE3055408F212941AF75361B0D761E41A3DF704A3521294123A60D78FE751E41B1974B4923212941354FD37A47751E414D0974AC6D212941DA02D81292741E4145E2323A04212941F1AFAE1D39741E413D246508C7202941EE9059E9DB731E414ADC68F79B2029416C9774364B741E412B4C4CCE6C202941E06B669F53731E4180C5C858E21F29414209A661F2721E419E3DFD7A0D202941C710AAFB5A731E41494DF607472029411F53781F49731E4162D9C332502029413104679A6A731E414F91608160202941716AAC007E721E41F75CCC36C5202941F96BB64557721E4129EE4DC7BE20294191BC2DC214721E41287C282D9120294104874D8259711E41796E18340B212941	2024-12-09 15:07:48.059
259	\N	\N	\N	TN14832H	1	\N	\N	0103000020067400000100000031000000F81D051A7A701E41C44E64E433262941C4A960BEE3701E419E7C39B2512629418C58CB8C5B711E41A82BDB3C67262941A4F3E70B16721E41ECED87551926294128B06E366C721E415C3C4D5114262941DEA2035E83731E41A8484AB1C1252941AE79A34465731E41E6F3AD4375252941B846DF4489731E41288CC3866B252941D291D40AF7731E4118A224CDD624294158E9C63012741E41C478C4B3B82429413668FA731A741E412ADCF6FAA12429414E3A68671D741E413CB52F5B73242941DA82FBB9D2751E417C50589517242941E4998701F2751E41C08FD63380232941001489511B761E41DE680F94512329418845A8D284751E4136D173CE192329410AF3E79F48751E4182605CE7EF222941A6B156C098741E4110025C93E522294158F4551884741E413C491361F12229417A9FFC6B58741E4170A57A3B0C232941025407A6EA731E41BA1A07D7352329414016B4BE9C731E413AD392CA4A23294140FD8EFD8D731E4120AEEA264D2329416C93428332731E41E620210AA8232941628C771664731E41A4B7C8D4622429411EB9DE21AD721E41D6A969B7632429411CF7FA02C4711E41ECC99CA661242941D69AD6E9C9711E415880099E45242941C2FB2CF6A2711E41ACB785134224294110FEC56F92711E419236B9564A242941120A495281711E41E6C99CA6612429419A9DE9E077711E41BE4AEFE59A24294128A43AD087711E41D64C0EE2CB2429418018DF2B1E711E4158F0E9C8D124294154726ACB28711E41C892203165242941702F6B733D711E4108E617203F24294164726ACB28711E41BC181FE13B2429415C2F6B733D711E4118F4F0BAFC232941AE956DF0B3701E414C831C95F32329410EF7C3FC8C701E4188CA162420242941E0141BB17A701E414EC34BB7512429418AD4B4D27E701E41908404D5862429411E2E407289701E41DA9F4892C6242941505CD27E86701E413A94C5AFD724294140C69876A0701E41820D4D82422529416C7E672BD6701E41EC48C42E802529412C95F372F5701E41A6484AB1C12529418A44523CEA701E4122F552C2E7252941F81D051A7A701E41C44E64E433262941	2024-12-09 15:07:48.065
260	\N	\N	\N	TN14831H	1	\N	\N	0103000020067400000100000009000000C059E60A63681E41608E5670771E2941006E2E597F681E4100796482D61E2941C00A21EF376A1E41608111BEB31E294140840479356A1E41A045B6216F1E2941806CCE53B7691E4100DB8E35661E2941C05FBC5547691E4140284449651E29418092A3CDE1681E4100DB8E35661E2941C056C57FAD681E4100843249691E2941C059E60A63681E41608E5670771E2941	2024-12-09 15:07:48.065
261	\N	\N	\N	TN14831H	2	\N	\N	01030000200674000001000000230000003070D449F6661E414CF78C516E2029413C52352078671E41DAB37E166D2029411A7EAD3033681E4190C64F7958202941C40BD3A56D681E418CE5B58BA3202941CA63292F8B681E41D6F8033D9F202941C83878079D681E4188EFD9B2B120294156AE3A06E5681E41164B4B64A52029418C3B332AAB691E419689C78B9F202941063209A0BD691E415C2E56DAAB20294170014916B8691E41369E8C28CC20294180B0FB8BD2691E41BE032201CE202941349CB33DB6691E41E092BE6139212941009EA777F7691E4104AB9E263C212941844236C6036A1E414423056229212941B4EAAC88926A1E411262818923212941663DC1FB446B1E4124DBE16131212941DEF46A47F96B1E41A4C71662252129417857DF94456C1E418023056229212941BC2110A9286C1E41F45E1664B120294124F664E4196C1E41366F763E4B2029410ED3E3A9F86B1E411C6D05B6F91F29410600BCBF7B6B1E412C383067FD1F2941369D47722F6B1E41B851BACB841F294172D02887EA6A1E41C09D7542631F294184906828136A1E4114A1131C291F29415A54903DBE691E41DC27B3431B1F2941BE42697A57691E4186315A1C191F29414AB128DD46691E4168A8496CD51E294104B86490D2681E416C8B54E2DB1E29414CEA4B086D681E41727D9844E71E29418C2F813103681E413ED05CBAFD1E2941D2DA4B339B671E419AA528E11F1F29414AD3489742671E416E410AF44E1F29413CDC722130671E4148ACAE2E681F29413070D449F6661E414CF78C516E202941	2024-12-09 15:07:48.07
262	\N	\N	\N	TN14831H	3	\N	\N	010300002006740000010000003400000072D7F5E45B721E41969E68295C21294198B303226A711E41A2DAECD4A921294108A61A3382711E41FC6DAAC04B21294144AC008611711E41EA68971C4A21294182A35DEF7E701E41B2C4B04C4C212941327D4880E26F1E418277D0084F212941001BAF65F86E1E41F28A1C99552129414AC1B8E1A06E1E41EC08BB4563212941A0110CCF656E1E414C48B29A782129417EFC1F44256E1E416218442F85212941E4A88C61EC6D1E418EBC2AFF8221294124B5D5559A6D1E411210BEE1BB212941C6796EF3156E1E413E80739FE1212941D8B12FF87E6E1E41385A2B7CF121294158B93294D76E1E414CCEA3E0FB21294168D2E1C5FC6E1E41462ABD10FE212941C8E16AAF1E6F1E4148CEA3E0FB21294166DF4703746F1E4180F9FEA7ED21294194F070E7CF6F1E41C4C8403FDD2129419CAFA6E32C701E4160B0E10AD521294160C0CFC788701E418EABCE66D3212941727F05C4E5701E418459DB7ED42129418CBB896F33711E41BC764D57DE21294138258C8E1D711E41D6BA5750F521294112DB1EF4E7701E41206451C4F4212941A0405E6CED701E41986EC70915222941D44CA7609B701E410C0475ED0D22294108A7209663701E41065B7B790E22294192D49E0900701E4156EC65B622222941EE6FE2426B6F1E41900A288C49222941AE7A8B3CDF6E1E41B88C89DF3B22294112368143C86E1E418A83B394552229412A5956BDF06E1E41AEA5381161222941E4F7D9EBCF6E1E412E933C7E7722294194796EF3156E1E41004EE28743222941005136D8CE6D1E41127067044F222941F6E4100D3A6E1E41E4F2E5A00A2329411AC358DCDA6E1E4146332DF33C232941E29A3D0A5D6F1E41602A57A856232941CA0B43C59F6F1E414C5E88BA2E2329412E96F7B107701E41F44DAFD3EF222941C6E5C7ED5B701E41F00855DDBB2229413CE3A441B1701E416A293A5F8D222941E2781F7156711E4196DE7CC73A222941C4A9DDD966711E41CAD96923392229417EBEC964A7711E410AB794A91022294178C6CC0000721E4118E19F73E5212941FEFF2D00A3721E418C0BAB3DBA2129414A519E3631731E41E45378DDB5212941C0C003F739731E415C402C4DAF2129417224A37405731E41CEDEAF7B8E21294172D7F5E45B721E41969E68295C212941	2024-12-09 15:07:48.07
263	\N	\N	\N	TN15341H	\N	\N	\N	0103000020067400000100000008000000F0A47BEBA6651E419AED85C53221294184D73DC750661E41242421FCE6202941D657FD718C661E41A0EC0670BB20294198A6FA401E661E41BC9F505B8A20294160E74904BE651E41C0199DB2412029412842DE6727651E41786E0DD5572029415C2603FBCB641E41C4C0837867202941F0A47BEBA6651E419AED85C532212941	2024-12-09 15:07:48.07
264	\N	\N	\N	TN15446H	1	\N	\N	01030000200674000001000000100000008461DA8306671E417C659D15511F29414A853B8F18671E415A443689451F2941A6C0986A1F671E410E6B2A403B1F294170F05EB14E671E41A4138C2FF01E2941DC43860390671E41F26D8871B61E2941AC4354AAD5671E416E26C65A921E2941E49187FE09681E41D8F2EF287C1E294122C8F0DB03681E4190B841E6321E29419C37BD15FE671E41DE0230D5171E2941824E25D9EE671E414EF02D95F01D294170375736CC661E41F828CE56FF1D2941864BA8D888661E419CE222B7F51D2941A2A0F942FD651E412ED00B5D6D1E2941E285D19A47661E41901AC8F2971E294154439FCFBB661E419C3C7A65EC1E29418461DA8306671E417C659D15511F2941	2024-12-09 15:07:48.07
265	\N	\N	\N	TN15446H	2	\N	\N	0103000020067400000100000009000000D46D2E597F681E41DA786482D61E2941B059E60A63681E414A8E5670771E2941047A8B2E15681E41D24FE7F4821E2941AC775D40E0671E41589B8692991E29417282DD5D9D671E4192FEBB37BC1E2941D242D5545E671E41A6449B46F41E294164C709A82F671E4108C17D6A3D1F2941E4DE078E98671E41C6D3EB040E1F2941D46D2E597F681E41DA786482D61E2941	2024-12-09 15:07:48.07
266	\N	\N	\N	Reboisement Andring*	\N	\N	\N	01030000200674000001000000380000009A2EB9EA11B51E412878081DA21C2941AE2E091293B61E41E277E88E911D2941062F998589B61E41047860DF141F2941B82E59F27CB71E4102782811AB202941002F290ECBB81E410A7870F206212941BE2E39113ABB1E411E7848352B212941782E49ADA4BC1E41E27770F206212941DE2E0988E2C01E412078805C9A202941BA2E39A068C41E410478984EF31F2941E02EE9D704C71E41FA774089E5202941C82E497974CA1E410278C8C969212941D42E2975FACB1E41387820A533222941A42EB9517CCE1E41E877E8DF7F2329410E2F2916B8CE1E410478204763242941C62EE9BFF1CE1E41FA7700AD3E252941E22ED94375CE1E410C7838CCD2252941A02EC9E3B9DA1E412C78B8A966282941EE2E6987C6E41E411A78D88CA6272941002F491CC1E51E41E677909E15262941962EF91F89E31E410E784037D82429419C2EF91F89E31E41FE77C8EC5A242941EC2E9928F1E41E41F077D01C66232941D02E6987C6E41E41307890EFB0222941C82E19B583E41E41FE7780F194212941EA8AC4BF5BE51E41909B1FC0E01D29416EC92BC7E0E01E41D66A334C991E2941B6BA1D0FBDE01E4180C284640821294190EDCED65DDE1E4144487DB4E02029412AA22C29E4DB1E41DE5BF21E591F29417AADD95E1ADE1E41107E2899CD1B29410C8AA8FF3DE41E41A850CDA3731B294130A55E95C3E61E41482A0F6E3F182941F6EC1247A3DF1E41C2B1A1FF471A29416A9A3B0650D91E411CBBBA1F361B29414C9A1C1E46D81E41400999173C1A2941AEA8E48E02DE1E41D6C4584B261829414CC6F74F12E61E41B6E0320BC9162941DC2E597B03E31E413878C019B4122941362F89C8D6E11E412C78008F98142941D62E994183E11E410078E02393152941022FA9AC88E01E410A78F0AAE6152941D02E892719DF1E41FA77F0AAE6152941B22E49472FDE1E411878E0AB58152941BE2E59B050DE1E413A7870CCE0132941022F49E8ECE01E41D877A01C0A112941DE2E892719DF1E411A78F0E1171029419E2E89E194D41E41DA774067AB102941942E99CB33D71E41067850E9A0142941AE2EF99EEFCD1E41FA77487D29162941E02EE993FFCD1E41E27738BBED162941C42EF91FDACC1E412078D08678172941D82EA9ACCAC81E412678601A53152941E22E29A7B4BB1E41E2777014E51729419E2EA9DF8CB81E41FC77C8DA44192941022FB937F4B41E41247810C9D51A29419A2EB9EA11B51E412878081DA21C2941	2024-12-09 15:07:48.07
267	\N	\N	\N	TN32099H	\N	\N	\N	010300002006740000010000002E000000B456A243AE431E41EE6F1541952E2941B4F5783544441E412022AAE8A32E29418A6CC61528451E41380695E7C22E2941081F20AA78451E417E760709BD2E29413E9C2D5CE7461E41A6336417502E294132241A29AE471E41FAF409A1572E2941E6CAD05BF1471E411431B6416E2E2941D837A20B10481E4108959CE49A2E29415ACFFD7F22481E412A97E128652F2941381FC5F208491E41B4E4B11E712F2941328A0C5E7E491E414EAC4A0DAA302941168DBA20634A1E41BC813A02A4302941548C4E96D64B1E4132A9276F83312941343CD7C4654B1E415CCD8F53B2312941F097F4BD414B1E410E488E07F83129418254F77FEE4A1E415609071599322941CEF69319A54A1E41285853D001332941BACF82FFFC491E41F652E2AAD7332941EE795554544B1E41289577AAC633294136E77389C74B1E4180828BE9AA342941AC504C20F74A1E41CC6243DA2B352941A20830591E4B1E415CE66D45AE352941325B109DC44A1E41CE15CA912936294176607A40144B1E41048A12C3A3362941A23984AF684B1E413E2FC3CAAD362941EE9F17AC2A4C1E41AA26D7A4CD36294122871F8DC14C1E41887C9224B53629417E909E661F4C1E415482197EE0352941881EC086094D1E41DEFE1C31A13429410C0803059E4C1E41B8C099A635342941FE25F6B80F4E1E4124D222C64A332941ECF7BB6BDE4E1E418CD17DE3B83229418824C1E3304F1E41DCFD778EBC322941A6B1FCD6BF4F1E41B8DBFDDF34322941B86B4BCA96501E4184D2B3515D32294158919A1BC1501E41BE9D47D1AC312941B820EAAE1F501E412A92526212312941042E08BB654F1E414E9805FA42312941C6391E795C4E1E41FA5AC3CF6E302941A2C3A63A444F1E41922BC1143A2F2941BE00BC9D494D1E41DAD60FB7AF2F29417A627CCCCD4B1E413CAEC9AAD52F2941E05251FB264A1E41AC036A20662F29412EB7623D36471E41B8D2DF76872D2941EA24E48BEB441E4190C68BB5462E2941B456A243AE431E41EE6F1541952E2941	2024-12-09 15:07:48.086
268	\N	\N	\N	TN32099H	\N	\N	\N	010300002006740000010000000500000002AB93084D471E412C43EC52802D2941C6ED09D03C4A1E41D0DB7480602F29413AD72CCD6E4A1E41D49D3E65612F2941DC4AF87D46491E417ADA2A5C672D294102AB93084D471E412C43EC52802D2941	2024-12-09 15:07:48.086
269	\N	\N	\N	TN33875H	\N	\N	\N	01030000200674000001000000090000003A13E8C79A4A1E41447BE6C5C521294186566B90724A1E41942B4F3CD7212941EEA6603FA34A1E41C647E8B4552229415EE40F59484B1E4194C65E4C4E222941F8A08C90704B1E41F6F8AE50A922294102AB3D99A54C1E41C64846DA9722294108351346E84C1E413068A0303A2229413E0BB8FF3D4D1E41E6F4D8955E2129413A13E8C79A4A1E41447BE6C5C5212941	2024-12-09 15:07:48.086
270	\N	\N	\N	TN33931H	\N	\N	\N	010300002006740000010000000700000040FC771F30621E4140D17AD6ED13294180AA85BC0B621E41E05CE8099A13294100F496AF70611E41403175B4B3132941C0DE24F386611E41C0133090E5132941C0A8DC65AC611E41C009B2810514294140EF51FC2A621E41604DCAC2EE13294140FC771F30621E4140D17AD6ED132941	2024-12-09 15:07:48.086
271	\N	\N	\N	TN33931H	\N	\N	\N	010300002006740000010000000E0000008026B0CA4B5E1E41603830B4CF1429410059D632435E1E41C01AB6E9A114294180E7889A205E1E418029B5FF5D142941C0AD5007015E1E4160A7C05E5514294140467A18825D1E41A061D0FF60142941C00A2279795D1E4120A37B78491429418064BD9D1F5C1E418015B5798114294140740CBCA25C1E41C0243E7087142941C0FDD340BD5C1E41A0749942B8142941C072E2900B5D1E4140FD34A9B8142941C03F056D0B5D1E41E0F30981BF142941002C813D0B5D1E4100DB0592C81429410022CFBD4C5E1E4160D3B8C3D41429418026B0CA4B5E1E41603830B4CF142941	2024-12-09 15:07:48.086
272	\N	\N	\N	TN33931H	\N	\N	\N	010300002006740000010000000B000000C0B5EF38B6611E41A00EC0992A14294180FA9E1682611E41E0EE4F3B04142941C0A609A56C611E4180FF2973F413294100BDC02945611E4180A793B1ED132941C0956BEEE3601E4160167ED8E613294100211C86B1601E4140CA6189D3132941803C9EAA5C601E416067BBA0DC132941800955E8AA601E41E02C00ED47142941407ADE9CE8601E41A0A9A05D3814294180487921F7601E41205249C246142941C0B5EF38B6611E41A00EC0992A142941	2024-12-09 15:07:48.086
273	\N	\N	\N	TN33932H	\N	\N	\N	010300002006740000010000000A000000102F27C50C611E4112F41435B114294110394ECD32621E410EBD7551871429414C274A0CDC611E41DC9163F451142941C4B5EF38B6611E41840EC0992A1429412C487921F7601E41FE5149C2461429412A7ADE9CE8601E41A8A9A05D381429417A0955E8AA601E41B82C00ED47142941C80BC09C6D601E413615204F5D142941F6183575C6601E416C15579AC7142941102F27C50C611E4112F41435B1142941	2024-12-09 15:07:48.086
274	\N	\N	\N	TN33932H	\N	\N	\N	0103000020067400000100000007000000F0FB771F30621E414CD17AD6ED13294108EF51FC2A621E413E4DCAC2EE132941B0A8DC65AC611E41B209B2810514294190E4EEABF7611E41A882D7CD4C1429419AA09A0F47621E41D8085E0380142941668266FC99621E414E426DEA6D142941F0FB771F30621E414CD17AD6ED132941	2024-12-09 15:07:48.086
275	\N	\N	\N	TN33916H	\N	\N	\N	010300002006740000010000000D0000004025120FF2611E41A052240F3115294100E3FBD7EF611E410087A18D3015294180BAEAF4D45F1E416075D9273B162941C046159FE15F1E4100EDD6F644162941406CD1CD1B601E41C04880067216294140825C4762601E41005D58B15316294100C31CA678611E41400F49F2B715294100AB4AA405621E416057222A791529414037ADC713621E41001A7BDE72152941C0E55E4919621E41E02DCD285C152941C02A24621E621E418083D52347152941408789490C621E418042960C371529414025120FF2611E41A052240F31152941	2024-12-09 15:07:48.086
276	\N	\N	\N	TN32917H	\N	\N	\N	010300002006740000010000000B00000000E3FBD7EF611E410087A18D3015294180CBDE08C0611E4180DB9A161F152941C0B2E40499611E4180BD520218152941C02EED3C77611E41E06F2EE111152941807A340E2B611E4160BBFAAE12152941002CD9BFCC601E41C09BA1051815294140E6F1AE8E601E414052A1E76C15294180E3D2ED32601E41C094D6215C15294100C67C5C5D5F1E410016BAFEEC15294180BAEAF4D45F1E416075D9273B16294100E3FBD7EF611E410087A18D30152941	2024-12-09 15:07:48.102
277	\N	\N	\N	TN33847H	\N	\N	\N	0103000020067400000100000005000000DC5368091B781E417AB82A82151D2941C69009E550771E4174ADD20B831D2941FC710DB4F0771E41C09B4122C41D2941F40F8EBAB8781E41FA0245E35B1D2941DC5368091B781E417AB82A82151D2941	2024-12-09 15:07:48.102
278	\N	\N	\N	TN33847H	\N	\N	\N	0103000020067400000100000009000000E8447C81A1741E41046A48A4F31C2941BE9A45DF04741E419435EC6D411D294188AACA966C741E41FE9AE3FC811D2941CE13E8C7CA741E4172DD0F3FCF1D2941D400A2323F751E416675AE58F51D2941FACDFAA759751E41BE0614FFEE1D294176A0DE838B761E41A8CB77B6581D2941F6E779B011751E41A6FA4F25AB1C2941E8447C81A1741E41046A48A4F31C2941	2024-12-09 15:07:48.102
279	\N	\N	\N	TN15728H	\N	\N	\N	0103000020067400000100000036000000E4A5F0C1E3801E41CEFD32176D1929413ECDBB03E1801E41F62F0D827F19294146581918F8801E41D6E7AE27AA192941F64758971B811E41A02C8D7DFA1929413A1DF1C131811E41CEDC96A0321A29415897C45038811E41F8691C3B511A2941CEA414563E811E417255E7536D1A2941689A18D239811E41EE9A776E8B1A29410A9E6C533B811E41CCBA2E1BBE1A2941C29728D140811E41A067B11CE81A2941E6E56AAE39811E416E7A1DA4001B2941A0DF624D44811E41FED37CB1FC1A29419640F30B0B821E41627749B10B1B294162C375964C821E41A6E34109031B29413C2E0FA5BC821E416814763CF41A29411621DBC202831E41B479D43EDB1A2941E0BE99B30A841E4164B6D72DCE1A2941CC24843EE0841E41D6468F9BC31A2941F6C98228CF851E4104B8BC59AC1A29415E51DC8E8F861E41D4591E4B861A2941F6ECA9D0F0861E41FE9227C0691A29412AA999A226871E4148C333BC631A294124487E875A871E4188DA1061751A294114A3523EC4871E41FE886D52991A2941204005AC03881E41F4008B26961A29419AAF4D3E0E881E415A8A527E771A294170304054FD871E413A96F117261A29414E4005AC03881E4170A79B9B0A1A29417E5EAA2F32881E41DEA190B1D4192941C4012D6641881E41C27E771D9719294120820D95F5871E41B057D6AE9A1929416ADB4C55AD871E41C4F356E85A1929418255CA629C871E41E2078CCF3E1929415EDB4C55AD871E41523861C12E19294128AB7763BD871E41EC02EE8C1319294116589BC4CA871E41A447F865E71829417ABF4324C8871E418A34F504A818294186A0B974BB871E41B80F606B65182941FE0DEF279A871E41B4E5ED9A3A18294188EE64788D871E41B2A6D93B211829417CEE64788D871E41608C2CC3FC172941D25B9A2B6C871E41725DDDBBE9172941D4B42D505C871E41926251CCF81729414437334577871E41E804784A47182941BA56BDF483871E41F2E51B4E88182941F846F89C7D871E417EE16CCAED1829413EDE716D39871E4100DD54207A192941D0E8598E57871E41BA40FE18D6192941D8B74B121D841E417C353438C819294136FFE32956831E4104F1295FF419294194FBCB232D821E41D06173E9EF1929410CDCDB32A7811E410A66F6F0AC192941541E3C492E811E416651E90475192941E4A5F0C1E3801E41CEFD32176D192941	2024-12-09 15:07:48.102
280	\N	\N	\N	TN296H	\N	\N	\N	010300002006740000010000001100000088FF52F9447E1E41728CC191C21D29419E780E7E977C1E41424C1764AB1D29416CC0B9AD567A1E4110BA5CC0781D294122C6DC23EA781E4190729EE4FB1E2941004C5E7F54781E41B2448732FF222941D850DF1227781E416EA65A4814242941969E10FA55781E41A2C0733416242941EC0500459F781E4118C66572C9232941E480389611791E412AF792D783232941F4EDADA1AF791E41BE74C4654B2329417CB251CFAA7A1E41082FB78A112329413C6C7868917B1E413824316DDC222941105786261C7C1E41902B1178BC222941D08D18EC337D1E415A8ECC2CB022294180227FE6E27D1E4188CE4EA1D2212941D0655F3F2D7E1E41F297B94E791F294188FF52F9447E1E41728CC191C21D2941	2024-12-09 15:07:48.102
281	\N	\N	\N	TN34714H	\N	\N	\N	010300002006740000010000000C000000002B5C503D611E41A03890CEF5142941402F27C50C611E4120F41435B114294100193575C6601E418015579AC7142941C00BC09C6D601E414015204F5D1429414018EBF80A601E4160ABBA3FDC132941407B780DDE5E1E41E0582CBF15142941806E1370E75E1E41407EBB062214294180A60E3F0E5F1E414039A08636142941C0B3F04B805F1E4160F7CB4DDF142941400A836E8A5F1E41605B634DEE142941009545DA40611E41202DC0CEFA142941002B5C503D611E41A03890CEF5142941	2024-12-09 15:07:48.102
282	\N	\N	\N	TN37369H	\N	\N	\N	010300002006740000010000000D000000BE9445DA40611E41F22CC0CEFA142941F209836E8A5F1E416A5B634DEE142941724D8EF8935F1E4112DA49680A1529412277C75C965F1E41B64A43BB0C152941B844F21EA15F1E418466B44F0E15294142390B4D8F5F1E412C0D1DA62C152941AC1321CA05601E41EC33A2123C15294172980EA120601E41FAC7746A1F15294126B4B34133601E41207D015C24152941049CBDF346601E4118065ACE1115294152EE2C904E601E414E8D2FEC07152941F83A0A317B601E41123895400C152941BE9445DA40611E41F22CC0CEFA142941	2024-12-09 15:07:48.102
283	\N	\N	\N	TN38298H	\N	\N	\N	010300002006740000010000001100000080E3D2ED32601E41C094D6215C15294180D8244BFC5F1E4180A469E64B152941001421CA05601E41E033A2123C15294140390B4D8F5F1E41400D1DA62C152941C044F21EA15F1E41A066B44F0E1529414077C75C965F1E41E04A43BB0C152941804D8EF8935F1E4140DA49680A15294100B6A07C575F1E4160ADB26F0915294180ECD4F1355F1E4180ADF3F44615294180EF7305415F1E41A0A925D3481529418064E1FA025F1E41607C6CCCA4152941C0A4324C165F1E414087DE38AA15294100A6971D0D5F1E410018F265B2152941001DE04D475F1E41407838BCC2152941004B5A12295F1E41203298B4D015294100C67C5C5D5F1E410016BAFEEC15294180E3D2ED32601E41C094D6215C152941	2024-12-09 15:07:48.102
284	\N	\N	\N	TN38297H	\N	\N	\N	0103000020067400000100000007000000C621CFBD4C5E1E4146D3B8C3D4142941DC2B813D0B5D1E41EADA0592C81429417E7D7D4C1F5D1E41DC60803C0115294164BD84AB495D1E41CEA09332331529413E5C5BD13B5E1E41FA67D5D2711529411CE863F6525E1E411690DDF544152941C621CFBD4C5E1E4146D3B8C3D4142941	2024-12-09 15:07:48.102
285	\N	\N	\N	TN38299H	\N	\N	\N	0103000020067400000100000007000000004B5A12295F1E41203298B4D0152941000BCE007F5D1E41E05E6CB15215294100335B77105D1E41E025587704162941C0BBDCE3375D1E4180649A4C2B162941403E9A608F5D1E41001BDB8A701629414034EE16B65D1E41805D037086162941004B5A12295F1E41203298B4D0152941	2024-12-09 15:07:48.102
286	\N	\N	\N	TN41612H	\N	\N	\N	0103000020067400000100000005000000FC97F06462971E41FAF113EB411F2941D66A751546971E41E410EB740E1F29411210A51905971E41AEF3059C1A1F29416C8D406239971E41AC8C48A24C1F2941FC97F06462971E41FAF113EB411F2941	2024-12-09 15:07:48.118
287	\N	\N	\N	TN38321H	\N	\N	\N	01030000200674000001000000130000006292FF351D8A1E41E63CD012E31E2941D6EF6074F58B1E41F6591CC61D1F2941E8025332378C1E41647FDFECC11E2941BA523399158C1E41C096C31B771E294138064FA3CF8B1E4136A4FEED661E294136EA431FC58B1E4110977691221E294188124194298B1E41CE1F20DD191E29410E1349C8078B1E412C203489F21D2941CCE6DE632D8B1E41F236D074EA1D2941DE0CE254398B1E416EFEEFE3B01D29419A846FF1498B1E41381163959A1D29411AFB48B61C8B1E41B272E0DEB11D294100D66552A98A1E41FECAC877DC1D294108201A0B858A1E4192DF21D4E21D29414C0A225EFE891E419C39419C181E294104D4FAA3CD8A1E41CCCB3B5D151E2941727D339BE08A1E41A6A2312E791E2941343C2FEA678A1E4136526F7D701E29416292FF351D8A1E41E63CD012E31E2941	2024-12-09 15:07:48.118
288	\N	\N	\N	TN5994H	\N	\N	\N	0103000020067400000100000022000000BCC251C771431E41D664FF2A852E29416678EFD8AC441E416865ABF23C2E29413030BC5F2F461E41E22ED856BA2D29416ADBBB4181461E417647370B992D29418E20867E75441E41E6AC2306572C294104D06E32C2441E41BA1FC901262C294174D350E59D421E4108C81CC98F2A2941D415EA19F0411E4176B692603E2A29413E1980806A411E4108EEF74720292941F8CDBE79BD3F1E41C0A321DF4629294190051F7E1D3F1E414284371DBF292941FED03C0EDA3E1E416A810C11962A2941A8DA335B593F1E41622F766BE22A2941687A59733D401E4178D082F3D42A294146F6A1C64B401E4104032A9A112B2941CEF675DB633F1E41DCA7EC4B1F2B2941407138E2473F1E416684937CE42A2941921035AAC93E1E41BE3C6AF6972A294174E6449CBE3D1E412C607134BA2A2941CEAFF47E473D1E4178C8723D5A2B29419AB6BD43323E1E41CE66AD4D6C2B2941C439B775CE3D1E418AE3D4FCF22B2941F46FB6069D3C1E413A0C3286172D29417031E7AAB33C1E41D0B67F0E3E2D2941DA1035229A401E41FC454462AB2C2941FC1757B7E8421E41D84A1EC8632C2941246325CDEC421E4168486265862D2941FEC34B89DC3F1E410EE0F226892D29418A207ECD093F1E41A6A09380FC2D294118CD0E95ED3E1E4132B8ADF6742E29414EF470E9303F1E41DEB73018742E2941B0B357B780401E41F48689C26F2E2941A6B0849401421E41A8DE68B37A2E2941BCC251C771431E41D664FF2A852E2941	2024-12-09 15:07:48.118
289	\N	\N	\N	TN493H	2	\N	\N	010300002006740000010000000F000000FCFA17CDF6541E410ACB4822771D294192777C6C04551E410A45F95E1F1D2941A2D155030E551E4134946D3CD51C2941AE469C0D12551E41F451A45D8F1C2941A616927F12551E41F08ECFAA871C2941E80591F5AB541E414C50EFB3851C2941D299ED09A2541E411C15646DE71C2941C89A95F876541E417482D127431D29415E78F1F095531E41E823D66A3E1D294100CBB47F82531E41382A55165C1D2941CE7CBE6A5C531E41EC407C65581D294176F3CBC551531E419AD9628D8C1D29413E33E13060541E414C13A43D981D29417893C366E7541E411402F514A31D2941FCFA17CDF6541E410ACB4822771D2941	2024-12-09 15:07:48.118
290	\N	\N	\N	T1177H	1	\N	\N	010300002006740000010000001C0000000ABD2ADFE65A1E41C2066EBA7F1C2941806B77CB0D5A1E4148D7FD82C71C2941BEF4BD1191591E410C75A07F051D2941BE8566B1F8571E413CA01464641D2941C88773C409571E413A4D3AD3C51D29418C2857D396561E41068AC72D021E294186654E11F4561E412091997C401E294100945FAA64571E4128FE6A648C1E2941C4A4697B73571E4148BC48C18A1E294182A5A9C896571E4188D3A26B7B1E2941461E4F28F2571E41BE43000B491E294170159E5B0F581E41E848A295381E2941006257A751581E41EC3AE6D51F1E294106B61F1F88581E41EC163A45041E2941FEA9BB67BA581E414065383FEB1D2941FCF4A21923591E41A494EF48B91D29414815982059591E4140C529F8A51D29417A116A48A4591E418E13A8198F1D29417870D2E21A5A1E41849E59EE5F1D294102AB43E9845A1E4138EE82063A1D2941B6706410A65A1E4160F516E3251D2941C8612FC6FE5A1E41A272A663EE1C2941844065D31C5B1E41861475ECD71C2941C629A255195B1E415817BBEBCB1C29417C05FBBC055B1E414A439040BD1C2941F6F356EEEB5A1E41DE4E9824AC1C29413E76AA26E75A1E41E24C211AA61C29410ABD2ADFE65A1E41C2066EBA7F1C2941	2024-12-09 15:07:48.118
291	\N	\N	\N	T491H	2	\N	\N	010300002006740000010000004E000000C82F689B6A5F1E418E7EBF72F5192941760C8DDE7D5F1E4164AB5AB7231A2941C00083FC0D601E410A6D6EF4841A2941143A0EAD5D601E4158B95754C21A29418AE3D1C4B0601E41C8A33B16381B29413659142958611E415443A13A7D1B2941B8EBACA9EB621E4140D750FC0E1B294106FB74E9B6621E41EA4B0A8D8C1A29417C2B75FFFD621E41E03972C2061A29414802B98EBF631E416479CE3714192941FCE4240453631E41E0545FF5BB18294104B492C99C631E41C0C4ECB4851829417A9AE2D6DE631E4148DEB635A3182941BE65DCAFC5631E41080CCFE7BA182941F43992422B641E4138A06FA1E21829412E9492CD43641E41A01310D3D9182941087D679E6C641E4122A16149EE1829413A2A03A17A631E41A8C7615FC71A294120C7FAE98D631E417044E8F1C81A2941CA53C92CDD631E4186027527A11A2941D829491766641E4180DA3B597E1A2941F8C0A0DAD6641E413A068B858D1A29414C695B1632651E4146F5EEF37A1A29417E0FAF695A651E4120A6142E651A29413C087A799F651E414CC300894B1A2941EEF0252BCE651E416862C4E1491A29417E3C8BCBD6651E417E59EA7B441A294184EB1A1BB8651E41001C0F55291A2941FE0EB67AE1651E412AD78FE30D1A294132E726DC06661E41969C2EECEC192941F6FF317634661E4194B8A003BE1929413C515B4643661E41C809E83499192941DE87B19F95671E41E8DC4686ED18294140FF93F6C5671E41A61A10B03B182941F8AFCEE440681E41086275EBDB172941C42997C807671E41F6B3B6F3511729417C9BD1AA30671E417E73D4E832172941BC6FA9F75A671E413C466EC03F1729417870B793AB671E4184836E6032172941049254B9DF671E415401C2E86A172941FAD804C907681E41E079ACDC72172941F670F7F876681E4186571FA0B41729414C197AC68C681E417C798B778A1729413A737BE987681E4160A41B6C7B17294184D2702A2D681E41BC7EC6D81D172941C2FA1A236A681E41EEBB3A0FFD1629418CD4D897DF671E4112C1509F6B162941A0BB374957671E4188F0383920162941803833D692671E41887A5F2A8915294188D8FF983A651E414816A8E32A16294108CE9CF9C9631E415CCB53C01A15294196560A65AF621E4186F4C3774D1529410C4C8C6458621E410C79A0956615294104ED4A439B611E41D0B24BA2D1152941BA1F2C2F0D611E4124F2966F1D162941143818539A601E41CEB2C935501629411EFACDA946601E41028F86EC84162941C61CAF12C95F1E41E6E11460BB162941DC87431DE75E1E41FA08F5BB1D172941C0A1B3582D5D1E41FA71552ED0172941C8A11714C05C1E4144B05D290E1829413AC0C2347B5D1E411A32EB4409182941F4DF6C3E8B5D1E41E6594A2117182941429E97FA2E5E1E4196EA6E6B07182941C0A0C3798F5E1E418004B962BE172941C6BF3880EE5E1E410E880E28DE172941768ADE3BD95F1E416481BAF4A017294184F69CC79D601E41A4026E1BFE1629419204D8FFD9601E418096DF24EB1629418225CF8F4A611E418083957C041729412A5B4B7A7A611E41EEADEC0E29172941083838D370611E416C5889906C172941B0FB16D45B5F1E414EE1DA2624182941B40ABD28685E1E419C2B18C1AF182941028D4A3B975E1E41626EEE0F3C192941B87B0CFC055F1E41CCF9F3D97D192941441B3103575F1E4142DF1339BF192941C82F689B6A5F1E418E7EBF72F5192941	2024-12-09 15:07:48.118
292	\N	\N	\N	T491H	1	\N	\N	010300002006740000010000001D00000020BD2ADFE65A1E41BE066EBA7F1C294184AF502C355C1E41C48D482E111C2941128CB9F7595E1E412497AE670A1C2941BE9258F91A5F1E41E059B6A1CB1B294108BBA53F97601E410452C7ACAF1B2941E2CD46FCB15F1E41CC1E79C5F61A29415E99E848685F1E41980D005DAC1A2941320FB396115F1E413036F3B05C1A2941088063D7F05E1E410E60D9983E1A29418257683CD25E1E417658CFC11E1A2941AE5730A80B5E1E41D03ED9A74D192941327DC2A2125E1E41B061B1CC2E192941726A76B9845D1E4178A7759EE2182941D6F81BA3AD5C1E412CEEC6827D182941FCCFA16F9A5C1E419A77FD81671829418C23D815815C1E4120BE27754A1829417A0C4168AE5B1E41DCA853FC9218294158FD871036581E415621C89CD019294156F1EAA2AC571E414E726489021A29411824BAB368541E41CC374B88CC1929410A0FDA9486541E412A706CC6161A2941E09A803EE0541E41D61D68AAA31A29416CE85363FB541E4154973D74E11A29415EC4D81600551E41DA307EE63D1B2941D466A1B212551E41347E59EE741B2941C870A7853A551E41C6AA3F25C11B29412E05D6B449581E41106CC4B7E21B2941986B77CB0D5A1E4148D7FD82C71C294120BD2ADFE65A1E41BE066EBA7F1C2941	2024-12-09 15:07:48.118
293	\N	\N	\N	T868H	7	\N	\N	0103000020067400000100000006000000143A0EAD5D601E4158B95754C21A2941C00083FC0D601E410A6D6EF4841A294190568F28C35F1E4130B940C0961A29418A99E848685F1E416C0D005DAC1A2941CACD46FCB15F1E41CC1E79C5F61A2941143A0EAD5D601E4158B95754C21A2941	2024-12-09 15:07:48.133
294	\N	\N	\N	T1177H	2	\N	\N	0103000020067400000100000009000000C00083FC0D601E410A6D6EF4841A2941760C8DDE7D5F1E4164AB5AB7231A2941C82F689B6A5F1E418E7EBF72F51929412857683CD25E1E418458CFC11E1A2941867F63D7F05E1E41F45FD9983E1A29410C0FB396115F1E413236F3B05C1A29418A99E848685F1E416C0D005DAC1A294190568F28C35F1E4130B940C0961A2941C00083FC0D601E410A6D6EF4841A2941	2024-12-09 15:07:48.133
295	\N	\N	\N	T491H	4	\N	\N	010300002006740000010000001400000000E3FBD7EF611E410487A18D301529413025120FF2611E419C52240F31152941B217679049621E41229C125F03152941042B5C503D611E41A43890CEF5142941F69445DA40611E41202DC0CEFA142941F63A0A317B601E41343895400C15294196EE2C904E601E41328D2FEC07152941349CBDF346601E414E065ACE1115294144B4B34133601E413A7D015C24152941B6980EA120601E4126C8746A1F152941FE1321CA05601E41D433A2123C1529417ED8244BFC5F1E4180A469E64B15294186E3D2ED32601E41BE94D6215C15294138E6F1AE8E601E413A52A1E76C152941F62BD9BFCC601E41D29BA10518152941887A340E2B611E415CBBFAAE12152941D42EED3C77611E41CC6F2EE111152941C0B2E40499611E417EBD5202181529417ECBDE08C0611E4186DB9A161F15294100E3FBD7EF611E410487A18D30152941	2024-12-09 15:07:48.133
296	\N	\N	\N	T491H	4	\N	\N	010300002006740000010000001F000000B646159FE15F1E41FEECD6F64416294194BAEAF4D45F1E416675D9273B162941FCC57C5C5D5F1E410416BAFEEC1529411C4B5A12295F1E41203298B4D01529413A34EE16B65D1E41885D037086162941363E9A608F5D1E410A1BDB8A70162941C4BBDCE3375D1E41A0649A4C2B16294100335B77105D1E41E425587704162941FE0ACE007F5D1E41E05E6CB1521529411C4B5A12295F1E41203298B4D0152941081DE04D475F1E413C7838BCC2152941F8A5971D0D5F1E41EE17F265B2152941C2A4324C165F1E414C87DE38AA1529417E64E1FA025F1E41647C6CCCA41529418CEF7305415F1E419EA925D34815294180ECD4F1355F1E417EADF3F446152941FCB5A07C575F1E415CADB26F09152941844D8EF8935F1E413EDA49680A152941400A836E8A5F1E41725B634DEE142941C6B3F04B805F1E417CF7CB4DDF1429418026B0CA4B5E1E416C3830B4CF142941E821CFBD4C5E1E4166D3B8C3D4142941F0E763F6525E1E414490DDF5441529413A5C5BD13B5E1E41F267D5D271152941BEBD84AB495D1E41BEA09332331529417E7D7D4C1F5D1E41FE60803C01152941022C813D0B5D1E41FCDA0592C8142941B03F056D0B5D1E41E0F30981BF142941F04F3024AB5A1E414A71C5BEA0142941885ACF5B5D5C1E4192CA3C011B182941B646159FE15F1E41FEECD6F644162941	2024-12-09 15:07:48.133
297	\N	\N	\N	T491H	3	\N	\N	01030000200674000001000000090000002C3833D692671E41587A5F2A891529410C0374F0B8681E411C05661137152941A84424AC67661E41C2532DB508132941D222AC4FA8651E41BE4C1D4306132941089D0B363D641E412E042969A7132941980AC0E1A2641E41D057AA119514294100B96407CB651E414469E1B2DB1329411A724F41D1671E41D8BE31B9091529412C3833D692671E41587A5F2A89152941	2024-12-09 15:07:48.133
298	\N	\N	\N	T493H	7	\N	\N	01030000200674000001000000080000008C2A984F83581E41507159DCFB1629414C04A2F0B3581E41220A7660E316294132E53A6290581E41D6C12C6DD3162941067CD6AB7D581E41D85E25BACD162941548A90DE4A581E41D8E0645FC7162941069216E41C581E41042A9707C616294110E73519F7571E41FA75F073C91629418C2A984F83581E41507159DCFB162941	2024-12-09 15:07:48.133
299	\N	\N	\N	T868H	1	\N	\N	010300002006740000010000000900000050AAA0E3CE591E4184A5FE1E961E29410E4B79A6345A1E41F676E825631E2941DAFD706557591E4180A3CC1AC31D29417296E6E641591E411C7EBE30CC1D294128C15A4531591E41145D7806D11D2941E2C700630D591E41FAFA34A9D61D2941A2DC5F3FEE581E41A62F1336DE1D2941287711F4D5581E41C4988265E51D294150AAA0E3CE591E4184A5FE1E961E2941	2024-12-09 15:07:48.133
300	\N	\N	\N	T868H	2	\N	\N	0103000020067400000100000010000000521E942C465C1E413C650B07C41C2941A8C40A31FB5B1E4152C5D2323A1C29416A0AD1C7DC5B1E410063592C421C2941AAFADD1DAD5B1E4168D43845501C294168054B102F5B1E41CA6DCC1D771C29418274742AF25A1E4176E91F5E891C294122A5728AEC5A1E41061F76E8931C2941621AABAEEC5A1E412A5419839A1C2941E23E7D71F85A1E41ECEE1EDEA41C2941209B9A7E115B1E416CB64219B51C2941188FD6302A5B1E41CC344CCBCB1C2941EA0A827C375B1E418EE64CFFDA1C2941909F6462785B1E4176580697D31C29419037FA1BBF5B1E416AF76DD6CB1C2941DE51578FE45B1E41A61A000BD51C2941521E942C465C1E413C650B07C41C2941	2024-12-09 15:07:48.133
301	\N	\N	\N	T868H	3	\N	\N	01030000200674000001000000090000005E78B898255F1E416E278480051D2941082DDB988F5F1E415C0EDE12271D294184633612C55F1E41203C35AC361D29410A019DE309601E419461C5B5101D2941241CD5C19E5F1E41B2E982DD731C2941AA18310D545F1E413C5F52B82D1C2941247F2A64135F1E413401866E451C2941B47ED5C94B5F1E4174886B08D01C29415E78B898255F1E416E278480051D2941	2024-12-09 15:07:48.133
302	\N	\N	\N	T868H	4	\N	\N	010300002006740000010000000D000000C8C9821648611E4190C9094C171D2941089C6CE0B5611E41CC849E0A091D2941E45AC2DE11611E414ECD89CC5F1C2941F2829488FD601E4130EC8BA7431C2941AE9465164F611E4144402E27381C2941BC4EECA404611E41587F3B38D31B29416A62A92364601E419639D26AD11B2941341422277C601E41FAB56BF4161C294118A73C3F39601E41C409F616191C2941AC1A7BFECF5F1E4184938E9D2D1C294192D96B2B27601E41567C685EA01C2941103A804CE3601E412AE3810C921C2941C8C9821648611E4190C9094C171D2941	2024-12-09 15:07:48.149
303	\N	\N	\N	T868H	5	\N	\N	010300002006740000010000000A00000050B30F29B8621E4122389592EC1C29414E8ABBFCBB631E4110151EEDAA1C294120A7914FD7631E41ACEA4A06901C29416249470E7B631E410662CB5F551C2941E4497B1316631E41FAB693F9761C29412C63A1AFA8621E41CEFD85F5131C29412CA11B8037621E416E04C7152D1C2941DA06B67C50621E4134D3D84E491C2941628AA41815621E410AAF743B571C294150B30F29B8621E4122389592EC1C2941	2024-12-09 15:07:48.151
304	\N	\N	\N	T868H	6	\N	\N	01030000200674000001000000120000007CB171ABEC621E415C11657D8F1B29411286656AD1621E4182857876651B2941C8BCAD7DAA621E419E3C14884B1B29410461C4CF9C621E415AA4E7F2511B29418EA976F389621E414A5B0A8D551B294110A4D38558621E41C4C798A15A1B294158CDCB0526621E41789ACA2E631B29419056EDA2F2611E41748D1C586D1B2941849CBFF9BA611E413040984A721B29410C3AB9098C611E41A272E2B67A1B2941D074C49869611E4110AF44CE821B29410E7D005F41611E41D05D1EDE8E1B2941124AD14015611E41D25E7E5DA01B294140BE7A3A39611E412E6056FDAE1B2941FE4CA12251611E41DCACBD83B21B29413476E51B59611E41EE69D320CC1B294106F9EC7237621E4186083187B31B29417CB171ABEC621E415C11657D8F1B2941	2024-12-09 15:07:48.151
\.


--
-- TOC entry 5297 (class 0 OID 0)
-- Dependencies: 344
-- Name: titre arivonimamo i eugenie_gid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"titre arivonimamo i eugenie_gid_seq"', 333, true);


--
-- TOC entry 5298 (class 0 OID 0)
-- Dependencies: 345
-- Name: titre_gid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('titre_gid_seq', 304, true);


--
-- TOC entry 5126 (class 0 OID 1516747)
-- Dependencies: 346
-- Data for Name: titrefoncier; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY titrefoncier (numerotitre, datetitre, contenance, cheminplanindividuel, originecontour, typetitre, acteurpublic, nompropriete, consistance, shape_length, shape_area, geom, gid, observation, datemaj) FROM stdin;
\.


--
-- TOC entry 5299 (class 0 OID 0)
-- Dependencies: 347
-- Name: titrefoncier_gid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('titrefoncier_gid_seq', 12, true);


--
-- TOC entry 5128 (class 0 OID 1516755)
-- Dependencies: 348
-- Data for Name: type_anomalie; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY type_anomalie (id_type_anomalie, valeur, csv_id, datemaj) FROM stdin;
\.


--
-- TOC entry 5300 (class 0 OID 0)
-- Dependencies: 349
-- Name: type_anomalie_id_type_anomalie_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('type_anomalie_id_type_anomalie_seq', 1, false);


--
-- TOC entry 5130 (class 0 OID 1516760)
-- Dependencies: 350
-- Data for Name: type_document; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY type_document (id_type, libelle_type, datemaj) FROM stdin;
\.


--
-- TOC entry 5301 (class 0 OID 0)
-- Dependencies: 351
-- Name: type_document_id_type_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('type_document_id_type_seq', 1, false);


--
-- TOC entry 5132 (class 0 OID 1516765)
-- Dependencies: 352
-- Data for Name: typeforfaitaire; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY typeforfaitaire (idforfaitaire, libelleforfaitaire, datemaj) FROM stdin;
\.


--
-- TOC entry 5302 (class 0 OID 0)
-- Dependencies: 353
-- Name: typeforfaitaire_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('typeforfaitaire_id_seq', 1, false);


--
-- TOC entry 5135 (class 0 OID 1516772)
-- Dependencies: 355
-- Data for Name: typeoperationsubsequente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY typeoperationsubsequente (idtype, libelleoperation, datemaj) FROM stdin;
1	Mutation par décès	2024-11-14 14:30:40.86
2	Vente total	2024-11-14 14:30:40.86
3	Vente partielle avec distraction de parcelle	2024-11-14 14:30:40.86
4	Vente partielle en restant dans l'indivision	2024-11-14 14:30:40.86
5	Donation total d'un certificat	2024-11-14 14:30:40.86
6	Donation partielle avec distraction 	2024-11-14 14:30:40.86
7	Donation partielle en restant dans l'indivision	2024-11-14 14:30:40.86
8	Echange total de deux certificats	2024-11-14 14:30:40.86
9	Fusion des certificats	2024-11-14 14:30:40.86
\.


--
-- TOC entry 5303 (class 0 OID 0)
-- Dependencies: 354
-- Name: typeoperationsubsequente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('typeoperationsubsequente_id_seq', 11, true);


--
-- TOC entry 5136 (class 0 OID 1516776)
-- Dependencies: 356
-- Data for Name: typepersonnemorale; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY typepersonnemorale (idtype, type, karazana, csv_id, datemaj) FROM stdin;
1	Société	Orinasa	\N	2024-11-14 14:30:40.86
2	ONG	ONG	\N	2024-11-14 14:30:40.86
3	Association	Fikambanana	\N	2024-11-14 14:30:40.86
\.


--
-- TOC entry 5304 (class 0 OID 0)
-- Dependencies: 357
-- Name: typepersonnemorale_idtype_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('typepersonnemorale_idtype_seq', 3, true);


--
-- TOC entry 5139 (class 0 OID 1516783)
-- Dependencies: 359
-- Data for Name: utilisateur; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY utilisateur (idutilisateur, nomutilisateur, prenomutilisateur, loginutilisateur, passwordutilisateur, typeutilisateur, telephone, adresse, fonction, loginufiplof, passwdfiplof, groupe_id, datemaj) FROM stdin;
8	Responsable	Commune	respcom	0308BD47138299D52D9A197C3D2178DD	\N	034			\N	\N	5	2024-11-14 14:30:40.86
10	Assistant	Technique	ats	34EE78AE5EDC56DC1DC00BB844C5D62A	\N	034			\N	\N	11	2024-11-14 14:30:40.86
11	Formateur		formation	06048D2F2D2CA345A721B4FD25B91A92	\N	034			\N	\N	12	2024-11-14 14:30:40.86
12	Agent	Topo	topo	1D6EA1F692424E806963838CF9E37E37	\N	034			\N	\N	13	2024-11-14 14:30:40.86
13	Disposition	Transitoire	dt	13D94D956F809706C5245ABD927A0E15	\N	034			\N	\N	14	2024-11-14 14:30:40.86
14	Agent	Guichet Foncier	agf	A3856373041BB18DD4A9943A55B4D654	\N	034			\N	\N	10	2024-11-14 14:30:40.86
1	Administrateur	Fiplof	admin	EC40092C49C76E8EA3A8AA7F7FA9B0EB	\N	034			maire	maire	1	2024-11-14 14:30:40.86
\.


--
-- TOC entry 5305 (class 0 OID 0)
-- Dependencies: 358
-- Name: utilisateur_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('utilisateur_id_seq', 15, true);


--
-- TOC entry 5141 (class 0 OID 1516792)
-- Dependencies: 361
-- Data for Name: voisinparcelle; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY voisinparcelle (idvp, idvoisin, idpacelle, iddemande, datemaj) FROM stdin;
\.


--
-- TOC entry 5306 (class 0 OID 0)
-- Dependencies: 360
-- Name: voisinparcelle_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('voisinparcelle_id_seq', 11, true);


--
-- TOC entry 5143 (class 0 OID 1516798)
-- Dependencies: 363
-- Data for Name: voisins; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY voisins (idvoisin, nom, prenom, adresse, datemaj) FROM stdin;
10	V01	\N	Adresse	2024-11-14 14:30:40.86
11	V02	\N	Adresse 2	2024-11-14 14:30:40.86
\.


--
-- TOC entry 5307 (class 0 OID 0)
-- Dependencies: 362
-- Name: voisins_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('voisins_id_seq', 11, true);


--
-- TOC entry 5145 (class 0 OID 1516847)
-- Dependencies: 374
-- Data for Name: z_certifiable; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY z_certifiable (gid, id, crtfbl, geom, datemaj) FROM stdin;
\.


--
-- TOC entry 5308 (class 0 OID 0)
-- Dependencies: 373
-- Name: z_certifiable_gid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('z_certifiable_gid_seq', 1, false);


SET search_path = topology, pg_catalog;

--
-- TOC entry 4047 (class 0 OID 1515990)
-- Dependencies: 195
-- Data for Name: layer; Type: TABLE DATA; Schema: topology; Owner: postgres
--

COPY layer (topology_id, layer_id, schema_name, table_name, feature_column, feature_type, level, child_id) FROM stdin;
\.


--
-- TOC entry 4046 (class 0 OID 1515977)
-- Dependencies: 194
-- Data for Name: topology; Type: TABLE DATA; Schema: topology; Owner: postgres
--

COPY topology (id, name, srid, "precision", hasz) FROM stdin;
\.


SET search_path = public, pg_catalog;

--
-- TOC entry 4261 (class 2606 OID 1516938)
-- Name: acces_nom_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY acces
    ADD CONSTRAINT acces_nom_key UNIQUE (nom);


--
-- TOC entry 4263 (class 2606 OID 1516940)
-- Name: acces_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY acces
    ADD CONSTRAINT acces_pkey PRIMARY KEY (id);


--
-- TOC entry 4576 (class 2606 OID 1529600)
-- Name: date_synchro_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY date_synchro
    ADD CONSTRAINT date_synchro_pkey PRIMARY KEY (id_synchro);


--
-- TOC entry 4383 (class 2606 OID 1516944)
-- Name: demande_crl_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY demande_crl
    ADD CONSTRAINT demande_crl_pkey PRIMARY KEY (idpersonne, iddemande, id_role);


--
-- TOC entry 4369 (class 2606 OID 1516946)
-- Name: demande_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY demande
    ADD CONSTRAINT demande_pkey PRIMARY KEY (iddemande);


--
-- TOC entry 4385 (class 2606 OID 1516948)
-- Name: demande_sans_geom_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY demande_sans_geom
    ADD CONSTRAINT demande_sans_geom_pkey PRIMARY KEY (iddemande);


--
-- TOC entry 4397 (class 2606 OID 1516952)
-- Name: document_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY document
    ADD CONSTRAINT document_pkey PRIMARY KEY (id_document);


--
-- TOC entry 4410 (class 2606 OID 1516954)
-- Name: groupe_acces_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY groupe_acces
    ADD CONSTRAINT groupe_acces_pkey PRIMARY KEY (id);


--
-- TOC entry 4408 (class 2606 OID 1516956)
-- Name: groupe_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY groupe
    ADD CONSTRAINT groupe_pkey PRIMARY KEY (id);


--
-- TOC entry 4437 (class 2606 OID 1516958)
-- Name: impot_minimum_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY impot_minimum
    ADD CONSTRAINT impot_minimum_pkey PRIMARY KEY (id_impotminimum);


--
-- TOC entry 4456 (class 2606 OID 1516960)
-- Name: operationsub_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY operationsub
    ADD CONSTRAINT operationsub_pkey PRIMARY KEY (id);


--
-- TOC entry 4464 (class 2606 OID 1516962)
-- Name: param_layer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY param_layer
    ADD CONSTRAINT param_layer_pkey PRIMARY KEY (id);


--
-- TOC entry 4474 (class 2606 OID 1516964)
-- Name: parcelle_d_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY parcelle_d
    ADD CONSTRAINT parcelle_d_pkey PRIMARY KEY (gid);


--
-- TOC entry 4265 (class 2606 OID 1516966)
-- Name: pk_actedeces; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY actedeces
    ADD CONSTRAINT pk_actedeces PRIMARY KEY (idactedeces);


--
-- TOC entry 4269 (class 2606 OID 1516968)
-- Name: pk_actedecessubsequente; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY actedecessubsequente
    ADD CONSTRAINT pk_actedecessubsequente PRIMARY KEY (idactedeces, idoperationsubsequente);


--
-- TOC entry 4271 (class 2606 OID 1516970)
-- Name: pk_actedejalance; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY actedejalance
    ADD CONSTRAINT pk_actedejalance PRIMARY KEY (id);


--
-- TOC entry 4273 (class 2606 OID 1516972)
-- Name: pk_acteprive; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY acteprive
    ADD CONSTRAINT pk_acteprive PRIMARY KEY (idacteprive);


--
-- TOC entry 4277 (class 2606 OID 1516974)
-- Name: pk_acteprivesubsequente; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY acteprivesubsequente
    ADD CONSTRAINT pk_acteprivesubsequente PRIMARY KEY (idacteprive, idoperationsubsequente);


--
-- TOC entry 4279 (class 2606 OID 1516976)
-- Name: pk_actepublic; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY actepublic
    ADD CONSTRAINT pk_actepublic PRIMARY KEY (idactepublic);


--
-- TOC entry 4283 (class 2606 OID 1516978)
-- Name: pk_actepublicsubsequente; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY actepublicsubsequente
    ADD CONSTRAINT pk_actepublicsubsequente PRIMARY KEY (idactepublic, idoperationsubsequente);


--
-- TOC entry 4285 (class 2606 OID 1516980)
-- Name: pk_aire; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY aireastatutspecifique
    ADD CONSTRAINT pk_aire PRIMARY KEY (idaireastatutspecifique);


--
-- TOC entry 4288 (class 2606 OID 1516982)
-- Name: pk_anomalie; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY anomalie
    ADD CONSTRAINT pk_anomalie PRIMARY KEY (idanomalie);


--
-- TOC entry 4292 (class 2606 OID 1516984)
-- Name: pk_autrecharge; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY autrecharge
    ADD CONSTRAINT pk_autrecharge PRIMARY KEY (idcharge);


--
-- TOC entry 4294 (class 2606 OID 1516986)
-- Name: pk_autrechargeparcelle_d; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY autrechargesparcelle_d
    ADD CONSTRAINT pk_autrechargeparcelle_d PRIMARY KEY (idcharge, idparcelle);


--
-- TOC entry 4296 (class 2606 OID 1516988)
-- Name: pk_avoir_demande; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY avoir_demande
    ADD CONSTRAINT pk_avoir_demande PRIMARY KEY (idpersonne, idparcelle);


--
-- TOC entry 4302 (class 2606 OID 1516990)
-- Name: pk_avoir_dmd; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY avoir_dmd
    ADD CONSTRAINT pk_avoir_dmd PRIMARY KEY (iddemande, iddemandeur);


--
-- TOC entry 4304 (class 2606 OID 1516992)
-- Name: pk_avoirconjoint; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY avoirconjoint
    ADD CONSTRAINT pk_avoirconjoint PRIMARY KEY (idconjoint_a, idconjoint_b);


--
-- TOC entry 4313 (class 2606 OID 1516994)
-- Name: pk_batiment; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY batiment
    ADD CONSTRAINT pk_batiment PRIMARY KEY (codebatiment);


--
-- TOC entry 4315 (class 2606 OID 1516996)
-- Name: pk_beneficiaire; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY beneficiaire
    ADD CONSTRAINT pk_beneficiaire PRIMARY KEY (idbeneficiaire);


--
-- TOC entry 4317 (class 2606 OID 1516998)
-- Name: pk_blob_personne; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY blob_personne
    ADD CONSTRAINT pk_blob_personne PRIMARY KEY (idblob);


--
-- TOC entry 4321 (class 2606 OID 1517000)
-- Name: pk_blob_voisin; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY blob_voisin
    ADD CONSTRAINT pk_blob_voisin PRIMARY KEY (idpoint, idparcelle, voisin);


--
-- TOC entry 4323 (class 2606 OID 1517002)
-- Name: pk_cadastre; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY cadastre
    ADD CONSTRAINT pk_cadastre PRIMARY KEY (gid);


--
-- TOC entry 4450 (class 2606 OID 1517004)
-- Name: pk_cardinal_parcelle; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY limitesparcelle
    ADD CONSTRAINT pk_cardinal_parcelle PRIMARY KEY (idpointscardinaux, idparcelle);


--
-- TOC entry 4325 (class 2606 OID 1517006)
-- Name: pk_categorie; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY categorie
    ADD CONSTRAINT pk_categorie PRIMARY KEY (idcategorie);


--
-- TOC entry 4329 (class 2606 OID 1517008)
-- Name: pk_categorieforfaitaire; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY categorieforfaitaire
    ADD CONSTRAINT pk_categorieforfaitaire PRIMARY KEY (idcategorie, idforfaitaire);


--
-- TOC entry 4332 (class 2606 OID 1517010)
-- Name: pk_certificat; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY certificat
    ADD CONSTRAINT pk_certificat PRIMARY KEY (idcertificat);


--
-- TOC entry 4336 (class 2606 OID 1517012)
-- Name: pk_classe; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY classe
    ADD CONSTRAINT pk_classe PRIMARY KEY (idclasse);


--
-- TOC entry 4340 (class 2606 OID 1517014)
-- Name: pk_classecategorieforfaitaire; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY classecategorieforfaitaire
    ADD CONSTRAINT pk_classecategorieforfaitaire PRIMARY KEY (idcategorie, idclasse);


--
-- TOC entry 4343 (class 2606 OID 1517016)
-- Name: pk_commune; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY commune
    ADD CONSTRAINT pk_commune PRIMARY KEY (idcommune);


--
-- TOC entry 4578 (class 2606 OID 2120354)
-- Name: pk_configuration; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY configuration
    ADD CONSTRAINT pk_configuration PRIMARY KEY (id_configuration);


--
-- TOC entry 4347 (class 2606 OID 1517018)
-- Name: pk_consistance; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY consistance
    ADD CONSTRAINT pk_consistance PRIMARY KEY (idconsistance);


--
-- TOC entry 4349 (class 2606 OID 1517020)
-- Name: pk_consistanceBat; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY consistance_batiment
    ADD CONSTRAINT "pk_consistanceBat" PRIMARY KEY (id);


--
-- TOC entry 4353 (class 2606 OID 1517022)
-- Name: pk_consistanceforfaitaire; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY consistanceforfaitaire
    ADD CONSTRAINT pk_consistanceforfaitaire PRIMARY KEY (idconsistance, idforfaitaire);


--
-- TOC entry 4363 (class 2606 OID 1517024)
-- Name: pk_contr_parcelle; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY contribuables_parcelle
    ADD CONSTRAINT pk_contr_parcelle PRIMARY KEY (idpersonne, idparcelle);


--
-- TOC entry 4356 (class 2606 OID 1517026)
-- Name: pk_contribuable; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY contribuable
    ADD CONSTRAINT pk_contribuable PRIMARY KEY (idcontribuable);


--
-- TOC entry 4361 (class 2606 OID 1517028)
-- Name: pk_contribuableconsorts; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY contribuableconsorts
    ADD CONSTRAINT pk_contribuableconsorts PRIMARY KEY (idcontribuable, idconsort);


--
-- TOC entry 4367 (class 2606 OID 1517032)
-- Name: pk_decisionsubsequente; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY decisionsubsequente
    ADD CONSTRAINT pk_decisionsubsequente PRIMARY KEY (idoperationsubsequente, iddecision);


--
-- TOC entry 4381 (class 2606 OID 1517034)
-- Name: pk_demande_anomalie; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY demande_anomalie
    ADD CONSTRAINT pk_demande_anomalie PRIMARY KEY (iddemande, idanomalie);


--
-- TOC entry 4389 (class 2606 OID 1517038)
-- Name: pk_demandefn; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY demandefn
    ADD CONSTRAINT pk_demandefn PRIMARY KEY (gid);


--
-- TOC entry 4393 (class 2606 OID 1517040)
-- Name: pk_district; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY district
    ADD CONSTRAINT pk_district PRIMARY KEY (iddistrict);


--
-- TOC entry 4402 (class 2606 OID 1517044)
-- Name: pk_fokontany; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY fokontany
    ADD CONSTRAINT pk_fokontany PRIMARY KEY (idfokontany);


--
-- TOC entry 4413 (class 2606 OID 1517046)
-- Name: pk_hameau; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY hameau
    ADD CONSTRAINT pk_hameau PRIMARY KEY (idhameau);


--
-- TOC entry 4419 (class 2606 OID 1517048)
-- Name: pk_historique; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY historique
    ADD CONSTRAINT pk_historique PRIMARY KEY (idhistorique);


--
-- TOC entry 4421 (class 2606 OID 1517050)
-- Name: pk_hypotheque; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY hypotheque
    ADD CONSTRAINT pk_hypotheque PRIMARY KEY (idhypotheque);


--
-- TOC entry 4423 (class 2606 OID 1517052)
-- Name: pk_hypothequeparcelle_d; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY hypothequeparcelle_d
    ADD CONSTRAINT pk_hypothequeparcelle_d PRIMARY KEY (idhypotheque, idparcelle);


--
-- TOC entry 4425 (class 2606 OID 1517054)
-- Name: pk_impot; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY impot
    ADD CONSTRAINT pk_impot PRIMARY KEY (idimpot);


--
-- TOC entry 4428 (class 2606 OID 1517056)
-- Name: pk_impot_batiment; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY impot_batiment
    ADD CONSTRAINT pk_impot_batiment PRIMARY KEY (id);


--
-- TOC entry 4433 (class 2606 OID 1517058)
-- Name: pk_impot_contribuable; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY impot_contribuable
    ADD CONSTRAINT pk_impot_contribuable PRIMARY KEY (id);


--
-- TOC entry 4440 (class 2606 OID 1517060)
-- Name: pk_impot_percelle; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY impot_parcelle
    ADD CONSTRAINT pk_impot_percelle PRIMARY KEY (id);


--
-- TOC entry 4446 (class 2606 OID 1517062)
-- Name: pk_impotparcelle; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY impotparcelle
    ADD CONSTRAINT pk_impotparcelle PRIMARY KEY (idparcelle, idimpot);


--
-- TOC entry 4448 (class 2606 OID 1517064)
-- Name: pk_journal; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY journal
    ADD CONSTRAINT pk_journal PRIMARY KEY (id);


--
-- TOC entry 4452 (class 2606 OID 1517068)
-- Name: pk_menage; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY menage
    ADD CONSTRAINT pk_menage PRIMARY KEY (id_menage);


--
-- TOC entry 4459 (class 2606 OID 1517074)
-- Name: pk_operationsubsequente; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY operationsubsequente
    ADD CONSTRAINT pk_operationsubsequente PRIMARY KEY (idoperationsubsequente);


--
-- TOC entry 4462 (class 2606 OID 1517076)
-- Name: pk_oppositions; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY oppositions
    ADD CONSTRAINT pk_oppositions PRIMARY KEY (idopposition);


--
-- TOC entry 4399 (class 2606 OID 1517078)
-- Name: pk_paiement_impot; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY fi_paiement_impot
    ADD CONSTRAINT pk_paiement_impot PRIMARY KEY (id_paiement);


--
-- TOC entry 4482 (class 2606 OID 1517086)
-- Name: pk_parcellegrevees; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY parcellegrevees
    ADD CONSTRAINT pk_parcellegrevees PRIMARY KEY (idparcellegrevees);


--
-- TOC entry 4484 (class 2606 OID 1517088)
-- Name: pk_path; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY path_personne
    ADD CONSTRAINT pk_path PRIMARY KEY (idpersonne);


--
-- TOC entry 4496 (class 2606 OID 1517092)
-- Name: pk_persmorale; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY personnemorale
    ADD CONSTRAINT pk_persmorale PRIMARY KEY (idpersonnemorale);


--
-- TOC entry 4486 (class 2606 OID 1517094)
-- Name: pk_personne; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY personne
    ADD CONSTRAINT pk_personne PRIMARY KEY (idpersonne);


--
-- TOC entry 4494 (class 2606 OID 1517096)
-- Name: pk_personne_menage; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY personne_menage
    ADD CONSTRAINT pk_personne_menage PRIMARY KEY (idpersonne, id_menage);


--
-- TOC entry 4503 (class 2606 OID 1517098)
-- Name: pk_personnemoraleparcelle; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY personnemoraleparcelle
    ADD CONSTRAINT pk_personnemoraleparcelle PRIMARY KEY (idparcelle, idpersonnemorale, idpersonne);


--
-- TOC entry 4507 (class 2606 OID 1517100)
-- Name: pk_personnemoraleparcelle_d; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY personnemoraleparcelle_d
    ADD CONSTRAINT pk_personnemoraleparcelle_d PRIMARY KEY (idpersonne, idparcelle);


--
-- TOC entry 4509 (class 2606 OID 1517104)
-- Name: pk_pointscardinaux; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY pointscardinaux
    ADD CONSTRAINT pk_pointscardinaux PRIMARY KEY (idpointscardinaux);


--
-- TOC entry 4515 (class 2606 OID 1517106)
-- Name: pk_projet_commune_idprojet_commune; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY projet_commune
    ADD CONSTRAINT pk_projet_commune_idprojet_commune PRIMARY KEY (idprojet_commune);


--
-- TOC entry 4513 (class 2606 OID 1517108)
-- Name: pk_projet_idprojet; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY projet
    ADD CONSTRAINT pk_projet_idprojet PRIMARY KEY (idprojet);


--
-- TOC entry 4525 (class 2606 OID 1517112)
-- Name: pk_proprietaire; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY proprietaireparcelle
    ADD CONSTRAINT pk_proprietaire PRIMARY KEY (idpersonne, idparcelle);


--
-- TOC entry 4527 (class 2606 OID 1517116)
-- Name: pk_region; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY region
    ADD CONSTRAINT pk_region PRIMARY KEY (idregion);


--
-- TOC entry 4531 (class 2606 OID 1517118)
-- Name: pk_rejet; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY rejet
    ADD CONSTRAINT pk_rejet PRIMARY KEY (idrejet);


--
-- TOC entry 4535 (class 2606 OID 1517120)
-- Name: pk_servitude; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY servitude
    ADD CONSTRAINT pk_servitude PRIMARY KEY (idservitude);


--
-- TOC entry 4541 (class 2606 OID 1517122)
-- Name: pk_servitude_parcelle; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY servitudeparcelle_d
    ADD CONSTRAINT pk_servitude_parcelle PRIMARY KEY (idservitude, idparcelle);


--
-- TOC entry 4539 (class 2606 OID 1517124)
-- Name: pk_servitudebeneficiaire; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY servitudebeneficiaire
    ADD CONSTRAINT pk_servitudebeneficiaire PRIMARY KEY (idbeneficiaire, idservitude);


--
-- TOC entry 4545 (class 2606 OID 1517126)
-- Name: pk_servitudeparcellegrevees; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY servitudeparcellegrevees
    ADD CONSTRAINT pk_servitudeparcellegrevees PRIMARY KEY (idparcellegrevees, idservitude);


--
-- TOC entry 4549 (class 2606 OID 1517128)
-- Name: pk_titre; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY titre
    ADD CONSTRAINT pk_titre PRIMARY KEY (gid);


--
-- TOC entry 4551 (class 2606 OID 1517130)
-- Name: pk_titrefoncier; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY titrefoncier
    ADD CONSTRAINT pk_titrefoncier PRIMARY KEY (gid);


--
-- TOC entry 4547 (class 2606 OID 1517132)
-- Name: pk_tss; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY terain_status_specifique
    ADD CONSTRAINT pk_tss PRIMARY KEY (gid);


--
-- TOC entry 4553 (class 2606 OID 1517134)
-- Name: pk_type_anomalie; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY type_anomalie
    ADD CONSTRAINT pk_type_anomalie PRIMARY KEY (id_type_anomalie);


--
-- TOC entry 4559 (class 2606 OID 1517136)
-- Name: pk_typeforfaitaire; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY typeforfaitaire
    ADD CONSTRAINT pk_typeforfaitaire PRIMARY KEY (idforfaitaire);


--
-- TOC entry 4561 (class 2606 OID 1517138)
-- Name: pk_typeoperationsubsequente; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY typeoperationsubsequente
    ADD CONSTRAINT pk_typeoperationsubsequente PRIMARY KEY (idtype);


--
-- TOC entry 4563 (class 2606 OID 1517140)
-- Name: pk_typepersonnemorale; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY typepersonnemorale
    ADD CONSTRAINT pk_typepersonnemorale PRIMARY KEY (idtype);


--
-- TOC entry 4567 (class 2606 OID 1517142)
-- Name: pk_utilisateur; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY utilisateur
    ADD CONSTRAINT pk_utilisateur PRIMARY KEY (idutilisateur);


--
-- TOC entry 4569 (class 2606 OID 1517144)
-- Name: pk_voisinparcelle; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY voisinparcelle
    ADD CONSTRAINT pk_voisinparcelle PRIMARY KEY (idvp);


--
-- TOC entry 4571 (class 2606 OID 1517146)
-- Name: pk_voisins; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY voisins
    ADD CONSTRAINT pk_voisins PRIMARY KEY (idvoisin);


--
-- TOC entry 4519 (class 2606 OID 1517148)
-- Name: projet_plof_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY projet_plof
    ADD CONSTRAINT projet_plof_pkey PRIMARY KEY (idprojet);


--
-- TOC entry 4521 (class 2606 OID 1517150)
-- Name: projetcouche_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY projetcouche
    ADD CONSTRAINT projetcouche_pkey PRIMARY KEY (id);


--
-- TOC entry 4533 (class 2606 OID 1517152)
-- Name: role_crl_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY role_crl
    ADD CONSTRAINT role_crl_pkey PRIMARY KEY (id_role);


--
-- TOC entry 4557 (class 2606 OID 1517154)
-- Name: type_document_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY type_document
    ADD CONSTRAINT type_document_pkey PRIMARY KEY (id_type);


--
-- TOC entry 4511 (class 2606 OID 1517156)
-- Name: ui_position; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY pointscardinaux
    ADD CONSTRAINT ui_position UNIQUE ("position");


--
-- TOC entry 4488 (class 2606 OID 1517158)
-- Name: uk_cin; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY personne
    ADD CONSTRAINT uk_cin UNIQUE (numcipersonne);


--
-- TOC entry 5309 (class 0 OID 0)
-- Dependencies: 4488
-- Name: CONSTRAINT uk_cin ON personne; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON CONSTRAINT uk_cin ON personne IS 'cle unique cin';


--
-- TOC entry 4404 (class 2606 OID 1517160)
-- Name: uk_code_fkt_idcom; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY fokontany
    ADD CONSTRAINT uk_code_fkt_idcom UNIQUE (codefokontany, idcommune);


--
-- TOC entry 4454 (class 2606 OID 1517162)
-- Name: uk_code_menage; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY menage
    ADD CONSTRAINT uk_code_menage UNIQUE (code_menage);


--
-- TOC entry 4476 (class 2606 OID 1517164)
-- Name: uk_code_parcelle; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY parcelle_d
    ADD CONSTRAINT uk_code_parcelle UNIQUE (codeparcelle, id_commune);


--
-- TOC entry 4415 (class 2606 OID 1517166)
-- Name: uk_codeham_idfkt; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY hameau
    ADD CONSTRAINT uk_codeham_idfkt UNIQUE (codehameau, idfokontany);


--
-- TOC entry 4372 (class 2606 OID 1517168)
-- Name: uk_codeparcelle; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY demande
    ADD CONSTRAINT uk_codeparcelle UNIQUE (code_parcelle, idcommune);


--
-- TOC entry 4290 (class 2606 OID 1517170)
-- Name: uk_csv_anomalie; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY anomalie
    ADD CONSTRAINT uk_csv_anomalie UNIQUE (csv_id);


--
-- TOC entry 4298 (class 2606 OID 1517172)
-- Name: uk_csv_avd; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY avoir_demande
    ADD CONSTRAINT uk_csv_avd UNIQUE (csv_id);


--
-- TOC entry 4345 (class 2606 OID 1517174)
-- Name: uk_csv_commu; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY commune
    ADD CONSTRAINT uk_csv_commu UNIQUE (csv_id);


--
-- TOC entry 4374 (class 2606 OID 1517176)
-- Name: uk_csv_dema; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY demande
    ADD CONSTRAINT uk_csv_dema UNIQUE (csv_id);


--
-- TOC entry 4387 (class 2606 OID 1517178)
-- Name: uk_csv_demande_sans; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY demande_sans_geom
    ADD CONSTRAINT uk_csv_demande_sans UNIQUE (csv_id);


--
-- TOC entry 4395 (class 2606 OID 1517180)
-- Name: uk_csv_dist; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY district
    ADD CONSTRAINT uk_csv_dist UNIQUE (csv_id);


--
-- TOC entry 4406 (class 2606 OID 1517182)
-- Name: uk_csv_foko; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY fokontany
    ADD CONSTRAINT uk_csv_foko UNIQUE (csv_id);


--
-- TOC entry 4417 (class 2606 OID 1517184)
-- Name: uk_csv_hame; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY hameau
    ADD CONSTRAINT uk_csv_hame UNIQUE (csv_id);


--
-- TOC entry 4478 (class 2606 OID 1517186)
-- Name: uk_csv_parcd; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY parcelle_d
    ADD CONSTRAINT uk_csv_parcd UNIQUE (csv_id);


--
-- TOC entry 4490 (class 2606 OID 1517188)
-- Name: uk_csv_pers; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY personne
    ADD CONSTRAINT uk_csv_pers UNIQUE (csv_id);


--
-- TOC entry 4505 (class 2606 OID 1517190)
-- Name: uk_csv_persmorparc; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY personnemoraleparcelle
    ADD CONSTRAINT uk_csv_persmorparc UNIQUE (csv_id);


--
-- TOC entry 4498 (class 2606 OID 1517192)
-- Name: uk_csv_personnemorale; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY personnemorale
    ADD CONSTRAINT uk_csv_personnemorale UNIQUE (csv_id);


--
-- TOC entry 4529 (class 2606 OID 1517194)
-- Name: uk_csv_reg; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY region
    ADD CONSTRAINT uk_csv_reg UNIQUE (csv_id);


--
-- TOC entry 4555 (class 2606 OID 1517196)
-- Name: uk_csv_typeano; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY type_anomalie
    ADD CONSTRAINT uk_csv_typeano UNIQUE (csv_id);


--
-- TOC entry 4565 (class 2606 OID 1517198)
-- Name: uk_csv_typersonnemorale; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY typepersonnemorale
    ADD CONSTRAINT uk_csv_typersonnemorale UNIQUE (csv_id);


--
-- TOC entry 4376 (class 2606 OID 1517200)
-- Name: uk_demande; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY demande
    ADD CONSTRAINT uk_demande UNIQUE (numdemande);


--
-- TOC entry 4378 (class 2606 OID 1517202)
-- Name: uk_gid; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY demande
    ADD CONSTRAINT uk_gid UNIQUE (gid);


--
-- TOC entry 5310 (class 0 OID 0)
-- Dependencies: 4378
-- Name: CONSTRAINT uk_gid ON demande; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON CONSTRAINT uk_gid ON demande IS 'unique gid from parcelle_d';


--
-- TOC entry 4319 (class 2606 OID 1517204)
-- Name: uk_idpersonne; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY blob_personne
    ADD CONSTRAINT uk_idpersonne UNIQUE (idpersonne);


--
-- TOC entry 4334 (class 2606 OID 1517206)
-- Name: uk_numcertificat; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY certificat
    ADD CONSTRAINT uk_numcertificat UNIQUE (numerocertificat);


--
-- TOC entry 4358 (class 2606 OID 1517208)
-- Name: unik_cin_contribuable; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY contribuable
    ADD CONSTRAINT unik_cin_contribuable UNIQUE (cin);


--
-- TOC entry 4430 (class 2606 OID 1517212)
-- Name: unik_impot_batiment; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY impot_batiment
    ADD CONSTRAINT unik_impot_batiment UNIQUE (annee, codebatiment);


--
-- TOC entry 4435 (class 2606 OID 1517214)
-- Name: unik_impot_contribuable; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY impot_contribuable
    ADD CONSTRAINT unik_impot_contribuable UNIQUE (annee, idpersonne);


--
-- TOC entry 4442 (class 2606 OID 1517216)
-- Name: unik_impot_parcelle; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY impot_parcelle
    ADD CONSTRAINT unik_impot_parcelle UNIQUE (annee, idparcelle);


--
-- TOC entry 4306 (class 2606 OID 1517218)
-- Name: unik_personne_a; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY avoirconjoint
    ADD CONSTRAINT unik_personne_a UNIQUE (idconjoint_a);


--
-- TOC entry 4308 (class 2606 OID 1517220)
-- Name: unik_personne_b; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY avoirconjoint
    ADD CONSTRAINT unik_personne_b UNIQUE (idconjoint_b);


--
-- TOC entry 4480 (class 2606 OID 1517222)
-- Name: unique_certificat; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY parcelle_d
    ADD CONSTRAINT unique_certificat UNIQUE (idcertificat);


--
-- TOC entry 4517 (class 2606 OID 1517224)
-- Name: uq_projet_commune; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY projet_commune
    ADD CONSTRAINT uq_projet_commune UNIQUE (idcommune, idprojet);


--
-- TOC entry 4574 (class 2606 OID 1517226)
-- Name: z_certifiable_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY z_certifiable
    ADD CONSTRAINT z_certifiable_pkey PRIMARY KEY (gid);


--
-- TOC entry 4379 (class 1259 OID 1517227)
-- Name: fki_anomalie; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_anomalie ON demande_anomalie USING btree (idanomalie);


--
-- TOC entry 4299 (class 1259 OID 1517228)
-- Name: fki_avoir_dmd_iddemande; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_avoir_dmd_iddemande ON avoir_dmd USING btree (iddemande);


--
-- TOC entry 4300 (class 1259 OID 1517229)
-- Name: fki_avoir_dmd_iddemandeur; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_avoir_dmd_iddemandeur ON avoir_dmd USING btree (iddemandeur);


--
-- TOC entry 4426 (class 1259 OID 1517230)
-- Name: fki_batiment; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_batiment ON impot_batiment USING btree (codebatiment);


--
-- TOC entry 4309 (class 1259 OID 1517231)
-- Name: fki_categorie; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_categorie ON batiment USING btree (idcategorie);


--
-- TOC entry 4465 (class 1259 OID 1517232)
-- Name: fki_certificat; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_certificat ON parcelle_d USING btree (idcertificat);


--
-- TOC entry 4466 (class 1259 OID 1517233)
-- Name: fki_charge; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_charge ON parcelle_d USING btree (idcharge);


--
-- TOC entry 4467 (class 1259 OID 1517234)
-- Name: fki_consistance; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_consistance ON parcelle_d USING btree (id_consistance);


--
-- TOC entry 4354 (class 1259 OID 1517235)
-- Name: fki_consort; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_consort ON contribuable USING btree (idcontribuableconsorts);


--
-- TOC entry 4359 (class 1259 OID 1517236)
-- Name: fki_consorts; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_consorts ON contribuableconsorts USING btree (idconsort);


--
-- TOC entry 4468 (class 1259 OID 1517237)
-- Name: fki_contribuable; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_contribuable ON parcelle_d USING btree (idcontribuable);


--
-- TOC entry 4460 (class 1259 OID 1517238)
-- Name: fki_demande; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_demande ON oppositions USING btree (iddemande);


--
-- TOC entry 4491 (class 1259 OID 1517239)
-- Name: fki_fk_menage; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_fk_menage ON personne_menage USING btree (id_menage);


--
-- TOC entry 4492 (class 1259 OID 1517240)
-- Name: fki_fk_personne; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_fk_personne ON personne_menage USING btree (idpersonne);


--
-- TOC entry 4390 (class 1259 OID 1517241)
-- Name: fki_fk_region; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_fk_region ON district USING btree (idregion);


--
-- TOC entry 4330 (class 1259 OID 1517242)
-- Name: fki_fokontany; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_fokontany ON certificat USING btree (idfokontany);


--
-- TOC entry 4469 (class 1259 OID 1517243)
-- Name: fki_hypotheque; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_hypotheque ON parcelle_d USING btree (idhypotheque);


--
-- TOC entry 4470 (class 1259 OID 1517244)
-- Name: fki_idcommune; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_idcommune ON parcelle_d USING btree (id_commune);


--
-- TOC entry 4522 (class 1259 OID 1517245)
-- Name: fki_parcelle; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_parcelle ON proprietaireparcelle USING btree (idparcelle);


--
-- TOC entry 4471 (class 1259 OID 1517246)
-- Name: fki_parcelle_classe; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_parcelle_classe ON parcelle_d USING btree (idclasse);


--
-- TOC entry 4438 (class 1259 OID 1517247)
-- Name: fki_parcelle_impot; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_parcelle_impot ON impot_parcelle USING btree (idparcelle);


--
-- TOC entry 4431 (class 1259 OID 1517248)
-- Name: fki_personne; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_personne ON impot_contribuable USING btree (idpersonne);


--
-- TOC entry 4472 (class 1259 OID 1517249)
-- Name: fki_servitude; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_servitude ON parcelle_d USING btree (idservitude);


--
-- TOC entry 4536 (class 1259 OID 1517250)
-- Name: fki_servitudebeneficiaire_serv; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_servitudebeneficiaire_serv ON servitudebeneficiaire USING btree (idservitude);


--
-- TOC entry 4542 (class 1259 OID 1517251)
-- Name: fki_servitudeparcellegrevees_serv; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_servitudeparcellegrevees_serv ON servitudeparcellegrevees USING btree (idservitude);


--
-- TOC entry 4286 (class 1259 OID 1517252)
-- Name: fki_type_anomalie; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_type_anomalie ON anomalie USING btree (id_type_anomalie);


--
-- TOC entry 4266 (class 1259 OID 1517253)
-- Name: i_fk_actedecessubsequente_acte; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_actedecessubsequente_acte ON actedecessubsequente USING btree (idactedeces);


--
-- TOC entry 4267 (class 1259 OID 1517254)
-- Name: i_fk_actedecessubsequente_oper; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_actedecessubsequente_oper ON actedecessubsequente USING btree (idoperationsubsequente);


--
-- TOC entry 4274 (class 1259 OID 1517255)
-- Name: i_fk_acteprivesubsequente_acte; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_acteprivesubsequente_acte ON acteprivesubsequente USING btree (idacteprive);


--
-- TOC entry 4275 (class 1259 OID 1517256)
-- Name: i_fk_acteprivesubsequente_oper; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_acteprivesubsequente_oper ON acteprivesubsequente USING btree (idoperationsubsequente);


--
-- TOC entry 4280 (class 1259 OID 1517257)
-- Name: i_fk_actepublicsubsequente_act; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_actepublicsubsequente_act ON actepublicsubsequente USING btree (idactepublic);


--
-- TOC entry 4281 (class 1259 OID 1517258)
-- Name: i_fk_actepublicsubsequente_ope; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_actepublicsubsequente_ope ON actepublicsubsequente USING btree (idoperationsubsequente);


--
-- TOC entry 4310 (class 1259 OID 1517259)
-- Name: i_fk_batiment_consistance; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_batiment_consistance ON batiment USING btree (idconsistance);


--
-- TOC entry 4311 (class 1259 OID 1517260)
-- Name: i_fk_batiment_parcelle; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_batiment_parcelle ON batiment USING btree (idparcelle);


--
-- TOC entry 4326 (class 1259 OID 1517261)
-- Name: i_fk_categorieforfaitaire_cate; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_categorieforfaitaire_cate ON categorieforfaitaire USING btree (idcategorie);


--
-- TOC entry 4327 (class 1259 OID 1517262)
-- Name: i_fk_categorieforfaitaire_type; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_categorieforfaitaire_type ON categorieforfaitaire USING btree (idforfaitaire);


--
-- TOC entry 4337 (class 1259 OID 1517263)
-- Name: i_fk_classecategorieforfaitai1; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_classecategorieforfaitai1 ON classecategorieforfaitaire USING btree (idclasse);


--
-- TOC entry 4338 (class 1259 OID 1517264)
-- Name: i_fk_classecategorieforfaitair; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_classecategorieforfaitair ON classecategorieforfaitaire USING btree (idcategorie);


--
-- TOC entry 4341 (class 1259 OID 1517265)
-- Name: i_fk_commune_district; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_commune_district ON commune USING btree (iddistrict);


--
-- TOC entry 4350 (class 1259 OID 1517266)
-- Name: i_fk_consistanceforfaitaire_co; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_consistanceforfaitaire_co ON consistanceforfaitaire USING btree (idconsistance);


--
-- TOC entry 4351 (class 1259 OID 1517267)
-- Name: i_fk_consistanceforfaitaire_ty; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_consistanceforfaitaire_ty ON consistanceforfaitaire USING btree (idforfaitaire);


--
-- TOC entry 4364 (class 1259 OID 1517268)
-- Name: i_fk_decisionsubsequente_decis; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_decisionsubsequente_decis ON decisionsubsequente USING btree (iddecision);


--
-- TOC entry 4365 (class 1259 OID 1517269)
-- Name: i_fk_decisionsubsequente_opera; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_decisionsubsequente_opera ON decisionsubsequente USING btree (idoperationsubsequente);


--
-- TOC entry 4370 (class 1259 OID 1517270)
-- Name: i_fk_demande_parcelle_d; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_demande_parcelle_d ON demande USING btree (gid);


--
-- TOC entry 4391 (class 1259 OID 1517271)
-- Name: i_fk_district_region; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_district_region ON district USING btree (idregion);


--
-- TOC entry 4400 (class 1259 OID 1517272)
-- Name: i_fk_fokontany_commune; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_fokontany_commune ON fokontany USING btree (idcommune);


--
-- TOC entry 4411 (class 1259 OID 1517273)
-- Name: i_fk_hameau_fokontany; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_hameau_fokontany ON hameau USING btree (idfokontany);


--
-- TOC entry 4443 (class 1259 OID 1517274)
-- Name: i_fk_impotparcelle_impot; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_impotparcelle_impot ON impotparcelle USING btree (idimpot);


--
-- TOC entry 4444 (class 1259 OID 1517275)
-- Name: i_fk_impotparcelle_parcelle; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_impotparcelle_parcelle ON impotparcelle USING btree (idparcelle);


--
-- TOC entry 4457 (class 1259 OID 1517276)
-- Name: i_fk_operationsubsequente_parc; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_operationsubsequente_parc ON operationsubsequente USING btree (idparcelle);


--
-- TOC entry 4499 (class 1259 OID 1517284)
-- Name: i_fk_personnemoraleparcelle_p1; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_personnemoraleparcelle_p1 ON personnemoraleparcelle USING btree (idpersonne);


--
-- TOC entry 4500 (class 1259 OID 1517285)
-- Name: i_fk_personnemoraleparcelle_pa; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_personnemoraleparcelle_pa ON personnemoraleparcelle USING btree (idparcelle);


--
-- TOC entry 4501 (class 1259 OID 1517286)
-- Name: i_fk_personnemoraleparcelle_pe; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_personnemoraleparcelle_pe ON personnemoraleparcelle USING btree (idpersonnemorale);


--
-- TOC entry 4523 (class 1259 OID 1517287)
-- Name: i_fk_proprietaireparcelle_pers; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_proprietaireparcelle_pers ON proprietaireparcelle USING btree (idpersonne);


--
-- TOC entry 4537 (class 1259 OID 1517288)
-- Name: i_fk_servitudebeneficiaire_ben; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_servitudebeneficiaire_ben ON servitudebeneficiaire USING btree (idbeneficiaire);


--
-- TOC entry 4543 (class 1259 OID 1517289)
-- Name: i_fk_servitudeparcellegrevees1; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX i_fk_servitudeparcellegrevees1 ON servitudeparcellegrevees USING btree (idparcellegrevees);


--
-- TOC entry 4572 (class 1259 OID 1517290)
-- Name: z_certifiable_geom_idx; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX z_certifiable_geom_idx ON z_certifiable USING gist (geom);


--
-- TOC entry 4675 (class 2620 OID 2257404)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON actepublic FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4671 (class 2620 OID 2257405)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON acteprive FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4669 (class 2620 OID 2257406)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON actedejalance FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4679 (class 2620 OID 2257407)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON aireastatutspecifique FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4701 (class 2620 OID 2257408)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON blob_voisin FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4703 (class 2620 OID 2257409)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON cadastre FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4737 (class 2620 OID 2257410)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON demande_sans_geom FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4767 (class 2620 OID 2257411)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON impot_minimum FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4805 (class 2620 OID 2257412)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON pointscardinaux FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4811 (class 2620 OID 2257413)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON projet_plof FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4693 (class 2620 OID 2257415)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON batiment FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4687 (class 2620 OID 2257416)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON avoir_demande FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4681 (class 2620 OID 2257417)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON anomalie FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4677 (class 2620 OID 2257418)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON actepublicsubsequente FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4663 (class 2620 OID 2257419)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON acces FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4689 (class 2620 OID 2257420)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON avoir_dmd FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4695 (class 2620 OID 2257421)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON beneficiaire FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4683 (class 2620 OID 2257422)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON autrecharge FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4685 (class 2620 OID 2257423)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON autrechargesparcelle_d FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4691 (class 2620 OID 2257424)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON avoirconjoint FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4711 (class 2620 OID 2257425)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON classe FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4719 (class 2620 OID 2257426)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON consistance_batiment FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4723 (class 2620 OID 2257427)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON contribuable FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4717 (class 2620 OID 2257428)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON consistance FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4721 (class 2620 OID 2257429)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON consistanceforfaitaire FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4715 (class 2620 OID 2257430)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON commune FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4705 (class 2620 OID 2257431)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON categorie FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4729 (class 2620 OID 2257432)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON decisionsubsequente FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4709 (class 2620 OID 2257433)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON certificat FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4725 (class 2620 OID 2257434)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON contribuableconsorts FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4727 (class 2620 OID 2257435)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON contribuables_parcelle FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4697 (class 2620 OID 2257436)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON blob_history FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4739 (class 2620 OID 2257437)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON demandefn FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4749 (class 2620 OID 2257438)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON groupe FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4745 (class 2620 OID 2257439)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON fi_paiement_impot FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4755 (class 2620 OID 2257440)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON historique FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4753 (class 2620 OID 2257441)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON hameau FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4747 (class 2620 OID 2257442)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON fokontany FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4741 (class 2620 OID 2257443)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON district FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4751 (class 2620 OID 2257444)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON groupe_acces FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4779 (class 2620 OID 2257445)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON migration_history FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4781 (class 2620 OID 2257446)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON operationsub FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4769 (class 2620 OID 2257447)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON impot_parcelle FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4787 (class 2620 OID 2257448)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON param_layer FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4763 (class 2620 OID 2257449)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON impot_batiment FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4761 (class 2620 OID 2257450)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON impot FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4757 (class 2620 OID 2257451)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON hypotheque FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4773 (class 2620 OID 2257452)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON journal FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4777 (class 2620 OID 2257453)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON menage FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4785 (class 2620 OID 2257454)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON oppositions FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4765 (class 2620 OID 2257455)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON impot_contribuable FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4775 (class 2620 OID 2257456)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON limitesparcelle FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4799 (class 2620 OID 2257457)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON personnemorale FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4793 (class 2620 OID 2257458)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON path_personne FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4797 (class 2620 OID 2257459)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON personne_menage FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4791 (class 2620 OID 2257460)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON parcellegrevees FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4819 (class 2620 OID 2257461)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON rejet FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4835 (class 2620 OID 2257462)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON titrefoncier FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4831 (class 2620 OID 2257463)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON terain_status_specifique FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4833 (class 2620 OID 2257464)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON titre FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4731 (class 2620 OID 2257465)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON demande FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4813 (class 2620 OID 2257466)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON projetcouche FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4823 (class 2620 OID 2257467)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON servitude FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4807 (class 2620 OID 2257468)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON projet FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4815 (class 2620 OID 2257469)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON proprietaireparcelle FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4817 (class 2620 OID 2257470)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON region FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4829 (class 2620 OID 2257471)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON servitudeparcellegrevees FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4843 (class 2620 OID 2257472)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON typeoperationsubsequente FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4849 (class 2620 OID 2257473)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON voisinparcelle FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4851 (class 2620 OID 2257474)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON voisins FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4853 (class 2620 OID 2257475)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON z_certifiable FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4845 (class 2620 OID 2257476)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON typepersonnemorale FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4847 (class 2620 OID 2257477)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON utilisateur FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4837 (class 2620 OID 2257478)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON type_anomalie FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4821 (class 2620 OID 2257479)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON role_crl FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4827 (class 2620 OID 2257480)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON servitudeparcelle_d FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4825 (class 2620 OID 2257481)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON servitudebeneficiaire FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4759 (class 2620 OID 2257482)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON hypothequeparcelle_d FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4735 (class 2620 OID 2257483)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON demande_crl FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4839 (class 2620 OID 2257484)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON type_document FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4743 (class 2620 OID 2257485)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON document FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4667 (class 2620 OID 2257486)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON actedecessubsequente FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4713 (class 2620 OID 2257487)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON classecategorieforfaitaire FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4673 (class 2620 OID 2257488)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON acteprivesubsequente FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4795 (class 2620 OID 2257489)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON personne FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4809 (class 2620 OID 2257490)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON projet_commune FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4699 (class 2620 OID 2257491)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON blob_personne FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4771 (class 2620 OID 2257492)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON impotparcelle FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4803 (class 2620 OID 2257493)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON personnemoraleparcelle_d FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4707 (class 2620 OID 2257494)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON categorieforfaitaire FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4841 (class 2620 OID 2257495)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON typeforfaitaire FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4783 (class 2620 OID 2257496)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON operationsubsequente FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4733 (class 2620 OID 2257497)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON demande_anomalie FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4801 (class 2620 OID 2257498)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON personnemoraleparcelle FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4789 (class 2620 OID 2257499)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON parcelle_d FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4665 (class 2620 OID 2257500)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON actedeces FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4854 (class 2620 OID 2257501)
-- Name: trigger_update_date_dernier_maj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_date_dernier_maj AFTER INSERT OR DELETE OR UPDATE ON date_synchro FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();


--
-- TOC entry 4662 (class 2620 OID 1529500)
-- Name: update_acces_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_acces_datemaj BEFORE UPDATE ON acces FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4664 (class 2620 OID 1529577)
-- Name: update_actedeces_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_actedeces_datemaj BEFORE UPDATE ON actedeces FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4666 (class 2620 OID 1529578)
-- Name: update_actedecessubsequente_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_actedecessubsequente_datemaj BEFORE UPDATE ON actedecessubsequente FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4668 (class 2620 OID 1529481)
-- Name: update_actedejalance_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_actedejalance_datemaj BEFORE UPDATE ON actedejalance FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4670 (class 2620 OID 1529498)
-- Name: update_acteprive_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_acteprive_datemaj BEFORE UPDATE ON acteprive FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4672 (class 2620 OID 1529580)
-- Name: update_acteprivesubsequente_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_acteprivesubsequente_datemaj BEFORE UPDATE ON acteprivesubsequente FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4674 (class 2620 OID 1529499)
-- Name: update_actepublic_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_actepublic_datemaj BEFORE UPDATE ON actepublic FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4676 (class 2620 OID 1529497)
-- Name: update_actepublicsubsequente_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_actepublicsubsequente_datemaj BEFORE UPDATE ON actepublicsubsequente FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4678 (class 2620 OID 1529482)
-- Name: update_aireastatutspecifique_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_aireastatutspecifique_datemaj BEFORE UPDATE ON aireastatutspecifique FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4680 (class 2620 OID 1529496)
-- Name: update_anomalie_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_anomalie_datemaj BEFORE UPDATE ON anomalie FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4682 (class 2620 OID 1529503)
-- Name: update_autrecharge_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_autrecharge_datemaj BEFORE UPDATE ON autrecharge FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4684 (class 2620 OID 1529504)
-- Name: update_autrechargesparcelle_d_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_autrechargesparcelle_d_datemaj BEFORE UPDATE ON autrechargesparcelle_d FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4686 (class 2620 OID 1529495)
-- Name: update_avoir_demande_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_avoir_demande_datemaj BEFORE UPDATE ON avoir_demande FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4688 (class 2620 OID 1529501)
-- Name: update_avoir_dmd_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_avoir_dmd_datemaj BEFORE UPDATE ON avoir_dmd FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4690 (class 2620 OID 1529505)
-- Name: update_avoirconjoint_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_avoirconjoint_datemaj BEFORE UPDATE ON avoirconjoint FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4692 (class 2620 OID 1529494)
-- Name: update_batiment_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_batiment_datemaj BEFORE UPDATE ON batiment FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4694 (class 2620 OID 1529502)
-- Name: update_beneficiaire_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_beneficiaire_datemaj BEFORE UPDATE ON beneficiaire FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4696 (class 2620 OID 1529518)
-- Name: update_blob_history_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_blob_history_datemaj BEFORE UPDATE ON blob_history FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4698 (class 2620 OID 1529583)
-- Name: update_blob_personne_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_blob_personne_datemaj BEFORE UPDATE ON blob_personne FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4700 (class 2620 OID 1529483)
-- Name: update_blob_voisin_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_blob_voisin_datemaj BEFORE UPDATE ON blob_voisin FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4702 (class 2620 OID 1529484)
-- Name: update_cadastre_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_cadastre_datemaj BEFORE UPDATE ON cadastre FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4704 (class 2620 OID 1529512)
-- Name: update_categorie_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_categorie_datemaj BEFORE UPDATE ON categorie FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4706 (class 2620 OID 1529586)
-- Name: update_categorieforfaitaire_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_categorieforfaitaire_datemaj BEFORE UPDATE ON categorieforfaitaire FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4708 (class 2620 OID 1529515)
-- Name: update_certificat_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_certificat_datemaj BEFORE UPDATE ON certificat FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4710 (class 2620 OID 1529506)
-- Name: update_classe_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_classe_datemaj BEFORE UPDATE ON classe FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4712 (class 2620 OID 1529579)
-- Name: update_classecategorieforfaitaire_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_classecategorieforfaitaire_datemaj BEFORE UPDATE ON classecategorieforfaitaire FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4714 (class 2620 OID 1529511)
-- Name: update_commune_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_commune_datemaj BEFORE UPDATE ON commune FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4718 (class 2620 OID 1529507)
-- Name: update_consistance_batiment_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_consistance_batiment_datemaj BEFORE UPDATE ON consistance_batiment FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4716 (class 2620 OID 1529509)
-- Name: update_consistance_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_consistance_datemaj BEFORE UPDATE ON consistance FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4720 (class 2620 OID 1529510)
-- Name: update_consistanceforfaitaire_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_consistanceforfaitaire_datemaj BEFORE UPDATE ON consistanceforfaitaire FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4722 (class 2620 OID 1529508)
-- Name: update_contribuable_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_contribuable_datemaj BEFORE UPDATE ON contribuable FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4724 (class 2620 OID 1529516)
-- Name: update_contribuableconsorts_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_contribuableconsorts_datemaj BEFORE UPDATE ON contribuableconsorts FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4726 (class 2620 OID 1529517)
-- Name: update_contribuables_parcelle_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_contribuables_parcelle_datemaj BEFORE UPDATE ON contribuables_parcelle FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4728 (class 2620 OID 1529514)
-- Name: update_decisionsubsequente_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_decisionsubsequente_datemaj BEFORE UPDATE ON decisionsubsequente FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4732 (class 2620 OID 1529589)
-- Name: update_demande_anomalie_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_demande_anomalie_datemaj BEFORE UPDATE ON demande_anomalie FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4734 (class 2620 OID 1529574)
-- Name: update_demande_crl_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_demande_crl_datemaj BEFORE UPDATE ON demande_crl FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4730 (class 2620 OID 1529527)
-- Name: update_demande_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_demande_datemaj BEFORE UPDATE ON demande FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4736 (class 2620 OID 1529485)
-- Name: update_demande_sans_geom_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_demande_sans_geom_datemaj BEFORE UPDATE ON demande_sans_geom FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4738 (class 2620 OID 1529519)
-- Name: update_demandefn_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_demandefn_datemaj BEFORE UPDATE ON demandefn FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4740 (class 2620 OID 1529528)
-- Name: update_district_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_district_datemaj BEFORE UPDATE ON district FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4742 (class 2620 OID 1529576)
-- Name: update_document_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_document_datemaj BEFORE UPDATE ON document FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4744 (class 2620 OID 1529522)
-- Name: update_fi_paiement_impot_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_fi_paiement_impot_datemaj BEFORE UPDATE ON fi_paiement_impot FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4746 (class 2620 OID 1529526)
-- Name: update_fokontany_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_fokontany_datemaj BEFORE UPDATE ON fokontany FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4750 (class 2620 OID 1529529)
-- Name: update_groupe_acces_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_groupe_acces_datemaj BEFORE UPDATE ON groupe_acces FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4748 (class 2620 OID 1529520)
-- Name: update_groupe_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_groupe_datemaj BEFORE UPDATE ON groupe FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4752 (class 2620 OID 1529525)
-- Name: update_hameau_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_hameau_datemaj BEFORE UPDATE ON hameau FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4754 (class 2620 OID 1529523)
-- Name: update_historique_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_historique_datemaj BEFORE UPDATE ON historique FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4756 (class 2620 OID 1529537)
-- Name: update_hypotheque_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_hypotheque_datemaj BEFORE UPDATE ON hypotheque FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4758 (class 2620 OID 1529573)
-- Name: update_hypothequeparcelle_d_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_hypothequeparcelle_d_datemaj BEFORE UPDATE ON hypothequeparcelle_d FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4762 (class 2620 OID 1529535)
-- Name: update_impot_batiment_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_impot_batiment_datemaj BEFORE UPDATE ON impot_batiment FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4764 (class 2620 OID 1529542)
-- Name: update_impot_contribuable_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_impot_contribuable_datemaj BEFORE UPDATE ON impot_contribuable FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4760 (class 2620 OID 1529536)
-- Name: update_impot_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_impot_datemaj BEFORE UPDATE ON impot FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4766 (class 2620 OID 1529487)
-- Name: update_impot_minimum_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_impot_minimum_datemaj BEFORE UPDATE ON impot_minimum FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4768 (class 2620 OID 1529532)
-- Name: update_impot_parcelle_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_impot_parcelle_datemaj BEFORE UPDATE ON impot_parcelle FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4770 (class 2620 OID 1529584)
-- Name: update_impotparcelle_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_impotparcelle_datemaj BEFORE UPDATE ON impotparcelle FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4772 (class 2620 OID 1529538)
-- Name: update_journal_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_journal_datemaj BEFORE UPDATE ON journal FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4774 (class 2620 OID 1529543)
-- Name: update_limitesparcelle_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_limitesparcelle_datemaj BEFORE UPDATE ON limitesparcelle FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4776 (class 2620 OID 1529539)
-- Name: update_menage_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_menage_datemaj BEFORE UPDATE ON menage FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4778 (class 2620 OID 1529530)
-- Name: update_migration_history_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_migration_history_datemaj BEFORE UPDATE ON migration_history FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4780 (class 2620 OID 1529531)
-- Name: update_operationsub_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_operationsub_datemaj BEFORE UPDATE ON operationsub FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4782 (class 2620 OID 1529588)
-- Name: update_operationsubsequente_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_operationsubsequente_datemaj BEFORE UPDATE ON operationsubsequente FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4784 (class 2620 OID 1529541)
-- Name: update_oppositions_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_oppositions_datemaj BEFORE UPDATE ON oppositions FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4786 (class 2620 OID 1529533)
-- Name: update_param_layer_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_param_layer_datemaj BEFORE UPDATE ON param_layer FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4788 (class 2620 OID 1529591)
-- Name: update_parcelle_d_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_parcelle_d_datemaj BEFORE UPDATE ON parcelle_d FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4790 (class 2620 OID 1529550)
-- Name: update_parcellegrevees_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_parcellegrevees_datemaj BEFORE UPDATE ON parcellegrevees FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4792 (class 2620 OID 1529546)
-- Name: update_path_personne_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_path_personne_datemaj BEFORE UPDATE ON path_personne FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4794 (class 2620 OID 1529581)
-- Name: update_personne_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_personne_datemaj BEFORE UPDATE ON personne FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4796 (class 2620 OID 1529548)
-- Name: update_personne_menage_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_personne_menage_datemaj BEFORE UPDATE ON personne_menage FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4798 (class 2620 OID 1529545)
-- Name: update_personnemorale_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_personnemorale_datemaj BEFORE UPDATE ON personnemorale FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4802 (class 2620 OID 1529585)
-- Name: update_personnemoraleparcelle_d_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_personnemoraleparcelle_d_datemaj BEFORE UPDATE ON personnemoraleparcelle_d FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4800 (class 2620 OID 1529590)
-- Name: update_personnemoraleparcelle_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_personnemoraleparcelle_datemaj BEFORE UPDATE ON personnemoraleparcelle FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4804 (class 2620 OID 1529489)
-- Name: update_pointscardinaux_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_pointscardinaux_datemaj BEFORE UPDATE ON pointscardinaux FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4808 (class 2620 OID 1529582)
-- Name: update_projet_commune_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_projet_commune_datemaj BEFORE UPDATE ON projet_commune FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4806 (class 2620 OID 1529558)
-- Name: update_projet_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_projet_datemaj BEFORE UPDATE ON projet FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4810 (class 2620 OID 1529491)
-- Name: update_projet_plof_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_projet_plof_datemaj BEFORE UPDATE ON projet_plof FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4812 (class 2620 OID 1529556)
-- Name: update_projetcouche_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_projetcouche_datemaj BEFORE UPDATE ON projetcouche FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4814 (class 2620 OID 1529559)
-- Name: update_proprietaireparcelle_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_proprietaireparcelle_datemaj BEFORE UPDATE ON proprietaireparcelle FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4816 (class 2620 OID 1529561)
-- Name: update_region_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_region_datemaj BEFORE UPDATE ON region FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4818 (class 2620 OID 1529552)
-- Name: update_rejet_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_rejet_datemaj BEFORE UPDATE ON rejet FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4820 (class 2620 OID 1529570)
-- Name: update_role_crl_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_role_crl_datemaj BEFORE UPDATE ON role_crl FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4822 (class 2620 OID 1529557)
-- Name: update_servitude_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_servitude_datemaj BEFORE UPDATE ON servitude FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4824 (class 2620 OID 1529572)
-- Name: update_servitudebeneficiaire_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_servitudebeneficiaire_datemaj BEFORE UPDATE ON servitudebeneficiaire FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4826 (class 2620 OID 1529571)
-- Name: update_servitudeparcelle_d_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_servitudeparcelle_d_datemaj BEFORE UPDATE ON servitudeparcelle_d FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4828 (class 2620 OID 1529562)
-- Name: update_servitudeparcellegrevees_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_servitudeparcellegrevees_datemaj BEFORE UPDATE ON servitudeparcellegrevees FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4830 (class 2620 OID 1529554)
-- Name: update_terain_status_specifique_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_terain_status_specifique_datemaj BEFORE UPDATE ON terain_status_specifique FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4832 (class 2620 OID 1529555)
-- Name: update_titre_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_titre_datemaj BEFORE UPDATE ON titre FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4834 (class 2620 OID 1529553)
-- Name: update_titrefoncier_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_titrefoncier_datemaj BEFORE UPDATE ON titrefoncier FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4836 (class 2620 OID 1529569)
-- Name: update_type_anomalie_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_type_anomalie_datemaj BEFORE UPDATE ON type_anomalie FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4838 (class 2620 OID 1529575)
-- Name: update_type_document_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_type_document_datemaj BEFORE UPDATE ON type_document FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4840 (class 2620 OID 1529587)
-- Name: update_typeforfaitaire_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_typeforfaitaire_datemaj BEFORE UPDATE ON typeforfaitaire FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4842 (class 2620 OID 1529563)
-- Name: update_typeoperationsubsequente_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_typeoperationsubsequente_datemaj BEFORE UPDATE ON typeoperationsubsequente FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4844 (class 2620 OID 1529567)
-- Name: update_typepersonnemorale_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_typepersonnemorale_datemaj BEFORE UPDATE ON typepersonnemorale FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4846 (class 2620 OID 1529568)
-- Name: update_utilisateur_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_utilisateur_datemaj BEFORE UPDATE ON utilisateur FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4848 (class 2620 OID 1529564)
-- Name: update_voisinparcelle_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_voisinparcelle_datemaj BEFORE UPDATE ON voisinparcelle FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4850 (class 2620 OID 1529565)
-- Name: update_voisins_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_voisins_datemaj BEFORE UPDATE ON voisins FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4852 (class 2620 OID 1529566)
-- Name: update_z_certifiable_datemaj; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_z_certifiable_datemaj BEFORE UPDATE ON z_certifiable FOR EACH ROW EXECUTE PROCEDURE update_datemaj();


--
-- TOC entry 4614 (class 2606 OID 1517291)
-- Name: demande_crl_id_role_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY demande_crl
    ADD CONSTRAINT demande_crl_id_role_fkey FOREIGN KEY (id_role) REFERENCES role_crl(id_role);


--
-- TOC entry 4615 (class 2606 OID 1517296)
-- Name: demande_crl_iddemande_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY demande_crl
    ADD CONSTRAINT demande_crl_iddemande_fkey FOREIGN KEY (iddemande) REFERENCES demande(iddemande);


--
-- TOC entry 4616 (class 2606 OID 1517301)
-- Name: demande_crl_idpersonne_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY demande_crl
    ADD CONSTRAINT demande_crl_idpersonne_fkey FOREIGN KEY (idpersonne) REFERENCES personne(idpersonne);


--
-- TOC entry 4618 (class 2606 OID 1517306)
-- Name: document_id_type_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY document
    ADD CONSTRAINT document_id_type_fkey FOREIGN KEY (id_type) REFERENCES type_document(id_type);


--
-- TOC entry 4619 (class 2606 OID 1517311)
-- Name: document_iddemande_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY document
    ADD CONSTRAINT document_iddemande_fkey FOREIGN KEY (iddemande) REFERENCES demande(iddemande);


--
-- TOC entry 4579 (class 2606 OID 1517316)
-- Name: fk_actedecessubsequente_actedece; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY actedecessubsequente
    ADD CONSTRAINT fk_actedecessubsequente_actedece FOREIGN KEY (idactedeces) REFERENCES actedeces(idactedeces);


--
-- TOC entry 4580 (class 2606 OID 1517321)
-- Name: fk_actedecessubsequente_operatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY actedecessubsequente
    ADD CONSTRAINT fk_actedecessubsequente_operatio FOREIGN KEY (idoperationsubsequente) REFERENCES operationsubsequente(idoperationsubsequente);


--
-- TOC entry 4581 (class 2606 OID 1517326)
-- Name: fk_acteprivesubsequente_actepriv; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY acteprivesubsequente
    ADD CONSTRAINT fk_acteprivesubsequente_actepriv FOREIGN KEY (idacteprive) REFERENCES acteprive(idacteprive);


--
-- TOC entry 4582 (class 2606 OID 1517331)
-- Name: fk_acteprivesubsequente_operatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY acteprivesubsequente
    ADD CONSTRAINT fk_acteprivesubsequente_operatio FOREIGN KEY (idoperationsubsequente) REFERENCES operationsubsequente(idoperationsubsequente);


--
-- TOC entry 4583 (class 2606 OID 1517336)
-- Name: fk_actepublicsubsequente_actepub; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY actepublicsubsequente
    ADD CONSTRAINT fk_actepublicsubsequente_actepub FOREIGN KEY (idactepublic) REFERENCES actepublic(idactepublic);


--
-- TOC entry 4584 (class 2606 OID 1517341)
-- Name: fk_actepublicsubsequente_operati; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY actepublicsubsequente
    ADD CONSTRAINT fk_actepublicsubsequente_operati FOREIGN KEY (idoperationsubsequente) REFERENCES operationsubsequente(idoperationsubsequente);


--
-- TOC entry 4612 (class 2606 OID 1517346)
-- Name: fk_anomalie; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY demande_anomalie
    ADD CONSTRAINT fk_anomalie FOREIGN KEY (idanomalie) REFERENCES anomalie(idanomalie);


--
-- TOC entry 4586 (class 2606 OID 1517351)
-- Name: fk_autrecharge; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY autrechargesparcelle_d
    ADD CONSTRAINT fk_autrecharge FOREIGN KEY (idcharge) REFERENCES autrecharge(idcharge);


--
-- TOC entry 4591 (class 2606 OID 1517356)
-- Name: fk_avoir_dmd_demande; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY avoir_dmd
    ADD CONSTRAINT fk_avoir_dmd_demande FOREIGN KEY (iddemande) REFERENCES demande(iddemande);


--
-- TOC entry 4627 (class 2606 OID 1517366)
-- Name: fk_batiment; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY impot_batiment
    ADD CONSTRAINT fk_batiment FOREIGN KEY (codebatiment) REFERENCES batiment(codebatiment);


--
-- TOC entry 4594 (class 2606 OID 1517371)
-- Name: fk_batiment_parcelle; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY batiment
    ADD CONSTRAINT fk_batiment_parcelle FOREIGN KEY (idparcelle) REFERENCES parcelle_d(gid);


--
-- TOC entry 4595 (class 2606 OID 1517381)
-- Name: fk_categorie; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY batiment
    ADD CONSTRAINT fk_categorie FOREIGN KEY (idcategorie) REFERENCES categorie(idcategorie);


--
-- TOC entry 4597 (class 2606 OID 1517386)
-- Name: fk_categorieforfaitaire_categori; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY categorieforfaitaire
    ADD CONSTRAINT fk_categorieforfaitaire_categori FOREIGN KEY (idcategorie) REFERENCES categorie(idcategorie);


--
-- TOC entry 4598 (class 2606 OID 1517391)
-- Name: fk_categorieforfaitaire_typeforf; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY categorieforfaitaire
    ADD CONSTRAINT fk_categorieforfaitaire_typeforf FOREIGN KEY (idforfaitaire) REFERENCES typeforfaitaire(idforfaitaire);


--
-- TOC entry 4636 (class 2606 OID 1517396)
-- Name: fk_certificat; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY parcelle_d
    ADD CONSTRAINT fk_certificat FOREIGN KEY (idcertificat) REFERENCES certificat(idcertificat);


--
-- TOC entry 4637 (class 2606 OID 1517401)
-- Name: fk_charge; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY parcelle_d
    ADD CONSTRAINT fk_charge FOREIGN KEY (idcharge) REFERENCES autrecharge(idcharge);


--
-- TOC entry 4600 (class 2606 OID 1517406)
-- Name: fk_classecategorieforfaitaire_ca; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY classecategorieforfaitaire
    ADD CONSTRAINT fk_classecategorieforfaitaire_ca FOREIGN KEY (idcategorie) REFERENCES categorie(idcategorie);


--
-- TOC entry 4601 (class 2606 OID 1517411)
-- Name: fk_classecategorieforfaitaire_cl; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY classecategorieforfaitaire
    ADD CONSTRAINT fk_classecategorieforfaitaire_cl FOREIGN KEY (idclasse) REFERENCES classe(idclasse);


--
-- TOC entry 4602 (class 2606 OID 1517416)
-- Name: fk_commune_district; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY commune
    ADD CONSTRAINT fk_commune_district FOREIGN KEY (iddistrict) REFERENCES district(iddistrict);


--
-- TOC entry 4650 (class 2606 OID 1517421)
-- Name: fk_commune_idcommune; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY projet_commune
    ADD CONSTRAINT fk_commune_idcommune FOREIGN KEY (idcommune) REFERENCES commune(idcommune) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4638 (class 2606 OID 1517426)
-- Name: fk_consistance; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY parcelle_d
    ADD CONSTRAINT fk_consistance FOREIGN KEY (id_consistance) REFERENCES consistance(idconsistance);


--
-- TOC entry 4596 (class 2606 OID 1517431)
-- Name: fk_consistance_batiment; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY batiment
    ADD CONSTRAINT fk_consistance_batiment FOREIGN KEY (idconsistance) REFERENCES consistance_batiment(id);


--
-- TOC entry 4603 (class 2606 OID 1517436)
-- Name: fk_consistanceforfaitaire_consis; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY consistanceforfaitaire
    ADD CONSTRAINT fk_consistanceforfaitaire_consis FOREIGN KEY (idconsistance) REFERENCES consistance(idconsistance);


--
-- TOC entry 4604 (class 2606 OID 1517441)
-- Name: fk_consistanceforfaitaire_typefo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY consistanceforfaitaire
    ADD CONSTRAINT fk_consistanceforfaitaire_typefo FOREIGN KEY (idforfaitaire) REFERENCES typeforfaitaire(idforfaitaire);


--
-- TOC entry 4605 (class 2606 OID 1517446)
-- Name: fk_consort; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY contribuable
    ADD CONSTRAINT fk_consort FOREIGN KEY (idcontribuableconsorts) REFERENCES contribuable(idcontribuable);


--
-- TOC entry 4606 (class 2606 OID 1517451)
-- Name: fk_consorts; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY contribuableconsorts
    ADD CONSTRAINT fk_consorts FOREIGN KEY (idconsort) REFERENCES contribuable(idcontribuable);


--
-- TOC entry 4607 (class 2606 OID 1517456)
-- Name: fk_contribuable; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY contribuableconsorts
    ADD CONSTRAINT fk_contribuable FOREIGN KEY (idcontribuable) REFERENCES contribuable(idcontribuable);


--
-- TOC entry 4639 (class 2606 OID 1517461)
-- Name: fk_contribuable; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY parcelle_d
    ADD CONSTRAINT fk_contribuable FOREIGN KEY (idcontribuable) REFERENCES contribuable(idcontribuable);


--
-- TOC entry 4610 (class 2606 OID 1517471)
-- Name: fk_decisionsubsequente_operation; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY decisionsubsequente
    ADD CONSTRAINT fk_decisionsubsequente_operation FOREIGN KEY (idoperationsubsequente) REFERENCES operationsubsequente(idoperationsubsequente);


--
-- TOC entry 4588 (class 2606 OID 1517476)
-- Name: fk_demande; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY avoir_demande
    ADD CONSTRAINT fk_demande FOREIGN KEY (iddemande) REFERENCES demande(iddemande);


--
-- TOC entry 4613 (class 2606 OID 1517481)
-- Name: fk_demande; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY demande_anomalie
    ADD CONSTRAINT fk_demande FOREIGN KEY (iddemande) REFERENCES demande(iddemande);


--
-- TOC entry 4611 (class 2606 OID 1517486)
-- Name: fk_demandecertificat_parcelle; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY demande
    ADD CONSTRAINT fk_demandecertificat_parcelle FOREIGN KEY (gid) REFERENCES parcelle_d(gid);


--
-- TOC entry 4599 (class 2606 OID 1517491)
-- Name: fk_fokontany; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY certificat
    ADD CONSTRAINT fk_fokontany FOREIGN KEY (idfokontany) REFERENCES fokontany(idfokontany);


--
-- TOC entry 4621 (class 2606 OID 1517496)
-- Name: fk_fokontany_commune; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY fokontany
    ADD CONSTRAINT fk_fokontany_commune FOREIGN KEY (idcommune) REFERENCES commune(idcommune);


--
-- TOC entry 4624 (class 2606 OID 1517501)
-- Name: fk_hameau_fokontany; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY hameau
    ADD CONSTRAINT fk_hameau_fokontany FOREIGN KEY (idfokontany) REFERENCES fokontany(idfokontany);


--
-- TOC entry 4640 (class 2606 OID 1517511)
-- Name: fk_hypotheque; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY parcelle_d
    ADD CONSTRAINT fk_hypotheque FOREIGN KEY (idhypotheque) REFERENCES hypotheque(idhypotheque);


--
-- TOC entry 4625 (class 2606 OID 1517516)
-- Name: fk_hypotheque; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY hypothequeparcelle_d
    ADD CONSTRAINT fk_hypotheque FOREIGN KEY (idhypotheque) REFERENCES hypotheque(idhypotheque);


--
-- TOC entry 4641 (class 2606 OID 1517521)
-- Name: fk_idcommune; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY parcelle_d
    ADD CONSTRAINT fk_idcommune FOREIGN KEY (id_commune) REFERENCES commune(idcommune);


--
-- TOC entry 4630 (class 2606 OID 1517526)
-- Name: fk_impotparcelle_impot; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY impotparcelle
    ADD CONSTRAINT fk_impotparcelle_impot FOREIGN KEY (idimpot) REFERENCES impot(idimpot);


--
-- TOC entry 4631 (class 2606 OID 1517531)
-- Name: fk_impotparcelle_parcelle; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY impotparcelle
    ADD CONSTRAINT fk_impotparcelle_parcelle FOREIGN KEY (idparcelle) REFERENCES parcelle_d(gid);


--
-- TOC entry 4632 (class 2606 OID 1517536)
-- Name: fk_journal_utilisateur; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY journal
    ADD CONSTRAINT fk_journal_utilisateur FOREIGN KEY (idutilisateur) REFERENCES utilisateur(idutilisateur);


--
-- TOC entry 4645 (class 2606 OID 1517541)
-- Name: fk_menage; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY personne_menage
    ADD CONSTRAINT fk_menage FOREIGN KEY (id_menage) REFERENCES menage(id_menage) NOT VALID;


--
-- TOC entry 4635 (class 2606 OID 1517556)
-- Name: fk_oppositions_demande; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY oppositions
    ADD CONSTRAINT fk_oppositions_demande FOREIGN KEY (iddemande) REFERENCES demande(iddemande);


--
-- TOC entry 4633 (class 2606 OID 1517561)
-- Name: fk_parcelle; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY limitesparcelle
    ADD CONSTRAINT fk_parcelle FOREIGN KEY (idparcelle) REFERENCES parcelle_d(gid);


--
-- TOC entry 4657 (class 2606 OID 1517566)
-- Name: fk_parcelle; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY servitudeparcelle_d
    ADD CONSTRAINT fk_parcelle FOREIGN KEY (idparcelle) REFERENCES parcelle_d(gid);


--
-- TOC entry 4626 (class 2606 OID 1517571)
-- Name: fk_parcelle; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY hypothequeparcelle_d
    ADD CONSTRAINT fk_parcelle FOREIGN KEY (idparcelle) REFERENCES parcelle_d(gid);


--
-- TOC entry 4587 (class 2606 OID 1517576)
-- Name: fk_parcelle; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY autrechargesparcelle_d
    ADD CONSTRAINT fk_parcelle FOREIGN KEY (idparcelle) REFERENCES parcelle_d(gid);


--
-- TOC entry 4653 (class 2606 OID 1517581)
-- Name: fk_parcelle; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY proprietaireparcelle
    ADD CONSTRAINT fk_parcelle FOREIGN KEY (idparcelle) REFERENCES parcelle_d(gid);


--
-- TOC entry 4608 (class 2606 OID 1517586)
-- Name: fk_parcelle; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY contribuables_parcelle
    ADD CONSTRAINT fk_parcelle FOREIGN KEY (idparcelle) REFERENCES parcelle_d(gid);


--
-- TOC entry 4642 (class 2606 OID 1517596)
-- Name: fk_parcelle_classe; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY parcelle_d
    ADD CONSTRAINT fk_parcelle_classe FOREIGN KEY (idclasse) REFERENCES classe(idclasse);


--
-- TOC entry 4648 (class 2606 OID 1517611)
-- Name: fk_parcelle_d; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY personnemoraleparcelle_d
    ADD CONSTRAINT fk_parcelle_d FOREIGN KEY (idparcelle) REFERENCES parcelle_d(gid);


--
-- TOC entry 4589 (class 2606 OID 1517616)
-- Name: fk_parcelle_d; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY avoir_demande
    ADD CONSTRAINT fk_parcelle_d FOREIGN KEY (idparcelle) REFERENCES parcelle_d(gid);


--
-- TOC entry 4643 (class 2606 OID 1517621)
-- Name: fk_parcelle_d_categorie; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY parcelle_d
    ADD CONSTRAINT fk_parcelle_d_categorie FOREIGN KEY (idcategorie) REFERENCES categorie(idcategorie);


--
-- TOC entry 4629 (class 2606 OID 1517631)
-- Name: fk_parcelle_impot; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY impot_parcelle
    ADD CONSTRAINT fk_parcelle_impot FOREIGN KEY (idparcelle) REFERENCES parcelle_d(gid);


--
-- TOC entry 4649 (class 2606 OID 1517636)
-- Name: fk_persmorale; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY personnemoraleparcelle_d
    ADD CONSTRAINT fk_persmorale FOREIGN KEY (idpersonne) REFERENCES personnemorale(idpersonnemorale);


--
-- TOC entry 4590 (class 2606 OID 1517646)
-- Name: fk_personne; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY avoir_demande
    ADD CONSTRAINT fk_personne FOREIGN KEY (idpersonne) REFERENCES personne(idpersonne);


--
-- TOC entry 4654 (class 2606 OID 1517651)
-- Name: fk_personne; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY proprietaireparcelle
    ADD CONSTRAINT fk_personne FOREIGN KEY (idpersonne) REFERENCES personne(idpersonne);


--
-- TOC entry 4609 (class 2606 OID 1517656)
-- Name: fk_personne; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY contribuables_parcelle
    ADD CONSTRAINT fk_personne FOREIGN KEY (idpersonne) REFERENCES personne(idpersonne);


--
-- TOC entry 4628 (class 2606 OID 1517661)
-- Name: fk_personne; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY impot_contribuable
    ADD CONSTRAINT fk_personne FOREIGN KEY (idpersonne) REFERENCES personne(idpersonne);


--
-- TOC entry 4646 (class 2606 OID 1517666)
-- Name: fk_personne; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY personne_menage
    ADD CONSTRAINT fk_personne FOREIGN KEY (idpersonne) REFERENCES personne(idpersonne) NOT VALID;


--
-- TOC entry 4620 (class 2606 OID 1517671)
-- Name: fk_personne; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY fi_paiement_impot
    ADD CONSTRAINT fk_personne FOREIGN KEY (idpersonne) REFERENCES personne(idpersonne);


--
-- TOC entry 4592 (class 2606 OID 1517676)
-- Name: fk_personne_a; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY avoirconjoint
    ADD CONSTRAINT fk_personne_a FOREIGN KEY (idconjoint_a) REFERENCES personne(idpersonne);


--
-- TOC entry 4593 (class 2606 OID 1517681)
-- Name: fk_personne_b; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY avoirconjoint
    ADD CONSTRAINT fk_personne_b FOREIGN KEY (idconjoint_b) REFERENCES personne(idpersonne);


--
-- TOC entry 4634 (class 2606 OID 1517696)
-- Name: fk_pointscardinaux; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY limitesparcelle
    ADD CONSTRAINT fk_pointscardinaux FOREIGN KEY (idpointscardinaux) REFERENCES pointscardinaux(idpointscardinaux);


--
-- TOC entry 4651 (class 2606 OID 1517701)
-- Name: fk_projet_idprojet; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY projet_commune
    ADD CONSTRAINT fk_projet_idprojet FOREIGN KEY (idprojet) REFERENCES projet(idprojet) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4617 (class 2606 OID 1517706)
-- Name: fk_region; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY district
    ADD CONSTRAINT fk_region FOREIGN KEY (idregion) REFERENCES region(idregion) NOT VALID;


--
-- TOC entry 4644 (class 2606 OID 1517711)
-- Name: fk_servitude; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY parcelle_d
    ADD CONSTRAINT fk_servitude FOREIGN KEY (idservitude) REFERENCES servitude(idservitude);


--
-- TOC entry 4658 (class 2606 OID 1517716)
-- Name: fk_servitude; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY servitudeparcelle_d
    ADD CONSTRAINT fk_servitude FOREIGN KEY (idservitude) REFERENCES servitude(idservitude);


--
-- TOC entry 4655 (class 2606 OID 1517721)
-- Name: fk_servitudebeneficiaire_benefic; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY servitudebeneficiaire
    ADD CONSTRAINT fk_servitudebeneficiaire_benefic FOREIGN KEY (idbeneficiaire) REFERENCES beneficiaire(idbeneficiaire);


--
-- TOC entry 4656 (class 2606 OID 1517726)
-- Name: fk_servitudebeneficiaire_serv; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY servitudebeneficiaire
    ADD CONSTRAINT fk_servitudebeneficiaire_serv FOREIGN KEY (idservitude) REFERENCES servitude(idservitude);


--
-- TOC entry 4659 (class 2606 OID 1517731)
-- Name: fk_servitudeparcellegrevees_parc; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY servitudeparcellegrevees
    ADD CONSTRAINT fk_servitudeparcellegrevees_parc FOREIGN KEY (idparcellegrevees) REFERENCES parcellegrevees(idparcellegrevees);


--
-- TOC entry 4660 (class 2606 OID 1517736)
-- Name: fk_servitudeparcellegrevees_serv; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY servitudeparcellegrevees
    ADD CONSTRAINT fk_servitudeparcellegrevees_serv FOREIGN KEY (idservitude) REFERENCES servitude(idservitude);


--
-- TOC entry 4647 (class 2606 OID 1517746)
-- Name: fk_type; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY personnemorale
    ADD CONSTRAINT fk_type FOREIGN KEY (idtype) REFERENCES typepersonnemorale(idtype);


--
-- TOC entry 4585 (class 2606 OID 1517751)
-- Name: fk_type_anomalie; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY anomalie
    ADD CONSTRAINT fk_type_anomalie FOREIGN KEY (id_type_anomalie) REFERENCES type_anomalie(id_type_anomalie);


--
-- TOC entry 4622 (class 2606 OID 1517766)
-- Name: groupe_acces_acces_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY groupe_acces
    ADD CONSTRAINT groupe_acces_acces_id_fkey FOREIGN KEY (acces_id) REFERENCES acces(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4623 (class 2606 OID 1517771)
-- Name: groupe_acces_groupe_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY groupe_acces
    ADD CONSTRAINT groupe_acces_groupe_id_fkey FOREIGN KEY (groupe_id) REFERENCES groupe(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4652 (class 2606 OID 1517776)
-- Name: projetcouche_idprojet_commune_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY projetcouche
    ADD CONSTRAINT projetcouche_idprojet_commune_fkey FOREIGN KEY (idprojet_commune) REFERENCES projet_commune(idprojet_commune) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4661 (class 2606 OID 1517781)
-- Name: utilisateur_groupe_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY utilisateur
    ADD CONSTRAINT utilisateur_groupe_id_fkey FOREIGN KEY (groupe_id) REFERENCES groupe(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 5156 (class 0 OID 0)
-- Dependencies: 9
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2025-04-28 13:16:31

--
-- PostgreSQL database dump complete
--

