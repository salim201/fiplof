INSERT INTO classe(idclasse, libelleclasse)
VALUES(1, 'Classe A'),(2, 'Classe B'),(3, 'Classe C'),(4, 'Classe D'),(5, 'Classe E');

ALTER TABLE classecategorieforfaitaire DROP CONSTRAINT fk_classecategorieforfaitaire_ty;

ALTER TABLE classecategorieforfaitaire DROP COLUMN debut, DROP COLUMN fin;

ALTER TABLE classecategorieforfaitaire
ADD COLUMN debut DATE,
ADD COLUMN fin DATE;

ALTER TABLE classecategorieforfaitaire DROP COLUMN valeurariary;

ALTER TABLE classecategorieforfaitaire
ADD COLUMN valeurariary INTEGER;

ALTER TABLE consistance ADD COLUMN valeurariary INTEGER;

ALTER TABLE categorie ADD COLUMN valeur_location_ha integer NOT NULL DEFAULT 0;

ALTER TABLE classecategorieforfaitaire
ADD COLUMN deb_ifpb DATE,
ADD COLUMN fin_ifpb DATE,
ADD COLUMN valeurariary_ifpb INTEGER;

alter table consistance ADD valeurariary_ifpb INTEGER;