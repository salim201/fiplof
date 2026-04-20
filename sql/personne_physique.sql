CREATE SEQUENCE personnephysique_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE personnephysique_id_seq
  OWNER TO postgres;

  
ALTER TABLE personnephysique
   ALTER COLUMN idpersonne SET DEFAULT nextval('personnephysique_id_seq'::regclass);
