SET NOCOUNT ON;
WITH x(v) AS (SELECT 'library' UNION ALL SELECT 'hand' UNION ALL SELECT 'battlefield' UNION ALL SELECT 'graveyard' UNION ALL SELECT 'exile' UNION ALL SELECT 'stack' UNION ALL SELECT 'command' UNION ALL SELECT 'ante')
INSERT INTO dbo.dim_zone(zone)
SELECT v FROM x WHERE NOT EXISTS (SELECT 1 FROM dbo.dim_zone d WHERE d.zone=x.v);
