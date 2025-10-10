MERGE dbo.dim_card_type AS t
USING (SELECT DISTINCT value AS card_type FROM dbo.stg_catalog WHERE catalog='card-types') s
ON (t.card_type=s.card_type) WHEN NOT MATCHED THEN INSERT(card_type) VALUES(s.card_type);
