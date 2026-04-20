DROP  VIEW IF EXISTS public.vw_shape_demande;

CREATE OR REPLACE VIEW public.vw_shape_demande AS 
 WITH q1 AS (
         SELECT demande_1.iddemande,
            string_agg((((((((((((((((((((((((((((((concat(p_1.nompersonne, ' ', COALESCE(p_1.prenompersonne, ''::character varying)) || '<FIELD>'::text) || p_1.sexepersonne::text) || '<FIELD>'::text) || COALESCE(p_1.datenaissancepersonne, '1000-01-01'::date)) || '<FIELD>'::text) || COALESCE(p_1.nevers::integer, 0)) || '<FIELD>'::text) || COALESCE(p_1.numcipersonne, ''::character varying)::text) || '<FIELD>'::text) || COALESCE(p_1.numactenaissancepersonne, ''::character varying)::text) || '<FIELD>'::text) || COALESCE(p_1.datecipersonne, '1000-01-01'::date)) || '<FIELD>'::text) || COALESCE(p_1.lieucipersonne, ''::character varying)::text) || '<FIELD>'::text) || COALESCE(p_1.dateactenaissancepersonne, '1000-01-01'::date)) || '<FIELD>'::text) || COALESCE(p_1.lieuactenaissancepersonne, ''::character varying)::text) || '<FIELD>'::text) || COALESCE(p_1.adressepersonne, ''::character varying)::text) || '<FIELD>'::text) || COALESCE(p_1.nompere, ''::character varying)::text) || '<FIELD>'::text) || COALESCE(p_1.nommere, ''::character varying)::text) || '<FIELD>'::text) || COALESCE(p_1.conjoint, ''::character varying)::text) || '<FIELD>'::text) || p_1.idpersonne) || '<FIELD>'::text) || COALESCE(a.representant, false), '<ROW>'::text) AS demandeurs
           FROM demande demande_1
             LEFT JOIN avoir_demande a ON a.iddemande = demande_1.iddemande
             LEFT JOIN personne p_1 ON p_1.idpersonne = a.idpersonne
          GROUP BY demande_1.iddemande
        )
 SELECT p.geom,
    COALESCE(demande.code_parcelle, ''::character varying) AS c_parcelle,
    demande.numdemande,
    demande.datedemande,
    p.surface,
    COALESCE(demande.region) AS "coalesce",
    demande.district,
    com.nomcommune,
    fkt.nomfokontany,
    COALESCE(demande.lieudit, ''::character varying) AS lieudit,
    demande.categorie,
    demande.consistance,
    q1.demandeurs,
    COALESCE(h.codehameau, ''::character varying) AS codehameau,
    COALESCE(h.nomhameau, ''::character varying) AS nomhameau
   FROM demande
     JOIN q1 ON q1.iddemande = demande.iddemande
     JOIN parcelle_d p ON p.gid = demande.gid
     JOIN commune com ON com.idcommune = demande.idcommune
     LEFT JOIN fokontany fkt ON fkt.idfokontany = demande.idfokontany
     LEFT JOIN hameau h ON h.idhameau = p.idhameau
  WHERE demande.numdemande IS NOT NULL;
  
  
ALTER TABLE public.vw_shape_demande
  OWNER TO postgres;
