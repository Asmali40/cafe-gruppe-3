"""Entity-Klasse für Produkte."""

from decimal import Decimal

from sqlalchemy import ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cafe.entity.base import Base


class Produkt(Base):
    """Entity-Klasse für Produkte."""

    __tablename__ = "produkt"

    name: Mapped[str]
    """Der Name des Produkts."""

    # Genauigkeit ("precision"): 28
    preis: Mapped[Decimal]
    """Der Preis."""

    waehrung: Mapped[str]
    """Die Währung."""

    id: Mapped[int] = mapped_column(
        Identity(start=1000),
        primary_key=True,
    )
    """Die generierte ID gemäß der zugehörigen IDENTITY-Spalte."""

    cafe_id: Mapped[int] = mapped_column(ForeignKey("cafe.id"))
    """ID des zugehörigen Cafés als Fremdschlüssel in der DB-Tabelle."""

    cafe: Mapped[Cafe] = relationship(  # noqa: F821 # ty: ignore[unresolved-reference] # pyright: ignore[reportUndefinedVariable]
        back_populates="produkte",
    )
    """Das zugehörige transiente Cafe-Objekt."""

    # __repr__ fuer Entwickler/innen, __str__ fuer User
    def __repr__(self) -> str:
        """Ausgabe eines Produkts als String ohne die Cafe-Daten."""
        return (
            f"Produkt(id={self.id}, name={self.name}, "
            + f"preis={self.preis}, waehrung={self.waehrung})"
        )
