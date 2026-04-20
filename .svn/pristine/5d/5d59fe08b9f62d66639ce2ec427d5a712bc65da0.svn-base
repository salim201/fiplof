ALTER TABLE parcelle_d
   ADD COLUMN id_consistance bigint;
COMMENT ON COLUMN parcelle_d.id_consistance
  IS 'Clé etrangère vers consistance';
  
ALTER TABLE parcelle_d
  ADD CONSTRAINT fk_consistance FOREIGN KEY (id_consistance) REFERENCES consistance (idconsistance)
   ON UPDATE NO ACTION ON DELETE NO ACTION;
CREATE INDEX fki_consistance
  ON parcelle_d(id_consistance);
