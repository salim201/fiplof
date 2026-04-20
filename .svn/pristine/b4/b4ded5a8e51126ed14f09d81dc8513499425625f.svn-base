CREATE TABLE anomalie
(
  idanomalie bigserial NOT NULL,
  id_type_anomalie bigint,
  description character varying(1024),
  resolu boolean,
  csv_iddemande character varying(32),
  date_anomalie date,
  csv_id character varying(32),
  csv_id_type_anomalie character varying(32),
  CONSTRAINT pk_anomalie PRIMARY KEY (idanomalie)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE anomalie
  OWNER TO postgres;
