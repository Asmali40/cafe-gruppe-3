"""CafeWriteRouter."""

from typing import Annotated, Final

from fastapi import APIRouter, Depends, Request, Response, status
from loguru import logger

from cafe.problem_details import create_problem_details
from cafe.router.constants import IF_MATCH, IF_MATCH_MIN_LEN
from cafe.router.dependencies import get_write_service
from cafe.router.cafe_model import CafeModel
from cafe.router.cafe_update_model import CafeUpdateModel
from cafe.security import Role, RolesRequired
from cafe.service import CafeWriteService

__all__ = ["cafe_write_router"]


cafe_write_router: Final = APIRouter(tags=["Schreiben"])


@cafe_write_router.post("")
def post(
    cafe_model: CafeModel,
    request: Request,
    service: Annotated[CafeWriteService, Depends(get_write_service)],
) -> Response:
    """POST-Request, um ein neues Café anzulegen.

    :param cafe_model: Café-Daten als Pydantic-Model
    :param request: Injiziertes Request-Objekt von FastAPI bzw. Starlette
        mit der Request-URL
    :param service: Injizierter Service für Geschäftslogik
    :rtype: Response
    :raises ValidationError: Falls es bei Pydantic Validierungsfehler gibt
    :raises EmailExistsError: Falls die Emailadresse bereits existiert
    """
    logger.debug("cafe_model={}", cafe_model)
    cafe_dto: Final = service.create(cafe=cafe_model.to_cafe())
    logger.debug("cafe_dto={}", cafe_dto)

    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={"Location": f"{request.url}/{cafe_dto.id}"},
    )


@cafe_write_router.put(
    "/{cafe_id}",
    dependencies=[Depends(RolesRequired([Role.ADMIN, Role.PATIENT]))],
)
def put(
    cafe_id: int,
    cafe_update_model: CafeUpdateModel,
    request: Request,
    service: Annotated[CafeWriteService, Depends(get_write_service)],
) -> Response:
    """PUT-Request, um ein Café zu aktualisieren.

    :param cafe_id: ID des zu aktualisierenden Cafés als Pfadparameter
    :param cafe_update_model: Neue Café-Daten als Pydantic-Model
    :param request: Injiziertes Request-Objekt von FastAPI bzw. Starlette
        mit If-Match im Header
    :param service: Injizierter Service für Geschäftslogik
    :return: Response mit Statuscode 204
    :rtype: Response
    :raises EmailExistsError: Falls die neue Emailadresse bereits existiert
    :raises NotFoundError: Falls zur ID kein Café existiert
    :raises VersionOutdatedError: Falls die Versionsnummer nicht aktuell ist
    """
    if_match_value: Final = request.headers.get(IF_MATCH)
    logger.debug(
        "cafe_id={}, if_match={}, cafe_update_model={}",
        cafe_id,
        if_match_value,
        cafe_update_model,
    )

    if if_match_value is None:
        return create_problem_details(
            status_code=status.HTTP_428_PRECONDITION_REQUIRED,
        )

    if (
        len(if_match_value) < IF_MATCH_MIN_LEN
        or not if_match_value.startswith('"')
        or not if_match_value.endswith('"')
    ):
        return create_problem_details(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
        )

    version: Final = if_match_value[1:-1]
    try:
        version_int: Final = int(version)
    except ValueError:
        return Response(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
        )

    cafe: Final = cafe_update_model.to_cafe()
    cafe_modified: Final = service.update(
        cafe=cafe,
        cafe_id=cafe_id,
        version=version_int,
    )
    logger.debug("cafe_modified={}", cafe_modified)

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
        headers={"ETag": f'"{cafe_modified.version}"'},
    )


@cafe_write_router.delete(
    "/{cafe_id}",
    dependencies=[Depends(RolesRequired([Role.ADMIN, Role.PATIENT]))],
)
def delete_by_id(
    cafe_id: int,
    service: Annotated[CafeWriteService, Depends(get_write_service)],
) -> Response:
    """DELETE-Request, um ein Café anhand seiner ID zu löschen.

    :param cafe_id: ID des zu löschenden Cafés
    :param service: Injizierter Service für Geschäftslogik
    :return: Response mit Statuscode 204
    :rtype: Response
    """
    logger.debug("cafe_id={}", cafe_id)
    service.delete_by_id(cafe_id=cafe_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
