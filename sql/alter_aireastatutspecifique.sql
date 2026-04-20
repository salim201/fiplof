ALTER TABLE aireastatutspecifique DROP COLUMN idaireastatuspecifique;
ALTER TABLE aireastatutspecifique ADD COLUMN idaireastatutspecifique BIGSERIAL;
ALTER TABLE aireastatutspecifique
  ADD CONSTRAINT pk_aire PRIMARY KEY (idaireastatutspecifique);
ALTER TABLE aireastatutspecifique ADD COLUMN geom geometry;