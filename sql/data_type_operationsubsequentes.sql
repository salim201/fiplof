--
-- PostgreSQL database dump
--

-- Dumped from database version 9.3.5
-- Dumped by pg_dump version 9.3.5
-- Started on 2018-06-09 20:46:33

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
-- TOC entry 372 (class 1259 OID 56500)
-- Name: typeoperationsubsequente; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE typeoperationsubsequente (
    idtype integer DEFAULT nextval('typeoperationsubsequente_id_seq'::regclass) NOT NULL,
    libelleoperation character varying(250)
);


ALTER TABLE public.typeoperationsubsequente OWNER TO postgres;

--
-- TOC entry 3894 (class 0 OID 56500)
-- Dependencies: 372
-- Data for Name: typeoperationsubsequente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY typeoperationsubsequente (idtype, libelleoperation) FROM stdin;
1	Mutation par decès
2	Vente totale
3	Vente partielle avec distraction de parcelle
4	Vente partielle en restant dans l'indivision
5	Donation totale d'un certificat
6	Donation partielle avec distraction
7	Donation partielle en restant dans l'indivision
8	Echange totale de deux certificats
9	Partage des certificats sans morcellement
10	Partage avec distraction
11	Fusion des certificats
\.


--
-- TOC entry 3777 (class 2606 OID 56505)
-- Name: pk_typeoperationsubsequente; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY typeoperationsubsequente
    ADD CONSTRAINT pk_typeoperationsubsequente PRIMARY KEY (idtype);


-- Completed on 2018-06-09 20:46:34

--
-- PostgreSQL database dump complete
--

