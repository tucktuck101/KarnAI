from __future__ import annotations

from typing import Any, Iterable, Mapping, Protocol


class DataSource(Protocol):
    """Generic key-value or record source."""

    def capabilities(self) -> dict[str, bool]: ...
    def get(self, key: str) -> bytes: ...
    def list(self, prefix: str = "") -> Iterable[str]: ...


class CRLoader(Protocol):
    """Loads Comprehensive Rules text and provides indexed anchors."""

    def capabilities(self) -> dict[str, bool]: ...
    def load_text(self) -> str: ...
    def rules_index(self) -> Mapping[str, int]: ...  # anchor -> position


class OracleLoader(Protocol):
    """Loads normalized Scryfall Oracle data."""

    def capabilities(self) -> dict[str, bool]: ...
    def load_cards(self) -> Iterable[dict[str, Any]]: ...
