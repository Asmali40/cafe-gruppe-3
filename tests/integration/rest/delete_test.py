# ruff: noqa: S101, D103
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

"""Tests für DELETE für das Cafe-Projekt."""

from typing import Final

from common_test import ctx, login, rest_url
from httpx import delete
from pytest import mark


@mark.rest
@mark.delete_request
def test_delete_cafe() -> None:
    # arrange
    cafe_id: Final = 60
    token: Final = login()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = delete(
        f"{rest_url}/{cafe_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == 204


@mark.rest
@mark.delete_request
def test_delete_cafe_not_found() -> None:
    # arrange
    cafe_id: Final = 999999
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = delete(
        f"{rest_url}/{cafe_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == 204
