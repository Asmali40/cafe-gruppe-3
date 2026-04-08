# ruff: noqa: S101, D103

"""Tests für Queries mit GraphQL."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, graphql_url, login_graphql
from httpx import post
from pytest import mark

GRAPHQL_PATH: Final = "/graphql"


@mark.graphql
@mark.query
def test_query_id() -> None:
    # arrange
    token: Final = login_graphql()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                cafe(cafeId: "20") {
                    version
                    name
                    email
                    kategorie
                    gruendungsdatum
                    kaffeesorten
                    cafeManager {
                        vorname
                        nachname
                    }
                    produkte {
                        name
                        preis
                        waehrung
                    }
                }
            }
        """,
    }

    # act
    response: Final = post(graphql_url, json=query, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    data: Final = response_body["data"]
    assert data is not None
    cafe: Final = data["cafe"]
    assert isinstance(cafe, dict)
    assert response_body.get("errors") is None


@mark.graphql
@mark.query
def test_query_id_notfound() -> None:
    # arrange
    token: Final = login_graphql()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                cafe(cafeId: "999999") {
                    name
                }
            }
        """,
    }

    # act
    response: Final = post(graphql_url, json=query, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    assert response_body["data"]["cafe"] is None
    assert response_body.get("errors") is None


@mark.graphql
@mark.query
def test_query_email() -> None:
    # arrange
    token: Final = login_graphql()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                cafes(suchparameter: {email: "admin@acme.com"}) {
                    id
                    version
                    name
                    email
                    kategorie
                    gruendungsdatum
                    kaffeesorten
                    cafeManager {
                        vorname
                        nachname
                    }
                    produkte {
                        name
                        preis
                        waehrung
                    }
                }
            }
        """,
    }

    # act
    response: Final = post(graphql_url, json=query, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    cafes: Final = response_body["data"]["cafes"]
    assert isinstance(cafes, list)
    assert len(cafes) > 0
    assert response_body.get("errors") is None


@mark.graphql
@mark.query
def test_query_email_notfound() -> None:
    # arrange
    token: Final = login_graphql()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                cafes(suchparameter: {email: "not.found@acme.com"}) {
                    id
                }
            }
        """,
    }

    # act
    response: Final = post(graphql_url, json=query, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    cafes: Final = response_body["data"]["cafes"]
    assert isinstance(cafes, list)
    assert len(cafes) == 0
    assert response_body.get("errors") is None


@mark.graphql
@mark.query
def test_query_name() -> None:
    # arrange
    token: Final = login_graphql()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                cafes(suchparameter: {name: "CafeBerlin"}) {
                    id
                    version
                    name
                    email
                    kategorie
                    gruendungsdatum
                    kaffeesorten
                    cafeManager {
                        vorname
                        nachname
                    }
                    produkte {
                        name
                        preis
                        waehrung
                    }
                }
            }
        """,
    }

    # act
    response: Final = post(graphql_url, json=query, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    cafes: Final = response_body["data"]["cafes"]
    assert isinstance(cafes, list)
    assert len(cafes) > 0
    assert response_body.get("errors") is None


@mark.graphql
@mark.query
def test_query_name_notfound() -> None:
    # arrange
    token: Final = login_graphql()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                cafes(suchparameter: {name: "Nichtvorhanden"}) {
                    id
                }
            }
        """,
    }

    # act
    response: Final = post(graphql_url, json=query, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    cafes: Final = response_body["data"]["cafes"]
    assert isinstance(cafes, list)
    assert len(cafes) == 0
