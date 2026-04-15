"""Schema für GraphQL durch Strawberry."""

from collections.abc import Sequence
from typing import Final

import strawberry
from fastapi import Request
from loguru import logger
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info

from cafe.config.graphql import graphql_ide
from cafe.graphql_api.graphql_types import (
    CafeInput,
    CreatePayload,
    LoginResult,
    Suchparameter,
)
from cafe.repository import CafeRepository, Pageable
from cafe.router.cafe_model import CafeModel
from cafe.security import Role, TokenService, UserService
from cafe.service import (
    CafeDTO,
    CafeService,
    CafeWriteService,
    NotFoundError,
)

__all__ = ["graphql_router"]


_repo: Final = CafeRepository()
_service: CafeService = CafeService(repo=_repo)
_user_service: UserService = UserService()
_write_service: CafeWriteService = CafeWriteService(
    repo=_repo, user_service=_user_service
)
_token_service: Final = TokenService()


@strawberry.type
class Query:
    """Queries, um Café-Daten zu lesen."""

    @strawberry.field
    def cafe(self, cafe_id: strawberry.ID, info: Info) -> CafeDTO | None:
        """Daten zu einem Café lesen.

        :param cafe_id: ID des gesuchten Cafés
        :return: Gesuchtes Café oder None
        :rtype: CafeDTO | None
        """
        logger.debug("cafe_id={}", cafe_id)

        request: Final[Request] = info.context.get("request")
        user: Final = _token_service.get_user_from_request(request=request)
        if user is None:
            return None

        try:
            cafe_dto: Final = _service.find_by_id(cafe_id=int(cafe_id), user=user)
        except NotFoundError:
            return None
        logger.debug("{}", cafe_dto)
        return cafe_dto

    @strawberry.field
    def cafes(self, suchparameter: Suchparameter, info: Info) -> Sequence[CafeDTO]:
        """Cafés anhand von Suchparameter suchen.

        :param suchparameter: name, email usw.
        :return: Die gefundenen Cafés
        :rtype: Sequence[CafeDTO]
        """
        logger.debug("suchparameter={}", suchparameter)

        request: Final[Request] = info.context["request"]
        user: Final = _token_service.get_user_from_request(request)
        if user is None or Role.ADMIN not in user.roles:
            return []

        suchparameter_dict: Final[dict[str, str]] = dict(vars(suchparameter))
        suchparameter_filtered = {
            key: value
            for key, value in suchparameter_dict.items()
            if value is not None and value
        }
        logger.debug("suchparameter_filtered={}", suchparameter_filtered)

        pageable: Final = Pageable.create(size=str(0))
        try:
            cafes_dto: Final = _service.find(
                suchparameter=suchparameter_filtered, pageable=pageable
            )
        except NotFoundError:
            return []
        logger.debug("{}", cafes_dto)
        return cafes_dto.content


@strawberry.type
class Mutation:
    """Mutations, um Café-Daten anzulegen."""

    # Mutation, weil evtl. der Login-Zeitpunkt gespeichert wird
    @strawberry.mutation
    def login(self, username: str, password: str) -> LoginResult:
        """Einen Token zu Benutzername und Passwort ermitteln.

        :param username: Benutzername
        :param password: Passwort
        :rtype: LoginResult
        """
        logger.debug("username={}, password={}", username, password)
        token_mapping = _token_service.token(username=username, password=password)

        token = token_mapping["access_token"]
        user = _token_service.get_user_from_token(token)
        roles: Final = [role.value for role in user.roles]
        return LoginResult(token=token, expiresIn="1d", roles=roles)

    @strawberry.mutation
    def create(self, cafe_input: CafeInput) -> CreatePayload:
        """Ein neues Café anlegen.

        :param cafe_input: Daten des neuen Cafés
        :return: ID des neuen Cafés
        :rtype: CreatePayload
        :raises EmailExistsError: Falls die Emailadresse bereits existiert
        """
        logger.debug("cafe_input={}", cafe_input)

        cafe_dict = cafe_input.__dict__
        cafe_dict["cafe_manager"] = cafe_input.cafe_manager.__dict__
        cafe_dict["produkte"] = [produkt.__dict__ for produkt in cafe_input.produkte]

        cafe_model: Final = CafeModel.model_validate(cafe_dict)
        cafe_dto: Final = _write_service.create(cafe=cafe_model.to_cafe())
        payload: Final = CreatePayload(id=cafe_dto.id)

        logger.debug("{}", payload)
        return payload


schema: Final = strawberry.Schema(query=Query, mutation=Mutation)

Context = dict[str, Request]


def get_context(request: Request) -> Context:
    return {"request": request}


graphql_router: Final = GraphQLRouter[Context](
    schema, context_getter=get_context, graphql_ide=graphql_ide
)
