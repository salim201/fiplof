ALTER TABLE parcelle_d
ADD COLUMN idcategorie bigint;

ALTER TABLE parcelle_d
ADD CONSTRAINT fk_parcelle_d_categorie FOREIGN KEY (idcategorie)
      REFERENCES categorie (idcategorie)