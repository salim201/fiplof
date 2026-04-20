CREATE SEQUENCE hameau_idhameau_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 10
  CACHE 1;
ALTER TABLE hameau_idhameau_seq
  OWNER TO postgres;

ALTER TABLE hameau
	ALTER COLUMN idhameau SET DEFAULT nextval('hameau_idhameau_seq'::regclass);