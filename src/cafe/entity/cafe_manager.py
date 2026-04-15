"""Entity-Klasse für den CafeManager."""

from sqlalchemy import ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cafe.entity.base import Base


class CafeManager(Base):
    """Entity-Klasse für den CafeManager."""

    __tablename__ = "cafe_manager"

    vorname: Mapped[str]
    """Der Vorname."""

    nachname: Mapped[str]
    """Der Nachname."""

    id: Mapped[int] = mapped_column(
        Identity(start=1000),
        primary_key=True,
    )
    """Die generierte ID gemäß der zugehörigen IDENTITY-Spalte."""

    cafe_id: Mapped[int] = mapped_column(ForeignKey("cafe.id"))
    """ID des zugehörigen Cafés als Fremdschlüssel in der DB-Tabelle."""

    cafe: Mapped[Cafe] = relationship(  # noqa: F821 # ty: ignore[unresolved-reference] # pyright: ignore[reportUndefinedVariable]
        back_populates="cafe_manager",
    )
    """Das zugehörige transiente Cafe-Objekt."""

    # __repr__ fuer Entwickler/innen, __str__ fuer User
    def __repr__(self) -> str:
        """Ausgabe eines CafeManagers als String ohne die Cafe-Daten."""
        return (
            f"CafeManager(id={self.id}, vorname={self.vorname}, "
            f"nachname={self.nachname})"
        )
