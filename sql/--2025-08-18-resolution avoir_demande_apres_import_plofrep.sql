--SELECT d.gid, d.iddemande,d.numdemande,d.nomdemandeur, p.idpersonne, TRUE FROM demande d, personne p WHERE gid NOT IN (SELECT idparcelle FROM avoir_demande) AND d.nomdemandeur IS NOT NULL AND TRIM(CONCAT(p.nompersonne,' ',p.prenompersonne)) = TRIM (d.nomdemandeur) ORDER BY p.idpersonne;
INSERT INTO avoir_demande (idparcelle, iddemande, idpersonne,representant) SELECT d.gid, d.iddemande, idpersonne, TRUE FROM demande d, personne p WHERE gid NOT IN (SELECT idparcelle FROM avoir_demande) AND d.nomdemandeur IS NOT NULL AND UPPER(TRIM(CONCAT(p.nompersonne,' ',p.prenompersonne))) = UPPER(TRIM (d.nomdemandeur)) ORDER BY p.idpersonne;
INSERT INTO proprietaireparcelle (idparcelle, idpersonne, representant) SELECT d.gid, idpersonne, TRUE FROM demande d, personne p WHERE gid NOT IN (SELECT idparcelle FROM proprietaireparcelle) AND d.nomdemandeur IS NOT NULL AND UPPER(TRIM(CONCAT(p.nompersonne,' ',p.prenompersonne))) = UPPER(TRIM (d.nomdemandeur)) ORDER BY p.idpersonne;
--SELECT d.numdemande,d.nomdemandeur FROM demande d WHERE gid IN (SELECT idparcelle FROM avoir_demande) ORDER BY d.iddemande;
--SELECT numerocertificat FROM certificat WHERE idcertificat IN (SELECT idcertificat FROM parcelle_d WHERE gid NOT IN (SELECT idparcelle FROM proprietaireparcelle));
INSERT INTO avoir_demande (idparcelle, iddemande, idpersonne,representant) SELECT d.gid, d.iddemande, pp.idpersonne, TRUE FROM demande d, proprietaireparcelle pp WHERE gid NOT IN (SELECT idparcelle FROM avoir_demande) AND pp.idparcelle = d.gid ORDER BY pp.idpersonne;
UPDATE demande
SET idfokontany = (
    SELECT DISTINCT certificat.idfokontany
    FROM certificat
    WHERE TRIM(certificat.numerodemande) = TRIM(demande.numdemande) LIMIT 1
);

