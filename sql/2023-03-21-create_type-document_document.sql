
CREATE TABLE type_document(
   id_type SERIAL,
   libelle_type CHARACTER VARYING(128) ,
   PRIMARY KEY(id_type)
);


CREATE TABLE document(
   id_document BIGSERIAL,
   photo_document BYTEA,
   extension_document CHARACTER VARYING(10) ,
   num_page INTEGER,
   observation TEXT,
   id_type SMALLINT,
   iddemande BIGINT,
   PRIMARY KEY(id_document),
   FOREIGN KEY(id_type) REFERENCES type_document(id_type),
   FOREIGN KEY(iddemande) REFERENCES demande(iddemande)
);

