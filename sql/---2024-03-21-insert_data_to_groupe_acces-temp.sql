--
-- PostgreSQL database dump
--

-- Dumped from database version 9.3.5
-- Dumped by pg_dump version 9.3.5
-- Started on 2024-05-23 16:00:09

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
-- TOC entry 276 (class 1259 OID 1281377)
-- Name: groupe_acces; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE groupe_acces (
    id bigint NOT NULL,
    groupe_id bigint,
    acces_id bigint,
    autorise boolean
);


ALTER TABLE public.groupe_acces OWNER TO postgres;

--
-- TOC entry 277 (class 1259 OID 1281380)
-- Name: groupe_acces_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE groupe_acces_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.groupe_acces_id_seq OWNER TO postgres;

--
-- TOC entry 4078 (class 0 OID 0)
-- Dependencies: 277
-- Name: groupe_acces_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE groupe_acces_id_seq OWNED BY groupe_acces.id;


--
-- TOC entry 3944 (class 2604 OID 1281838)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY groupe_acces ALTER COLUMN id SET DEFAULT nextval('groupe_acces_id_seq'::regclass);


--
-- TOC entry 4072 (class 0 OID 1281377)
-- Dependencies: 276
-- Data for Name: groupe_acces; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY groupe_acces (id, groupe_id, acces_id, autorise) FROM stdin;
188	10	3	t
189	10	4	t
22	5	2	t
23	5	3	f
24	5	4	f
135	5	35	f
136	5	36	f
137	5	37	f
144	5	75	f
30	5	6	t
31	5	7	f
32	5	8	f
124	5	21	t
125	5	23	f
138	5	40	f
139	5	41	f
33	5	9	f
34	5	10	f
35	5	11	f
36	5	12	f
37	5	13	f
38	5	14	f
53	5	15	f
54	5	16	f
55	5	17	f
56	5	18	f
57	5	19	f
126	5	24	f
127	5	25	f
128	5	26	f
129	5	27	f
130	5	28	f
131	5	29	t
132	5	30	f
145	5	42	f
141	5	34	f
142	5	38	f
143	5	39	f
146	5	43	t
190	10	35	t
191	10	36	t
192	10	37	t
193	10	75	t
194	10	5	t
195	10	6	t
196	10	7	f
198	10	21	t
199	10	23	f
200	10	40	t
201	10	41	f
202	10	9	t
203	10	10	t
204	10	11	t
205	10	12	t
206	10	13	t
207	10	14	t
208	10	15	t
209	10	16	t
210	10	17	t
211	10	18	t
213	10	24	t
214	10	25	t
215	10	26	t
216	10	27	t
217	10	28	t
218	10	29	t
219	10	30	t
220	10	42	t
221	10	33	t
222	10	34	t
223	10	38	t
224	10	39	t
225	10	43	t
226	10	76	t
228	10	45	f
229	10	46	f
230	10	47	t
231	10	48	t
232	10	49	t
233	10	50	t
234	10	51	t
235	10	52	t
236	10	53	t
237	10	54	f
238	10	55	t
239	10	56	t
21	5	1	f
29	5	5	f
140	5	33	f
147	5	76	f
148	5	77	f
149	5	45	f
151	5	47	f
152	5	48	f
153	5	49	f
154	5	50	f
155	5	51	f
156	5	52	f
157	5	53	f
158	5	54	f
159	5	55	f
160	5	56	f
161	5	57	f
162	5	58	f
163	5	59	f
164	5	60	f
166	5	62	f
167	5	63	f
168	5	64	f
169	5	65	t
170	5	66	f
171	5	67	f
172	5	68	f
173	5	69	t
174	5	70	f
175	5	71	f
176	5	72	f
177	5	73	f
178	5	74	f
179	5	78	f
181	5	83	f
182	5	80	f
183	5	81	f
184	5	82	f
185	5	84	f
187	10	2	t
242	10	59	t
243	10	60	t
244	10	61	t
245	10	62	t
246	10	63	t
247	10	64	t
248	10	65	t
249	10	66	t
250	10	67	t
251	10	68	t
252	10	69	t
253	10	70	f
254	10	71	f
255	10	72	f
256	10	73	f
257	10	74	f
258	10	78	f
259	10	79	f
260	10	83	f
261	10	80	f
262	10	81	f
263	10	82	f
264	10	84	t
265	11	1	t
266	11	2	t
267	11	3	t
268	11	4	t
269	11	35	t
270	11	36	t
271	11	37	t
272	11	75	t
273	11	5	t
274	11	6	t
275	11	7	t
276	11	8	t
277	11	21	t
278	11	23	f
279	11	40	t
280	11	41	f
281	11	9	t
282	11	10	t
283	11	11	t
284	11	12	t
285	11	13	t
286	11	14	t
287	11	15	t
288	11	16	t
289	11	17	t
290	11	18	t
291	11	19	t
292	11	24	f
293	11	25	f
294	11	26	f
295	11	27	f
296	11	28	f
297	11	29	f
298	11	30	f
299	11	42	f
300	11	33	t
301	11	34	t
302	11	38	t
303	11	39	t
304	11	43	t
305	11	76	t
306	11	77	t
307	11	45	t
308	11	46	t
309	11	47	t
310	11	48	t
311	11	49	t
312	11	50	t
313	11	51	t
314	11	52	f
315	11	53	t
316	11	54	f
317	11	55	t
318	11	56	t
319	11	57	t
320	11	58	t
321	11	59	t
322	11	60	t
323	11	61	t
324	11	62	t
325	11	63	t
326	11	64	t
327	11	65	t
328	11	66	t
329	11	67	t
330	11	68	t
331	11	69	t
332	11	70	f
333	11	71	t
334	11	72	t
335	11	73	t
336	11	74	f
337	11	78	t
338	11	79	t
339	11	83	f
340	11	80	t
341	11	81	t
342	11	82	t
343	11	84	f
345	12	2	t
346	12	3	t
212	10	19	t
227	10	77	t
241	10	58	f
347	12	4	t
348	12	35	t
349	12	36	t
350	12	37	t
351	12	75	t
352	12	5	t
353	12	6	t
354	12	7	t
355	12	8	t
356	12	21	t
357	12	23	f
358	12	40	t
360	12	9	t
361	12	10	t
362	12	11	t
363	12	12	t
364	12	13	t
344	12	1	t
197	10	8	f
368	12	17	t
369	12	18	t
370	12	19	t
371	12	24	t
372	12	25	t
373	12	26	t
427	13	35	f
428	13	36	f
429	13	37	f
430	13	75	f
431	13	5	f
432	13	6	t
433	13	7	f
434	13	8	f
435	13	21	f
436	13	23	f
437	13	40	f
438	13	41	f
439	13	9	f
440	13	10	f
442	13	12	f
443	13	13	f
444	13	14	f
445	13	15	f
446	13	16	f
447	13	17	f
448	13	18	f
449	13	19	f
450	13	24	f
451	13	25	f
452	13	26	f
453	13	27	f
454	13	28	f
455	13	29	f
457	13	42	f
458	13	33	f
459	13	34	f
460	13	38	f
461	13	39	f
462	13	43	t
463	13	76	f
464	13	77	t
465	13	45	f
466	13	46	f
467	13	47	f
468	13	48	t
469	13	49	f
470	13	50	f
472	13	52	f
473	13	53	f
474	13	54	f
475	13	55	t
476	13	56	f
477	13	57	f
478	13	58	f
479	13	59	f
480	13	60	f
481	13	61	f
482	13	62	f
483	13	63	f
484	13	64	f
485	13	65	f
487	13	67	f
488	13	68	f
489	13	69	t
490	13	70	t
491	13	71	f
492	13	72	f
493	13	73	t
494	13	74	t
495	13	78	f
496	13	79	f
497	13	83	f
498	13	80	t
499	13	81	t
500	13	82	t
367	12	16	t
374	12	27	t
375	12	28	t
376	12	29	t
377	12	30	t
378	12	42	t
379	12	33	t
380	12	34	t
381	12	38	t
382	12	39	t
383	12	43	t
384	12	76	t
385	12	77	t
387	12	46	t
388	12	47	t
389	12	48	t
390	12	49	t
391	12	50	t
392	12	51	t
393	12	52	t
394	12	53	t
395	12	54	t
396	12	55	t
397	12	56	t
398	12	57	t
399	12	58	t
400	12	59	t
402	12	61	t
403	12	62	t
404	12	63	t
405	12	64	t
406	12	65	t
407	12	66	t
408	12	67	t
409	12	68	t
410	12	69	t
411	12	70	t
412	12	71	t
413	12	72	t
414	12	73	t
415	12	74	t
417	12	79	t
418	12	83	f
419	12	80	t
420	12	81	t
421	12	82	t
422	12	84	f
424	13	2	t
366	12	15	t
425	13	3	f
503	14	2	t
504	14	3	t
506	14	35	t
507	14	36	t
508	14	37	t
523	14	14	t
524	14	15	t
525	14	16	t
526	14	17	t
527	14	18	t
528	14	19	t
529	14	24	t
530	14	25	f
531	14	26	f
532	14	27	f
533	14	28	f
535	14	30	f
536	14	42	f
537	14	33	t
538	14	34	t
539	14	38	t
540	14	39	t
541	14	43	t
542	14	76	t
543	14	77	t
544	14	45	t
545	14	46	t
150	5	46	f
165	5	61	f
180	5	79	f
186	10	1	t
240	10	57	t
359	12	41	f
365	12	14	t
386	12	45	t
401	12	60	t
416	12	78	t
423	13	1	f
426	13	4	f
441	13	11	f
456	13	30	f
471	13	51	f
486	13	66	f
501	13	84	f
502	14	1	t
505	14	4	t
509	14	75	t
510	14	5	t
511	14	6	t
512	14	7	t
513	14	8	t
514	14	21	t
515	14	23	f
516	14	40	t
517	14	41	f
518	14	9	t
519	14	10	t
520	14	11	t
521	14	12	t
522	14	13	t
534	14	29	f
546	14	47	t
547	14	48	t
548	14	49	t
549	14	50	t
550	14	51	t
551	14	52	f
552	14	53	t
553	14	54	f
554	14	55	t
555	14	56	t
556	14	57	t
557	14	58	f
558	14	59	t
559	14	60	t
560	14	61	t
561	14	62	t
562	14	63	t
563	14	64	t
564	14	65	f
565	14	66	t
566	14	67	t
567	14	68	t
568	14	69	t
569	14	70	t
570	14	71	t
571	14	72	t
572	14	73	t
573	14	74	t
574	14	78	t
575	14	79	t
576	14	83	t
577	14	80	t
578	14	81	t
579	14	82	t
580	14	84	f
\.


--
-- TOC entry 4079 (class 0 OID 0)
-- Dependencies: 277
-- Name: groupe_acces_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('groupe_acces_id_seq', 580, true);


--
-- TOC entry 3946 (class 2606 OID 1281891)
-- Name: groupe_acces_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY groupe_acces
    ADD CONSTRAINT groupe_acces_pkey PRIMARY KEY (id);


--
-- TOC entry 3947 (class 2606 OID 1282698)
-- Name: groupe_acces_acces_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY groupe_acces
    ADD CONSTRAINT groupe_acces_acces_id_fkey FOREIGN KEY (acces_id) REFERENCES acces(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3948 (class 2606 OID 1282703)
-- Name: groupe_acces_groupe_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY groupe_acces
    ADD CONSTRAINT groupe_acces_groupe_id_fkey FOREIGN KEY (groupe_id) REFERENCES groupe(id) ON UPDATE CASCADE ON DELETE CASCADE;


-- Completed on 2024-05-23 16:00:09

--
-- PostgreSQL database dump complete
--

