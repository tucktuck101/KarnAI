from karnai.deck import DeckValidator
from karnai.schemas import Decklist


def test_valid_mono_green_deck():
    # Color lookup for a tiny universe
    ci_map = {
        "Ezuri, Renegade Leader": ["G"],
        "Llanowar Elves": ["G"],
        "Elvish Mystic": ["G"],
        "Forest": [],
    }

    def lookup(name: str):
        return ci_map.get(name, [])

    # Build a 100-card mono-green deck: 1 commander + 2 creatures + 97 Forests
    cards = ["Llanowar Elves", "Elvish Mystic"] + ["Forest"] * 97
    deck = Decklist(
        name="Mono-Green Elves",
        commander="Ezuri, Renegade Leader",
        partner=None,
        cards=cards,
        color_identity=["G"],
    )
    res = DeckValidator().validate(deck, lookup)
    assert res.is_valid, f"Issues: {res.issues}"


def test_banned_card_detected():
    ci_map = {
        "Ezuri, Renegade Leader": ["G"],
        "Shahrazad": ["W"],
        "Forest": [],
    }

    def lookup(name: str):
        return ci_map.get(name, [])

    cards = ["Shahrazad"] + ["Forest"] * 98  # 1 commander + 99 others = 100
    deck = Decklist(
        name="Bad Deck",
        commander="Ezuri, Renegade Leader",
        partner=None,
        cards=cards,
        color_identity=["G"],
    )
    res = DeckValidator().validate(deck, lookup)
    assert not res.is_valid
    assert any("Banned cards present" in m for m in res.issues)


def test_color_identity_violation():
    ci_map = {
        "Ezuri, Renegade Leader": ["G"],
        "Counterspell": ["U"],
        "Forest": [],
    }

    def lookup(name: str):
        return ci_map.get(name, [])

    cards = ["Counterspell"] + ["Forest"] * 98
    deck = Decklist(
        name="Oops",
        commander="Ezuri, Renegade Leader",
        partner=None,
        cards=cards,
        color_identity=["G"],
    )
    res = DeckValidator().validate(deck, lookup)
    assert not res.is_valid
    assert any("Color identity violation" in m for m in res.issues)
