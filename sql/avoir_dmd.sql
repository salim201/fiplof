--
-- PostgreSQL database dump
--

-- Dumped from database version 9.3.5
-- Dumped by pg_dump version 9.3.5
-- Started on 2018-05-08 13:15:24

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
-- TOC entry 368 (class 1259 OID 69670)
-- Name: avoir_dmd; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE avoir_dmd (
    iddemandeur integer NOT NULL,
    iddemande integer NOT NULL,
    gid integer
);


ALTER TABLE public.avoir_dmd OWNER TO postgres;

--
-- TOC entry 3878 (class 0 OID 69670)
-- Dependencies: 368
-- Data for Name: avoir_dmd; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3759 (class 2606 OID 69674)
-- Name: pk_avoir_dmd; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY avoir_dmd
    ADD CONSTRAINT pk_avoir_dmd PRIMARY KEY (iddemande, iddemandeur);


--
-- TOC entry 3756 (class 1259 OID 69675)
-- Name: fki_avoir_dmd_iddemande; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_avoir_dmd_iddemande ON avoir_dmd USING btree (iddemande);


--
-- TOC entry 3757 (class 1259 OID 69676)
-- Name: fki_avoir_dmd_iddemandeur; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_avoir_dmd_iddemandeur ON avoir_dmd USING btree (iddemandeur);


--
-- TOC entry 3761 (class 2606 OID 69682)
-- Name: fk_avoir_dmd_demande; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY avoir_dmd
    ADD CONSTRAINT fk_avoir_dmd_demande FOREIGN KEY (iddemande) REFERENCES demande(iddemande);


--
-- TOC entry 3760 (class 2606 OID 69687)
-- Name: fk_avoir_dmd_demandeurd_d; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY avoir_dmd
    ADD CONSTRAINT fk_avoir_dmd_demandeurd_d FOREIGN KEY (iddemandeur) REFERENCES demandeur_d(iddemandeur);


-- Completed on 2018-05-08 13:15:24

--
-- PostgreSQL database dump complete
--

