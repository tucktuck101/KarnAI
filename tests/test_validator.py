from karnai.models.card import Card, Face
from karnai.validator.deck import validate_commander_deck


def test_deck_singleton_check():
    c = Card(
        id="1",
        name="A",
        faces=[Face(name="A", type_line="Artifact")],
        type_line="Artifact",
    )
    errs = validate_commander_deck([c, c])
    assert any("singleton" in e for e in errs)
