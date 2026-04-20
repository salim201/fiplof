-- Table: type_anomalie

-- DROP TABLE type_anomalie;

CREATE TABLE type_anomalie
(
  id_type_anomalie bigserial NOT NULL,
  valeur character varying(32),
  csv_id character varying(32),
  CONSTRAINT pk_type_anomalie PRIMARY KEY (id_type_anomalie)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE type_anomalie
  OWNER TO postgres;