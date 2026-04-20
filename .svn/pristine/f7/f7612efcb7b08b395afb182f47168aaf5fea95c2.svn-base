CREATE SEQUENCE public.param_layer_id_seq;
ALTER SEQUENCE public.param_layer_id_seq
  OWNER TO postgres;


CREATE TABLE public.param_layer
(
  id integer NOT NULL DEFAULT nextval('param_layer_id_seq'::regclass),
  label_font character varying(64),
  label_size smallint,
  label_color character varying(7),
  stroke_size smallint,
  stroke_color character varying(7),
  layer_index smallint,
  font_size_map_units boolean,
  CONSTRAINT param_layer_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.param_layer
  OWNER TO postgres;

