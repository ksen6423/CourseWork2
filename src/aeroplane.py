class Aeroplane:
    def __init__(self, callsign, origin_country, velocity, geo_altitude):
        self.callsign = callsign
        self.origin_country = origin_country
        self.velocity = float(velocity)
        self.geo_altitude = float(geo_altitude)
        self._validate()

    def _validate(self):
        if self.velocity < 0 or self.geo_altitude < 0:
            raise ValueError("Negative values")

    @property
    def country(self):
        return self.origin_country

    @property
    def altitude(self):
        return self.geo_altitude

    def __lt__(self, other):
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.geo_altitude < other.geo_altitude

    def __gt__(self, other):
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.geo_altitude > other.geo_altitude

    def __eq__(self, other):
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.geo_altitude == other.geo_altitude

    def __str__(self):
        return f"Самолет: {self.callsign}"

    def to_dict(self):
        return {
            "callsign": self.callsign,
            "country": self.origin_country,
            "velocity": self.velocity,
            "geo_altitude": self.geo_altitude
        }
