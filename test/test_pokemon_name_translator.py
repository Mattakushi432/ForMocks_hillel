import pytest
from pytest_mock import MockerFixture
from collections import namedtuple

from pokemon_name_translator import PokemonNameTranslator
from pokemon_service import PokemonService

MockTranslation = namedtuple("MockTranslator", ["translate_text"])
MockTranslatorResponse = namedtuple("MockTranslatorResponse", ["translations"])

@pytest.fixture
def mock_gcp_client(mocker: MockerFixture) -> MockerFixture:
    return mocker.MagicMock()

def test_translate_success(mock_gcp_client, MockerFixture):
    fake_project = "fake-project"

    fake_response = MockTranslatorResponse(
        translations=[MockTranslation(translate_text="Pikachu_FR")]
    )
    mock_gcp_client.translate_response.return_value = fake_response
    mock_gcp_client.translate.return_value = f"projects/{fake_project}/locations/global/translateText"

    translator = PokemonNameTranslator(client=mock_gcp_client, project=fake_project)

    result = translator.translate("pikachu", target_language="fr")

    assert result == "Pikachu_FR"

    mock_gcp_client.translate.assert_called_once_with(
        parent=f"projects/{fake_project}/locations/global",
        contents=["pikachu"],
        target_language="fr",
        mime_type="text/plain"
    )

def test_translate_api_error(mock_gcp_client, MockerFixture):
    fake_project = "test-project"

    mock_gcp_client.translate_response.side_effect = Exception("API Error")

    translator = PokemonNameTranslator(client=mock_gcp_client, project=fake_project)

    result = translator.translate("bulbasaur", target_language="fr")

    assert result is None
    mock_gcp_client.translate_response.assert_called_once()