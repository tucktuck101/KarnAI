# ETL Makefile (keeps root layout unchanged)
PY=python

db-seed:
	powershell -ExecutionPolicy Bypass -File bin/sqlcmd_all.ps1 etl/sql/seeds

scryfall:
	$(PY) -m etl.jobs.scryfall.load_core

edhrec:
	$(PY) -m etl.jobs.edhrec.load_commander
