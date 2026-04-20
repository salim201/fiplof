ALTER TABLE parcelle
DROP CONSTRAINT fk_parcelle_hypotheque;

ALTER TABLE parcelle
ALTER COLUMN idhypotheque TYPE bigint USING idhypotheque::numeric;

ALTER TABLE hypotheque
ALTER COLUMN idhypotheque TYPE bigint USING idhypotheque::numeric;

ALTER TABLE parcelle
  ADD CONSTRAINT fk_parcelle_hypotheque FOREIGN KEY (idhypotheque)
      REFERENCES hypotheque (idhypotheque) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

-----------------------------------------------------------------------

ALTER TABLE parcelle
DROP CONSTRAINT fk_parcelle_servitude;
ALTER TABLE parcelle
ALTER COLUMN idservitude TYPE bigint USING idservitude::numeric;

ALTER TABLE servitudebeneficiaire
DROP CONSTRAINT fk_servitudebeneficiaire_servitu;
ALTER TABLE servitudebeneficiaire
ALTER COLUMN idservitude TYPE bigint USING idservitude::numeric;

ALTER TABLE servitudeparcellegrevees
DROP CONSTRAINT fk_servitudeparcellegrevees_serv;
ALTER TABLE servitudeparcellegrevees
ALTER COLUMN idservitude TYPE bigint USING idservitude::numeric;



ALTER TABLE servitude
ALTER COLUMN idservitude TYPE bigint USING idservitude::numeric;

ALTER TABLE parcelle
ADD CONSTRAINT fk_parcelle_servitude FOREIGN KEY (idservitude)
      REFERENCES servitude (idservitude) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE servitudebeneficiaire
  ADD CONSTRAINT fk_servitudebeneficiaire_servitu FOREIGN KEY (idservitude)
      REFERENCES servitude (idservitude) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE servitudeparcellegrevees
  ADD CONSTRAINT fk_servitudeparcellegrevees_serv FOREIGN KEY (idservitude)
      REFERENCES servitude (idservitude) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;