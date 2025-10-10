SET NOCOUNT ON;
WITH x(v) AS (SELECT 'stax' UNION ALL SELECT 'storm' UNION ALL SELECT 'mill' UNION ALL SELECT 'reanimation' UNION ALL SELECT 'extra_turns' UNION ALL SELECT 'treasure' UNION ALL SELECT 'infinite_combat')
INSERT INTO dbo.dim_combo_tag(tag)
SELECT v FROM x WHERE NOT EXISTS (SELECT 1 FROM dbo.dim_combo_tag d WHERE d.tag=x.v);
