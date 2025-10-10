IF OBJECT_ID('dbo.stg_catalog') IS NULL
BEGIN
  CREATE TABLE dbo.stg_catalog(
    catalog NVARCHAR(64) NOT NULL,
    value   NVARCHAR(200) NOT NULL
  );
END;
