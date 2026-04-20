ALTER TABLE personnemoraleparcelle 
DROP CONSTRAINT fk_personnemoraleparcelle_person;

ALTER TABLE personnemorale
DROP CONSTRAINT pk_personnemorale;

ALTER TABLE personnemorale
ALTER COLUMN idpersonnemorale TYPE BIGINT USING idpersonnemorale::numeric,
ADD CONSTRAINT pk_personnemorale PRIMARY KEY (idpersonnemorale);

ALTER TABLE personnemoraleparcelle
ALTER COLUMN idpersonnemorale TYPE BIGINT USING idpersonnemorale::numeric;

ALTER TABLE personnemoraleparcelle
ADD CONSTRAINT fk_personnemoraleparcelle_person FOREIGN KEY (idpersonnemorale)
REFERENCES personnemorale (idpersonnemorale) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;



-- Table: personnemoraleparcelle_d

-- DROP TABLE personnemoraleparcelle_d;

CREATE TABLE personnemoraleparcelle_d
(
  idpersonne bigint NOT NULL,
  idparcelle bigint NOT NULL,
  CONSTRAINT pk_personnemoraleparcelle_d PRIMARY KEY (idpersonne, idparcelle),
  CONSTRAINT fk_parcelle_d FOREIGN KEY (idparcelle)
      REFERENCES parcelle_d (gid) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT fk_persmorale FOREIGN KEY (idpersonne)
      REFERENCES personnemorale (idpersonnemorale) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE personnemoraleparcelle_d
  OWNER TO postgres;
