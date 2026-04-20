ALTER TABLE public.projetcouche
   ADD COLUMN label_name character varying(64);

ALTER TABLE public.projetcouche
   ADD COLUMN show_label boolean;

ALTER TABLE public.projetcouche
   ADD COLUMN font character varying(64);

ALTER TABLE public.projetcouche
   ADD COLUMN font_size smallint;

ALTER TABLE public.projetcouche
   ADD COLUMN font_size_map_unit boolean;

ALTER TABLE public.projetcouche
   ADD COLUMN font_color character varying(7);

ALTER TABLE public.projetcouche
   ADD COLUMN show_stroke boolean;

ALTER TABLE public.projetcouche
   ADD COLUMN stroke_width smallint;

ALTER TABLE public.projetcouche
   ADD COLUMN stroke_color character varying(7);
