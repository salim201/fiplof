--
-- PostgreSQL database dump
--

-- Dumped from database version 9.3.5
-- Dumped by pg_dump version 9.3.5
-- Started on 2018-06-03 01:18:06

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

CREATE SEQUENCE public.typeoperationsubsequente_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 11
  CACHE 1;
ALTER TABLE public.typeoperationsubsequente_id_seq
  OWNER TO postgres;

--
-- TOC entry 371 (class 1259 OID 86996)
-- Name: typeoperationsubsequente; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE typeoperationsubsequente (
    idtype integer DEFAULT nextval('typeoperationsubsequente_id_seq'::regclass) NOT NULL,
    libelleoperation character varying(250)
);


ALTER TABLE public.typeoperationsubsequente OWNER TO postgres;

--
-- TOC entry 3886 (class 0 OID 86996)
-- Dependencies: 371
-- Data for Name: typeoperationsubsequente; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3769 (class 2606 OID 87003)
-- Name: pk_typeoperationsubsequente; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY typeoperationsubsequente
    ADD CONSTRAINT pk_typeoperationsubsequente PRIMARY KEY (idtype);


-- Completed on 2018-06-03 01:18:07

--
-- PostgreSQL database dump complete
--

