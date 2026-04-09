"""Input-Typen für die GraphQL-Schnittstelle."""

from datetime import date
from decimal import Decimal

import strawberry

from cafe.entity import Kaffeeart

__all__ = [
    "CafeInput",
    "CafeManagerInput",
    "CreatePayload",
    "ProduktInput",
    "Suchparameter",
]


@strawberry.input
class Suchparameter:
    """Suchparameter für die Suche nach Cafés."""

    name: str | None = None
    """Name als Suchkriterium."""

    email: str | None = None
    """Emailadresse als Suchkriterium."""


@strawberry.input
class CafeManagerInput:
    """Daten für den Manager eines neuen Cafés."""

    vorname: str
    """Vorname des Café-Managers."""

    nachname: str
    """Nachname des Café-Managers."""


@strawberry.input
class ProduktInput:
    """Daten für ein Produkt eines neuen Cafés."""

    name: str
    """Name des Produkts."""

    preis: Decimal
    """Preis des Produkts."""

    waehrung: str
    """Währung (3 Großbuchstaben, z.B. EUR)."""


@strawberry.input
class CafeInput:
    """Daten für ein neues Café."""

    name: str
    """Name des Cafés."""

    email: str
    """Emailadresse des Cafés."""

    kategorie: int
    """Kategorie (Sternebewertung 1–9)."""

    gruendungsdatum: date
    """Gründungsdatum des Cafés."""

    cafe_manager: CafeManagerInput
    """Manager des Cafés."""

    produkte: list[ProduktInput]
    """Liste der Produkte."""

    kaffeesorten: list[Kaffeeart]
    """Liste der Kaffeesorten."""

    username: str
    """Benutzername für Login."""


@strawberry.type
class CreatePayload:
    """Resultat-Typ, wenn ein neues Café angelegt wurde."""

    id: int
    """ID des neu angelegten Cafés."""


@strawberry.type
class LoginResult:
    """Resultat-Typ, wenn ein Login erfolgreich war."""

    token: str
    """Token des eingeloggten Users."""

    expiresIn: str  # noqa: N815  # NOSONAR
    """Gültigkeitsdauer des Tokens."""

    roles: list[str]
    """Rollen des eingeloggten Users."""
