ALTER TABLE public.configuration
   ADD COLUMN date_dernier_maj timestamp without time zone;
ALTER TABLE public.configuration
   ADD COLUMN date_dernier_autobackup timestamp without time zone;

CREATE OR REPLACE FUNCTION update_date_dernier_maj() 
RETURNS TRIGGER AS $$
BEGIN
    -- Mettre à jour la colonne date_dernier_maj dans la table configuration
    UPDATE configuration
    SET date_dernier_maj = CURRENT_TIMESTAMP
    WHERE id_configuration=(SELECT MIN(id_configuration) FROM configuration);  -- Assure-toi de cibler la bonne ligne (ici, par exemple, la ligne avec id = 1)
    
    -- Retourner la ligne affectée pour le trigger
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;


DO $$ 
DECLARE
    r RECORD;
BEGIN
    -- Boucle sur toutes les tables de la base de données
    FOR r IN (SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE' AND table_name <> 'configuration') 
    LOOP
        -- Créer un trigger pour chaque table
        EXECUTE format('
            CREATE TRIGGER trigger_update_date_dernier_maj
            AFTER INSERT OR UPDATE OR DELETE ON %I
            FOR EACH ROW EXECUTE PROCEDURE update_date_dernier_maj();',
            r.table_name);
    END LOOP;
END $$;
