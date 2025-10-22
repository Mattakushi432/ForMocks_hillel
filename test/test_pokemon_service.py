import pytest
import requests
from pytest_mock import MockerFixture
from typing import Dict, Any

from pokemon_service import PokemonService

FAKE_PIKACHU_DATA: Dict[str, Any] = {
    "name": "pikachu",
    "height": 4,
    "weight": 60,
    "abilities": [
        {"ability": {"name": "static"}},
        {"ability": {"name": "lightning-rod"}}
    ]
}


@pytest.fixture
def pokemon_service() -> PokemonService:
    return PokemonService()


def test_get_pokemon_info_success(mocker: MockerFixture, pokemon_service: PokemonService):
    mack_get = mocker.patch("pokemon_service.requests.get")

    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = FAKE_PIKACHU_DATA
    mack_get.return_value = mock_response

    result = pokemon_service.get_pokemon_info("pikachu")

    assert result == FAKE_PIKACHU_DATA
    mack_get.assert_called_once_with(
        "https://pokeapi.co/api/v2/pokemon/pikachu",
        timeout=10
    )


def test_get_pokemon_info_not_found(mocker: MockerFixture, pokemon_service: PokemonService):
    mack_get = mocker.patch("pokemon_service.requests.get")

    mock_response = mocker.MagicMock()
    mock_response.status_code = 404
    mack_get.return_value = mock_response

    result = pokemon_service.get_pokemon_info("unknown-pokemon")

    assert result is None
    mack_get.assert_called_once()


def test_get_pokemon_info_network_error(mocker: MockerFixture, pokemon_service: PokemonService):
    mock_get = mocker.patch(
        "pokemon_service.requests.get",
        side_effect=requests.exceptions.RequestException("Network error")
    )

    result = pokemon_service.get_pokemon_info("pikachu")

    assert result is None
    mock_get.assert_called_once()


def test_get_pokemon_info_empty_name(mocker: MockerFixture, pokemon_service: PokemonService):
    result = pokemon_service.get_pokemon_info("")
    assert result is None
