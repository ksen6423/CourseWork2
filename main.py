from src.aeroplane import Aeroplane
from src.base_api import OpenSkyAdapter
from src.cli import user_interface
from src.views import OpenSkyAPI, JSONStorage, Aircraft


def main():
    api = OpenSkyAPI()
    storage = JSONStorage()
    country = input("Страна: ")
    for state in (api.get_aircraft(country) or []):
        if state[1]:
            storage.add_aircraft(Aircraft(state[0], state[1], state[2], state[9], state[13]))
    n = int(input("Top N по высоте: "))
    aircraft = storage.get_by_country(country)
    print(sorted(aircraft, key=lambda x: x.altitude, reverse=True)[:n])


if __name__ == "__main__":
    main()


def main():
    adapter = OpenSkyAdapter()
    storage = JSONStorage("aircraft.json")

    country = input("Введите страну: ")
    bounds = adapter.get_country_bounds(country)
    if bounds:
        raw = adapter.get_aircraft(bounds)
        aircraft = []
        for state in raw:
            try:
                a = Aeroplane(
                    state[1],  # callsign
                    state[2],  # origin_country
                    state[9] or 0,  # velocity (скорость)
                    state[13] or 0  # geo_altitude (геометрическая высота)
                )
                storage.add_aircraft(a)
                aircraft.append(a)
            except (ValueError, IndexError):
                continue

        n = int(input("Топ N по высоте: "))
        sorted_aircraft = sorted(aircraft, reverse=True)[:n]
        for a in sorted_aircraft:
            print(f"{a.callsign} - {a.altitude}м")


if __name__ == "__main__":
    try:
        user_interface()
    except KeyboardInterrupt:
        print("\nПрограмма принудительно завершена пользователем. До свидания!")
