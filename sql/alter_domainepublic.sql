ALTER TABLE domainepublique DROP COLUMN iddomainepublique;
ALTER TABLE domainepublique ADD COLUMN iddomainepublique BIGSERIAL;
ALTER TABLE domainepublique
  ADD CONSTRAINT pk_domainepublique PRIMARY KEY (iddomainepublique);
ALTER TABLE domainepublique ADD COLUMN geom geometry;