--
-- PostgreSQL database dump
--

-- Dumped from database version 9.3.5
-- Dumped by pg_dump version 9.3.5
-- Started on 2019-03-09 19:10:13

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
-- TOC entry 354 (class 1259 OID 34664)
-- Name: voisinparcelle; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE SEQUENCE public.voisinparcelle_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 2147483647
  START 10
  CACHE 1;
ALTER TABLE public.voisinparcelle_id_seq
  OWNER TO postgres;


CREATE TABLE voisinparcelle (
    idvp bigint DEFAULT nextval('voisinparcelle_id_seq'::regclass) NOT NULL,
    idvoisin bigint NOT NULL,
    idpacelle bigint NOT NULL,
    iddemande bigint NOT NULL
);


ALTER TABLE public.voisinparcelle OWNER TO postgres;




--
-- TOC entry 3936 (class 0 OID 34664)
-- Dependencies: 354
-- Data for Name: voisinparcelle; Type: TABLE DATA; Schema: public; Owner: postgres
--

--
-- TOC entry 3818 (class 2606 OID 34671)
-- Name: pk_voisinparcelle; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY voisinparcelle
    ADD CONSTRAINT pk_voisinparcelle PRIMARY KEY (idvp);


-- Completed on 2019-03-09 19:10:14

--
-- PostgreSQL database dump complete
--

