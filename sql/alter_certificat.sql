ALTER TABLE certificat
   ADD COLUMN idfokontany bigint;
ALTER TABLE certificat
  ADD CONSTRAINT fk_fokontany FOREIGN KEY (idfokontany) REFERENCES fokontany (idfokontany)
   ON UPDATE NO ACTION ON DELETE NO ACTION;
CREATE INDEX fki_fokontany
  ON certificat(idfokontany);
