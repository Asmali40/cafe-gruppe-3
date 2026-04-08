# ruff: noqa: S101, D103
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

"""Tests für PUT (Cafe)."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, login, rest_url
from httpx import put
from pytest import mark

EMAIL_UPDATE: Final = "updated@cafe.de"


@mark.rest
@mark.put_request
def test_put() -> None:
    # arrange
    cafe_id: Final = 20
    if_match: Final = '"0"'

    geaendertes_cafe: Final = {
        "name": "CafeUpdated",
        "email": EMAIL_UPDATE,
        "kategorie": 9,
        "gruendungsdatum": "2025-01-01",
    }

    token: Final = login()
    assert token is not None

    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": if_match,
    }

    # act
    response: Final = put(
        f"{rest_url}/{cafe_id}",
        json=geaendertes_cafe,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert not response.text


@mark.rest
@mark.put_request
def test_put_invalid() -> None:
    # arrange
    cafe_id: Final = 20

    geaendertes_cafe_invalid: Final = {
        "name": "",
        "email": "invalid@",
        "kategorie": 11,
        "gruendungsdatum": "2025-01-01",
    }

    token: Final = login()
    assert token is not None

    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": '"0"',
    }

    # act
    response: Final = put(
        f"{rest_url}/{cafe_id}",
        json=geaendertes_cafe_invalid,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "name" in response.text
    assert "email" in response.text
    assert "kategorie" in response.text


@mark.rest
@mark.put_request
def test_put_nicht_vorhanden() -> None:
    # arrange
    cafe_id: Final = 999999

    geaendertes_cafe: Final = {
        "name": "CafeUpdated",
        "email": EMAIL_UPDATE,
        "kategorie": 5,
        "gruendungsdatum": "2025-01-01",
    }

    token: Final = login()
    assert token is not None

    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": '"0"',
    }

    # act
    response: Final = put(
        f"{rest_url}/{cafe_id}",
        json=geaendertes_cafe,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NOT_FOUND


@mark.rest
@mark.put_request
def test_put_email_exists() -> None:
    # arrange
    cafe_id: Final = 20
    email_exists: Final = "admin@cafe.com"

    geaendertes_cafe: Final = {
        "name": "CafeUpdated",
        "email": email_exists,
        "kategorie": 5,
        "gruendungsdatum": "2025-01-01",
    }

    token: Final = login()
    assert token is not None

    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": '"0"',
    }

    # act
    response: Final = put(
        f"{rest_url}/{cafe_id}",
        json=geaendertes_cafe,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert email_exists in response.text


@mark.rest
@mark.put_request
def test_put_ohne_versionsnr() -> None:
    # arrange
    cafe_id: Final = 20

    geaendertes_cafe: Final = {
        "name": "CafeUpdated",
        "email": EMAIL_UPDATE,
        "kategorie": 5,
        "gruendungsdatum": "2025-01-01",
    }

    token: Final = login()
    assert token is not None

    headers = {
        "Authorization": f"Bearer {token}",
    }

    # act
    response: Final = put(
        f"{rest_url}/{cafe_id}",
        json=geaendertes_cafe,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.PRECONDITION_REQUIRED


@mark.rest
@mark.put_request
def test_put_alte_versionsnr() -> None:
    # arrange
    cafe_id: Final = 20

    geaendertes_cafe: Final = {
        "name": "CafeUpdated",
        "email": EMAIL_UPDATE,
        "kategorie": 5,
        "gruendungsdatum": "2025-01-01",
    }

    token: Final = login()
    assert token is not None

    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": '"-1"',
    }

    # act
    response: Final = put(
        f"{rest_url}/{cafe_id}",
        json=geaendertes_cafe,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.PRECONDITION_FAILED


@mark.rest
@mark.put_request
def test_put_ungueltige_versionsnr() -> None:
    # arrange
    cafe_id: Final = 20

    geaendertes_cafe: Final = {
        "name": "CafeUpdated",
        "email": EMAIL_UPDATE,
        "kategorie": 5,
        "gruendungsdatum": "2025-01-01",
    }

    token: Final = login()
    assert token is not None

    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": '"xy"',
    }

    # act
    response: Final = put(
        f"{rest_url}/{cafe_id}",
        json=geaendertes_cafe,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.PRECONDITION_FAILED
    assert not response.text


@mark.rest
@mark.put_request
def test_put_versionsnr_ohne_quotes() -> None:
    # arrange
    cafe_id: Final = 20

    geaendertes_cafe: Final = {
        "name": "CafeUpdated",
        "email": EMAIL_UPDATE,
        "kategorie": 5,
        "gruendungsdatum": "2025-01-01",
    }

    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": "0",
    }

    # act
    response: Final = put(
        f"{rest_url}/{cafe_id}",
        json=geaendertes_cafe,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.PRECONDITION_FAILED
