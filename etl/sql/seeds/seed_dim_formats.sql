-- Seed formats
INSERT INTO dbo.dim_format(format_name) VALUES
('commander'),('oathbreaker'),('vintage'),('legacy'),('modern')
WHERE NOT EXISTS (SELECT 1 FROM dbo.dim_format);
