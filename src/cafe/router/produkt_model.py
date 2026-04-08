"""Pydantic-Model für die Produkte."""

from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

from cafe.entity import Produkt

__all__ = ["ProduktModel"]


class ProduktModel(BaseModel):
    """Pydantic-Model für ein Produkt."""

    name: Annotated[str, StringConstraints(max_length=64)]
    """Der Name des Produkts."""

    preis: Decimal
    """Der Preis des Produkts."""

    waehrung: Annotated[str, StringConstraints(pattern=r"^[A-Z]{3}$")]
    """Die Währung (3 Großbuchstaben, z.B. EUR)."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Cappuccino",
                "preis": "3.50",
                "waehrung": "EUR",
            },
        }
    )

    def to_produkt(self) -> Produkt:
        """Konvertierung in ein Produkt-Objekt für SQLAlchemy.

        :return: Produkt-Objekt für SQLAlchemy
        :rtype: Produkt
        """
        produkt_dict = self.model_dump()
        produkt_dict["id"] = None
        produkt_dict["cafe_id"] = None
        produkt_dict["cafe"] = None

        return Produkt(**produkt_dict)
