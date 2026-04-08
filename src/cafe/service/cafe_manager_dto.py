
"""DTO-Klasse für den CafeManager, insbesondere ohne Decorators für SQLAlchemy."""

from dataclasses import dataclass

import strawberry

from cafe.entity import CafeManager

__all__ = ["CafeManagerDTO"]


# Mit der Funktion asdict() kann ein Objekt einfach in ein dict konvertiert werden
# init=True (default): __init__ fuer die "member variables" wird generiert
# eq=True (default): __eq__ wird generiert
# unsafe_hash=False (default): __hash__ passend zu __eq__ wird generiert
# repr=True (default): __repr__ wird generiert
# frozen=False (default): mutable
# kw_only=False (default): Initialisierungs-Fkt auch ohne "Keyword Arguments" aufrufen
# slots=False (default): __dict__ zur Speicherung statt slots
# slots: schnellerer Zugriff, kompakte Speicherung
@dataclass(eq=False, slots=True, kw_only=True)
@strawberry.type
class CafeManagerDTO:
    """DTO-Klasse für den CafeManager, insbesondere ohne Decorators für SQLAlchemy."""

    vorname: str
    nachname: str

    def __init__(self, cafe_manager: CafeManager) -> None:
        """Initialisierung von CafeManagerDTO durch ein Entity-Objekt von CafeManager.

        :param cafe_manager: CafeManager-Objekt mit Decorators für SQLAlchemy
        """
        self.vorname = cafe_manager.vorname
        self.nachname = cafe_manager.nachname
