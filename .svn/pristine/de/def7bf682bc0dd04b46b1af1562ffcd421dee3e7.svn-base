--
-- PostgreSQL database dump
--

-- Dumped from database version 9.3.5
-- Dumped by pg_dump version 9.3.5
-- Started on 2018-05-09 21:55:04

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
-- TOC entry 287 (class 1259 OID 64996)
-- Name: demandeur_d; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE demandeur_d (
    iddemandeur integer NOT NULL,
    nom character varying(250),
    prenom character varying(250)
);


ALTER TABLE public.demandeur_d OWNER TO postgres;

--
-- TOC entry 288 (class 1259 OID 65002)
-- Name: demandeur_d_id_seq1; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE demandeur_d_id_seq1
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.demandeur_d_id_seq1 OWNER TO postgres;

--
-- TOC entry 3881 (class 0 OID 0)
-- Dependencies: 288
-- Name: demandeur_d_id_seq1; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE demandeur_d_id_seq1 OWNED BY demandeur_d.iddemandeur;


--
-- TOC entry 3756 (class 2604 OID 66854)
-- Name: iddemandeur; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY demandeur_d ALTER COLUMN iddemandeur SET DEFAULT nextval('demandeur_d_id_seq1'::regclass);


--
-- TOC entry 3875 (class 0 OID 64996)
-- Dependencies: 287
-- Data for Name: demandeur_d; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3882 (class 0 OID 0)
-- Dependencies: 288
-- Name: demandeur_d_id_seq1; Type: SEQUENCE SET; Schema: public; Owner: postgres
--




--
-- TOC entry 3758 (class 2606 OID 66344)
-- Name: demandeur_d_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY demandeur_d
    ADD CONSTRAINT demandeur_d_pkey PRIMARY KEY (iddemandeur);


-- Completed on 2018-05-09 21:55:05

--
-- PostgreSQL database dump complete
--

