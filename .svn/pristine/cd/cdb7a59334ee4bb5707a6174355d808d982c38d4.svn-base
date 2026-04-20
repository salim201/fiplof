ALTER TABLE impotparcelle
  DROP CONSTRAINT fk_impotparcelle_parcelle;
ALTER TABLE impotparcelle
  ADD CONSTRAINT fk_impotparcelle_parcelle FOREIGN KEY (idparcelle)
      REFERENCES parcelle_d (gid) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE impotparcelle
   ADD COLUMN etatpaiement smallint;
ALTER TABLE impotparcelle
   ADD COLUMN montantpayee money;
