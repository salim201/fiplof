delete from actedeces; SELECT setval('public.actedeces_id_seq', 1, false);
delete from acteprive; SELECT setval('public.acteprive_id_seq', 1, false);
delete from actepublic; SELECT setval('public.actepublic_id_seq', 1, false);
delete from aireastatutspecifique;
delete from autrecharge;
delete from servitudebeneficiaire ;
delete from beneficiaire; SELECT setval('public.beneficiaire_id_seq', 1, false);
delete from avoir_dmd;
delete from avoir_demande;
delete from demande; SELECT setval('public.iddemande_seq', 1, false);
delete from servitudeparcelle_d ; 
delete from parcelle; SELECT setval('public.parcelle_id_seq', 1, false);
delete from proprietaireparcelle_d ;
delete from limitesparcelle;
delete from proprietaireparcelle; 
delete from parcelle_d; SELECT setval('public.parcelle_d_id_seq', 1, false);
delete from classecategorieforfaitaire ;
delete from categorie; SELECT setval('public.categorie_id_seq', 1, false);
delete from certificat; 

-- delete from crd;
delete from decision; SELECT setval('public.decision_id_seq', 1, false);

delete from demandedetitrepoint; SELECT setval('public.demandedetitrepoint_id_seq', 1, false);
delete from demandeur_d; SELECT setval('public.demandeur_d_id_seq1', 1, false);
delete from domainepublique;
delete from historique;
delete from hypotheque;
delete from impot; SELECT setval('public.impot_id_seq', 1, false);
delete from impotparcelle;
delete from journal;
-- delete from limcommanjozorobe;
delete from limitesparcelle;
delete from occupant_titrefoncier;
delete from occupant;
delete from operationsubsequente; SELECT setval('public.operationsubsequente_id_seq', 1, false);
delete from oppositions; SELECT setval('public.oppositions_id_seq', 1, false);

delete from parcellecadastreencours; SELECT setval('public.parcellecadastreencours_id_seq', 1, false);
delete from parcelledemandedetitre; SELECT setval('public.parcelledemandedetitre_id_seq', 1, false);
delete from servitudeparcellegrevees;
delete from parcellegrevees; SELECT setval('public.parcellegrevees_id_seq', 1, false);
delete from perimetrecadastre; SELECT setval('public.perimetrecadastre_id_seq', 1, false);
delete from personnemorale;
delete from personnemoraleparcelle;
delete from personnemoraleparcelle_d;
delete from personnephysique; SELECT setval('public.personnephysique_id_seq', 1, false);
delete from rejet; SELECT setval('public.rejet_id_seq', 1, false);
delete from servitude;
-- drop table if exists titre_sylvio_arivonimamo_i;
delete from titrefoncier;

delete from hameau; SELECT setval('public.hameau_id_seq', 1, false);
delete from fokontany; SELECT setval('public.fokontany_id_seq', 1, false);
delete from commune; SELECT setval('public.commune_id_seq', 1, false);
delete from district; SELECT setval('public.district_id_seq', 1, false);
delete from region; SELECT setval('public.region_id_seq', 1, false);

delete from certificat; SELECT setval('public.certificat_idcertificat_seq', 1, false);

delete from projet; SELECT setval('public.projet_idprojet_seq', 1, false);
delete from projetcouche; SELECT setval('public.projetcouche_id_seq', 1, false);
delete from personne; SELECT setval('personne_idpersonne_seq', 1, false);