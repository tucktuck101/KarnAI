import argparse
from pathlib import Path

CFG_DIMS = Path("etl/config/dims.yml")
CFG_BULK = Path("etl/config/bulk.yml")
CACHE = Path("etl/cache")
CACHE.mkdir(parents=True, exist_ok=True)


def main():
    ap = argparse.ArgumentParser(prog="etl")
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("catalogs")
    sp.add_parser("bulk")
    args = ap.parse_args()
    if args.cmd == "catalogs":
        print("TODO: implement: fetch Scryfall catalogs, upsert dims via pyodbc MERGE")
        print("Config:", CFG_DIMS)
    elif args.cmd == "bulk":
        print(
            "TODO: implement: download JSONL bulks with ETag to etl/cache, stage to stg.*, then MERGE"
        )
        print("Config:", CFG_BULK)


if __name__ == "__main__":
    main()
