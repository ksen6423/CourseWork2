from src.base_api import OpenSkyAdapter
from views import OpenSkyAPI, JSONStorage, Aircraft


def main():
    api = OpenSkyAPI()
    storage = JSONStorage()
    country = input("Страна: ")
    for state in api.get_aircraft(country):
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
                a = Aircraft(state[0], state[1], state[2], state[6], state[5],
                            state[9] or 0, state[13] or 0)
                storage.save_aircraft(a)
                aircraft.append(a)
            except (ValueError, IndexError):
                continue

        n = int(input("Топ N по высоте: "))
        sorted_aircraft = sorted(aircraft, key=lambda x: x.altitude, reverse=True)[:n]
        for a in sorted_aircraft:
            print(f"{a._callsign} - {a.altitude}м")

if __name__ == "__main__":
    main()

# for plane in filtered_planes:
#     print(plane)
# elif choice == "4":
#     callsign = input("Введите позывной самолета для удаления: ").strip()
#     storage.delete_aeroplane(callsign)
#     print(f"🗑️ Запись о самолете {callsign} удалена, если она существовала.")
# elif choice == "5":
#     print("Завершение работы программы.")
#     break
# else:
#     print("❌ Некорректный выбор. Попробуйте еще раз.")
# if name == "main":
# user_interface()