SET NOCOUNT ON;
WITH x(v) AS (SELECT 'infinite_mana' UNION ALL SELECT 'infinite_damage' UNION ALL SELECT 'infinite_tokens' UNION ALL SELECT 'win_the_game' UNION ALL SELECT 'lock' UNION ALL SELECT 'resource_denial' UNION ALL SELECT 'tutor_loop')
INSERT INTO dbo.dim_combo_result(result_code)
SELECT v FROM x WHERE NOT EXISTS (SELECT 1 FROM dbo.dim_combo_result d WHERE d.result_code=x.v);
