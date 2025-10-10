MERGE dbo.dim_watermark AS t
USING (SELECT DISTINCT value AS watermark FROM dbo.stg_catalog WHERE catalog='watermarks') s
ON (t.watermark=s.watermark) WHEN NOT MATCHED THEN INSERT(watermark) VALUES(s.watermark);
