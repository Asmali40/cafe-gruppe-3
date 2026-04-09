"""Pydantic-Model für die Café-Daten."""

from typing import Annotated, Final

from loguru import logger
from pydantic import StringConstraints

from cafe.entity import Cafe, Kaffeeart
from cafe.router.cafe_manager_model import CafeManagerModel
from cafe.router.cafe_update_model import CafeUpdateModel
from cafe.router.produkt_model import ProduktModel

__all__ = ["CafeModel"]


class CafeModel(CafeUpdateModel):
    """Pydantic-Model für die Café-Daten."""

    cafe_manager: CafeManagerModel
    """Der zugehörige CafeManager."""

    produkte: list[ProduktModel]
    """Die Liste der Produkte."""

    kaffeesorten: list[Kaffeeart]
    """Die Liste mit Kaffeesorten als Enum-Werte."""

    username: Annotated[str, StringConstraints(max_length=20)]
    """Der Benutzername für Login."""

    def to_cafe(self) -> Cafe:
        """Konvertierung in ein Cafe-Objekt für SQLAlchemy.

        :return: Cafe-Objekt für SQLAlchemy
        :rtype: Cafe
        """
        logger.debug("self={}", self)
        cafe_dict = self.to_dict()
        cafe_dict["kaffeesorten"] = self.kaffeesorten
        cafe_dict["username"] = self.username

        # double star operator: Dictionary auspacken als Schluessel-Wert-Paare
        cafe: Final = Cafe(**cafe_dict)
        cafe.cafe_manager = self.cafe_manager.to_cafe_manager()
        cafe.produkte = [
            produkt_model.to_produkt() for produkt_model in self.produkte
        ]
        logger.debug("cafe={}", cafe)
        return cafe
