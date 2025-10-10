# Catalogs → dims

Order:
1) Seed non-catalog dims:
   powershell -File etl/bin/sqlcmd_all.ps1 etl/sql/seed
2) Ensure staging:
   powershell -File etl/bin/sqlcmd_all.ps1 etl/sql/staging/005_stg_catalog.sql
3) Load catalogs:
   python -m etl.jobs.scryfall.catalogs
4) Merge to dims:
   powershell -File etl/bin/run_dim_merges.ps1

Notes:
- Colors: W,U,B,R,G,C (Scryfall colors reference).
- Finishes: nonfoil, foil, etched, glossy (Scryfall API blog, SDK docs).
- Formats: seeded from legalities keys shown in API examples; you can extend later when new keys appear.
