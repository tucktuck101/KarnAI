SET NOCOUNT ON;
WITH x(v) AS (SELECT 'small' UNION ALL SELECT 'normal' UNION ALL SELECT 'large' UNION ALL SELECT 'png' UNION ALL SELECT 'art_crop' UNION ALL SELECT 'border_crop')
INSERT INTO dbo.dim_uri_kind(uri_kind)
SELECT v FROM x WHERE NOT EXISTS (SELECT 1 FROM dbo.dim_uri_kind d WHERE d.uri_kind=x.v);
