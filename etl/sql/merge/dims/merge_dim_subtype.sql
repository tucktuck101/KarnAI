MERGE dbo.dim_subtype AS t
USING (
  SELECT DISTINCT value AS subtype FROM dbo.stg_catalog
  WHERE catalog IN ('artifact-types','creature-types','enchantment-types','land-types','planeswalker-types','spell-types')
) s ON (t.subtype=s.subtype)
WHEN NOT MATCHED THEN INSERT(subtype) VALUES(s.subtype);
