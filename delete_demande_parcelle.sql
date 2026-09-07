BEGIN;

-- =====================================
-- DERNIER GID
-- =====================================

-- blob_personne
DELETE FROM public.blob_personne
WHERE idpersonne IN (
    SELECT ad.idpersonne
    FROM public.avoir_demande ad
    WHERE ad.idparcelle = (
        SELECT MAX(gid)
        FROM public.parcelle_d
    )
);

-- proprietaireparcelle
DELETE FROM public.proprietaireparcelle
WHERE idpersonne IN (
    SELECT ad.idpersonne
    FROM public.avoir_demande ad
    WHERE ad.idparcelle = (
        SELECT MAX(gid)
        FROM public.parcelle_d
    )
);

-- avoir_demande par iddemande
DELETE FROM public.avoir_demande
WHERE iddemande IN (
    SELECT iddemande
    FROM public.demande
    WHERE gid = (
        SELECT MAX(gid)
        FROM public.parcelle_d
    )
);

-- IMPORTANT : avoir_demande par parcelle
DELETE FROM public.avoir_demande
WHERE idparcelle = (
    SELECT MAX(gid)
    FROM public.parcelle_d
);

-- limitesparcelle
DELETE FROM public.limitesparcelle
WHERE idparcelle = (
    SELECT MAX(gid)
    FROM public.parcelle_d
);

-- voisinparcelle
DELETE FROM public.voisinparcelle
WHERE idpacelle = (
    SELECT MAX(gid)
    FROM public.parcelle_d
);

-- demande
DELETE FROM public.demande
WHERE gid = (
    SELECT MAX(gid)
    FROM public.parcelle_d
);

-- personnes orphelines
DELETE FROM public.personne
WHERE idpersonne NOT IN (
    SELECT DISTINCT idpersonne
    FROM public.avoir_demande
)
AND idpersonne NOT IN (
    SELECT DISTINCT idpersonne
    FROM public.proprietaireparcelle
);

-- parcelle_d
DELETE FROM public.parcelle_d
WHERE gid = (
    SELECT MAX(gid)
    FROM public.parcelle_d
);

COMMIT;