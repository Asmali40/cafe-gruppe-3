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

"""Tests für Mutations mit GraphQL."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, graphql_url
from httpx import post
from pytest import mark


@mark.graphql
@mark.mutation
def test_create() -> None:
    query: Final = {
        "query": """
            mutation {
                create(
                    cafeInput: {
                        name: "Namegraphql"
                        email: "testgraphql@graphql.de"
                        kategorie: 5
                        gruendungsdatum: "2025-01-01"
                        kaffeesorten: [ESPRESSO]
                        cafeManager: {
                            vorname: "Max"
                            nachname: "Mustermann"
                        }
                        produkte: [
                            {
                                name: "Espresso"
                                preis: "2.50"
                                waehrung: "EUR"
                            }
                        ]
                        username: "testgraphql"
                    }
                ) {
                    id
                }
            }
        """,
    }

    response: Final = post(graphql_url, json=query, verify=ctx)

    assert response is not None
    assert response.status_code == HTTPStatus.OK

    body: Final = response.json()
    assert isinstance(body, dict)
    assert isinstance(body["data"]["create"]["id"], int)
    assert body.get("errors") is None

@mark.graphql
@mark.mutation
def test_create_invalid() -> None:
    query: Final = {
        "query": """
            mutation {
                create(
                    cafeInput: {
                        name: "falscher_nachname"
                        email: "falsche_email@"
                        kategorie: 0
                        gruendungsdatum: "invalid-date"
                        kaffeesorten: [ESPRESSO]
                        cafeManager: {
                            vorname: ""
                            nachname: ""
                        }
                        produkte: [
                            {
                                name: ""
                                preis: "abc"
                                waehrung: "EU"
                            }
                        ]
                    }
                ) {
                    id
                }
            }
        """,
    }

    response: Final = post(graphql_url, json=query, verify=ctx)

    assert response.status_code == HTTPStatus.OK

    body: Final = response.json()
    assert isinstance(body, dict)
    assert body["data"] is None

    errors: Final = body["errors"]
    assert isinstance(errors, list)
    assert len(errors) >= 1
