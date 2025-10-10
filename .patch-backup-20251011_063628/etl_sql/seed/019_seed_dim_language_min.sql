SET NOCOUNT ON;
IF NOT EXISTS (SELECT 1 FROM dbo.dim_language WHERE lang_code='en')
  INSERT INTO dbo.dim_language(lang_code,name) VALUES ('en','English');
