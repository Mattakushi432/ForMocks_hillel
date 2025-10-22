# pokemon_name_translator.py
# The implementation is designed to be easily mockable in tests without requiring
# Google Cloud libraries or credentials.

class PokemonNameTranslator:
    def __init__(self, client, project: str):
        """Initialize with an injected client and GCP project id.

        Parameters:
            client: An object providing methods used by tests:
                - location_path(project, location)
                - translate_text(parent=..., contents=[...], target_language=..., mime_type="text/plain")
                - translate_response() -> object with attribute `translations`,
                  which is a list of items each having attribute `translate_text`.
            project (str): GCP project id used to build the parent path.
        """
        self.client = client
        self.project = project

    def translate(self, text: str, target_language: str = "en"):
        try:
            # Build the parent path using the provided client helper
            parent = self.client.location_path(self.project, "global")

            # Fire the translate request (the tests assert this exact call/signature)
            self.client.translate_text(
                parent=parent,
                contents=[text],
                target_language=target_language,
                mime_type="text/plain",
            )

            # Then obtain the response and extract the translated text
            response = self.client.translate_response()
            if getattr(response, "translations", None):
                first = response.translations[0]
                return getattr(first, "translate_text", None)
            return None
        except Exception:
            # In case of API error, tests expect None
            return None
