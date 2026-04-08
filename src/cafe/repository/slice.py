"""Ausschnitt an gefundenen Daten."""

from dataclasses import dataclass
from typing import TypeVar

__all__ = ["Slice"]


T = TypeVar("T")


@dataclass(eq=False, slots=True, kw_only=True)
class Slice[T]:
    """Data class für den Ausschnitt an gefundenen Daten."""

    content: tuple[T, ...]
    """Ausschnitt der gefundenen Datensätze als Tupel beliebiger Länge."""

    total_elements: int
    """Gesamte Anzahl an Datensätzen."""
