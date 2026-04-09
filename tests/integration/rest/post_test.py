# ruff: noqa: S101, D103
"""Tests für POST."""

from http import HTTPStatus
from re import search
from typing import Final

from common_test import ctx, rest_url
from httpx import post
from pytest import mark


@mark.rest
@mark.post_request
def test_post() -> None:
    # arrange
    neues_cafe: Final = {
        "name": "Testcafe",
        "email": "testrest@rest.de",
        "kategorie": 3,
        "gruendungsdatum": "2022-02-01",
        "kaffeesorten": ["ESPRESSO"],
        "cafe_manager": {"vorname": "Max", "nachname": "Mustermann"},
        "produkte": [{"name": "Espresso", "preis": "2.50", "waehrung": "EUR"}],
        "username": "testrest",
    }
    headers = {"Content-Type": "application/json"}

    # act
    response: Final = post(
        rest_url,
        json=neues_cafe,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.CREATED
    location: Final = response.headers.get("Location")
    assert location is not None
    int_pattern: Final = "[1-9][0-9]*$"
    assert search(int_pattern, location) is not None
    assert not response.text


@mark.rest
@mark.post_request
def test_post_invalid() -> None:
    # arrange
    neues_cafe_invalid: Final = {
        "name": "",
        "email": "falsche_email@",
        "kategorie": 11,
        "gruendungsdatum": "2022-02-01",
        "kaffeesorten": ["ESPRESSO"],
        "cafe_manager": {"vorname": "", "nachname": ""},
        "produkte": [{"name": "", "preis": "abc", "waehrung": "EU"}],
        "username": "testrestinvalid",
    }
    headers = {"Content-Type": "application/json"}

    # act
    response: Final = post(
        rest_url,
        json=neues_cafe_invalid,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@mark.rest
@mark.post_request
def test_post_email_exists() -> None:
    # arrange
    email_exists: Final = "admin@acme.com"
    neues_cafe: Final = {
        "name": "Testcafe",
        "email": email_exists,
        "kategorie": 3,
        "gruendungsdatum": "2022-02-01",
        "kaffeesorten": ["ESPRESSO"],
        "cafe_manager": {"vorname": "Max", "nachname": "Mustermann"},
        "produkte": [{"name": "Espresso", "preis": "2.50", "waehrung": "EUR"}],
        "username": "emailexists",
    }
    headers = {"Content-Type": "application/json"}

    # act
    response: Final = post(
        rest_url,
        json=neues_cafe,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert email_exists in response.text


@mark.rest
@mark.post_request
def test_post_invalid_json() -> None:
    # arrange
    json_invalid: Final = '{"name" "Testcafe"}'
    headers = {"Content-Type": "application/json"}

    # act
    response: Final = post(
        rest_url,
        json=json_invalid,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "should be a valid dictionary" in response.text
