-- MERGE card_print from stg_card_print (minimal)
MERGE dbo.card_print AS tgt
USING (SELECT id, oracle_id, set_id FROM dbo.stg_card_print) AS src
ON (tgt.id = src.id)
WHEN NOT MATCHED BY TARGET THEN
  INSERT (id, oracle_id, set_id) VALUES (src.id, src.oracle_id, src.set_id)
WHEN MATCHED AND (ISNULL(tgt.oracle_id,'') <> ISNULL(src.oracle_id,'')
   OR ISNULL(tgt.set_id,'') <> ISNULL(src.set_id,'')) THEN
  UPDATE SET oracle_id = src.oracle_id, set_id = src.set_id;
