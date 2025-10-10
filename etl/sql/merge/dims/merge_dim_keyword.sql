MERGE dbo.dim_keyword AS t
USING (
  SELECT DISTINCT value AS keyword FROM dbo.stg_catalog
  WHERE catalog IN ('keyword-abilities','keyword-actions')
) s ON (t.keyword=s.keyword)
WHEN NOT MATCHED THEN INSERT(keyword) VALUES(s.keyword);
