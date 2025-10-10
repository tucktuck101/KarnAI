SET NOCOUNT ON;
WITH x(format_name) AS (
  SELECT 'standard' UNION ALL SELECT 'future' UNION ALL SELECT 'historic' UNION ALL SELECT 'timeless'
  UNION ALL SELECT 'gladiator' UNION ALL SELECT 'pioneer' UNION ALL SELECT 'modern' UNION ALL SELECT 'legacy'
  UNION ALL SELECT 'pauper' UNION ALL SELECT 'vintage' UNION ALL SELECT 'penny' UNION ALL SELECT 'commander'
  UNION ALL SELECT 'oathbreaker' UNION ALL SELECT 'standardbrawl' UNION ALL SELECT 'brawl' UNION ALL SELECT 'alchemy'
  UNION ALL SELECT 'paupercommander' UNION ALL SELECT 'duel' UNION ALL SELECT 'oldschool' UNION ALL SELECT 'premodern'
  UNION ALL SELECT 'explorer' UNION ALL SELECT 'historicbrawl' UNION ALL SELECT 'predh'
)
INSERT INTO dbo.dim_format(format_name)
SELECT format_name FROM x WHERE NOT EXISTS (SELECT 1 FROM dbo.dim_format d WHERE d.format_name=x.format_name);
