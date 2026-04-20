--
-- PostgreSQL database dump
--

-- Dumped from database version 9.3.5
-- Dumped by pg_dump version 9.3.5
-- Started on 2018-05-08 13:22:41

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
-- TOC entry 366 (class 1259 OID 69658)
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
    gid integer
);


ALTER TABLE public.oppositions OWNER TO postgres;

--
-- TOC entry 3877 (class 0 OID 69658)
-- Dependencies: 366
-- Data for Name: oppositions; Type: TABLE DATA; Schema: public; Owner: postgres
--


--
-- TOC entry 3759 (class 2606 OID 69667)
-- Name: pk_oppositions; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY oppositions
    ADD CONSTRAINT pk_oppositions PRIMARY KEY (idopposition);


--
-- TOC entry 3757 (class 1259 OID 69669)
-- Name: fki_demande; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_demande ON oppositions USING btree (iddemande);


--
-- TOC entry 3760 (class 2606 OID 69677)
-- Name: fk_oppositions_demande; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY oppositions
    ADD CONSTRAINT fk_oppositions_demande FOREIGN KEY (iddemande) REFERENCES demande(iddemande);


-- Completed on 2018-05-08 13:22:41

--
-- PostgreSQL database dump complete
--

