DROP TABLE IF EXISTS public.journal;

CREATE SEQUENCE journal_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 51
  CACHE 1;
ALTER TABLE journal_id_seq
  OWNER TO postgres;


CREATE TABLE public.journal
(
   id bigint NOT NULL DEFAULT nextval('journal_id_seq'::regclass), 
   idutilisateur bigint, 
   idobjetcible bigint, 
   typeobjectcible character varying(100), 
   description character varying(150), 
   dateaction date, 
   heureaction time without time zone, 
   CONSTRAINT pk_journal PRIMARY KEY (id), 
   CONSTRAINT fk_journal_utilisateur FOREIGN KEY (idutilisateur) REFERENCES utilisateur (idutilisateur) ON UPDATE NO ACTION ON DELETE NO ACTION
) 
WITH (
  OIDS = FALSE
)
;
ALTER TABLE public.journal
  OWNER TO postgres;
  
