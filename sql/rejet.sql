--
-- PostgreSQL database dump
--

-- Dumped from database version 9.3.5
-- Dumped by pg_dump version 9.3.5
-- Started on 2018-05-12 09:25:05

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
-- TOC entry 370 (class 1259 OID 70578)
-- Name: rejet; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE rejet (
    idrejet integer DEFAULT nextval('rejet_id_seq'::regclass) NOT NULL,
    typerejet character varying(250),
    daterejet date,
    motifrejet character varying(250)
);


ALTER TABLE public.rejet OWNER TO postgres;

--
-- TOC entry 3881 (class 0 OID 70578)
-- Dependencies: 370
-- Data for Name: rejet; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY rejet (idrejet, typerejet, daterejet, motifrejet) FROM stdin;
\.


--
-- TOC entry 3764 (class 2606 OID 70586)
-- Name: pk_rejet; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY rejet
    ADD CONSTRAINT pk_rejet PRIMARY KEY (idrejet);


-- Completed on 2018-05-12 09:25:06

--
-- PostgreSQL database dump complete
--

