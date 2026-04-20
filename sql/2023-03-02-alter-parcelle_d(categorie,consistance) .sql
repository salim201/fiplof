ALTER TABLE parcelle_d
   ADD COLUMN categorie character varying(128);
ALTER TABLE parcelle_d
   ALTER COLUMN consistance TYPE character varying(128);
   
ALTER TABLE parcelle_d
   ALTER COLUMN region TYPE character varying(128);
   
ALTER TABLE parcelle_d
   ALTER COLUMN commune TYPE character varying(128);
   
ALTER TABLE parcelle_d
   ALTER COLUMN fkt TYPE character varying(128);


