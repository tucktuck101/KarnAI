from karnai.data.scryfall_loader import OracleLoaderFile
from karnai.schemas import Card


def test_oracle_loader_normalizes_cards(tmp_path):
    cache = tmp_path / ".cache"
    loader = OracleLoaderFile("tests/fixtures/oracle_sample.json", cache_dir=cache)
    cards = list(loader.load_cards())
    assert len(cards) >= 2
    # Validate with Pydantic
    c0 = Card.model_validate(cards[0])
    assert c0.name and isinstance(c0.mana_value, float)
    # Second run should hit parquet cache
    cards2 = list(loader.load_cards())
    assert len(cards2) == len(cards)
