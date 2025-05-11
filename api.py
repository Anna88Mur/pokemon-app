import requests
from requests.exceptions import HTTPError, ConnectionError, RequestException

BASE_URL = "https://pokeapi.co/api/v2/pokemon"


def fetch_data(name_or_id):

    url = f"{BASE_URL}/{name_or_id.lower()}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        return (data)

    except HTTPError as e:
        print(f"Server error: {e}")  # Für Terminal
        if response.status_code == 404:
            return {"error": f"Pokémon '{name_or_id}' ist not gefunden",
                    "error_code": 404,
                    "suggestions": ["Tippfehler überprüfen",
                                    "Probieren Sie Groß-/Kleinschreibung",
                                    "ID statt Name verwenden"]}
        return {"error": f"HTTP Fehler: {str(e)}"}

    except ConnectionError:
        return {"error": "Fehler bei der Verbindung zum Server"}

    except RequestException as e:
        return {"error": f"Fehler bei der Ausführung der Abfrage: {str(e)}"}

    except Exception as e:
        return {"error": f"Unerwartete Fehler: {str(e)}"}


def fetch_species_data(name_or_id):
    url = f"https://pokeapi.co/api/v2/pokemon-species/{name_or_id}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}
