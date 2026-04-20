ALTER TABLE titrefoncier DROP CONSTRAINT pk_titrefoncier;
ALTER TABLE titrefoncier DROP COLUMN idtitrefoncier;
ALTER TABLE titrefoncier ADD COLUMN gid BIGSERIAL;