-- MERGE oracle_card from stg_oracle_card
MERGE dbo.oracle_card AS tgt
USING (SELECT oracle_id, oracle_name FROM dbo.stg_oracle_card) AS src
ON (tgt.oracle_id = src.oracle_id)
WHEN NOT MATCHED BY TARGET THEN
  INSERT (oracle_id, oracle_name) VALUES (src.oracle_id, src.oracle_name)
WHEN MATCHED AND (ISNULL(tgt.oracle_name,'') <> ISNULL(src.oracle_name,'')) THEN
  UPDATE SET oracle_name = src.oracle_name;
