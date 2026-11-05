import os
from abc import ABC, abstractmethod
import requests
import json
from src.aeroplane import Aeroplane


class GeoAPI(ABC):
    @abstractmethod
    def get_coordinates(self, country):
        pass

    @abstractmethod
    def get_aircraft(self, country):
        pass


class OpenSkyAPI(GeoAPI):
    def get_coordinates(self, country):
        r = requests.get(f"https://nominatim.openstreetmap.org/search?q={country}&format=json",
                         headers={"User-Agent": "Test"})
        return r.json()[0] if r.json() else {}

    def get_aircraft(self, country):
        c = self.get_coordinates(country)
        lat, lon = float(c["lat"]), float(c["lon"])
        url = f"https://opensky-network.org/api/states/all?lamin={lat-5}&lomin={lon-5}&lamax={lat+5}&lomax={lon+5}"
        return requests.get(url).json().get("states", [])


class Aircraft:
    def __init__(self,
                 icao24,
                 callsign,
                 country,
                 velocity,
                 altitude
                 ):
        self.icao24 = icao24
        self.callsign = callsign
        self.country = country
        self.velocity = float(velocity)
        self.altitude = float(altitude)
        self._validate()

    def _validate(self):
        if self.velocity < 0 or self.altitude < 0:
            raise ValueError("Negative values")

    def __lt__(self, other):
        return self.velocity < other.velocity

    def __gt__(self, other):
        return self.altitude > other.altitude


class Storage(ABC):
    @abstractmethod
    def add_aircraft(self, aircraft):
        pass

    @abstractmethod
    def get_by_country(self, country):
        pass

    @abstractmethod
    def delete_all(self):
        pass


class JSONStorage(Storage):
    def __init__(self, path="aircraft.json"):
        self.path = path
        if not os.path.exists(self.path) or os.path.getsize(self.path) == 0:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _read_file(self):
        """Вспомогательный метод для безопасного чтения данных."""
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_file(self, data):
        """Вспомогательный метод для записи данных."""
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def add_aircraft(self, a):
        data = self._read_file()

        _aircraft_dict = {
            "callsign": a.callsign,
            "country": a.country,
            "velocity": a.velocity,
            "altitude": a.altitude
        }

        data.append(a.to_dict())
        self._write_file(data)

    def save_aircraft(self, a):
        """Алиас для совместимости"""
        self.add_aircraft(a)

    def get_by_country(self, country):
        data = self._read_file()
        return [Aeroplane(**d) for d in data if d.get("origin_country") == country]

    def delete_aeroplane(self, callsign):
        """Удаление по позывному (поскольку icao24 отсутствует)"""
        data = self._read_file()
        data = [p for p in data if p.get("callsign") != callsign]
        self._write_file(data)

    def delete_all(self):
        with open("storage.json", "w") as f:
            f.write("{}")

    def get_aeroplanes(self, criteria=None):
        """
        Возвращает список самолетов, отфильтрованных по переданным критериям.
        """
        data = self._read_file()  # Читаем данные из файла

        planes = [
            Aeroplane(d["callsign"], d["origin_country"], d["velocity"], d["geo_altitude"])
            for d in data
        ]

        if not criteria:
            return planes

        country_criterion = criteria.get("origin_country") or criteria.get("country")
        if country_criterion:
            target_country = country_criterion.strip().lower()
            return [p for p in planes if p.origin_country.strip().lower() == target_country]

        return planes
