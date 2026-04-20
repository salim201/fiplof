--
-- PostgreSQL database dump
--

-- Dumped from database version 9.3.5
-- Dumped by pg_dump version 9.3.5
-- Started on 2019-03-09 19:12:53

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 352 (class 1259 OID 34653)
-- Name: voisins; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--
CREATE SEQUENCE public.voisins_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 2147483647
  START 10
  CACHE 1;
ALTER TABLE public.voisins_id_seq
  OWNER TO postgres;
  
CREATE TABLE voisins (
    idvoisin bigint DEFAULT nextval('voisins_id_seq'::regclass) NOT NULL,
    nom character varying(250),
    prenom character varying(250),
    adresse character varying(250)
);


ALTER TABLE public.voisins OWNER TO postgres;

--
-- TOC entry 3936 (class 0 OID 34653)
-- Dependencies: 352
-- Data for Name: voisins; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3818 (class 2606 OID 34663)
-- Name: pk_voisins; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY voisins
    ADD CONSTRAINT pk_voisins PRIMARY KEY (idvoisin);


-- Completed on 2019-03-09 19:12:54

--
-- PostgreSQL database dump complete
--

