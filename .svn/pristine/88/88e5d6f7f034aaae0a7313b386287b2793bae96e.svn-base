UPDATE public.groupe_acces SET autorise = TRUE WHERE groupe_id = 14 AND acces_id = 
(SELECT id from public.acces WHERE nom = 'OPERATIONS_SUBSEQUENTES');
INSERT INTO groupe_acces VALUES (581, 14, 86, true);
SELECT pg_catalog.setval('groupe_acces_id_seq', 581, true);