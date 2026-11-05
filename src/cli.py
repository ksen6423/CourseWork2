from src.aeroplane import Aeroplane
from src.base_api import OpenSkyAdapter
from src.views import JSONStorage


def user_interface():
    adapter = OpenSkyAdapter()
    storage = JSONStorage('aircrafts.json')

    print("=== Программа мониторинга воздушного пространства ===")

    while True:
        print("\nДоступные действия:")
        print("1. Запросить самолеты в воздушном пространстве страны и сохранить")
        print("2. Получить ТОП N самолетов по высоте полета (из сохраненных)")
        print("3. Получить самолеты по стране их регистрации (из сохраненных)")
        print("4. Удалить самолет из базы по позывному")
        print("5. Выйти")

        choice = input("\nВыберите пункт меню: ").strip()

        if choice == "1":
            country = input("Введите название страны на английском (например, Canada, France): ").strip()
            print("Получение координат страны...")

            bbox = adapter.get_country_bounds(country)
            if not bbox:
                print("Не удалось найти страну или получить ее координаты.")
                continue

            print(f"Координаты найдены. Запрос самолетов в небе над {country}...")
            states = adapter.get_aircraft(bbox)

            if not states:
                print("В данный момент в воздушном пространстве этой страны нет самолетов.")
                continue

            count = 0
            for state in states:
                if not state or len(state) < 10:
                    continue

                callsign = state[1].strip() if state[1] else "UNKNOWN"
                origin_country = state[2].strip() if state[2] else "UNKNOWN"
                geo_altitude = state[7] if state[7] is not None else 0.0
                velocity = state[9] if state[9] is not None else 0.0

                plane = Aeroplane(
                    callsign=callsign,
                    origin_country=origin_country,
                    velocity=velocity,
                    geo_altitude=geo_altitude
                )
                storage.save_aircraft(plane)
                count += 1
            print(f"Успешно загружено и сохранено самолетов: {count}")

        elif choice == "2":
            try:
                n = int(input("Введите количество самолетов (N): "))
                if n <= 0:
                    print("Пожалуйста, введите число больше 0.")
                    continue
            except ValueError:
                print("Пожалуйста, введите корректное число.")
                continue

            all_planes = storage.get_aeroplanes()
            sorted_planes = sorted(all_planes, reverse=True)

            print(f"\n--- ТОП {n} самолетов по высоте ---")
            for plane in sorted_planes[:n]:
                print(plane)

        elif choice == "3":
            country_origin = input("Введите страну регистрации самолета (например, 'United States'): ").strip()
            filtered_planes = storage.get_aeroplanes(criteria={"origin_country": country_origin})

            print(f"\n--- Самолеты, зарегистрированные в {country_origin} ---")
            if not filtered_planes:
                print("Нет данных.")
            else:
                for plane in filtered_planes:
                    print(plane)

        elif choice == "4":
            callsign_to_delete = input("Введите позывной самолета для удаления: ").strip()
            storage.delete_aeroplane(callsign_to_delete)
            print(f"Запрос на удаление самолета {callsign_to_delete} выполнен.")

        elif choice == '5':
            print("Завершение работы программы.")
            break
        else:
            print("Неверный ввод. Пожалуйста, выберите существующий пункт меню.")
