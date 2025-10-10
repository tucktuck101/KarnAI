SET NOCOUNT ON;
WITH x(v,n) AS (SELECT 1,'Scryfall' UNION ALL SELECT 2,'TCGplayer' UNION ALL SELECT 3,'Cardmarket' UNION ALL SELECT 4,'Cardhoarder')
INSERT INTO dbo.dim_vendor(vendor_id,name)
SELECT v,n FROM x WHERE NOT EXISTS (SELECT 1 FROM dbo.dim_vendor d WHERE d.vendor_id=x.v);
