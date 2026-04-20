ALTER TABLE titrefoncier DROP COLUMN objectid;
ALTER TABLE titrefoncier ADD COLUMN idtitrefoncier BIGSERIAL;
ALTER TABLE titrefoncier
  ADD CONSTRAINT pk_titrefoncier PRIMARY KEY (idtitrefoncier);
ALTER TABLE titrefoncier ADD COLUMN geom geometry;