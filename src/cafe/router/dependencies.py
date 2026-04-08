"""Factory-Funktionen für Dependency Injection."""

from typing import Annotated

from fastapi import Depends

from cafe.repository.cafe_repository import CafeRepository
from cafe.security.dependencies import get_user_service
from cafe.security.user_service import UserService
from cafe.service.cafe_service import CafeService
from cafe.service.cafe_write_service import CafeWriteService


def get_repository() -> CafeRepository:
    """Factory-Funktion für CafeRepository.

    :return: Das Repository
    :rtype: CafeRepository
    """
    return CafeRepository()


def get_service(
    repo: Annotated[CafeRepository, Depends(get_repository)],
) -> CafeService:
    """Factory-Funktion für CafeService."""
    return CafeService(repo=repo)


def get_write_service(
    repo: Annotated[CafeRepository, Depends(get_repository)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> CafeWriteService:
    """Factory-Funktion für CafeWriteService."""
    return CafeWriteService(repo=repo, user_service=user_service)
