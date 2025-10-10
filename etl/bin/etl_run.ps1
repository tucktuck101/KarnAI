# Simple orchestrator stub
Write-Host "Starting ETL run..."
python -m etl.jobs.scryfall.fetch_oracle
python -m etl.jobs.scryfall.fetch_all_cards
python -m etl.jobs.scryfall.stage_oracle
python -m etl.jobs.scryfall.stage_cards
python -m etl.jobs.scryfall.load_core
Write-Host "ETL run completed."
