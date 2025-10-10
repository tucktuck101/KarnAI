-- Seed colors
INSERT INTO dbo.dim_color(code) VALUES
('W'),('U'),('B'),('R'),('G'),('C')
WHERE NOT EXISTS (SELECT 1 FROM dbo.dim_color);
