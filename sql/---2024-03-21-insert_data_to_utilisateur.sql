INSERT INTO acces VALUES (84, 'PROJET_UTILISATEUR/GERER_GROUPE', 'Gestion des groupes');

SELECT pg_catalog.setval('acces_id_seq', 84, true);

INSERT INTO groupe VALUES (1, 'Admin', 'Administrateur de l''application');
INSERT INTO groupe VALUES (5, 'Responsable Commune', ' Responsable des communes');
INSERT INTO groupe VALUES (10, 'Guichet Foncier', ' Agent Guichet Foncier');
INSERT INTO groupe VALUES (11, 'Assistants Techniques', 'Assistants Techniques ');
INSERT INTO groupe VALUES (12, 'Formateur', ' Formateur');
INSERT INTO groupe VALUES (13, 'Guichet Unique (TOPO)', ' TOPO pour mise à jour PLOF');
INSERT INTO groupe VALUES (14, 'Disposition Transitoire', ' Disposition Transitoire');


SELECT pg_catalog.setval('groupe_id_seq', 14, true);


UPDATE utilisateur SET  nomutilisateur = 'Responsable', prenomutilisateur =  'Commune', loginutilisateur = 'respcom', passwordutilisateur = '0308BD47138299D52D9A197C3D2178DD', telephone = '034', group_id = 5 WHERE idutilisateur = 8;
INSERT INTO utilisateur VALUES (10, 'Assistant', 'Technique', 'ats', '34EE78AE5EDC56DC1DC00BB844C5D62A', NULL, '', '', '', NULL, NULL, 11);
UPDATE utilisateur SET  nomutilisateur = 'Assistant', prenomutilisateur =  'Technique', loginutilisateur = 'respcom', passwordutilisateur = '0308BD47138299D52D9A197C3D2178DD', telephone = '034', group_id = 5 WHERE idutilisateur = 8;
INSERT INTO utilisateur VALUES (11, 'Formateur', '', 'formation', '06048D2F2D2CA345A721B4FD25B91A92', NULL, '', '', '', NULL, NULL, 12);
INSERT INTO utilisateur VALUES (12, 'Agent', 'Topo', 'topo', '1D6EA1F692424E806963838CF9E37E37', NULL, '', '', '', NULL, NULL, 13);
INSERT INTO utilisateur VALUES (13, 'Disposition', 'Transitoire', 'dt', '13D94D956F809706C5245ABD927A0E15', NULL, '', '', '', NULL, NULL, 14);
INSERT INTO utilisateur VALUES (14, 'Agent', 'Guichet Foncier', 'agf', 'A3856373041BB18DD4A9943A55B4D654', NULL, '', '', '', NULL, NULL, 10);
UPDATE utilisateur SET  nomutilisateur = 'Administrateur', prenomutilisateur =  'Fiplof', loginutilisateur = 'admin', passwordutilisateur = 'EC40092C49C76E8EA3A8AA7F7FA9B0EB', telephone = '034', group_id = 1 WHERE idutilisateur = 1;

DROP TABLE groupe_acces;

CREATE TABLE groupe_acces (
    id bigint NOT NULL,
    groupe_id bigint,
    acces_id bigint,
    autorise boolean
);


ALTER TABLE public.groupe_acces OWNER TO postgres;

--
-- TOC entry 276 (class 1259 OID 54177)
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
-- TOC entry 4081 (class 0 OID 0)
-- Dependencies: 276
-- Name: groupe_acces_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE groupe_acces_id_seq OWNED BY groupe_acces.id;


--
-- TOC entry 3947 (class 2604 OID 54623)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY groupe_acces ALTER COLUMN id SET DEFAULT nextval('groupe_acces_id_seq'::regclass);


--
-- TOC entry 4075 (class 0 OID 54174)
-- Dependencies: 275
-- Data for Name: groupe_acces; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO groupe_acces VALUES (188, 10, 3, true);
INSERT INTO groupe_acces VALUES (189, 10, 4, true);
INSERT INTO groupe_acces VALUES (22, 5, 2, true);
INSERT INTO groupe_acces VALUES (23, 5, 3, false);
INSERT INTO groupe_acces VALUES (24, 5, 4, false);
INSERT INTO groupe_acces VALUES (135, 5, 35, false);
INSERT INTO groupe_acces VALUES (136, 5, 36, false);
INSERT INTO groupe_acces VALUES (137, 5, 37, false);
INSERT INTO groupe_acces VALUES (144, 5, 75, false);
INSERT INTO groupe_acces VALUES (30, 5, 6, true);
INSERT INTO groupe_acces VALUES (31, 5, 7, false);
INSERT INTO groupe_acces VALUES (32, 5, 8, false);
INSERT INTO groupe_acces VALUES (124, 5, 21, true);
INSERT INTO groupe_acces VALUES (125, 5, 23, false);
INSERT INTO groupe_acces VALUES (138, 5, 40, false);
INSERT INTO groupe_acces VALUES (139, 5, 41, false);
INSERT INTO groupe_acces VALUES (33, 5, 9, false);
INSERT INTO groupe_acces VALUES (34, 5, 10, false);
INSERT INTO groupe_acces VALUES (35, 5, 11, false);
INSERT INTO groupe_acces VALUES (36, 5, 12, false);
INSERT INTO groupe_acces VALUES (37, 5, 13, false);
INSERT INTO groupe_acces VALUES (38, 5, 14, false);
INSERT INTO groupe_acces VALUES (53, 5, 15, false);
INSERT INTO groupe_acces VALUES (54, 5, 16, false);
INSERT INTO groupe_acces VALUES (55, 5, 17, false);
INSERT INTO groupe_acces VALUES (56, 5, 18, false);
INSERT INTO groupe_acces VALUES (57, 5, 19, false);
INSERT INTO groupe_acces VALUES (126, 5, 24, false);
INSERT INTO groupe_acces VALUES (127, 5, 25, false);
INSERT INTO groupe_acces VALUES (128, 5, 26, false);
INSERT INTO groupe_acces VALUES (129, 5, 27, false);
INSERT INTO groupe_acces VALUES (130, 5, 28, false);
INSERT INTO groupe_acces VALUES (131, 5, 29, true);
INSERT INTO groupe_acces VALUES (132, 5, 30, false);
INSERT INTO groupe_acces VALUES (145, 5, 42, false);
INSERT INTO groupe_acces VALUES (141, 5, 34, false);
INSERT INTO groupe_acces VALUES (142, 5, 38, false);
INSERT INTO groupe_acces VALUES (143, 5, 39, false);
INSERT INTO groupe_acces VALUES (146, 5, 43, true);
INSERT INTO groupe_acces VALUES (190, 10, 35, true);
INSERT INTO groupe_acces VALUES (191, 10, 36, true);
INSERT INTO groupe_acces VALUES (192, 10, 37, true);
INSERT INTO groupe_acces VALUES (193, 10, 75, true);
INSERT INTO groupe_acces VALUES (194, 10, 5, true);
INSERT INTO groupe_acces VALUES (195, 10, 6, true);
INSERT INTO groupe_acces VALUES (196, 10, 7, false);
INSERT INTO groupe_acces VALUES (198, 10, 21, true);
INSERT INTO groupe_acces VALUES (199, 10, 23, false);
INSERT INTO groupe_acces VALUES (200, 10, 40, true);
INSERT INTO groupe_acces VALUES (201, 10, 41, false);
INSERT INTO groupe_acces VALUES (202, 10, 9, true);
INSERT INTO groupe_acces VALUES (203, 10, 10, true);
INSERT INTO groupe_acces VALUES (204, 10, 11, true);
INSERT INTO groupe_acces VALUES (205, 10, 12, true);
INSERT INTO groupe_acces VALUES (206, 10, 13, true);
INSERT INTO groupe_acces VALUES (207, 10, 14, true);
INSERT INTO groupe_acces VALUES (208, 10, 15, true);
INSERT INTO groupe_acces VALUES (209, 10, 16, true);
INSERT INTO groupe_acces VALUES (210, 10, 17, true);
INSERT INTO groupe_acces VALUES (211, 10, 18, true);
INSERT INTO groupe_acces VALUES (213, 10, 24, true);
INSERT INTO groupe_acces VALUES (214, 10, 25, true);
INSERT INTO groupe_acces VALUES (215, 10, 26, true);
INSERT INTO groupe_acces VALUES (216, 10, 27, true);
INSERT INTO groupe_acces VALUES (217, 10, 28, true);
INSERT INTO groupe_acces VALUES (218, 10, 29, true);
INSERT INTO groupe_acces VALUES (219, 10, 30, true);
INSERT INTO groupe_acces VALUES (220, 10, 42, true);
INSERT INTO groupe_acces VALUES (221, 10, 33, true);
INSERT INTO groupe_acces VALUES (222, 10, 34, true);
INSERT INTO groupe_acces VALUES (223, 10, 38, true);
INSERT INTO groupe_acces VALUES (224, 10, 39, true);
INSERT INTO groupe_acces VALUES (225, 10, 43, true);
INSERT INTO groupe_acces VALUES (226, 10, 76, true);
INSERT INTO groupe_acces VALUES (228, 10, 45, false);
INSERT INTO groupe_acces VALUES (229, 10, 46, false);
INSERT INTO groupe_acces VALUES (230, 10, 47, true);
INSERT INTO groupe_acces VALUES (231, 10, 48, true);
INSERT INTO groupe_acces VALUES (232, 10, 49, true);
INSERT INTO groupe_acces VALUES (233, 10, 50, true);
INSERT INTO groupe_acces VALUES (234, 10, 51, true);
INSERT INTO groupe_acces VALUES (235, 10, 52, true);
INSERT INTO groupe_acces VALUES (236, 10, 53, true);
INSERT INTO groupe_acces VALUES (237, 10, 54, false);
INSERT INTO groupe_acces VALUES (238, 10, 55, true);
INSERT INTO groupe_acces VALUES (239, 10, 56, true);
INSERT INTO groupe_acces VALUES (21, 5, 1, false);
INSERT INTO groupe_acces VALUES (29, 5, 5, false);
INSERT INTO groupe_acces VALUES (140, 5, 33, false);
INSERT INTO groupe_acces VALUES (147, 5, 76, false);
INSERT INTO groupe_acces VALUES (148, 5, 77, false);
INSERT INTO groupe_acces VALUES (149, 5, 45, false);
INSERT INTO groupe_acces VALUES (151, 5, 47, false);
INSERT INTO groupe_acces VALUES (152, 5, 48, false);
INSERT INTO groupe_acces VALUES (153, 5, 49, false);
INSERT INTO groupe_acces VALUES (154, 5, 50, false);
INSERT INTO groupe_acces VALUES (155, 5, 51, false);
INSERT INTO groupe_acces VALUES (156, 5, 52, false);
INSERT INTO groupe_acces VALUES (157, 5, 53, false);
INSERT INTO groupe_acces VALUES (158, 5, 54, false);
INSERT INTO groupe_acces VALUES (159, 5, 55, false);
INSERT INTO groupe_acces VALUES (160, 5, 56, false);
INSERT INTO groupe_acces VALUES (161, 5, 57, false);
INSERT INTO groupe_acces VALUES (162, 5, 58, false);
INSERT INTO groupe_acces VALUES (163, 5, 59, false);
INSERT INTO groupe_acces VALUES (164, 5, 60, false);
INSERT INTO groupe_acces VALUES (166, 5, 62, false);
INSERT INTO groupe_acces VALUES (167, 5, 63, false);
INSERT INTO groupe_acces VALUES (168, 5, 64, false);
INSERT INTO groupe_acces VALUES (169, 5, 65, true);
INSERT INTO groupe_acces VALUES (170, 5, 66, false);
INSERT INTO groupe_acces VALUES (171, 5, 67, false);
INSERT INTO groupe_acces VALUES (172, 5, 68, false);
INSERT INTO groupe_acces VALUES (173, 5, 69, true);
INSERT INTO groupe_acces VALUES (174, 5, 70, false);
INSERT INTO groupe_acces VALUES (175, 5, 71, false);
INSERT INTO groupe_acces VALUES (176, 5, 72, false);
INSERT INTO groupe_acces VALUES (177, 5, 73, false);
INSERT INTO groupe_acces VALUES (178, 5, 74, false);
INSERT INTO groupe_acces VALUES (179, 5, 78, false);
INSERT INTO groupe_acces VALUES (181, 5, 83, false);
INSERT INTO groupe_acces VALUES (182, 5, 80, false);
INSERT INTO groupe_acces VALUES (183, 5, 81, false);
INSERT INTO groupe_acces VALUES (184, 5, 82, false);
INSERT INTO groupe_acces VALUES (185, 5, 84, false);
INSERT INTO groupe_acces VALUES (187, 10, 2, true);
INSERT INTO groupe_acces VALUES (242, 10, 59, true);
INSERT INTO groupe_acces VALUES (243, 10, 60, true);
INSERT INTO groupe_acces VALUES (244, 10, 61, true);
INSERT INTO groupe_acces VALUES (245, 10, 62, true);
INSERT INTO groupe_acces VALUES (246, 10, 63, true);
INSERT INTO groupe_acces VALUES (247, 10, 64, true);
INSERT INTO groupe_acces VALUES (248, 10, 65, true);
INSERT INTO groupe_acces VALUES (249, 10, 66, true);
INSERT INTO groupe_acces VALUES (250, 10, 67, true);
INSERT INTO groupe_acces VALUES (251, 10, 68, true);
INSERT INTO groupe_acces VALUES (252, 10, 69, true);
INSERT INTO groupe_acces VALUES (253, 10, 70, false);
INSERT INTO groupe_acces VALUES (254, 10, 71, false);
INSERT INTO groupe_acces VALUES (255, 10, 72, false);
INSERT INTO groupe_acces VALUES (256, 10, 73, false);
INSERT INTO groupe_acces VALUES (257, 10, 74, false);
INSERT INTO groupe_acces VALUES (258, 10, 78, false);
INSERT INTO groupe_acces VALUES (259, 10, 79, false);
INSERT INTO groupe_acces VALUES (260, 10, 83, false);
INSERT INTO groupe_acces VALUES (261, 10, 80, false);
INSERT INTO groupe_acces VALUES (262, 10, 81, false);
INSERT INTO groupe_acces VALUES (263, 10, 82, false);
INSERT INTO groupe_acces VALUES (264, 10, 84, true);
INSERT INTO groupe_acces VALUES (265, 11, 1, true);
INSERT INTO groupe_acces VALUES (266, 11, 2, true);
INSERT INTO groupe_acces VALUES (267, 11, 3, true);
INSERT INTO groupe_acces VALUES (268, 11, 4, true);
INSERT INTO groupe_acces VALUES (269, 11, 35, true);
INSERT INTO groupe_acces VALUES (270, 11, 36, true);
INSERT INTO groupe_acces VALUES (271, 11, 37, true);
INSERT INTO groupe_acces VALUES (272, 11, 75, true);
INSERT INTO groupe_acces VALUES (273, 11, 5, true);
INSERT INTO groupe_acces VALUES (274, 11, 6, true);
INSERT INTO groupe_acces VALUES (275, 11, 7, true);
INSERT INTO groupe_acces VALUES (276, 11, 8, true);
INSERT INTO groupe_acces VALUES (277, 11, 21, true);
INSERT INTO groupe_acces VALUES (278, 11, 23, false);
INSERT INTO groupe_acces VALUES (279, 11, 40, true);
INSERT INTO groupe_acces VALUES (280, 11, 41, false);
INSERT INTO groupe_acces VALUES (281, 11, 9, true);
INSERT INTO groupe_acces VALUES (282, 11, 10, true);
INSERT INTO groupe_acces VALUES (283, 11, 11, true);
INSERT INTO groupe_acces VALUES (284, 11, 12, true);
INSERT INTO groupe_acces VALUES (285, 11, 13, true);
INSERT INTO groupe_acces VALUES (286, 11, 14, true);
INSERT INTO groupe_acces VALUES (287, 11, 15, true);
INSERT INTO groupe_acces VALUES (288, 11, 16, true);
INSERT INTO groupe_acces VALUES (289, 11, 17, true);
INSERT INTO groupe_acces VALUES (290, 11, 18, true);
INSERT INTO groupe_acces VALUES (291, 11, 19, true);
INSERT INTO groupe_acces VALUES (292, 11, 24, false);
INSERT INTO groupe_acces VALUES (293, 11, 25, false);
INSERT INTO groupe_acces VALUES (294, 11, 26, false);
INSERT INTO groupe_acces VALUES (295, 11, 27, false);
INSERT INTO groupe_acces VALUES (296, 11, 28, false);
INSERT INTO groupe_acces VALUES (297, 11, 29, false);
INSERT INTO groupe_acces VALUES (298, 11, 30, false);
INSERT INTO groupe_acces VALUES (299, 11, 42, false);
INSERT INTO groupe_acces VALUES (300, 11, 33, true);
INSERT INTO groupe_acces VALUES (301, 11, 34, true);
INSERT INTO groupe_acces VALUES (302, 11, 38, true);
INSERT INTO groupe_acces VALUES (303, 11, 39, true);
INSERT INTO groupe_acces VALUES (304, 11, 43, true);
INSERT INTO groupe_acces VALUES (305, 11, 76, true);
INSERT INTO groupe_acces VALUES (306, 11, 77, true);
INSERT INTO groupe_acces VALUES (307, 11, 45, true);
INSERT INTO groupe_acces VALUES (308, 11, 46, true);
INSERT INTO groupe_acces VALUES (309, 11, 47, true);
INSERT INTO groupe_acces VALUES (310, 11, 48, true);
INSERT INTO groupe_acces VALUES (311, 11, 49, true);
INSERT INTO groupe_acces VALUES (312, 11, 50, true);
INSERT INTO groupe_acces VALUES (313, 11, 51, true);
INSERT INTO groupe_acces VALUES (314, 11, 52, false);
INSERT INTO groupe_acces VALUES (315, 11, 53, true);
INSERT INTO groupe_acces VALUES (316, 11, 54, false);
INSERT INTO groupe_acces VALUES (317, 11, 55, true);
INSERT INTO groupe_acces VALUES (318, 11, 56, true);
INSERT INTO groupe_acces VALUES (319, 11, 57, true);
INSERT INTO groupe_acces VALUES (320, 11, 58, true);
INSERT INTO groupe_acces VALUES (321, 11, 59, true);
INSERT INTO groupe_acces VALUES (322, 11, 60, true);
INSERT INTO groupe_acces VALUES (323, 11, 61, true);
INSERT INTO groupe_acces VALUES (324, 11, 62, true);
INSERT INTO groupe_acces VALUES (325, 11, 63, true);
INSERT INTO groupe_acces VALUES (326, 11, 64, true);
INSERT INTO groupe_acces VALUES (327, 11, 65, true);
INSERT INTO groupe_acces VALUES (328, 11, 66, true);
INSERT INTO groupe_acces VALUES (329, 11, 67, true);
INSERT INTO groupe_acces VALUES (330, 11, 68, true);
INSERT INTO groupe_acces VALUES (331, 11, 69, true);
INSERT INTO groupe_acces VALUES (332, 11, 70, false);
INSERT INTO groupe_acces VALUES (333, 11, 71, true);
INSERT INTO groupe_acces VALUES (334, 11, 72, true);
INSERT INTO groupe_acces VALUES (335, 11, 73, true);
INSERT INTO groupe_acces VALUES (336, 11, 74, false);
INSERT INTO groupe_acces VALUES (337, 11, 78, true);
INSERT INTO groupe_acces VALUES (338, 11, 79, true);
INSERT INTO groupe_acces VALUES (339, 11, 83, false);
INSERT INTO groupe_acces VALUES (340, 11, 80, true);
INSERT INTO groupe_acces VALUES (341, 11, 81, true);
INSERT INTO groupe_acces VALUES (342, 11, 82, true);
INSERT INTO groupe_acces VALUES (343, 11, 84, false);
INSERT INTO groupe_acces VALUES (345, 12, 2, true);
INSERT INTO groupe_acces VALUES (346, 12, 3, true);
INSERT INTO groupe_acces VALUES (212, 10, 19, true);
INSERT INTO groupe_acces VALUES (227, 10, 77, true);
INSERT INTO groupe_acces VALUES (241, 10, 58, false);
INSERT INTO groupe_acces VALUES (347, 12, 4, true);
INSERT INTO groupe_acces VALUES (348, 12, 35, true);
INSERT INTO groupe_acces VALUES (349, 12, 36, true);
INSERT INTO groupe_acces VALUES (350, 12, 37, true);
INSERT INTO groupe_acces VALUES (351, 12, 75, true);
INSERT INTO groupe_acces VALUES (352, 12, 5, true);
INSERT INTO groupe_acces VALUES (353, 12, 6, true);
INSERT INTO groupe_acces VALUES (354, 12, 7, true);
INSERT INTO groupe_acces VALUES (355, 12, 8, true);
INSERT INTO groupe_acces VALUES (356, 12, 21, true);
INSERT INTO groupe_acces VALUES (357, 12, 23, false);
INSERT INTO groupe_acces VALUES (358, 12, 40, true);
INSERT INTO groupe_acces VALUES (360, 12, 9, true);
INSERT INTO groupe_acces VALUES (361, 12, 10, true);
INSERT INTO groupe_acces VALUES (362, 12, 11, true);
INSERT INTO groupe_acces VALUES (363, 12, 12, true);
INSERT INTO groupe_acces VALUES (364, 12, 13, true);
INSERT INTO groupe_acces VALUES (344, 12, 1, true);
INSERT INTO groupe_acces VALUES (197, 10, 8, false);
INSERT INTO groupe_acces VALUES (368, 12, 17, true);
INSERT INTO groupe_acces VALUES (369, 12, 18, true);
INSERT INTO groupe_acces VALUES (370, 12, 19, true);
INSERT INTO groupe_acces VALUES (371, 12, 24, true);
INSERT INTO groupe_acces VALUES (372, 12, 25, true);
INSERT INTO groupe_acces VALUES (373, 12, 26, true);
INSERT INTO groupe_acces VALUES (427, 13, 35, false);
INSERT INTO groupe_acces VALUES (428, 13, 36, false);
INSERT INTO groupe_acces VALUES (429, 13, 37, false);
INSERT INTO groupe_acces VALUES (430, 13, 75, false);
INSERT INTO groupe_acces VALUES (431, 13, 5, false);
INSERT INTO groupe_acces VALUES (432, 13, 6, true);
INSERT INTO groupe_acces VALUES (433, 13, 7, false);
INSERT INTO groupe_acces VALUES (434, 13, 8, false);
INSERT INTO groupe_acces VALUES (435, 13, 21, false);
INSERT INTO groupe_acces VALUES (436, 13, 23, false);
INSERT INTO groupe_acces VALUES (437, 13, 40, false);
INSERT INTO groupe_acces VALUES (438, 13, 41, false);
INSERT INTO groupe_acces VALUES (439, 13, 9, false);
INSERT INTO groupe_acces VALUES (440, 13, 10, false);
INSERT INTO groupe_acces VALUES (442, 13, 12, false);
INSERT INTO groupe_acces VALUES (443, 13, 13, false);
INSERT INTO groupe_acces VALUES (444, 13, 14, false);
INSERT INTO groupe_acces VALUES (445, 13, 15, false);
INSERT INTO groupe_acces VALUES (446, 13, 16, false);
INSERT INTO groupe_acces VALUES (447, 13, 17, false);
INSERT INTO groupe_acces VALUES (448, 13, 18, false);
INSERT INTO groupe_acces VALUES (449, 13, 19, false);
INSERT INTO groupe_acces VALUES (450, 13, 24, false);
INSERT INTO groupe_acces VALUES (451, 13, 25, false);
INSERT INTO groupe_acces VALUES (452, 13, 26, false);
INSERT INTO groupe_acces VALUES (453, 13, 27, false);
INSERT INTO groupe_acces VALUES (454, 13, 28, false);
INSERT INTO groupe_acces VALUES (455, 13, 29, false);
INSERT INTO groupe_acces VALUES (457, 13, 42, false);
INSERT INTO groupe_acces VALUES (458, 13, 33, false);
INSERT INTO groupe_acces VALUES (459, 13, 34, false);
INSERT INTO groupe_acces VALUES (460, 13, 38, false);
INSERT INTO groupe_acces VALUES (461, 13, 39, false);
INSERT INTO groupe_acces VALUES (462, 13, 43, true);
INSERT INTO groupe_acces VALUES (463, 13, 76, false);
INSERT INTO groupe_acces VALUES (464, 13, 77, true);
INSERT INTO groupe_acces VALUES (465, 13, 45, false);
INSERT INTO groupe_acces VALUES (466, 13, 46, false);
INSERT INTO groupe_acces VALUES (467, 13, 47, false);
INSERT INTO groupe_acces VALUES (468, 13, 48, true);
INSERT INTO groupe_acces VALUES (469, 13, 49, false);
INSERT INTO groupe_acces VALUES (470, 13, 50, false);
INSERT INTO groupe_acces VALUES (472, 13, 52, false);
INSERT INTO groupe_acces VALUES (473, 13, 53, false);
INSERT INTO groupe_acces VALUES (474, 13, 54, false);
INSERT INTO groupe_acces VALUES (475, 13, 55, true);
INSERT INTO groupe_acces VALUES (476, 13, 56, false);
INSERT INTO groupe_acces VALUES (477, 13, 57, false);
INSERT INTO groupe_acces VALUES (478, 13, 58, false);
INSERT INTO groupe_acces VALUES (479, 13, 59, false);
INSERT INTO groupe_acces VALUES (480, 13, 60, false);
INSERT INTO groupe_acces VALUES (481, 13, 61, false);
INSERT INTO groupe_acces VALUES (482, 13, 62, false);
INSERT INTO groupe_acces VALUES (483, 13, 63, false);
INSERT INTO groupe_acces VALUES (484, 13, 64, false);
INSERT INTO groupe_acces VALUES (485, 13, 65, false);
INSERT INTO groupe_acces VALUES (487, 13, 67, false);
INSERT INTO groupe_acces VALUES (488, 13, 68, false);
INSERT INTO groupe_acces VALUES (489, 13, 69, true);
INSERT INTO groupe_acces VALUES (490, 13, 70, true);
INSERT INTO groupe_acces VALUES (491, 13, 71, false);
INSERT INTO groupe_acces VALUES (492, 13, 72, false);
INSERT INTO groupe_acces VALUES (493, 13, 73, true);
INSERT INTO groupe_acces VALUES (494, 13, 74, true);
INSERT INTO groupe_acces VALUES (495, 13, 78, false);
INSERT INTO groupe_acces VALUES (496, 13, 79, false);
INSERT INTO groupe_acces VALUES (497, 13, 83, false);
INSERT INTO groupe_acces VALUES (498, 13, 80, true);
INSERT INTO groupe_acces VALUES (499, 13, 81, true);
INSERT INTO groupe_acces VALUES (500, 13, 82, true);
INSERT INTO groupe_acces VALUES (367, 12, 16, true);
INSERT INTO groupe_acces VALUES (374, 12, 27, true);
INSERT INTO groupe_acces VALUES (375, 12, 28, true);
INSERT INTO groupe_acces VALUES (376, 12, 29, true);
INSERT INTO groupe_acces VALUES (377, 12, 30, true);
INSERT INTO groupe_acces VALUES (378, 12, 42, true);
INSERT INTO groupe_acces VALUES (379, 12, 33, true);
INSERT INTO groupe_acces VALUES (380, 12, 34, true);
INSERT INTO groupe_acces VALUES (381, 12, 38, true);
INSERT INTO groupe_acces VALUES (382, 12, 39, true);
INSERT INTO groupe_acces VALUES (383, 12, 43, true);
INSERT INTO groupe_acces VALUES (384, 12, 76, true);
INSERT INTO groupe_acces VALUES (385, 12, 77, true);
INSERT INTO groupe_acces VALUES (387, 12, 46, true);
INSERT INTO groupe_acces VALUES (388, 12, 47, true);
INSERT INTO groupe_acces VALUES (389, 12, 48, true);
INSERT INTO groupe_acces VALUES (390, 12, 49, true);
INSERT INTO groupe_acces VALUES (391, 12, 50, true);
INSERT INTO groupe_acces VALUES (392, 12, 51, true);
INSERT INTO groupe_acces VALUES (393, 12, 52, true);
INSERT INTO groupe_acces VALUES (394, 12, 53, true);
INSERT INTO groupe_acces VALUES (395, 12, 54, true);
INSERT INTO groupe_acces VALUES (396, 12, 55, true);
INSERT INTO groupe_acces VALUES (397, 12, 56, true);
INSERT INTO groupe_acces VALUES (398, 12, 57, true);
INSERT INTO groupe_acces VALUES (399, 12, 58, true);
INSERT INTO groupe_acces VALUES (400, 12, 59, true);
INSERT INTO groupe_acces VALUES (402, 12, 61, true);
INSERT INTO groupe_acces VALUES (403, 12, 62, true);
INSERT INTO groupe_acces VALUES (404, 12, 63, true);
INSERT INTO groupe_acces VALUES (405, 12, 64, true);
INSERT INTO groupe_acces VALUES (406, 12, 65, true);
INSERT INTO groupe_acces VALUES (407, 12, 66, true);
INSERT INTO groupe_acces VALUES (408, 12, 67, true);
INSERT INTO groupe_acces VALUES (409, 12, 68, true);
INSERT INTO groupe_acces VALUES (410, 12, 69, true);
INSERT INTO groupe_acces VALUES (411, 12, 70, true);
INSERT INTO groupe_acces VALUES (412, 12, 71, true);
INSERT INTO groupe_acces VALUES (413, 12, 72, true);
INSERT INTO groupe_acces VALUES (414, 12, 73, true);
INSERT INTO groupe_acces VALUES (415, 12, 74, true);
INSERT INTO groupe_acces VALUES (417, 12, 79, true);
INSERT INTO groupe_acces VALUES (418, 12, 83, false);
INSERT INTO groupe_acces VALUES (419, 12, 80, true);
INSERT INTO groupe_acces VALUES (420, 12, 81, true);
INSERT INTO groupe_acces VALUES (421, 12, 82, true);
INSERT INTO groupe_acces VALUES (422, 12, 84, false);
INSERT INTO groupe_acces VALUES (424, 13, 2, true);
INSERT INTO groupe_acces VALUES (366, 12, 15, true);
INSERT INTO groupe_acces VALUES (425, 13, 3, false);
INSERT INTO groupe_acces VALUES (544, 14, 45, true);
INSERT INTO groupe_acces VALUES (502, 14, 1, true);
INSERT INTO groupe_acces VALUES (503, 14, 2, true);
INSERT INTO groupe_acces VALUES (504, 14, 3, true);
INSERT INTO groupe_acces VALUES (505, 14, 4, true);
INSERT INTO groupe_acces VALUES (506, 14, 35, true);
INSERT INTO groupe_acces VALUES (507, 14, 36, true);
INSERT INTO groupe_acces VALUES (508, 14, 37, true);
INSERT INTO groupe_acces VALUES (523, 14, 14, true);
INSERT INTO groupe_acces VALUES (524, 14, 15, true);
INSERT INTO groupe_acces VALUES (525, 14, 16, true);
INSERT INTO groupe_acces VALUES (526, 14, 17, true);
INSERT INTO groupe_acces VALUES (527, 14, 18, true);
INSERT INTO groupe_acces VALUES (528, 14, 19, true);
INSERT INTO groupe_acces VALUES (529, 14, 24, false);
INSERT INTO groupe_acces VALUES (530, 14, 25, false);
INSERT INTO groupe_acces VALUES (531, 14, 26, false);
INSERT INTO groupe_acces VALUES (532, 14, 27, false);
INSERT INTO groupe_acces VALUES (533, 14, 28, false);
INSERT INTO groupe_acces VALUES (534, 14, 29, false);
INSERT INTO groupe_acces VALUES (535, 14, 30, false);
INSERT INTO groupe_acces VALUES (536, 14, 42, false);
INSERT INTO groupe_acces VALUES (537, 14, 33, true);
INSERT INTO groupe_acces VALUES (538, 14, 34, true);
INSERT INTO groupe_acces VALUES (539, 14, 38, true);
INSERT INTO groupe_acces VALUES (540, 14, 39, true);
INSERT INTO groupe_acces VALUES (541, 14, 43, true);
INSERT INTO groupe_acces VALUES (542, 14, 76, true);
INSERT INTO groupe_acces VALUES (543, 14, 77, true);
INSERT INTO groupe_acces VALUES (545, 14, 46, true);
INSERT INTO groupe_acces VALUES (546, 14, 47, true);
INSERT INTO groupe_acces VALUES (547, 14, 48, true);
INSERT INTO groupe_acces VALUES (548, 14, 49, true);
INSERT INTO groupe_acces VALUES (549, 14, 50, true);
INSERT INTO groupe_acces VALUES (550, 14, 51, true);
INSERT INTO groupe_acces VALUES (551, 14, 52, false);
INSERT INTO groupe_acces VALUES (552, 14, 53, true);
INSERT INTO groupe_acces VALUES (553, 14, 54, false);
INSERT INTO groupe_acces VALUES (554, 14, 55, true);
INSERT INTO groupe_acces VALUES (555, 14, 56, true);
INSERT INTO groupe_acces VALUES (556, 14, 57, true);
INSERT INTO groupe_acces VALUES (557, 14, 58, false);
INSERT INTO groupe_acces VALUES (558, 14, 59, true);
INSERT INTO groupe_acces VALUES (559, 14, 60, true);
INSERT INTO groupe_acces VALUES (560, 14, 61, true);
INSERT INTO groupe_acces VALUES (561, 14, 62, true);
INSERT INTO groupe_acces VALUES (562, 14, 63, true);
INSERT INTO groupe_acces VALUES (563, 14, 64, true);
INSERT INTO groupe_acces VALUES (564, 14, 65, false);
INSERT INTO groupe_acces VALUES (565, 14, 66, true);
INSERT INTO groupe_acces VALUES (566, 14, 67, true);
INSERT INTO groupe_acces VALUES (567, 14, 68, true);
INSERT INTO groupe_acces VALUES (568, 14, 69, true);
INSERT INTO groupe_acces VALUES (569, 14, 70, true);
INSERT INTO groupe_acces VALUES (570, 14, 71, true);
INSERT INTO groupe_acces VALUES (571, 14, 72, true);
INSERT INTO groupe_acces VALUES (572, 14, 73, true);
INSERT INTO groupe_acces VALUES (573, 14, 74, true);
INSERT INTO groupe_acces VALUES (574, 14, 78, true);
INSERT INTO groupe_acces VALUES (575, 14, 79, true);
INSERT INTO groupe_acces VALUES (576, 14, 83, true);
INSERT INTO groupe_acces VALUES (577, 14, 80, true);
INSERT INTO groupe_acces VALUES (578, 14, 81, true);
INSERT INTO groupe_acces VALUES (579, 14, 82, true);
INSERT INTO groupe_acces VALUES (580, 14, 84, false);
INSERT INTO groupe_acces VALUES (150, 5, 46, false);
INSERT INTO groupe_acces VALUES (165, 5, 61, false);
INSERT INTO groupe_acces VALUES (180, 5, 79, false);
INSERT INTO groupe_acces VALUES (186, 10, 1, true);
INSERT INTO groupe_acces VALUES (240, 10, 57, true);
INSERT INTO groupe_acces VALUES (509, 14, 75, true);
INSERT INTO groupe_acces VALUES (510, 14, 5, true);
INSERT INTO groupe_acces VALUES (511, 14, 6, true);
INSERT INTO groupe_acces VALUES (512, 14, 7, true);
INSERT INTO groupe_acces VALUES (513, 14, 8, true);
INSERT INTO groupe_acces VALUES (359, 12, 41, false);
INSERT INTO groupe_acces VALUES (365, 12, 14, true);
INSERT INTO groupe_acces VALUES (386, 12, 45, true);
INSERT INTO groupe_acces VALUES (401, 12, 60, true);
INSERT INTO groupe_acces VALUES (416, 12, 78, true);
INSERT INTO groupe_acces VALUES (423, 13, 1, false);
INSERT INTO groupe_acces VALUES (426, 13, 4, false);
INSERT INTO groupe_acces VALUES (441, 13, 11, false);
INSERT INTO groupe_acces VALUES (456, 13, 30, false);
INSERT INTO groupe_acces VALUES (471, 13, 51, false);
INSERT INTO groupe_acces VALUES (486, 13, 66, false);
INSERT INTO groupe_acces VALUES (501, 13, 84, false);
INSERT INTO groupe_acces VALUES (514, 14, 21, true);
INSERT INTO groupe_acces VALUES (515, 14, 23, false);
INSERT INTO groupe_acces VALUES (516, 14, 40, true);
INSERT INTO groupe_acces VALUES (517, 14, 41, false);
INSERT INTO groupe_acces VALUES (518, 14, 9, true);
INSERT INTO groupe_acces VALUES (519, 14, 10, true);
INSERT INTO groupe_acces VALUES (520, 14, 11, true);
INSERT INTO groupe_acces VALUES (521, 14, 12, true);
INSERT INTO groupe_acces VALUES (522, 14, 13, true);


--
-- TOC entry 4082 (class 0 OID 0)
-- Dependencies: 276
-- Name: groupe_acces_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('groupe_acces_id_seq', 580, true);


--
-- TOC entry 3949 (class 2606 OID 54683)
-- Name: groupe_acces_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY groupe_acces
    ADD CONSTRAINT groupe_acces_pkey PRIMARY KEY (id);


--
-- TOC entry 3950 (class 2606 OID 55469)
-- Name: groupe_acces_acces_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY groupe_acces
    ADD CONSTRAINT groupe_acces_acces_id_fkey FOREIGN KEY (acces_id) REFERENCES acces(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3951 (class 2606 OID 55474)
-- Name: groupe_acces_groupe_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY groupe_acces
    ADD CONSTRAINT groupe_acces_groupe_id_fkey FOREIGN KEY (groupe_id) REFERENCES groupe(id) ON UPDATE CASCADE ON DELETE CASCADE;


-- Completed on 2024-03-21 10:28:30

--
-- PostgreSQL database dump complete
--
