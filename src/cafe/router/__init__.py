"""Modul für die REST-Schnittstelle einschließlich Validierung."""

from collections.abc import Sequence

from cafe.router.health_router import liveness, readiness
from cafe.router.health_router import router as health_router
from cafe.router.cafe_router import cafe_router, get, get_by_id, get_namen
from cafe.router.cafe_write_router import (
    cafe_write_router,
    delete_by_id,
    post,
    put,
)
from cafe.router.shutdown_router import router as shutdown_router
from cafe.router.shutdown_router import shutdown

__all__: Sequence[str] = [
    "cafe_router",
    "cafe_write_router",
    "delete_by_id",
    "get",
    "get_by_id",
    "get_namen",
    "health_router",
    "liveness",
    "post",
    "put",
    "readiness",
    "shutdown",
    "shutdown_router",
]
