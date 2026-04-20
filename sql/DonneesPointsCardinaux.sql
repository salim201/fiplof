--
-- PostgreSQL database dump
--

-- Dumped from database version 9.3.5
-- Dumped by pg_dump version 9.3.5
-- Started on 2018-09-01 13:05:46

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

--
-- TOC entry 3906 (class 0 OID 25508)
-- Dependencies: 343
-- Data for Name: pointscardinaux; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY pointscardinaux (idpointscardinaux, "position", fanondroana) FROM stdin;
1	Nord	Avaratra
2	Sud	Atsimo
4	Ouest	Andrefana
3	Est	Atsinanana
\.


--
-- TOC entry 3912 (class 0 OID 0)
-- Dependencies: 344
-- Name: pointscardinaux_idpointscardinaux_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('pointscardinaux_idpointscardinaux_seq', 4, true);


-- Completed on 2018-09-01 13:05:46

--
-- PostgreSQL database dump complete
--

