"""CafeGetRouter."""

from dataclasses import asdict
from typing import Annotated, Any, Final

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import JSONResponse
from loguru import logger

from cafe.repository import Pageable
from cafe.repository.slice import Slice
from cafe.router.constants import ETAG, IF_NONE_MATCH, IF_NONE_MATCH_MIN_LEN
from cafe.router.dependencies import get_service
from cafe.router.page import Page
from cafe.security import Role, RolesRequired, User
from cafe.service import CafeDTO, CafeService

__all__ = ["cafe_router"]


# APIRouter auf Basis der Klasse Router von Starlette
cafe_router: Final = APIRouter(tags=["Lesen"])


@cafe_router.get(
    "/{cafe_id}",
    dependencies=[Depends(RolesRequired([Role.ADMIN, Role.CAFE]))],
)
def get_by_id(
    cafe_id: int,
    request: Request,
    service: Annotated[CafeService, Depends(get_service)],
) -> Response:
    """Suche mit der Café-ID.

    :param cafe_id: ID des gesuchten Cafés als Pfadparameter
    :param request: Injiziertes Request-Objekt von FastAPI bzw. Starlette
        mit ggf. If-None-Match im Header
    :param service: Injizierter Service für Geschäftslogik
    :return: Response mit dem gefundenen Café-Datensatz
    :rtype: Response
    :raises NotFoundError: Falls kein Café gefunden wurde
    """
    # User-Objekt ist durch Depends(RolesRequired()) in Request.state gepuffert
    user: Final[User] = request.state.current_user
    logger.debug("cafe_id={}, user={}", cafe_id, user)

    cafe: Final = service.find_by_id(cafe_id=cafe_id, user=user)
    logger.debug("{}", cafe)

    if_none_match: Final = request.headers.get(IF_NONE_MATCH)
    if (
        if_none_match is not None
        and len(if_none_match) >= IF_NONE_MATCH_MIN_LEN
        and if_none_match.startswith('"')
        and if_none_match.endswith('"')
    ):
        version = if_none_match[1:-1]
        logger.debug("version={}", version)
        if version is not None:
            try:
                if int(version) == cafe.version:
                    return Response(status_code=status.HTTP_304_NOT_MODIFIED)
            except ValueError:
                logger.debug("invalid version={}", version)

    return JSONResponse(
        content=_cafe_to_dict(cafe),
        headers={ETAG: f'"{cafe.version}"'},
    )


@cafe_router.get(
    "",
    dependencies=[Depends(RolesRequired(Role.ADMIN))],
)
def get(
    request: Request,
    service: Annotated[CafeService, Depends(get_service)],
) -> JSONResponse:
    """Suche mit Query-Parameter.

    :param request: Injiziertes Request-Objekt von FastAPI bzw. Starlette
        mit Query-Parameter
    :param service: Injizierter Service für Geschäftslogik
    :return: Response mit einer Seite mit Café-Daten
    :rtype: JSONResponse
    :raises NotFoundError: Falls keine Cafés gefunden wurden
    """
    query_params: Final = request.query_params
    log_str: Final = "{}"
    logger.debug(log_str, query_params)

    page: Final = query_params.get("page")
    size: Final = query_params.get("size")
    pageable: Final = Pageable.create(number=page, size=size)

    suchparameter = dict(query_params)
    if "page" in query_params:
        del suchparameter["page"]
    if "size" in query_params:
        del suchparameter["size"]

    cafe_slice: Final = service.find(suchparameter=suchparameter, pageable=pageable)

    result: Final = _cafe_slice_to_page(cafe_slice, pageable)
    logger.debug(log_str, result)
    return JSONResponse(content=result)


@cafe_router.get(
    "/namen/{teil}",
    dependencies=[Depends(RolesRequired(Role.ADMIN))],
)
def get_namen(
    teil: str,
    service: Annotated[CafeService, Depends(get_service)],
) -> JSONResponse:
    """Suche Café-Namen zum gegebenen Teilstring.

    :param teil: Teilstring der gefundenen Namen
    :param service: Injizierter Service für Geschäftslogik
    :return: Response mit Statuscode 200 und gefundenen Namen im Body
    :rtype: JSONResponse
    :raises NotFoundError: Falls keine Namen gefunden wurden
    """
    logger.debug("teil={}", teil)
    namen: Final = service.find_namen(teil=teil)
    return JSONResponse(content=namen)


def _cafe_slice_to_page(
    cafe_slice: Slice[CafeDTO],
    pageable: Pageable,
) -> dict[str, Any]:
    cafe_dict: Final = tuple(_cafe_to_dict(cafe) for cafe in cafe_slice.content)
    page: Final = Page.create(
        content=cafe_dict,
        pageable=pageable,
        total_elements=cafe_slice.total_elements,
    )
    return asdict(obj=page)


def _cafe_to_dict(cafe: CafeDTO) -> dict[str, Any]:
    cafe_dict: Final = asdict(obj=cafe)
    cafe_dict.pop("version")
    cafe_dict.update({"gruendungsdatum": cafe.gruendungsdatum.isoformat()})
    return cafe_dict
