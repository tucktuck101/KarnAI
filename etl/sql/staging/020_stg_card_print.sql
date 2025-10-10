-- Create staging table for card prints if not present
IF OBJECT_ID('dbo.stg_card_print') IS NULL
CREATE TABLE dbo.stg_card_print (
  id NVARCHAR(64) NOT NULL,
  oracle_id NVARCHAR(64) NULL,
  set_id NVARCHAR(32) NULL
);
