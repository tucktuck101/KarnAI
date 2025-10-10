-- Part 0: reset and create database KarnAI
USE master;
GO
IF DB_ID(N'KarnAI') IS NOT NULL
BEGIN
  ALTER DATABASE [KarnAI] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
  DROP DATABASE [KarnAI];
END
GO
CREATE DATABASE [KarnAI];
GO
USE [KarnAI];
GO

-- Part 1: schema and dimensions
IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'dbo') EXEC('CREATE SCHEMA dbo');
GO

-- Dimensions
CREATE TABLE dbo.dim_color (code NVARCHAR(10) NOT NULL, CONSTRAINT PK_dim_color PRIMARY KEY (code));
CREATE TABLE dbo.dim_keyword (keyword NVARCHAR(100) NOT NULL, CONSTRAINT PK_dim_keyword PRIMARY KEY (keyword));
CREATE TABLE dbo.dim_format (format_name NVARCHAR(100) NOT NULL, CONSTRAINT PK_dim_format PRIMARY KEY (format_name));
CREATE TABLE dbo.dim_watermark (watermark NVARCHAR(100) NOT NULL, CONSTRAINT PK_dim_watermark PRIMARY KEY (watermark));
CREATE TABLE dbo.dim_supertype (supertype NVARCHAR(100) NOT NULL, CONSTRAINT PK_dim_supertype PRIMARY KEY (supertype));
CREATE TABLE dbo.dim_card_type (card_type NVARCHAR(100) NOT NULL, CONSTRAINT PK_dim_card_type PRIMARY KEY (card_type));
CREATE TABLE dbo.dim_subtype (subtype NVARCHAR(100) NOT NULL, CONSTRAINT PK_dim_subtype PRIMARY KEY (subtype));
CREATE TABLE dbo.dim_finish (finish NVARCHAR(50) NOT NULL, CONSTRAINT PK_dim_finish PRIMARY KEY (finish));
CREATE TABLE dbo.dim_currency (currency_code NVARCHAR(10) NOT NULL, CONSTRAINT PK_dim_currency PRIMARY KEY (currency_code));
CREATE TABLE dbo.dim_theme (theme_id INT NOT NULL, theme_name NVARCHAR(200), theme_kind NVARCHAR(100), CONSTRAINT PK_dim_theme PRIMARY KEY (theme_id));
CREATE TABLE dbo.dim_combo_result (result_code NVARCHAR(50) NOT NULL, CONSTRAINT PK_dim_combo_result PRIMARY KEY (result_code));
CREATE TABLE dbo.dim_combo_tag (tag NVARCHAR(100) NOT NULL, CONSTRAINT PK_dim_combo_tag PRIMARY KEY (tag));
CREATE TABLE dbo.dim_vendor (vendor_id INT NOT NULL, name NVARCHAR(200), CONSTRAINT PK_dim_vendor PRIMARY KEY (vendor_id));
CREATE TABLE dbo.dim_language (lang_code NVARCHAR(16) NOT NULL, name NVARCHAR(100), CONSTRAINT PK_dim_language PRIMARY KEY (lang_code));
CREATE TABLE dbo.dim_event_type (event_type NVARCHAR(100) NOT NULL, CONSTRAINT PK_dim_event_type PRIMARY KEY (event_type));
CREATE TABLE dbo.dim_phase (phase NVARCHAR(50) NOT NULL, CONSTRAINT PK_dim_phase PRIMARY KEY (phase));
CREATE TABLE dbo.dim_step (step NVARCHAR(50) NOT NULL, CONSTRAINT PK_dim_step PRIMARY KEY (step));
CREATE TABLE dbo.dim_zone (zone NVARCHAR(50) NOT NULL, CONSTRAINT PK_dim_zone PRIMARY KEY (zone));
CREATE TABLE dbo.dim_token (
  token_id INT NOT NULL, name NVARCHAR(200), type_line NVARCHAR(200),
  power NVARCHAR(16), toughness NVARCHAR(16), color_mask NVARCHAR(10),
  CONSTRAINT PK_dim_token PRIMARY KEY (token_id)
);
CREATE TABLE dbo.dim_uri_kind (uri_kind NVARCHAR(50) NOT NULL, CONSTRAINT PK_dim_uri_kind PRIMARY KEY (uri_kind));
GO

-- Part 2: ETL backbone and audit, staging, history
CREATE TABLE dbo.etl_run (
  run_id INT NOT NULL, source_name NVARCHAR(100), bulk_type NVARCHAR(100), bulk_url NVARCHAR(500),
  file_sha256_hex NVARCHAR(64), started_at_utc DATETIME2(0), finished_at_utc DATETIME2(0), status NVARCHAR(50),
  CONSTRAINT PK_etl_run PRIMARY KEY (run_id)
);
GO
CREATE TABLE dbo.audit_event (
  event_id NVARCHAR(64) NOT NULL, source NVARCHAR(100), actor NVARCHAR(100),
  note NVARCHAR(1000), recorded_at DATETIME2(0), run_id INT,
  CONSTRAINT PK_audit_event PRIMARY KEY (event_id),
  CONSTRAINT FK_audit_event_run FOREIGN KEY (run_id) REFERENCES dbo.etl_run(run_id)
);
GO
CREATE TABLE dbo.etl_run_stat (
  run_id INT NOT NULL, table_name NVARCHAR(128) NOT NULL, inserted INT, updated INT, deleted INT,
  CONSTRAINT PK_etl_run_stat PRIMARY KEY (run_id, table_name),
  CONSTRAINT FK_ers_run FOREIGN KEY (run_id) REFERENCES dbo.etl_run(run_id)
);
CREATE TABLE dbo.etl_change (
  change_id INT NOT NULL, run_id INT, table_name NVARCHAR(128), op NVARCHAR(10), pk_text NVARCHAR(400),
  CONSTRAINT PK_etl_change PRIMARY KEY (change_id),
  CONSTRAINT FK_ec_run FOREIGN KEY (run_id) REFERENCES dbo.etl_run(run_id)
);
-- Fix: avoid 900-byte clustered key overflow by making PK NONCLUSTERED and adding a smaller clustered index.
CREATE TABLE dbo.etl_validation_issue (
  run_id INT NOT NULL, table_name NVARCHAR(128) NOT NULL, pk_text NVARCHAR(400) NOT NULL,
  column_name NVARCHAR(128) NOT NULL, issue_code NVARCHAR(64) NOT NULL,
  CONSTRAINT PK_etl_validation_issue PRIMARY KEY NONCLUSTERED (run_id, table_name, pk_text, column_name, issue_code),
  CONSTRAINT FK_evi_run FOREIGN KEY (run_id) REFERENCES dbo.etl_run(run_id)
);
CREATE CLUSTERED INDEX IX_evi_run_table ON dbo.etl_validation_issue(run_id, table_name);
GO
CREATE TABLE dbo.stg_card_print (id NVARCHAR(64) NOT NULL, oracle_id NVARCHAR(64), set_id NVARCHAR(32),
  CONSTRAINT PK_stg_card_print PRIMARY KEY (id)
);
GO
-- History tables (depend on audit_event only)
CREATE TABLE dbo.card_print_hist (
  id NVARCHAR(64) NOT NULL, valid_from NVARCHAR(25) NOT NULL, valid_to NVARCHAR(25),
  recorded_at NVARCHAR(25), oracle_id NVARCHAR(64), set_id NVARCHAR(32), released_at DATE,
  layout NVARCHAR(50), watermark NVARCHAR(100), collector_number NVARCHAR(50),
  rarity NVARCHAR(50), frame NVARCHAR(50), border_color NVARCHAR(50), card_back_id NVARCHAR(64),
  highres_image BIT, image_status NVARCHAR(50), reserved BIT, game_changer BIT, foil BIT,
  nonfoil BIT, oversized BIT, promo BIT, reprint BIT, variation BIT, digital BIT,
  edhrec_rank INT, penny_rank INT, change_hash NVARCHAR(64), event_id NVARCHAR(64),
  CONSTRAINT PK_card_print_hist PRIMARY KEY (id, valid_from),
  CONSTRAINT FK_cph_event FOREIGN KEY (event_id) REFERENCES dbo.audit_event(event_id)
);
CREATE TABLE dbo.card_face_hist (
  face_id INT NOT NULL, valid_from NVARCHAR(25) NOT NULL, valid_to NVARCHAR(25), recorded_at NVARCHAR(25),
  card_id NVARCHAR(64), face_index INT, mana_cost NVARCHAR(100), cmc FLOAT, power NVARCHAR(16), toughness NVARCHAR(16),
  change_hash NVARCHAR(64), event_id NVARCHAR(64),
  CONSTRAINT PK_card_face_hist PRIMARY KEY (face_id, valid_from),
  CONSTRAINT FK_cfh_event FOREIGN KEY (event_id) REFERENCES dbo.audit_event(event_id)
);
CREATE TABLE dbo.card_legality_hist (
  card_id NVARCHAR(64) NOT NULL, format_name NVARCHAR(100) NOT NULL, valid_from NVARCHAR(25) NOT NULL,
  valid_to NVARCHAR(25), recorded_at NVARCHAR(25), status NVARCHAR(50), change_hash NVARCHAR(64), event_id NVARCHAR(64),
  CONSTRAINT PK_card_legality_hist PRIMARY KEY (card_id, format_name, valid_from),
  CONSTRAINT FK_clh_event FOREIGN KEY (event_id) REFERENCES dbo.audit_event(event_id)
);
CREATE TABLE dbo.set_membership_hist (
  entity NVARCHAR(50) NOT NULL, entity_id NVARCHAR(64) NOT NULL, member NVARCHAR(64) NOT NULL,
  valid_from NVARCHAR(25) NOT NULL, valid_to NVARCHAR(25), recorded_at NVARCHAR(25),
  change_hash NVARCHAR(64), event_id NVARCHAR(64),
  CONSTRAINT PK_set_membership_hist PRIMARY KEY (entity, entity_id, member, valid_from),
  CONSTRAINT FK_smh_event FOREIGN KEY (event_id) REFERENCES dbo.audit_event(event_id)
);
GO

-- Part 3: Sets, Oracle, Prints, Faces, Localizations, URIs
CREATE TABLE dbo.mtgs_set (
  set_id NVARCHAR(32) NOT NULL, code NVARCHAR(16), name NVARCHAR(200), set_type NVARCHAR(50),
  CONSTRAINT PK_mtgs_set PRIMARY KEY (set_id)
);
CREATE TABLE dbo.oracle_card (oracle_id NVARCHAR(64) NOT NULL, oracle_name NVARCHAR(200), CONSTRAINT PK_oracle_card PRIMARY KEY (oracle_id));

CREATE TABLE dbo.card_print (
  id NVARCHAR(64) NOT NULL, oracle_id NVARCHAR(64) NOT NULL, set_id NVARCHAR(32) NOT NULL,
  released_at DATE, layout NVARCHAR(50), watermark NVARCHAR(100), collector_number NVARCHAR(50),
  rarity NVARCHAR(50), frame NVARCHAR(50), border_color NVARCHAR(50), card_back_id NVARCHAR(64),
  highres_image BIT, image_status NVARCHAR(50), reserved BIT, game_changer BIT, foil BIT, nonfoil BIT,
  oversized BIT, promo BIT, reprint BIT, variation BIT, digital BIT, edhrec_rank INT, penny_rank INT,
  CONSTRAINT PK_card_print PRIMARY KEY (id),
  CONSTRAINT FK_card_print_oracle FOREIGN KEY (oracle_id) REFERENCES dbo.oracle_card(oracle_id),
  CONSTRAINT FK_card_print_set FOREIGN KEY (set_id) REFERENCES dbo.mtgs_set(set_id),
  CONSTRAINT FK_card_print_watermark FOREIGN KEY (watermark) REFERENCES dbo.dim_watermark(watermark)
);

CREATE TABLE dbo.card_face (
  face_id INT NOT NULL, card_id NVARCHAR(64) NOT NULL, face_index INT,
  mana_cost NVARCHAR(100), cmc FLOAT, power NVARCHAR(16), toughness NVARCHAR(16),
  CONSTRAINT PK_card_face PRIMARY KEY (face_id),
  CONSTRAINT FK_card_face_card FOREIGN KEY (card_id) REFERENCES dbo.card_print(id)
);

CREATE TABLE dbo.card_text_localized (
  face_id INT NOT NULL, lang_code NVARCHAR(16) NOT NULL, name NVARCHAR(200),
  type_line NVARCHAR(200), oracle_text NVARCHAR(4000),
  CONSTRAINT PK_card_text_localized PRIMARY KEY (face_id, lang_code),
  CONSTRAINT FK_card_text_face FOREIGN KEY (face_id) REFERENCES dbo.card_face(face_id),
  CONSTRAINT FK_card_text_lang FOREIGN KEY (lang_code) REFERENCES dbo.dim_language(lang_code)
);

CREATE TABLE dbo.print_localized (
  card_id NVARCHAR(64) NOT NULL, lang_code NVARCHAR(16) NOT NULL, printed_name NVARCHAR(200),
  CONSTRAINT PK_print_localized PRIMARY KEY (card_id, lang_code),
  CONSTRAINT FK_print_loc_card FOREIGN KEY (card_id) REFERENCES dbo.card_print(id),
  CONSTRAINT FK_print_loc_lang FOREIGN KEY (lang_code) REFERENCES dbo.dim_language(lang_code)
);

CREATE TABLE dbo.face_image_uri (
  face_id INT NOT NULL, uri_kind NVARCHAR(50) NOT NULL, uri NVARCHAR(500) NOT NULL,
  CONSTRAINT PK_face_image_uri PRIMARY KEY (face_id, uri_kind),
  CONSTRAINT FK_face_image_face FOREIGN KEY (face_id) REFERENCES dbo.card_face(face_id),
  CONSTRAINT FK_face_image_kind FOREIGN KEY (uri_kind) REFERENCES dbo.dim_uri_kind(uri_kind)
);

CREATE TABLE dbo.card_image_uri (
  card_id NVARCHAR(64) NOT NULL, uri_kind NVARCHAR(50) NOT NULL, uri NVARCHAR(500) NOT NULL,
  CONSTRAINT PK_card_image_uri PRIMARY KEY (card_id, uri_kind),
  CONSTRAINT FK_card_image_card FOREIGN KEY (card_id) REFERENCES dbo.card_print(id),
  CONSTRAINT FK_card_image_kind FOREIGN KEY (uri_kind) REFERENCES dbo.dim_uri_kind(uri_kind)
);
GO

-- Part 4: Card attribute bridges, legality, artists, prices, relations, rulings
CREATE TABLE dbo.card_color (
  card_id NVARCHAR(64) NOT NULL, color NVARCHAR(10) NOT NULL,
  CONSTRAINT PK_card_color PRIMARY KEY (card_id, color),
  CONSTRAINT FK_card_color_card FOREIGN KEY (card_id) REFERENCES dbo.card_print(id),
  CONSTRAINT FK_card_color_dim FOREIGN KEY (color) REFERENCES dbo.dim_color(code)
);
CREATE TABLE dbo.card_color_identity (
  card_id NVARCHAR(64) NOT NULL, color NVARCHAR(10) NOT NULL,
  CONSTRAINT PK_card_color_identity PRIMARY KEY (card_id, color),
  CONSTRAINT FK_card_color_identity_card FOREIGN KEY (card_id) REFERENCES dbo.card_print(id),
  CONSTRAINT FK_card_color_identity_dim FOREIGN KEY (color) REFERENCES dbo.dim_color(code)
);
CREATE TABLE dbo.card_keyword (
  card_id NVARCHAR(64) NOT NULL, keyword NVARCHAR(100) NOT NULL,
  CONSTRAINT PK_card_keyword PRIMARY KEY (card_id, keyword),
  CONSTRAINT FK_card_keyword_card FOREIGN KEY (card_id) REFERENCES dbo.card_print(id),
  CONSTRAINT FK_card_keyword_dim FOREIGN KEY (keyword) REFERENCES dbo.dim_keyword(keyword)
);
CREATE TABLE dbo.card_game (card_id NVARCHAR(64) NOT NULL, game NVARCHAR(50) NOT NULL,
  CONSTRAINT PK_card_game PRIMARY KEY (card_id, game),
  CONSTRAINT FK_card_game_card FOREIGN KEY (card_id) REFERENCES dbo.card_print(id)
);
CREATE TABLE dbo.card_finish (
  card_id NVARCHAR(64) NOT NULL, finish NVARCHAR(50) NOT NULL,
  CONSTRAINT PK_card_finish PRIMARY KEY (card_id, finish),
  CONSTRAINT FK_card_finish_card FOREIGN KEY (card_id) REFERENCES dbo.card_print(id),
  CONSTRAINT FK_card_finish_dim FOREIGN KEY (finish) REFERENCES dbo.dim_finish(finish)
);
CREATE TABLE dbo.card_supertype (
  card_id NVARCHAR(64) NOT NULL, supertype NVARCHAR(100) NOT NULL,
  CONSTRAINT PK_card_supertype PRIMARY KEY (card_id, supertype),
  CONSTRAINT FK_card_supertype_card FOREIGN KEY (card_id) REFERENCES dbo.card_print(id),
  CONSTRAINT FK_card_supertype_dim FOREIGN KEY (supertype) REFERENCES dbo.dim_supertype(supertype)
);
CREATE TABLE dbo.card_type (
  card_id NVARCHAR(64) NOT NULL, card_type NVARCHAR(100) NOT NULL,
  CONSTRAINT PK_card_type PRIMARY KEY (card_id, card_type),
  CONSTRAINT FK_card_type_card FOREIGN KEY (card_id) REFERENCES dbo.card_print(id),
  CONSTRAINT FK_card_type_dim FOREIGN KEY (card_type) REFERENCES dbo.dim_card_type(card_type)
);
CREATE TABLE dbo.card_subtype (
  card_id NVARCHAR(64) NOT NULL, subtype NVARCHAR(100) NOT NULL,
  CONSTRAINT PK_card_subtype PRIMARY KEY (card_id, subtype),
  CONSTRAINT FK_card_subtype_card FOREIGN KEY (card_id) REFERENCES dbo.card_print(id),
  CONSTRAINT FK_card_subtype_dim FOREIGN KEY (subtype) REFERENCES dbo.dim_subtype(subtype)
);

CREATE TABLE dbo.artist (artist_id NVARCHAR(64) NOT NULL, name NVARCHAR(200), CONSTRAINT PK_artist PRIMARY KEY (artist_id));
CREATE TABLE dbo.card_artist (
  card_id NVARCHAR(64) NOT NULL, artist_id NVARCHAR(64) NOT NULL,
  CONSTRAINT PK_card_artist PRIMARY KEY (card_id, artist_id),
  CONSTRAINT FK_card_artist_card FOREIGN KEY (card_id) REFERENCES dbo.card_print(id),
  CONSTRAINT FK_card_artist_artist FOREIGN KEY (artist_id) REFERENCES dbo.artist(artist_id)
);

CREATE TABLE dbo.card_price (
  card_id NVARCHAR(64) NOT NULL, as_of DATE NOT NULL, currency_code NVARCHAR(10) NOT NULL,
  finish NVARCHAR(50) NOT NULL, vendor_id INT NOT NULL, amount DECIMAL(18,4), event_id NVARCHAR(64),
  CONSTRAINT PK_card_price PRIMARY KEY (card_id, as_of, currency_code, finish, vendor_id),
  CONSTRAINT FK_card_price_card FOREIGN KEY (card_id) REFERENCES dbo.card_print(id),
  CONSTRAINT FK_card_price_currency FOREIGN KEY (currency_code) REFERENCES dbo.dim_currency(currency_code),
  CONSTRAINT FK_card_price_finish FOREIGN KEY (finish) REFERENCES dbo.dim_finish(finish),
  CONSTRAINT FK_card_price_vendor FOREIGN KEY (vendor_id) REFERENCES dbo.dim_vendor(vendor_id),
  CONSTRAINT FK_card_price_event FOREIGN KEY (event_id) REFERENCES dbo.audit_event(event_id)
);

CREATE TABLE dbo.card_legality (
  card_id NVARCHAR(64) NOT NULL, format_name NVARCHAR(100) NOT NULL,
  status NVARCHAR(50), event_id NVARCHAR(64),
  CONSTRAINT PK_card_legality PRIMARY KEY (card_id, format_name),
  CONSTRAINT FK_card_legality_card FOREIGN KEY (card_id) REFERENCES dbo.card_print(id),
  CONSTRAINT FK_card_legality_format FOREIGN KEY (format_name) REFERENCES dbo.dim_format(format_name),
  CONSTRAINT FK_card_legality_event FOREIGN KEY (event_id) REFERENCES dbo.audit_event(event_id)
);

CREATE TABLE dbo.card_related_uri (
  card_id NVARCHAR(64) NOT NULL, uri_kind NVARCHAR(50) NOT NULL, uri NVARCHAR(500) NOT NULL,
  CONSTRAINT PK_card_related_uri PRIMARY KEY (card_id, uri_kind),
  CONSTRAINT FK_card_related_uri_card FOREIGN KEY (card_id) REFERENCES dbo.card_print(id),
  CONSTRAINT FK_card_related_uri_kind FOREIGN KEY (uri_kind) REFERENCES dbo.dim_uri_kind(uri_kind)
);

CREATE TABLE dbo.card_relation (
  card_id NVARCHAR(64) NOT NULL, related_id NVARCHAR(64) NOT NULL, component NVARCHAR(50) NOT NULL,
  CONSTRAINT PK_card_relation PRIMARY KEY (card_id, related_id, component),
  CONSTRAINT FK_card_relation_card FOREIGN KEY (card_id) REFERENCES dbo.card_print(id),
  CONSTRAINT FK_card_relation_related FOREIGN KEY (related_id) REFERENCES dbo.card_print(id)
);

CREATE TABLE dbo.card_ruling (
  ruling_id INT NOT NULL, oracle_id NVARCHAR(64), source NVARCHAR(100), published_at DATE, comment NVARCHAR(4000),
  CONSTRAINT PK_card_ruling PRIMARY KEY (ruling_id),
  CONSTRAINT FK_card_ruling_oracle FOREIGN KEY (oracle_id) REFERENCES dbo.oracle_card(oracle_id)
);
GO

-- Part 5: Format rules and banlist
CREATE TABLE dbo.format_rule_change (
  format_name NVARCHAR(100) NOT NULL, effective_date DATE NOT NULL,
  note NVARCHAR(2000), source_uri NVARCHAR(500),
  CONSTRAINT PK_format_rule_change PRIMARY KEY (format_name, effective_date),
  CONSTRAINT FK_frc_format FOREIGN KEY (format_name) REFERENCES dbo.dim_format(format_name)
);
CREATE TABLE dbo.format_banlist (
  format_name NVARCHAR(100) NOT NULL, oracle_id NVARCHAR(64) NOT NULL,
  valid_from NVARCHAR(20) NOT NULL, valid_to NVARCHAR(20), status NVARCHAR(50),
  CONSTRAINT PK_format_banlist PRIMARY KEY (format_name, oracle_id, valid_from),
  CONSTRAINT FK_fb_format FOREIGN KEY (format_name) REFERENCES dbo.dim_format(format_name),
  CONSTRAINT FK_fb_oracle FOREIGN KEY (oracle_id) REFERENCES dbo.oracle_card(oracle_id)
);
GO

-- Part 6: EDH sources, snapshots, commander metrics
CREATE TABLE dbo.edh_source (source_id INT NOT NULL, url NVARCHAR(500), CONSTRAINT PK_edh_source PRIMARY KEY (source_id));
CREATE TABLE dbo.edh_snapshot (
  snapshot_id INT NOT NULL, captured_at DATETIME2(0), source_id INT,
  CONSTRAINT PK_edh_snapshot PRIMARY KEY (snapshot_id),
  CONSTRAINT FK_edh_snapshot_source FOREIGN KEY (source_id) REFERENCES dbo.edh_source(source_id)
);

CREATE TABLE dbo.commander_rank (
  oracle_id NVARCHAR(64) NOT NULL, format_name NVARCHAR(100) NOT NULL, snapshot_id INT NOT NULL,
  rank INT, meta_share DECIMAL(18,4), event_id NVARCHAR(64),
  CONSTRAINT PK_commander_rank PRIMARY KEY (oracle_id, format_name, snapshot_id),
  CONSTRAINT FK_cr_oracle FOREIGN KEY (oracle_id) REFERENCES dbo.oracle_card(oracle_id),
  CONSTRAINT FK_cr_format FOREIGN KEY (format_name) REFERENCES dbo.dim_format(format_name),
  CONSTRAINT FK_cr_snapshot FOREIGN KEY (snapshot_id) REFERENCES dbo.edh_snapshot(snapshot_id),
  CONSTRAINT FK_cr_event FOREIGN KEY (event_id) REFERENCES dbo.audit_event(event_id)
);

CREATE TABLE dbo.commander_partner_rank (
  oracle_id NVARCHAR(64) NOT NULL, partner_oracle_id NVARCHAR(64) NOT NULL,
  format_name NVARCHAR(100) NOT NULL, snapshot_id INT NOT NULL,
  rank INT, meta_share DECIMAL(18,4), event_id NVARCHAR(64),
  CONSTRAINT PK_commander_partner_rank PRIMARY KEY (oracle_id, partner_oracle_id, format_name, snapshot_id),
  CONSTRAINT FK_cpr_oracle FOREIGN KEY (oracle_id) REFERENCES dbo.oracle_card(oracle_id),
  CONSTRAINT FK_cpr_partner FOREIGN KEY (partner_oracle_id) REFERENCES dbo.oracle_card(oracle_id),
  CONSTRAINT FK_cpr_format FOREIGN KEY (format_name) REFERENCES dbo.dim_format(format_name),
  CONSTRAINT FK_cpr_snapshot FOREIGN KEY (snapshot_id) REFERENCES dbo.edh_snapshot(snapshot_id),
  CONSTRAINT FK_cpr_event FOREIGN KEY (event_id) REFERENCES dbo.audit_event(event_id)
);

CREATE TABLE dbo.commander_card_popularity (
  commander_oracle_id NVARCHAR(64) NOT NULL, card_oracle_id NVARCHAR(64) NOT NULL,
  format_name NVARCHAR(100) NOT NULL, snapshot_id INT NOT NULL,
  include_rate DECIMAL(18,4), synergy_pct DECIMAL(18,4), role NVARCHAR(100), event_id NVARCHAR(64),
  CONSTRAINT PK_commander_card_popularity PRIMARY KEY (commander_oracle_id, card_oracle_id, format_name, snapshot_id),
  CONSTRAINT FK_ccp_cmd FOREIGN KEY (commander_oracle_id) REFERENCES dbo.oracle_card(oracle_id),
  CONSTRAINT FK_ccp_card FOREIGN KEY (card_oracle_id) REFERENCES dbo.oracle_card(oracle_id),
  CONSTRAINT FK_ccp_format FOREIGN KEY (format_name) REFERENCES dbo.dim_format(format_name),
  CONSTRAINT FK_ccp_snapshot FOREIGN KEY (snapshot_id) REFERENCES dbo.edh_snapshot(snapshot_id),
  CONSTRAINT FK_ccp_event FOREIGN KEY (event_id) REFERENCES dbo.audit_event(event_id)
);

CREATE TABLE dbo.commander_theme (
  commander_oracle_id NVARCHAR(64) NOT NULL, theme_id INT NOT NULL, format_name NVARCHAR(100) NOT NULL, snapshot_id INT NOT NULL,
  popularity DECIMAL(18,4), event_id NVARCHAR(64),
  CONSTRAINT PK_commander_theme PRIMARY KEY (commander_oracle_id, theme_id, format_name, snapshot_id),
  CONSTRAINT FK_ct_cmd FOREIGN KEY (commander_oracle_id) REFERENCES dbo.oracle_card(oracle_id),
  CONSTRAINT FK_ct_theme FOREIGN KEY (theme_id) REFERENCES dbo.dim_theme(theme_id),
  CONSTRAINT FK_ct_format FOREIGN KEY (format_name) REFERENCES dbo.dim_format(format_name),
  CONSTRAINT FK_ct_snapshot FOREIGN KEY (snapshot_id) REFERENCES dbo.edh_snapshot(snapshot_id),
  CONSTRAINT FK_ct_event FOREIGN KEY (event_id) REFERENCES dbo.audit_event(event_id)
);

CREATE TABLE dbo.theme_card_popularity (
  theme_id INT NOT NULL, card_oracle_id NVARCHAR(64) NOT NULL, format_name NVARCHAR(100) NOT NULL, snapshot_id INT NOT NULL,
  include_rate DECIMAL(18,4), synergy_pct DECIMAL(18,4), event_id NVARCHAR(64),
  CONSTRAINT PK_theme_card_popularity PRIMARY KEY (theme_id, card_oracle_id, format_name, snapshot_id),
  CONSTRAINT FK_tcp_theme FOREIGN KEY (theme_id) REFERENCES dbo.dim_theme(theme_id),
  CONSTRAINT FK_tcp_card FOREIGN KEY (card_oracle_id) REFERENCES dbo.oracle_card(oracle_id),
  CONSTRAINT FK_tcp_format FOREIGN KEY (format_name) REFERENCES dbo.dim_format(format_name),
  CONSTRAINT FK_tcp_snapshot FOREIGN KEY (snapshot_id) REFERENCES dbo.edh_snapshot(snapshot_id),
  CONSTRAINT FK_tcp_event FOREIGN KEY (event_id) REFERENCES dbo.audit_event(event_id)
);

CREATE TABLE dbo.card_salt (
  card_oracle_id NVARCHAR(64) NOT NULL, snapshot_id INT NOT NULL,
  salt_score DECIMAL(18,4), salt_rank INT, votes INT, event_id NVARCHAR(64),
  CONSTRAINT PK_card_salt PRIMARY KEY (card_oracle_id, snapshot_id),
  CONSTRAINT FK_cs_card FOREIGN KEY (card_oracle_id) REFERENCES dbo.oracle_card(oracle_id),
  CONSTRAINT FK_cs_snapshot FOREIGN KEY (snapshot_id) REFERENCES dbo.edh_snapshot(snapshot_id),
  CONSTRAINT FK_cs_event FOREIGN KEY (event_id) REFERENCES dbo.audit_event(event_id)
);

CREATE TABLE dbo.commander_price (
  commander_oracle_id NVARCHAR(64) NOT NULL, snapshot_id INT NOT NULL,
  currency_code NVARCHAR(10) NOT NULL, amount DECIMAL(18,4), vendor_id INT NOT NULL, event_id NVARCHAR(64),
  CONSTRAINT PK_commander_price PRIMARY KEY (commander_oracle_id, snapshot_id, currency_code, vendor_id),
  CONSTRAINT FK_cprice_cmd FOREIGN KEY (commander_oracle_id) REFERENCES dbo.oracle_card(oracle_id),
  CONSTRAINT FK_cprice_snapshot FOREIGN KEY (snapshot_id) REFERENCES dbo.edh_snapshot(snapshot_id),
  CONSTRAINT FK_cprice_currency FOREIGN KEY (currency_code) REFERENCES dbo.dim_currency(currency_code),
  CONSTRAINT FK_cprice_vendor FOREIGN KEY (vendor_id) REFERENCES dbo.dim_vendor(vendor_id),
  CONSTRAINT FK_cprice_event FOREIGN KEY (event_id) REFERENCES dbo.audit_event(event_id)
);

CREATE TABLE dbo.commander_theme_rank (
  commander_oracle_id NVARCHAR(64) NOT NULL, theme_id INT NOT NULL,
  format_name NVARCHAR(100) NOT NULL, snapshot_id INT NOT NULL,
  rank INT, deck_count INT, meta_share DECIMAL(18,4), event_id NVARCHAR(64),
  CONSTRAINT PK_commander_theme_rank PRIMARY KEY (commander_oracle_id, theme_id, format_name, snapshot_id),
  CONSTRAINT FK_ctr_cmd FOREIGN KEY (commander_oracle_id) REFERENCES dbo.oracle_card(oracle_id),
  CONSTRAINT FK_ctr_theme FOREIGN KEY (theme_id) REFERENCES dbo.dim_theme(theme_id),
  CONSTRAINT FK_ctr_format FOREIGN KEY (format_name) REFERENCES dbo.dim_format(format_name),
  CONSTRAINT FK_ctr_snapshot FOREIGN KEY (snapshot_id) REFERENCES dbo.edh_snapshot(snapshot_id),
  CONSTRAINT FK_ctr_event FOREIGN KEY (event_id) REFERENCES dbo.audit_event(event_id)
);

CREATE TABLE dbo.theme_deck_stats (
  theme_id INT NOT NULL, format_name NVARCHAR(100) NOT NULL, snapshot_id INT NOT NULL,
  deck_count INT, avg_cmc FLOAT, event_id NVARCHAR(64),
  CONSTRAINT PK_theme_deck_stats PRIMARY KEY (theme_id, format_name, snapshot_id),
  CONSTRAINT FK_tds_theme FOREIGN KEY (theme_id) REFERENCES dbo.dim_theme(theme_id),
  CONSTRAINT FK_tds_format FOREIGN KEY (format_name) REFERENCES dbo.dim_format(format_name),
  CONSTRAINT FK_tds_snapshot FOREIGN KEY (snapshot_id) REFERENCES dbo.edh_snapshot(snapshot_id),
  CONSTRAINT FK_tds_event FOREIGN KEY (event_id) REFERENCES dbo.audit_event(event_id)
);
GO

-- Part 7: Spellbook sources and combos
CREATE TABLE dbo.spellbook_source (source_id INT NOT NULL, url NVARCHAR(500), license NVARCHAR(200), CONSTRAINT PK_spellbook_source PRIMARY KEY (source_id));

CREATE TABLE dbo.combo (
  combo_id NVARCHAR(64) NOT NULL, slug NVARCHAR(200), primary_name NVARCHAR(200),
  url NVARCHAR(500), verified BIT, status NVARCHAR(50), created_at DATETIME2(0), updated_at DATETIME2(0),
  source_id INT, combo_hash NVARCHAR(64),
  CONSTRAINT PK_combo PRIMARY KEY (combo_id),
  CONSTRAINT FK_combo_source FOREIGN KEY (source_id) REFERENCES dbo.spellbook_source(source_id)
);

CREATE TABLE dbo.combo_piece (
  combo_id NVARCHAR(64) NOT NULL, oracle_id NVARCHAR(64) NOT NULL, role NVARCHAR(50) NOT NULL,
  qty INT, is_commander BIT, is_partner BIT,
  CONSTRAINT PK_combo_piece PRIMARY KEY (combo_id, oracle_id, role),
  CONSTRAINT FK_cpp_combo FOREIGN KEY (combo_id) REFERENCES dbo.combo(combo_id),
  CONSTRAINT FK_cp_oracle FOREIGN KEY (oracle_id) REFERENCES dbo.oracle_card(oracle_id)
);

CREATE TABLE dbo.combo_step (
  combo_id NVARCHAR(64) NOT NULL, step_no INT NOT NULL,
  action NVARCHAR(100), text NVARCHAR(2000), notes NVARCHAR(1000),
  CONSTRAINT PK_combo_step PRIMARY KEY (combo_id, step_no),
  CONSTRAINT FK_cstep_combo FOREIGN KEY (combo_id) REFERENCES dbo.combo(combo_id)
);

CREATE TABLE dbo.combo_prereq (combo_id NVARCHAR(64) NOT NULL, prereq_no INT NOT NULL, text NVARCHAR(2000),
  CONSTRAINT PK_combo_prereq PRIMARY KEY (combo_id, prereq_no),
  CONSTRAINT FK_cpr_combo FOREIGN KEY (combo_id) REFERENCES dbo.combo(combo_id)
);

CREATE TABLE dbo.combo_result (
  combo_id NVARCHAR(64) NOT NULL, result_code NVARCHAR(50) NOT NULL, magnitude NVARCHAR(100), text NVARCHAR(2000),
  CONSTRAINT PK_combo_result PRIMARY KEY (combo_id, result_code),
  CONSTRAINT FK_cres_combo FOREIGN KEY (combo_id) REFERENCES dbo.combo(combo_id),
  CONSTRAINT FK_cres_dim FOREIGN KEY (result_code) REFERENCES dbo.dim_combo_result(result_code)
);

CREATE TABLE dbo.combo_color_identity (
  combo_id NVARCHAR(64) NOT NULL, color NVARCHAR(10) NOT NULL,
  CONSTRAINT PK_combo_color_identity PRIMARY KEY (combo_id, color),
  CONSTRAINT FK_cci_combo FOREIGN KEY (combo_id) REFERENCES dbo.combo(combo_id),
  CONSTRAINT FK_cci_color FOREIGN KEY (color) REFERENCES dbo.dim_color(code)
);

CREATE TABLE dbo.combo_tag (
  combo_id NVARCHAR(64) NOT NULL, tag NVARCHAR(100) NOT NULL,
  CONSTRAINT PK_combo_tag PRIMARY KEY (combo_id, tag),
  CONSTRAINT FK_ctag_combo FOREIGN KEY (combo_id) REFERENCES dbo.combo(combo_id),
  CONSTRAINT FK_ctag_dim FOREIGN KEY (tag) REFERENCES dbo.dim_combo_tag(tag)
);

CREATE TABLE dbo.combo_legality (
  combo_id NVARCHAR(64) NOT NULL, format_name NVARCHAR(100) NOT NULL, status NVARCHAR(50),
  CONSTRAINT PK_combo_legality PRIMARY KEY (combo_id, format_name),
  CONSTRAINT FK_cl_combo FOREIGN KEY (combo_id) REFERENCES dbo.combo(combo_id),
  CONSTRAINT FK_cl_format FOREIGN KEY (format_name) REFERENCES dbo.dim_format(format_name)
);

CREATE TABLE dbo.combo_popularity (
  combo_id NVARCHAR(64) NOT NULL, snapshot_id INT NOT NULL, votes INT, score DECIMAL(18,4), event_id NVARCHAR(64),
  CONSTRAINT PK_combo_popularity PRIMARY KEY (combo_id, snapshot_id),
  CONSTRAINT FK_cpop_combo FOREIGN KEY (combo_id) REFERENCES dbo.combo(combo_id),
  CONSTRAINT FK_cpop_snapshot FOREIGN KEY (snapshot_id) REFERENCES dbo.edh_snapshot(snapshot_id),
  CONSTRAINT FK_cpop_event FOREIGN KEY (event_id) REFERENCES dbo.audit_event(event_id)
);

CREATE TABLE dbo.commander_combo_fit (
  commander_oracle_id NVARCHAR(64) NOT NULL, combo_id NVARCHAR(64) NOT NULL, snapshot_id INT NOT NULL,
  usable BIT, reason NVARCHAR(2000),
  CONSTRAINT PK_commander_combo_fit PRIMARY KEY (commander_oracle_id, combo_id, snapshot_id),
  CONSTRAINT FK_ccf_cmd FOREIGN KEY (commander_oracle_id) REFERENCES dbo.oracle_card(oracle_id),
  CONSTRAINT FK_ccf_combo FOREIGN KEY (combo_id) REFERENCES dbo.combo(combo_id),
  CONSTRAINT FK_ccf_snapshot FOREIGN KEY (snapshot_id) REFERENCES dbo.edh_snapshot(snapshot_id)
);
GO

-- Part 8: Decks and pricing
CREATE TABLE dbo.deck (
  deck_id NVARCHAR(64) NOT NULL, slug NVARCHAR(200), name NVARCHAR(200),
  source_id INT, snapshot_id INT, format_name NVARCHAR(100),
  card_count INT, land_count INT, avg_cmc DECIMAL(18,4), notes NVARCHAR(2000),
  event_id NVARCHAR(64), org_id INT,
  CONSTRAINT PK_deck PRIMARY KEY (deck_id),
  CONSTRAINT FK_deck_source FOREIGN KEY (source_id) REFERENCES dbo.edh_source(source_id),
  CONSTRAINT FK_deck_snapshot FOREIGN KEY (snapshot_id) REFERENCES dbo.edh_snapshot(snapshot_id),
  CONSTRAINT FK_deck_format FOREIGN KEY (format_name) REFERENCES dbo.dim_format(format_name),
  CONSTRAINT FK_deck_event FOREIGN KEY (event_id) REFERENCES dbo.audit_event(event_id)
);
CREATE TABLE dbo.deck_version (
  deck_id NVARCHAR(64) NOT NULL, version_no INT NOT NULL,
  created_at DATETIME2(0), author NVARCHAR(200), notes NVARCHAR(2000),
  CONSTRAINT PK_deck_version PRIMARY KEY (deck_id, version_no),
  CONSTRAINT FK_deck_version_deck FOREIGN KEY (deck_id) REFERENCES dbo.deck(deck_id)
);
CREATE TABLE dbo.deck_commander (
  deck_id NVARCHAR(64) NOT NULL, commander_oracle_id NVARCHAR(64) NOT NULL, role NVARCHAR(50) NOT NULL,
  CONSTRAINT PK_deck_commander PRIMARY KEY (deck_id, commander_oracle_id, role),
  CONSTRAINT FK_dc_deck FOREIGN KEY (deck_id) REFERENCES dbo.deck(deck_id),
  CONSTRAINT FK_dc_oracle FOREIGN KEY (commander_oracle_id) REFERENCES dbo.oracle_card(oracle_id)
);
CREATE TABLE dbo.deck_card_versioned (
  deck_id NVARCHAR(64) NOT NULL, version_no INT NOT NULL, card_oracle_id NVARCHAR(64) NOT NULL,
  board NVARCHAR(50) NOT NULL, qty INT, section NVARCHAR(100),
  CONSTRAINT PK_deck_card_versioned PRIMARY KEY (deck_id, version_no, card_oracle_id, board),
  CONSTRAINT FK_dcv_deckver FOREIGN KEY (deck_id, version_no) REFERENCES dbo.deck_version(deck_id, version_no),
  CONSTRAINT FK_dcv_oracle FOREIGN KEY (card_oracle_id) REFERENCES dbo.oracle_card(oracle_id)
);
CREATE TABLE dbo.deck_color_identity (
  deck_id NVARCHAR(64) NOT NULL, color NVARCHAR(10) NOT NULL,
  CONSTRAINT PK_deck_color_identity PRIMARY KEY (deck_id, color),
  CONSTRAINT FK_dci_deck FOREIGN KEY (deck_id) REFERENCES dbo.deck(deck_id),
  CONSTRAINT FK_dci_color FOREIGN KEY (color) REFERENCES dbo.dim_color(code)
);
CREATE TABLE dbo.deck_price (
  deck_id NVARCHAR(64) NOT NULL, snapshot_id INT NOT NULL, currency_code NVARCHAR(10) NOT NULL, vendor_id INT NOT NULL,
  amount DECIMAL(18,4),
  CONSTRAINT PK_deck_price PRIMARY KEY (deck_id, snapshot_id, currency_code, vendor_id),
  CONSTRAINT FK_dp_deck FOREIGN KEY (deck_id) REFERENCES dbo.deck(deck_id),
  CONSTRAINT FK_dp_snapshot FOREIGN KEY (snapshot_id) REFERENCES dbo.edh_snapshot(snapshot_id),
  CONSTRAINT FK_dp_currency FOREIGN KEY (currency_code) REFERENCES dbo.dim_currency(currency_code),
  CONSTRAINT FK_dp_vendor FOREIGN KEY (vendor_id) REFERENCES dbo.dim_vendor(vendor_id)
);
CREATE TABLE dbo.deck_uri (
  deck_id NVARCHAR(64) NOT NULL, uri_kind NVARCHAR(50) NOT NULL, uri NVARCHAR(500) NOT NULL,
  CONSTRAINT PK_deck_uri PRIMARY KEY (deck_id, uri_kind),
  CONSTRAINT FK_du_deck FOREIGN KEY (deck_id) REFERENCES dbo.deck(deck_id),
  CONSTRAINT FK_du_kind FOREIGN KEY (uri_kind) REFERENCES dbo.dim_uri_kind(uri_kind)
);
CREATE TABLE dbo.deck_theme_tag (
  deck_id NVARCHAR(64) NOT NULL, theme_id INT NOT NULL,
  CONSTRAINT PK_deck_theme_tag PRIMARY KEY (deck_id, theme_id),
  CONSTRAINT FK_dtt_deck FOREIGN KEY (deck_id) REFERENCES dbo.deck(deck_id),
  CONSTRAINT FK_dtt_theme FOREIGN KEY (theme_id) REFERENCES dbo.dim_theme(theme_id)
);
GO

-- Part 9: Orgs and players
CREATE TABLE dbo.org (org_id INT NOT NULL, name NVARCHAR(200), CONSTRAINT PK_org PRIMARY KEY (org_id));
ALTER TABLE dbo.deck ADD CONSTRAINT FK_deck_org FOREIGN KEY (org_id) REFERENCES dbo.org(org_id);

CREATE TABLE dbo.player (
  player_id NVARCHAR(64) NOT NULL, display_name NVARCHAR(200),
  contact_opt_in BIT, created_at DATETIME2(0), org_id INT,
  CONSTRAINT PK_player PRIMARY KEY (player_id),
  CONSTRAINT FK_player_org FOREIGN KEY (org_id) REFERENCES dbo.org(org_id)
);
CREATE TABLE dbo.org_membership (
  org_id INT NOT NULL, player_id NVARCHAR(64) NOT NULL, role NVARCHAR(100) NOT NULL,
  CONSTRAINT PK_org_membership PRIMARY KEY (org_id, player_id),
  CONSTRAINT FK_om_org FOREIGN KEY (org_id) REFERENCES dbo.org(org_id),
  CONSTRAINT FK_om_player FOREIGN KEY (player_id) REFERENCES dbo.player(player_id)
);
CREATE TABLE dbo.player_handle (
  player_id NVARCHAR(64) NOT NULL, platform NVARCHAR(50) NOT NULL, handle NVARCHAR(100) NOT NULL,
  CONSTRAINT PK_player_handle PRIMARY KEY (player_id, platform),
  CONSTRAINT FK_ph_player FOREIGN KEY (player_id) REFERENCES dbo.player(player_id)
);
CREATE TABLE dbo.player_consent (
  player_id NVARCHAR(64) NOT NULL, consent_type NVARCHAR(100) NOT NULL, granted_at DATETIME2(0), revoked_at DATETIME2(0),
  CONSTRAINT PK_player_consent PRIMARY KEY (player_id, consent_type),
  CONSTRAINT FK_pc_player FOREIGN KEY (player_id) REFERENCES dbo.player(player_id)
);
GO

-- Part 10: Matches, games, objects, stack, logs, infractions
CREATE TABLE dbo.match (
  match_id NVARCHAR(64) NOT NULL, format_name NVARCHAR(100), pod_size INT,
  scheduled_at DATETIME2(0), started_at DATETIME2(0), ended_at DATETIME2(0),
  table_id NVARCHAR(64), rules_modifiers NVARCHAR(200), game_rule_set NVARCHAR(100),
  random_seed NVARCHAR(64), recording_uri NVARCHAR(500), source NVARCHAR(100),
  ingested_at DATETIME2(0), org_id INT,
  CONSTRAINT PK_match PRIMARY KEY (match_id),
  CONSTRAINT FK_match_format FOREIGN KEY (format_name) REFERENCES dbo.dim_format(format_name),
  CONSTRAINT FK_match_org FOREIGN KEY (org_id) REFERENCES dbo.org(org_id)
);

CREATE TABLE dbo.match_participant (
  participant_id NVARCHAR(64) NOT NULL, match_id NVARCHAR(64), seat_no INT,
  player_id NVARCHAR(64), deck_id NVARCHAR(64), starting_life INT,
  turn_order INT, final_place INT, elimination_reason NVARCHAR(200),
  elimination_turn INT, scooped BIT,
  CONSTRAINT PK_match_participant PRIMARY KEY (participant_id),
  CONSTRAINT FK_mp_match FOREIGN KEY (match_id) REFERENCES dbo.match(match_id),
  CONSTRAINT FK_mp_player FOREIGN KEY (player_id) REFERENCES dbo.player(player_id),
  CONSTRAINT FK_mp_deck FOREIGN KEY (deck_id) REFERENCES dbo.deck(deck_id)
);

CREATE TABLE dbo.game (
  game_id NVARCHAR(64) NOT NULL, match_id NVARCHAR(64), game_no INT,
  started_at DATETIME2(0), ended_at DATETIME2(0), winner_participant_id NVARCHAR(64),
  CONSTRAINT PK_game PRIMARY KEY (game_id),
  CONSTRAINT FK_game_match FOREIGN KEY (match_id) REFERENCES dbo.match(match_id),
  CONSTRAINT FK_game_winner FOREIGN KEY (winner_participant_id) REFERENCES dbo.match_participant(participant_id)
);

CREATE TABLE dbo.starting_hand (
  participant_id NVARCHAR(64) NOT NULL, mulligans INT, opening_hand_size INT,
  CONSTRAINT PK_starting_hand PRIMARY KEY (participant_id),
  CONSTRAINT FK_sh_participant FOREIGN KEY (participant_id) REFERENCES dbo.match_participant(participant_id)
);
CREATE TABLE dbo.starting_hand_card (
  participant_id NVARCHAR(64) NOT NULL, seq_no INT NOT NULL, oracle_id NVARCHAR(64),
  CONSTRAINT PK_starting_hand_card PRIMARY KEY (participant_id, seq_no),
  CONSTRAINT FK_shc_hand FOREIGN KEY (participant_id) REFERENCES dbo.starting_hand(participant_id),
  CONSTRAINT FK_shc_oracle FOREIGN KEY (oracle_id) REFERENCES dbo.oracle_card(oracle_id)
);

CREATE TABLE dbo.turn (
  turn_id NVARCHAR(64) NOT NULL, game_id NVARCHAR(64), turn_no INT,
  active_participant_id NVARCHAR(64), turn_seq_start INT, turn_seq_end INT,
  CONSTRAINT PK_turn PRIMARY KEY (turn_id),
  CONSTRAINT FK_turn_game FOREIGN KEY (game_id) REFERENCES dbo.game(game_id),
  CONSTRAINT FK_turn_active FOREIGN KEY (active_participant_id) REFERENCES dbo.match_participant(participant_id)
);

CREATE TABLE dbo.phase_step (
  phase_step_id NVARCHAR(64) NOT NULL, turn_id NVARCHAR(64), phase NVARCHAR(50), step NVARCHAR(50),
  started_seq INT, ended_seq INT,
  CONSTRAINT PK_phase_step PRIMARY KEY (phase_step_id),
  CONSTRAINT FK_ps_turn FOREIGN KEY (turn_id) REFERENCES dbo.turn(turn_id),
  CONSTRAINT FK_ps_phase FOREIGN KEY (phase) REFERENCES dbo.dim_phase(phase),
  CONSTRAINT FK_ps_step FOREIGN KEY (step) REFERENCES dbo.dim_step(step)
);

CREATE TABLE dbo.object_instance (
  object_id NVARCHAR(64) NOT NULL, game_id NVARCHAR(64), oracle_id NVARCHAR(64),
  card_face_index INT, print_id NVARCHAR(64), controller_participant_id NVARCHAR(64),
  owner_participant_id NVARCHAR(64), zone NVARCHAR(50), token BIT, token_id INT, copy_of_object_id NVARCHAR(64),
  CONSTRAINT PK_object_instance PRIMARY KEY (object_id),
  CONSTRAINT FK_obj_game FOREIGN KEY (game_id) REFERENCES dbo.game(game_id),
  CONSTRAINT FK_obj_oracle FOREIGN KEY (oracle_id) REFERENCES dbo.oracle_card(oracle_id),
  CONSTRAINT FK_obj_print FOREIGN KEY (print_id) REFERENCES dbo.card_print(id),
  CONSTRAINT FK_obj_controller FOREIGN KEY (controller_participant_id) REFERENCES dbo.match_participant(participant_id),
  CONSTRAINT FK_obj_owner FOREIGN KEY (owner_participant_id) REFERENCES dbo.match_participant(participant_id),
  CONSTRAINT FK_obj_zone FOREIGN KEY (zone) REFERENCES dbo.dim_zone(zone),
  CONSTRAINT FK_obj_token_def FOREIGN KEY (token_id) REFERENCES dbo.dim_token(token_id),
  CONSTRAINT FK_obj_copy FOREIGN KEY (copy_of_object_id) REFERENCES dbo.object_instance(object_id)
);

CREATE TABLE dbo.object_state (
  object_state_id NVARCHAR(64) NOT NULL, object_id NVARCHAR(64), seq_applied INT,
  tapped BIT, counters_json NVARCHAR(2000), attached_to_object_id NVARCHAR(64),
  power NVARCHAR(16), toughness NVARCHAR(16), notes NVARCHAR(1000),
  CONSTRAINT PK_object_state PRIMARY KEY (object_state_id),
  CONSTRAINT FK_os_object FOREIGN KEY (object_id) REFERENCES dbo.object_instance(object_id),
  CONSTRAINT FK_os_attached FOREIGN KEY (attached_to_object_id) REFERENCES dbo.object_instance(object_id)
);

CREATE TABLE dbo.stack_item (
  stack_item_id NVARCHAR(64) NOT NULL, game_id NVARCHAR(64), created_seq INT,
  controller_participant_id NVARCHAR(64), source_object_id NVARCHAR(64), kind NVARCHAR(50),
  targets_json NVARCHAR(2000), resolved_seq INT, countered_seq INT,
  CONSTRAINT PK_stack_item PRIMARY KEY (stack_item_id),
  CONSTRAINT FK_si_game FOREIGN KEY (game_id) REFERENCES dbo.game(game_id),
  CONSTRAINT FK_si_ctrl FOREIGN KEY (controller_participant_id) REFERENCES dbo.match_participant(participant_id),
  CONSTRAINT FK_si_source FOREIGN KEY (source_object_id) REFERENCES dbo.object_instance(object_id)
);

CREATE TABLE dbo.log_event (
  event_id NVARCHAR(64) NOT NULL, game_id NVARCHAR(64), seq INT, ts DATETIME2(0),
  actor_participant_id NVARCHAR(64), phase_step_id NVARCHAR(64), event_type NVARCHAR(100),
  CONSTRAINT PK_log_event PRIMARY KEY (event_id),
  CONSTRAINT FK_le_game FOREIGN KEY (game_id) REFERENCES dbo.game(game_id),
  CONSTRAINT FK_le_actor FOREIGN KEY (actor_participant_id) REFERENCES dbo.match_participant(participant_id),
  CONSTRAINT FK_le_ps FOREIGN KEY (phase_step_id) REFERENCES dbo.phase_step(phase_step_id),
  CONSTRAINT FK_le_type FOREIGN KEY (event_type) REFERENCES dbo.dim_event_type(event_type)
);

CREATE TABLE dbo.event_payload (
  event_id NVARCHAR(64) NOT NULL, payload_json NVARCHAR(MAX),
  CONSTRAINT PK_event_payload PRIMARY KEY (event_id),
  CONSTRAINT FK_ep_event FOREIGN KEY (event_id) REFERENCES dbo.log_event(event_id)
);

CREATE TABLE dbo.life_total (
  game_id NVARCHAR(64) NOT NULL, participant_id NVARCHAR(64) NOT NULL, seq INT NOT NULL, life INT,
  CONSTRAINT PK_life_total PRIMARY KEY (game_id, participant_id, seq),
  CONSTRAINT FK_lt_game FOREIGN KEY (game_id) REFERENCES dbo.game(game_id),
  CONSTRAINT FK_lt_participant FOREIGN KEY (participant_id) REFERENCES dbo.match_participant(participant_id)
);

CREATE TABLE dbo.mana_delta (
  mana_id NVARCHAR(64) NOT NULL, game_id NVARCHAR(64), participant_id NVARCHAR(64),
  seq INT, color NVARCHAR(10), delta INT, pool_after_json NVARCHAR(1000),
  CONSTRAINT PK_mana_delta PRIMARY KEY (mana_id),
  CONSTRAINT FK_md_game FOREIGN KEY (game_id) REFERENCES dbo.game(game_id),
  CONSTRAINT FK_md_participant FOREIGN KEY (participant_id) REFERENCES dbo.match_participant(participant_id)
);

CREATE TABLE dbo.commander_damage (
  game_id NVARCHAR(64) NOT NULL, from_participant_id NVARCHAR(64) NOT NULL,
  to_participant_id NVARCHAR(64) NOT NULL, commander_oracle_id NVARCHAR(64) NOT NULL,
  total_damage INT,
  CONSTRAINT PK_commander_damage PRIMARY KEY (game_id, from_participant_id, to_participant_id, commander_oracle_id),
  CONSTRAINT FK_cd_game FOREIGN KEY (game_id) REFERENCES dbo.game(game_id),
  CONSTRAINT FK_cd_from FOREIGN KEY (from_participant_id) REFERENCES dbo.match_participant(participant_id),
  CONSTRAINT FK_cd_to FOREIGN KEY (to_participant_id) REFERENCES dbo.match_participant(participant_id),
  CONSTRAINT FK_cd_commander FOREIGN KEY (commander_oracle_id) REFERENCES dbo.oracle_card(oracle_id)
);

CREATE TABLE dbo.ruling_reference (
  event_id NVARCHAR(64) NOT NULL, oracle_id NVARCHAR(64), ruling_id INT, note NVARCHAR(1000),
  CONSTRAINT PK_ruling_reference PRIMARY KEY (event_id),
  CONSTRAINT FK_rr_event FOREIGN KEY (event_id) REFERENCES dbo.log_event(event_id),
  CONSTRAINT FK_rr_oracle FOREIGN KEY (oracle_id) REFERENCES dbo.oracle_card(oracle_id),
  CONSTRAINT FK_rr_ruling FOREIGN KEY (ruling_id) REFERENCES dbo.card_ruling(ruling_id)
);

CREATE TABLE dbo.infraction (
  infraction_id NVARCHAR(64) NOT NULL, match_id NVARCHAR(64), game_id NVARCHAR(64),
  participant_id NVARCHAR(64), seq INT, code NVARCHAR(50), description NVARCHAR(1000), resolved BIT,
  CONSTRAINT PK_infraction PRIMARY KEY (infraction_id),
  CONSTRAINT FK_inf_match FOREIGN KEY (match_id) REFERENCES dbo.match(match_id),
  CONSTRAINT FK_inf_game FOREIGN KEY (game_id) REFERENCES dbo.game(game_id),
  CONSTRAINT FK_inf_participant FOREIGN KEY (participant_id) REFERENCES dbo.match_participant(participant_id)
);

CREATE TABLE dbo.participant_combo_use (
  participant_id NVARCHAR(64) NOT NULL, combo_id NVARCHAR(64) NOT NULL, detected BIT, first_seen_seq INT,
  CONSTRAINT PK_participant_combo_use PRIMARY KEY (participant_id, combo_id),
  CONSTRAINT FK_pcu_participant FOREIGN KEY (participant_id) REFERENCES dbo.match_participant(participant_id),
  CONSTRAINT FK_pcu_combo FOREIGN KEY (combo_id) REFERENCES dbo.combo(combo_id)
);

CREATE TABLE dbo.ability_parse (
  face_id INT NOT NULL, parser_version NVARCHAR(50), tokens_json NVARCHAR(MAX),
  symbols_json NVARCHAR(MAX), layers_json NVARCHAR(MAX), parsed_at DATETIME2(0),
  CONSTRAINT PK_ability_parse PRIMARY KEY (face_id),
  CONSTRAINT FK_ap_face FOREIGN KEY (face_id) REFERENCES dbo.card_face(face_id)
);

CREATE TABLE dbo.combo_detection_run (
  run_id NVARCHAR(64) NOT NULL, game_id NVARCHAR(64), algorithm NVARCHAR(100), version NVARCHAR(50), created_at DATETIME2(0),
  CONSTRAINT PK_combo_detection_run PRIMARY KEY (run_id),
  CONSTRAINT FK_cdr_game FOREIGN KEY (game_id) REFERENCES dbo.game(game_id)
);
GO

-- Part 11: Rollups, search, data quality
CREATE TABLE dbo.card_rollup_daily (
  as_of NVARCHAR(20) NOT NULL, oracle_id NVARCHAR(64) NOT NULL, avg_price DECIMAL(18,4),
  best_finish NVARCHAR(50), legality_bitmap NVARCHAR(200),
  CONSTRAINT PK_card_rollup_daily PRIMARY KEY (as_of, oracle_id),
  CONSTRAINT FK_crd_oracle FOREIGN KEY (oracle_id) REFERENCES dbo.oracle_card(oracle_id)
);
CREATE TABLE dbo.commander_rollup_daily (
  as_of NVARCHAR(20) NOT NULL, oracle_id NVARCHAR(64) NOT NULL,
  rank INT, meta_share DECIMAL(18,4), deck_count INT,
  CONSTRAINT PK_commander_rollup_daily PRIMARY KEY (as_of, oracle_id),
  CONSTRAINT FK_crld_oracle FOREIGN KEY (oracle_id) REFERENCES dbo.oracle_card(oracle_id)
);
CREATE TABLE dbo.deck_perf (
  deck_id NVARCHAR(64) NOT NULL, version_no INT NOT NULL,
  games INT, wins INT, avg_turns_to_win FLOAT, mulligan_rate FLOAT,
  CONSTRAINT PK_deck_perf PRIMARY KEY (deck_id, version_no),
  CONSTRAINT FK_dp_deckver FOREIGN KEY (deck_id, version_no) REFERENCES dbo.deck_version(deck_id, version_no)
);
CREATE TABLE dbo.dq_issue (
  entity_type NVARCHAR(50) NOT NULL, entity_id NVARCHAR(64) NOT NULL, issue_code NVARCHAR(64) NOT NULL,
  detected_at DATETIME2(0), status NVARCHAR(50), event_id NVARCHAR(64),
  CONSTRAINT PK_dq_issue PRIMARY KEY (entity_type, entity_id, issue_code),
  CONSTRAINT FK_dq_event FOREIGN KEY (event_id) REFERENCES dbo.audit_event(event_id)
);
CREATE TABLE dbo.search_index (
  entity_type NVARCHAR(50) NOT NULL, entity_id NVARCHAR(64) NOT NULL, lang_code NVARCHAR(16) NOT NULL,
  text NVARCHAR(MAX), ngrams_json NVARCHAR(MAX),
  CONSTRAINT PK_search_index PRIMARY KEY (entity_type, entity_id, lang_code),
  CONSTRAINT FK_si_lang FOREIGN KEY (lang_code) REFERENCES dbo.dim_language(lang_code)
);
GO
