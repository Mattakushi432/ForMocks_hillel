# pokemon_report.py
import pdfkit
from typing import Any, Dict


class PokemonReport:
    def __init__(self, pdfkit_config=None) -> None:
        # store pdfkit configuration (can be None and will be passed through)
        self.pdfkit_config = pdfkit_config

    def generate_report(self, pokemon_info: Dict[str, Any], translated_name: str, output_pdf: str) -> bool:
        """Generate a PDF report from provided pokemon info.
        Returns True on success, False if PDF generation fails.
        """
        try:
            html_report = self.create_html_report(pokemon_info, translated_name)
            pdfkit.from_string(html_report, output_pdf, configuration=self.pdfkit_config)
            return True
        except Exception:
            return False

    def create_html_report(self, pokemon_info: Dict[str, Any], translated_name: str) -> str:
        # Format abilities as a comma-separated list
        abilities = ", ".join(ability["ability"]["name"] for ability in pokemon_info["abilities"])

        html = (
            "<!DOCTYPE html>\n"
            "<html>\n"
            "<head>\n"
            "    <title>Pokemon Report</title>\n"
            "</head>\n"
            "<body>\n"
            "    <h1>Pokemon Report</h1>\n"
            f"    <p><strong>Name:</strong> {translated_name}</p>\n"
            f"    <p><strong>Height:</strong> {pokemon_info['height']} decimet</p>\n"
            f"    <p><strong>Weight:</strong> {pokemon_info['weight']} hectograms</p>\n"
            f"    <p><strong>Abilities:</strong> {abilities}</p>\n"
            "</body>\n"
            "</html>\n"
        )
        return html
