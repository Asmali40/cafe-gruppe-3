"""REST-Schnittstelle für Shutdown."""

import os
import signal
from typing import Any, Final

from fastapi import APIRouter, Depends
from loguru import logger

from cafe.security.role import Role
from cafe.security.roles_required import RolesRequired

__all__ = ["router"]


router: Final = APIRouter(tags=["Admin"])


@router.post("/shutdown", dependencies=[Depends(RolesRequired(Role.ADMIN))])
def shutdown() -> dict[str, Any]:
    """Der Server wird heruntergefahren."""
    logger.warning("Server shutting down without calling cleanup handlers.")
    os.kill(os.getpid(), signal.SIGINT)  # NOSONAR
    return {"message": "Server is shutting down..."}
