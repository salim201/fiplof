-- Check: geometry_valid_check

-- ALTER TABLE parcelle_d DROP CONSTRAINT geometry_valid_check;

ALTER TABLE parcelle_d
  ADD CONSTRAINT geometry_valid_check CHECK (st_isvalid(geom));