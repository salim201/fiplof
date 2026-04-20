ALTER TABLE parcelle_d
   ADD COLUMN conversion smallint;
COMMENT ON COLUMN parcelle_d.conversion
  IS 'Valeur = 1 equivalent parcelle convertie en demande
Valeur = 2 equivalent parcelle convertie en Certficat';