"""Enum für Kaffeesorten."""

from enum import StrEnum

import strawberry


@strawberry.enum
class Kaffeeart(StrEnum):
    """Enum für Kaffeesorten."""

    ESPRESSO = "E"
    """Espresso."""

    CAPPUCCINO = "C"
    """Cappuccino."""

    LATTE_MACCHIATO = "LM"
    """Latte Macchiato."""

    AMERICANO = "A"
    """Americano."""

    FLAT_WHITE = "FW"
    """Flat White."""

    COLD_BREW = "CB"
    """Cold Brew."""

    MATCHA = "M"
    """Matcha."""
