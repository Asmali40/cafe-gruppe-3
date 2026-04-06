# Copyright (C) 2023 - present Juergen Zimmermann, Hochschule Karlsruhe
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
