MERGE dbo.dim_supertype AS t
USING (SELECT DISTINCT value AS supertype FROM dbo.stg_catalog WHERE catalog='supertypes') s
ON (t.supertype=s.supertype) WHEN NOT MATCHED THEN INSERT(supertype) VALUES(s.supertype);
