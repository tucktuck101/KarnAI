SET NOCOUNT ON;
WITH x(finish) AS (SELECT 'nonfoil' UNION ALL SELECT 'foil' UNION ALL SELECT 'etched' UNION ALL SELECT 'glossy')
INSERT INTO dbo.dim_finish(finish)
SELECT finish FROM x WHERE NOT EXISTS (SELECT 1 FROM dbo.dim_finish d WHERE d.finish=x.finish);
