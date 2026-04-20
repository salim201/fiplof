CREATE SEQUENCE fokontany_idfokontany_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 10
  CACHE 1;
ALTER TABLE fokontany_idfokontany_seq
  OWNER TO postgres;

ALTER TABLE fokontany
	ALTER COLUMN idfokontany SET DEFAULT nextval('fokontany_idfokontany_seq'::regclass);