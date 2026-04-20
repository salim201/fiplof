ALTER TABLE parcelle_d
   ADD COLUMN etatparcelle_d smallint;
COMMENT ON COLUMN parcelle_d.etatparcelle_d
  IS '0 aucun
1 titre
2 cadastre
3 certificat
';
