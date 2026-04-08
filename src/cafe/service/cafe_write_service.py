"""Geschäftslogik zum Schreiben von Café-Daten."""

from typing import Final

from loguru import logger

from cafe.entity import Cafe
from cafe.repository import CafeRepository, Session
from cafe.security import User, UserService
from cafe.service.cafe_dto import CafeDTO
from cafe.service.exceptions import (
    EmailExistsError,
    NotFoundError,
    UsernameExistsError,
    VersionOutdatedError,
)
from cafe.service.mailer import send_mail

__all__ = ["CafeWriteService"]


class CafeWriteService:
    """Service-Klasse mit Geschäftslogik für Café."""

    def __init__(self, repo: CafeRepository, user_service: UserService) -> None:
        """Konstruktor mit abhängigem CafeRepository und UserService."""
        self.repo: CafeRepository = repo
        self.user_service: UserService = user_service

    def create(self, cafe: Cafe) -> CafeDTO:
        """Ein neues Café anlegen.

        :param cafe: Das neue Café ohne ID
        :return: Das neu angelegte Café mit generierter ID
        :rtype: CafeDTO
        :raises EmailExistsError: Falls die Emailadresse bereits existiert
        :raises UsernameExistsError: Falls der Benutzername bereits existiert
        """
        logger.debug(
            "cafe={}, cafe_manager={}, produkte={}",
            cafe,
            cafe.cafe_manager,
            cafe.produkte,
        )

        username: Final = cafe.username
        if username is None:
            raise ValueError

        if self.user_service.username_exists(username):
            raise UsernameExistsError(username)

        email: Final = cafe.email
        if self.user_service.email_exists(email):
            raise EmailExistsError(email=email)

        user: Final = User(
            username=username,
            email=cafe.email,
            nachname=cafe.name,
            vorname=cafe.name,
            password="p",  # noqa: S106 # NOSONAR
            roles=[],
        )
        user_id = self.user_service.create_user(user)
        logger.debug("user_id={}", user_id)

        # durch "with" erhaelt man einen "Context Manager", der die Ressource/Session
        # am Endes des Blocks schliesst
        with Session() as session:
            if self.repo.exists_email(email=email, session=session):
                raise EmailExistsError(email=email)

            cafe_db: Final = self.repo.create(cafe=cafe, session=session)
            cafe_dto: Final = CafeDTO(cafe_db)
            session.commit()

        # TODO User aus Keycloak loeschen, falls die DB-Transaktion fehlschlaegt

        send_mail(cafe_dto=cafe_dto)
        logger.debug("cafe_dto={}", cafe_dto)
        return cafe_dto

    def update(self, cafe: Cafe, cafe_id: int, version: int) -> CafeDTO:
        """Daten eines Cafés ändern.

        :param cafe: Die neuen Daten
        :param cafe_id: ID des zu aktualisierenden Cafés
        :param version: Version für optimistische Synchronisation
        :return: Das aktualisierte Café
        :rtype: CafeDTO
        :raises NotFoundError: Falls das zu aktualisierende Café nicht existiert
        :raises VersionOutdatedError: Falls die Versionsnummer nicht aktuell ist
        :raises EmailExistsError: Falls die Emailadresse bereits existiert
        """
        logger.debug("cafe_id={}, version={}, {}", cafe_id, version, cafe)

        with Session() as session:
            if (
                cafe_db := self.repo.find_by_id(
                    cafe_id=cafe_id, session=session
                )
            ) is None:
                raise NotFoundError(cafe_id)
            if cafe_db.version > version:
                raise VersionOutdatedError(version)

            email: Final = cafe.email
            if email != cafe_db.email and self.repo.exists_email_other_id(
                cafe_id=cafe_id,
                email=email,
                session=session,
            ):
                raise EmailExistsError(email)

            cafe_db.set(cafe)
            if (
                cafe_updated := self.repo.update(cafe=cafe_db, session=session)
            ) is None:
                raise NotFoundError(cafe_id)
            cafe_dto: Final = CafeDTO(cafe_updated)
            logger.debug("{}", cafe_dto)

            session.commit()
            # CAVEAT: Die erhoehte Versionsnummer ist erst nach COMMIT sichtbar
            cafe_dto.version += 1
            return cafe_dto

    def delete_by_id(self, cafe_id: int) -> None:
        """Ein Café anhand seiner ID löschen.

        :param cafe_id: ID des zu löschenden Cafés
        """
        logger.debug("cafe_id={}", cafe_id)
        with Session() as session:
            self.repo.delete_by_id(cafe_id=cafe_id, session=session)
            session.commit()
