--
-- PostgreSQL database dump
--

-- Dumped from database version 9.3.5
-- Dumped by pg_dump version 9.3.5
-- Started on 2018-08-19 20:35:48

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
-- TOC entry 382 (class 1259 OID 160165)
-- Name: operationsub; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE SEQUENCE public.operationsub_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 18845
  CACHE 1;
ALTER TABLE public.operationsub_id_seq
  OWNER TO postgres;


CREATE TABLE operationsub (
    id bigint DEFAULT nextval('operationsub_id_seq'::regclass) NOT NULL,
    typeacte bigint,
    idacte bigint,
    idcf character varying(250),
    datedepot date,
    dateinscription date,
    cout real,
    cout2 real
);


ALTER TABLE public.operationsub OWNER TO postgres;

--
-- TOC entry 3915 (class 0 OID 160165)
-- Dependencies: 382
-- Data for Name: operationsub; Type: TABLE DATA; Schema: public; Owner: postgres
--


--
-- TOC entry 3798 (class 2606 OID 160289)
-- Name: operationsub_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY operationsub
    ADD CONSTRAINT operationsub_pkey PRIMARY KEY (id);


-- Completed on 2018-08-19 20:35:49

--
-- PostgreSQL database dump complete
--

