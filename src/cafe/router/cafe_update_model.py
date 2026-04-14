"""Pydantic-Model zum Aktualisieren von Café-Daten."""

from datetime import date
from typing import Annotated, Any

from loguru import logger
from pydantic import BaseModel, ConfigDict, EmailStr, Field, StringConstraints

from cafe.entity.cafe import Cafe

__all__ = ["CafeUpdateModel"]


class CafeUpdateModel(BaseModel):
    """Pydantic-Model zum Aktualisieren von Café-Daten."""

    name: Annotated[
        str,
        StringConstraints(
            min_length=1,
            max_length=64,
            strip_whitespace=True,
        ),
    ]
    """Der Name des Cafés."""

    email: EmailStr
    """Die eindeutige Emailadresse."""

    kategorie: Annotated[int, Field(ge=1, le=9)]
    """Die Kategorie (Sternebewertung 1-9)."""

    gruendungsdatum: date
    """Das Gründungsdatum."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Kaffeehaus Mitte",
                "email": "kaffeehaus@acme.com",
                "kategorie": 3,
                "gruendungsdatum": "2010-05-15",
            },
        }
    )

    def to_dict(self) -> dict[str, Any]:
        """Konvertierung der primitiven Attribute in ein Dictionary.

        :return: Dictionary mit den primitiven Café-Attributen
        :rtype: dict[str, Any]
        """
        # Model von Pydantic in ein Dictionary konvertieren
        cafe_dict = self.model_dump()
        cafe_dict["id"] = None
        cafe_dict["cafe_manager"] = None
        cafe_dict["produkte"] = []
        cafe_dict["kaffeesorten"] = []
        cafe_dict["username"] = None
        cafe_dict["erzeugt"] = None
        cafe_dict["aktualisiert"] = None
        return cafe_dict

    def to_cafe(self) -> Cafe:
        """Konvertierung in ein Cafe-Objekt für SQLAlchemy.

        :return: Cafe-Objekt für SQLAlchemy
        :rtype: Cafe
        """
        logger.debug("self={}", self)
        # Model von Pydantic in ein Dictionary konvertieren
        cafe_dict = self.to_dict()

        # double star operator: Dictionary auspacken als Schluessel-Wert-Paare
        cafe = Cafe(**cafe_dict)
        logger.debug("cafe={}", cafe)
        return cafe
