import pytest
from typing import Dict, Any

from pytest_mock import MockerFixture

from pokemon_report import PokemonReport

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
def report_generator() -> PokemonReport:
    return PokemonReport(pdfkit_config=None)

def test_create_html_pure(report_generator: PokemonReport):
    info = FAKE_PIKACHU_DATA
    translated_name = "Pikachu"

    html = report_generator.create_html_report(info, translated_name)

    assert "<h1>Pokemon Report</h1>" in html
    assert f"<p><strong>Name:</strong> {translated_name}</p>" in html
    assert f"<p><strong>Height:</strong> {info['height']} decimet</p>" in html
    assert f"<p><strong>Weight:</strong> {info['weight']} hectograms</p>" in html
    assert f"<p><strong>Abilities:</strong> static, lightning-rod</p>" in html

def test_generate_report_success(mocker: MockerFixture, report_generator: PokemonReport):
    mock_from_string = mocker.patch("pokemon_report.pdfkit.from_string")

    info = FAKE_PIKACHU_DATA
    translated_name = "Pikachu"
    output_pdf = "test_report.pdf"

    success = report_generator.generate_report(info, translated_name, output_pdf)

    assert success is True

    mock_from_string.assert_called_once()

    call_args = mock_from_string.call_args

    html_content_passed = call_args.args[0]
    output_pdf_passed = call_args.args[1]

    assert output_pdf_passed == output_pdf
    assert f"<p><strong>Name:</strong> {translated_name}</p>" in html_content_passed

    assert "configuration" in call_args.kwargs
    assert call_args.kwargs["configuration"] is None

def test_generate_report_failure(mocker: MockerFixture, report_generator: PokemonReport):
    mock_from_string = mocker.patch(
        "pokemon_report.pdfkit.from_string",
        side_effect=Exception("PDF generation failed")
    )

    success = report_generator.generate_report(FAKE_PIKACHU_DATA, "Pikachu", "test_report.pdf")

    assert success is False

    mock_from_string.assert_called_once()