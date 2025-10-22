import pytest
from pytest_mock import MockerFixture
from unittest.mock import MagicMock
from collections import namedtuple

from pokemon_name_translator import PokemonNameTranslator

MockTranslation = namedtuple("MockTranslator", ["translate_text"])
MockTranslatorResponse = namedtuple("MockTranslatorResponse", ["translations"])


@pytest.fixture
def mock_gcp_client(mocker: MockerFixture) -> MagicMock:
    return mocker.MagicMock()


def test_translate_success(mock_gcp_client):
    fake_project_id = "fake-project"

    mock_gcp_client.location_path.return_value = f"projects/{fake_project_id}/locations/global"

    fake_response = MockTranslatorResponse(
        translations=[MockTranslation(translate_text="Pikachu_FR")]
    )
    mock_gcp_client.translate_response.return_value = fake_response

    translator = PokemonNameTranslator(client=mock_gcp_client, project=fake_project_id)

    result = translator.translate("pikachu", target_language="fr")

    assert result == "Pikachu_FR"

    mock_gcp_client.translate_text.assert_called_once_with(
        parent=f"projects/{fake_project_id}/locations/global",
        contents=["pikachu"],
        target_language="fr",
        mime_type="text/plain"
    )

    mock_gcp_client.location_path.assert_called_once_with(fake_project_id, "global")


def test_translate_api_error(mock_gcp_client):
    fake_project_id = "test-project"

    mock_gcp_client.location_path.return_value = f"projects/{fake_project_id}/locations/global"

    mock_gcp_client.translate_response.side_effect = Exception("API Error")

    translator = PokemonNameTranslator(client=mock_gcp_client, project=fake_project_id)

    result = translator.translate("bulbasaur", target_language="fr")

    assert result is None
    mock_gcp_client.translate_response.assert_called_once()
