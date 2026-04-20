DO $$ 
DECLARE
    r RECORD;
    column_exists BOOLEAN;
BEGIN
    -- Parcours de toutes les tables du schéma public (en excluant les vues et les tables système)
    FOR r IN 
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'  -- Utilisez votre schéma si nécessaire, ici 'public'
        AND table_type = 'BASE TABLE'  -- Exclut les vues et autres objets non-table
    LOOP
        -- Vérifier si la colonne 'datemaj' existe déjà dans la table
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_schema = 'public' 
            AND table_name = r.table_name
            AND column_name = 'datemaj'
        ) INTO column_exists;

        -- Si la colonne 'datemaj' n'existe pas, on l'ajoute
        IF NOT column_exists THEN
            EXECUTE 'ALTER TABLE public.' || r.table_name || ' ADD COLUMN datemaj TIMESTAMP DEFAULT CURRENT_TIMESTAMP';
        END IF;
    END LOOP;
END $$;


CREATE OR REPLACE FUNCTION update_datemaj()
RETURNS TRIGGER AS $$
BEGIN
    NEW.datemaj = CURRENT_TIMESTAMP;  -- Définit la valeur de datemaj à l'heure actuelle lors d'une mise à jour
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 3. Créer les triggers pour mettre à jour la colonne datemaj à chaque mise à jour de ligne
DO $$ 
DECLARE
    r RECORD;
BEGIN
    -- Parcours de toutes les tables du schéma public (en excluant les vues et les tables système)
    FOR r IN 
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'  -- Utilisez votre schéma si nécessaire, ici 'public'
        AND table_type = 'BASE TABLE'  -- Exclut les vues et autres objets non-table
    LOOP
        -- Créer le trigger pour mettre à jour 'datemaj' à chaque mise à jour de ligne
        EXECUTE 'CREATE TRIGGER update_' || r.table_name || '_datemaj
                 BEFORE UPDATE ON public.' || r.table_name || '
                 FOR EACH ROW EXECUTE PROCEDURE update_datemaj()';  -- Syntaxe correcte pour PostgreSQL 9.x
    END LOOP;
END $$;


CREATE TABLE date_synchro (
    id_synchro SERIAL PRIMARY KEY,  -- Clé primaire auto-incrémentée
    date_synchro TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Date de synchronisation avec la valeur par défaut de l'heure actuelle
);