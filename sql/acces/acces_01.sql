INSERT INTO public.acces(nom, libelle)
   VALUES('CERTIFICAT/CREATE', 'Creation Certificat'),
   ('CERTIFICAT/READ', 'Consultation Certificat'),
   ('CERTIFICAT/EDIT_INFO', 'Edition des informations des certificats'),
   ('CERTIFICAT/EDIT_GEO', 'Edition des geometries des certificats');

INSERT INTO public.acces(nom, libelle)
   VALUES('PERSONNE_PHYSIQUE/CREATE', 'Creation Personne Physique'),
   ('PERSONNE_PHYSIQUE/READ', 'Consultation Personne Physique'),
   ('PERSONNE_PHYSIQUE/EDIT', 'Edition Personne Physique'),

   ('PERSONNE_MORALE/CREATE', 'Creation Personne Morale'),
   ('PERSONNE_MORALE/READ', 'Consultation Personne Morale'),
   ('PERSONNE_MORALE/EDIT', 'Edition Personne Morale');