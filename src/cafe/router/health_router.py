"""HealthRouter."""

from typing import Any, Final

from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from cafe.repository import engine

__all__ = ["router"]

router: Final = APIRouter(tags=["Health"])


@router.get("/liveness")
def liveness() -> dict[str, Any]:
    """Überprüfen der Liveness.

    :return: JSON-Datensatz mit der Statusmeldung
    :rtype: dict[str, Any]
    """
    return {"status": "up"}


@router.get("/readiness")
def readiness() -> dict[str, Any]:
    """Überprüfen der Readiness.

    :return: JSON-Datensatz mit der Statusmeldung
    :rtype: dict[str, Any]
    """
    with engine.connect() as connection:
        try:
            connection.scalar(text("SELECT 1"))
        except OperationalError:
            return {"db": "down"}
    return {"db": "up"}
