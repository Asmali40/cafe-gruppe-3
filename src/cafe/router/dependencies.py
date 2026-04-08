"""Factory-Funktionen für Dependency Injection."""

from typing import Annotated

from fastapi import Depends

from cafe.repository.cafe_repository import CafeRepository
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
) -> CafeWriteService:
    """Factory-Funktion für CafeWriteService."""
    return CafeWriteService(repo=repo)
