# ruff: noqa: D103, S101
# Copyright (C) 2023 - present Juergen Zimmermann, Hochschule Karlsruhe
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

"""Tests für GET mit Pfadparameter für die ID des Cafés."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, login, rest_url
from httpx import get
from pytest import mark


@mark.rest
@mark.get_request
@mark.parametrize("cafe_id", [30, 1, 20])
def test_get_cafe_by_id_admin(cafe_id: int) -> None:
    # arrange
    token: Final = login()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(
        f"{rest_url}/{cafe_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    id_actual: Final = response_body.get("id")
    assert id_actual is not None
    assert id_actual == cafe_id


@mark.rest
@mark.get_request
@mark.parametrize("cafe_id", [0, 999999])
def test_get_cafe_by_id_not_found(cafe_id: int) -> None:
    # arrange
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(
        f"{rest_url}/{cafe_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NOT_FOUND


@mark.rest
@mark.get_request
def test_get_cafe_by_id_user() -> None:
    # arrange
    cafe_id: Final = 20
    token: Final = login(username="cafeberlin")
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(
        f"{rest_url}/{cafe_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    cafe_id_response: Final = response_body.get("id")
    assert cafe_id_response is not None
    assert cafe_id_response == cafe_id


@mark.rest
@mark.get_request
@mark.parametrize("cafe_id", [1, 30])
def test_get_cafe_by_id_not_allowed(cafe_id: int) -> None:
    # arrange
    token: Final = login(username="cafeberlin")
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(
        f"{rest_url}/{cafe_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.FORBIDDEN


@mark.rest
@mark.get_request
@mark.parametrize("cafe_id", [0, 999999])
def test_get_cafe_by_id_not_allowed_not_found(cafe_id: int) -> None:
    # arrange
    token: Final = login(username="cafeberlin")
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(
        f"{rest_url}/{cafe_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.FORBIDDEN


@mark.rest
@mark.get_request
@mark.parametrize("cafe_id", [30, 1, 20])
def test_get_cafe_by_id_invalid_token(cafe_id: int) -> None:
    # arrange
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}XXX"}

    # act
    response: Final = get(
        f"{rest_url}/{cafe_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@mark.rest
@mark.get_request
@mark.parametrize("cafe_id", [30, 1, 20])
def test_get_cafe_by_id_ohne_token(cafe_id: int) -> None:
    # act
    response: Final = get(f"{rest_url}/{cafe_id}", verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@mark.rest
@mark.get_request
@mark.parametrize("cafe_id,if_none_match", [(20, '"0"'), (30, '"0"')])
def test_get_cafe_by_id_etag(cafe_id: int, if_none_match: str) -> None:
    # arrange
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "If-None-Match": if_none_match,
    }

    # act
    response: Final = get(
        f"{rest_url}/{cafe_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NOT_MODIFIED
    assert not response.text


@mark.rest
@mark.get_request
@mark.parametrize(
    "cafe_id,if_none_match", [(30, 'xxx"'), (1, "xxx"), (20, "xxx")]
)
def test_get_cafe_by_id_etag_invalid(cafe_id: int, if_none_match: str) -> None:
    # arrange
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "If-None-Match": if_none_match,
    }

    # act
    response: Final = get(
        f"{rest_url}/{cafe_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    id_actual: Final = response_body.get("id")
    assert id_actual is not None
    assert id_actual == cafe_id
