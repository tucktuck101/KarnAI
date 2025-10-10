-- Seed uri kinds
INSERT INTO dbo.dim_uri_kind(uri_kind) VALUES
('art_crop'),('large'),('normal'),('png'),('small')
WHERE NOT EXISTS (SELECT 1 FROM dbo.dim_uri_kind);
