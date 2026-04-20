CREATE SEQUENCE personnemorale_idpersonnemorale_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 10
  CACHE 1;
ALTER TABLE personnemorale_idpersonnemorale_seq
  OWNER TO postgres;

ALTER TABLE personnemorale
	ALTER COLUMN idpersonnemorale SET DEFAULT nextval('personnemorale_idpersonnemorale_seq'::regclass),
	DROP COLUMN type;