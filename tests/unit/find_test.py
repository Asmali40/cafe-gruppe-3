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

"""Unit-Tests für find() von CafeService."""

from datetime import date
from typing import TYPE_CHECKING

from pytest import fixture, mark, raises

from cafe.entity import Cafe, CafeManager
from cafe.repository import Pageable
from cafe.service import NotFoundError

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
@mark.unit_find
def test_find_by_name(cafe_service, session_mock) -> None:
    # Arrange
    name = "Mocktest Cafe"
    cafe_id = 1
    cafe_manager_mock = CafeManager(
        id=1,
        vorname="Max",
        nachname="Mustermann",
        cafe_id=cafe_id,
        cafe=None,
    )
    cafe_mock = Cafe(
        id=cafe_id,
        email="mock@email.test",
        name=name,
        kategorie=1,
        gruendungsdatum=date(2020, 1, 1),
        kaffeesorten=None,
        username="mocktest",
        cafe_manager=cafe_manager_mock,
        produkte=[],
    )
    cafe_manager_mock.cafe = cafe_mock
    suchparameter = {"name": name}
    pageable = Pageable(size=5, number=0)
    # session.scalars(select(Cafe)...).all()
    session_mock.scalars.return_value.all.return_value = [cafe_mock]

    # Act
    cafes_slice = cafe_service.find(
        suchparameter=suchparameter, pageable=pageable
    )

    # Assert
    assert len(cafes_slice.content) == 1
    assert cafes_slice.content[0].name == name


@mark.unit
@mark.unit_find
def test_find_by_name_not_found(cafe_service, session_mock) -> None:
    # Arrange
    name = "Notfound"
    suchparameter = {"name": name}
    pageable = Pageable(size=5, number=0)
    # session.scalars(select(Cafe)...).all()
    session_mock.scalars.return_value.all.return_value = []

    # Act
    with raises(NotFoundError) as err:
        cafe_service.find(suchparameter=suchparameter, pageable=pageable)

    # Assert
    assert err.type == NotFoundError
    assert str(err.value) == "Not Found"  # super().__init__("Not Found")
    assert err.value.suchparameter is not None
    assert err.value.suchparameter.get("name") == name  # pyright: ignore[reportOptionalMemberAccess]


@mark.unit
@mark.unit_find
def test_find_by_email(cafe_service, session_mock) -> None:
    # Arrange
    email = "mock@email.test"
    cafe_id = 1
    cafe_manager_mock = CafeManager(
        id=1,
        vorname="Max",
        nachname="Mustermann",
        cafe_id=cafe_id,
        cafe=None,
    )
    cafe_mock = Cafe(
        id=cafe_id,
        email=email,
        name="Mocktest Cafe",
        kategorie=1,
        gruendungsdatum=date(2020, 1, 1),
        kaffeesorten=None,
        username="mocktest",
        cafe_manager=cafe_manager_mock,
        produkte=[],
    )
    cafe_manager_mock.cafe = cafe_mock
    suchparameter = {"email": email}
    pageable = Pageable(size=5, number=0)
    # session.scalar(select(Cafe)...)
    session_mock.scalar.return_value = cafe_mock

    # Act
    cafes_slice = cafe_service.find(
        suchparameter=suchparameter, pageable=pageable
    )

    # Assert
    assert len(cafes_slice.content) == 1
    assert cafes_slice.content[0].email == email


@mark.unit
@mark.unit_find
def test_find_by_email_not_found(cafe_service, session_mock) -> None:
    # Arrange
    email = "not@found.mock"
    suchparameter = {"email": email}
    pageable = Pageable(size=5, number=0)
    # session.scalar(select(Cafe)...)
    session_mock.scalar.return_value = None

    # Act
    with raises(NotFoundError) as err:
        cafe_service.find(suchparameter=suchparameter, pageable=pageable)

    # Assert
    assert str(err.value) == "Not Found"  # super().__init__("Not Found")
    assert err.value.suchparameter is not None
    assert err.value.suchparameter.get("email") == email  # pyright: ignore[reportOptionalMemberAccess]
