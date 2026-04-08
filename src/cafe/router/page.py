"""Parameter für Pagination."""

from dataclasses import dataclass
from math import ceil
from typing import Any, Final

from cafe.repository import Pageable

__all__ = ["Page"]


@dataclass(eq=False, slots=True, kw_only=True)
class PageMeta:
    """Data class für die Metadaten einer Seite."""

    size: int
    """Maximale Anzahl Datensätze pro Seite."""

    number: int
    """Seitennummer."""

    total_elements: int
    """Gesamte Anzahl an Datensätzen."""

    total_pages: int
    """Gesamte Anzahl an Seiten."""


@dataclass(eq=False, slots=True, kw_only=True)
class Page:
    """Data class für eine Seite mit gefundenen Daten."""

    content: tuple[dict[str, Any], ...]
    """Ausschnitt der gefundenen Datensätze als Tupel, d.h. readonly Liste."""

    page: PageMeta  # NOSONAR
    """Metadaten zur Seite."""

    @staticmethod
    def create(
        content: tuple[dict[str, Any], ...], pageable: Pageable, total_elements: int
    ) -> Page:
        """Eine Seite mit einem Datenausschnitt und Metadaten erstellen."""
        total_pages: Final = ceil(total_elements / pageable.size)
        page_meta = PageMeta(
            size=pageable.size,
            number=pageable.number,
            total_elements=total_elements,
            total_pages=total_pages,
        )
        return Page(content=content, page=page_meta)
