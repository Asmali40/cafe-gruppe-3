"""Repository für persistente Cafe-Daten."""

from collections.abc import Mapping, Sequence
from typing import Final

from loguru import logger
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from cafe.entity import Cafe
from cafe.repository.pageable import Pageable
from cafe.repository.slice import Slice

__all__ = ["CafeRepository"]


class CafeRepository:
    """Repository-Klasse mit CRUD-Methoden für die Entity-Klasse Cafe."""

    def find_by_id(self, cafe_id: int | None, session: Session) -> Cafe | None:
        """Suche mit der Cafe-ID.

        :param cafe_id: ID des gesuchten Cafés
        :param session: Session für SQLAlchemy
        :return: Das gefundene Café oder None
        :rtype: Cafe | None
        """
        logger.debug("cafe_id={}", cafe_id)  # NOSONAR

        if cafe_id is None:
            return None

        statement: Final = (
            select(Cafe)
            .options(joinedload(Cafe.cafe_manager))
            .where(Cafe.id == cafe_id)
        )
        cafe: Final = session.scalar(statement)

        logger.debug("{}", cafe)
        return cafe

    def find(
        self,
        suchparameter: Mapping[str, str],
        pageable: Pageable,
        session: Session,
    ) -> Slice[Cafe]:
        """Suche mit Suchparameter.

        :param suchparameter: Suchparameter als Dictionary
        :param pageable: Anzahl Datensätze und Seitennummer
        :param session: Session für SQLAlchemy
        :return: Ausschnitt der gefundenen Cafés oder leeres Tupel
        :rtype: Slice[Cafe]
        """
        log_str: Final = "{}"
        logger.debug(log_str, suchparameter)
        if not suchparameter:
            return self._find_all(pageable=pageable, session=session)

        # Iteration ueber die Schluessel des Dictionaries mit den Suchparameter
        for key, value in suchparameter.items():
            if key == "email":
                cafe = self._find_by_email(email=value, session=session)
                logger.debug(log_str, cafe)
                return (
                    Slice(content=(cafe,), total_elements=1)
                    if cafe is not None
                    else Slice(content=(), total_elements=0)
                )
            if key == "name":
                cafes = self._find_by_name(
                    teil=value, pageable=pageable, session=session
                )
                logger.debug(log_str, cafes)
                return cafes
        return Slice(content=(), total_elements=0)

    def _find_all(self, pageable: Pageable, session: Session) -> Slice[Cafe]:
        logger.debug("aufgerufen")
        offset = pageable.number * pageable.size
        statement: Final = (
            (
                select(Cafe)
                .options(joinedload(Cafe.cafe_manager))
                .limit(pageable.size)
                .offset(offset)
            )
            if pageable.size != 0
            else (select(Cafe).options(joinedload(Cafe.cafe_manager)))
        )
        cafes: Final = (session.scalars(statement)).all()
        anzahl: Final = self._count_all_rows(session)
        cafe_slice: Final = Slice(content=tuple(cafes), total_elements=anzahl)
        logger.debug("cafe_slice={}", cafe_slice)
        return cafe_slice

    def _count_all_rows(self, session: Session) -> int:
        statement: Final = select(func.count()).select_from(Cafe)
        count: Final = session.execute(statement).scalar()
        return count if count is not None else 0

    def _find_by_email(self, email: str, session: Session) -> Cafe | None:
        """Ein Café anhand der Emailadresse suchen.

        :param email: Emailadresse
        :param session: Session für SQLAlchemy
        :return: Gefundenes Café, falls vorhanden, sonst None
        :rtype: Cafe | None
        """
        logger.debug("email={}", email)  # NOSONAR
        statement: Final = (
            select(Cafe)
            .options(joinedload(Cafe.cafe_manager))
            .where(Cafe.email == email)
        )
        cafe: Final = session.scalar(statement)
        logger.debug("{}", cafe)
        return cafe

    def _find_by_name(
        self,
        teil: str,
        pageable: Pageable,
        session: Session,
    ) -> Slice[Cafe]:
        logger.debug("teil={}", teil)
        offset = pageable.number * pageable.size
        statement: Final = (
            (
                select(Cafe)
                .options(joinedload(Cafe.cafe_manager))
                .filter(Cafe.name.ilike(f"%{teil}%"))
                .limit(pageable.size)
                .offset(offset)
            )
            if pageable.size != 0
            else (
                select(Cafe)
                .options(joinedload(Cafe.cafe_manager))
                .filter(Cafe.name.ilike(f"%{teil}%"))
            )
        )
        cafes: Final = session.scalars(statement).all()
        anzahl: Final = self._count_rows_name(teil, session)
        cafe_slice: Final = Slice(content=tuple(cafes), total_elements=anzahl)
        logger.debug("{}", cafe_slice)
        return cafe_slice

    def _count_rows_name(self, teil: str, session: Session) -> int:
        statement: Final = (
            select(func.count())
            .select_from(Cafe)
            .filter(Cafe.name.ilike(f"%{teil}%"))
        )
        count: Final = session.execute(statement).scalar()
        return count if count is not None else 0

    def exists_email(self, email: str, session: Session) -> bool:
        """Abfrage, ob die Emailadresse bereits vergeben ist.

        :param email: Emailadresse
        :param session: Session für SQLAlchemy
        :return: True, falls die Emailadresse bereits vergeben ist, False sonst
        :rtype: bool
        """
        logger.debug("email={}", email)

        statement: Final = select(func.count()).where(Cafe.email == email)
        anzahl: Final = session.scalar(statement)
        logger.debug("anzahl={}", anzahl)
        return anzahl is not None and anzahl > 0

    def exists_email_other_id(
        self,
        email: str,
        cafe_id: int,
        session: Session,
    ) -> bool:
        """Abfrage, ob die Emailadresse bei einer anderen Cafe-ID bereits vergeben ist.

        :param email: Emailadresse
        :param cafe_id: eigene Cafe-ID
        :param session: Session für SQLAlchemy
        :return: True, falls die Emailadresse bei einer anderen ID existiert, False sonst
        :rtype: bool
        """
        logger.debug("email={}", email)

        statement: Final = select(Cafe.id).where(Cafe.email == email)
        id_db: Final = session.scalar(statement)
        logger.debug("id_db={}", id_db)
        return id_db is not None and id_db != cafe_id

    def create(self, cafe: Cafe, session: Session) -> Cafe:
        """Speichere ein neues Café ab.

        :param cafe: Die Daten des neuen Cafés ohne ID
        :param session: Session für SQLAlchemy
        :return: Das neu angelegte Café mit generierter ID
        :rtype: Cafe
        """
        logger.debug(
            "cafe={}, cafe.cafe_manager={}, cafe.produkte={}",
            cafe,
            cafe.cafe_manager,
            cafe.produkte,
        )
        session.add(instance=cafe)
        # flush(), damit die ID aus der Sequence vor COMMIT fuer Logging verfuegbar ist
        session.flush(objects=[cafe])
        logger.debug("cafe_id={}", cafe.id)
        return cafe

    def update(self, cafe: Cafe, session: Session) -> Cafe | None:
        """Aktualisiere ein Café.

        :param cafe: Die neuen Café-Daten
        :param session: Session für SQLAlchemy
        :return: Das aktualisierte Café oder None, falls kein Café mit der ID existiert
        :rtype: Cafe | None
        """
        logger.debug("{}", cafe)

        if (
            cafe_db := self.find_by_id(cafe_id=cafe.id, session=session)
        ) is None:
            return None

        # session.add(cafe_db) nicht notwendig, da bereits in der Session zugegriffen
        # CAVEAT: Die erhoehte Versionsnummer ist erst *nach* COMMIT sichtbar

        logger.debug("{}", cafe_db)
        return cafe_db

    def delete_by_id(self, cafe_id: int, session: Session) -> None:
        """Lösche die Daten zu einem Café.

        :param cafe_id: Die ID des zu löschenden Cafés
        :param session: Session für SQLAlchemy
        """
        logger.debug("cafe_id={}", cafe_id)

        # "walrus operator"
        if (cafe := self.find_by_id(cafe_id=cafe_id, session=session)) is None:
            return
        session.delete(cafe)
        logger.debug("ok")

    def find_namen(self, teil: str, session: Session) -> Sequence[str]:
        """Suche Café-Namen zu einem Teilstring.

        :param teil: Teilstring zu den gesuchten Namen
        :param session: Session für SQLAlchemy
        :return: Liste der gefundenen Namen oder eine leere Liste
        :rtype: Sequence[str]
        """
        logger.debug("teil={}", teil)

        statement: Final = (
            select(Cafe.name)
            .filter(Cafe.name.ilike(f"%{teil}%"))
            .distinct()
        )
        namen: Final = (session.scalars(statement)).all()

        logger.debug("namen={}", namen)
        return namen
