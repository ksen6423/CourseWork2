from abc import ABC, abstractmethod
import requests


class APIAdapter(ABC):
    @abstractmethod
    def get_country_bounds(self, country):
        pass

    @abstractmethod
    def get_aircraft(self, bounds):
        pass


class OpenSkyAdapter(APIAdapter):
    def get_country_bounds(self, country):
        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": country, "format": "json", "limit": 1}
        resp = requests.get(url, params=params, headers={"User-Agent": "StudentBot"})
        if resp.status_code == 200 and resp.json():
            bbox = resp.json()[0]["boundingbox"]
            return {"south": float(bbox[0]), "north": float(bbox[1]),
                    "west": float(bbox[2]), "east": float(bbox[3])}
        return None

    def get_aircraft(self, country_name):
        """
        Запрашивает все самолеты в мире и фильтрует их по указанной стране.
        """
        url = "https://opensky-network.org"

        try:
            resp = requests.get(url, timeout=15)

            if resp.status_code == 200:
                all_states = resp.json().get("states", [])
                if not all_states:
                    return []

                filtered_aircraft = [
                    state for state in all_states
                    if state[2] and state[2].strip().lower() == country_name.strip().lower()
                ]
                return filtered_aircraft

        except Exception as e:
            print(f"Ошибка при запросе или фильтрации: {e}")
        return []
