SET NOCOUNT ON;
WITH x(v) AS (
  SELECT 'match_created' UNION ALL SELECT 'match_started' UNION ALL SELECT 'match_ended'
  UNION ALL SELECT 'game_started' UNION ALL SELECT 'game_ended'
  UNION ALL SELECT 'draw' UNION ALL SELECT 'play' UNION ALL SELECT 'cast' UNION ALL SELECT 'activate' UNION ALL SELECT 'trigger' UNION ALL SELECT 'resolve'
  UNION ALL SELECT 'move_zone' UNION ALL SELECT 'attack' UNION ALL SELECT 'block' UNION ALL SELECT 'damage' UNION ALL SELECT 'life_change'
  UNION ALL SELECT 'counter_add' UNION ALL SELECT 'counter_remove' UNION ALL SELECT 'scry' UNION ALL SELECT 'mill' UNION ALL SELECT 'shuffle'
)
INSERT INTO dbo.dim_event_type(event_type)
SELECT v FROM x WHERE NOT EXISTS (SELECT 1 FROM dbo.dim_event_type d WHERE d.event_type=x.v);
