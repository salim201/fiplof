DO $$
DECLARE
  rec RECORD;
  excluded_tables text[] := ARRAY['demandedetitrepoint', 'perimetrecadastre', 'propositiondomainepublique'];  -- liste des tables à exclure
BEGIN
  FOR rec IN
    SELECT
      s.relname AS sequence_name,
      d.refobjid::regclass AS table_name,
      a.attname AS column_name
    FROM pg_depend d
    JOIN pg_class s ON s.oid = d.objid AND s.relkind = 'S'
    JOIN pg_class t ON t.oid = d.refobjid AND t.relkind = 'r'
    JOIN pg_attribute a ON a.attrelid = d.refobjid AND a.attnum = d.refobjsubid
    WHERE d.refobjsubid > 0
      AND NOT (d.refobjid::regclass::text = ANY(excluded_tables))
  LOOP
    EXECUTE format(
      'SELECT setval(%L, COALESCE((SELECT MAX(%I) FROM %s), 0) + 1, false);',
      rec.sequence_name,
      rec.column_name,
      rec.table_name
    );
  END LOOP;
END;
$$;