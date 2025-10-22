# pokemon_service.py
import requests

class PokemonService:
    BASE_URL = "https://pokeapi.co/api/v2/pokemon"

    def get_pokemon_info(self, pokemon_name):
        if not pokemon_name:
            return None

        url = f"{self.BASE_URL}/{pokemon_name}"
        try:
            response = requests.get(url, timeout=10)
        except requests.exceptions.RequestException:
            return None

        if response.status_code == 200:
            return response.json()
        else:
            return None
