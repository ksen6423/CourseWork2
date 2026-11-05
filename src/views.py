from abc import ABC, abstractmethod
import requests, json

class GeoAPI(ABC):
    @abstractmethod
    def get_coordinates(self, country): pass
    @abstractmethod
    def get_aircraft(self, country): pass

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
    def __init__(self, icao24, callsign, country, velocity, altitude):
        self.icao24 = icao24; self.callsign = callsign
        self.country = country; self.velocity = float(velocity)
        self.altitude = float(altitude)
        self._validate()

    def _validate(self):
        if self.velocity < 0 or self.altitude < 0: raise ValueError("Negative values")

    def __lt__(self, other): return self.velocity < other.velocity
    def __gt__(self, other): return self.altitude > other.altitude

class Storage(ABC):
    @abstractmethod
    def add_aircraft(self, aircraft): pass
    @abstractmethod
    def get_by_country(self, country): pass
    @abstractmethod
    def delete_all(self): pass

class JSONStorage(Storage):
    def __init__(self, path="aircraft.json"):
        self.path = path
        try: open(self.path, "x")
        except: pass

    def add_aircraft(self, a):
        with open(self.path, "r") as f:
            data = json.load(f) if f.read() else []
        data.append(a.__dict__)
        with open(self.path, "w") as f: json.dump(data, f)

    def get_by_country(self, country):
        with open(self.path) as f: data = json.load(f)
        return [Aircraft(**d) for d in data if d["country"] == country]

    def delete_all(self):
        open(self.path, "w").write("[]")


