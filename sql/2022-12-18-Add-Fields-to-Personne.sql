ALTER TABLE public.personne
    ADD COLUMN handicap boolean DEFAULT False;

ALTER TABLE public.personne
    ADD COLUMN niveau_education text;

ALTER TABLE public.personne
    ADD COLUMN possede_emploi boolean DEFAULT True;

ALTER TABLE public.personne
    ADD COLUMN migrant boolean DEFAULT False;

ALTER TABLE public.personne
    ADD COLUMN date_arrivee date;