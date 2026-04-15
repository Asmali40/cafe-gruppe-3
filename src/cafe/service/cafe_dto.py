"""DTO-Klasse für Café-Daten, insbesondere ohne Decorators für SQLAlchemy."""

from dataclasses import dataclass
from datetime import date

import strawberry

from cafe.entity import Cafe, Kaffeeart
from cafe.service.cafe_manager_dto import CafeManagerDTO

__all__ = ["CafeDTO"]


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
# Strawberry konvertiert automatisch zwischen snake_case (Python) und camelCase (Schema)
@strawberry.type
class CafeDTO:
    """DTO-Klasse für aus gelesene oder gespeicherte Café-Daten: ohne Decorators."""

    id: int
    version: int
    name: str
    email: str
    kategorie: int
    gruendungsdatum: date
    cafe_manager: CafeManagerDTO
    kaffeesorten: list[Kaffeeart]
    username: str | None

    # asdict kann nicht verwendet werden: Rueckwaertsverweise Cafe - CafeManager
    def __init__(self, cafe: Cafe):
        """Initialisierung von CafeDTO durch ein Entity-Objekt von Cafe.

        :param cafe: Cafe-Objekt mit Decorators zu SQLAlchemy
        """
        cafe_id = cafe.id
        self.id = cafe_id if cafe_id is not None else -1
        self.version = cafe.version
        self.name = cafe.name
        self.email = cafe.email
        self.kategorie = cafe.kategorie
        self.gruendungsdatum = cafe.gruendungsdatum
        self.cafe_manager = CafeManagerDTO(cafe.cafe_manager)
        self.kaffeesorten = (
            [Kaffeeart[kaffeeart_name] for kaffeeart_name in cafe.kaffeesorten_json]
            if cafe.kaffeesorten_json is not None
            else []
        )
        self.username = cafe.username if cafe.username is not None else "N/A"
