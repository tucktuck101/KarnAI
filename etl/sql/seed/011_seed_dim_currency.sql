SET NOCOUNT ON;
WITH x(v) AS (SELECT 'USD' UNION ALL SELECT 'EUR' UNION ALL SELECT 'TIX')
INSERT INTO dbo.dim_currency(currency_code)
SELECT v FROM x WHERE NOT EXISTS (SELECT 1 FROM dbo.dim_currency d WHERE d.currency_code=x.v);
