"""Basisklasse für Entity-Klassen."""

from typing import TYPE_CHECKING, Any

from sqlalchemy.orm import DeclarativeBase

if TYPE_CHECKING:

    class MappedAsDataclass:
        """Mixin class ohne die Directiven von PEP 681."""

        def __init__(self, *arg: Any, **kw: Any) -> None:
            """Mixin class ohne die Directiven von PEP 681."""

else:
    from sqlalchemy.orm import MappedAsDataclass


class Base(MappedAsDataclass, DeclarativeBase):
    """Basisklasse für Entity-Klassen als dataclass."""
