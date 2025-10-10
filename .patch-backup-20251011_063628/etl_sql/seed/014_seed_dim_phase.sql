SET NOCOUNT ON;
WITH x(v) AS (SELECT 'beginning' UNION ALL SELECT 'precombat_main' UNION ALL SELECT 'combat' UNION ALL SELECT 'postcombat_main' UNION ALL SELECT 'ending')
INSERT INTO dbo.dim_phase(phase)
SELECT v FROM x WHERE NOT EXISTS (SELECT 1 FROM dbo.dim_phase d WHERE d.phase=x.v);
