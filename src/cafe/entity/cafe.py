"""Entity-Klasse für Cafe-Daten."""

from dataclasses import InitVar
from datetime import date, datetime
from typing import Any, Self

from loguru import logger
from sqlalchemy import JSON, Identity, func
from sqlalchemy.orm import Mapped, mapped_column, reconstructor, relationship

from cafe.entity.base import Base
from cafe.entity.cafe_manager import CafeManager
from cafe.entity.produkt import Produkt
from cafe.entity.kaffeeart import Kaffeeart


# noinspection PyUnresolvedReferences
class Cafe(Base):
    """Entity-Klasse für Cafe-Daten."""

    __tablename__ = "cafe"

    name: Mapped[str]
    """Der Name des Cafés."""

    kategorie: Mapped[int]
    """Die Kategorie (Sternebewertung 1–9)."""

    gruendungsdatum: Mapped[date]
    """Das Gründungsdatum."""

    kaffeesorten: InitVar[list[Kaffeeart] | None]
    """Die transiente Liste mit Kaffeesorten als Enum-Werte."""

    id: Mapped[int | None] = mapped_column(
        Identity(start=1000),
        primary_key=True,
    )
    """Die generierte ID gemäß der zugehörigen IDENTITY-Spalte."""

    email: Mapped[str] = mapped_column(unique=True)
    """Die eindeutige Emailadresse."""

    username: Mapped[str]
    """Der Benutzername für Login."""

    cafe_manager: Mapped[CafeManager] = relationship(
        back_populates="cafe",
        innerjoin=True,
        cascade="save-update, delete",
    )
    """Der in einer 1:1-Beziehung referenzierte CafeManager."""

    produkte: Mapped[list[Produkt]] = relationship(
        back_populates="cafe",
        cascade="save-update, delete",
    )
    """Die in einer 1:N-Beziehung referenzierten Produkte."""

    # JSON ist in Python kein Typ, sondern nur Syntax fuer Strings mit codierten Daten
    kaffeesorten_json: Mapped[list[str] | None] = mapped_column(
        JSON,
        name="kaffeesorten",
        init=False,
    )
    """Die persistente Liste der Kaffeesorten für ein JSON-Array."""

    version: Mapped[int] = mapped_column(nullable=False, default=0)
    """Die Versionsnummer für optimistische Synchronisation."""

    erzeugt: Mapped[datetime | None] = mapped_column(
        insert_default=func.now(),
        default=None,
    )
    """Der Zeitstempel für das initiale INSERT in die DB-Tabelle."""

    aktualisiert: Mapped[datetime | None] = mapped_column(
        insert_default=func.now(),
        onupdate=func.now(),
        default=None,
    )
    """Der Zeitstempel vom letzten UPDATE in der DB-Tabelle."""

    __mapper_args__ = {"version_id_col": version}

    # Argumente in der Reihenfolge, wie die InitVar-Attribute deklariert sind
    def __post_init__(
        self,
        kaffeesorten: list[Kaffeeart] | None,
    ) -> None:
        """Für SQLAlchemy: JSON-Array für DB-Spalte setzen für INSERT oder UPDATE.

        :param kaffeesorten: Liste mit Kaffeesorten als Enum
        """
        logger.debug("kaffeesorten={}", kaffeesorten)
        logger.debug("self={}", self)
        self.kaffeesorten_json = (
            [kaffeeart.name for kaffeeart in kaffeesorten]
            if kaffeesorten is not None
            else None
        )
        logger.debug("self.kaffeesorten_json={}", self.kaffeesorten_json)

    # alternativ: @event.listens_for(Cafe, 'load')
    @reconstructor
    def on_load(self) -> None:
        """Auslesen aus der DB: die Enum-Liste durch die DB-Strings initialisieren."""
        self.kaffeesorten = (  # pyright: ignore[reportAttributeAccessIssue]
            [Kaffeeart[kaffeeart_name] for kaffeeart_name in self.kaffeesorten_json]
            if self.kaffeesorten_json is not None
            else []
        )
        logger.debug(
            "kaffeesorten={}",
            self.kaffeesorten,  # pyright: ignore[reportAttributeAccessIssue]
        )

    def set(self, cafe: Self) -> None:
        """Primitive Attributwerte überschreiben, z.B. vor DB-Update.

        :param cafe: Cafe-Objekt mit den aktuellen Daten
        """
        self.name = cafe.name
        self.email = cafe.email
        self.kategorie = cafe.kategorie
        self.gruendungsdatum = cafe.gruendungsdatum

    def __eq__(self, other: Any) -> bool:
        """Vergleich auf Gleichheit, ohne Joins zu verursachen."""
        # Vergleich der Referenzen: id(self) == id(other)
        if self is other:
            return True
        if not isinstance(other, type(self)):
            return False
        return self.id is not None and self.id == other.id

    def __hash__(self) -> int:
        """Hash-Funktion anhand der ID, ohne Joins zu verursachen."""
        return hash(self.id) if self.id is not None else hash(type(self))

    # __repr__ fuer Entwickler/innen, __str__ fuer User
    def __repr__(self) -> str:
        """Ausgabe eines Cafés als String, ohne Joins zu verursachen."""
        return (
            f"Cafe(id={self.id}, version={self.version}, "
            + f"name={self.name}, email={self.email}, "
            + f"kategorie={self.kategorie}, "
            + f"gruendungsdatum={self.gruendungsdatum}, "
            + f"kaffeesorten_json={self.kaffeesorten_json}, "
            + f"erzeugt={self.erzeugt}, aktualisiert={self.aktualisiert})"
        )
