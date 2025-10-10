SET NOCOUNT ON;
WITH x(v) AS (
  SELECT 'untap' UNION ALL SELECT 'upkeep' UNION ALL SELECT 'draw' UNION ALL SELECT 'precombat_main'
  UNION ALL SELECT 'begin_combat' UNION ALL SELECT 'declare_attackers' UNION ALL SELECT 'declare_blockers'
  UNION ALL SELECT 'combat_damage' UNION ALL SELECT 'end_combat'
  UNION ALL SELECT 'postcombat_main' UNION ALL SELECT 'end' UNION ALL SELECT 'cleanup'
)
INSERT INTO dbo.dim_step(step)
SELECT v FROM x WHERE NOT EXISTS (SELECT 1 FROM dbo.dim_step d WHERE d.step=x.v);
