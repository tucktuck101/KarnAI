-- Create staging table for oracle cards if not present
IF OBJECT_ID('dbo.stg_oracle_card') IS NULL
CREATE TABLE dbo.stg_oracle_card (
  oracle_id NVARCHAR(64) NOT NULL,
  oracle_name NVARCHAR(200) NULL
);
