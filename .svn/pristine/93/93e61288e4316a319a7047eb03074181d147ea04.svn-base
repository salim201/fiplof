CREATE TABLE public.configuration
(
   id_configuration bigserial, 
   host_remote character varying(128), 
   port_remote character varying(128), 
   user_remote character varying(128), 
   password_remote text, 
   dbname_remote character varying(128), 
   host_backup character varying(128), 
   port_backup character varying(128), 
   user_backup character varying(128), 
   password_backup text, 
   dbname_backup character varying(128), 
   auto_save_path text, 
   has_z_certifiable boolean NOT NULL DEFAULT FALSE, 
   online_interco boolean NOT NULL DEFAULT FALSE, 
   CONSTRAINT pk_configuration PRIMARY KEY (id_configuration)
) 
WITH (
  OIDS = FALSE
)
;
ALTER TABLE public.configuration
  OWNER TO postgres;