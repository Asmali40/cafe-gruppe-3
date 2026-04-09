# ruff: noqa: S101, D103, ARG005
# Copyright (C) 2022 - present Juergen Zimmermann, Hochschule Karlsruhe
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

"""Unit-Tests für create() von CafeWriteService."""

from copy import deepcopy
from datetime import date
from typing import TYPE_CHECKING

from pytest import fixture, mark, raises

from cafe.entity import Cafe, CafeManager
from cafe.service import EmailExistsError, UsernameExistsError

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


@fixture
def session_mock(mocker: MockerFixture):
    session = mocker.Mock()
    # Patching von "with Session() as session:" in cafe_write_service.py
    mocker.patch(
        "cafe.service.cafe_write_service.Session",
        return_value=mocker.MagicMock(
            __enter__=lambda self: session,
            __exit__=lambda self, exc_type, exc, tb: None,
        ),
    )
    return session


@mark.unit
@mark.unit_create
def test_create(
    cafe_write_service, session_mock, keycloak_admin_mock, mocker
) -> None:
    # Arrange
    email = "mock@email.test"
    cafe_manager = CafeManager(
        id=999,
        vorname="Max",
        nachname="Mustermann",
        cafe_id=None,
        cafe=None,
    )
    cafe = Cafe(
        id=None,
        email=email,
        name="Mocktest Cafe",
        kategorie=1,
        gruendungsdatum=date(2020, 1, 1),
        kaffeesorten=None,
        username="mocktest",
        cafe_manager=cafe_manager,
        produkte=[],
    )
    cafe_manager.cafe = cafe
    cafe_db_mock = deepcopy(cafe)
    generierte_id = 1
    cafe_db_mock.id = generierte_id
    cafe_db_mock.cafe_manager.id = generierte_id

    # Patch fuer KeycloakAdmin.get_user_id() und KeycloakAdmin.get_users()
    keycloak_admin_mock.get_user_id.return_value = None
    keycloak_admin_mock.get_users.return_value = []

    # session.scalar(select(func.count()).where(Cafe.email == email)
    session_mock.scalar.return_value = 0
    session_mock.add.return_value = None

    def flush_side_effect(objects=None):
        for obj in objects or []:
            obj.id = generierte_id  # Emulation: generierter PK in session.flush()

    session_mock.flush.side_effect = flush_side_effect

    # Patch fuer die Funktion send_mail
    mocker.patch("cafe.service.cafe_write_service.send_mail", return_value=None)

    # Act
    cafe_dto = cafe_write_service.create(cafe=cafe)

    # Assert
    assert cafe_dto.id == generierte_id


@mark.unit
@mark.unit_create
def test_create_username_none(cafe_write_service) -> None:
    # Arrange
    cafe_manager = CafeManager(
        id=999,
        vorname="Max",
        nachname="Mustermann",
        cafe_id=None,
        cafe=None,
    )
    cafe = Cafe(
        id=None,
        email="mock@email.test",
        name="Mocktest Cafe",
        kategorie=1,
        gruendungsdatum=date(2020, 1, 1),
        kaffeesorten=None,
        username=None,
        cafe_manager=cafe_manager,
        produkte=[],
    )
    cafe_manager.cafe = cafe

    # Act
    with raises(ValueError) as err:
        cafe_write_service.create(cafe=cafe)

    # Assert
    assert err.type is ValueError


@mark.unit
@mark.unit_create
def test_create_username_exists(cafe_write_service, keycloak_admin_mock) -> None:
    # Arrange
    email = "mock@email.test"
    cafe_manager = CafeManager(
        id=999,
        vorname="Max",
        nachname="Mustermann",
        cafe_id=None,
        cafe=None,
    )
    cafe = Cafe(
        id=None,
        email=email,
        name="Mocktest Cafe",
        kategorie=1,
        gruendungsdatum=date(2020, 1, 1),
        kaffeesorten=None,
        username="mocktest",
        cafe_manager=cafe_manager,
        produkte=[],
    )
    cafe_manager.cafe = cafe

    # Patch fuer KeycloakAdmin.get_user_id()
    user_id = "12345678-1234-1234-1234-123456789012"
    keycloak_admin_mock.get_user_id.return_value = user_id
    keycloak_admin_mock.get_users.return_value = []

    # Act
    with raises(UsernameExistsError) as err:
        cafe_write_service.create(cafe=cafe)

    # Assert
    assert err.type is UsernameExistsError


@mark.unit
@mark.unit_create
def test_create_email_exists(cafe_write_service, keycloak_admin_mock) -> None:
    # Arrange
    email = "mock@email.test"
    cafe_manager = CafeManager(
        id=999,
        vorname="Max",
        nachname="Mustermann",
        cafe_id=None,
        cafe=None,
    )
    cafe = Cafe(
        id=None,
        email=email,
        name="Mocktest Cafe",
        kategorie=1,
        gruendungsdatum=date(2020, 1, 1),
        kaffeesorten=None,
        username="mocktest",
        cafe_manager=cafe_manager,
        produkte=[],
    )
    cafe_manager.cafe = cafe

    # Patch fuer KeycloakAdmin.get_users()
    keycloak_admin_mock.get_user_id.return_value = None  # sonst UsernameExistsError
    keycloak_admin_mock.get_users.return_value = [
        {"id": "12345678-1234-1234-1234-123456789012", "email": email}
    ]

    # Act
    with raises(EmailExistsError) as err:
        cafe_write_service.create(cafe=cafe)

    # Assert
    assert err.type is EmailExistsError
