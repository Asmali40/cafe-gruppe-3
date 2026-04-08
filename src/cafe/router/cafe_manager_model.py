"""Pydantic-Model für den CafeManager."""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

from cafe.entity import CafeManager

__all__ = ["CafeManagerModel"]


class CafeManagerModel(BaseModel):
    """Pydantic-Model für den CafeManager."""

    vorname: Annotated[str, StringConstraints(max_length=64)]
    """Vorname des Café-Managers."""

    nachname: Annotated[str, StringConstraints(max_length=64)]
    """Nachname des Café-Managers."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "vorname": "Max",
                "nachname": "Mustermann",
            },
        }
    )

    def to_cafe_manager(self) -> CafeManager:
        """Konvertierung in ein CafeManager-Objekt für SQLAlchemy.

        :return: CafeManager-Objekt für SQLAlchemy
        :rtype: CafeManager
        """
        # Model von Pydantic in ein Dictionary konvertieren
        cafe_manager_dict = self.model_dump()
        cafe_manager_dict["id"] = None
        cafe_manager_dict["cafe_id"] = None
        cafe_manager_dict["cafe"] = None

        # double star operator: Dictionary auspacken als Schluessel-Wert-Paare
        return CafeManager(**cafe_manager_dict)
