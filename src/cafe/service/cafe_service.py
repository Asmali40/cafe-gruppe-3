"""Geschäftslogik zum Lesen von Café-Daten."""

from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Final

from loguru import logger
from openpyxl import Workbook  # pyright: ignore[reportMissingModuleSource]

from cafe.config import excel_enabled
from cafe.repository import (
    CafeRepository,
    Pageable,
    Session,
    Slice,
)
from cafe.service.cafe_dto import CafeDTO
from cafe.service.exceptions import NotFoundError

__all__ = ["CafeService"]


class CafeService:
    """Service-Klasse mit Geschäftslogik für Café."""

    def __init__(self, repo: CafeRepository) -> None:
        """Konstruktor mit abhängigem CafeRepository."""
        self.repo: CafeRepository = repo

    def find_by_id(self, cafe_id: int) -> CafeDTO:
        """Suche mit der Café-ID.

        :param cafe_id: ID für die Suche
        :return: Das gefundene Café
        :rtype: CafeDTO
        :raises NotFoundError: Falls kein Café gefunden wurde
        """
        logger.debug("cafe_id={}", cafe_id)

        # Session-Objekt ist die Schnittstelle zur DB, nutzt intern ein Transaktionsobj.
        # implizites "autobegin()" bei einem with-Block
        # durch "with" erhaelt man einen "Context Manager", der die Ressource/Session
        # am Endes des Blocks schliesst
        with Session() as session:
            if (
                cafe := self.repo.find_by_id(cafe_id=cafe_id, session=session)
            ) is None:
                message: Final = f"Kein Café mit der ID {cafe_id}"
                logger.debug("NotFoundError: {}", message)
                raise NotFoundError(cafe_id=cafe_id)

            cafe_dto: Final = CafeDTO(cafe)
            session.commit()

        logger.debug("{}", cafe_dto)
        return cafe_dto

    # ab Python 3.9 (2019) ist der Element-Type in eckigen Klammern und
    # der Name von eingebauten Collections ist kleingeschrieben.
    def find(
        self,
        suchparameter: Mapping[str, str],
        pageable: Pageable,
    ) -> Slice[CafeDTO]:
        """Suche mit Suchparameter.

        :param suchparameter: Suchparameter
        :param pageable: Anzahl Datensätze und Seitennummer
        :return: Ausschnitt der gefundenen Cafés
        :rtype: Slice[CafeDTO]
        :raises NotFoundError: Falls keine Cafés gefunden wurden
        """
        logger.debug("{}", suchparameter)
        with Session() as session:
            cafe_slice: Final = self.repo.find(
                suchparameter=suchparameter, pageable=pageable, session=session
            )
            if len(cafe_slice.content) == 0:
                raise NotFoundError(suchparameter=suchparameter)

            # tuple mit einem "Generator"-Ausdruck
            # vgl. List Comprehension ab Python 2.0 (2000)
            cafes_dto: Final = tuple(
                CafeDTO(cafe) for cafe in cafe_slice.content
            )
            session.commit()

        if excel_enabled:
            self._create_excelsheet(cafes_dto)
        cafes_dto_slice = Slice(
            content=cafes_dto, total_elements=cafe_slice.total_elements
        )
        logger.debug("{}", cafes_dto_slice)
        return cafes_dto_slice

    def find_namen(self, teil: str) -> Sequence[str]:
        """Suche Café-Namen zu einem Teilstring.

        :param teil: Teilstring der gesuchten Namen
        :return: Liste der gefundenen Namen oder eine leere Liste
        :rtype: Sequence[str]
        :raises NotFoundError: Falls keine Namen gefunden wurden
        """
        logger.debug("teil={}", teil)
        with Session() as session:
            namen: Final = self.repo.find_namen(teil=teil, session=session)
            session.commit()

        logger.debug("{}", namen)
        if len(namen) == 0:
            raise NotFoundError
        return namen

    def _create_excelsheet(self, cafes: tuple[CafeDTO, ...]) -> None:
        """Ein Excelsheet mit den gefundenen Cafés erstellen.

        :param cafes: Café-Daten für das Excelsheet
        """
        workbook: Final = Workbook()
        worksheet: Final = workbook.active
        if worksheet is None:
            return

        worksheet.append(["Name", "Emailadresse", "Kategorie", "Gründungsdatum"])
        for cafe in cafes:
            worksheet.append((
                cafe.name,
                cafe.email,
                cafe.kategorie,
                str(cafe.gruendungsdatum),
            ))

        timestamp: Final = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        workbook.save(f"cafes-{timestamp}.xlsx")
