

--INSERT INTO groupe VALUES (1, 'Admin', 'Administrateur de l''application');
--INSERT INTO groupe VALUES (5, 'Responsable Commune', ' Responsable des communes');
INSERT INTO groupe VALUES (10, 'Guichet Foncier', ' Agent Guichet Foncier');
INSERT INTO groupe VALUES (11, 'Assistants Techniques', 'Assistants Techniques ');
INSERT INTO groupe VALUES (12, 'Formateur', ' Formateur');
INSERT INTO groupe VALUES (13, 'Guichet Unique (TOPO)', ' TOPO pour mise à jour PLOF');
INSERT INTO groupe VALUES (14, 'Disposition Transitoire', ' Disposition Transitoire');


SELECT pg_catalog.setval('groupe_id_seq', 14, true);

