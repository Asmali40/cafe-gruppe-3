# ruff: noqa: S101, S106, D103, ARG005
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

"""Unit-Tests für find_by_id() von CafeService."""

from dataclasses import asdict
from datetime import date
from typing import TYPE_CHECKING

from pytest import fixture, mark, raises

from cafe.entity import Cafe, CafeManager
from cafe.security import Role, User
from cafe.service import CafeDTO, CafeService, ForbiddenError, NotFoundError

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


@fixture
def session_mock(mocker: MockerFixture):
    session = mocker.Mock()
    # Patching von "with Session() as session:" in cafe_service.py
    mocker.patch(
        "cafe.service.cafe_service.Session",
        return_value=mocker.MagicMock(
            __enter__=lambda self: session,
            __exit__=lambda self, exc_type, exc, tb: None,
        ),
    )
    return session


@mark.unit
@mark.unit_find_by_id
def test_find_by_id(cafe_service, session_mock) -> None:
    # Arrange
    cafe_id = 1
    username = "mocktest"
    email = "mock@email.test"
    name = "Mocktest Cafe"

    user_mock = User(
        username=username,
        email=email,
        nachname=name,
        vorname=name,
        roles=[Role.ADMIN],
        password="mockpass",
    )
    cafe_manager_mock = CafeManager(
        id=11,
        vorname="Max",
        nachname="Mustermann",
        cafe_id=cafe_id,
        cafe=None,
    )
    cafe_mock = Cafe(
        id=cafe_id,
        email=email,
        name=name,
        kategorie=1,
        gruendungsdatum=date(2020, 1, 1),
        kaffeesorten=None,
        username=username,
        cafe_manager=cafe_manager_mock,
        produkte=[],
    )
    cafe_manager_mock.cafe = cafe_mock
    cafe_dto_mock = CafeDTO(cafe_mock)
    # session.scalar(select(Cafe)...)
    session_mock.scalar.return_value = cafe_mock

    # Act
    cafe_dto = cafe_service.find_by_id(cafe_id=cafe_id, user=user_mock)

    # Assert
    assert asdict(cafe_dto) == asdict(cafe_dto_mock)


@mark.unit
@mark.unit_find_by_id
def test_find_by_id_not_found(cafe_service: CafeService, session_mock) -> None:
    # Arrange
    cafe_id = 999
    user_mock = User(
        username="mocktest",
        email="mock@email.test",
        nachname="Mocktest",
        vorname="Mocktest",
        roles=[Role.ADMIN],
        password="mockpass",
    )
    # session.scalar(select(Cafe)...)
    session_mock.scalar.return_value = None

    # Act
    with raises(NotFoundError) as err:
        cafe_service.find_by_id(cafe_id=cafe_id, user=user_mock)

    # Assert
    assert err.type == NotFoundError
    assert str(err.value) == "Not Found"  # super().__init__("Not Found")
    assert err.value.cafe_id == cafe_id


@mark.unit
@mark.unit_find_by_id
def test_find_by_id_not_found_not_admin(
    cafe_service: CafeService, session_mock
) -> None:
    # Arrange
    cafe_id = 999
    user_mock = User(
        username="mocktest",
        email="mock@email.test",
        nachname="Mocktest",
        vorname="Mocktest",
        roles=[],
        password="mockpass",
    )
    # session.scalar(select(Cafe)...)
    session_mock.scalar.return_value = None

    # Act
    with raises(ForbiddenError) as err:
        cafe_service.find_by_id(cafe_id=cafe_id, user=user_mock)

    # Assert
    assert err.type == ForbiddenError


@mark.unit
@mark.unit_find_by_id
def test_find_by_id_not_admin(cafe_service, session_mock) -> None:
    # Arrange
    cafe_id = 1
    username = "mocktest"
    email = "mock@email.test"
    name = "Mocktest Cafe"

    user_mock = User(
        username=username,
        email=email,
        nachname=name,
        vorname=name,
        roles=[Role.CAFE],
        password="mockpass",
    )
    cafe_manager_mock = CafeManager(
        id=11,
        vorname="Max",
        nachname="Mustermann",
        cafe_id=cafe_id,
        cafe=None,
    )
    cafe_mock = Cafe(
        id=cafe_id,
        email=email,
        name=name,
        kategorie=1,
        gruendungsdatum=date(2020, 1, 1),
        kaffeesorten=None,
        username=username,
        cafe_manager=cafe_manager_mock,
        produkte=[],
    )
    cafe_manager_mock.cafe = cafe_mock
    cafe_dto_mock = CafeDTO(cafe_mock)
    # session.scalar(select(Cafe)...)
    session_mock.scalar.return_value = cafe_mock

    # Act
    cafe_dto = cafe_service.find_by_id(cafe_id=cafe_id, user=user_mock)

    # Assert
    assert asdict(cafe_dto) == asdict(cafe_dto_mock)


@mark.unit
@mark.unit_find_by_id
def test_find_by_id_other(cafe_service, session_mock) -> None:
    # Arrange
    cafe_id = 1
    email = "mock@email.test"
    name = "Mocktest Cafe"

    user_mock = User(
        username="other",
        email=email,
        nachname=name,
        vorname=name,
        roles=[Role.CAFE],
        password="mockpass",
    )
    cafe_manager_mock = CafeManager(
        id=11,
        vorname="Max",
        nachname="Mustermann",
        cafe_id=cafe_id,
        cafe=None,
    )
    cafe_mock = Cafe(
        id=cafe_id,
        email=email,
        name=name,
        kategorie=1,
        gruendungsdatum=date(2020, 1, 1),
        kaffeesorten=None,
        username="mocktest",
        cafe_manager=cafe_manager_mock,
        produkte=[],
    )
    cafe_manager_mock.cafe = cafe_mock
    # session.scalar(select(Cafe)...)
    session_mock.scalar.return_value = cafe_mock

    # Act
    with raises(ForbiddenError) as err:
        cafe_service.find_by_id(cafe_id=cafe_id, user=user_mock)

    # Assert
    assert err.type == ForbiddenError
