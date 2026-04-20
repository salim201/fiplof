   
ALTER TABLE avoir_demande DROP CONSTRAINT pk_avoir_demande;

ALTER TABLE avoir_demande
  ADD CONSTRAINT pk_avoir_demande PRIMARY KEY(idpersonne, idparcelle);
  
ALTER TABLE avoir_demande
   ALTER COLUMN iddemande DROP NOT NULL;